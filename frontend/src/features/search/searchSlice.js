import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { client, getSearchSqueaks, getSqueak, likeSqueak, unlikeSqueak } from '../../api/client'

const searchAdapter = createEntityAdapter()

const initialState = {
  searchSqueaksStatus: 'idle',
  searchSqueaks: []
}

// Thunk functions
export const fetchSearch = createAsyncThunk(
  'search/fetchSearch',
  async (values) => {
    const response = await getSearchSqueaks(
      values.searchText,
      values.limit,
      values.lastSqueak,
    );
    return response.getSqueakDisplayEntriesList();
  }
)

export const setLikeSqueak = createAsyncThunk(
  'search/setLikeSqueak',
  async (squeakHash) => {
    await likeSqueak(squeakHash);
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)

export const setUnlikeSqueak = createAsyncThunk(
  'search/setUnlikeSqueak',
  async (squeakHash) => {
    await unlikeSqueak(squeakHash);
    const response = await getSqueak(squeakHash);
    return response.getSqueakDisplayEntry();
  }
)



const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    clearSearch(state, action) {
      state.searchSqueaks = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSearch.pending, (state, action) => {
      state.searchSqueaksStatus = 'loading'
    })
    .addCase(fetchSearch.fulfilled, (state, action) => {
      const newEntities = action.payload;
      state.searchSqueaks = state.searchSqueaks.concat(newEntities);
      state.searchSqueaksStatus = 'idle'
    })
    .addCase(setLikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.searchSqueaks.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.searchSqueaks[currentIndex] = newSqueak;
    })
    .addCase(setUnlikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.searchSqueaks.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.searchSqueaks[currentIndex] = newSqueak;
    })
  },
})

export const {
  clearSearch,
} = searchSlice.actions

export default searchSlice.reducer

export const selectSearchSqueaks = state => state.search.searchSqueaks

export const selectSearchSqueaksStatus = state => state.search.searchSqueaksStatus

export const selectLastSearchSqueak = createSelector(
  selectSearchSqueaks,
  squeaks => squeaks.length > 0 && squeaks[squeaks.length - 1]
)
