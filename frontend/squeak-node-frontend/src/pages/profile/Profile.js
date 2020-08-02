import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Grid,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  FormHelperText,
  Switch,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";

import {
  GetSqueakProfileRequest,
  SetSqueakProfileFollowingRequest,
  SetSqueakProfileSharingRequest,
  SetSqueakProfileWhitelistedRequest,
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);

  const getSqueakProfile = (id) => {
        console.log("called getSqueakProfile with profileId: " + id);
        var getSqueakProfileRequest = new GetSqueakProfileRequest()
        getSqueakProfileRequest.setProfileId(id);
        console.log(getSqueakProfileRequest);
        client.getSqueakProfile(getSqueakProfileRequest, {}, (err, response) => {
          console.log(response);
          setSqueakProfile(response.getSqueakProfile())
        });
  };
  const setFollowing = (id, following) => {
        console.log("called setFollowing with profileId: " + id + ", following: " + following);
        var setSqueakProfileFollowingRequest = new SetSqueakProfileFollowingRequest()
        setSqueakProfileFollowingRequest.setProfileId(id);
        setSqueakProfileFollowingRequest.setFollowing(following);
        console.log(setSqueakProfileFollowingRequest);
        client.setSqueakProfileFollowing(setSqueakProfileFollowingRequest, {}, (err, response) => {
          console.log(response);
          getSqueakProfile(id);
        });
  };
  const setSharing = (id, sharing) => {
        console.log("called setSharing with profileId: " + id + ", sharing: " + sharing);
        var setSqueakProfileSharingRequest = new SetSqueakProfileSharingRequest()
        setSqueakProfileSharingRequest.setProfileId(id);
        setSqueakProfileSharingRequest.setSharing(sharing);
        console.log(setSqueakProfileSharingRequest);
        client.setSqueakProfileSharing(setSqueakProfileSharingRequest, {}, (err, response) => {
          console.log(response);
          getSqueakProfile(id);
        });
  };
  const setWhitelisted = (id, whitelisted) => {
        console.log("called setWhitelisted with profileId: " + id + ", whitelisted: " + whitelisted);
        var setSqueakProfileWhitelistedRequest = new SetSqueakProfileWhitelistedRequest()
        setSqueakProfileWhitelistedRequest.setProfileId(id);
        setSqueakProfileWhitelistedRequest.setWhitelisted(whitelisted);
        console.log(setSqueakProfileWhitelistedRequest);
        client.setSqueakProfileWhitelisted(setSqueakProfileWhitelistedRequest, {}, (err, response) => {
          console.log(response);
          getSqueakProfile(id);
        });
  };


  useEffect(()=>{
    getSqueakProfile(id)
  },[id]);

  const handleSettingsFollowingChange = (event) => {
    console.log("Following changed for profile id: " + id);
    console.log("Following changed to: " + event.target.checked);
    setFollowing(id, event.target.checked);
  };

  const handleSettingsSharingChange = (event) => {
    console.log("Sharing changed for profile id: " + id);
    console.log("Sharing changed to: " + event.target.checked);
    setSharing(id, event.target.checked);
  };

  const handleSettingsWhitelistedChange = (event) => {
    console.log("Whitelisted changed for profile id: " + id);
    console.log("Whitelisted changed to: " + event.target.checked);
    setWhitelisted(id, event.target.checked);
  };

  function NoProfileContent() {
    return (
      <p>
        No profile loaded
      </p>
    )
  }

  function ProfileContent() {
    return (
      <>
        <p>
          Profile name: {squeakProfile.getProfileName()}
        </p>
        {ProfileSettingsForm()}
      </>
    )
  }

  function ProfileSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Profile settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={squeakProfile.getFollowing()} onChange={handleSettingsFollowingChange} />}
            label="Following"
          />
          <FormControlLabel
            control={<Switch checked={squeakProfile.getSharing()} onChange={handleSettingsSharingChange} />}
            label="Sharing"
          />
          <FormControlLabel
            control={<Switch checked={squeakProfile.getWhitelisted()} onChange={handleSettingsWhitelistedChange} />}
            label="Whitelisted"
          />
        </FormGroup>
      </FormControl>
    )
  }

  return (
    <>
      <PageTitle title={'Squeak Profile: ' + (squeakProfile ? squeakProfile.getProfileName() : null)} />
      <div>
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()
      }
      </div>
    </>
  );
}
