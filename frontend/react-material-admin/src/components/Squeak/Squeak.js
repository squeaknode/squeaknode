import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import classnames from "classnames";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

export default function Squeak({
  hash,
  isUnlocked,
  contentStr,
  isReply,
  replyTo,
  isAuthorKnown,
  authorName,
  blockHeight,
  blockTime,
  ...props
}) {
  var classes = useStyles();

  // local
  // var [moreButtonRef, setMoreButtonRef] = useState(null);
  // var [isMoreMenuOpen, setMoreMenuOpen] = useState(false);

  return (
    <Grid item xs={12}>
        <Widget
          disableWidgetMenu
          upperTitle
          bodyClass={classes.fullHeightBody}
          className={classes.card}
        >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              <Typography color="text" colorBrightness="secondary">
                <Box fontWeight="fontWeightBold">
                  {authorName}
                </Box>
              </Typography>
            </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            <Typography size="md">{contentStr}</Typography>
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
              <Typography color="text" colorBrightness="secondary">
                <Box color="secondary.main">
                  {new Date(blockTime*1000).toString()} (Block # {blockHeight})
                </Box>
              </Typography>
            </Grid>
          </Grid>
        </Widget>
    </Grid>
  )
}
