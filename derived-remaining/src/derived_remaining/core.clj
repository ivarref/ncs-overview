(ns derived-remaining.core
  (:require [derived-remaining.reserve :as reserve]
            [derived-remaining.produced :as produced]
            [derived-remaining.props :as props]))

(defn derive-remaining
  [{fldName :fldName :as original-data} {recoverable :recoverable remaining :remaining produced :produced}]
  (println "doing field" fldName "for" remaining)
  (let [cumulative-produced (produced/produced-field fldName produced)
        original-value (read-string (get original-data remaining))
        new-value (- (read-string (get original-data recoverable)) cumulative-produced)]
    (println "recoverable" recoverable " => " (get original-data recoverable))
    (println "cumulative" produced " => " (format "%.2f" cumulative-produced))
    (println "remaining value" remaining " => " original-value)
    (println "new value" remaining " => " (format "%.2f" new-value))
    (cond (< new-value 0)
          (do (println "new values is less than zero, doing nothing.")
              original-data)
          (>= new-value original-value)
          (do
            (println "new values is bigger or equal to remaining ... doing nothing.")
            original-data)
          :else (do
                  (println "updating value ...")
                  (assoc original-data remaining (format "%.2f" new-value))))))

(defn derive-field-remaining
  [field]
  (let [original-reserve-data (first (filter #(= field (:fldName %)) reserve/data))]
    (reduce derive-remaining original-reserve-data props/all)))

(def fields (map :fldName reserve/data))

(def new-reserves (map derive-field-remaining fields))

(defn sum-reserves
  [data kind]
  (reduce + 0 (->> data
                   (map kind)
                   (map read-string))))

(def diff (- (sum-reserves reserve/data :fldRemainingOE)
             (sum-reserves new-reserves :fldRemainingOE)))

(println "diff between listed and derived is " (format "%.2f" (* 6.29 diff)) " mboe")