import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  getSigningProfiles,
  getContactProfiles,
} from '../../api/client'

const profilesAdapter = createEntityAdapter()

const initialState = {
  signingProfilesStatus: 'idle',
  signingProfiles: [],
  contactProfilesStatus: 'idle',
  contactProfiles: [],
}

// Thunk functions
export const fetchSigningProfiles = createAsyncThunk(
  'profiles/fetchSigningProfiles',
  async () => {
    const response = await getSigningProfiles();
    return response.getSqueakProfilesList();
  }
)

export const fetchContactProfiles = createAsyncThunk(
  'profiles/fetchContactProfiles',
  async () => {
    const response = await getContactProfiles();
    return response.getSqueakProfilesList();
  }
)


const profilesSlice = createSlice({
  name: 'profiles',
  initialState,
  reducers: {
    clearSigningProfiles(state, action) {
      state.signingProfilesStatus = 'idle'
      state.signingProfiles = [];
    },
    clearContactProfiles(state, action) {
      state.contactProfilesStatus = 'idle'
      state.contactProfiles = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSigningProfiles.pending, (state, action) => {
      state.signingProfilesStatus = 'loading'
    })
    .addCase(fetchSigningProfiles.fulfilled, (state, action) => {
      const newSigningProfiles = action.payload;
      state.signingProfiles = newSigningProfiles;
      state.signingProfilesStatus = 'idle'
    })
    .addCase(fetchContactProfiles.pending, (state, action) => {
      state.contactProfilesStatus = 'loading'
    })
    .addCase(fetchContactProfiles.fulfilled, (state, action) => {
      const newContactProfiles = action.payload;
      state.contactProfiles = newContactProfiles;
      state.contactProfilesStatus = 'idle'
    })
  },
})

export const {
  clearSigningProfiles,
  clearContactProfiles,
} = profilesSlice.actions

export default profilesSlice.reducer

export const selectSigningProfiles = state => state.profiles.signingProfiles

export const selectSigningProfilesStatus = state => state.profiles.signingProfilesStatus

export const selectContactProfiles = state => state.profiles.contactProfiles

export const selectContactProfilesStatus = state => state.profiles.contactProfilesStatus
