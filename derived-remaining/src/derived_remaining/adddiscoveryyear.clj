(ns derived-remaining.adddiscoveryyear
  (:require [derived-remaining.csvmap :as csvmap]
            [clojure.test :as test]))

(defonce content (slurp "../data/raw_field_overview.csv"))

(def columns (:columns (csvmap/csv-map content)))

(def data (:data (csvmap/csv-map content)))
(defonce discovery-data (:data (csvmap/csv-map (slurp "../data/raw_discovery_overview.csv"))))
(defonce discovery-columns (:columns (csvmap/csv-map (slurp "../data/raw_discovery_overview.csv"))))

(test/is (= columns [:fldName :cmpLongName :fldCurrentActivitySatus :wlbName :wlbCompletionDate :fldMainArea :fldOwnerKind
                     :fldOwnerName :fldMainSupplyBase :fldNpdidOwner :fldNpdidField :wlbNpdidWellbore :cmpNpdidCompany]))

(test/is (= discovery-columns [:dscName
                               :cmpLongName
                               :dscCurrentActivityStatus
                               :dscHcType
                               :wlbName
                               :nmaName
                               :fldName
                               :dscDateFromInclInField
                               :dscDiscoveryYear
                               :dscResInclInDiscoveryName
                               :dscOwnerKind
                               :dscOwnerName
                               :dscNpdidDiscovery
                               :fldNpdidField
                               :wlbNpdidWellbore
                               :dscFactPageUrl
                               :dscFactMapUrl]))

(def bad-data (remove #(= 4 (count (:dscDiscoveryYear %))) discovery-data))
(test/is (= 0 (count bad-data)))

; take the smallest possible value for dscDiscoveryYear ... ...

(defn fldname-to-discoveryyear [[fldname values]]
  [fldname (first (sort-by :dscDiscoveryYear values))])

(def by-field (mapv fldname-to-discoveryyear (group-by :fldName discovery-data)))

(def simplified-resource-overview (sort-by :fldName (mapv second by-field)))

(csvmap/write-csv "../data/raw_discovery_overview_simplified.csv"
                  {:columns discovery-columns
                   :data simplified-resource-overview})

(defn -main
  []
  (println "File created as side effect... ^__^"))

;
;(def fld-to-discoveryyear (reduce (fn [o v] (merge o (fldname-to-discoveryyear v))) {} by-field))
;
;(def new-data (mapv (fn [x] (assoc x :dscDiscoveryYear (get fld-to-discoveryyear (:fldName x)))) data))
;
;(def troublesome (filter #(> (count %) 1) (vals by-field)))

;(def bad-data (filter #(= "" (:wlbCompletionDate %)) data))