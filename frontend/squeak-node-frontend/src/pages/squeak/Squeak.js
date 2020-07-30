import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";

import {
  GetSqueakDisplayRequest,
  GetAncestorSqueakDisplaysRequest,
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [ancestorSqueaks, setAncestorSqueaks] = useState(null);
  const [open, setOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

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
  const getAncestorSqueaks = (hash) => {
      var getAncestorSqueakDisplaysRequest = new GetAncestorSqueakDisplaysRequest()
      getAncestorSqueakDisplaysRequest.setSqueakHash(hash);
      console.log(getAncestorSqueakDisplaysRequest);

      client.getAncestorSqueakDisplays(getAncestorSqueakDisplaysRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting ancestor squeaks for hash: ' + err.message);
          return;
        }
        console.log(response);
        console.log(response.getSqueakDisplayEntriesList());
        setAncestorSqueaks(response.getSqueakDisplayEntriesList())
      });
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
     setOpen(false);
  };

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log("deleteDialogOpen: " + deleteDialogOpen);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
  };

  const showDeleteDialog = (hash) => {
    handleClickOpenDeleteDialog()
  };

  useEffect(()=>{
    getSqueak(hash)
  },[hash]);
  useEffect(()=>{
    getAncestorSqueaks(hash)
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
        <div>
          {ancestorSqueaks.slice(0, -1)
            //.reverse()
            .map(ancestorSqueak =>
            <Box
              key={ancestorSqueak.getSqueakHash()}
              >
            <SqueakThreadItem
              key={ancestorSqueak.getSqueakHash()}
              handleAddressClick={() => goToSqueakAddressPage(ancestorSqueak.getAuthorAddress())}
              handleSqueakClick={() => goToSqueakPage(ancestorSqueak.getSqueakHash())}
              squeak={ancestorSqueak}>
            </SqueakThreadItem>
            <Divider />
            </Box>
          )}
        </div>
        <div>
          <SqueakDetailItem
            key={squeak.getSqueakHash()}
            handleAddressClick={() => goToSqueakAddressPage(squeak.getAuthorAddress())}
            handleReplyClick={handleClickOpen}
            handleDeleteClick={showDeleteDialog}
            squeak={squeak}>
          </SqueakDetailItem>
        </div>
        {MakeSqueakDialogContent()}
        {DeleteSqueakDialogContent()}
      </>
    )
  }

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={open}
          handleClose={handleClose}
          replytoSqueak={squeak}
          ></MakeSqueakDialog>
      </>
    )
  }

  function DeleteSqueakDialogContent() {
    return (
      <>
        <DeleteSqueakDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          squeakToDelete={squeak}
          ></DeleteSqueakDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Squeak" />
      {(squeak && ancestorSqueaks)
        ? SqueakContent()
        : NoSqueakContent()
      }
    </>
  );
}
