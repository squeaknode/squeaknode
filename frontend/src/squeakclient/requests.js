import {
  GetInfoRequest,
  GetInfoResponse,
  WalletBalanceRequest,
  WalletBalanceResponse,
  GetTransactionsRequest,
  TransactionDetails,
  ListPeersRequest,
  ListPeersResponse,
  ListChannelsRequest,
  ListChannelsResponse,
  PendingChannelsRequest,
  PendingChannelsResponse,
  ConnectPeerRequest,
  ConnectPeerResponse,
  LightningAddress,
  DisconnectPeerRequest,
  DisconnectPeerResponse,
  OpenChannelRequest,
  CloseChannelRequest,
  CloseStatusUpdate,
  ChannelPoint,
  NewAddressRequest,
  NewAddressResponse,
  SendCoinsRequest,
  SendCoinsResponse,
} from '../proto/lnd_pb';
import {
  GetSqueakProfileRequest,
  GetSqueakProfileReply,
  GetTimelineSqueakDisplaysRequest,
  GetTimelineSqueakDisplaysReply,
  SetSqueakProfileFollowingRequest,
  SetSqueakProfileFollowingReply,
  SetSqueakProfileUseCustomPriceRequest,
  SetSqueakProfileUseCustomPriceReply,
  SetSqueakProfileCustomPriceRequest,
  SetSqueakProfileCustomPriceReply,
  GetPeersRequest,
  PayOfferRequest,
  GetBuyOffersRequest,
  GetBuyOfferRequest,
  GetPeerRequest,
  SetPeerAutoconnectRequest,
  GetSigningProfilesRequest,
  GetProfilesRequest,
  GetContactProfilesRequest,
  MakeSqueakRequest,
  GetSqueakDisplayRequest,
  GetAncestorSqueakDisplaysRequest,
  GetReplySqueakDisplaysRequest,
  GetSqueakProfileByAddressRequest,
  GetAddressSqueakDisplaysRequest,
  CreateContactProfileRequest,
  CreateSigningProfileRequest,
  ImportSigningProfileRequest,
  CreatePeerRequest,
  DeletePeerRequest,
  DeleteSqueakProfileRequest,
  DeleteSqueakRequest,
  DownloadSqueakRequest,
  GetSqueakDetailsRequest,
  GetSentPaymentsRequest,
  GetReceivedPaymentsRequest,
  GetNetworkRequest,
  GetSqueakProfilePrivateKeyRequest,
  GetPaymentSummaryRequest,
  RenameSqueakProfileRequest,
  RenameSqueakProfileReply,
  SetSqueakProfileImageRequest,
  ClearSqueakProfileImageRequest,
  ReprocessReceivedPaymentsRequest,
  LikeSqueakRequest,
  UnlikeSqueakRequest,
  GetLikedSqueakDisplaysRequest,
  GetConnectedPeersRequest,
  GetConnectedPeerRequest,
  ConnectPeerRequest as ConnectSqueakPeerRequest,
  DisconnectPeerRequest as DisconnectSqueakPeerRequest,
  DownloadOffersRequest,
  DownloadRepliesRequest,
  DownloadAddressSqueaksRequest,
  PeerAddress,
  SetSqueakProfileImageReply,
  ClearSqueakProfileImageReply,
  GetPeersReply,
  PayOfferReply,
  GetBuyOffersReply,
  GetBuyOfferReply,
  GetPeerReply,
  SetPeerAutoconnectReply,
  GetProfilesReply,
  GetSigningProfilesReply,
  GetContactProfilesReply,
  MakeSqueakReply,
  GetSqueakDisplayReply,
  GetAncestorSqueakDisplaysReply,
  GetReplySqueakDisplaysReply,
  GetAddressSqueakDisplaysReply,
  GetSqueakProfileByAddressReply,
  CreateContactProfileReply,
  CreateSigningProfileReply,
  ImportSigningProfileReply,
  CreatePeerReply,
  DeletePeerReply,
  DeleteSqueakProfileReply,
  DeleteSqueakReply,
  DownloadSqueakReply,
  DownloadOffersReply,
  DownloadRepliesReply,
  DownloadAddressSqueaksReply,
  GetSqueakDetailsReply,
  GetSentPaymentsReply,
  GetReceivedPaymentsReply,
  GetNetworkReply,
  GetSqueakProfilePrivateKeyReply,
  GetPaymentSummaryReply,
  ReprocessReceivedPaymentsReply,
  LikeSqueakReply,
  UnlikeSqueakReply,
  GetLikedSqueakDisplaysReply,
  GetConnectedPeersReply,
  GetConnectedPeerReply,
  ConnectPeerReply as ConnectSqueakPeerReply,
  DisconnectPeerReply as DisconnectSqueakPeerReply,
  GetExternalAddressRequest,
  GetExternalAddressReply,
  GetSearchSqueakDisplaysRequest,
  GetSearchSqueakDisplaysReply,
  GetPeerByAddressRequest,
  GetPeerByAddressReply,
  GetDefaultPeerPortRequest,
  GetDefaultPeerPortReply,
  GetTwitterBearerTokenRequest,
  GetTwitterBearerTokenReply,
  SetTwitterBearerTokenRequest,
  SetTwitterBearerTokenReply,
  GetTwitterAccountsRequest,
  GetTwitterAccountsReply,
  AddTwitterAccountRequest,
  AddTwitterAccountReply,
  DeleteTwitterAccountRequest,
  DeleteTwitterAccountReply,
  SetPeerShareForFreeRequest,
  SetPeerShareForFreeReply,
  SetSellPriceRequest,
  SetSellPriceReply,
  GetSellPriceRequest,
  GetSellPriceReply,
} from '../proto/squeak_admin_pb';

console.log('The value of REACT_APP_DEV_MODE_ENABLED is:', Boolean(process.env.REACT_APP_DEV_MODE_ENABLED));
const DEV_MODE_ENABLED = process.env.REACT_APP_DEV_MODE_ENABLED;

console.log('The value of REACT_APP_SERVER_PORT is:', process.env.REACT_APP_SERVER_PORT);
const SERVER_PORT = process.env.REACT_APP_SERVER_PORT || window.location.port;

export const web_host_port = `${window.location.protocol}//${window.location.hostname}:${SERVER_PORT}`;

export function logoutRequest(handleResponse) {
  fetch(`${web_host_port}/logout`, {
    method: 'get',
  }).then((response) => response.arrayBuffer()).then((data) => {
    handleResponse(data);
  });
}

export function getUserRequest(handleResponse) {
  if (DEV_MODE_ENABLED) {
    handleResponse('DEV_MODE');
    return;
  }
  fetch(`${web_host_port}/user`, {
    method: 'get',
  }).then((response) => response.text()).then((data) => {
    handleResponse(data);
  });
}

/**
 * Copied from here:
 * https://gist.github.com/odewahn/5a5eeb23279eed6a80d7798fdb47fe91
 */
function makeRequest(route, request, deserializeMsg, handleResponse, handleError) {
  fetch(`${web_host_port}/${route}`, {
    method: 'post',
    body: request.serializeBinary(),
  })
    .then((response) => {
      if (!response.ok) { throw response; }
      return response.arrayBuffer(); // we only get here if there is no error
    })
    .then((buffer) => {
      handleResponse(deserializeMsg(buffer));
    })
    .catch((err) => {
      if (!handleError) {
        return;
      }
      if (err.text) {
        err.text().then((errorMessage) => {
          handleError(errorMessage);
        });
      } else {
        handleError('Error.'); // Hardcoded error here
      }
    });
}

export function getTimelineSqueakDisplaysRequest(limit, lastEntry, handleResponse, handleErr) {
  const request = new GetTimelineSqueakDisplaysRequest();
  request.setLimit(limit);
  request.setLastEntry(lastEntry);
  // client.getTimelineSqueakDisplays(request, {}, (err, response) => {
  //   if (err) {
  //     handleErr(err);
  //   } else {
  //     handleResponse(response.getSqueakDisplayEntriesList());
  //   }
  // });
  makeRequest(
    'gettimelinesqueakdisplays',
    request,
    GetTimelineSqueakDisplaysReply.deserializeBinary,
    handleResponse,
    handleErr,
  );
}

export function lndGetInfoRequest(handleResponse, handleErr) {
  const request = new GetInfoRequest();
  makeRequest(
    'lndgetinfo',
    request,
    GetInfoResponse.deserializeBinary,
    handleResponse,
    handleErr,
  );
}

export function lndWalletBalanceRequest(handleResponse) {
  const request = new WalletBalanceRequest();
  makeRequest(
    'lndwalletbalance',
    request,
    WalletBalanceResponse.deserializeBinary,
    handleResponse,
  );
}

export function lndGetTransactionsRequest(handleResponse) {
  const request = new GetTransactionsRequest();
  makeRequest(
    'lndgettransactions',
    request,
    TransactionDetails.deserializeBinary,
    (response) => {
      handleResponse(response.getTransactionsList());
    },
  );
}

export function lndListPeersRequest(handleResponse) {
  const request = new ListPeersRequest();
  makeRequest(
    'lndlistpeers',
    request,
    ListPeersResponse.deserializeBinary,
    (response) => {
      handleResponse(response.getPeersList());
    },
  );
}

export function lndListChannelsRequest(handleResponse) {
  const request = new ListChannelsRequest();
  makeRequest(
    'lndlistchannels',
    request,
    ListChannelsResponse.deserializeBinary,
    (response) => {
      handleResponse(response.getChannelsList());
    },
  );
}

export function lndPendingChannelsRequest(handleResponse) {
  const request = new PendingChannelsRequest();
  makeRequest(
    'lndpendingchannels',
    request,
    PendingChannelsResponse.deserializeBinary,
    handleResponse,
  );
}

export function lndConnectPeerRequest(pubkey, host, handleResponse, handleErr) {
  const request = new ConnectPeerRequest();
  const address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
  makeRequest(
    'lndconnectpeer',
    request,
    ConnectPeerResponse.deserializeBinary,
    handleResponse,
    handleErr,
  );

  // client.lndConnectPeer(request, {}, (err, response) => {
  //   if (err) {
  //     handleErr(err);
  //   }
  //   if (response) {
  //     handleResponse(response);
  //   }
  // });
}

export function lndDisconnectPeerRequest(pubkey, handleResponse) {
  const request = new DisconnectPeerRequest();
  request.setPubKey(pubkey);
  makeRequest(
    'lnddisconnectpeer',
    request,
    DisconnectPeerResponse.deserializeBinary,
    handleResponse,
  );
  // client.lndDisconnectPeer(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function lndOpenChannelSyncRequest(pubkey, amount, satperbyte, handleResponse, handleErr) {
  const request = new OpenChannelRequest();
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  request.setSatPerByte(satperbyte);
  makeRequest(
    'lndopenchannelsync',
    request,
    ChannelPoint.deserializeBinary,
    handleResponse,
    handleErr,
  );
}

export function lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr) {
  const request = new CloseChannelRequest();
  const channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  makeRequest(
    'lndclosechannel',
    request,
    CloseStatusUpdate.deserializeBinary,
    // TODO: handle streaming response
    handleResponse,
    handleErr,
  );
}

export function lndNewAddressRequest(handleResponse) {
  const request = new NewAddressRequest();
  makeRequest(
    'lndnewaddress',
    request,
    NewAddressResponse.deserializeBinary,
    handleResponse,
  );
}

export function lndSendCoins(address, amount, satperbyte, sendall, handleResponse) {
  const request = new SendCoinsRequest();
  request.setAddr(address);
  request.setAmount(amount);
  request.setSatPerByte(satperbyte);
  request.setSendAll(sendall);
  makeRequest(
    'lndsendcoins',
    request,
    SendCoinsResponse.deserializeBinary,
    handleResponse,
  );
}

export function getSqueakProfileRequest(id, handleResponse, handleErr) {
  const request = new GetSqueakProfileRequest();
  request.setProfileId(id);
  makeRequest(
    'getsqueakprofile',
    request,
    GetSqueakProfileReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakProfile());
    },
    handleErr,
  );
  // client.getSqueakProfile(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakProfile());
  // });
}

export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
  const request = new SetSqueakProfileFollowingRequest();
  request.setProfileId(id);
  request.setFollowing(following);
  makeRequest(
    'setsqueakprofilefollowing',
    request,
    SetSqueakProfileFollowingReply.deserializeBinary,
    handleResponse,
  );
}

export function setSqueakProfileUseCustomPriceRequest(id, useCustomPrice, handleResponse) {
  const request = new SetSqueakProfileUseCustomPriceRequest();
  request.setProfileId(id);
  request.setUseCustomPrice(useCustomPrice);
  makeRequest(
    'setsqueakprofileusecustomprice',
    request,
    SetSqueakProfileUseCustomPriceReply.deserializeBinary,
    handleResponse,
  );
}

export function setSqueakProfileCustomPriceRequest(id, customPriceMsat, handleResponse) {
  const request = new SetSqueakProfileCustomPriceRequest();
  request.setProfileId(id);
  request.setCustomPriceMsat(customPriceMsat);
  makeRequest(
    'setsqueakprofilecustomprice',
    request,
    SetSqueakProfileCustomPriceReply.deserializeBinary,
    handleResponse,
  );
}

export function renameSqueakProfileRequest(id, profileName, handleResponse) {
  const request = new RenameSqueakProfileRequest();
  request.setProfileId(id);
  request.setProfileName(profileName);
  makeRequest(
    'renamesqueakprofile',
    request,
    RenameSqueakProfileReply.deserializeBinary,
    handleResponse,
  );
}

export function setSqueakProfileImageRequest(id, profileImage, handleResponse) {
  const request = new SetSqueakProfileImageRequest();
  request.setProfileId(id);
  request.setProfileImage(profileImage);
  makeRequest(
    'setsqueakprofileimage',
    request,
    SetSqueakProfileImageReply.deserializeBinary,
    handleResponse,
  );
}

export function clearSqueakProfileImageRequest(id, handleResponse) {
  const request = new ClearSqueakProfileImageRequest();
  request.setProfileId(id);
  makeRequest(
    'clearsqueakprofileimage',
    request,
    ClearSqueakProfileImageReply.deserializeBinary,
    handleResponse,
  );
}

export function getPeersRequest(handleResponse) {
  const request = new GetPeersRequest();
  makeRequest(
    'getpeers',
    request,
    GetPeersReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakPeersList());
    },
  );
}

export function payOfferRequest(offerId, handleResponse, handleErr) {
  const request = new PayOfferRequest();
  request.setOfferId(offerId);
  makeRequest(
    'payoffer',
    request,
    PayOfferReply.deserializeBinary,
    handleResponse,
    handleErr,
  );
  // client.payOffer(request, {}, (err, response) => {
  //   if (err) {
  //     handleErr(err);
  //   }
  //   if (response) {
  //     handleResponse(response);
  //   }
  // });
}

export function getBuyOffersRequest(hash, handleResponse) {
  const request = new GetBuyOffersRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'getbuyoffers',
    request,
    GetBuyOffersReply.deserializeBinary,
    (response) => {
      handleResponse(response.getOffersList());
    },
  );
}

export function getBuyOfferRequest(offerId, handleResponse) {
  const request = new GetBuyOfferRequest();
  request.setOfferId(offerId);
  makeRequest(
    'getbuyoffer',
    request,
    GetBuyOfferReply.deserializeBinary,
    (response) => {
      handleResponse(response.getOffer());
    },
  );
}

export function getPeerRequest(id, handleResponse) {
  const request = new GetPeerRequest();
  request.setPeerId(id);
  makeRequest(
    'getpeer',
    request,
    GetPeerReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakPeer());
    },
  );
  // client.getPeer(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakPeer());
  // });
}

export function getPeerByAddressRequest(network, host, port, handleResponse) {
  const request = new GetPeerByAddressRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setNetwork(network);
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  makeRequest(
    'getpeerbyaddress',
    request,
    GetPeerByAddressReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakPeer());
    },
  );
}

export function setPeerAutoconnectRequest(id, autoconnect, handleResponse) {
  const request = new SetPeerAutoconnectRequest();
  request.setPeerId(id);
  request.setAutoconnect(autoconnect);
  makeRequest(
    'setpeerautoconnect',
    request,
    SetPeerAutoconnectReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
}

export function setPeerShareForFreeRequest(id, shareForFree, handleResponse) {
  const request = new SetPeerShareForFreeRequest();
  request.setPeerId(id);
  request.setShareForFree(shareForFree);
  makeRequest(
    'setpeershareforfree',
    request,
    SetPeerShareForFreeReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
}

export function getProfilesRequest(handleResponse) {
  const request = new GetProfilesRequest();
  makeRequest(
    'getprofiles',
    request,
    GetProfilesReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakProfilesList());
    },
  );
  // client.getProfiles(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakProfilesList());
  // });
}

export function getSigningProfilesRequest(handleResponse) {
  const request = new GetSigningProfilesRequest();
  makeRequest(
    'getsigningprofiles',
    request,
    GetSigningProfilesReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakProfilesList());
    },
  );
  // client.getSigningProfiles(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakProfilesList());
  // });
}

export function getContactProfilesRequest(handleResponse) {
  const request = new GetContactProfilesRequest();
  makeRequest(
    'getcontactprofiles',
    request,
    GetContactProfilesReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakProfilesList());
    },
  );
  // client.getContactProfiles(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakProfilesList());
  // });
}

export function makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr) {
  const request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  makeRequest(
    'makesqueakrequest',
    request,
    MakeSqueakReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
    handleErr,
  );
  // client.makeSqueak(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getSqueakDisplayRequest(hash, handleResponse) {
  const request = new GetSqueakDisplayRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'getsqueakdisplay',
    request,
    GetSqueakDisplayReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntry());
    },
  );
  // client.getSqueakDisplay(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntry());
  // });
}

export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
  const request = new GetAncestorSqueakDisplaysRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'getancestorsqueakdisplays',
    request,
    GetAncestorSqueakDisplaysReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntriesList());
    },
  );
  // client.getAncestorSqueakDisplays(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntriesList());
  // });
}

export function getReplySqueakDisplaysRequest(hash, limit, lastEntry, handleResponse) {
  const request = new GetReplySqueakDisplaysRequest();
  request.setSqueakHash(hash);
  request.setLimit(limit);
  request.setLastEntry(lastEntry);
  makeRequest(
    'getreplysqueakdisplays',
    request,
    GetReplySqueakDisplaysReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntriesList());
    },
  );
  // client.getReplySqueakDisplays(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntriesList());
  // });
}

export function getSqueakProfileByAddressRequest(address, handleResponse) {
  const request = new GetSqueakProfileByAddressRequest();
  request.setAddress(address);
  makeRequest(
    'getsqueakprofilebyaddress',
    request,
    GetSqueakProfileByAddressReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakProfile());
    },
  );
  // client.getSqueakProfileByAddress(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakProfile());
  // });
}

export function getAddressSqueakDisplaysRequest(address, limit, lastEntry, handleResponse) {
  const request = new GetAddressSqueakDisplaysRequest();
  request.setAddress(address);
  request.setLimit(limit);
  request.setLastEntry(lastEntry);
  makeRequest(
    'getaddresssqueakdisplays',
    request,
    GetAddressSqueakDisplaysReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntriesList());
    },
  );
  // client.getAddressSqueakDisplays(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntriesList());
  // });
}

export function getSearchSqueakDisplaysRequest(searchText, limit, lastEntry, handleResponse) {
  const request = new GetSearchSqueakDisplaysRequest();
  request.setSearchText(searchText);
  request.setLimit(limit);
  request.setLastEntry(lastEntry);
  makeRequest(
    'getsearchsqueakdisplays',
    request,
    GetSearchSqueakDisplaysReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntriesList());
    },
  );
  // client.getAddressSqueakDisplays(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntriesList());
  // });
}

export function createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr) {
  const request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  makeRequest(
    'createcontactprofile',
    request,
    CreateContactProfileReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
    handleErr,
  );
  // client.createContactProfile(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function createSigningProfileRequest(profileName, handleResponse, handleErr) {
  const request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  makeRequest(
    'createsigningprofile',
    request,
    CreateSigningProfileReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
    handleErr,
  );
  // client.createSigningProfile(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function importSigningProfileRequest(profileName, privateKey, handleResponse, handleErr) {
  const request = new ImportSigningProfileRequest();
  request.setProfileName(profileName);
  request.setPrivateKey(privateKey);
  makeRequest(
    'importsigningprofile',
    request,
    ImportSigningProfileReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
    handleErr,
  );
  // client.importSigningProfile(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function createPeerRequest(peerName, network, host, port, handleResponse) {
  const request = new CreatePeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setNetwork(network);
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerName(peerName);
  request.setPeerAddress(peerAddress);
  makeRequest(
    'createpeer',
    request,
    CreatePeerReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.createPeer(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function deletePeerRequest(peerId, handleResponse) {
  const request = new DeletePeerRequest();
  request.setPeerId(peerId);
  makeRequest(
    'deletepeer',
    request,
    DeletePeerReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.deletePeer(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function deleteProfileRequest(profileId, handleResponse) {
  const request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  makeRequest(
    'deleteprofile',
    request,
    DeleteSqueakProfileReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.deleteSqueakProfile(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function deleteSqueakRequest(squeakHash, handleResponse) {
  const request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  makeRequest(
    'deletesqueak',
    request,
    DeleteSqueakReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.deleteSqueak(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function downloadSqueakRequest(squeakHash, handleResponse) {
  const request = new DownloadSqueakRequest();
  request.setSqueakHash(squeakHash);
  makeRequest(
    'downloadsqueak',
    request,
    DownloadSqueakReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.downloadSqueak(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function downloadOffersRequest(squeakHash, handleResponse) {
  const request = new DownloadOffersRequest();
  request.setSqueakHash(squeakHash);
  makeRequest(
    'downloadoffers',
    request,
    DownloadOffersReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.downloadOffers(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function downloadRepliesRequest(squeakHash, handleResponse) {
  const request = new DownloadRepliesRequest();
  request.setSqueakHash(squeakHash);
  makeRequest(
    'downloadreplies',
    request,
    DownloadRepliesReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.downloadReplies(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function downloadAddressSqueaksRequest(address, handleResponse) {
  const request = new DownloadAddressSqueaksRequest();
  request.setAddress(address);
  makeRequest(
    'downloadaddresssqueaks',
    request,
    DownloadAddressSqueaksReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.downloadAddressSqueaks(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getSqueakDetailsRequest(hash, handleResponse) {
  const request = new GetSqueakDetailsRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'getsqueakdetails',
    request,
    GetSqueakDetailsReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDetailEntry());
    },
  );
  // client.getSqueakDetails(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDetailEntry());
  // });
}

export function getSentPaymentsRequest(limit, lastSentPayment, handleResponse) {
  const request = new GetSentPaymentsRequest();
  request.setLimit(limit);
  request.setLastSentPayment(lastSentPayment);
  makeRequest(
    'getsentpayments',
    request,
    GetSentPaymentsReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.getSentPayments(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getReceivedPaymentsRequest(limit, lastReceivedPayment, handleResponse) {
  const request = new GetReceivedPaymentsRequest();
  request.setLimit(limit);
  request.setLastReceivedPayment(lastReceivedPayment);
  makeRequest(
    'getreceivedpayments',
    request,
    GetReceivedPaymentsReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.getReceivedPayments(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getNetworkRequest(handleResponse) {
  const request = new GetNetworkRequest();
  makeRequest(
    'getnetwork',
    request,
    GetNetworkReply.deserializeBinary,
    (response) => {
      handleResponse(response.getNetwork());
    },
  );
  // client.getNetwork(request, {}, (err, response) => {
  //   handleResponse(response.getNetwork());
  // });
}

export function getSqueakProfilePrivateKey(id, handleResponse) {
  const request = new GetSqueakProfilePrivateKeyRequest();
  request.setProfileId(id);
  makeRequest(
    'getsqueakprofileprivatekey',
    request,
    GetSqueakProfilePrivateKeyReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.getSqueakProfilePrivateKey(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getPaymentSummaryRequest(handleResponse) {
  const request = new GetPaymentSummaryRequest();
  makeRequest(
    'getpaymentsummary',
    request,
    GetPaymentSummaryReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.getPaymentSummary(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function reprocessReceivedPaymentsRequest(handleResponse) {
  const request = new ReprocessReceivedPaymentsRequest();
  makeRequest(
    'reprocessreceivedpayments',
    request,
    ReprocessReceivedPaymentsReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.reprocessReceivedPayments(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function likeSqueakRequest(hash, handleResponse) {
  const request = new LikeSqueakRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'likesqueak',
    request,
    LikeSqueakReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.likeSqueak(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function unlikeSqueakRequest(hash, handleResponse) {
  const request = new UnlikeSqueakRequest();
  request.setSqueakHash(hash);
  makeRequest(
    'unlikesqueak',
    request,
    UnlikeSqueakReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.unlikeSqueak(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getLikedSqueakDisplaysRequest(limit, lastEntry, handleResponse, handleErr) {
  const request = new GetLikedSqueakDisplaysRequest();
  request.setLimit(limit);
  request.setLastEntry(lastEntry);
  makeRequest(
    'getlikedsqueakdisplays',
    request,
    GetLikedSqueakDisplaysReply.deserializeBinary,
    (response) => {
      handleResponse(response.getSqueakDisplayEntriesList());
    },
    handleErr,
  );
  // client.getLikedSqueakDisplays(request, {}, (err, response) => {
  //   handleResponse(response.getSqueakDisplayEntriesList());
  // });
}

export function getConnectedPeersRequest(handleResponse) {
  const request = new GetConnectedPeersRequest();
  makeRequest(
    'getconnectedpeers',
    request,
    GetConnectedPeersReply.deserializeBinary,
    (response) => {
      handleResponse(response.getConnectedPeersList());
    },
  );
  // client.getConnectedPeers(request, {}, (err, response) => {
  //   handleResponse(response.getConnectedPeersList());
  // });
}

export function getConnectedPeerRequest(network, host, port, handleResponse) {
  const request = new GetConnectedPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setNetwork(network);
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  makeRequest(
    'getconnectedpeer',
    request,
    GetConnectedPeerReply.deserializeBinary,
    (response) => {
      handleResponse(response.getConnectedPeer());
    },
  );
  // client.getConnectedPeer(request, {}, (err, response) => {
  //   handleResponse(response.getConnectedPeer());
  // });
}

export function connectSqueakPeerRequest(network, host, port, handleResponse, handleErr) {
  const request = new ConnectSqueakPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setNetwork(network);
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  makeRequest(
    'connectpeer',
    request,
    ConnectSqueakPeerReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
    handleErr,
  );
  // client.connectPeer(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function disconnectSqueakPeerRequest(network, host, port, handleResponse) {
  const request = new DisconnectSqueakPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setNetwork(network);
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  makeRequest(
    'disconnectpeer',
    request,
    DisconnectSqueakPeerReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
  // client.disconnectPeer(request, {}, (err, response) => {
  //   handleResponse(response);
  // });
}

export function getExternalAddressRequest(handleResponse) {
  const request = new GetExternalAddressRequest();
  makeRequest(
    'getexternaladdress',
    request,
    GetExternalAddressReply.deserializeBinary,
    (response) => {
      handleResponse(response.getPeerAddress());
    },
  );
  // client.getNetwork(request, {}, (err, response) => {
  //   handleResponse(response.getNetwork());
  // });
}

export function getDefaultPeerPortRequest(handleResponse) {
  const request = new GetDefaultPeerPortRequest();
  makeRequest(
    'getdefaultpeerport',
    request,
    GetDefaultPeerPortReply.deserializeBinary,
    (response) => {
      handleResponse(response.getPort());
    },
  );
}

export function setTwitterBearerTokenRequest(bearerToken, handleResponse) {
  const request = new SetTwitterBearerTokenRequest();
  request.setBearerToken(bearerToken);
  makeRequest(
    'settwitterbearertoken',
    request,
    SetTwitterBearerTokenReply.deserializeBinary,
    handleResponse,
  );
}

export function getTwitterBearerTokenRequest(handleResponse) {
  const request = new GetTwitterBearerTokenRequest();
  makeRequest(
    'gettwitterbearertoken',
    request,
    GetTwitterBearerTokenReply.deserializeBinary,
    (response) => {
      handleResponse(response.getBearerToken());
    },
  );
}

export function getTwitterAccountsRequest(handleResponse) {
  const request = new GetTwitterAccountsRequest();
  makeRequest(
    'gettwitteraccounts',
    request,
    GetTwitterAccountsReply.deserializeBinary,
    (response) => {
      handleResponse(response.getTwitterAccountsList());
    },
  );
}

export function addTwitterAccountRequest(twitterHandle, profileId, handleResponse) {
  const request = new AddTwitterAccountRequest();
  request.setHandle(twitterHandle);
  request.setProfileId(profileId);
  makeRequest(
    'addtwitteraccount',
    request,
    AddTwitterAccountReply.deserializeBinary,
    handleResponse,
  );
}

export function deleteTwitterAccountRequest(twitterAccountId, handleResponse) {
  const request = new DeleteTwitterAccountRequest();
  request.setTwitterAccountId(twitterAccountId);
  makeRequest(
    'deletetwitteraccount',
    request,
    DeleteTwitterAccountReply.deserializeBinary,
    handleResponse,
  );
}

export function setSellPriceRequest(bearerToken, handleResponse) {
  const request = new SetSellPriceRequest();
  request.setBearerToken(bearerToken);
  makeRequest(
    'setsellprice',
    request,
    SetSellPriceReply.deserializeBinary,
    handleResponse,
  );
}

export function getSellPriceRequest(handleResponse) {
  const request = new GetSellPriceRequest();
  makeRequest(
    'getsellprice',
    request,
    GetSellPriceReply.deserializeBinary,
    (response) => {
      handleResponse(response);
    },
  );
}

// export function subscribeConnectedPeersRequest(handleResponse) {
//   const request = new SubscribeConnectedPeersRequest();
//   const stream = client.subscribeConnectedPeers(request);
//   stream.on('data', (response) => {
//     // handleResponse(response.getConnectedPeersList());
//     handleResponse(response.getConnectedPeersList());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeConnectedPeerRequest(host, port, handleResponse) {
//   const request = new SubscribeConnectedPeerRequest();
//   const peerAddress = new PeerAddress();
//   peerAddress.setHost(host);
//   peerAddress.setPort(port);
//   request.setPeerAddress(peerAddress);
//   const stream = client.subscribeConnectedPeer(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getConnectedPeer());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeBuyOffersRequest(hash, handleResponse) {
//   const request = new SubscribeBuyOffersRequest();
//   request.setSqueakHash(hash);
//   const stream = client.subscribeBuyOffers(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getOffer());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeSqueakDisplayRequest(hash, handleResponse) {
//   const request = new SubscribeSqueakDisplayRequest();
//   request.setSqueakHash(hash);
//   const stream = client.subscribeSqueakDisplay(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntry());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeReplySqueakDisplaysRequest(hash, handleResponse) {
//   const request = new SubscribeReplySqueakDisplaysRequest();
//   request.setSqueakHash(hash);
//   const stream = client.subscribeReplySqueakDisplays(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntry());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeAddressSqueakDisplaysRequest(address, handleResponse) {
//   const request = new SubscribeAddressSqueakDisplaysRequest();
//   request.setAddress(address);
//   const stream = client.subscribeAddressSqueakDisplays(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntry());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeAncestorSqueakDisplaysRequest(hash, handleResponse) {
//   const request = new SubscribeAncestorSqueakDisplaysRequest();
//   request.setSqueakHash(hash);
//   const stream = client.subscribeAncestorSqueakDisplays(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntriesList());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeSqueakDisplaysRequest(handleResponse) {
//   const request = new SubscribeSqueakDisplaysRequest();
//   const stream = client.subscribeSqueakDisplays(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntry());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
//
// export function subscribeTimelineSqueakDisplaysRequest(handleResponse) {
//   const request = new SubscribeTimelineSqueakDisplaysRequest();
//   const stream = client.subscribeSqueakDisplays(request);
//   stream.on('data', (response) => {
//     handleResponse(response.getSqueakDisplayEntry());
//   });
//   stream.on('end', (end) => {
//     // stream end signal
//     alert(`Stream ended: ${end}`);
//   });
//   return stream;
// }
