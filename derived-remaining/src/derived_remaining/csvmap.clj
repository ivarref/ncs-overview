(ns derived-remaining.csvmap
  (:require [clojure.data.csv :as csv]))

(defn- debomify
  [^String line]
  (let [bom "\uFEFF"]
    (if (.startsWith line bom)
      (.substring line 1)
      line)))

(def sample-csv "hello,world\n123,999\n333,777")

(defn- produce-row
  [columns row]
  (zipmap columns row))

(defn csv-map [^String input]
  (let [csv-raw (csv/read-csv (debomify input))
        columns (mapv keyword (first csv-raw))
        data (filter #(= (count columns) (count %)) (rest csv-raw))]
    {:columns columns
     :data (mapv #(produce-row columns %) data)}))