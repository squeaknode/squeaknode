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
import Squeak from "../../components/Squeak";
import { Typography } from "../../components/Wrappers";

import { GetInfoRequest, WalletBalanceRequest } from "../../proto/lnd_pb"
import {HelloRequest, GetFollowedSqueakDisplaysRequest, GetSigningProfilesRequest} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function TimelinePage() {
  var classes = useStyles();
  var theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const history = useHistory();

  const getSqueaks = () => {
    console.log("called getSqueaks");
    var getSqueaksRequest = new GetFollowedSqueakDisplaysRequest()
    client.getFollowedSqueakDisplays(getSqueaksRequest, {}, (err, response) => {
      console.log(response);
      setSqueaks(response.getSqueakDisplayEntriesList())
    });
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  useEffect(()=>{
    getSqueaks()
  },[]);

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
          <Squeak
            key={squeak.getSqueakHash()}
            squeak={squeak}
            handleAddressClick={() => goToSqueakAddressPage(squeak.getAuthorAddress())}>
          </Squeak>
        )}
        </Grid>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Timeline" />
      {(squeaks)
        ? SqueaksContent()
        : NoSqueaksContent()
      }
    </>
  );
}
