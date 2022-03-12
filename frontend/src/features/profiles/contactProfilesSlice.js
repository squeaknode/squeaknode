import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getContactProfiles } from '../../api/client'

const contactProfilesAdapter = createEntityAdapter()

const initialState = {
  status: 'idle',
  contactProfiles: []
}

// Thunk functions
export const fetchContactProfiles = createAsyncThunk(
  'contactProfiles/fetchContactProfiles',
  async () => {
    const response = await getContactProfiles();
    return response.getSqueakProfilesList();
  }
)


const contactProfilesSlice = createSlice({
  name: 'contactProfiles',
  initialState,
  reducers: {
    clearContactProfiles(state, action) {
      state.status = 'idle'
      state.contactProfiles = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchContactProfiles.pending, (state, action) => {
      state.status = 'loading'
    })
    .addCase(fetchContactProfiles.fulfilled, (state, action) => {
      const newContactProfiles = action.payload;
      state.contactProfiles = newContactProfiles;
      state.status = 'idle'
    })
  },
})

export const {
  clearContactProfiles,
} = contactProfilesSlice.actions

export default contactProfilesSlice.reducer

export const selectContactProfiles = state => state.contactProfiles.contactProfiles

export const selectContactProfilesStatus = state => state.contactProfiles.status
