import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/network/networkSlice'
import timelineReducer from './features/timeline/timelineSlice'
import squeakReducer from './features/squeak/squeakSlice'
import ancestorSqueaksReducer from './features/squeak/ancestorSqueaksSlice'
import replySqueaksReducer from './features/squeak/replySqueaksSlice'
import makeSqueakReducer from './features/makesqueak/makeSqueakSlice'
import signingProfilesReducer from './features/profiles/signingProfilesSlice'
import contactProfilesReducer from './features/profiles/contactProfilesSlice'
import paymentSummaryReducer from './features/paymentsummary/paymentSummarySlice'
import sentPaymentsReducer from './features/payments/sentPaymentsSlice'
import receivedPaymentsReducer from './features/payments/receivedPaymentsSlice'
import searchReducer from './features/search/searchSlice'
import createSigningProfileReducer from './features/profiles/createSigningProfileSlice'
import importSigningProfileReducer from './features/profiles/importSigningProfileSlice'
import createContactProfileReducer from './features/profiles/createContactProfileSlice'
import profileReducer from './features/profile/profileSlice'

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
    contactProfiles: contactProfilesReducer,
    createSigningProfile: createSigningProfileReducer,
    importSigningProfile: importSigningProfileReducer,
    createContactProfile: createContactProfileReducer,
    paymentSummary: paymentSummaryReducer,
    sentPayments: sentPaymentsReducer,
    receivedPayments: receivedPaymentsReducer,
    search: searchReducer,
    profile: profileReducer,
  },
})

export default store
