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
  OpenChannelRequest,
  CloseChannelRequest,
  ChannelPoint,
  NewAddressRequest,
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
} from "../proto/squeak_admin_pb"


export function getFollowedSqueakDisplaysRequest(handleResponse) {
  console.log("called getSqueaks with handleResponse");
  var request = new GetFollowedSqueakDisplaysRequest();
  client.getFollowedSqueakDisplays(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList())
  });
};


export function lndGetInfoRequest(handleResponse) {
  console.log("called lndGetInfo");
  var request = new GetInfoRequest();
  console.log(request);
  client.lndGetInfo(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response);
  });
};

export function lndWalletBalanceRequest(handleResponse) {
      console.log("called lndWalletBalance");
      var request = new WalletBalanceRequest();
      console.log(request);
      client.lndWalletBalance(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndGetTransactionsRequest(handleResponse) {
      console.log("called lndGetTransactions");
      var request = new GetTransactionsRequest();
      console.log(request);
      client.lndGetTransactions(request, {}, (err, response) => {
        console.log(response);
        console.log("response.getTransactionsList()");
        console.log(response.getTransactionsList());
        handleResponse(response.getTransactionsList());
      });
};

export function lndListPeersRequest(handleResponse) {
      console.log("called listPeers");
      var request = new ListPeersRequest();
      console.log(request);
      client.lndListPeers(request, {}, (err, response) => {
        console.log(response);
        console.log("response.getPeersList()");
        console.log(response.getPeersList());
        handleResponse(response.getPeersList());
      });
};

export function lndListChannelsRequest(handleResponse) {
      console.log("called lndListChannels");
      var request = new ListChannelsRequest();
      console.log(request);
      client.lndListChannels(request, {}, (err, response) => {
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

export function lndPendingChannelsRequest(handleResponse) {
      console.log("called lndPendingChannels");
      var request = new PendingChannelsRequest();
      console.log(request);
      client.lndPendingChannels(request, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting pending channels: ' + err.message);
          return;
        }
        console.log(response);
        handleResponse(response);
      });
};

export function getSqueakProfileRequest(id, handleResponse) {
      console.log("called getSqueakProfile with profileId: " + id);
      var request = new GetSqueakProfileRequest();
      request.setProfileId(id);
      console.log(request);
      client.getSqueakProfile(request, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          return;
        }
        console.log(response);
        handleResponse(response.getSqueakProfile())
      });
};

export function setSqueakProfileFollowingRequest(id, following, handleResponse) {
      console.log("called setFollowing with profileId: " + id + ", following: " + following);
      var request = new SetSqueakProfileFollowingRequest();
      request.setProfileId(id);
      request.setFollowing(following);
      console.log(request);
      client.setSqueakProfileFollowing(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setSqueakProfileSharingRequest(id, sharing, handleResponse) {
      console.log("called setSharing with profileId: " + id + ", sharing: " + sharing);
      var request = new SetSqueakProfileSharingRequest();
      request.setProfileId(id);
      request.setSharing(sharing);
      console.log(request);
      client.setSqueakProfileSharing(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setSqueakProfileWhitelistedRequest(id, whitelisted, handleResponse) {
      console.log("called setWhitelisted with profileId: " + id + ", whitelisted: " + whitelisted);
      var request = new SetSqueakProfileWhitelistedRequest()
      request.setProfileId(id);
      request.setWhitelisted(whitelisted);
      console.log(request);
      client.setSqueakProfileWhitelisted(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndConnectPeer(pubkey, host, handleResponse) {
  console.log("called connectPeer");
  var request = new ConnectPeerRequest()
  var address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
  console.log(request);
  client.lndConnectPeer(request, {}, (err, response) => {
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
  var request = new DisconnectPeerRequest()
  request.setPubKey(pubkey);
  console.log(request);
  client.lndDisconnectPeer(request, {}, (err, response) => {
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
  var request = new GetPeersRequest();
  client.getPeers(request, {}, (err, response) => {
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
  var request = new PayOfferRequest();
  request.setOfferId(offerId);
  console.log(request);
  client.payOffer(request, {}, (err, response) => {
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


export function lndOpenChannelSync(pubkey, amount, handleResponse) {
  console.log("called lndOpenChannelSync");
  var request = new OpenChannelRequest()
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  console.log(request);
  client.lndOpenChannelSync(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error opening channel: ' + err.message);
      return;
    }
    console.log(response);
    console.log(response.getFundingTxidStr());
    console.log(response.getOutputIndex());
    // goToProfilePage(response.getProfileId());
    handleResponse(response);
  });
};

export function lndCloseChannel(txId, outputIndex, handleResponse) {
  console.log("called closeChannel");
  var request = new CloseChannelRequest();
  var channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  console.log(request);
  client.lndCloseChannel(request, {}, (err, response) => {
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
    var request = new GetBuyOffersRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getBuyOffers(request, {}, (err, response) => {
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
    var request = new GetBuyOfferRequest();
    request.setOfferId(offerId);
    console.log(request);
    client.getBuyOffer(request, {}, (err, response) => {
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
      var request = new GetPeerRequest();
      request.setPeerId(id);
      console.log(request);
      client.getPeer(request, {}, (err, response) => {
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
      var request = new SetPeerDownloadingRequest();
      request.setPeerId(id);
      request.setDownloading(downloading);
      console.log(request);
      client.setPeerDownloading(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setPeerUploading(id, uploading, handleResponse) {
      console.log("called setUploading with peerId: " + id + ", uploading: " + uploading);
      var request = new SetPeerUploadingRequest();
      request.setPeerId(id);
      request.setUploading(uploading);
      console.log(request);
      client.setPeerUploading(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function getSigningProfiles(handleResponse) {
  console.log("called getSigningProfiles");
  var request = new GetSigningProfilesRequest();
  client.getSigningProfiles(request, {}, (err, response) => {
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
  var request = new GetContactProfilesRequest();
  client.getContactProfiles(request, {}, (err, response) => {
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
  var request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  console.log(request);
  client.makeSqueak(request, {}, (err, response) => {
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
    var request = new GetSqueakDisplayRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getSqueakDisplay(request, {}, (err, response) => {
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
    var request = new GetAncestorSqueakDisplaysRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getAncestorSqueakDisplays(request, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error getting ancestor squeaks for hash: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getSqueakDisplayEntriesList());
      handleResponse(response.getSqueakDisplayEntriesList());
    });
};

export function getSqueakProfileByAddress(address, handleResponse) {
      var request = new GetSqueakProfileByAddressRequest();
      request.setAddress(address);
      console.log(request);
      client.getSqueakProfileByAddress(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response.getSqueakProfile());
      });
};

export function getAddressSqueakDisplays(address, handleResponse) {
    var request = new GetAddressSqueakDisplaysRequest();
    request.setAddress(address);
    console.log(request);
    client.getAddressSqueakDisplays(request, {}, (err, response) => {
      console.log(response);
      console.log(response.getSqueakDisplayEntriesList());
      handleResponse(response.getSqueakDisplayEntriesList());
    });
};

export function createContactProfile(profileName, squeakAddress, handleResponse) {
  console.log("called createContactProfile");
  var request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  console.log(request);
  client.createContactProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error creating contact profile: ' + err.message);
      return;
    }
    console.log(response);
    console.log(response.getProfileId());
    handleResponse(response);
  });
};

export function createSigningProfile(profileName, handleResponse) {
  console.log("called createSigningProfile");
  var request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  console.log(request);
  client.createSigningProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error creating signing profile: ' + err.message);
      return;
    }
    console.log(response);
    console.log(response.getProfileId());
    handleResponse(response);
  });
};

export function createPeer(peerName, host, port, handleResponse) {
  console.log("called createPeer");
  var request = new CreatePeerRequest();
  request.setPeerName(peerName);
  request.setHost(host);
  request.setPort(port);
  console.log(request);
  client.createPeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error creating peer: ' + err.message);
      return;
    }
    console.log(response);
    console.log(response.getPeerId());
    handleResponse(response);
  });
};

export function deletePeer(peerId, handleResponse) {
  console.log("called deletePeer");
  var request = new DeletePeerRequest();
  request.setPeerId(peerId);
  console.log(request);
  client.deletePeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error deleting peer: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function deleteProfile(profileId, handleResponse) {
  console.log("called deleteSqueak");
  var request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  console.log(request);
  client.deleteSqueakProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error deleting profile: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function deleteSqueak(squeakHash, handleResponse) {
  console.log("called deleteSqueak");
  var request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  console.log(request);
  client.deleteSqueak(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error deleting squeak: ' + err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function lndNewAddress(handleResponse) {
  console.log("called newAddress");
  var request = new NewAddressRequest();
  console.log(request);
  client.lndNewAddress(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      alert('Error getting new address: ' + err.message);
      return;
    }
    console.log(response);
    console.log(response.getAddress());
    // goToProfilePage(response.getProfileId());
    handleResponse(response);
  });
};
