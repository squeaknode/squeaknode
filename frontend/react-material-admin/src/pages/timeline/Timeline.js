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

import { GetInfoRequest, WalletBalanceRequest } from "../../proto/lnd_pb"
import {HelloRequest, GetFollowedSqueakDisplaysRequest, GetSigningProfilesRequest} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function TimelinePage() {
  var classes = useStyles();
  var theme = useTheme();

  const [squeaks, setSqueaks] = useState([]);

  const getSqueaks = () => {
    console.log("called getSqueaks");

    var getSqueaksRequest = new GetFollowedSqueakDisplaysRequest()

    client.getFollowedSqueakDisplays(getSqueaksRequest, {}, (err, response) => {
      console.log(response);
      setSqueaks(response.getSqueakDisplayEntriesList())
    });
  };

  useEffect(()=>{
    getSqueaks()
  },[]);

  function NoInfoContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    )
  }

  function InfoContent() {
    return (
      <>
      <div>
        Number of squeaks: {squeaks.length}
      </div>

      <ul>
        {squeaks.map(i =>
          <li key={i.getSqueakHash()}>{i.getSqueakHash()}</li>
        )}
      </ul>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Timeline" />
      {(squeaks)
        ? InfoContent()
        : NoInfoContent()
      }
    </>
  );
}
