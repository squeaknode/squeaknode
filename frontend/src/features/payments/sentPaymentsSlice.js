import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getSentPayments } from '../../api/client'

const sentPaymentsAdapter = createEntityAdapter()

const initialState = {
  status: 'idle',
  sentPayments: []
}

// Thunk functions
export const fetchSentPayments = createAsyncThunk(
  'sentPayments/fetchSentPayments',
  async (lastSentPayment) => {
    console.log('Fetching sentPayments');
    const response = await getSentPayments(5, lastSentPayment);
    console.log(response);
    return response.getSentPaymentsList();
  }
)


const sentPaymentsSlice = createSlice({
  name: 'sentPayments',
  initialState,
  reducers: {
    clearSentPayments(state, action) {
      console.log('Clear sentPayments reducer.');
      state.status = 'idle'
      state.sentPayments = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSentPayments.pending, (state, action) => {
      state.status = 'loading'
    })
    .addCase(fetchSentPayments.fulfilled, (state, action) => {
      console.log('Add case');
      console.log(action);
      const newSentPayments = action.payload;
      state.sentPayments = state.sentPayments.concat(newSentPayments);
      state.status = 'idle'
    })
  },
})

export const {
  clearSentPayments,
} = sentPaymentsSlice.actions

export default sentPaymentsSlice.reducer

export const selectSentPayments = state => state.sentPayments.sentPayments

export const selectLastSentPaymentsSqueak = createSelector(
  selectSentPayments,
  sentPayments => sentPayments.length > 0 && sentPayments[sentPayments.length - 1]
)

export const selectSentPaymentsStatus = state => state.sentPayments.status
