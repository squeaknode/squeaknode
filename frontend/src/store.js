import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/squeak/networkSlice'
import timelineReducer from './features/timeline/timelineSlice'
import squeakReducer from './features/squeak/squeakSlice'
import ancestorSqueaksReducer from './features/squeak/ancestorSqueaksSlice'
import replySqueaksReducer from './features/squeak/replySqueaksSlice'
import makeSqueakReducer from './features/makesqueak/makeSqueakSlice'
import signingProfilesReducer from './features/makesqueak/signingProfilesSlice'
import paymentSummaryReducer from './features/paymentsummary/paymentSummarySlice'

const store = configureStore({
  reducer: {
    // Define a top-level state field named `todos`, handled by `todosReducer`
    network: networkReducer,
    timeline: timelineReducer,
    squeak: squeakReducer,
    ancestorSqueaks: ancestorSqueaksReducer,
    replySqueaks: replySqueaksReducer,
    makeSqueak: makeSqueakReducer,
    signingProfiles: signingProfilesReducer,
    paymentSummary: paymentSummaryReducer,
  },
})

export default store
