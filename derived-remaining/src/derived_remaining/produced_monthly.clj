(ns derived-remaining.produced-monthly
  (:require [clj-http.client :as client]
            [clojure.string :as string]
            [derived-remaining.csvmap :as csvmap]))

; field-monthly-produced (all fields)
(def url "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_production_totalt_NCS_month__DisplayAllRows&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.237.130&CultureCode=en")
(defonce raw-data (-> url client/get :body csvmap/csv-map))

(def last-year-data (->> (:data raw-data)
                         (filter #(= "2016" (:prfYear %)))
                         (map #(update % :prfMonth read-string))
                         (map #(update % :prfPrdOeNetMillSm3 read-string))
                         (sort-by :prfMonth)
                         (map :prfPrdOeNetMillSm3)
                         vec))

(def mx (apply max last-year-data))
(def relative-data (mapv #(* 60 (/ % mx)) last-year-data))

(dorun (map #(println (string/join "" (repeat % "*"))) relative-data))
