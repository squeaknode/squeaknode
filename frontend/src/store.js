import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/network/networkSlice'
import squeaksReducer from './features/squeaks/squeaksSlice'
import profilesReducer from './features/profiles/profilesSlice'
import peersReducer from './features/peers/peersSlice'
import paymentsReducer from './features/payments/paymentsSlice'

const store = configureStore({
  reducer: {
    network: networkReducer,
    squeaks: squeaksReducer,
    profiles: profilesReducer,
    peers: peersReducer,
    payments: paymentsReducer,
  },
})

export default store
