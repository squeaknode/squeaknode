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
} from '../../api/client'

const squeakAdapter = createEntityAdapter()

const initialState = {
  currentSqueakStatus: 'idle',
  currentSqueak: null,
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


const squeakSlice = createSlice({
  name: 'squeak',
  initialState,
  reducers: {
    clearAll(state, action) {
      console.log('Clear squeak and other data.');
      state.currentSqueakStatus = 'idle';
      state.currentSqueak = null;
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
      state.currentSqueak = newSqueak;
      state.currentSqueakStatus = 'idle';
    })
    .addCase(setUnlikeSqueak.fulfilled, (state, action) => {
      console.log(action);
      const newSqueak = action.payload;
      state.currentSqueak = newSqueak;
      state.currentSqueakStatus = 'idle';
    })
  },
})

export const {
  clearAll,
} = squeakSlice.actions

export default squeakSlice.reducer

export const selectCurrentSqueak = state => state.squeak.currentSqueak

export const selectCurrentSqueakStatus = state => state.squeak.currentSqueakStatus
