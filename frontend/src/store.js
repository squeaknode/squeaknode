import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/network/networkSlice'
import squeaksReducer from './features/squeaks/squeaksSlice'
import profilesReducer from './features/profiles/profilesSlice'
import paymentsReducer from './features/payments/paymentsSlice'
import profileReducer from './features/profile/profileSlice'

const store = configureStore({
  reducer: {
    network: networkReducer,
    squeaks: squeaksReducer,
    profiles: profilesReducer,
    payments: paymentsReducer,
    profile: profileReducer,
  },
})

export default store
