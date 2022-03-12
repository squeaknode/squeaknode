import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  client,
  getSqueak,
  getReplySqueaks,
  likeSqueak,
  unlikeSqueak,
  getSigningProfiles,
} from '../../api/client'

const signingProfilesAdapter = createEntityAdapter()

const initialState = {
  signingProfiles: [],
}

// Thunk functions
export const fetchSigningProfiles = createAsyncThunk(
  'signingProfiles/fetchSigningProfiles',
  async (squeakHash) => {
    console.log('Fetching signing profiles');
    const response = await getSigningProfiles();
    return response.getSqueakProfilesList();
  }
)

const signingProfilesSlice = createSlice({
  name: 'signingProfiles',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(fetchSigningProfiles.fulfilled, (state, action) => {
      console.log(action);
      const signingProfiles = action.payload;
      state.signingProfiles = signingProfiles;
    })
  },
})

// export const {
//   clearAll,
// } = signingProfilesSlice.actions

export default signingProfilesSlice.reducer

export const selectSigningProfiles = state => state.signingProfiles.signingProfiles
