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
  getAncestorSqueaks,
  getReplySqueaks,
  getTimelineSqueaks,
} from '../../api/client'

const squeakAdapter = createEntityAdapter()

const initialState = {
  currentSqueakStatus: 'idle',
  currentSqueak: null,
  ancestorSqueaksStatus: 'idle',
  ancestorSqueaks: [],
  replySqueaksStatus: 'idle',
  replySqueaks: [],
  timelineSqueaksStatus: 'idle',
  timelineSqueaks: []
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

export const setLikeSqueak = createAsyncThunk(
  'squeak/setLikeSqueak',
  async (squeakHash) => {
    console.log('Liking squeak');
    await likeSqueak(squeakHash);
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)

export const setUnlikeSqueak = createAsyncThunk(
  'squeak/setUnlikeSqueak',
  async (squeakHash) => {
    console.log('Unliking squeak');
    await unlikeSqueak(squeakHash);
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

export const fetchTimeline = createAsyncThunk(
  'squeak/fetchTimeline',
  async (lastSqueak) => {
    const response = await getTimelineSqueaks(5, lastSqueak);
    return response.getSqueakDisplayEntriesList();
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
    },
    clearAncestors(state, action) {
      console.log('Clear squeak and other data.');
      state.ancestorSqueaksStatus = 'idle';
      state.ancestorSqueaks = []
    },
    clearReplies(state, action) {
      console.log('Clear reply squeaks.');
      state.replySqueaksStatus = 'idle';
      state.replySqueaks = [];
    },
    clearTimeline(state, action) {
      state.timelineSqueaks = [];
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
    .addCase(setLikeSqueak.fulfilled, (state, action) => {
      console.log(action);
      const newSqueak = action.payload;
      // TODO: only update state if the new squeak has the same id/hash.
      state.currentSqueak = newSqueak;
      state.currentSqueakStatus = 'idle';
    })
    .addCase(setUnlikeSqueak.fulfilled, (state, action) => {
      console.log(action);
      const newSqueak = action.payload;
      // TODO: only update state if the new squeak has the same id/hash.
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
    .addCase(fetchTimeline.pending, (state, action) => {
      state.timelineSqueaksStatus = 'loading'
    })
    .addCase(fetchTimeline.fulfilled, (state, action) => {
      const newEntities = action.payload;
      state.timelineSqueaks = state.timelineSqueaks.concat(newEntities);
      state.timelineSqueaksStatus = 'idle'
    })
  },
})

export const {
  clearAll,
  clearAncestors,
  clearReplies,
  clearTimeline,
} = squeakSlice.actions

export default squeakSlice.reducer

export const selectCurrentSqueak = state => state.squeak.currentSqueak

export const selectCurrentSqueakStatus = state => state.squeak.currentSqueakStatus

export const selectAncestorSqueaks = state => state.squeak.ancestorSqueaks

export const selectAncestorSqueaksStatus = state => state.squeak.ancestorSqueaksStatus

export const selectReplySqueaks = state => state.squeak.replySqueaks

export const selectReplySqueaksStatus = state => state.squeak.replySqueaksStatus

export const selectTimelineSqueaks = state => state.squeak.timelineSqueaks

export const selectTimelineSqueaksStatus = state => state.squeak.timelineSqueaksStatus

export const selectLastTimelineSqueak = createSelector(
  selectTimelineSqueaks,
  squeaks => squeaks.length > 0 && squeaks[squeaks.length - 1]
)
