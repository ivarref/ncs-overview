(ns derived-remaining.produced-field-monthly
  (:require [clj-http.client :as client]
            [clojure.string :as string]
            [clojure.test :as test]
            [derived-remaining.csvmap :as csvmap]
            [clojure.pprint :as pprint]
            [derived-remaining.reserve :as reserve])
  (:import (java.time YearMonth)))

(def field-monthly-production-url "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_monthly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.237.130&CultureCode=en")
(defonce raw-data (-> field-monthly-production-url client/get :body csvmap/csv-map))

(test/is (= (:columns raw-data) [:prfInformationCarrier
                                 :prfYear
                                 :prfMonth
                                 :prfPrdOilNetMillSm3
                                 :prfPrdGasNetBillSm3
                                 :prfPrdNGLNetMillSm3
                                 :prfPrdCondensateNetMillSm3
                                 :prfPrdOeNetMillSm3
                                 :prfPrdProducedWaterInFieldMillSm3
                                 :prfNpdidInformationCarrier]))

(def data (->> raw-data
               :data
               (remove #(= "33/9-6 DELTA" (:prfInformationCarrier %)))
               (map #(update % :prfYear read-string))
               (map #(update % :prfMonth read-string))
               (map #(update % :prfPrdOilNetMillSm3 read-string))
               (map #(update % :prfPrdGasNetBillSm3 read-string))
               (map #(update % :prfPrdOeNetMillSm3 read-string))
               (map #(assoc % :date (str (format "%04d-%02d" (:prfYear %) (:prfMonth %)))))
               (map #(assoc % :days-in-month (. (YearMonth/of (:prfYear %) (:prfMonth %)) lengthOfMonth)))
               ; bootstrap cumulative values
               (map #(assoc % :oil-cumulative (:prfPrdOilNetMillSm3 %)))
               (map #(assoc % :gas-cumulative (:prfPrdGasNetBillSm3 %)))
               (map #(assoc % :oe-cumulative (:prfPrdOeNetMillSm3 %)))
               ; bootstrap start production year
               (map #(assoc % :start-production (:prfYear %)))
               ; fetch original recoverable reserves
               (map #(assoc % :fldRecoverableOil (reserve/get-reserve (:prfInformationCarrier %) :fldRecoverableOil)))
               (map #(assoc % :fldRecoverableGas (reserve/get-reserve (:prfInformationCarrier %) :fldRecoverableGas)))
               (map #(assoc % :fldRecoverableOE (reserve/get-reserve (:prfInformationCarrier %) :fldRecoverableOE)))
               ; remove unused values
               (map #(dissoc % :prfPrdNGLNetMillSm3))
               (map #(dissoc % :prfPrdCondensateNetMillSm3))
               (map #(dissoc % :prfPrdProducedWaterInFieldMillSm3))
               (map #(dissoc % :prfNpdidInformationCarrier))
               (sort-by :date)
               vec))

(defn percentage-produced
  [production reserve item]
  (if (> (get item reserve) 0)
    (* 100 (/ (get item production) (get item reserve)))
    -1.0))

(defn produce-cumulative
  [production]
  {:pre [(coll? production)]}
  (->> (sort-by :date production)
       (reductions (fn [old n] (assoc n :start-production (:start-production old))))
       (reductions (fn [old n] (update n :oil-cumulative (fn [v] (+ v (:oil-cumulative old))))))
       (reductions (fn [old n] (update n :gas-cumulative (fn [v] (+ v (:gas-cumulative old))))))
       (reductions (fn [old n] (update n :oe-cumulative (fn [v] (+ v (:oe-cumulative old))))))
       (mapv #(assoc % :oil-percentage-produced (percentage-produced :oil-cumulative :fldRecoverableOil %)))
       (mapv #(assoc % :gas-percentage-produced (percentage-produced :gas-cumulative :fldRecoverableGas %)))
       (mapv #(assoc % :oe-percentage-produced (percentage-produced :oe-cumulative :fldRecoverableOE %)))))

(def with-cumulative (mapcat produce-cumulative (vals (group-by :prfInformationCarrier data))))

(defn process-date
  [empty-buckets production]
  {:pre [(coll? production)]}
  (let [buckets (group-by :bucket production)
        days-in-month (:days-in-month (first production))
        mboe (fn [x] (format "%.2f" (/ (* 6.29 x) days-in-month)))
        oil-buckets (map #(mboe (reduce + 0.0 (map :prfPrdOilNetMillSm3 %))) (vals buckets))
        ;gas-buckets (map #(mboe (reduce + 0.0 (map :prfPrdGasNetBillSm3 %))) (vals buckets))
        ;oe-buckets (map #(mboe (reduce + 0.0 (map :prfPrdOeNetMillSm3 %))) (vals buckets))
        ]
    (merge {:date          (:date (first production))
            :days-in-month days-in-month
            :total         (reduce + 0 (map :prfPrdOilNetMillSm3 production))
            :mboed         (mboe (reduce + 0 (map :prfPrdOilNetMillSm3 production)))}
           (merge empty-buckets (zipmap (keys buckets) oil-buckets)))))

;(str (subs (str (:oil-percentage-produced %)) 0 1) "0")
#_(cond (< (:oil-percentage-produced %) 80) "1-0 - 80% produced"
        :else "2-80 - 100% produced")

(defn mma [prod {date :date}]
  (let [items (take-last 12 (filter #(>= (compare date (:date %)) 0) prod))
        production (->> items (map :total) (reduce + 0))
        days (->> items (map :days-in-month) (reduce + 0))]
    (format "%.2f" (/ (* 6.29 production) days))))

(defn generate-bucket-file
  [filename data bucket-fn]
  (let [with-bucket (->> data (mapv #(assoc % :bucket (bucket-fn %))))
        empty-buckets (reduce (fn [o n] (assoc o n "0.00")) {} (distinct (map :bucket with-bucket)))
        flat-production (->> with-bucket
                             (group-by :date)
                             vals
                             (map (partial process-date empty-buckets))
                             (sort-by :date))
        with-mma (->> flat-production
                      (map #(assoc % :mma (mma flat-production %)))
                      (map #(dissoc % :days-in-month))
                      (map #(dissoc % :total)))]
    (csvmap/write-csv filename
                      {:columns (cons :date (cons :mma (keys empty-buckets)))
                       :data    with-mma})
    (println "wrote" filename)))

(generate-bucket-file "../data/oil-production-bucket-stacked.csv"
                      with-cumulative
                      #(cond
                         (< (:oil-percentage-produced %) 50) "1-0 - 50% produsert"
                         (< (:oil-percentage-produced %) 60) "1-50 - 60% produsert"
                         (< (:oil-percentage-produced %) 70) "3-60 - 70% produsert"
                         (< (:oil-percentage-produced %) 80) "4-70 - 80% produsert"
                         (< (:oil-percentage-produced %) 90) "5-80 - 90% produsert"
                         :else "6-90 - 100% produsert"))


(generate-bucket-file "../data/oil-production-bucket-stacked-old-fields.csv"
                      (filter #(< (:start-production %) 2002) with-cumulative)
                      #(cond
                         (< (:oil-percentage-produced %) 50) "1-0 - 50% produsert"
                         (< (:oil-percentage-produced %) 60) "1-50 - 60% produsert"
                         (< (:oil-percentage-produced %) 70) "3-60 - 70% produsert"
                         (< (:oil-percentage-produced %) 80) "4-70 - 80% produsert"
                         (< (:oil-percentage-produced %) 90) "5-80 - 90% produsert"
                         :else "6-90 - 100% produsert"))


(generate-bucket-file "../data/oil-production-bucket-stacked-new-fields.csv"
                      (remove #(< (:start-production %) 2002) with-cumulative)
                      #(cond
                         (< (:oil-percentage-produced %) 50) "1-0 - 50% produsert"
                         (< (:oil-percentage-produced %) 60) "1-50 - 60% produsert"
                         (< (:oil-percentage-produced %) 70) "3-60 - 70% produsert"
                         (< (:oil-percentage-produced %) 80) "4-70 - 80% produsert"
                         (< (:oil-percentage-produced %) 90) "5-80 - 90% produsert"
                         :else "6-90 - 100% produsert"))


#_(generate-bucket-file "../data/oil-production-bucket-stacked-new-fields.csv"
                      (filter #(>= (:start-production %) 2008) with-cumulative)
                      #(cond
                         (< (:oil-percentage-produced %) 50) "1-0 - 50% produsert"
                         (< (:oil-percentage-produced %) 60) "1-50 - 60% produsert"
                         (< (:oil-percentage-produced %) 70) "3-60 - 70% produsert"
                         (< (:oil-percentage-produced %) 80) "4-70 - 80% produsert"
                         (< (:oil-percentage-produced %) 90) "5-80 - 90% produsert"
                         :else "6-90 - 100% produsert"))

(defn -main
  []
  (println "File created as side effect... ^__^"))

