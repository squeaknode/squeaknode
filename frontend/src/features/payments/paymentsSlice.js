import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  getSentPayments,
  getReceivedPayments,
  getPaymentSummary,
} from '../../api/client'

const initialState = {
  sentPaymentsStatus: 'idle',
  sentPayments: [],
  receivedPaymentsStatus: 'idle',
  receivedPayments: [],
  paymentSummary: null,
}

// Thunk functions
export const fetchSentPayments = createAsyncThunk(
  'payments/fetchSentPayments',
  async (lastSentPayment) => {
    const response = await getSentPayments(5, lastSentPayment);
    return response.getSentPaymentsList();
  }
)

export const fetchReceivedPayments = createAsyncThunk(
  'payments/fetchReceivedPayments',
  async (lastReceivedPayment) => {
    const response = await getReceivedPayments(5, lastReceivedPayment);
    return response.getReceivedPaymentsList();
  }
)

export const fetchPaymentSummary = createAsyncThunk(
  'payments/fetchPaymentSummary',
  async () => {
    console.log('Fetching paymentSummary');
    const response = await getPaymentSummary();
    return response.getPaymentSummary();
  }
)


const paymentsSlice = createSlice({
  name: 'sentPayments',
  initialState,
  reducers: {
    clearSentPayments(state, action) {
      state.sentPaymentsStatus = 'idle'
      state.sentPayments = [];
    },
    clearReceivedPayments(state, action) {
      state.receivedPaymentsStatus = 'idle'
      state.receivedPayments = [];
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
    .addCase(fetchReceivedPayments.pending, (state, action) => {
      state.receivedPaymentsStatus = 'loading'
    })
    .addCase(fetchReceivedPayments.fulfilled, (state, action) => {
      const newReceivedPayments = action.payload;
      state.receivedPayments = state.receivedPayments.concat(newReceivedPayments);
      state.receivedPaymentsStatus = 'idle'
    })
    .addCase(fetchPaymentSummary.fulfilled, (state, action) => {
      const paymentSummary = action.payload;
      state.paymentSummary = paymentSummary;
    })
  },
})

export const {
  clearSentPayments,
  clearReceivedPayments,
} = paymentsSlice.actions

export default paymentsSlice.reducer

export const selectSentPayments = state => state.payments.sentPayments

export const selectLastSentPaymentsSqueak = createSelector(
  selectSentPayments,
  sentPayments => sentPayments.length > 0 && sentPayments[sentPayments.length - 1]
)

export const selectSentPaymentsStatus = state => state.payments.sentPaymentsStatus

export const selectReceivedPayments = state => state.payments.receivedPayments

export const selectLastReceivedPaymentsSqueak = createSelector(
  selectReceivedPayments,
  receivedPayments => receivedPayments.length > 0 && receivedPayments[receivedPayments.length - 1]
)

export const selectReceivedPaymentsStatus = state => state.payments.receivedPaymentsStatus

export const selectPaymentSummary = state => state.payments.paymentSummary
