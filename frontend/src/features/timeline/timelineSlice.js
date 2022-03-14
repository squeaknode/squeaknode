import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { client, getTimelineSqueaks, getSqueak, likeSqueak, unlikeSqueak } from '../../api/client'

const timelineAdapter = createEntityAdapter()

const initialState = {
  timelineSqueaksStatus: 'idle',
  timelineSqueaks: []
}

// Thunk functions
export const fetchTimeline = createAsyncThunk(
  'timeline/fetchTimeline',
  async (lastSqueak) => {
    const response = await getTimelineSqueaks(5, lastSqueak);
    return response.getSqueakDisplayEntriesList();
  }
)

export const setLikeSqueak = createAsyncThunk(
  'timeline/setLikeSqueak',
  async (squeakHash) => {
    await likeSqueak(squeakHash);
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)

export const setUnlikeSqueak = createAsyncThunk(
  'timeline/setUnlikeSqueak',
  async (squeakHash) => {
    await unlikeSqueak(squeakHash);
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)



const timelineSlice = createSlice({
  name: 'timeline',
  initialState,
  reducers: {
    clearTimeline(state, action) {
      state.timelineSqueaks = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchTimeline.pending, (state, action) => {
      state.timelineSqueaksStatus = 'loading'
    })
    .addCase(fetchTimeline.fulfilled, (state, action) => {
      const newEntities = action.payload;
      state.timelineSqueaks = state.timelineSqueaks.concat(newEntities);
      state.timelineSqueaksStatus = 'idle'
    })
    .addCase(setLikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.timelineSqueaks.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.timelineSqueaks[currentIndex] = newSqueak;
    })
    .addCase(setUnlikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.timelineSqueaks.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.timelineSqueaks[currentIndex] = newSqueak;
    })
  },
})

export const {
  clearTimeline,
} = timelineSlice.actions

export default timelineSlice.reducer

export const selectTimelineSqueaks = state => state.timeline.timelineSqueaks

export const selectTimelineSqueaksStatus = state => state.timeline.timelineSqueaksStatus

export const selectLastTimelineSqueak = createSelector(
  selectTimelineSqueaks,
  squeaks => squeaks.length > 0 && squeaks[squeaks.length - 1]
)

export const selectTimelineSqueakIds = createSelector(
  // First, pass one or more "input selector" functions:
  selectTimelineSqueaks,
  // Then, an "output selector" that receives all the input results as arguments
  // and returns a final result value
  squeaks => squeaks.map(squeak => squeak.getSqueakHash())
)

export const selectTimelineSqueakById = (state, squeakId) => {
  return selectTimelineSqueaks(state).find(squeak => squeak.getSqueakHash() === squeakId)
}
