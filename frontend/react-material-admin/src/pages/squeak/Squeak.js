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

import { GetSqueakDisplayRequest } from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);

  const getSqueak = (hash) => {
      var getSqueakDisplayRequest = new GetSqueakDisplayRequest()
      getSqueakDisplayRequest.setSqueakHash(hash);
      console.log(getSqueakDisplayRequest);

      client.getSqueakDisplay(getSqueakDisplayRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting squeak with hash: ' + err.message);
          return;
        }
        console.log(response);
        console.log(response.getSqueakDisplayEntry());
        setSqueak(response.getSqueakDisplayEntry())
      });
};

  const goToCreateProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  useEffect(()=>{
    getSqueak(hash)
  },[hash]);

  function NoSqueakContent() {
    return (
      <div>
        Unable to load squeak.
      </div>
    )
  }

  function SqueakContent() {
    return (
      <>
        <Grid container spacing={4} >
          <Squeak
            key={squeak.getSqueakHash()}
            squeak={squeak}>
          </Squeak>
        </Grid>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Squeak" />
      {squeak
        ? SqueakContent()
        : NoSqueakContent()
      }
    </>
  );
}
