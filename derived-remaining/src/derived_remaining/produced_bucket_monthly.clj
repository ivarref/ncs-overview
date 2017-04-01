(ns derived-remaining.produced-bucket-monthly
  (:require [clj-http.client :as client]
            [clojure.string :as string]
            [clojure.test :as test]
            [derived-remaining.csvmap :as csvmap]
            [derived-remaining.produced-field-monthly :as produced-field-monthly]
            [clojure.pprint :as pprint])
  (:import [java.time.YearMonth]
           (java.time YearMonth)))

; field-monthly-produced (all fields)
(def url "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_totalt_NCS_month__DisplayAllRows&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.237.130&CultureCode=en")
(defonce raw-data (-> url client/get :body csvmap/csv-map))

(test/is (= (:columns raw-data) [:prfYear
                                 :prfMonth
                                 :prfPrdOilNetMillSm3
                                 :prfPrdGasNetBillSm3
                                 :prfPrdNGLNetMillSm3
                                 :prfPrdCondensateNetMillSm3
                                 :prfPrdOeNetMillSm3
                                 :prfPrdProducedWaterInFieldMillSm3]))

(defn mboed-prop [new-prop prop row]
  (assoc row new-prop (format "%.2f" (/ (* 6.29 (get row prop)) (:days-in-month row)))))

(def parsed-data (->> (:data raw-data)
                      (map #(update % :prfYear read-string))
                      (map #(update % :prfMonth read-string))
                      (map #(update % :prfPrdOilNetMillSm3 read-string))
                      (map #(update % :prfPrdGasNetBillSm3 read-string))
                      (map #(update % :prfPrdOeNetMillSm3 read-string))
                      (map #(assoc % :days-in-month (. (YearMonth/of (:prfYear %) (:prfMonth %)) lengthOfMonth)))
                      (map #(assoc % :date (str (format "%04d-%02d" (:prfYear %) (:prfMonth %)))))
                      (map (partial mboed-prop :oil-mboed :prfPrdOilNetMillSm3))
                      (map (partial mboed-prop :gas-mboed :prfPrdGasNetBillSm3))
                      (map (partial mboed-prop :oe-mboed :prfPrdOeNetMillSm3))
                      (map #(assoc % :oil-bucket (produced-field-monthly/bucket-sums-for-date (:date %) :oil-pp-bucket :prfPrdOilNetMillSm3)))
                      ;(map #(assoc % :oil-less-than-half-produced (-> % :oil-bucket (nth 0) (nth 1))))
                      ;(map #(assoc % :oil-more-than-half-produced (-> % :oil-bucket (nth 1) (nth 1))))
                      (sort-by :date)
                      vec))

#_(defn mma [prop {date :date}]
  (let [items (take-last 12 (filter #(>= (compare date (:date %)) 0) parsed-data))
        production (->> items (map prop) (reduce + 0))
        days (->> items (map :days-in-month) (reduce + 0))]
    (format "%.2f" (/ (* 6.29 production) days))))

#_(def parsed-data-with-mma (->> parsed-data
                               (mapv #(assoc % :oil-mma (mma :prfPrdOilNetMillSm3 %)))
                               (mapv #(assoc % :gas-mma (mma :prfPrdGasNetBillSm3 %)))
                               (mapv #(assoc % :oe-mma (mma :prfPrdOeNetMillSm3 %)))))

#_(csvmap/write-csv "recent-oil-production-bucket-monthly.csv" {:columns [:date :mboed :mma]
                                                       :data    (->> parsed-data-with-mma
                                                                     (mapv #(assoc % :mma (:oil-mma %)))
                                                                     (mapv #(assoc % :mboed (:oil-mboed %))))})

#_(csvmap/write-csv "recent-gas-production-monthly.csv" {:columns [:date :mboed :mma]
                                                       :data    (->> parsed-data-with-mma
                                                                     (mapv #(assoc % :mma (:gas-mma %)))
                                                                     (mapv #(assoc % :mboed (:gas-mboed %))))})

#_(csvmap/write-csv "recent-oe-production-monthly.csv" {:columns [:date :mboed :mma]
                                                      :data    (->> parsed-data-with-mma
                                                                    (mapv #(assoc % :mma (:oe-mma %)))
                                                                    (mapv #(assoc % :mboed (:oe-mboed %))))})
