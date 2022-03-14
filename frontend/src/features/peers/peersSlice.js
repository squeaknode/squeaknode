import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  getPeer,
} from '../../api/client'

const initialState = {
  currentPeerStatus: 'idle',
  currentPeer: null,
  connectedPeersStatus: 'idle',
  connectedPeers: [],
  savedPeersStatus: 'idle',
  savedPeers: [],
  connectPeerStatus: 'idle',
  disconnectPeerStatus: 'idle',
  savePeerStatus: 'idle',
}

// Thunk functions
export const fetchPeer = createAsyncThunk(
  'peers/fetchPeer',
  async (values) => {
    console.log('Fetching peer');
    let network = values.network;
    let host = values.host;
    let port = values.port;
    const response = await getPeer(
      network,
      host,
      port,
    );
    console.log(response);
    return response.getSqueakPeer();
  }
)

const peersSlice = createSlice({
  name: 'peers',
  initialState,
  reducers: {
    clearAll(state, action) {
      console.log('Clear current peer and status.');
      state.currentPeerStatus = 'idle';
      state.currentPeer = null;
    },
    clearSavedPeers(state, action) {
      state.savedPeersStatus = 'idle'
      state.savedPeers = [];
    },
  },
  extraReducers: (builder) => {
    builder
    .addCase(fetchPeer.pending, (state, action) => {
      state.currentPeerStatus = 'loading'
    })
    .addCase(fetchPeer.fulfilled, (state, action) => {
      console.log(action);
      const newPeer = action.payload;
      state.currentPeer = newPeer;
      state.currentPeerStatus = 'idle';
    })
  },
})

export const {
  clearAll,
  clearSavedPeers,
} = peersSlice.actions

export default peersSlice.reducer

export const selectCurrentPeer = state => state.peers.currentPeer

export const selectCurrentPeerStatus = state => state.peers.currentPeerStatus

export const selectSavedPeers = state => state.peers.savedPeers

export const selectSavedPeersStatus = state => state.peers.savedPeersStatus
