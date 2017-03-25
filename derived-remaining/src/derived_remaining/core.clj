(ns derived-remaining.core
  (:require [derived-remaining.reserve :as reserve]
            [derived-remaining.produced :as produced]))

(defn derive-stat
  [{fldName :fldName :as original-data} {recoverable :recoverable original :original produced :produced}]
  (println "doing field" fldName "for" original)
  (let [cumulative-produced (produced/produced-field fldName produced)
        original-value (read-string (get original-data original))
        new-value (- (read-string (get original-data recoverable)) cumulative-produced)]
    (println "recoverable" recoverable " => " (get original-data recoverable))
    (println "cumulative" produced " => " (format "%.2f" cumulative-produced))
    (println "original value" original " => " original-value)
    (println "new value" original " => " (format "%.2f" new-value))
    (cond (< new-value 0)
          (do (println "new values is less than zero, doing nothing.")
              original-data)
          (>= new-value original-value)
          (do
            (println "new values is bigger or equal to original ... doing nothing.")
            original-data)
          :else (do
                  (println "updating value ...")
                  (assoc original-data original (format "%.2f" new-value))))))

(def oil {:recoverable :fldRecoverableOil
          :original    :fldRemainingOil
          :produced    :prfPrdOilNetMillSm3})

(def gas {:recoverable :fldRecoverableGas
          :original    :fldRemainingGas
          :produced    :prfPrdGasNetBillSm3})

(def ngl {:recoverable :fldRecoverableNGL
          :original    :fldRemainingNGL
          :produced    :prfPrdNGLNetMillSm3})

(def condensate {:recoverable :fldRecoverableCondensate
                 :original    :fldRemainingCondensate
                 :produced    :prfPrdCondensateNetMillSm3})

(def oe {:recoverable :fldRecoverableOE
         :original    :fldRemainingOE
         :produced    :prfPrdOeNetMillSm3})

(defn do-field
  [field]
  (let [original-reserve-data (first (filter #(= field (:fldName %)) reserve/data))]
    (reduce derive-stat original-reserve-data [oil gas ngl condensate oe])))

(def fields (map :fldName reserve/data))

(def new-reserves (map do-field fields))

(defn sum-reserves
  [data kind]
  (reduce + 0 (->> data
                   (map kind)
                   (map read-string))))

(def diff (- (sum-reserves reserve/data :fldRemainingOE)
             (sum-reserves new-reserves :fldRemainingOE)))

(println "diff between derived and listed is " (format "%.2f" (* 6.29 diff)) " mboe")