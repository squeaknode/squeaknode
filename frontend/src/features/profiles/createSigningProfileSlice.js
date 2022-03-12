import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  client,
  getSqueak,
  likeSqueak,
  unlikeSqueak,
  createSigningProfile,
} from '../../api/client'

const createSigningProfileAdapter = createEntityAdapter()

const initialState = {
  createSigningProfileStatus: 'idle',
}

// Thunk functions
export const setCreateSigningProfile = createAsyncThunk(
  'profiles/createSigningProfile',
  async (values) => {
    console.log('Creating signing profile');
    let profileName = values.profileName;

    const response = await createSigningProfile(profileName);
    console.log(response);
    return response.getSqueakHash();
  }
)

const createSigningProfileSlice = createSlice({
  name: 'createSigningProfile',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(setCreateSigningProfile.pending, (state, action) => {
      console.log('setCreateSigningProfile pending');
      state.createSigningProfileStatus = 'loading'
    })
    .addCase(setCreateSigningProfile.fulfilled, (state, action) => {
      console.log('setCreateSigningProfile fulfilled');
      console.log(action);
      const newSqueakHash = action.payload;
      state.createSigningProfileStatus = 'idle';
      console.log('Go to new squeak');
    })
  },
})

export const {
  clearAll,
} = createSigningProfileSlice.actions

export default createSigningProfileSlice.reducer

export const selectCreateSigningProfileStatus = state => state.createSigningProfile.createSigningProfileStatus
