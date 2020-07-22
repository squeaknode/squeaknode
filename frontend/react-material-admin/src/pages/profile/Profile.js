import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Grid } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import { GetSqueakProfileRequest } from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);

  const getSqueakProfile = () => {
        console.log("called getSqueakProfile with profileId: " + id);

        var getSqueaksRequest = new GetSqueakProfileRequest()
        getSqueaksRequest.setProfileId(id);
        console.log(getSqueaksRequest);

        client.getSqueakProfile(getSqueaksRequest, {}, (err, response) => {
          console.log(err);
          console.log(response);
          console.log(response.getSqueakProfile());
          // console.log(response.getSqueakDisplayEntriesList(),length);
          setSqueakProfile(response.getSqueakProfile())
        });
  };
  useEffect(()=>{
    getSqueakProfile()
  },[]);

  function NoProfileContent() {
    return (
      <p>
        No profile loaded
      </p>
    )
  }

  function ProfileContent() {
    return (
      <p>
        Profile name: {squeakProfile.getProfileName()}
      </p>
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
