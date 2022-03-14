import { configureStore } from '@reduxjs/toolkit'

import networkReducer from './features/network/networkSlice'
import squeaksReducer from './features/squeaks/squeaksSlice'
import signingProfilesReducer from './features/profiles/signingProfilesSlice'
import contactProfilesReducer from './features/profiles/contactProfilesSlice'
import paymentsReducer from './features/payments/paymentsSlice'
import createSigningProfileReducer from './features/profiles/createSigningProfileSlice'
import importSigningProfileReducer from './features/profiles/importSigningProfileSlice'
import createContactProfileReducer from './features/profiles/createContactProfileSlice'
import profileReducer from './features/profile/profileSlice'

const store = configureStore({
  reducer: {
    // Define a top-level state field named `todos`, handled by `todosReducer`
    network: networkReducer,
    squeaks: squeaksReducer,
    signingProfiles: signingProfilesReducer,
    contactProfiles: contactProfilesReducer,
    createSigningProfile: createSigningProfileReducer,
    importSigningProfile: importSigningProfileReducer,
    createContactProfile: createContactProfileReducer,
    payments: paymentsReducer,
    profile: profileReducer,
  },
})

export default store
