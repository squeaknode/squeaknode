import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/squeak/networkSlice'
import timelineReducer from './features/timeline/timelineSlice'
import squeakReducer from './features/squeak/squeakSlice'
import ancestorSqueaksReducer from './features/squeak/ancestorSqueaksSlice'
import replySqueaksReducer from './features/squeak/replySqueaksSlice'
import makeSqueakReducer from './features/makesqueak/makeSqueakSlice'
import signingProfilesReducer from './features/makesqueak/signingProfilesSlice'
import paymentSummaryReducer from './features/paymentsummary/paymentSummarySlice'
import sentPaymentsReducer from './features/payments/sentPaymentsSlice'
import receivedPaymentsReducer from './features/payments/receivedPaymentsSlice'
import searchReducer from './features/search/searchSlice'

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
    sentPayments: sentPaymentsReducer,
    receivedPayments: receivedPaymentsReducer,
    search: searchReducer,
  },
})

export default store
