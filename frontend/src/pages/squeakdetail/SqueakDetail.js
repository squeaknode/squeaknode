import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
  TextField,
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
  getSqueakDetailsRequest,
} from "../../squeakclient/requests"


export default function SqueakDetailPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [squeak, setSqueak] = useState(null);
  const [squeakDetails, setSqueakDetails] = useState(null);

  const getSqueak = (hash) => {
      getSqueakDisplayRequest(hash, setSqueak);
  };
  const getSqueakDetails = (hash) => {
      getSqueakDetailsRequest(hash, setSqueakDetails);
  };

  useEffect(()=>{
    getSqueak(hash)
  },[hash]);
  useEffect(()=>{
    getSqueakDetails(hash)
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
        <Widget disableWidgetMenu>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <div>
                <div key="address" className={classes.legendItemContainer}>

                  <Typography color="text" colorBrightness="secondary">
                    Address
                  </Typography>
                  <Typography color="text">
                      &nbsp;{squeak.getAuthorAddress()}
                  </Typography>
                </div>

                <div key="rawdata" className={classes.legendItemContainer}>
                  <Typography color="text" colorBrightness="secondary">
                    Raw Data
                  </Typography>
                  <TextField
                    id="standard-textarea"
                    placeholder="Placeholder"
                    value={squeakDetails.getSqueakDetailEntry().getSerializedSqueakHex()}
                    fullWidth="true"
                    variant="outlined"
                    multiline
                  />
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
      <PageTitle title="Squeak Details" />
      {(squeak && squeakDetails)
        ? SqueakContent()
        : NoSqueakContent()
      }
    </>
  );
}
