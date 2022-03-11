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

const squeakAdapter = createEntityAdapter()

const initialState = {
  currentSqueakStatus: 'idle',
  currentSqueak: null,
  ancestorSqueaksStatus: 'idle',
  ancestorSqueaks: [],
  replySqueaksStatus: 'idle',
  replySqueaks: [],
}

// Thunk functions
export const fetchSqueak = createAsyncThunk(
  'squeak/fetchSqueak',
  async (squeakHash) => {
    console.log('Fetching squeak');
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)

export const fetchAncestorSqueaks = createAsyncThunk(
  'squeak/fetchAncestorSqueaks',
  async (squeakHash) => {
    console.log('Fetching ancestor squeaks');
    const response = await getAncestorSqueaks(squeakHash);
    return response.getSqueakDisplayEntriesList();
  }
)

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

export const setLikeSqueak = createAsyncThunk(
  'squeak/setLikeSqueak',
  async (squeakHash) => {
    console.log('Liking squeak');
    const response = await likeSqueak(squeakHash);
    return response;
  }
)

export const setUnlikeSqueak = createAsyncThunk(
  'squeak/setUnlikeSqueak',
  async (squeakHash) => {
    console.log('Unliking squeak');
    const response = await unlikeSqueak(squeakHash);
    return response;
  }
)


const squeakSlice = createSlice({
  name: 'squeak',
  initialState,
  reducers: {
    clearAll(state, action) {
      console.log('Clear squeak and other data.');
      state.currentSqueakStatus = 'idle';
      state.currentSqueak = null;
      state.ancestorSqueaksStatus = 'idle';
      state.ancestorSqueaks = []
      state.replySqueaks = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSqueak.pending, (state, action) => {
      state.currentSqueakStatus = 'loading'
    })
    .addCase(fetchSqueak.fulfilled, (state, action) => {
      console.log(action);
      const newSqueak = action.payload;
      state.currentSqueak = newSqueak;
      state.currentSqueakStatus = 'idle';
    })
    .addCase(fetchAncestorSqueaks.pending, (state, action) => {
      state.ancestorSqueaksStatus = 'loading'
    })
    .addCase(fetchAncestorSqueaks.fulfilled, (state, action) => {
      console.log(action);
      const ancestorSqueaks = action.payload;
      state.ancestorSqueaks = ancestorSqueaks;
      state.ancestorSqueaksStatus = 'idle';
    })
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
  clearAll,
} = squeakSlice.actions

export default squeakSlice.reducer

export const selectCurrentSqueak = state => state.squeak.currentSqueak

export const selectAncestorSqueaks = state => state.squeak.ancestorSqueaks

export const selectReplySqueaks = state => state.squeak.replySqueaks
