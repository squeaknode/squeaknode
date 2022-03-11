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
} from '../../api/client'

const squeakAdapter = createEntityAdapter()

const initialState = {
  replySqueaksStatus: 'idle',
  replySqueaks: [],
}

// Thunk functions
export const fetchReplySqueaks = createAsyncThunk(
  'squeak/fetchReplySqueaks',
  async (values) => {
    console.log('Fetching reply squeaks');
    console.log(values.squeakHash);
    console.log(values.limit);
    console.log(values.lastSqueak);
    const response = await getReplySqueaks(
      values.squeakHash,
      values.limit,
      values.lastSqueak,
    );
    return response.getSqueakDisplayEntriesList();
  }
)


const replySqueaksSlice = createSlice({
  name: 'replySqueaks',
  initialState,
  reducers: {
    clearReplies(state, action) {
      console.log('Clear reply squeaks.');
      state.replySqueaksStatus = 'idle';
      state.replySqueaks = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchReplySqueaks.pending, (state, action) => {
      state.replySqueaksStatus = 'loading'
    })
    .addCase(fetchReplySqueaks.fulfilled, (state, action) => {
      console.log(action);
      const replySqueaks = action.payload;
      state.replySqueaks = replySqueaks;
      state.replySqueaksStatus = 'idle';
    })
  },
})

export const {
  clearReplies,
} = replySqueaksSlice.actions

export default replySqueaksSlice.reducer

export const selectReplySqueaks = state => state.replySqueaks.replySqueaks

export const selectAncestorSqueaksStatus = state => state.replySqueaks.replySqueaksStatus
