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


export async function client(endpoint, { body, ...customConfig } = {}) {
  const headers = { 'Content-Type': 'application/json' }

  const config = {
    method: body ? 'POST' : 'GET',
    ...customConfig,
    headers: {
      ...headers,
      ...customConfig.headers,
    },
  }

  if (body) {
    config.body = JSON.stringify(body)
  }

  let data
  try {
    const response = await window.fetch(endpoint, config)
    data = await response.json()
    if (response.ok) {
      return data
    }
    throw new Error(response.statusText)
  } catch (err) {
    return Promise.reject(err.message ? err.message : data)
  }
}

client.get = function (endpoint, customConfig = {}) {
  return client(endpoint, { ...customConfig, method: 'GET' })
}

client.post = function (endpoint, body, customConfig = {}) {
  return client(endpoint, { ...customConfig, body })
}


export const axiosBaseQuery =
  async ({ url, req, deser }) => {
    try {
      const data = req.serializeBinary();
      const result = await axios({ url: web_host_port + url, responseType: 'arraybuffer', method: 'post', data })
      const deserRes = deser(result.data);
      return deserRes;
    } catch (axiosError) {
      console.log('got error');
      console.log(axiosError);
      let err = axiosError
      return {
        error: { status: err.response?.status, data: err.response?.data },
      }
    }
  }


export const getTimelineSqueaks = (limit, lastSqueak) => {
    console.log('Calling getTimelineSqueaks');
    const request = new GetTimelineSqueakDisplaysRequest();
    request.setLimit(limit);
    if (lastSqueak) {
      request.setLastEntry(lastSqueak);
    }
    const deser = GetTimelineSqueakDisplaysReply.deserializeBinary;
    return axiosBaseQuery({
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
    return axiosBaseQuery({
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
    return axiosBaseQuery({
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
    return axiosBaseQuery({
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
    return axiosBaseQuery({
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
    return axiosBaseQuery({
      url: '/unlikesqueak',
      req: request,
      deser: deser,
    });
}
