import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  client,
  getSqueak,
  getAncestorSqueaks,
  getReplySqueaks,
  likeSqueak,
  unlikeSqueak,
} from '../../api/client'

const ancestorSqueaksAdapter = createEntityAdapter()

const initialState = {
  ancestorSqueaksStatus: 'idle',
  ancestorSqueaks: [],
}

// Thunk functions
export const fetchAncestorSqueaks = createAsyncThunk(
  'squeak/fetchAncestorSqueaks',
  async (squeakHash) => {
    console.log('Fetching ancestor squeaks');
    const response = await getAncestorSqueaks(squeakHash);
    return response.getSqueakDisplayEntriesList();
  }
)

const ancestorSqueaksSlice = createSlice({
  name: 'ancestorSqueaks',
  initialState,
  reducers: {
    clearAncestors(state, action) {
      console.log('Clear squeak and other data.');
      state.ancestorSqueaksStatus = 'idle';
      state.ancestorSqueaks = []
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchAncestorSqueaks.pending, (state, action) => {
      state.ancestorSqueaksStatus = 'loading'
    })
    .addCase(fetchAncestorSqueaks.fulfilled, (state, action) => {
      console.log(action);
      const ancestorSqueaks = action.payload;
      state.ancestorSqueaks = ancestorSqueaks;
      state.ancestorSqueaksStatus = 'idle';
    })
  },
})

export const {
  clearAncestors,
} = ancestorSqueaksSlice.actions

export default ancestorSqueaksSlice.reducer

export const selectAncestorSqueaks = state => state.ancestorSqueaks.ancestorSqueaks

export const selectAncestorSqueaksStatus = state => state.ancestorSqueaks.ancestorSqueaksStatus
