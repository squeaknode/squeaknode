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
  CloseChannelRequest,
  ChannelPoint,
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

export function lndCloseChannel(txId, outputIndex, handleResponse) {
  console.log("called closeChannel");
  var closeChannelRequest = new CloseChannelRequest();
  var channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  closeChannelRequest.setChannelPoint(channelPoint);
  console.log(closeChannelRequest);
  client.lndCloseChannel(closeChannelRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error closing channel: ' + err.message);
      return;
    }
    console.log(response);
    // goToProfilePage(response.getProfileId());
    handleResponse(response);
  });
};

export function getBuyOffers(hash, handleResponse) {
    var getBuyOffersRequest = new GetBuyOffersRequest();
    getBuyOffersRequest.setSqueakHash(hash);
    console.log(getBuyOffersRequest);
    client.getBuyOffers(getBuyOffersRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error getting offers: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getOffersList());
      handleResponse(response.getOffersList());
    });
};

export function getBuyOffer(offerId, handleResponse) {
    console.log("Getting offer with offerId: " + offerId);
    var getBuyOfferRequest = new GetBuyOfferRequest();
    getBuyOfferRequest.setOfferId(offerId);
    console.log(getBuyOfferRequest);
    client.getBuyOffer(getBuyOfferRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error getting offer: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getOffer());
      handleResponse(response.getOffer())
    });
};

export function getPeer(id, handleResponse) {
      console.log("called getPeer with peerId: " + id);
      var getPeerRequest = new GetPeerRequest();
      getPeerRequest.setPeerId(id);
      console.log(getPeerRequest);
      client.getPeer(getPeerRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          return;
        }
        console.log(response);
        handleResponse(response.getSqueakPeer())
      });
};

export function setPeerDownloading(id, downloading, handleResponse) {
      console.log("called setDownloading with peerId: " + id + ", downloading: " + downloading);
      var setPeerDownloadingRequest = new SetPeerDownloadingRequest();
      setPeerDownloadingRequest.setPeerId(id);
      setPeerDownloadingRequest.setDownloading(downloading);
      console.log(setPeerDownloadingRequest);
      client.setPeerDownloading(setPeerDownloadingRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setPeerUploading(id, uploading, handleResponse) {
      console.log("called setUploading with peerId: " + id + ", uploading: " + uploading);
      var setPeerUploadingRequest = new SetPeerUploadingRequest();
      setPeerUploadingRequest.setPeerId(id);
      setPeerUploadingRequest.setUploading(uploading);
      console.log(setPeerUploadingRequest);
      client.setPeerUploading(setPeerUploadingRequest, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function getSigningProfiles(handleResponse) {
  console.log("called getSigningProfiles");
  var getSigningProfilesRequest = new GetSigningProfilesRequest();
  client.getSigningProfiles(getSigningProfilesRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response.getSqueakProfilesList());
  });
};

export function getContactProfiles(handleResponse) {
  console.log("called getContactProfiles");
  var getContactProfilesRequest = new GetContactProfilesRequest();
  client.getContactProfiles(getContactProfilesRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response.getSqueakProfilesList());
  });
};

export function makeSqueak(profileId, content, replyto, handleResponse) {
  console.log("called makeSqueak");
  var makeSqueakRequest = new MakeSqueakRequest();
  makeSqueakRequest.setProfileId(profileId);
  makeSqueakRequest.setContent(content);
  makeSqueakRequest.setReplyto(replyto);
  console.log(makeSqueakRequest);
  client.makeSqueak(makeSqueakRequest, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error making squeak: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function getSqueakDisplay(hash, handleResponse) {
    var getSqueakDisplayRequest = new GetSqueakDisplayRequest();
    getSqueakDisplayRequest.setSqueakHash(hash);
    console.log(getSqueakDisplayRequest);
    client.getSqueakDisplay(getSqueakDisplayRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error getting squeak with hash: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getSqueakDisplayEntry());
      handleResponse(response.getSqueakDisplayEntry())
    });
};

export function getAncestorSqueakDisplays(hash, handleResponse) {
    var getAncestorSqueakDisplaysRequest = new GetAncestorSqueakDisplaysRequest();
    getAncestorSqueakDisplaysRequest.setSqueakHash(hash);
    console.log(getAncestorSqueakDisplaysRequest);
    client.getAncestorSqueakDisplays(getAncestorSqueakDisplaysRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error getting ancestor squeaks for hash: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getSqueakDisplayEntriesList());
      handleResponse(response.getSqueakDisplayEntriesList())
    });
};
