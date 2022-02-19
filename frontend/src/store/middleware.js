import types from './typeActions'
import axios from 'axios'
import {API_URL} from '../config'

import {
  getTimelineSqueakDisplaysRequest,
  getSqueakDisplayRequest,
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getAncestorSqueakDisplaysRequest,
  makeSqueakRequest,
  getSigningProfilesRequest,
  getContactProfilesRequest,
  setSqueakProfileFollowingRequest,
  getSqueakProfileRequest,
  renameSqueakProfileRequest,
  setSqueakProfileImageRequest,
  createSigningProfileRequest,
  createContactProfileRequest,
  deleteProfileRequest,
  deleteSqueakRequest,
  likeSqueakRequest,
  unlikeSqueakRequest,
  getPeersRequest,
  getConnectedPeersRequest,
  connectSqueakPeerRequest,
} from '../squeakclient/requests';

export const token = () => {
    if(localStorage.getItem('Twittertoken')){
        return localStorage.getItem('Twittertoken')
    }
    return null
}


export const applyMiddleware = dispatch => action => {
    let headers = { headers: { Authorization: `Bearer ${token()}` } }
    switch (action.type){
        case types.LOGIN:
            return axios.post(`${API_URL}/auth/login`, action.payload)
            .then(res=>dispatch({ type: types.LOGIN, payload: res.data, rememberMe: action.payload.remember }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.REGISTER:
            return axios.post(`${API_URL}/auth/register`, action.payload)
            .then(res=>dispatch({ type: types.REGISTER, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.TWEET:
            // return axios.post(`${API_URL}/tweet/create`, action.payload, headers)
            // .then(res=>dispatch({ type: types.TWEET, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            let profileId = action.payload.signingProfile;
            let content = action.payload.description;
            let replyTo = action.payload.replyTo;
            let hasRecipient = action.payload.hasRecipient;
            let recipientProfileId = action.payload.recipientProfileId;
            return makeSqueakRequest(profileId, content, replyTo, hasRecipient, recipientProfileId, (resp) => {
                let squeakHash = resp.getSqueakHash();
                return getSqueakDisplayRequest(squeakHash, (resp) => {
                    let payload = {"tweet": resp };
                    dispatch({ type: types.TWEET, payload: payload, data: action.payload });
    	          });
            });
            // TODO: handle error response

        case types.LIKE_TWEET:
            // return axios.post(`${API_URL}/tweet/${action.payload.id}/like`, action.payload, headers)
            // .then(res=>dispatch({ type: types.LIKE_TWEET, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))
            let likeTweetId = action.payload;
            return likeSqueakRequest(likeTweetId, (resp) => {
              return getSqueakDisplayRequest(likeTweetId, (resp) => {
                  let payload = {tweet: resp, squeakHash:  likeTweetId};
                  dispatch({ type: types.UPDATE_TWEET, payload: payload, data: action.payload });
              });
            });

        case types.UNLIKE_TWEET:
            let unlikeTweetId = action.payload;
            return unlikeSqueakRequest(unlikeTweetId, (resp) => {
              return getSqueakDisplayRequest(unlikeTweetId, (resp) => {
                  let payload = {tweet: resp, squeakHash:  unlikeTweetId};
                  dispatch({ type: types.UPDATE_TWEET, payload: payload, data: action.payload });
              });
            });

        case types.GET_TWEETS:
            // return axios.get(`${API_URL}/tweet`, action.payload)
            // .then(res=> {
            //   console.log(res.data);
            //   dispatch({ type: types.GET_TWEETS, payload: res.data })
            // })
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            let lastTweet = action.payload.lastTweet
	          return getTimelineSqueakDisplaysRequest(10, lastTweet, (resp) => {
                let payload = {"tweets": resp.getSqueakDisplayEntriesList() };
	              dispatch({ type: types.GET_TWEETS, payload: payload })
	          });
            // TODO: handle error response

        case types.CLEAR_TWEETS:
            dispatch({ type: types.CLEAR_TWEETS, payload: {}})

        case types.GET_TWEET:
            // return axios.get(`${API_URL}/tweet/${action.payload}`, action.payload)
            // .then(res=> {
            //   console.log(res.data);
            //   dispatch({ type: types.GET_TWEET, payload: res.data });
            // })
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            return getSqueakDisplayRequest(action.payload, (resp) => {
                let payload = {"tweet": resp };
                dispatch({ type: types.GET_TWEET, payload: payload });
	          });
            // TODO: handle error response

        case types.GET_ACCOUNT:
            return axios.get(`${API_URL}/auth/user`, headers)
            .then(res=>dispatch({ type: types.GET_ACCOUNT, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.BOOKMARK:
            return axios.post(`${API_URL}/tweet/${action.payload.id}/bookmark`, action.payload, headers)
            .then(res=>dispatch({ type: types.BOOKMARK, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_USER:
            // return axios.get(`${API_URL}/user/${action.payload}/tweets`)
            // .then(res=> {
            //   console.log(res);
            //   dispatch({ type: types.GET_USER, payload: res.data });
            // })
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            return getSqueakProfileByAddressRequest(action.payload, (resp) => {
                let payload = {"user": resp };
                dispatch({ type: types.GET_USER, payload: payload });
            });
            // TODO: handle error response

        case types.GET_USER_TWEETS:
            let username = action.payload.username
            let lastUserTweet = action.payload.lastUserTweet
            return getAddressSqueakDisplaysRequest(username, 10, lastUserTweet, (resp) => {
                let payload = {"userTweets": resp };
                dispatch({ type: types.GET_USER_TWEETS, payload: payload });
            });
            // TODO: handle error response

        case types.CLEAR_USER_TWEETS:
            dispatch({ type: types.CLEAR_USER_TWEETS, payload: {}})

        case types.GET_ANCESTOR_TWEETS:
            return getAncestorSqueakDisplaysRequest(action.payload, (resp) => {
                let payload = {"ancestorTweets": resp };
                dispatch({ type: types.GET_ANCESTOR_TWEETS, payload: payload });
            });
            // TODO: handle error response

        case types.GET_REPLY_TWEETS:
            return getReplySqueakDisplaysRequest(action.payload, 10, null, (resp) => {
                let payload = {"replyTweets": resp };
                dispatch({ type: types.GET_REPLY_TWEETS, payload: payload });
            });
            // TODO: handle error response

        case types.GET_BOOKMARKS:
            return axios.get(`${API_URL}/user/i/bookmarks`, headers)
            .then(res=>dispatch({ type: types.GET_BOOKMARKS, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.UPDATE_USER:
            // return axios.put(`${API_URL}/user/i`, action.payload, headers)
            // .then(res=>dispatch({ type: types.UPDATE_USER, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))
            let updateProfileId = action.payload.profileId;
            let newName = action.payload.name;
            return renameSqueakProfileRequest(updateProfileId, newName, (resp) => {
              return getSqueakProfileRequest(updateProfileId, (resp) => {
                  let payload = {"user": resp.getSqueakProfile() };
                  dispatch({ type: types.UPDATE_USER, payload: payload, data: action.payload });
              });
            });

        case types.UPDATE_USER_IMAGE:
            let updateImageProfileId = action.payload.profileId;
            let profileImg = action.payload.profileImg;
            return setSqueakProfileImageRequest(updateImageProfileId, profileImg, (resp) => {
              return getSqueakProfileRequest(updateImageProfileId, (resp) => {
                  let payload = {"user": resp.getSqueakProfile() };
                  dispatch({ type: types.UPDATE_USER, payload: payload, data: action.payload });
              });
            });

        case types.DELETE_USER:
            let deleteProfileId = action.payload.profileId;
            return deleteProfileRequest(deleteProfileId, (resp) => {
              dispatch({ type: types.DELETE_USER, payload: {}, data: action.payload });
            });

        case types.RETWEET:
            return axios.post(`${API_URL}/tweet/${action.payload.id}/retweet`, action.payload, headers)
            .then(res=>dispatch({ type: types.RETWEET, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.DELETE_TWEET:
            // return axios.delete(`${API_URL}/tweet/${action.payload}/delete`, headers)
            // .then(res=>dispatch({ type: types.DELETE_TWEET, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            let deleteTweetId = action.payload;
            return deleteSqueakRequest(deleteTweetId, (resp) => {
              let payload = {tweet: null, squeakHash:  deleteTweetId};
              dispatch({ type: types.DELETE_TWEET, payload: payload, data: action.payload });
            });

        case types.FOLLOW_USER:
            return setSqueakProfileFollowingRequest(action.payload, true, (resp) => {
              return getSqueakProfileRequest(action.payload, (resp) => {
                  let payload = {"user": resp.getSqueakProfile() };
                  dispatch({ type: types.FOLLOW_USER, payload: payload, data: action.payload });
              });
            });

        case types.UNFOLLOW_USER:
            return setSqueakProfileFollowingRequest(action.payload, false, (resp) => {
              return getSqueakProfileRequest(action.payload, (resp) => {
                  let payload = {"user": resp.getSqueakProfile() };
                  dispatch({ type: types.UNFOLLOW_USER, payload: payload, data: action.payload });
            });
        });

        case types.EDIT_LIST:
            return axios.put(`${API_URL}/lists/${action.payload.id}/edit`, action.payload, headers)
            .then(res=>dispatch({ type: types.EDIT_LIST, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.CREATE_LIST:
            return axios.post(`${API_URL}/lists/create`, action.payload, headers)
            .then(res=>dispatch({ type: types.CREATE_LIST, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.DELETE_LIST:
            return axios.delete(`${API_URL}/lists/${action.payload}/delete`, headers)
            .then(res=>dispatch({ type: types.DELETE_LIST, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_LISTS:
            return axios.get(`${API_URL}/user/i/lists`, headers)
            .then(res=>dispatch({ type: types.GET_LISTS, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_LIST:
            return axios.get(`${API_URL}/lists/${action.payload}`, headers )
            .then(res=>dispatch({ type: types.GET_LIST, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_TREND:
            return axios.get(`${API_URL}/trend`)
            .then(res=>dispatch({ type: types.GET_TREND, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.SEARCH:
            return axios.post(`${API_URL}/trend`, action.payload)
            .then(res=>dispatch({ type: types.SEARCH, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.SEARCH_USERS:
            return axios.post(`${API_URL}/user`, action.payload)
            .then(res=>dispatch({ type: types.SEARCH_USERS, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.TREND_TWEETS:
            return axios.get(`${API_URL}/trend/${action.payload}`)
            .then(res=>dispatch({ type: types.TREND_TWEETS, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.ADD_TO_LIST:
            return axios.post(`${API_URL}/lists/${action.payload.username}/${action.payload.id}`, action.payload, headers)
            .then(res=>dispatch({ type: types.ADD_TO_LIST, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_FOLLOWERS:
            return axios.get(`${API_URL}/user/${action.payload}/followers`, headers)
            .then(res=>dispatch({ type: types.GET_FOLLOWERS, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        // case types.GET_FOLLOWING:
        //     return axios.get(`${API_URL}/lists/i/following`, action.payload, headers)
        //     .then(res=>dispatch({ type: types.GET_FOLLOWING, payload: res.data, data: action.payload }))
        //     .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.CREATE_SIGNING_PROFILE:
            let newSigningProfileName = action.payload.profileName
            return createSigningProfileRequest(newSigningProfileName, (resp) => {
                let newSigningProfileId = resp.getProfileId();
                return getSqueakProfileRequest(newSigningProfileId, (resp) => {
                    let payload = {"user": resp.getSqueakProfile() };
                    dispatch({ type: types.CREATE_SIGNING_PROFILE, payload: payload, data: action.payload });
                });
            });

        case types.CREATE_CONTACT_PROFILE:
            let newContactProfileName = action.payload.profileName
            let newContactProfilePubkey = action.payload.pubkey
            return createContactProfileRequest(newContactProfileName, newContactProfilePubkey, (resp) => {
                let newContactProfileId = resp.getProfileId();
                return getSqueakProfileRequest(newContactProfileId, (resp) => {
                    let payload = {"user": resp.getSqueakProfile() };
                    dispatch({ type: types.CREATE_CONTACT_PROFILE, payload: payload, data: action.payload });
                });
            });

        case types.GET_SIGNING_PROFILES:
            return getSigningProfilesRequest((resp) => {
                let payload = {"signingProfiles": resp };
                dispatch({ type: types.GET_SIGNING_PROFILES, payload: payload });
            });

        case types.GET_CONTACT_PROFILES:
            return getContactProfilesRequest((resp) => {
                let payload = {"contactProfiles": resp };
                dispatch({ type: types.GET_CONTACT_PROFILES, payload: payload });
            });

        case types.CONNECT_PEER:
            let connectPeerNetwork = action.payload.network;
            let connectPeerHost = action.payload.host;
            let connectPeerPort = action.payload.port;

            return connectSqueakPeerRequest(connectPeerNetwork, connectPeerHost, connectPeerPort, (resp) => {
              return getConnectedPeersRequest((resp) => {
                  let payload = {"connectedPeers": resp };
                  dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
              });
            });

        case types.GET_CONNECTED_PEERS:
            return getConnectedPeersRequest((resp) => {
                let payload = {"connectedPeers": resp };
                dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
            });

        case types.WHO_TO_FOLLOW:
            return axios.get(`${API_URL}/user/i/suggestions`, headers)
            .then(res=>dispatch({ type: types.WHO_TO_FOLLOW, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_CONVERSATIONS:
            return axios.get(`${API_URL}/chat/conversations`, headers)
            .then(res=>dispatch({ type: types.GET_CONVERSATIONS, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.START_CHAT:
            return axios.post(`${API_URL}/chat/conversation`, action.payload, headers)
            .then(res=>dispatch({ type: types.START_CHAT, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_SINGLE_CONVERSATION:
            return axios.get(`${API_URL}/chat/conversation?id=${action.payload.id}`, headers)
            .then(res=>dispatch({ type: types.GET_SINGLE_CONVERSATION, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        default: dispatch(action)
    }
}
