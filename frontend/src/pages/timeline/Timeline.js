import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Fab,
  Box,
} from "@material-ui/core";
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
import EditIcon from '@material-ui/icons/Edit';

import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';
import TimelineDot from '@material-ui/lab/TimelineDot';
import Paper from '@material-ui/core/Paper';

import FaceIcon from '@material-ui/icons/Face';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import { Typography } from "../../components/Wrappers";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import SqueakUserAvatar from "../../components/SqueakUserAvatar";

import {
  getTimelineSqueakDisplaysRequest,
  getNetworkRequest,
  getSqueakDisplayRequest,
} from "../../squeakclient/requests"
import {
  goToSqueakAddressPage,
} from "../../navigation/navigation"


export default function TimelinePage() {
  var classes = useStyles();
  var theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const [open, setOpen] = React.useState(false);
  const [network, setNetwork] = useState("");

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
      setSqueaks(newSqueaks);
    })
  }

  const handleReloadSqueakItem = (itemHash) => {
    console.log("Setting up handle reload squeak function with hash: " + itemHash);
    const innerFunc = () => {
      console.log("Calling inner reload squeak function with hash: " + itemHash);
      reloadSqueakItem(itemHash);
    }
    return innerFunc;
  }

  const getSqueaks = () => {
    getTimelineSqueakDisplaysRequest(setSqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
     setOpen(false);
  };

  useEffect(()=>{
    getSqueaks(setSqueaks)
  },[]);
  useEffect(()=>{
    getNetwork()
  },[]);

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    )
  }

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={open}
          handleClose={handleClose}
          ></MakeSqueakDialog>
      </>
    )
  }

  function TimelineUserAvatar(squeak) {
    const handleAvatarClick = () => {
      console.log("Avatar clicked...");
      goToSqueakAddressPage(history, squeak.getAuthorAddress());
    };
    return (
      <TimelineDot
      onClick={handleAvatarClick}
      style={{cursor: 'pointer'}}
      >
        <FaceIcon />
      </TimelineDot>
    )
  }

  function SqueaksContent() {
    return (
      <>
        <div>
        {squeaks.map(squeak =>
          <Timeline
            align="left"
            key={squeak.getSqueakHash()}
          >

          <TimelineItem>
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
    <SqueakThreadItem
      key={squeak.getSqueakHash()}
      hash={squeak.getSqueakHash()}
      squeak={squeak}
      network={network}
      reloadSqueak={handleReloadSqueakItem(squeak.getSqueakHash())}>
    </SqueakThreadItem>
    </TimelineContent>
    </TimelineItem>

          </Timeline>
        )}
        </div>
      </>
    )
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
      <Grid item xs={12} sm={9}>
        <Paper className={classes.paper}>
        {(squeaks)
          ? SqueaksContent()
          : NoSqueaksContent()
        }
        </Paper>
      </Grid>
      <Grid item xs={12} sm={3}>
        <Paper className={classes.paper}>

        </Paper>
      </Grid>
      </Grid>
    )
  }

  return (
    <>
      {GridContent()}
      <Fab color="secondary" aria-label="edit" className={classes.fab} onClick={handleClickOpen}>
        <EditIcon />
      </Fab>

      {MakeSqueakDialogContent()}
    </>
  );
}
