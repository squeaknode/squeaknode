import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
   Grid,
   Button,
   Box,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
   GetAddressSqueakDisplaysRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function LightningNodePage() {
  var classes = useStyles();
  const history = useHistory();
  const { pubkey, host } = useParams();


  function NoPubkeyContent() {
    return (
      <div>
        No pubkey.
      </div>
    )
  }

  function PubkeyContent() {
    return (
      <div className={classes.root}>
        pubkey:
        <Button variant="contained">{pubkey}</Button>
        host:
        <Button variant="contained">{host}</Button>
      </div>
    )
  }

  return (
    <>
      <PageTitle title={'Lightning Node: ' + pubkey} />
      {pubkey
        ? PubkeyContent()
        : NoPubkeyContent()
      }
    </>
  );
}
