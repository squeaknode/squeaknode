import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/network/networkSlice'
import squeaksReducer from './features/squeaks/squeaksSlice'
import profilesReducer from './features/profiles/profilesSlice'
import peersReducer from './features/peers/peersSlice'
import externalAddressReducer from './features/externalAddress/externalAddressSlice'
import paymentsReducer from './features/payments/paymentsSlice'
import sellPriceReducer from './features/sellPrice/sellPriceSlice'

const store = configureStore({
  reducer: {
    network: networkReducer,
    squeaks: squeaksReducer,
    profiles: profilesReducer,
    peers: peersReducer,
    externalAddress: externalAddressReducer,
    payments: paymentsReducer,
    sellPrice: sellPriceReducer,
  },
})

export default store
