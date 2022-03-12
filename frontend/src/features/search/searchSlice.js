import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { client, getSearchSqueaks, getSqueak, likeSqueak, unlikeSqueak } from '../../api/client'

const searchAdapter = createEntityAdapter()

const initialState = {
  status: 'idle',
  entities: []
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
      state.entities = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSearch.pending, (state, action) => {
      state.status = 'loading'
    })
    .addCase(fetchSearch.fulfilled, (state, action) => {
      const newEntities = action.payload;
      state.entities = state.entities.concat(newEntities);
      state.status = 'idle'
    })
    .addCase(setLikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.entities.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.entities[currentIndex] = newSqueak;
    })
    .addCase(setUnlikeSqueak.fulfilled, (state, action) => {
      const newSqueak = action.payload;
      const currentIndex = state.entities.findIndex(squeak => squeak.getSqueakHash() === newSqueak.getSqueakHash());
      state.entities[currentIndex] = newSqueak;
    })
  },
})

export const {
  clearSearch,
} = searchSlice.actions

export default searchSlice.reducer

export const selectSearchSqueaks = state => state.search.entities

export const selectLastSearchSqueak = createSelector(
  selectSearchSqueaks,
  squeaks => squeaks.length > 0 && squeaks[squeaks.length - 1]
)

export const selectSearchSqueakIds = createSelector(
  // First, pass one or more "input selector" functions:
  selectSearchSqueaks,
  // Then, an "output selector" that receives all the input results as arguments
  // and returns a final result value
  squeaks => squeaks.map(squeak => squeak.getSqueakHash())
)

export const selectSearchSqueakById = (state, squeakId) => {
  return selectSearchSqueaks(state).find(squeak => squeak.getSqueakHash() === squeakId)
}
