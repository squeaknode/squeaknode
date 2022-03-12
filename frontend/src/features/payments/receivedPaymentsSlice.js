import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getReceivedPayments } from '../../api/client'

const receivedPaymentsAdapter = createEntityAdapter()

const initialState = {
  status: 'idle',
  receivedPayments: []
}

// Thunk functions
export const fetchReceivedPayments = createAsyncThunk(
  'receivedPayments/fetchReceivedPayments',
  async (lastReceivedPayment) => {
    const response = await getReceivedPayments(5, lastReceivedPayment);
    return response.getReceivedPaymentsList();
  }
)


const receivedPaymentsSlice = createSlice({
  name: 'receivedPayments',
  initialState,
  reducers: {
    clearReceivedPayments(state, action) {
      state.status = 'idle'
      state.receivedPayments = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchReceivedPayments.pending, (state, action) => {
      state.status = 'loading'
    })
    .addCase(fetchReceivedPayments.fulfilled, (state, action) => {
      const newReceivedPayments = action.payload;
      state.receivedPayments = state.receivedPayments.concat(newReceivedPayments);
      state.status = 'idle'
    })
  },
})

export const {
  clearReceivedPayments,
} = receivedPaymentsSlice.actions

export default receivedPaymentsSlice.reducer

export const selectReceivedPayments = state => state.receivedPayments.receivedPayments

export const selectLastReceivedPaymentsSqueak = createSelector(
  selectReceivedPayments,
  receivedPayments => receivedPayments.length > 0 && receivedPayments[receivedPayments.length - 1]
)

export const selectReceivedPaymentsStatus = state => state.receivedPayments.status
