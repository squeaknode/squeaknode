import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  client,
  getProfile,
  getProfileByPubkey,
  setProfileFollowing,
} from '../../api/client'

const profileAdapter = createEntityAdapter()

const initialState = {
  currentProfileStatus: 'idle',
  currentProfile: null,
}

// Thunk functions
export const fetchProfile = createAsyncThunk(
  'profile/fetchProfile',
  async (pubkey) => {
    console.log('Fetching profile');
    const response = await getProfileByPubkey(pubkey);
    console.log(response);
    return response.getSqueakProfile();
  }
)

// Use profile id for now. In the future, change RPC to accept pubkey.
export const setFollowProfile = createAsyncThunk(
  'profile/setFollowProfile',
  async (id) => {
    console.log('Following profile');
    await setProfileFollowing(id, true);
    const response = await getProfile(id);
    return response.getSqueakProfile();
  }
)

// Use profile id for now. In the future, change RPC to accept pubkey.
export const setUnfollowProfile = createAsyncThunk(
  'profile/setUnfollowProfile',
  async (id) => {
    console.log('Unfollowing profile');
    await setProfileFollowing(id, false);
    const response = await getProfile(id);
    return response.getSqueakProfile();
  }
)


const profileSlice = createSlice({
  name: 'profile',
  initialState,
  reducers: {
    clearAll(state, action) {
      console.log('Clear profile and other data.');
      state.currentProfileStatus = 'idle';
      state.currentProfile = null;
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchProfile.pending, (state, action) => {
      state.currentProfileStatus = 'loading'
    })
    .addCase(fetchProfile.fulfilled, (state, action) => {
      console.log(action);
      const newProfile = action.payload;
      state.currentProfile = newProfile;
      state.currentProfileStatus = 'idle';
    })
    .addCase(setFollowProfile.fulfilled, (state, action) => {
      console.log(action);
      const newProfile = action.payload;
      // TODO: only update state if the new profile has the same id/pubkey.
      state.currentProfile = newProfile;
      state.currentProfileStatus = 'idle';
    })
    .addCase(setUnfollowProfile.fulfilled, (state, action) => {
      console.log(action);
      const newProfile = action.payload;
      // TODO: only update state if the new profile has the same id/pubkey.
      state.currentProfile = newProfile;
      state.currentProfileStatus = 'idle';
    })
  },
})

export const {
  clearAll,
} = profileSlice.actions

export default profileSlice.reducer

export const selectCurrentProfile = state => state.profile.currentProfile

export const selectCurrentProfileStatus = state => state.profile.currentProfileStatus
