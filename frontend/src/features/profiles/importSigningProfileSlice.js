import {
  createSlice,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  client,
  getSqueak,
  likeSqueak,
  unlikeSqueak,
  importSigningProfile,
} from '../../api/client'

const importSigningProfileAdapter = createEntityAdapter()

const initialState = {
  importSigningProfileStatus: 'idle',
}

// Thunk functions
export const setImportSigningProfile = createAsyncThunk(
  'profiles/importSigningProfile',
  async (values) => {
    console.log('Importing signing profile');
    let profileName = values.profileName;
    let privateKey = values.privateKey;

    const response = await importSigningProfile(profileName, privateKey);
    console.log(response);
    return response.getSqueakHash();
  }
)

const importSigningProfileSlice = createSlice({
  name: 'importSigningProfile',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(setImportSigningProfile.pending, (state, action) => {
      console.log('setImportSigningProfile pending');
      state.importSigningProfileStatus = 'loading'
    })
    .addCase(setImportSigningProfile.fulfilled, (state, action) => {
      console.log('setImportSigningProfile fulfilled');
      console.log(action);
      const newSqueakHash = action.payload;
      state.importSigningProfileStatus = 'idle';
      console.log('Go to new profile');
    })
  },
})

export const {
  clearAll,
} = importSigningProfileSlice.actions

export default importSigningProfileSlice.reducer

export const selectImportSigningProfileStatus = state => state.importSigningProfile.importSigningProfileStatus
