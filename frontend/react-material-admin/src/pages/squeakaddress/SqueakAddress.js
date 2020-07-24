import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import { Grid, Button } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import Squeak from "../../components/Squeak";

import {
   GetAddressSqueakDisplaysRequest,
   GetSqueakProfileByAddressRequest,
   GetSqueakProfileRequest } from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SqueakAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);

  const getSqueakProfile = () => {
        var getSqueakProfileByAddressRequest = new GetSqueakProfileByAddressRequest()
        getSqueakProfileByAddressRequest.setAddress(address);
        console.log(getSqueakProfileByAddressRequest);

        client.getSqueakProfileByAddress(getSqueakProfileByAddressRequest, {}, (err, response) => {
          console.log(response);
          setSqueakProfile(response.getSqueakProfile())
        });
  };
  const getSqueaks = () => {
      var getAddressSqueakDisplaysRequest = new GetAddressSqueakDisplaysRequest()
      getAddressSqueakDisplaysRequest.setAddress(address);
      console.log(getAddressSqueakDisplaysRequest);

      client.getAddressSqueakDisplays(getAddressSqueakDisplaysRequest, {}, (err, response) => {
        console.log(response);
        console.log(response.getSqueakDisplayEntriesList());
        setSqueaks(response.getSqueakDisplayEntriesList())
      });
};

  const goToCreateProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  useEffect(()=>{
    getSqueakProfile()
  },[]);
  useEffect(()=>{
    getSqueaks()
  },[]);

  function NoProfileContent() {
    return (
      <div>
        No profile loaded
      </div>
    )
  }

  function ProfileContent() {
    return (
      <div className={classes.root}>
        Profile:
        <Button variant="contained" onClick={() => {
            goToCreateProfilePage(squeakProfile.getProfileId());
          }}>{squeakProfile.getProfileName()}</Button>
      </div>
    )
  }

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    )
  }

  function SqueaksContent() {
    return (
      <>
        <Grid container spacing={4} >
          {squeaks.map(squeak =>
            <Squeak key={squeak.getSqueakHash()} squeak={squeak}></Squeak>
          )}
          </Grid>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Squeak Address: ' + address} />
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()
      }
      {(squeaks)
        ? SqueaksContent()
        : NoSqueaksContent()
      }
    </>
  );
}
