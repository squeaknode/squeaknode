import types from './typeActions'
import jwt_decode from 'jwt-decode'

export const useActions = (state, dispatch) => ({
    login: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.LOGIN, payload: data})
    },
    signup: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.REGISTER, payload: data})
    },
    getNetwork: data => {
        dispatch({type: types.GET_NETWORK, payload: data})
    },
    squeak: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.TWEET, payload: data})
    },
    likeSqueak: data => {
        dispatch({type: types.LIKE_TWEET, payload: data})
    },
    unlikeSqueak: data => {
        dispatch({type: types.UNLIKE_TWEET, payload: data})
    },
    // getSqueaks: data => {
    //     dispatch({type: types.SET_STATE, payload: {loading: true}})
    //     dispatch({type: types.GET_TWEETS, payload: data})
    // },
    // clearSqueaks: data => {
    //     dispatch({type: types.CLEAR_TWEETS, payload: data})
    // },
    getSqueak: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_TWEET, payload: data})
    },
    downloadSqueak: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.DOWNLOAD_TWEET, payload: data})
    },
    buySqueak: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.BUY_TWEET, payload: data})
    },
    verifyToken: data => {
        if(localStorage.getItem('Twittertoken')){
        const jwt = jwt_decode(localStorage.getItem('Twittertoken'))
        const current_time = new Date().getTime() / 1000;
            if(current_time > jwt.exp){
                dispatch({type: types.SET_STATE, payload: {session: false}})
                localStorage.removeItem("Twittertoken")
            }else{
                if(data === 'get account'){ dispatch({type: types.GET_ACCOUNT}) }
                dispatch({type: types.SET_STATE, payload: {session: true, decoded: jwt}})
            }
       }else{
            dispatch({type: types.SET_STATE, payload: {session: false}})
       }
    },
    getUser: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_USER, payload: data})
    },
    updateUser: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.UPDATE_USER, payload: data})
    },
    updateUserImage: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.UPDATE_USER_IMAGE, payload: data})
    },
    deleteUser: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.DELETE_USER, payload: data})
    },
    downloadUserSqueaks: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.DOWNLOAD_USER_SQUEAKS, payload: data})
    },
    exportPrivateKey: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.EXPORT_PRIVATE_KEY, payload: data})
    },
    deleteSqueak: data => {
        dispatch({type: types.DELETE_TWEET, payload: data})
    },
    followUser: data => {
        dispatch({type: types.FOLLOW_USER, payload: data})
    },
    unfollowUser: data => {
        dispatch({type: types.UNFOLLOW_USER, payload: data})
    },
    setPeerAutoconnect: data => {
        dispatch({type: types.SET_PEER_AUTOCONNECT, payload: data})
    },
    setPeerNotAutoconnect: data => {
        dispatch({type: types.SET_PEER_NOT_AUTOCONNECT, payload: data})
    },
    logout: () => {
        // localStorage.removeItem("Twittertoken")
        // window.location.reload()
        dispatch({type: types.LOGOUT, payload: {}})
    },
    getList: data => {
        dispatch({type: types.GET_LIST, payload: data})
    },
    getTrend: data => {
        dispatch({type: types.GET_TREND, payload: data})
    },
    clearSearch: data => {
        console.log(data)
        dispatch({type: types.CLEAR_SEARCH, payload: data})
    },
    search: data => {
        console.log(data)
        dispatch({type: types.SEARCH, payload: data})
    },
    getTrendSqueaks: data => {
        dispatch({type: types.TREND_TWEETS, payload: data})
    },
    addToList: data => {
        dispatch({type: types.ADD_TO_LIST, payload: data})
    },
    getUserSqueaks: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_USER_TWEETS, payload: data})
    },
    clearUserSqueaks: data => {
        dispatch({type: types.CLEAR_USER_TWEETS, payload: data})
    },
    getAncestorSqueaks: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_ANCESTOR_TWEETS, payload: data})
    },
    getReplySqueaks: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_REPLY_TWEETS, payload: data})
    },
    getSqueakOffers: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_TWEET_OFFERS, payload: data})
    },
    getFollowers: data => {
        dispatch({type: types.GET_FOLLOWERS, payload: data})
    },
    getFollowing: data => {
        dispatch({type: types.GET_FOLLOWING, payload: data})
    },
    searchUsers: data => {
        dispatch({type: types.SEARCH_USERS, payload: data})
    },
    alert: data => {
        dispatch({type: types.SET_STATE, payload: {top: '16px', msg: data}})
        setTimeout(() => { dispatch({type: types.SET_STATE, payload: {top: '-100px'}}) }, 2700)
    },
    getConversations: data => {
        dispatch({type: types.GET_CONVERSATIONS, payload: data})
    },
    getSingleConversation: data =>{
        dispatch({type: types.GET_SINGLE_CONVERSATION, payload: data})
    },
    importSigningProfile: data => {
        dispatch({type: types.IMPORT_SIGNING_PROFILE, payload: data})
    },
    createSigningProfile: data => {
        dispatch({type: types.CREATE_SIGNING_PROFILE, payload: data})
    },
    createContactProfile: data => {
        dispatch({type: types.CREATE_CONTACT_PROFILE, payload: data})
    },
    getSigningProfiles: data => {
        dispatch({type: types.GET_SIGNING_PROFILES, payload: data})
    },
    getContactProfiles: data => {
        dispatch({type: types.GET_CONTACT_PROFILES, payload: data})
    },
    getPaymentSummary: data => {
        dispatch({type: types.GET_PAYMENT_SUMMARY, payload: data})
    },
    getSentPayments: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_SENT_PAYMENTS, payload: data})
    },
    clearSentPayments: data => {
        dispatch({type: types.CLEAR_SENT_PAYMENTS, payload: data})
    },
    getReceivedPayments: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_RECEIVED_PAYMENTS, payload: data})
    },
    clearReceivedPayments: data => {
        dispatch({type: types.CLEAR_RECEIVED_PAYMENTS, payload: data})
    },
    getExternalAddress: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_EXTERNAL_ADDRESS, payload: data})
    },
    getSellPrice: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_SELL_PRICE, payload: data})
    },
    setSellPrice: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.SET_SELL_PRICE, payload: data})
    },
    clearSellPrice: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.CLEAR_SELL_PRICE, payload: data})
    },
    connectPeer: data => {
        dispatch({type: types.CONNECT_PEER, payload: data})
    },
    disconnectPeer: data => {
        dispatch({type: types.DISCONNECT_PEER, payload: data})
    },
    savePeer: data => {
        dispatch({type: types.SAVE_PEER, payload: data})
    },
    getConnectedPeers: data => {
        dispatch({type: types.GET_CONNECTED_PEERS, payload: data})
    },
    getPeers: data => {
        dispatch({type: types.GET_PEERS, payload: data})
    },
    getPeer: data => {
        dispatch({type: types.GET_PEER, payload: data})
    },
    getPeerConnection: data => {
        dispatch({type: types.GET_PEER_CONNECTION, payload: data})
    },
    deletePeer: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.DELETE_PEER, payload: data})
    }
})
