import { client } from "../squeakclient/squeakclient"

import {
  GetFollowedSqueakDisplaysRequest,
  GetSigningProfilesRequest,
} from "../proto/squeak_admin_pb"


export function getFollowedSqueaks(handleResponse) {
  console.log("called getSqueaks with handleResponse");
  var getFollowedSqueakDisplaysRequest = new GetFollowedSqueakDisplaysRequest()
  client.getFollowedSqueakDisplays(getFollowedSqueakDisplaysRequest, {}, (err, response) => {
    console.log(response);
    handleResponse(response.getSqueakDisplayEntriesList())
  });
};
