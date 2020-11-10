import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';
import DownloadIcon from '@material-ui/icons/CloudDownload';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function SentPayment({
  sentPayment,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
  };

  const onSqueakClick = (event) => {
    event.preventDefault();
    console.log("Handling squeak click for hash: " + hash);
    if (goToSqueakPage) {
      goToSqueakPage(hash);
    }
  }

  return (
    <Box
      p={1}
      m={0}
      style={backgroundColor: 'lightgray'}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box fontWeight="fontWeightBold">
                  <Link href="#"
                    Show something here
                  </Link>
                </Box>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            Sent payment content here
          </Grid>
          </Grid>
    </Box>
  )
}
