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
} from "../../squeakclient/requests"


export default function TimelinePage() {
  var classes = useStyles();
  var theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const [open, setOpen] = React.useState(false);
  const [network, setNetwork] = useState("");

  const history = useHistory();

  const getSqueaks = () => {
    getTimelineSqueakDisplaysRequest(setSqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
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
      goToSqueakAddressPage(squeak.getAuthorAddress());
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
        squeak={squeak}
      />
    </TimelineSeparator>
    <TimelineContent>
    <SqueakThreadItem
      key={squeak.getSqueakHash()}
      hash={squeak.getSqueakHash()}
      squeak={squeak}
      network={network}>
    </SqueakThreadItem>
    </TimelineContent>
    </TimelineItem>

          </Timeline>
        )}
        </div>
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
      <Fab color="secondary" aria-label="edit" className={classes.fab} onClick={handleClickOpen}>
        <EditIcon />
      </Fab>

      {MakeSqueakDialogContent()}
    </>
  );
}
