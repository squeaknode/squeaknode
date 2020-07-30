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
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [state, setState] = useState({
    gilad: true,
    jason: false,
    antoine: true,
  });

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


  useEffect(()=>{
    getSqueakProfile(id)
  },[id]);

  const handleSettingsFollowingChange = (event) => {
    console.log("Settings changed for profile id: " + id);
    console.log("Following changed to: " + event.target.checked);
    setFollowing(id, event.target.checked);
  };

  const handleSettingsChange = (event) => {
    console.log("Settings changed...");
    setState({ ...state, [event.target.name]: event.target.checked });
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
            control={<Switch checked={squeakProfile.getShared()} onChange={handleSettingsChange} />}
            label="Shared"
          />
          <FormControlLabel
            control={<Switch checked={squeakProfile.getWhitelisted()} onChange={handleSettingsChange} />}
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
