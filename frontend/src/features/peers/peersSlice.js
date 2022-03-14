import {
  createSlice,
  createSelector,
  createAsyncThunk,
  createEntityAdapter,
} from '@reduxjs/toolkit'
import {
  getPeer,
  getConnectedPeers,
  connectPeer,
  disconnectPeer,
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

export const fetchConnectedPeers = createAsyncThunk(
  'peers/fetchConnectedPeers',
  async () => {
    console.log('Fetching connected peers');
    const response = await getConnectedPeers();
    console.log(response);
    return response.getConnectedPeersList();
  }
)

export const setConnectPeer = createAsyncThunk(
  'peers/setConnectPeer',
  async (values) => {
    console.log('Connecting peer');
    let network = values.network;
    let host = values.host;
    let port = values.port;
    await connectPeer(
      network,
      host,
      port,
    );
    const response = await getConnectedPeers();
    return response.getConnectedPeersList();
  }
)

export const setDisconnectPeer = createAsyncThunk(
  'peers/setDisconnectPeer',
  async (values) => {
    console.log('Disconnecting peer');
    let network = values.network;
    let host = values.host;
    let port = values.port;
    await disconnectPeer(
      network,
      host,
      port,
    );
    const response = await getConnectedPeers();
    return response.getConnectedPeersList();
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
      const newPeer = action.payload;
      state.currentPeer = newPeer;
      state.currentPeerStatus = 'idle';
    })
    .addCase(fetchConnectedPeers.pending, (state, action) => {
      state.connectedPeersStatus = 'loading'
    })
    .addCase(fetchConnectedPeers.fulfilled, (state, action) => {
      const newConnectedPeers = action.payload;
      state.connectedPeers = newConnectedPeers;
      state.connectedPeersStatus = 'idle';
    })
    .addCase(setConnectPeer.pending, (state, action) => {
      console.log(action);
      state.connectPeerStatus = 'loading'
    })
    .addCase(setConnectPeer.fulfilled, (state, action) => {
      console.log(action);
      const newConnectedPeers = action.payload;
      state.connectedPeers = newConnectedPeers;
      state.connectPeerStatus = 'idle';
    })
    .addCase(setDisconnectPeer.pending, (state, action) => {
      console.log(action);
      state.disconnectPeerStatus = 'loading'
    })
    .addCase(setDisconnectPeer.fulfilled, (state, action) => {
      console.log(action);
      const newConnectedPeers = action.payload;
      state.connectedPeers = newConnectedPeers;
      state.disconnectPeerStatus = 'idle';
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

export const selectConnectedPeers = state => state.peers.connectedPeers

export const selectConnectedPeersStatus = state => state.peers.connectedPeersStatus

export const selectPeerConnectionByAddress = createSelector(
  [
    selectConnectedPeers,
    (state, address) => address
  ],
  (connectedPeers, address) => {
    return connectedPeers.find(obj => {
      return obj.getPeerAddress().getNetwork() === address.network &&
      obj.getPeerAddress().getHost() === address.host &&
      obj.getPeerAddress().getPort() == address.port
    });
  }
)
