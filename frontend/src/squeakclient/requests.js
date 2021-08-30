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
} from '../proto/lnd_pb';
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
  GetProfilesRequest,
  GetContactProfilesRequest,
  MakeSqueakRequest,
  GetSqueakDisplayRequest,
  SubscribeSqueakDisplayRequest,
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
  SubscribeConnectedPeersRequest,
  SubscribeConnectedPeerRequest,
  PeerAddress,
  SubscribeBuyOffersRequest,
  SubscribeReplySqueakDisplaysRequest,
  SubscribeAddressSqueakDisplaysRequest,
} from '../proto/squeak_admin_pb';

import { SqueakAdminClient } from '../proto/squeak_admin_grpc_web_pb';

console.log('Using SqueakAdminClient');

const RPC_PROXY_PORT = 15081;

const clientUrl = `http://${window.location.hostname}:15081`;
console.log(`Using clientUrl: ${clientUrl}`);
const client = new SqueakAdminClient(clientUrl);

console.log('The value of REACT_APP_SERVER_PORT is:', process.env.REACT_APP_SERVER_PORT);
const SERVER_PORT = process.env.REACT_APP_SERVER_PORT || window.location.port;

export const web_host_port = `${window.location.protocol}//${window.location.hostname}:${SERVER_PORT}`;

export function logoutRequest(handleResponse) {
  fetch(`${web_host_port}/` + 'logout', {
    method: 'get',
  }).then((response) => response.arrayBuffer()).then((data) => {
    handleResponse(data);
  });
}

export function getUserRequest(handleResponse) {
  fetch(`${web_host_port}/` + 'user', {
    method: 'get',
  }).then((response) => response.text()).then((data) => {
    handleResponse(data);
  });
}

export function getTimelineSqueakDisplaysRequest(limit, blockHeight, squeakTime, squeakHash, handleResponse) {
  const request = new GetTimelineSqueakDisplaysRequest();
  request.setLimit(limit);
  request.setBlockHeight(blockHeight);
  request.setSqueakTime(squeakTime);
  request.setSqueakHash(squeakHash);
  client.getTimelineSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function lndGetInfoRequest(handleResponse, handleErr) {
  const request = new GetInfoRequest();
  client.lndGetInfo(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndWalletBalanceRequest(handleResponse) {
  const request = new WalletBalanceRequest();
  client.lndWalletBalance(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndGetTransactionsRequest(handleResponse) {
  const request = new GetTransactionsRequest();
  client.lndGetTransactions(request, {}, (err, response) => {
    handleResponse(response.getTransactionsList());
  });
}

export function lndListPeersRequest(handleResponse) {
  const request = new ListPeersRequest();
  client.lndListPeers(request, {}, (err, response) => {
    handleResponse(response.getPeersList());
  });
}

export function lndListChannelsRequest(handleResponse) {
  const request = new ListChannelsRequest();
  client.lndListChannels(request, {}, (err, response) => {
    handleResponse(response.getChannelsList());
  });
}

export function lndPendingChannelsRequest(handleResponse) {
  const request = new PendingChannelsRequest();
  client.lndPendingChannels(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakProfileRequest(id, handleResponse, handleErr) {
  const request = new GetSqueakProfileRequest();
  request.setProfileId(id);
  client.getSqueakProfile(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfile());
  });
}

export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
  const request = new SetSqueakProfileFollowingRequest();
  request.setProfileId(id);
  request.setFollowing(following);
  client.setSqueakProfileFollowing(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function renameSqueakProfileRequest(id, profileName, handleResponse) {
  const request = new RenameSqueakProfileRequest();
  request.setProfileId(id);
  request.setProfileName(profileName);
  client.renameSqueakProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function setSqueakProfileImageRequest(id, profileImage, handleResponse) {
  const request = new SetSqueakProfileImageRequest();
  request.setProfileId(id);
  request.setProfileImage(profileImage);
  client.setSqueakProfileImage(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function clearSqueakProfileImageRequest(id, handleResponse) {
  const request = new ClearSqueakProfileImageRequest();
  request.setProfileId(id);
  client.clearSqueakProfileImage(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndConnectPeerRequest(pubkey, host, handleResponse, handleErr) {
  const request = new ConnectPeerRequest();
  const address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
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
  const request = new DisconnectPeerRequest();
  request.setPubKey(pubkey);
  client.lndDisconnectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getPeersRequest(handleResponse) {
  const request = new GetPeersRequest();
  client.getPeers(request, {}, (err, response) => {
    handleResponse(response.getSqueakPeersList());
  });
}

export function payOfferRequest(offerId, handleResponse, handleErr) {
  const request = new PayOfferRequest();
  request.setOfferId(offerId);
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
  const request = new OpenChannelRequest();
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  request.setSatPerByte(satperbyte);
  client.lndOpenChannelSync(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr) {
  const request = new CloseChannelRequest();
  const channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  client.lndCloseChannel(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getBuyOffersRequest(hash, handleResponse) {
  const request = new GetBuyOffersRequest();
  request.setSqueakHash(hash);
  client.getBuyOffers(request, {}, (err, response) => {
    handleResponse(response.getOffersList());
  });
}

export function getBuyOfferRequest(offerId, handleResponse) {
  const request = new GetBuyOfferRequest();
  request.setOfferId(offerId);
  client.getBuyOffer(request, {}, (err, response) => {
    handleResponse(response.getOffer());
  });
}

export function getPeerRequest(id, handleResponse) {
  const request = new GetPeerRequest();
  request.setPeerId(id);
  client.getPeer(request, {}, (err, response) => {
    handleResponse(response.getSqueakPeer());
  });
}

export function setPeerAutoconnectRequest(id, autoconnect, handleResponse) {
  const request = new SetPeerAutoconnectRequest();
  request.setPeerId(id);
  request.setAutoconnect(autoconnect);
  client.setPeerAutoconnect(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getProfilesRequest(handleResponse) {
  const request = new GetProfilesRequest();
  client.getProfiles(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfilesList());
  });
}

export function getSigningProfilesRequest(handleResponse) {
  const request = new GetSigningProfilesRequest();
  client.getSigningProfiles(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfilesList());
  });
}

export function getContactProfilesRequest(handleResponse) {
  const request = new GetContactProfilesRequest();
  client.getContactProfiles(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfilesList());
  });
}

export function makeSqueakRequest(profileId, content, replyto, handleResponse, handleErr) {
  const request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  client.makeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakDisplayRequest(hash, handleResponse) {
  const request = new GetSqueakDisplayRequest();
  request.setSqueakHash(hash);
  client.getSqueakDisplay(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntry());
  });
}

export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
  const request = new GetAncestorSqueakDisplaysRequest();
  request.setSqueakHash(hash);
  client.getAncestorSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getReplySqueakDisplaysRequest(hash, handleResponse) {
  const request = new GetReplySqueakDisplaysRequest();
  request.setSqueakHash(hash);
  client.getReplySqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getSqueakProfileByAddressRequest(address, handleResponse) {
  const request = new GetSqueakProfileByAddressRequest();
  request.setAddress(address);
  client.getSqueakProfileByAddress(request, {}, (err, response) => {
    handleResponse(response.getSqueakProfile());
  });
}

export function getAddressSqueakDisplaysRequest(address, handleResponse) {
  const request = new GetAddressSqueakDisplaysRequest();
  request.setAddress(address);
  client.getAddressSqueakDisplays(request, {}, (err, response) => {
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function createContactProfileRequest(profileName, squeakAddress, handleResponse, handleErr) {
  const request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  client.createContactProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function createSigningProfileRequest(profileName, handleResponse, handleErr) {
  const request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  client.createSigningProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function importSigningProfileRequest(profileName, privateKey, handleResponse, handleErr) {
  const request = new ImportSigningProfileRequest();
  request.setProfileName(profileName);
  request.setPrivateKey(privateKey);
  client.importSigningProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function createPeerRequest(peerName, host, port, handleResponse) {
  const request = new CreatePeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerName(peerName);
  request.setPeerAddress(peerAddress);
  client.createPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deletePeerRequest(peerId, handleResponse) {
  const request = new DeletePeerRequest();
  request.setPeerId(peerId);
  client.deletePeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deleteProfileRequest(profileId, handleResponse) {
  const request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  client.deleteSqueakProfile(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function deleteSqueakRequest(squeakHash, handleResponse) {
  const request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  client.deleteSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndNewAddressRequest(handleResponse) {
  const request = new NewAddressRequest();
  client.lndNewAddress(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function lndSendCoins(address, amount, satperbyte, sendall, handleResponse) {
  const request = new SendCoinsRequest();
  request.setAddr(address);
  request.setAmount(amount);
  request.setSatPerByte(satperbyte);
  request.setSendAll(sendall);
  client.lndSendCoins(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function downloadSqueakRequest(squeakHash, handleResponse) {
  const request = new DownloadSqueakRequest();
  request.setSqueakHash(squeakHash);
  client.downloadSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function downloadOffersRequest(squeakHash, handleResponse) {
  const request = new DownloadOffersRequest();
  request.setSqueakHash(squeakHash);
  client.downloadOffers(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function downloadRepliesRequest(squeakHash, handleResponse) {
  const request = new DownloadRepliesRequest();
  request.setSqueakHash(squeakHash);
  client.downloadReplies(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getSqueakDetailsRequest(hash, handleResponse) {
  const request = new GetSqueakDetailsRequest();
  request.setSqueakHash(hash);
  client.getSqueakDetails(request, {}, (err, response) => {
    handleResponse(response.getSqueakDetailEntry());
  });
}

export function getSentPaymentsRequest(handleResponse) {
  const request = new GetSentPaymentsRequest();
  client.getSentPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getReceivedPaymentsRequest(handleResponse) {
  const request = new GetReceivedPaymentsRequest();
  client.getReceivedPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getNetworkRequest(handleResponse) {
  const request = new GetNetworkRequest();
  client.getNetwork(request, {}, (err, response) => {
    handleResponse(response.getNetwork());
  });
}

export function getSqueakProfilePrivateKey(id, handleResponse) {
  const request = new GetSqueakProfilePrivateKeyRequest();
  request.setProfileId(id);
  client.getSqueakProfilePrivateKey(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getPaymentSummaryRequest(handleResponse) {
  const request = new GetPaymentSummaryRequest();
  client.getPaymentSummary(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function reprocessReceivedPaymentsRequest(handleResponse) {
  const request = new ReprocessReceivedPaymentsRequest();
  client.reprocessReceivedPayments(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function likeSqueakRequest(hash, handleResponse) {
  const request = new LikeSqueakRequest();
  request.setSqueakHash(hash);
  client.likeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function unlikeSqueakRequest(hash, handleResponse) {
  const request = new UnlikeSqueakRequest();
  request.setSqueakHash(hash);
  client.unlikeSqueak(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function getLikedSqueakDisplaysRequest(handleResponse) {
  const request = new GetLikedSqueakDisplaysRequest();
  client.getLikedSqueakDisplays(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList());
  });
}

export function getConnectedPeersRequest(handleResponse) {
  const request = new GetConnectedPeersRequest();
  client.getConnectedPeers(request, {}, (err, response) => {
    handleResponse(response.getConnectedPeersList());
  });
}

export function getConnectedPeerRequest(host, port, handleResponse) {
  const request = new GetConnectedPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  client.getConnectedPeer(request, {}, (err, response) => {
    handleResponse(response.getConnectedPeer());
  });
}

export function connectSqueakPeerRequest(host, port, handleResponse) {
  const request = new ConnectSqueakPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  client.connectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function disconnectSqueakPeerRequest(host, port, handleResponse) {
  const request = new DisconnectSqueakPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  client.disconnectPeer(request, {}, (err, response) => {
    handleResponse(response);
  });
}

export function subscribeConnectedPeersRequest(handleResponse) {
  const request = new SubscribeConnectedPeersRequest();
  const stream = client.subscribeConnectedPeers(request);
  stream.on('data', (response) => {
    // handleResponse(response.getConnectedPeersList());
    handleResponse(response.getConnectedPeersList());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
  return stream;
}

export function subscribeConnectedPeerRequest(host, port, handleResponse) {
  const request = new SubscribeConnectedPeerRequest();
  const peerAddress = new PeerAddress();
  peerAddress.setHost(host);
  peerAddress.setPort(port);
  request.setPeerAddress(peerAddress);
  const stream = client.subscribeConnectedPeer(request);
  stream.on('data', (response) => {
    handleResponse(response.getConnectedPeer());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
  return stream;
}

export function subscribeBuyOffersRequest(hash, handleResponse) {
  const request = new SubscribeBuyOffersRequest();
  request.setSqueakHash(hash);
  const stream = client.subscribeBuyOffers(request);
  stream.on('data', (response) => {
    handleResponse(response.getOffer());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
}

export function subscribeSqueakDisplayRequest(hash, handleResponse) {
  const request = new SubscribeSqueakDisplayRequest();
  request.setSqueakHash(hash);
  const stream = client.subscribeSqueakDisplay(request);
  stream.on('data', (response) => {
    handleResponse(response.getSqueakDisplayEntry());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
  console.log("Stream object:");
  console.log(stream);
  return stream;
}

export function subscribeReplySqueakDisplaysRequest(hash, handleResponse) {
  const request = new SubscribeReplySqueakDisplaysRequest();
  request.setSqueakHash(hash);
  const stream = client.subscribeReplySqueakDisplays(request);
  stream.on('data', (response) => {
    handleResponse(response.getSqueakDisplayEntry());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
  console.log("Stream object:");
  console.log(stream);
  return stream;
}

export function subscribeAddressSqueakDisplaysRequest(address, handleResponse) {
  const request = new SubscribeAddressSqueakDisplaysRequest();
  request.setAddress(address);
  const stream = client.subscribeAddressSqueakDisplays(request);
  stream.on('data', (response) => {
    handleResponse(response.getSqueakDisplayEntry());
  });
  stream.on('end', (end) => {
    // stream end signal
    console.log(end);
    alert(`Stream ended: ${end}`);
  });
  console.log("Stream object:");
  console.log(stream);
  return stream;
}
