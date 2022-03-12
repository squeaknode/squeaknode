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
  makeSqueak,
} from '../../api/client'

const makeSqueakAdapter = createEntityAdapter()

const initialState = {
  makeSqueakStatus: 'idle',
}

// Thunk functions
export const setMakeSqueak = createAsyncThunk(
  'squeak/makeSqueak',
  async (values) => {
    console.log('Making squeak');
    let profileId = values.signingProfile;
    let content = values.description;
    let replyTo = values.replyTo;
    let hasRecipient = values.hasRecipient;
    let recipientProfileId = values.recipientProfileId;

    const response = await makeSqueak(
      profileId,
      content,
      replyTo,
      hasRecipient,
      recipientProfileId,
    );
    return response.getSqueakHash();
  }
)

const makeSqueakSlice = createSlice({
  name: 'makeSqueak',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(setMakeSqueak.pending, (state, action) => {
      console.log('setMakeSqueak pending');
      state.makeSqueakStatus = 'loading'
    })
    .addCase(setMakeSqueak.fulfilled, (state, action) => {
      console.log('setMakeSqueak fulfilled');
      console.log(action);
      const newSqueakHash = action.payload;
      state.makeSqueakStatus = 'idle';
      console.log('Go to new squeak');
    })
  },
})

export const {
  clearAll,
} = makeSqueakSlice.actions

export default makeSqueakSlice.reducer

export const selectMakeSqueakStatus = state => state.makeSqueak.makeSqueakStatus
