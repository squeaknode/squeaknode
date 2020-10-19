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
  var request = new GetFollowedSqueakDisplaysRequest();
  client.getFollowedSqueakDisplays(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList())
  });
};


export function lndGetInfoRequest(handleResponse) {
  var request = new GetInfoRequest();
  console.log(request);
  client.lndGetInfo(request, {}, (err, response) => {
    console.log(response);
    handleResponse(response);
  });
};

export function lndWalletBalanceRequest(handleResponse) {
      var request = new WalletBalanceRequest();
      console.log(request);
      client.lndWalletBalance(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndGetTransactionsRequest(handleResponse) {
      var request = new GetTransactionsRequest();
      console.log(request);
      client.lndGetTransactions(request, {}, (err, response) => {
        console.log(response);
        console.log(response.getTransactionsList());
        handleResponse(response.getTransactionsList());
      });
};

export function lndListPeersRequest(handleResponse) {
      var request = new ListPeersRequest();
      console.log(request);
      client.lndListPeers(request, {}, (err, response) => {
        console.log(response);
        console.log(response.getPeersList());
        handleResponse(response.getPeersList());
      });
};

export function lndListChannelsRequest(handleResponse) {
      var request = new ListChannelsRequest();
      console.log(request);
      client.lndListChannels(request, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          return;
        }
        console.log(response);
        handleResponse(response.getChannelsList());
      });
};

export function lndPendingChannelsRequest(handleResponse) {
      var request = new PendingChannelsRequest();
      console.log(request);
      client.lndPendingChannels(request, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          return;
        }
        console.log(response);
        handleResponse(response);
      });
};

export function getSqueakProfileRequest(id, handleResponse) {
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
      var request = new SetSqueakProfileWhitelistedRequest()
      request.setProfileId(id);
      request.setWhitelisted(whitelisted);
      console.log(request);
      client.setSqueakProfileWhitelisted(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function lndConnectPeerRequest(pubkey, host, handleResponse) {
  var request = new ConnectPeerRequest()
  var address = new LightningAddress();
  address.setPubkey(pubkey);
  address.setHost(host);
  request.setAddr(address);
  console.log(request);
  client.lndConnectPeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function lndDisconnectPeerRequest(pubkey, handleResponse) {
  var request = new DisconnectPeerRequest()
  request.setPubKey(pubkey);
  console.log(request);
  client.lndDisconnectPeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function getPeersRequest(handleResponse) {
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

export function payOfferRequest(offerId, handleResponse) {
  var request = new PayOfferRequest();
  request.setOfferId(offerId);
  console.log(request);
  client.payOffer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};


export function lndOpenChannelSyncRequest(pubkey, amount, handleResponse) {
  var request = new OpenChannelRequest()
  request.setNodePubkeyString(pubkey);
  request.setLocalFundingAmount(amount);
  console.log(request);
  client.lndOpenChannelSync(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    console.log(response.getFundingTxidStr());
    console.log(response.getOutputIndex());
    handleResponse(response);
  });
};

export function lndCloseChannelRequest(txId, outputIndex, handleResponse) {
  var request = new CloseChannelRequest();
  var channelPoint = new ChannelPoint();
  channelPoint.setFundingTxidStr(txId);
  channelPoint.setOutputIndex(outputIndex);
  request.setChannelPoint(channelPoint);
  console.log(request);
  client.lndCloseChannel(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function getBuyOffersRequest(hash, handleResponse) {
    var request = new GetBuyOffersRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getBuyOffers(request, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      console.log(response.getOffersList());
      handleResponse(response.getOffersList());
    });
};

export function getBuyOfferRequest(offerId, handleResponse) {
    var request = new GetBuyOfferRequest();
    request.setOfferId(offerId);
    console.log(request);
    client.getBuyOffer(request, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      console.log(response.getOffer());
      handleResponse(response.getOffer())
    });
};

export function getPeerRequest(id, handleResponse) {
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

export function setPeerDownloadingRequest(id, downloading, handleResponse) {
      var request = new SetPeerDownloadingRequest();
      request.setPeerId(id);
      request.setDownloading(downloading);
      console.log(request);
      client.setPeerDownloading(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function setPeerUploadingRequest(id, uploading, handleResponse) {
      var request = new SetPeerUploadingRequest();
      request.setPeerId(id);
      request.setUploading(uploading);
      console.log(request);
      client.setPeerUploading(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response);
      });
};

export function getSigningProfilesRequest(handleResponse) {
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

export function getContactProfilesRequest(handleResponse) {
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

export function makeSqueakRequest(profileId, content, replyto, handleResponse) {
  var request = new MakeSqueakRequest();
  request.setProfileId(profileId);
  request.setContent(content);
  request.setReplyto(replyto);
  console.log(request);
  client.makeSqueak(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function getSqueakDisplayRequest(hash, handleResponse) {
    var request = new GetSqueakDisplayRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getSqueakDisplay(request, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      console.log(response.getSqueakDisplayEntry());
      handleResponse(response.getSqueakDisplayEntry())
    });
};

export function getAncestorSqueakDisplaysRequest(hash, handleResponse) {
    var request = new GetAncestorSqueakDisplaysRequest();
    request.setSqueakHash(hash);
    console.log(request);
    client.getAncestorSqueakDisplays(request, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      console.log(response.getSqueakDisplayEntriesList());
      handleResponse(response.getSqueakDisplayEntriesList());
    });
};

export function getSqueakProfileByAddressRequest(address, handleResponse) {
      var request = new GetSqueakProfileByAddressRequest();
      request.setAddress(address);
      console.log(request);
      client.getSqueakProfileByAddress(request, {}, (err, response) => {
        console.log(response);
        handleResponse(response.getSqueakProfile());
      });
};

export function getAddressSqueakDisplaysRequest(address, handleResponse) {
    var request = new GetAddressSqueakDisplaysRequest();
    request.setAddress(address);
    console.log(request);
    client.getAddressSqueakDisplays(request, {}, (err, response) => {
      console.log(response);
      console.log(response.getSqueakDisplayEntriesList());
      handleResponse(response.getSqueakDisplayEntriesList());
    });
};

export function createContactProfileRequest(profileName, squeakAddress, handleResponse) {
  var request = new CreateContactProfileRequest();
  request.setProfileName(profileName);
  request.setAddress(squeakAddress);
  console.log(request);
  client.createContactProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    console.log(response.getProfileId());
    handleResponse(response);
  });
};

export function createSigningProfileRequest(profileName, handleResponse) {
  var request = new CreateSigningProfileRequest();
  request.setProfileName(profileName);
  console.log(request);
  client.createSigningProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    console.log(response.getProfileId());
    handleResponse(response);
  });
};

export function createPeerRequest(peerName, host, port, handleResponse) {
  var request = new CreatePeerRequest();
  request.setPeerName(peerName);
  request.setHost(host);
  request.setPort(port);
  console.log(request);
  client.createPeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    console.log(response.getPeerId());
    handleResponse(response);
  });
};

export function deletePeerRequest(peerId, handleResponse) {
  var request = new DeletePeerRequest();
  request.setPeerId(peerId);
  console.log(request);
  client.deletePeer(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function deleteProfileRequest(profileId, handleResponse) {
  var request = new DeleteSqueakProfileRequest();
  request.setProfileId(profileId);
  console.log(request);
  client.deleteSqueakProfile(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function deleteSqueakRequest(squeakHash, handleResponse) {
  var request = new DeleteSqueakRequest();
  request.setSqueakHash(squeakHash);
  console.log(request);
  client.deleteSqueak(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    handleResponse(response);
  });
};

export function lndNewAddressRequest(handleResponse) {
  var request = new NewAddressRequest();
  console.log(request);
  client.lndNewAddress(request, {}, (err, response) => {
    if (err) {
      console.log(err.message);
      return;
    }
    console.log(response);
    console.log(response.getAddress());
    handleResponse(response);
  });
};
