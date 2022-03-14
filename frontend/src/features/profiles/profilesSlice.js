import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  getSigningProfiles,
  getContactProfiles,
  createContactProfile,
  createSigningProfile,
  importSigningProfile,
} from '../../api/client'

const profilesAdapter = createEntityAdapter()

const initialState = {
  signingProfilesStatus: 'idle',
  signingProfiles: [],
  contactProfilesStatus: 'idle',
  contactProfiles: [],
  createContactProfileStatus: 'idle',
  createSigningProfileStatus: 'idle',
  importSigningProfileStatus: 'idle',
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
    .addCase(setCreateSigningProfile.pending, (state, action) => {
      console.log('setCreateSigningProfile pending');
      state.createSigningProfileStatus = 'loading'
    })
    .addCase(setCreateSigningProfile.fulfilled, (state, action) => {
      console.log('setCreateSigningProfile fulfilled');
      console.log(action);
      const newSqueakHash = action.payload;
      state.createSigningProfileStatus = 'idle';
      console.log('Go to new profile');
    })
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
  clearSigningProfiles,
  clearContactProfiles,
} = profilesSlice.actions

export default profilesSlice.reducer

export const selectSigningProfiles = state => state.profiles.signingProfiles

export const selectSigningProfilesStatus = state => state.profiles.signingProfilesStatus

export const selectContactProfiles = state => state.profiles.contactProfiles

export const selectContactProfilesStatus = state => state.profiles.contactProfilesStatus

export const selectCreateContactProfileStatus = state => state.createContactProfile.createContactProfileStatus

export const selectCreateSigningProfileStatus = state => state.createSigningProfile.createSigningProfileStatus

export const selectImportSigningProfileStatus = state => state.importSigningProfile.importSigningProfileStatus
