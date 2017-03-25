(ns derived-remaining.produced
  (:require [clj-http.client :as client]
            [derived-remaining.csvmap :as csvmap]
            [derived-remaining.reserve :as reserve]
            [clojure.test :as test]))

(def field-yearly-produced-url "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_yearly&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.237.130&CultureCode=en")
(defonce field-yearly-produced-raw (-> field-yearly-produced-url client/get :body csvmap/csv-map))

(def columns (:columns field-yearly-produced-raw))
(def data (:data field-yearly-produced-raw))

(test/is (= columns [:prfInformationCarrier
                     :prfYear
                     :prfPrdOilNetMillSm3
                     :prfPrdGasNetBillSm3
                     :prfPrdNGLNetMillSm3
                     :prfPrdCondensateNetMillSm3
                     :prfPrdOeNetMillSm3
                     :prfPrdProducedWaterInFieldMillSm3
                     :prfNpdidInformationCarrier]))

(defn- production-data-of-field
  [field kind]
  (->> data
       (filter #(= field (:prfInformationCarrier %)))
       (mapv kind)
       (remove #(. % startsWith "("))                       ;; remove negative (!) value in MURCHISON ...
       (mapv read-string)))

(defn produced-field
  [field kind]
  {:pre [(some #{field} reserve/field-names)
         (some #{kind} [:prfPrdOilNetMillSm3 :prfPrdGasNetBillSm3 :prfPrdNGLNetMillSm3 :prfPrdCondensateNetMillSm3 :prfPrdOeNetMillSm3])]}
  (let [field-data (production-data-of-field field kind)]
    (reduce + 0.0 field-data)))
