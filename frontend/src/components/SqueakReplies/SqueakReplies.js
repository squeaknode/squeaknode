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
import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';
import TimelineDot from '@material-ui/lab/TimelineDot';

// styles
import useStyles from "./styles";

import SqueakThreadItem from "../../components/SqueakThreadItem";
import SqueakUserAvatar from "../../components/SqueakUserAvatar";
import Widget from "../../components/Widget";

import moment from 'moment';

import {
  getTimelineSqueakDisplaysRequest,
  getNetworkRequest,
  getSqueakDisplayRequest,
} from "../../squeakclient/requests"


export default function SqueakReplies({
  squeaks,
  network,
  setSqueaksFn,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  function reloadSqueakItem(itemHash) {
    // Get the new squeak.
    getSqueakDisplayRequest(itemHash, (newSqueak) => {
      const newSqueaks = squeaks.map((item) => {
        // TODO: .hash or .getHash() ?
        if (item.getSqueakHash() === itemHash) {
          return newSqueak;
        }
        return item;
      });
      setSqueaksFn(newSqueaks);
    })
  }

  const handleReloadSqueakItem = (itemHash) => {
    const innerFunc = () => {
      reloadSqueakItem(itemHash);
    }
    return innerFunc;
  }

  return (
    <Timeline align="left">

      {squeaks
        .map(squeak =>
          <TimelineItem
          key={squeak.getSqueakHash()}
          >
          <TimelineOppositeContent
            className={classes.oppositeContent}
            color="textSecondary"
          ></TimelineOppositeContent>
          <TimelineSeparator>
            <SqueakUserAvatar
              squeakProfile={squeak.getAuthor()}
            />
          </TimelineSeparator>
          <TimelineContent>
          <Box
            p={1}
            key={squeak.getSqueakHash()}
            >
          <SqueakThreadItem
            hash={squeak.getSqueakHash()}
            key={squeak.getSqueakHash()}
            squeak={squeak}
            network={network}
            reloadSqueak={handleReloadSqueakItem(squeak.getSqueakHash())}
            showActionBar={true}>
          </SqueakThreadItem>
          </Box>
          </TimelineContent>
          </TimelineItem>
      )}

    </Timeline>
  )
}
