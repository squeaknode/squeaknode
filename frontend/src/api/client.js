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
  GetSqueakProfileByPubKeyRequest,
  GetPubKeySqueakDisplaysRequest,
  CreateContactProfileRequest,
  CreateSigningProfileRequest,
  ImportSigningProfileRequest,
  CreatePeerRequest,
  DeletePeerRequest,
  DeleteSqueakProfileRequest,
  DeleteSqueakRequest,
  DownloadSqueakRequest,
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
  DownloadPubKeySqueaksRequest,
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
  GetPubKeySqueakDisplaysReply,
  GetSqueakProfileByPubKeyReply,
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
  DownloadPubKeySqueaksReply,
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
  ClearSellPriceRequest,
  ClearSellPriceReply,
  GetTwitterStreamStatusRequest,
  GetTwitterStreamStatusReply,
  DecryptSqueakRequest,
  DecryptSqueakReply,
} from '../proto/squeak_admin_pb';

import axios from 'axios'

// A tiny wrapper around fetch(), borrowed from
// https://kentcdodds.com/blog/replace-axios-with-a-simple-custom-fetch-wrapper

console.log('The value of REACT_APP_DEV_MODE_ENABLED is:', Boolean(process.env.REACT_APP_DEV_MODE_ENABLED));
const DEV_MODE_ENABLED = process.env.REACT_APP_DEV_MODE_ENABLED;

console.log('The value of REACT_APP_SERVER_PORT is:', process.env.REACT_APP_SERVER_PORT);
const SERVER_PORT = process.env.REACT_APP_SERVER_PORT || window.location.port;

export const web_host_port = `${window.location.protocol}//${window.location.hostname}:${SERVER_PORT}`;

export const baseRequest =
  async ({ url, req, deser }) => {
    try {
      const data = req.serializeBinary();
      // const result = await axios({ url: web_host_port + url, responseType: 'arraybuffer', method: 'post', data })
      const result = await fetch(web_host_port + url, {
        method: 'post',
        body: data,
      });
      if (!result.ok) { throw result; }
      const buf = await result.arrayBuffer();
      const deserRes = deser(buf);
      return deserRes;
    } catch (axiosError) {
      const errorText = await axiosError.text();
      throw errorText;
    }
  }

export const getNetwork = () => {
    console.log('Calling getNetwork');
    const request = new GetNetworkRequest();
    const deser = GetNetworkReply.deserializeBinary;
    return baseRequest({
      url: '/getnetwork',
      req: request,
      deser: deser,
    });
}

export const getTimelineSqueaks = (limit, lastSqueak) => {
    console.log('Calling getTimelineSqueaks');
    const request = new GetTimelineSqueakDisplaysRequest();
    request.setLimit(limit);
    if (lastSqueak) {
      request.setLastEntry(lastSqueak);
    }
    const deser = GetTimelineSqueakDisplaysReply.deserializeBinary;
    return baseRequest({
      url: '/gettimelinesqueakdisplays',
      req: request,
      deser: deser,
    });
}

export const getSqueak = (squeakHash) => {
    console.log('Calling getSqueak');
    const request = new GetSqueakDisplayRequest();
    request.setSqueakHash(squeakHash);
    const deser = GetSqueakDisplayReply.deserializeBinary;
    return baseRequest({
      url: '/getsqueakdisplay',
      req: request,
      deser: deser,
    });
}

export const getAncestorSqueaks = (squeakHash) => {
    console.log('Calling getAncestorSqueaks');
    const request = new GetAncestorSqueakDisplaysRequest();
    request.setSqueakHash(squeakHash);
    const deser = GetAncestorSqueakDisplaysReply.deserializeBinary;
    return baseRequest({
      url: '/getancestorsqueakdisplays',
      req: request,
      deser: deser,
    });
}

export const getReplySqueaks = (squeakHash, limit, lastSqueak) => {
    console.log('Calling getAncestorSqueaks');
    const request = new GetReplySqueakDisplaysRequest();
    request.setSqueakHash(squeakHash);
    request.setLimit(limit);
    if (lastSqueak) {
      request.setLastEntry(lastSqueak);
    }
    const deser = GetReplySqueakDisplaysReply.deserializeBinary;
    return baseRequest({
      url: '/getreplysqueakdisplays',
      req: request,
      deser: deser,
    });
}

export const getProfileSqueaks = (pubkey, limit, lastSqueak) => {
    console.log('Calling getProfileSqueaks');
    const request = new GetPubKeySqueakDisplaysRequest();
    request.setPubkey(pubkey);
    request.setLimit(limit);
    if (lastSqueak) {
      request.setLastEntry(lastSqueak);
    }
    const deser = GetPubKeySqueakDisplaysReply.deserializeBinary;
    return baseRequest({
      url: '/getpubkeysqueakdisplays',
      req: request,
      deser: deser,
    });
}

export const likeSqueak = (squeakHash) => {
    console.log('Calling likeSqueak');
    const request = new LikeSqueakRequest();
    request.setSqueakHash(squeakHash);
    const deser = LikeSqueakReply.deserializeBinary;
    return baseRequest({
      url: '/likesqueak',
      req: request,
      deser: deser,
    });
}

export const unlikeSqueak = (squeakHash) => {
    console.log('Calling unlikeSqueak');
    const request = new UnlikeSqueakRequest();
    request.setSqueakHash(squeakHash);
    const deser = UnlikeSqueakReply.deserializeBinary;
    return baseRequest({
      url: '/unlikesqueak',
      req: request,
      deser: deser,
    });
}

export const deleteSqueak = (squeakHash) => {
    console.log('Calling deleteSqueak');
    const request = new DeleteSqueakRequest();
    request.setSqueakHash(squeakHash);
    const deser = DeleteSqueakReply.deserializeBinary;
    return baseRequest({
      url: '/deletesqueak',
      req: request,
      deser: deser,
    });
}

export const makeSqueak = (profileId, content, replyTo, hasRecipient, recipientProfileId) => {
    console.log('Calling makeSqueak');
    const request = new MakeSqueakRequest();
    request.setProfileId(profileId);
    request.setContent(content);
    request.setReplyto(replyTo);
    request.setHasRecipient(hasRecipient);
    request.setRecipientProfileId(recipientProfileId);
    const deser = MakeSqueakReply.deserializeBinary;
    return baseRequest({
      url: '/makesqueakrequest',
      req: request,
      deser: deser,
    });
}

export const getSigningProfiles = () => {
    console.log('Calling getSigningProfiles');
    const request = new GetSigningProfilesRequest();
    const deser = GetSigningProfilesReply.deserializeBinary;
    return baseRequest({
      url: '/getsigningprofiles',
      req: request,
      deser: deser,
    });
}

export const getContactProfiles = () => {
    console.log('Calling getContactProfiles');
    const request = new GetContactProfilesRequest();
    const deser = GetContactProfilesReply.deserializeBinary;
    return baseRequest({
      url: '/getcontactprofiles',
      req: request,
      deser: deser,
    });
}

export const getPaymentSummary = () => {
    console.log('Calling getPaymentSummary');
    const request = new GetPaymentSummaryRequest();
    const deser = GetPaymentSummaryReply.deserializeBinary;
    return baseRequest({
      url: '/getpaymentsummary',
      req: request,
      deser: deser,
    });
}

export const getSentPayments = (limit, lastSentPayment) => {
    console.log('Calling getSentPayments');
    const request = new GetSentPaymentsRequest();
    request.setLimit(limit);
    if (lastSentPayment) {
      request.setLastSentPayment(lastSentPayment);
    }
    const deser = GetSentPaymentsReply.deserializeBinary;
    return baseRequest({
      url: '/getsentpayments',
      req: request,
      deser: deser,
    });
}

export const getReceivedPayments = (limit, lastReceivedPayment) => {
    console.log('Calling getSentPayments');
    const request = new GetReceivedPaymentsRequest();
    request.setLimit(limit);
    if (lastReceivedPayment) {
      request.setLastReceivedPayment(lastReceivedPayment);
    }
    const deser = GetReceivedPaymentsReply.deserializeBinary;
    return baseRequest({
      url: '/getreceivedpayments',
      req: request,
      deser: deser,
    });
}

export const getSearchSqueaks = (searchText, limit, lastSqueak) => {
    console.log('Calling getSearchSqueaks');
    const request = new GetSearchSqueakDisplaysRequest();
    request.setSearchText(searchText);
    request.setLimit(limit);
    if (lastSqueak) {
      request.setLastEntry(lastSqueak);
    }
    const deser = GetSearchSqueakDisplaysReply.deserializeBinary;
    return baseRequest({
      url: '/getsearchsqueakdisplays',
      req: request,
      deser: deser,
    });
}

export const createSigningProfile = (profileName) => {
    console.log('Calling createSigningProfile');
    const request = new CreateSigningProfileRequest();
    request.setProfileName(profileName);
    const deser = CreateSigningProfileReply.deserializeBinary;
    return baseRequest({
      url: '/createsigningprofile',
      req: request,
      deser: deser,
    });
}

export const importSigningProfile = (profileName, privateKey) => {
    console.log('Calling importSigningProfile');
    const request = new ImportSigningProfileRequest();
    request.setProfileName(profileName);
    request.setPrivateKey(privateKey);
    const deser = ImportSigningProfileReply.deserializeBinary;
    return baseRequest({
      url: '/importsigningprofile',
      req: request,
      deser: deser,
    });
}

export const createContactProfile = (profileName, pubkey) => {
    console.log('Calling createContactProfile');
    const request = new CreateContactProfileRequest();
    request.setProfileName(profileName);
    request.setPubkey(pubkey);
    const deser = CreateContactProfileReply.deserializeBinary;
    return baseRequest({
      url: '/createcontactprofile',
      req: request,
      deser: deser,
    });
}

export const getProfile = (id) => {
    console.log('Calling getProfile');
    const request = new GetSqueakProfileRequest();
    request.setProfileId(id);
    const deser = GetSqueakProfileReply.deserializeBinary;
    return baseRequest({
      url: '/getsqueakprofile',
      req: request,
      deser: deser,
    });
}

export const getProfileByPubkey = (pubkey) => {
    console.log('Calling getProfileByPubkey');
    const request = new GetSqueakProfileByPubKeyRequest();
    request.setPubkey(pubkey);
    const deser = GetSqueakProfileByPubKeyReply.deserializeBinary;
    return baseRequest({
      url: '/getsqueakprofilebypubkey',
      req: request,
      deser: deser,
    });
}

export const setProfileFollowing = (id, following) => {
    console.log('Calling setProfileFollowing');
    const request = new SetSqueakProfileFollowingRequest();
    request.setProfileId(id);
    request.setFollowing(following);
    const deser = SetSqueakProfileFollowingReply.deserializeBinary;
    return baseRequest({
      url: '/setsqueakprofilefollowing',
      req: request,
      deser: deser,
    });
}

export const deleteProfile = (id) => {
    console.log('Calling deleteProfile');
    const request = new DeleteSqueakProfileRequest();
    request.setProfileId(id);
    const deser = DeleteSqueakProfileReply.deserializeBinary;
    return baseRequest({
      url: '/deleteprofile',
      req: request,
      deser: deser,
    });
}

export const renameProfile = (id, profileName) => {
    console.log('Calling renameProfile');
    const request = new RenameSqueakProfileRequest();
    request.setProfileId(id);
    request.setProfileName(profileName);
    const deser = RenameSqueakProfileReply.deserializeBinary;
    return baseRequest({
      url: '/renamesqueakprofile',
      req: request,
      deser: deser,
    });
}

export const changeProfileImage = (id, imageBase64) => {
    console.log('Calling changeProfileImage');
    const request = new SetSqueakProfileImageRequest();
    request.setProfileId(id);
    request.setProfileImage(imageBase64);
    const deser = SetSqueakProfileImageReply.deserializeBinary;
    return baseRequest({
      url: '/setsqueakprofileimage',
      req: request,
      deser: deser,
    });
}

export const clearProfileImage = (id, imageBase64) => {
    console.log('Calling clearProfileImage');
    const request = new ClearSqueakProfileImageRequest();
    request.setProfileId(id);
    const deser = ClearSqueakProfileImageReply.deserializeBinary;
    return baseRequest({
      url: '/clearsqueakprofileimage',
      req: request,
      deser: deser,
    });
}

export const getPrivateKey = (id) => {
    console.log('Calling getProfilePrivateKey');
    const request = new GetSqueakProfilePrivateKeyRequest();
    request.setProfileId(id);
    const deser = GetSqueakProfilePrivateKeyReply.deserializeBinary;
    return baseRequest({
      url: '/getsqueakprofileprivatekey',
      req: request,
      deser: deser,
    });
}

export const getPeer = (network, host, port) => {
    console.log('Calling getPeer');
    const request = new GetPeerByAddressRequest();
    const peerAddress = new PeerAddress();
    peerAddress.setNetwork(network);
    peerAddress.setHost(host);
    peerAddress.setPort(port);
    request.setPeerAddress(peerAddress);
    const deser = GetPeerByAddressReply.deserializeBinary;
    return baseRequest({
      url: '/getpeerbyaddress',
      req: request,
      deser: deser,
    });
}
