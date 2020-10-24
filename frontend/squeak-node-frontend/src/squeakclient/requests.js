import {
  GetInfoRequest,
  WalletBalanceRequest,
  GetTransactionsRequest,
  ListPeersRequest,
  ListChannelsRequest,
  PendingChannelsRequest,
  ConnectPeerRequest,
  LightningAddress,
  DisconnectPeerRequest,
  OpenChannelRequest,
  CloseChannelRequest,
  ChannelPoint,
  NewAddressRequest,
  GetInfoResponse,
  WalletBalanceResponse,
  TransactionDetails,
  ListPeersResponse,
  ListChannelsResponse,
  PendingChannelsResponse,
  ConnectPeerResponse,
  DisconnectPeerResponse,
  CloseStatusUpdate,
  NewAddressResponse
} from "../proto/lnd_pb"
import {
  GetSqueakProfileRequest,
  GetFollowedSqueakDisplaysRequest,
  SetSqueakProfileFollowingRequest,
  SetSqueakProfileSharingRequest,
  SetSqueakProfileWhitelistedRequest,
  GetPeersRequest,
  PayOfferRequest,
  GetBuyOffersRequest,
  GetBuyOfferRequest,
  GetPeerRequest,
  SetPeerDownloadingRequest,
  SetPeerUploadingRequest,
  GetSigningProfilesRequest,
  GetContactProfilesRequest,
  MakeSqueakRequest,
  GetSqueakDisplayRequest,
  GetAncestorSqueakDisplaysRequest,
  GetSqueakProfileByAddressRequest,
  GetAddressSqueakDisplaysRequest,
  CreateContactProfileRequest,
  CreateSigningProfileRequest,
  CreatePeerRequest,
  DeletePeerRequest,
  DeleteSqueakProfileRequest,
  DeleteSqueakRequest,
  GetFollowedSqueakDisplaysReply,
  SetSqueakProfileSharingReply,
  GetSqueakProfileReply,
  SetSqueakProfileFollowingReply,
  SetSqueakProfileWhitelistedReply,
  GetPeersReply,
  PayOfferReply,
  GetBuyOffersReply,
  GetBuyOfferReply,
  GetPeerReply,
  SetPeerDownloadingReply,
  SetPeerUploadingReply,
  GetSigningProfilesReply,
  GetContactProfilesReply,
  MakeSqueakReply,
  GetSqueakDisplayReply,
  GetAncestorSqueakDisplaysReply,
  GetSqueakProfileByAddressReply,
  GetAddressSqueakDisplaysReply,
  CreateContactProfileReply,
  CreateSigningProfileReply,
  CreatePeerReply,
  DeletePeerReply,
  DeleteSqueakProfileReply,
  DeleteSqueakReply,
} from "../proto/squeak_admin_pb"


export let web_host_port = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;


function makeRequest(route, request, handleResponse) {
  fetch(web_host_port + '/' + route, {
    method: 'post',
    body: request.serializeBinary()
  }).then(function(response) {
    return response.arrayBuffer();
  }).then(function(data) {
    handleResponse(data);
  });
}

// export function getFollowedSqueakDisplaysRequest(handleResponse) {
//   var request = new GetFollowedSqueakDisplaysRequest();
//   client.getFollowedSqueakDisplays(request, {}, (err, response) => {
//     handleResponse(response.getSqueakDisplayEntriesList())
//   });
// };

export function getFollowedSqueakDisplaysRequest(handleResponse) {
  var request = new GetFollowedSqueakDisplaysRequest();
  makeRequest('getfollowedsqueakdisplays', request, (data) => {
    var response = GetFollowedSqueakDisplaysReply.deserializeBinary(data);
    handleResponse(response.getSqueakDisplayEntriesList());
  });
};

// export function lndGetInfoRequest(handleResponse) {
//   var request = new GetInfoRequest();
//   client.lndGetInfo(request, {}, (err, response) => {
//     handleResponse(response);
//   });
// };

export function lndGetInfoRequest(handleResponse) {
  var request = new GetInfoRequest();
  makeRequest('lndgetinfo', request, (data) => {
    var response = GetInfoResponse.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndWalletBalanceRequest(handleResponse) {
//       var request = new WalletBalanceRequest();
//       client.lndWalletBalance(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function lndWalletBalanceRequest(handleResponse) {
  var request = new WalletBalanceRequest();
  makeRequest('lndwalletbalance', request, (data) => {
    var response = WalletBalanceResponse.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndGetTransactionsRequest(handleResponse) {
//       var request = new GetTransactionsRequest();
//       client.lndGetTransactions(request, {}, (err, response) => {
//         handleResponse(response.getTransactionsList());
//       });
// };

export function lndGetTransactionsRequest(handleResponse) {
  var request = new GetTransactionsRequest();
  makeRequest('lndgettransactions', request, (data) => {
    var response = TransactionDetails.deserializeBinary(data);
    handleResponse(response.getTransactionsList());
  });
};

// export function lndListPeersRequest(handleResponse) {
//       var request = new ListPeersRequest();
//       client.lndListPeers(request, {}, (err, response) => {
//         handleResponse(response.getPeersList());
//       });
// };

export function lndListPeersRequest(handleResponse) {
      var request = new ListPeersRequest();
      makeRequest('lndlistpeers', request, (data) => {
        var response = ListPeersResponse.deserializeBinary(data);
        handleResponse(response.getPeersList());
      });
};

// export function lndListChannelsRequest(handleResponse) {
//       var request = new ListChannelsRequest();
//       client.lndListChannels(request, {}, (err, response) => {
//         if (err) {
//           return;
//         }
//         handleResponse(response.getChannelsList());
//       });
// };

export function lndListChannelsRequest(handleResponse) {
  var request = new ListChannelsRequest();
  makeRequest('lndlistchannels', request, (data) => {
    var response = ListChannelsResponse.deserializeBinary(data);
    handleResponse(response.getChannelsList());
  });
};

// export function lndPendingChannelsRequest(handleResponse) {
//       var request = new PendingChannelsRequest();
//       client.lndPendingChannels(request, {}, (err, response) => {
//         if (err) {
//           return;
//         }
//         handleResponse(response);
//       });
// };

export function lndPendingChannelsRequest(handleResponse) {
  var request = new PendingChannelsRequest();
  makeRequest('lndpendingchannels', request, (data) => {
    var response = PendingChannelsResponse.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function getSqueakProfileRequest(id, handleResponse) {
//       var request = new GetSqueakProfileRequest();
//       request.setProfileId(id);
//       client.getSqueakProfile(request, {}, (err, response) => {
//         if (err) {
//           return;
//         }
//         handleResponse(response.getSqueakProfile())
//       });
// };

export function getSqueakProfileRequest(id, handleResponse) {
  var request = new GetSqueakProfileRequest();
  request.setProfileId(id);
  makeRequest('getsqueakprofile', request, (data) => {
    var response = GetSqueakProfileReply.deserializeBinary(data);
    handleResponse(response.getSqueakProfile());
  });
};

// export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
//       var request = new SetSqueakProfileFollowingRequest();
//       request.setProfileId(id);
//       request.setFollowing(following);
//       client.setSqueakProfileFollowing(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
  var request = new SetSqueakProfileFollowingRequest();
  request.setProfileId(id);
  request.setFollowing(following);
  makeRequest('setsqueakprofilefollowing', request, (data) => {
    var response = SetSqueakProfileFollowingReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function setSqueakProfileSharingRequest(id, sharing, handleResponse) {
//       var request = new SetSqueakProfileSharingRequest();
//       request.setProfileId(id);
//       request.setSharing(sharing);
//       client.setSqueakProfileSharing(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function setSqueakProfileSharingRequest(id, sharing, handleResponse) {
  var request = new SetSqueakProfileSharingRequest();
  request.setProfileId(id);
  request.setSharing(sharing);
  makeRequest('setsqueakprofilesharing', request, (data) => {
    var response = SetSqueakProfileSharingReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function setSqueakProfileWhitelistedRequest(id, whitelisted, handleResponse) {
//       var request = new SetSqueakProfileWhitelistedRequest()
//       request.setProfileId(id);
//       request.setWhitelisted(whitelisted);
//       client.setSqueakProfileWhitelisted(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function setSqueakProfileWhitelistedRequest(id, whitelisted, handleResponse) {
  var request = new SetSqueakProfileWhitelistedRequest()
  request.setProfileId(id);
  request.setWhitelisted(whitelisted);
  makeRequest('setsqueakprofilewhitelisted', request, (data) => {
    var response = SetSqueakProfileWhitelistedReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndConnectPeerRequest(pubkey, host, handleResponse) {
//   var request = new ConnectPeerRequest()
//   var address = new LightningAddress();
//   address.setPubkey(pubkey);
//   address.setHost(host);
//   request.setAddr(address);
//   client.lndConnectPeer(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function lndConnectPeerRequest(pubkey, host, handleResponse) {
  var request = new ConnectPeerRequest()
  var address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
  makeRequest('lndconnectpeer', request, (data) => {
    var response = ConnectPeerResponse.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndDisconnectPeerRequest(pubkey, handleResponse) {
//   var request = new DisconnectPeerRequest()
//   request.setPubKey(pubkey);
//   client.lndDisconnectPeer(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function lndDisconnectPeerRequest(pubkey, handleResponse) {
  var request = new DisconnectPeerRequest()
  request.setPubKey(pubkey);
  makeRequest('lnddisconnectpeer', request, (data) => {
    var response = DisconnectPeerResponse.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function getPeersRequest(handleResponse) {
//   var request = new GetPeersRequest();
//   client.getPeers(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response.getSqueakPeersList());
//   });
// };

export function getPeersRequest(handleResponse) {
  var request = new GetPeersRequest();
  makeRequest('getpeers', request, (data) => {
    var response = GetPeersReply.deserializeBinary(data);
    handleResponse(response.getSqueakPeersList());
  });
};

// export function payOfferRequest(offerId, handleResponse, handleErr) {
//   var request = new PayOfferRequest();
//   request.setOfferId(offerId);
//   client.payOffer(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function payOfferRequest(offerId, handleResponse, handleErr) {
  var request = new PayOfferRequest();
  request.setOfferId(offerId);
  makeRequest('payoffer', request, (data) => {
    var response = PayOfferReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndOpenChannelSyncRequest(pubkey, amount, handleResponse, handleErr) {
//   var request = new OpenChannelRequest()
//   request.setNodePubkeyString(pubkey);
//   request.setLocalFundingAmount(amount);
//   client.lndOpenChannelSync(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function lndOpenChannelSyncRequest(pubkey, amount, handleResponse, handleErr) {
  var request = new OpenChannelRequest()
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  makeRequest('lndopenchannelsync', request, (data) => {
    var response = ChannelPoint.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr) {
//   var request = new CloseChannelRequest();
//   var channelPoint = new ChannelPoint();
//   channelPoint.setFundingTxidStr(txId);
//   channelPoint.setOutputIndex(outputIndex);
//   request.setChannelPoint(channelPoint);
//   client.lndCloseChannel(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr) {
  var request = new CloseChannelRequest();
  var channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  makeRequest('lndclosechannel', request, (data) => {
    // TODO: handle streaming response
    var response = CloseStatusUpdate.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function getBuyOffersRequest(hash, handleResponse) {
//     var request = new GetBuyOffersRequest();
//     request.setSqueakHash(hash);
//     client.getBuyOffers(request, {}, (err, response) => {
//       if (err) {
//         return;
//       }
//       handleResponse(response.getOffersList());
//     });
// };

export function getBuyOffersRequest(hash, handleResponse) {
  var request = new GetBuyOffersRequest();
  request.setSqueakHash(hash);
  makeRequest('getbuyoffers', request, (data) => {
    var response = GetBuyOffersReply.deserializeBinary(data);
    handleResponse(response.getOffersList());
  });
};

// export function getBuyOfferRequest(offerId, handleResponse) {
//     var request = new GetBuyOfferRequest();
//     request.setOfferId(offerId);
//     client.getBuyOffer(request, {}, (err, response) => {
//       if (err) {
//         return;
//       }
//       handleResponse(response.getOffer())
//     });
// };

export function getBuyOfferRequest(offerId, handleResponse) {
  var request = new GetBuyOfferRequest();
  request.setOfferId(offerId);
  makeRequest('getbuyoffer', request, (data) => {
    var response = GetBuyOfferReply.deserializeBinary(data);
    handleResponse(response.getOffer());
  });
};

// export function getPeerRequest(id, handleResponse) {
//       var request = new GetPeerRequest();
//       request.setPeerId(id);
//       client.getPeer(request, {}, (err, response) => {
//         if (err) {
//           return;
//         }
//         handleResponse(response.getSqueakPeer())
//       });
// };

export function getPeerRequest(id, handleResponse) {
  var request = new GetPeerRequest();
  request.setPeerId(id);
  makeRequest('getpeer', request, (data) => {
    var response = GetPeerReply.deserializeBinary(data);
    handleResponse(response.getSqueakPeer());
  });
};

// export function setPeerDownloadingRequest(id, downloading, handleResponse) {
//       var request = new SetPeerDownloadingRequest();
//       request.setPeerId(id);
//       request.setDownloading(downloading);
//       client.setPeerDownloading(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function setPeerDownloadingRequest(id, downloading, handleResponse) {
  var request = new SetPeerDownloadingRequest();
  request.setPeerId(id);
  request.setDownloading(downloading);
  makeRequest('setpeerdownloading', request, (data) => {
    var response = SetPeerDownloadingReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function setPeerUploadingRequest(id, uploading, handleResponse) {
//       var request = new SetPeerUploadingRequest();
//       request.setPeerId(id);
//       request.setUploading(uploading);
//       client.setPeerUploading(request, {}, (err, response) => {
//         handleResponse(response);
//       });
// };

export function setPeerUploadingRequest(id, uploading, handleResponse) {
  var request = new SetPeerUploadingRequest();
  request.setPeerId(id);
  request.setUploading(uploading);
  makeRequest('setpeeruploading', request, (data) => {
    var response = SetPeerUploadingReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function getSigningProfilesRequest(handleResponse) {
//   var request = new GetSigningProfilesRequest();
//   client.getSigningProfiles(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response.getSqueakProfilesList());
//   });
// };

export function getSigningProfilesRequest(handleResponse) {
  var request = new GetSigningProfilesRequest();
  makeRequest('getsigningprofiles', request, (data) => {
    var response = GetSigningProfilesReply.deserializeBinary(data);
    handleResponse(response.getSqueakProfilesList());
  });
};

// export function getContactProfilesRequest(handleResponse) {
//   var request = new GetContactProfilesRequest();
//   client.getContactProfiles(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response.getSqueakProfilesList());
//   });
// };

export function getContactProfilesRequest(handleResponse) {
  var request = new GetContactProfilesRequest();
  makeRequest('getcontactprofiles', request, (data) => {
    var response = GetContactProfilesReply.deserializeBinary(data);
    handleResponse(response.getSqueakProfilesList());
  });
};

// export function makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr) {
//   var request = new MakeSqueakRequest();
//   request.setProfileId(profileId);
//   request.setContent(content);
//   request.setReplyto(replyto);
//   client.makeSqueak(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr) {
  var request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  makeRequest('makesqueakrequest', request, (data) => {
    var response = MakeSqueakReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function getSqueakDisplayRequest(hash, handleResponse) {
//     var request = new GetSqueakDisplayRequest();
//     request.setSqueakHash(hash);
//     client.getSqueakDisplay(request, {}, (err, response) => {
//       if (err) {
//         return;
//       }
//       handleResponse(response.getSqueakDisplayEntry())
//     });
// };

export function getSqueakDisplayRequest(hash, handleResponse) {
  var request = new GetSqueakDisplayRequest();
  request.setSqueakHash(hash);
  makeRequest('getsqueakdisplay', request, (data) => {
    var response = GetSqueakDisplayReply.deserializeBinary(data);
    handleResponse(response.getSqueakDisplayEntry());
  });
};

// export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
//     var request = new GetAncestorSqueakDisplaysRequest();
//     request.setSqueakHash(hash);
//     client.getAncestorSqueakDisplays(request, {}, (err, response) => {
//       if (err) {
//         return;
//       }
//       handleResponse(response.getSqueakDisplayEntriesList());
//     });
// };

export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
  var request = new GetAncestorSqueakDisplaysRequest();
  request.setSqueakHash(hash);
  makeRequest('getancestorsqueakdisplays', request, (data) => {
    var response = GetAncestorSqueakDisplaysReply.deserializeBinary(data);
    handleResponse(response.getSqueakDisplayEntriesList());
  });
};

// export function getSqueakProfileByAddressRequest(address, handleResponse) {
//       var request = new GetSqueakProfileByAddressRequest();
//       request.setAddress(address);
//       client.getSqueakProfileByAddress(request, {}, (err, response) => {
//         handleResponse(response.getSqueakProfile());
//       });
// };

export function getSqueakProfileByAddressRequest(address, handleResponse) {
  var request = new GetSqueakProfileByAddressRequest();
  request.setAddress(address);
  makeRequest('getsqueakprofilebyaddress', request, (data) => {
    var response = GetSqueakProfileByAddressReply.deserializeBinary(data);
    handleResponse(response.getSqueakProfile());
  });
};

// export function getAddressSqueakDisplaysRequest(address, handleResponse) {
//     var request = new GetAddressSqueakDisplaysRequest();
//     request.setAddress(address);
//     client.getAddressSqueakDisplays(request, {}, (err, response) => {
//       handleResponse(response.getSqueakDisplayEntriesList());
//     });
// };

export function getAddressSqueakDisplaysRequest(address, handleResponse) {
    var request = new GetAddressSqueakDisplaysRequest();
    request.setAddress(address);
    makeRequest('getaddresssqueakdisplays', request, (data) => {
      var response = GetAddressSqueakDisplaysReply.deserializeBinary(data);
      handleResponse(response.getSqueakDisplayEntriesList());
    });
};

// export function createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr) {
//   var request = new CreateContactProfileRequest();
//   request.setProfileName(profileName);
//   request.setAddress(squeakAddress);
//   client.createContactProfile(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr) {
  var request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  makeRequest('createcontactprofile', request, (data) => {
    var response = CreateContactProfileReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function createSigningProfileRequest(profileName, handleResponse, handleErr) {
//   var request = new CreateSigningProfileRequest();
//   request.setProfileName(profileName);
//   client.createSigningProfile(request, {}, (err, response) => {
//     if (err) {
//       handleErr(err);
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function createSigningProfileRequest(profileName, handleResponse, handleErr) {
  var request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  makeRequest('createsigningprofile', request, (data) => {
    var response = CreateSigningProfileReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function createPeerRequest(peerName, host, port, handleResponse) {
//   var request = new CreatePeerRequest();
//   request.setPeerName(peerName);
//   request.setHost(host);
//   request.setPort(port);
//   client.createPeer(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function createPeerRequest(peerName, host, port, handleResponse) {
  var request = new CreatePeerRequest();
  request.setPeerName(peerName);
  request.setHost(host);
  request.setPort(port);
  makeRequest('createpeer', request, (data) => {
    var response = CreatePeerReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function deletePeerRequest(peerId, handleResponse) {
//   var request = new DeletePeerRequest();
//   request.setPeerId(peerId);
//   client.deletePeer(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function deletePeerRequest(peerId, handleResponse) {
  var request = new DeletePeerRequest();
  request.setPeerId(peerId);
  makeRequest('deletepeer', request, (data) => {
    var response = DeletePeerReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function deleteProfileRequest(profileId, handleResponse) {
//   var request = new DeleteSqueakProfileRequest();
//   request.setProfileId(profileId);
//   client.deleteSqueakProfile(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function deleteProfileRequest(profileId, handleResponse) {
  var request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  makeRequest('deleteprofile', request, (data) => {
    var response = DeleteSqueakProfileReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function deleteSqueakRequest(squeakHash, handleResponse) {
//   var request = new DeleteSqueakRequest();
//   request.setSqueakHash(squeakHash);
//   client.deleteSqueak(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function deleteSqueakRequest(squeakHash, handleResponse) {
  var request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  makeRequest('deletesqueak', request, (data) => {
    var response = DeleteSqueakReply.deserializeBinary(data);
    handleResponse(response);
  });
};

// export function lndNewAddressRequest(handleResponse) {
//   var request = new NewAddressRequest();
//   client.lndNewAddress(request, {}, (err, response) => {
//     if (err) {
//       return;
//     }
//     handleResponse(response);
//   });
// };

export function lndNewAddressRequest(handleResponse) {
  var request = new NewAddressRequest();
  makeRequest('lndnewaddress', request, (data) => {
    var response = NewAddressResponse.deserializeBinary(data);
    handleResponse(response);
  });
};
