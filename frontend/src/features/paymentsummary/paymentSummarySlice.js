import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import { getPaymentSummary } from '../../api/client'

const paymentSummaryAdapter = createEntityAdapter()

const initialState = {
  paymentSummary: null,
}

// Thunk functions
export const fetchPaymentSummary = createAsyncThunk(
  'paymentSummary/fetchPaymentSummary',
  async () => {
    console.log('Fetching paymentSummary');
    const response = await getPaymentSummary();
    console.log(response);
    return response.getPaymentSummary();
  }
)


const paymentSummarySlice = createSlice({
  name: 'paymentSummary',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(fetchPaymentSummary.fulfilled, (state, action) => {
      console.log(action);
      const paymentSummary = action.payload;
      state.paymentSummary = paymentSummary;
    })
  },
})

// export const {
//   clearPaymentSummary,
// } = paymentSummarySlice.actions

export default paymentSummarySlice.reducer

export const selectPaymentSummary = state => state.paymentSummary.paymentSummary
