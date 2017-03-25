(ns derived-remaining.props)

(def oil {:recoverable :fldRecoverableOil
          :remaining   :fldRemainingOil
          :produced    :prfPrdOilNetMillSm3})

(def gas {:recoverable :fldRecoverableGas
          :remaining   :fldRemainingGas
          :produced    :prfPrdGasNetBillSm3})

(def ngl {:recoverable :fldRecoverableNGL
          :remaining   :fldRemainingNGL
          :produced    :prfPrdNGLNetMillSm3})

(def condensate {:recoverable :fldRecoverableCondensate
                 :remaining   :fldRemainingCondensate
                 :produced    :prfPrdCondensateNetMillSm3})

(def oe {:recoverable :fldRecoverableOE
         :remaining   :fldRemainingOE
         :produced    :prfPrdOeNetMillSm3})

(def all [oil gas ngl condensate oe])