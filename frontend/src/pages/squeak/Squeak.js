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
  getSqueakDisplayRequest,
  getAncestorSqueakDisplaysRequest,
} from "../../squeakclient/requests"


export default function SqueakPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [ancestorSqueaks, setAncestorSqueaks] = useState(null);
  const [open, setOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const getSqueak = (hash) => {
      getSqueakDisplayRequest(hash, setSqueak);
  };
  const getAncestorSqueaks = (hash) => {
      getAncestorSqueakDisplaysRequest(hash, setAncestorSqueaks);
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

  const goToBuyPage = (hash) => {
    history.push("/app/buy/" + hash);
  };

  const showDeleteDialog = (hash) => {
    handleClickOpenDeleteDialog()
  };

  const unknownAncestorHash = () => {
      if (!ancestorSqueaks) {
        return null;
      }
      var oldestKnownAncestor = ancestorSqueaks[0];
      console.log(oldestKnownAncestor);
      console.log("oldestKnownAncestor");
      return oldestKnownAncestor.getReplyTo();
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

  function UnkownReplyToContent() {
    var squeakHash = unknownAncestorHash();
    if (!squeakHash) {
      return (
        <></>
      )
    }
    return (
      <div>
          <Box
            key={squeakHash}
            >
          <SqueakThreadItem
            hash={squeakHash}
            key={squeakHash}
            handleSqueakClick={() => goToSqueakPage(squeakHash)}
            squeak={null}>
          </SqueakThreadItem>
          <Divider />
          </Box>
      </div>
    )
  }

  function AncestorsContent() {
    return (
      <div>
        {ancestorSqueaks.slice(0, -1)
          //.reverse()
          .map(ancestorSqueak =>
          <Box
            key={ancestorSqueak.getSqueakHash()}
            >
          <SqueakThreadItem
            hash={squeak.getSqueakHash()}
            key={ancestorSqueak.getSqueakHash()}
            handleAddressClick={() => goToSqueakAddressPage(ancestorSqueak.getAuthorAddress())}
            handleSqueakClick={() => goToSqueakPage(ancestorSqueak.getSqueakHash())}
            squeak={ancestorSqueak}>
          </SqueakThreadItem>
          <Divider />
          </Box>
        )}
      </div>
    )
  }

  function SqueakContent() {
    return (
      <>
        {UnkownReplyToContent()}
        {AncestorsContent()}
        <div>
          <SqueakDetailItem
            key={squeak.getSqueakHash()}
            handleAddressClick={() => goToSqueakAddressPage(squeak.getAuthorAddress())}
            handleReplyClick={handleClickOpen}
            handleDeleteClick={showDeleteDialog}
            handleUnlockClick={() => goToBuyPage(squeak.getSqueakHash())}
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
