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
  SendCoinsRequest,
  SendCoinsResponse,
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
  GetTimelineSqueakDisplaysRequest,
  SetSqueakProfileFollowingRequest,
  GetPeersRequest,
  PayOfferRequest,
  GetBuyOffersRequest,
  GetBuyOfferRequest,
  GetPeerRequest,
  SetPeerAutoconnectRequest,
  GetSigningProfilesRequest,
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
  GetTimelineSqueakDisplaysReply,
  GetSqueakProfileReply,
  SetSqueakProfileFollowingReply,
  GetPeersReply,
  PayOfferReply,
  GetBuyOffersReply,
  GetBuyOfferReply,
  GetPeerReply,
  SetPeerAutoconnectReply,
  GetSigningProfilesReply,
  GetContactProfilesReply,
  MakeSqueakReply,
  GetSqueakDisplayReply,
  GetAncestorSqueakDisplaysReply,
  GetReplySqueakDisplaysReply,
  GetSqueakProfileByAddressReply,
  GetAddressSqueakDisplaysReply,
  CreateContactProfileReply,
  CreateSigningProfileReply,
  ImportSigningProfileReply,
  CreatePeerReply,
  DeletePeerReply,
  DeleteSqueakProfileReply,
  DeleteSqueakReply,
  SyncSqueakRequest,
  SyncSqueakReply,
  GetSqueakDetailsRequest,
  GetSqueakDetailsReply,
  GetSentPaymentsRequest,
  GetSentPaymentsReply,
  GetSentOffersRequest,
  GetSentOffersReply,
  GetReceivedPaymentsRequest,
  GetReceivedPaymentsReply,
  GetNetworkRequest,
  GetNetworkReply,
  GetSqueakProfilePrivateKeyRequest,
  GetSqueakProfilePrivateKeyReply,
  GetPaymentSummaryRequest,
  GetPaymentSummaryReply,
  RenameSqueakProfileRequest,
  RenameSqueakProfileReply,
  SetSqueakProfileImageRequest,
  SetSqueakProfileImageReply,
  ClearSqueakProfileImageRequest,
  ClearSqueakProfileImageReply,
  ReprocessReceivedPaymentsRequest,
  ReprocessReceivedPaymentsReply,
  LikeSqueakRequest,
  LikeSqueakReply,
  UnlikeSqueakRequest,
  UnlikeSqueakReply,
  GetLikedSqueakDisplaysRequest,
  GetLikedSqueakDisplaysReply,
  GetConnectedPeersRequest,
  GetConnectedPeersReply,
  GetConnectedPeerRequest,
  GetConnectedPeerReply,
  ConnectPeerRequest as ConnectSqueakPeerRequest,
  ConnectPeerReply as ConnectSqueakPeerReply,
  DisconnectPeerRequest as DisconnectSqueakPeerRequest,
  DisconnectPeerReply as DisconnectSqueakPeerReply,
  DownloadOffersRequest,
  DownloadOffersReply,
  DownloadRepliesRequest,
  DownloadRepliesReply,
  SubscribeConnectedPeersRequest,
} from "../proto/squeak_admin_pb"

import { SqueakAdminClient } from "../proto/squeak_admin_grpc_web_pb"

console.log("Using SqueakAdminClient");

const RPC_PROXY_PORT = 15081;

var clientUrl = 'http://' + window.location.hostname + ':15081';
console.log("Using clientUrl: " + clientUrl);
var client = new SqueakAdminClient(clientUrl);

console.log('The value of REACT_APP_SERVER_PORT is:', process.env.REACT_APP_SERVER_PORT);
const SERVER_PORT = process.env.REACT_APP_SERVER_PORT || window.location.port;

export let web_host_port = window.location.protocol + '//' + window.location.hostname + ':' + SERVER_PORT;

export function logoutRequest(handleResponse) {
  fetch(web_host_port + '/' + 'logout', {
    method: 'get',
  }).then(function(response) {
    return response.arrayBuffer();
  }).then(function(data) {
    handleResponse(data);
  });
}

export function getUserRequest(handleResponse) {
  fetch(web_host_port + '/' + 'user', {
    method: 'get',
  }).then(function(response) {
    return response.text();
  }).then(function(data) {
    handleResponse(data);
  });
}

export function getTimelineSqueakDisplaysRequest(handleResponse) {
  var request = new GetTimelineSqueakDisplaysRequest()
  client.getTimelineSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function lndGetInfoRequest(handleResponse, handleErr) {
  // var request = new GetInfoRequest();
  // makeRequest(
  //   'lndgetinfo',
  //   request,
  //   GetInfoResponse.deserializeBinary,
  //   handleResponse,
  //   handleErr
  // );
  var request = new GetInfoRequest()
  client.lndGetInfo(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndWalletBalanceRequest(handleResponse) {
  // var request = new WalletBalanceRequest();
  // makeRequest(
  //   'lndwalletbalance',
  //   request,
  //   WalletBalanceResponse.deserializeBinary,
  //   handleResponse,
  // );
  var request = new WalletBalanceRequest()
  client.lndWalletBalance(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndGetTransactionsRequest(handleResponse) {
  // var request = new GetTransactionsRequest();
  // makeRequest(
  //   'lndgettransactions',
  //   request,
  //   TransactionDetails.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getTransactionsList());
  //   }
  // );
  var request = new GetTransactionsRequest()
  client.lndGetTransactions(request, {}, (err, response) => {
    handleResponse(response.getTransactionsList());
  });
}

export function lndListPeersRequest(handleResponse) {
  // var request = new ListPeersRequest();
  // makeRequest(
  //   'lndlistpeers',
  //   request,
  //   ListPeersResponse.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getPeersList());
  //   }
  // );
  var request = new ListPeersRequest()
  client.lndListPeers(request, {}, (err, response) => {
    handleResponse(response.getPeersList());
  });
}

export function lndListChannelsRequest(handleResponse) {
  // var request = new ListChannelsRequest();
  // makeRequest(
  //   'lndlistchannels',
  //   request,
  //   ListChannelsResponse.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getChannelsList());
  //   }
  // );
  var request = new ListChannelsRequest()
  client.lndListChannels(request, {}, (err, response) => {
    handleResponse(response.getChannelsList());
  });
}

export function lndPendingChannelsRequest(handleResponse) {
  // var request = new PendingChannelsRequest();
  // makeRequest(
  //   'lndpendingchannels',
  //   request,
  //   PendingChannelsResponse.deserializeBinary,
  //   handleResponse,
  // );
  var request = new PendingChannelsRequest()
  client.lndPendingChannels(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakProfileRequest(id, handleResponse, handleErr) {
  // var request = new GetSqueakProfileRequest();
  // request.setProfileId(id);
  // makeRequest(
  //   'getsqueakprofile',
  //   request,
  //   GetSqueakProfileReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakProfile());
  //   },
  //   handleErr,
  // );
  var request = new GetSqueakProfileRequest()
  request.setProfileId(id);
  client.getSqueakProfile(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfile());
  });
}

export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
  // var request = new SetSqueakProfileFollowingRequest();
  // request.setProfileId(id);
  // request.setFollowing(following);
  // makeRequest(
  //   'setsqueakprofilefollowing',
  //   request,
  //   SetSqueakProfileFollowingReply.deserializeBinary,
  //   handleResponse,
  // );
  var request = new SetSqueakProfileFollowingRequest()
  request.setProfileId(id);
  request.setFollowing(following);
  client.setSqueakProfileFollowing(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function renameSqueakProfileRequest(id, profileName, handleResponse) {
  // var request = new RenameSqueakProfileRequest();
  // request.setProfileId(id);
  // request.setProfileName(profileName);
  // makeRequest(
  //   'renamesqueakprofile',
  //   request,
  //   RenameSqueakProfileReply.deserializeBinary,
  //   handleResponse,
  // );
  var request = new RenameSqueakProfileRequest();
  request.setProfileId(id);
  request.setProfileName(profileName);
  client.renameSqueakProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function setSqueakProfileImageRequest(id, profileImage, handleResponse) {
  var request = new SetSqueakProfileImageRequest();
  request.setProfileId(id);
  request.setProfileImage(profileImage);
  // makeRequest(
  //   'setsqueakprofileimage',
  //   request,
  //   SetSqueakProfileImageReply.deserializeBinary,
  //   handleResponse,
  // );
  client.setSqueakProfileImage(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function clearSqueakProfileImageRequest(id, handleResponse) {
  var request = new ClearSqueakProfileImageRequest();
  request.setProfileId(id);
  // makeRequest(
  //   'clearsqueakprofileimage',
  //   request,
  //   ClearSqueakProfileImageReply.deserializeBinary,
  //   handleResponse,
  // );
  client.clearSqueakProfileImage(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndConnectPeerRequest(pubkey, host, handleResponse, handleErr) {
  var request = new ConnectPeerRequest()
  var address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
  // makeRequest(
  //   'lndconnectpeer',
  //   request,
  //   ConnectPeerResponse.deserializeBinary,
  //   handleResponse,
  // );
  client.lndConnectPeer(request, {}, (err, response) => {
    if (err) {
      handleErr(err);
    }
    if (response) {
      handleResponse(response);
    }
  });
}

export function lndDisconnectPeerRequest(pubkey, handleResponse) {
  var request = new DisconnectPeerRequest()
  request.setPubKey(pubkey);
  // makeRequest(
  //   'lnddisconnectpeer',
  //   request,
  //   DisconnectPeerResponse.deserializeBinary,
  //   handleResponse,
  // );
  client.lndDisconnectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getPeersRequest(handleResponse) {
  var request = new GetPeersRequest();
  // makeRequest(
  //   'getpeers',
  //   request,
  //   GetPeersReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakPeersList());
  //   }
  // );
  client.getPeers(request, {}, (err, response) => {
    handleResponse(response.getSqueakPeersList());
  });
}

export function payOfferRequest(offerId, handleResponse, handleErr) {
  var request = new PayOfferRequest();
  request.setOfferId(offerId);
  // makeRequest(
  //   'payoffer',
  //   request,
  //   PayOfferReply.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.payOffer(request, {}, (err, response) => {
    if (err) {
      handleErr(err);
    }
    if (response) {
      handleResponse(response);
    }
  });
}

export function lndOpenChannelSyncRequest(pubkey, amount, satperbyte, handleResponse, handleErr) {
  var request = new OpenChannelRequest()
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  request.setSatPerByte(satperbyte);
  // makeRequest(
  //   'lndopenchannelsync',
  //   request,
  //   ChannelPoint.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.lndOpenChannelSync(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr) {
  var request = new CloseChannelRequest();
  var channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  // makeRequest(
  //   'lndclosechannel',
  //   request,
  //   CloseStatusUpdate.deserializeBinary,
  //   // TODO: handle streaming response
  //   handleResponse,
  //   handleErr,
  // );
  client.lndCloseChannel(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getBuyOffersRequest(hash, handleResponse) {
  var request = new GetBuyOffersRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'getbuyoffers',
  //   request,
  //   GetBuyOffersReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getOffersList());
  //   }
  // );
  client.getBuyOffers(request, {}, (err, response) => {
    handleResponse(response.getOffersList());
  });
}

export function getBuyOfferRequest(offerId, handleResponse) {
  var request = new GetBuyOfferRequest();
  request.setOfferId(offerId);
  // makeRequest(
  //   'getbuyoffer',
  //   request,
  //   GetBuyOfferReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getOffer());
  //   }
  // );
  client.getBuyOffer(request, {}, (err, response) => {
    handleResponse(response.getOffer());
  });
}

export function getPeerRequest(id, handleResponse) {
  var request = new GetPeerRequest();
  request.setPeerId(id);
  // makeRequest(
  //   'getpeer',
  //   request,
  //   GetPeerReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakPeer());
  //   }
  // );
  client.getPeer(request, {}, (err, response) => {
    handleResponse(response.getSqueakPeer());
  });
}

export function setPeerAutoconnectRequest(id, autoconnect, handleResponse) {
  var request = new SetPeerAutoconnectRequest();
  request.setPeerId(id);
  request.setAutoconnect(autoconnect);
  client.setPeerAutoconnect(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSigningProfilesRequest(handleResponse) {
  var request = new GetSigningProfilesRequest();
  // makeRequest(
  //   'getsigningprofiles',
  //   request,
  //   GetSigningProfilesReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakProfilesList());
  //   }
  // );
  client.getSigningProfiles(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfilesList());
  });
}

export function getContactProfilesRequest(handleResponse) {
  var request = new GetContactProfilesRequest();
  // makeRequest(
  //   'getcontactprofiles',
  //   request,
  //   GetContactProfilesReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakProfilesList());
  //   }
  // );
  client.getContactProfiles(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfilesList());
  });
}

export function makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr) {
  var request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  // makeRequest(
  //   'makesqueakrequest',
  //   request,
  //   MakeSqueakReply.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.makeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakDisplayRequest(hash, handleResponse) {
  var request = new GetSqueakDisplayRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'getsqueakdisplay',
  //   request,
  //   GetSqueakDisplayReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDisplayEntry());
  //   }
  // );
  client.getSqueakDisplay(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntry());
  });
}

export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
  var request = new GetAncestorSqueakDisplaysRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'getancestorsqueakdisplays',
  //   request,
  //   GetAncestorSqueakDisplaysReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDisplayEntriesList());
  //   }
  // );
  client.getAncestorSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getReplySqueakDisplaysRequest(hash, handleResponse) {
  var request = new GetReplySqueakDisplaysRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'getreplysqueakdisplays',
  //   request,
  //   GetReplySqueakDisplaysReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDisplayEntriesList());
  //   }
  // );
  client.getReplySqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getSqueakProfileByAddressRequest(address, handleResponse) {
  var request = new GetSqueakProfileByAddressRequest();
  request.setAddress(address);
  // makeRequest(
  //   'getsqueakprofilebyaddress',
  //   request,
  //   GetSqueakProfileByAddressReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakProfile());
  //   }
  // );
  client.getSqueakProfileByAddress(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfile());
  });
}

export function getAddressSqueakDisplaysRequest(address, handleResponse) {
  var request = new GetAddressSqueakDisplaysRequest();
  request.setAddress(address);
  // makeRequest(
  //   'getaddresssqueakdisplays',
  //   request,
  //   GetAddressSqueakDisplaysReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDisplayEntriesList());
  //   }
  // );
  client.getAddressSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr) {
  const request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  // makeRequest(
  //   'createcontactprofile',
  //   request,
  //   CreateContactProfileReply.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.createContactProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function createSigningProfileRequest(profileName, handleResponse, handleErr) {
  var request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  // makeRequest(
  //   'createsigningprofile',
  //   request,
  //   CreateSigningProfileReply.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.createSigningProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function importSigningProfileRequest(profileName, privateKey, handleResponse, handleErr) {
  const request = new ImportSigningProfileRequest();
  request.setProfileName(profileName);
  request.setPrivateKey(privateKey);
  // makeRequest(
  //   'importsigningprofile',
  //   request,
  //   ImportSigningProfileReply.deserializeBinary,
  //   handleResponse,
  //   handleErr,
  // );
  client.importSigningProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function createPeerRequest(peerName, host, port, handleResponse) {
  var request = new CreatePeerRequest();
  request.setPeerName(peerName);
  request.setHost(host);
  request.setPort(port);
  // makeRequest(
  //   'createpeer',
  //   request,
  //   CreatePeerReply.deserializeBinary,
  //   handleResponse,
  // );
  client.createPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deletePeerRequest(peerId, handleResponse) {
  var request = new DeletePeerRequest();
  request.setPeerId(peerId);
  // makeRequest(
  //   'deletepeer',
  //   request,
  //   DeletePeerReply.deserializeBinary,
  //   handleResponse,
  // );
  client.deletePeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deleteProfileRequest(profileId, handleResponse) {
  var request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  // makeRequest(
  //   'deleteprofile',
  //   request,
  //   DeleteSqueakProfileReply.deserializeBinary,
  //   handleResponse,
  // );
  client.deleteSqueakProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deleteSqueakRequest(squeakHash, handleResponse) {
  var request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  // makeRequest(
  //   'deletesqueak',
  //   request,
  //   DeleteSqueakReply.deserializeBinary,
  //   handleResponse,
  // );
  client.deleteSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndNewAddressRequest(handleResponse) {
  var request = new NewAddressRequest();
  // makeRequest(
  //   'lndnewaddress',
  //   request,
  //   NewAddressResponse.deserializeBinary,
  //   handleResponse,
  // );
  client.lndNewAddress(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndSendCoins(address, amount, satperbyte, sendall, handleResponse) {
  var request = new SendCoinsRequest();
  request.setAddr(address);
  request.setAmount(amount);
  request.setSatPerByte(satperbyte);
  request.setSendAll(sendall);
  // makeRequest(
  //   'lndsendcoins',
  //   request,
  //   SendCoinsResponse.deserializeBinary,
  //   handleResponse,
  // );
  client.lndSendCoins(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function syncSqueakRequest(squeakHash, handleResponse) {
  var request = new SyncSqueakRequest();
  request.setSqueakHash(squeakHash);
  // makeRequest(
  //   'syncsqueak',
  //   request,
  //   SyncSqueakReply.deserializeBinary,
  //   handleResponse,
  // );
  client.syncSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function downloadOffersRequest(squeakHash, handleResponse) {
  var request = new DownloadOffersRequest();
  request.setSqueakHash(squeakHash);
  // makeRequest(
  //   'downloadoffers',
  //   request,
  //   DownloadOffersReply.deserializeBinary,
  //   handleResponse,
  // );
  client.downloadOffers(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function downloadRepliesRequest(squeakHash, handleResponse) {
  var request = new DownloadRepliesRequest();
  request.setSqueakHash(squeakHash);
  // makeRequest(
  //   'downloadreplies',
  //   request,
  //   DownloadRepliesReply.deserializeBinary,
  //   handleResponse,
  // );
  client.downloadReplies(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakDetailsRequest(hash, handleResponse) {
  var request = new GetSqueakDetailsRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'getsqueakdetails',
  //   request,
  //   GetSqueakDetailsReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDetailEntry());
  //   }
  // );
  client.getSqueakDetails(request, {}, (err, response) => {
    handleResponse(response.getSqueakDetailEntry());
  });
}

export function getSentPaymentsRequest(handleResponse) {
  var request = new GetSentPaymentsRequest();
  // makeRequest(
  //   'getsentpayments',
  //   request,
  //   GetSentPaymentsReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response);
  //   }
  // );
  client.getSentPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

// export function getSentOffersRequest(handleResponse) {
//   var request = new GetSentOffersRequest();
//   makeRequest(
//     'getsentoffers',
//     request,
//     GetSentOffersReply.deserializeBinary,
//     (response) => {
//       handleResponse(response);
//     }
//   );
// }

export function getReceivedPaymentsRequest(handleResponse) {
  var request = new GetReceivedPaymentsRequest();
  // makeRequest(
  //   'getreceivedpayments',
  //   request,
  //   GetReceivedPaymentsReply.deserializeBinary,
  //   handleResponse,
  // );
  client.getReceivedPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getNetworkRequest(handleResponse) {
  var request = new GetNetworkRequest();
  // makeRequest(
  //   'getnetwork',
  //   request,
  //   GetNetworkReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getNetwork());
  //   }
  // );
  client.getNetwork(request, {}, (err, response) => {
    handleResponse(response.getNetwork());
  });
}

export function getSqueakProfilePrivateKey(id, handleResponse) {
  var request = new GetSqueakProfilePrivateKeyRequest();
  request.setProfileId(id);
  // makeRequest(
  //   'getsqueakprofileprivatekey',
  //   request,
  //   GetSqueakProfilePrivateKeyReply.deserializeBinary,
  //   handleResponse,
  // );
  client.getSqueakProfilePrivateKey(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getPaymentSummaryRequest(handleResponse) {
  var request = new GetPaymentSummaryRequest();
  // makeRequest(
  //   'getpaymentsummary',
  //   request,
  //   GetPaymentSummaryReply.deserializeBinary,
  //   handleResponse,
  // );
  client.getPaymentSummary(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function reprocessReceivedPaymentsRequest(handleResponse) {
  var request = new ReprocessReceivedPaymentsRequest();
  // makeRequest(
  //   'reprocessreceivedpayments',
  //   request,
  //   ReprocessReceivedPaymentsReply.deserializeBinary,
  //   handleResponse,
  // );
  client.reprocessReceivedPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function likeSqueakRequest(hash, handleResponse) {
  var request = new LikeSqueakRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'likesqueak',
  //   request,
  //   LikeSqueakReply.deserializeBinary,
  //   handleResponse,
  // );
  client.likeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function unlikeSqueakRequest(hash, handleResponse) {
  var request = new UnlikeSqueakRequest();
  request.setSqueakHash(hash);
  // makeRequest(
  //   'unlikesqueak',
  //   request,
  //   UnlikeSqueakReply.deserializeBinary,
  //   handleResponse,
  // );
  client.unlikeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getLikedSqueakDisplaysRequest(handleResponse) {
  var request = new GetLikedSqueakDisplaysRequest();
  // makeRequest(
  //   'getlikedsqueakdisplays',
  //   request,
  //   GetLikedSqueakDisplaysReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getSqueakDisplayEntriesList());
  //   }
  // );
  client.getLikedSqueakDisplays(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getConnectedPeersRequest(handleResponse) {
  var request = new GetConnectedPeersRequest();
  // makeRequest(
  //   'getconnectedpeers',
  //   request,
  //   GetConnectedPeersReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getConnectedPeersList());
  //   }
  // );
  client.getConnectedPeers(request, {}, (err, response) => {
    handleResponse(response.getConnectedPeersList());
  });
}

export function getConnectedPeerRequest(host, port, handleResponse) {
  var request = new GetConnectedPeerRequest();
  request.setHost(host);
  request.setPort(port);
  // makeRequest(
  //   'getconnectedpeer',
  //   request,
  //   GetConnectedPeerReply.deserializeBinary,
  //   (response) => {
  //     handleResponse(response.getConnectedPeer());
  //   }
  // );
  client.getConnectedPeer(request, {}, (err, response) => {
    handleResponse(response.getConnectedPeer());
  });
}

export function connectSqueakPeerRequest(host, port, handleResponse) {
  var request = new ConnectSqueakPeerRequest();
  request.setHost(host);
  request.setPort(port);
  // makeRequest(
  //   'connectpeer',
  //   request,
  //   ConnectSqueakPeerReply.deserializeBinary,
  //   handleResponse,
  // );
  client.connectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function disconnectSqueakPeerRequest(host, port, handleResponse) {
  var request = new DisconnectSqueakPeerRequest();
  request.setHost(host);
  request.setPort(port);
  // makeRequest(
  //   'disconnectpeer',
  //   request,
  //   DisconnectSqueakPeerReply.deserializeBinary,
  //   handleResponse,
  // );
  client.disconnectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function subscribeConnectedPeersRequest(handleResponse) {
  var request = new SubscribeConnectedPeersRequest();
  var stream = client.subscribeConnectedPeers(request);
  stream.on('data', (response) => {
    // handleResponse(response.getConnectedPeersList());
    handleResponse(response.getConnectedPeersList());
  });
  stream.on('end', function(end) {
    // stream end signal
    console.log(end);
    alert("Stream ended: " + end);
  });
}
