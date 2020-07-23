import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
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
            justify="space-between"
            alignItems="center"
          >
            <Grid item>
              <Typography size="md">{contentStr}</Typography>
            </Grid>
            <Grid item>
              <Typography color="text" colorBrightness="secondary">
                {authorName}
              </Typography>
            </Grid>
            <Grid item>
              <Typography color="text" colorBrightness="secondary">
                {new Date(blockTime*1000).toString()} (Block # {blockHeight})
              </Typography>
            </Grid>
          </Grid>
        </Widget>
    </Grid>
  )
}
