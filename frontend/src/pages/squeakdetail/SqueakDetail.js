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
import { Typography } from "../../components/Wrappers";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
  getSqueakDisplayRequest,
  getAncestorSqueakDisplaysRequest,
} from "../../squeakclient/requests"


export default function SqueakDetailPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);

  const getSqueak = (hash) => {
      getSqueakDisplayRequest(hash, setSqueak);
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
        {SqueakDetailsContent()}
      </>
    )
  }

  function SqueakDetailsContent() {
    return (
      <>
        <Widget title="Squeak details" upperTitle className={classes.card}>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <div className={classes.pieChartLegendWrapper}>
                <div key="yellow" className={classes.legendItemContainer}>
                  <Typography style={{ whiteSpace: "nowrap" }}>
                      &nbsp;content&nbsp;
                  </Typography>
                  <Typography color="text" colorBrightness="secondary">
                      &nbsp;{squeak.getAuthorAddress()}
                  </Typography>
                </div>
              </div>
            </Grid>
          </Grid>
        </Widget>
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
