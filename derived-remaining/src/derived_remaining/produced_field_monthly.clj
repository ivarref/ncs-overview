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
  [[field production]]
  {:prf [(coll? production)]}
  [field (->> production
              (reductions (fn [old n] (update n :oil-cumulative (fn [v] (+ v (:oil-cumulative old))))))
              (reductions (fn [old n] (update n :gas-cumulative (fn [v] (+ v (:gas-cumulative old))))))
              (reductions (fn [old n] (update n :oe-cumulative (fn [v] (+ v (:oe-cumulative old))))))
              (mapv #(assoc % :oil-percentage-produced (percentage-produced :oil-cumulative :fldRecoverableOil %)))
              (mapv #(assoc % :gas-percentage-produced (percentage-produced :gas-cumulative :fldRecoverableGas %)))
              (mapv #(assoc % :oe-percentage-produced (percentage-produced :oe-cumulative :fldRecoverableOE %))))])

(def fields (distinct (map :prfInformationCarrier data)))

(def with-cumulative (map produce-cumulative (group-by :prfInformationCarrier data)))

(def flat-production (->> (mapcat second with-cumulative)
                          (sort-by :date)
                          vec))

;(def field (produce-cumulative (get by-field "TROLL")))

#_(csvmap/write-csv "field-production-monthly.csv" {:columns [:date :prfInformationCarrier :prfPrdOilNetMillSm3] :data data})
