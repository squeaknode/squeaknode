import { client } from "../squeakclient/squeakclient"

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
} from "../proto/lnd_pb"
import {
  GetSqueakProfileRequest,
  GetFollowedSqueakDisplaysRequest,
  GetSigningProfilesRequest,
  SetSqueakProfileFollowingRequest,
  SetSqueakProfileSharingRequest,
  SetSqueakProfileWhitelistedRequest,
  GetPeersRequest,
  PayOfferRequest,
} from "../proto/squeak_admin_pb"


export function getFollowedSqueakDisplays(handleResponse) {
  console.log("called getSqueaks with handleResponse");
  var getFollowedSqueakDisplaysRequest = new GetFollowedSqueakDisplaysRequest();
  client.getFollowedSqueakDisplays(getFollowedSqueakDisplaysRequest, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList())
  });
};


export function lndGetInfo(handleResponse) {
  console.log("called lndGetInfo");
  var getInfoRequest = new GetInfoRequest();
  console.log(getInfoRequest);
  client.lndGetInfo(getInfoRequest, {}, (err, response) => {
    console.log(response);
    handleResponse(response);
  });
};

export function lndWalletBalance(handleResponse) {
      console.log("called lndWalletBalanceRequest");
      var walletBalanceRequest = new WalletBalanceRequest();
      console.log(walletBalanceRequest);
      client.lndWalletBalance(walletBalanceRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndGetTransactions(handleResponse) {
      console.log("called lndGetTransactions");
      var getTransactionsRequest = new GetTransactionsRequest();
      console.log(getTransactionsRequest);
      client.lndGetTransactions(getTransactionsRequest, {}, (err, response) => {
        console.log(response);
        console.log("response.getTransactionsList()");
        console.log(response.getTransactionsList());
        handleResponse(response.getTransactionsList());
      });
};

export function lndListPeers(handleResponse) {
      console.log("called listPeers");
      var listPeersRequest = new ListPeersRequest();
      console.log(listPeersRequest);
      client.lndListPeers(listPeersRequest, {}, (err, response) => {
        console.log(response);
        console.log("response.getPeersList()");
        console.log(response.getPeersList());
        handleResponse(response.getPeersList());
      });
};

export function lndListChannels(handleResponse) {
      console.log("called lndListChannels");
      var listChannelsRequest = new ListChannelsRequest();
      console.log(listChannelsRequest);
      client.lndListChannels(listChannelsRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting channels: ' + err.message);
          return;
        }
        console.log(response);
        console.log("response.getChannelsList()");
        console.log(response.getChannelsList());
        handleResponse(response.getChannelsList());
      });
};

export function lndPendingChannels(handleResponse) {
      console.log("called lndPendingChannels");
      var pendingChannelsRequest = new PendingChannelsRequest();
      console.log(pendingChannelsRequest);
      client.lndPendingChannels(pendingChannelsRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting pending channels: ' + err.message);
          return;
        }
        console.log(response);
        handleResponse(response);
      });
};

export function getSqueakProfile(id, handleResponse) {
      console.log("called getSqueakProfile with profileId: " + id);
      var getSqueakProfileRequest = new GetSqueakProfileRequest();
      getSqueakProfileRequest.setProfileId(id);
      console.log(getSqueakProfileRequest);
      client.getSqueakProfile(getSqueakProfileRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          return;
        }
        console.log(response);
        handleResponse(response.getSqueakProfile())
      });
};

export function setSqueakProfileFollowing(id, following, handleResponse) {
      console.log("called setFollowing with profileId: " + id + ", following: " + following);
      var setSqueakProfileFollowingRequest = new SetSqueakProfileFollowingRequest();
      setSqueakProfileFollowingRequest.setProfileId(id);
      setSqueakProfileFollowingRequest.setFollowing(following);
      console.log(setSqueakProfileFollowingRequest);
      client.setSqueakProfileFollowing(setSqueakProfileFollowingRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setSqueakProfileSharing(id, sharing, handleResponse) {
      console.log("called setSharing with profileId: " + id + ", sharing: " + sharing);
      var setSqueakProfileSharingRequest = new SetSqueakProfileSharingRequest();
      setSqueakProfileSharingRequest.setProfileId(id);
      setSqueakProfileSharingRequest.setSharing(sharing);
      console.log(setSqueakProfileSharingRequest);
      client.setSqueakProfileSharing(setSqueakProfileSharingRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setSqueakProfileWhitelisted(id, whitelisted, handleResponse) {
      console.log("called setWhitelisted with profileId: " + id + ", whitelisted: " + whitelisted);
      var setSqueakProfileWhitelistedRequest = new SetSqueakProfileWhitelistedRequest()
      setSqueakProfileWhitelistedRequest.setProfileId(id);
      setSqueakProfileWhitelistedRequest.setWhitelisted(whitelisted);
      console.log(setSqueakProfileWhitelistedRequest);
      client.setSqueakProfileWhitelisted(setSqueakProfileWhitelistedRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndConnectPeer(pubkey, host, handleResponse) {
  console.log("called connectPeer");
  var connectPeerRequest = new ConnectPeerRequest()
  var address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  connectPeerRequest.setAddr(address);
  console.log(connectPeerRequest);
  client.lndConnectPeer(connectPeerRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error connecting peer: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function lndDisconnectPeer(pubkey, handleResponse) {
  console.log("called disconnectPeer");
  var disconnectPeerRequest = new DisconnectPeerRequest()
  disconnectPeerRequest.setPubKey(pubkey);
  console.log(disconnectPeerRequest);
  client.lndDisconnectPeer(disconnectPeerRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error disconnecting peer: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function getPeers(handleResponse) {
  console.log("called getPeers");
  var getPeersRequest = new GetPeersRequest();
  client.getPeers(getPeersRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response.getSqueakPeersList());
  });
};

export function payOffer(offerId, handleResponse) {
  console.log("called payOffer");
  var payOfferRequest = new PayOfferRequest();
  payOfferRequest.setOfferId(offerId);
  console.log(payOfferRequest);
  client.payOffer(payOfferRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error paying offer: ' + err.message);
      return;
    }
    console.log(response);
    //goToSqueakPage(offer.getSqueakHash());
    handleResponse(response);
  });
};
