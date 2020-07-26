import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import { Grid, Button } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";

import { GetSqueakDisplayRequest } from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [open, setOpen] = React.useState(false);

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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
     setOpen(false);
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
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
          <SqueakDetailItem
            key={squeak.getSqueakHash()}
            handleAddressClick={() => goToSqueakAddressPage(squeak.getAuthorAddress())}
            handleReplyClick={handleClickOpen}
            squeak={squeak}>
          </SqueakDetailItem>
        </Grid>
      </>
    )
  }

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={open}
          handleClose={handleClose}
          ></MakeSqueakDialog>
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

      {MakeSqueakDialogContent()}
    </>
  );
}
