import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  logout,
} from '../../api/client'

const initialState = {
  userName: null,
}

// Thunk functions
export const setLogout = createAsyncThunk(
  'account/setLogout',
  async () => {
    console.log('Logging out');
    await logout();
    return null;
  }
)

const accountSlice = createSlice({
  name: 'account',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(setLogout.fulfilled, (state, action) => {
      console.log(action);
      // Reload page to show logged out page.
      window.location.replace('/')
    })
  },
})

export default accountSlice.reducer

export const selectUsername = state => state.account.userName
