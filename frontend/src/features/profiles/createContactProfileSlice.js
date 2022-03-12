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
  createContactProfile,
} from '../../api/client'

const createContactProfileAdapter = createEntityAdapter()

const initialState = {
  createContactProfileStatus: 'idle',
}

// Thunk functions
export const setCreateContactProfile = createAsyncThunk(
  'profiles/createContactProfile',
  async (values) => {
    console.log('Creating contact profile');
    let profileName = values.profileName;
    let pubkey = values.pubkey;

    const response = await createContactProfile(profileName, pubkey);
    console.log(response);
    return response.getSqueakHash();
  }
)

const createContactProfileSlice = createSlice({
  name: 'createContactProfile',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(setCreateContactProfile.pending, (state, action) => {
      console.log('setCreateContactProfile pending');
      state.createContactProfileStatus = 'loading'
    })
    .addCase(setCreateContactProfile.fulfilled, (state, action) => {
      console.log('setCreateContactProfile fulfilled');
      console.log(action);
      const newSqueakHash = action.payload;
      state.createContactProfileStatus = 'idle';
      console.log('Go to new profile');
    })
  },
})

export const {
  clearAll,
} = createContactProfileSlice.actions

export default createContactProfileSlice.reducer

export const selectCreateContactProfileStatus = state => state.createContactProfile.createContactProfileStatus
