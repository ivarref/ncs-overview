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

(defonce data (->> raw-data
               :data
               (remove #(= "33/9-6 DELTA" (:prfInformationCarrier %)))
               (map #(update % :prfYear read-string))
               (map #(update % :prfMonth read-string))
               (map #(update % :prfPrdOilNetMillSm3 read-string))
               (map #(update % :prfPrdGasNetBillSm3 read-string))
               (map #(update % :prfPrdOeNetMillSm3 read-string))
               (map #(assoc % :date (str (format "%04d-%02d" (:prfYear %) (:prfMonth %)))))
               ; bootstrap cumulative values
               (map #(assoc % :oil-cumulative (:prfPrdOilNetMillSm3 %)))
               (map #(assoc % :gas-cumulative (:prfPrdGasNetBillSm3 %)))
               (map #(assoc % :oe-cumulative (:prfPrdOeNetMillSm3 %)))
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
    "NA"))

(defn produce-cumulative
  [production]
  {:prf [(coll? production)]}
  (->> (sort-by :date production)
       (reductions (fn [old n] (update n :oil-cumulative (fn [v] (+ v (:oil-cumulative old))))))
       (reductions (fn [old n] (update n :gas-cumulative (fn [v] (+ v (:gas-cumulative old))))))
       (reductions (fn [old n] (update n :oe-cumulative (fn [v] (+ v (:oe-cumulative old))))))
       (mapv #(assoc % :oil-percentage-produced (percentage-produced :oil-cumulative :fldRecoverableOil %)))
       (mapv #(assoc % :gas-percentage-produced (percentage-produced :gas-cumulative :fldRecoverableGas %)))
       (mapv #(assoc % :oe-percentage-produced (percentage-produced :oe-cumulative :fldRecoverableOE %)))))

(defn bucket
  [v]
  (cond (= "NA" v) "NA"
        (< v 50) "<50"
        :else ">50"))

(defonce with-cumulative (mapcat produce-cumulative (vals (group-by :prfInformationCarrier data))))
(defonce flat-production (->> with-cumulative
                          (map #(assoc % :oil-pp-bucket (bucket (:oil-percentage-produced %))))
                          (map #(assoc % :gas-pp-bucket (bucket (:gas-percentage-produced %))))
                          (map #(assoc % :oe-pp-bucket (bucket (:oe-percentage-produced %))))
                          (sort-by :date)
                          vec))

(defn sum-bucket
  [prop [buck values]]
  [buck (reduce + 0 (map prop values))])

(defn bucket-sums-for-date
  [date buck prop]
  {:pre [(some #{buck} [:oil-pp-bucket :gas-pp-bucket :oe-pp-bucket])
         (some #{prop} [:prfPrdOeNetMillSm3 :prfPrdOilNetMillSm3 :prfPrdGasNetBillSm3])]}
  (let [items (filter #(= date (:date %)) flat-production)
        items (remove #(= "NA" (get % buck)) items)
        sum-buckets (map (partial sum-bucket prop) (sort-by first (group-by buck items)))]
    sum-buckets))
