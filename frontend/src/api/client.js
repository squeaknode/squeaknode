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
