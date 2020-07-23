import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import { Grid, Button } from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import {
  ResponsiveContainer,
  ComposedChart,
  AreaChart,
  LineChart,
  Line,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import { Typography } from "../../components/Wrappers";

import { GetInfoRequest } from "../../proto/lnd_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function LightningPage() {
  var classes = useStyles();
  var theme = useTheme();

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

  function InfoContentOld() {
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

  function InfoContent() {
    return (
      <>
         {PubkeyGridItem()}
         {StatusGridItem()}
      </>
    )
  }

  function StatusGridItem() {
    return (
      <Grid container spacing={4}>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Node status"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  synced to chain
                </Typography>
                <Typography size="md">{lndInfo.getSyncedToChain().toString()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  synced to graph
                </Typography>
                <Typography size="md">{lndInfo.getSyncedToGraph().toString()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  block height
                </Typography>
                <Typography size="md">{lndInfo.getBlockHeight()}</Typography>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
      </Grid>
    )
  }

  function PubkeyGridItem() {
    return (
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget
            title="Node pubkey"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <div className={classes.visitsNumberContainer}>
              <Typography size="xl" weight="medium">
                {lndInfo.getIdentityPubkey()}
              </Typography>

            </div>
          </Widget>
        </Grid>
      </Grid>
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
