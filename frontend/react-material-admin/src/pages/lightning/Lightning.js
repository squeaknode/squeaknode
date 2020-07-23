import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import { Grid, Button } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
// import { Typography } from "../../components/Wrappers";

import { GetInfoRequest } from "../../proto/lnd_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function LightningPage() {
  var classes = useStyles();
  const [lndInfo, setLndInfo] = useState(null);

  const getLndInfo = () => {
        console.log("called getLndInfo");

        var getInfoRequest = new GetInfoRequest()
        console.log(getInfoRequest);

        client.lndGetInfo(getInfoRequest, {}, (err, response) => {
          console.log(response);
          console.log(response.getColor());
          setLndInfo(response);
        });
  };

  useEffect(()=>{
    getLndInfo()
  },[]);

  function NoInfoContent() {
    return (
      <div>
        No info
      </div>
    )
  }

  function InfoContent() {
    return (
      <div>
        <p>identity_pubkey: {lndInfo.getIdentityPubkey()}</p>
        <p>alias: {lndInfo.getAlias()}</p>
        <p>num_pending_channels: {lndInfo.getNumPendingChannels()}</p>
        <p>num_active_channels: {lndInfo.getNumActiveChannels()}</p>
        <p>num_inactive_channels: {lndInfo.getNumInactiveChannels()}</p>
        <p>num_peers: {lndInfo.getNumPeers()}</p>
        <p>block_height: {lndInfo.getBlockHeight()}</p>
        <p>block_hash: {lndInfo.getBlockHash()}</p>
        <p>synced_to_chain: {lndInfo.getSyncedToChain().toString()}</p>
        <p>synced_to_graph: {lndInfo.getSyncedToGraph().toString()}</p>
      </div>
    )
  }

  return (
    <>
      <PageTitle title="Lightning" />
      {lndInfo
        ? InfoContent()
        : NoInfoContent()
      }
    </>
  );
}
