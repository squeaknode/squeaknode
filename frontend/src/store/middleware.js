import types from './typeActions'
import axios from 'axios'
import {API_URL} from '../config'

import {
  getTimelineSqueakDisplaysRequest,
  getSqueakDisplayRequest,
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  //getReplySqueakDisplaysRequest,
  //getAncestorSqueakDisplaysRequest,
  //makeSqueakRequest,
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
  disconnectSqueakPeerRequest,
  createPeerRequest,
  getPeerByAddressRequest,
  getConnectedPeerRequest,
  deletePeerRequest,
  getNetworkRequest,
  downloadSqueakRequest,
  getBuyOffersRequest,
  payOfferRequest,
  getPaymentSummaryRequest,
  getSentPaymentsRequest,
  getReceivedPaymentsRequest,
  getSqueakProfilePrivateKey,
  importSigningProfileRequest,
  downloadAddressSqueaksRequest,
  logoutRequest,
  setPeerAutoconnectRequest,
  getPeerRequest,
  getExternalAddressRequest,
  getSearchSqueakDisplaysRequest,
  getSellPriceRequest,
  setSellPriceRequest,
  clearSellPriceRequest,
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

        case types.LOGOUT:
            return logoutRequest((resp) => {
                dispatch({ type: types.LOGOUT, payload: {} });
            })

        case types.REGISTER:
            return axios.post(`${API_URL}/auth/register`, action.payload)
            .then(res=>dispatch({ type: types.REGISTER, payload: res.data, data: action.payload }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_NETWORK:
            return getNetworkRequest((resp) => {
                let payload = {"network": resp };
                dispatch({ type: types.GET_NETWORK, payload: payload });
    	       });

        // case types.TWEET:
        //     // return axios.post(`${API_URL}/squeak/create`, action.payload, headers)
        //     // .then(res=>dispatch({ type: types.TWEET, payload: res.data, data: action.payload }))
        //     // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))
        //
        //     let profileId = action.payload.signingProfile;
        //     let content = action.payload.description;
        //     let replyTo = action.payload.replyTo;
        //     let hasRecipient = action.payload.hasRecipient;
        //     let recipientProfileId = action.payload.recipientProfileId;
        //     return makeSqueakRequest(profileId, content, replyTo, hasRecipient, recipientProfileId, (resp) => {
        //         let squeakHash = resp.getSqueakHash();
        //         return getSqueakDisplayRequest(squeakHash, (resp) => {
        //             let payload = {"squeak": resp };
        //             dispatch({ type: types.TWEET, payload: payload, data: action.payload });
    	  //         });
        //     });
        //     // TODO: handle error response

        case types.LIKE_TWEET:
            // return axios.post(`${API_URL}/squeak/${action.payload.id}/like`, action.payload, headers)
            // .then(res=>dispatch({ type: types.LIKE_TWEET, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))
            let likeSqueakId = action.payload;
            return likeSqueakRequest(likeSqueakId, (resp) => {
              return getSqueakDisplayRequest(likeSqueakId, (resp) => {
                  let payload = {squeak: resp, squeakHash:  likeSqueakId};
                  dispatch({ type: types.UPDATE_TWEET, payload: payload, data: action.payload });
              });
            });

        case types.UNLIKE_TWEET:
            let unlikeSqueakId = action.payload;
            return unlikeSqueakRequest(unlikeSqueakId, (resp) => {
              return getSqueakDisplayRequest(unlikeSqueakId, (resp) => {
                  let payload = {squeak: resp, squeakHash:  unlikeSqueakId};
                  dispatch({ type: types.UPDATE_TWEET, payload: payload, data: action.payload });
              });
            });

        // case types.GET_TWEETS:
        //     // return axios.get(`${API_URL}/squeak`, action.payload)
        //     // .then(res=> {
        //     //   dispatch({ type: types.GET_TWEETS, payload: res.data })
        //     // })
        //     // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))
        //
        //     let lastSqueak = action.payload.lastSqueak
	      //     return getTimelineSqueakDisplaysRequest(10, lastSqueak, (resp) => {
        //         let payload = {"squeaks": resp.getSqueakDisplayEntriesList() };
	      //         dispatch({ type: types.GET_TWEETS, payload: payload })
	      //     });
        //     // TODO: handle error response

        case types.BUY_TWEET:
                let buyOfferId = action.payload.offerId
                let buySqueakHash = action.payload.squeakHash
                return payOfferRequest(buyOfferId,
                  (resp) => {
                    getSqueakDisplayRequest(buySqueakHash, (resp) => {
                      let payload = {"squeak": resp };
                      dispatch({ type: types.GET_TWEET, payload: payload });
      	          })},
                  (err) => {
                    alert(err);
                  },
              );

        // case types.CLEAR_TWEETS:
        //     dispatch({ type: types.CLEAR_TWEETS, payload: {}})
        //     return;

        case types.GET_TWEET:
            // return axios.get(`${API_URL}/squeak/${action.payload}`, action.payload)
            // .then(res=> {
            //   dispatch({ type: types.GET_TWEET, payload: res.data });
            // })
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            return getSqueakDisplayRequest(action.payload, (resp) => {
                let payload = {"squeak": resp };
                dispatch({ type: types.GET_TWEET, payload: payload });
	          });
            // TODO: handle error response

        case types.DOWNLOAD_TWEET:
            return downloadSqueakRequest(action.payload, (resp) => {
                const downloadResult = resp.getDownloadResult();
                const numPeers = downloadResult.getNumberPeers();
                const numDownloaded = downloadResult.getNumberDownloaded();
                if (numPeers === 0) {
                  let payload = {msg: "Unable to download because zero connected peers."}
                  dispatch({ type: types.ERROR, payload: payload });
                } else {
                  let payload = {msg: `Downloaded ${numDownloaded} squeaks from ${numPeers} connected peers.`}
                  dispatch({ type: types.ERROR, payload: payload });
                }
                if (downloadResult.getNumberDownloaded() === 0) {
                  return;
                }
                getSqueakDisplayRequest(action.payload, (resp) => {
                    let payload = {"squeak": resp };
                    dispatch({ type: types.GET_TWEET, payload: payload });
    	          });
                // getAncestorSqueakDisplaysRequest(action.payload, (resp) => {
                //     let payload = {"ancestorSqueaks": resp };
                //     dispatch({ type: types.GET_ANCESTOR_TWEETS, payload: payload });
                // });
                return;
    	       });

        case types.DOWNLOAD_USER_SQUEAKS:
            return downloadAddressSqueaksRequest(action.payload, (resp) => {
                const downloadResult = resp.getDownloadResult();
                const numPeers = downloadResult.getNumberPeers();
                const numDownloaded = downloadResult.getNumberDownloaded();
                if (numPeers === 0) {
                  let payload = {msg: "Unable to download because zero connected peers."}
                    dispatch({ type: types.ERROR, payload: payload });
                  } else {
                    let payload = {msg: `Downloaded ${numDownloaded} squeaks from ${numPeers} connected peers.`}
                    dispatch({ type: types.ERROR, payload: payload });
                  }
                  if (downloadResult.getNumberDownloaded() === 0) {
                    return;
                  }
                  getAddressSqueakDisplaysRequest(action.payload, 10, null, (resp) => {
                      let payload = {"userSqueaks": resp };
                      dispatch({ type: types.CLEAR_USER_TWEETS, payload: {}})
                      dispatch({ type: types.GET_USER_TWEETS, payload: payload });
                  });
                  return;
         	  });

        case types.GET_ACCOUNT:
            return axios.get(`${API_URL}/auth/user`, headers)
            .then(res=>dispatch({ type: types.GET_ACCOUNT, payload: res.data }))
            .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

        case types.GET_USER:
            // return axios.get(`${API_URL}/user/${action.payload}/squeaks`)
            // .then(res=> {
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
            let lastUserSqueak = action.payload.lastUserSqueak
            return getAddressSqueakDisplaysRequest(username, 10, lastUserSqueak, (resp) => {
                let payload = {"userSqueaks": resp };
                dispatch({ type: types.GET_USER_TWEETS, payload: payload });
            });
            // TODO: handle error response

        case types.CLEAR_USER_TWEETS:
            dispatch({ type: types.CLEAR_USER_TWEETS, payload: {}})

        // case types.GET_ANCESTOR_TWEETS:
        //     return getAncestorSqueakDisplaysRequest(action.payload, (resp) => {
        //         let payload = {"ancestorSqueaks": resp };
        //         dispatch({ type: types.GET_ANCESTOR_TWEETS, payload: payload });
        //     });
        //     // TODO: handle error response

        // case types.GET_REPLY_TWEETS:
        //     return getReplySqueakDisplaysRequest(action.payload, 10, null, (resp) => {
        //         let payload = {"replySqueaks": resp };
        //         dispatch({ type: types.GET_REPLY_TWEETS, payload: payload });
        //     });
        //     // TODO: handle error response

        case types.GET_TWEET_OFFERS:
            return getBuyOffersRequest(action.payload, (resp) => {
                let payload = {"squeakOffers": resp };
                dispatch({ type: types.GET_TWEET_OFFERS, payload: payload });
            });

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

        case types.EXPORT_PRIVATE_KEY:
            let exportProfileID = action.payload.profileId;
            return getSqueakProfilePrivateKey(exportProfileID, (resp) => {
              let payload = {"privateKey": resp.getPrivateKey() };
              dispatch({ type: types.EXPORT_PRIVATE_KEY, payload: payload, data: action.payload });
            });

        case types.DELETE_TWEET:
            // return axios.delete(`${API_URL}/squeak/${action.payload}/delete`, headers)
            // .then(res=>dispatch({ type: types.DELETE_TWEET, payload: res.data, data: action.payload }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            let deleteSqueakId = action.payload;
            return deleteSqueakRequest(deleteSqueakId, (resp) => {
              let payload = {squeak: null, squeakHash:  deleteSqueakId};
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

        case types.SET_PEER_AUTOCONNECT:
            return setPeerAutoconnectRequest(action.payload, true, (resp) => {
              getPeerRequest(action.payload, (resp) => {
                  let payload = {"savedPeer": resp.getSqueakPeer() };
                  dispatch({ type: types.SAVE_PEER, payload: payload });
              });
            });

        case types.SET_PEER_NOT_AUTOCONNECT:
            return setPeerAutoconnectRequest(action.payload, false, (resp) => {
              getPeerRequest(action.payload, (resp) => {
                  let payload = {"savedPeer": resp.getSqueakPeer() };
                  dispatch({ type: types.SAVE_PEER, payload: payload });
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

        case types.CLEAR_SEARCH:
            dispatch({ type: types.CLEAR_SEARCH, payload: {}})
            return;

        case types.SEARCH:
            // return axios.post(`${API_URL}/trend`, action.payload)
            // .then(res=>dispatch({ type: types.SEARCH, payload: res.data }))
            // .catch(err=>dispatch({ type: types.ERROR, payload: err.response.data }))

            let searchText = action.payload.searchText
            let lastSearchSqueak = action.payload.lastSqueak
	          return getSearchSqueakDisplaysRequest(searchText, 10, lastSearchSqueak, (resp) => {
                let payload = {"searchSqueaks": resp };
	              dispatch({ type: types.SEARCH, payload: payload })
	          });

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

        case types.IMPORT_SIGNING_PROFILE:
            let importSigningProfileName = action.payload.profileName
            let importSigningProfilePrivKey = action.payload.privateKey
            return importSigningProfileRequest(importSigningProfileName, importSigningProfilePrivKey, (resp) => {
                let importSigningProfileId = resp.getProfileId();
                return getSqueakProfileRequest(importSigningProfileId, (resp) => {
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

        case types.GET_PAYMENT_SUMMARY:
            return getPaymentSummaryRequest((resp) => {
                let payload = {"paymentSummary": resp.getPaymentSummary() };
                dispatch({ type: types.GET_PAYMENT_SUMMARY, payload: payload });
            });

        // case types.GET_SENT_PAYMENTS:
        //     let lastSentPayment = action.payload.lastSentPayment
        //     return getSentPaymentsRequest(10, lastSentPayment, (resp) => {
        //         let payload = {"sentPayments": resp.getSentPaymentsList() };
        //         dispatch({ type: types.GET_SENT_PAYMENTS, payload: payload });
        //     });

        // case types.CLEAR_SENT_PAYMENTS:
        //     dispatch({ type: types.CLEAR_SENT_PAYMENTS, payload: {}})
        //     return;

        // case types.GET_RECEIVED_PAYMENTS:
        //     let lastReceivedPayment = action.payload.lastReceivedPayment
        //     return getReceivedPaymentsRequest(10, lastReceivedPayment, (resp) => {
        //         let payload = {"receivedPayments": resp.getReceivedPaymentsList() };
        //         dispatch({ type: types.GET_RECEIVED_PAYMENTS, payload: payload });
        //     });
        //
        // case types.CLEAR_RECEIVED_PAYMENTS:
        //     dispatch({ type: types.CLEAR_RECEIVED_PAYMENTS, payload: {}})
        //     return;

        case types.CONNECT_PEER:
            let connectPeerNetwork = action.payload.network;
            let connectPeerHost = action.payload.host;
            let connectPeerPort = action.payload.port;

            return connectSqueakPeerRequest(connectPeerNetwork, connectPeerHost, connectPeerPort,
               (resp) => {
                 getConnectedPeersRequest((resp) => {
                  let connectedPeerConnection = resp.find(obj => {
                    return obj.getPeerAddress().getNetwork() === connectPeerNetwork &&
                    obj.getPeerAddress().getHost() === connectPeerHost &&
                    obj.getPeerAddress().getPort() == connectPeerPort
                  })
                  let payload = {"connectedPeers": resp, "peerConnection": connectedPeerConnection };
                  dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
                });
              },
            (err) => {
              alert(err);
            }
          );

        case types.DISCONNECT_PEER:
            let disconnectPeerNetwork = action.payload.network;
            let disconnectPeerHost = action.payload.host;
            let disconnectPeerPort = action.payload.port;

            return disconnectSqueakPeerRequest(disconnectPeerNetwork, disconnectPeerHost, disconnectPeerPort, (resp) => {
              return getConnectedPeersRequest((resp) => {
                  let disconnectedPeerConnection = resp.find(obj => {
                    return obj.getPeerAddress().getNetwork() === connectPeerNetwork &&
                      obj.getPeerAddress().getHost() === connectPeerHost &&
                      obj.getPeerAddress().getPort() == connectPeerPort
                  })
                  let payload = {"connectedPeers": resp, "peerConnection": disconnectedPeerConnection };
                  dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
              });
            });

        case types.GET_EXTERNAL_ADDRESS:
            return getExternalAddressRequest((resp) => {
                let payload = {"externalAddress": resp };
                dispatch({ type: types.GET_EXTERNAL_ADDRESS, payload: payload, data: action.payload });
            });

        case types.GET_SELL_PRICE:
            return getSellPriceRequest((resp) => {
                let payload = {"sellPrice": resp };
                dispatch({ type: types.GET_SELL_PRICE, payload: payload, data: action.payload });
            });

        case types.SET_SELL_PRICE:
            let newSellPriceMsat = action.payload.sellPriceMsat;
            return setSellPriceRequest(newSellPriceMsat, (resp) => {
              return getSellPriceRequest((resp) => {
                  let payload = {"sellPrice": resp };
                  dispatch({ type: types.GET_SELL_PRICE, payload: payload, data: action.payload });
              });
            });

        case types.CLEAR_SELL_PRICE:
            return clearSellPriceRequest((resp) => {
              return getSellPriceRequest((resp) => {
                  let payload = {"sellPrice": resp };
                  dispatch({ type: types.GET_SELL_PRICE, payload: payload, data: action.payload });
              });
            });

        case types.SAVE_PEER:
            let savePeerName = action.payload.name;
            let savePeerNetwork = action.payload.network;
            let savePeerHost = action.payload.host;
            let savePeerPort = action.payload.port;

            return createPeerRequest(savePeerName, savePeerNetwork, savePeerHost, savePeerPort, (resp) => {
              getPeerByAddressRequest(savePeerNetwork, savePeerHost, savePeerPort, (resp) => {
                  let payload = {"savedPeer": resp };
                  dispatch({ type: types.SAVE_PEER, payload: payload });
              });
              getConnectedPeersRequest((resp) => {
                  let payload = {"connectedPeers": resp };
                  dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
              });
            });

        case types.GET_CONNECTED_PEERS:
            return getConnectedPeersRequest((resp) => {
                let payload = {"connectedPeers": resp };
                dispatch({ type: types.GET_CONNECTED_PEERS, payload: payload });
            });

        case types.GET_PEERS:
            return getPeersRequest((resp) => {
                let payload = {"peers": resp };
                dispatch({ type: types.GET_PEERS, payload: payload });
            });

        case types.GET_PEER:
            let getPeerNetwork = action.payload.network;
            let getPeerHost = action.payload.host;
            let getPeerPort = action.payload.port;

            return getPeerByAddressRequest(getPeerNetwork, getPeerHost, getPeerPort, (resp) => {
                let payload = {"peer": resp };
                dispatch({ type: types.GET_PEERS, payload: payload });
            });

        case types.GET_PEER_CONNECTION:
            let getPeerConnectionNetwork = action.payload.network;
            let getPeerConnectionHost = action.payload.host;
            let getPeerConnectionPort = action.payload.port;

            return getConnectedPeerRequest(getPeerConnectionNetwork, getPeerConnectionHost, getPeerConnectionPort, (resp) => {
                let payload = {"peerConnection": resp };
                dispatch({ type: types.GET_PEER_CONNECTION, payload: payload });
            });

        case types.DELETE_PEER:
            let deletePeerId = action.payload.peerId;
            return deletePeerRequest(deletePeerId, (resp) => {
                dispatch({ type: types.UPDATE_PEER, payload: {}, data: action.payload });
            });

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
