(ns derived-remaining.reserve
  (:require [clj-http.client :as client]
            [derived-remaining.csvmap :as csvmap]
            [clojure.pprint :as pprint]
            [clojure.test :as test]))

(def field-reserves-url "http://factpages.npd.no/ReportServer?/FactPages/TableView/field_reserves&rs:Command=Render&rc:Toolbar=false&rc:Parameters=f&rs:Format=CSV&Top100=false&IpAddress=80.213.237.130&CultureCode=en")
(defonce field-reserves-raw (-> field-reserves-url client/get :body csvmap/csv-map))

(def columns (:columns field-reserves-raw))
(def data (:data field-reserves-raw))

(test/is (= columns [:fldName
                     :fldRecoverableOil
                     :fldRecoverableGas
                     :fldRecoverableNGL
                     :fldRecoverableCondensate
                     :fldRecoverableOE
                     :fldRemainingOil
                     :fldRemainingGas
                     :fldRemainingNGL
                     :fldRemainingCondensate
                     :fldRemainingOE
                     :fldDateOffResEstDisplay
                     :fldNpdidField
                     :DatesyncNPD]))

(def field-names (map :fldName data))
