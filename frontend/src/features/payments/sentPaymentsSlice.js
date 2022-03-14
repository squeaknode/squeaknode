import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getSentPayments } from '../../api/client'

const sentPaymentsAdapter = createEntityAdapter()

const initialState = {
  sentPaymentsStatus: 'idle',
  sentPayments: []
}

// Thunk functions
export const fetchSentPayments = createAsyncThunk(
  'sentPayments/fetchSentPayments',
  async (lastSentPayment) => {
    const response = await getSentPayments(5, lastSentPayment);
    return response.getSentPaymentsList();
  }
)


const sentPaymentsSlice = createSlice({
  name: 'sentPayments',
  initialState,
  reducers: {
    clearSentPayments(state, action) {
      state.sentPaymentsStatus = 'idle'
      state.sentPayments = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchSentPayments.pending, (state, action) => {
      state.sentPaymentsStatus = 'loading'
    })
    .addCase(fetchSentPayments.fulfilled, (state, action) => {
      const newSentPayments = action.payload;
      state.sentPayments = state.sentPayments.concat(newSentPayments);
      state.sentPaymentsStatus = 'idle'
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

export const selectSentPaymentsStatus = state => state.sentPayments.sentPaymentsStatus
