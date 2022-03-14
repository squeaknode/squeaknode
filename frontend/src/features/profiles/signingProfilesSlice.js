import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getSigningProfiles } from '../../api/client'

const signingProfilesAdapter = createEntityAdapter()

const initialState = {
  signingProfilesStatus: 'idle',
  signingProfiles: []
}

// Thunk functions
export const fetchSigningProfiles = createAsyncThunk(
  'signingProfiles/fetchSigningProfiles',
  async () => {
    const response = await getSigningProfiles();
    return response.getSqueakProfilesList();
  }
)


const signingProfilesSlice = createSlice({
  name: 'signingProfiles',
  initialState,
  reducers: {
    clearSigningProfiles(state, action) {
      state.signingProfilesStatus = 'idle'
      state.signingProfiles = [];
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
  },
})

export const {
  clearSigningProfiles,
} = signingProfilesSlice.actions

export default signingProfilesSlice.reducer

export const selectSigningProfiles = state => state.signingProfiles.signingProfiles

export const selectSigningProfilesStatus = state => state.signingProfiles.signingProfilesStatus
