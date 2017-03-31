(ns derived-remaining.produced-monthly
  (:require [clj-http.client :as client]
            [clojure.string :as string]
            [clojure.test :as test]
            [derived-remaining.csvmap :as csvmap]
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

(def parsed-data (->> (:data raw-data)
                      (map #(update % :prfYear read-string))
                      (map #(update % :prfMonth read-string))
                      (map #(update % :prfPrdOilNetMillSm3 read-string))
                      (map #(assoc % :days-in-month (. (YearMonth/of (:prfYear %) (:prfMonth %)) lengthOfMonth)))
                      (map #(assoc % :date (str (format "%04d-%02d" (:prfYear %) (:prfMonth %)))))
                      (map #(assoc % :mboed (:prfPrdOilNetMillSm3 %)))
                      (map #(assoc % :mboed (/ (* 6.29 (:mboed %)) (:days-in-month %))))
                      (map #(update % :mboed (fn [x] (format "%.2f" x))))
                      (sort-by :date)
                      vec))

(defn mma [{date :date}]
  (let [items (take-last 12 (filter #(>= (compare date (:date %)) 0) parsed-data))
        production (->> items (map :prfPrdOilNetMillSm3) (reduce + 0))
        days (->> items (map :days-in-month) (reduce + 0))]
    (/ (* 6.29 production) days)))

(def parsed-data-with-mma (->> parsed-data
                               (mapv #(assoc % :mma (mma %)))
                               (mapv #(update % :mma (partial format "%.2f")))))

(csvmap/write-csv "recent-oil-production-monthly.csv" {:columns [:date :mboed :mma] :data    parsed-data-with-mma})
