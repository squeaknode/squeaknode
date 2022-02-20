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
    tweet: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.TWEET, payload: data})
    },
    likeTweet: data => {
        dispatch({type: types.LIKE_TWEET, payload: data})
    },
    unlikeTweet: data => {
        dispatch({type: types.UNLIKE_TWEET, payload: data})
    },
    getTweets: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_TWEETS, payload: data})
    },
    clearTweets: data => {
        dispatch({type: types.CLEAR_TWEETS, payload: data})
    },
    bookmarkTweet: data => {
        dispatch({type: types.BOOKMARK, payload: data})
    },
    getTweet: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_TWEET, payload: data})
    },
    downloadTweet: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.DOWNLOAD_TWEET, payload: data})
    },
    buyTweet: data => {
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
    getBookmarks: data => {
        dispatch({type: types.GET_BOOKMARKS})
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
    exportPrivateKey: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.EXPORT_PRIVATE_KEY, payload: data})
    },
    retweet: data => {
        dispatch({type: types.RETWEET, payload: data})
    },
    deleteTweet: data => {
        dispatch({type: types.DELETE_TWEET, payload: data})
    },
    followUser: data => {
        dispatch({type: types.FOLLOW_USER, payload: data})
    },
    unfollowUser: data => {
        dispatch({type: types.UNFOLLOW_USER, payload: data})
    },
    editList: data => {
        dispatch({type: types.EDIT_LIST, payload: data})
    },
    createList: data => {
        dispatch({type: types.CREATE_LIST, payload: data})
    },
    deleteList: data => {
        dispatch({type: types.DELETE_LIST, payload: data})
    },
    getLists: data => {
        dispatch({type: types.GET_LISTS, payload: data})
    },
    logout: () => {
        localStorage.removeItem("Twittertoken")
        window.location.reload()
    },
    getList: data => {
        dispatch({type: types.GET_LIST, payload: data})
    },
    getTrend: data => {
        dispatch({type: types.GET_TREND, payload: data})
    },
    search: data => {
        dispatch({type: types.SEARCH, payload: data})
    },
    getTrendTweets: data => {
        dispatch({type: types.TREND_TWEETS, payload: data})
    },
    addToList: data => {
        dispatch({type: types.ADD_TO_LIST, payload: data})
    },
    getUserTweets: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_USER_TWEETS, payload: data})
    },
    clearUserTweets: data => {
        dispatch({type: types.CLEAR_USER_TWEETS, payload: data})
    },
    getAncestorTweets: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_ANCESTOR_TWEETS, payload: data})
    },
    getReplyTweets: data => {
        dispatch({type: types.SET_STATE, payload: {loading: true}})
        dispatch({type: types.GET_REPLY_TWEETS, payload: data})
    },
    getTweetOffers: data => {
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
    whoToFollow: data => {
        dispatch({type: types.WHO_TO_FOLLOW, payload: data})
    },
    alert: data => {
        dispatch({type: types.SET_STATE, payload: {top: '16px', msg: data}})
        setTimeout(() => { dispatch({type: types.SET_STATE, payload: {top: '-100px'}}) }, 2700)
    },
    getConversations: data => {
        dispatch({type: types.GET_CONVERSATIONS, payload: data})
    },
    startChat: data => {
        dispatch({type: types.SET_STATE, payload: {startingChat: true}})
        dispatch({type: types.START_CHAT, payload: data})
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
