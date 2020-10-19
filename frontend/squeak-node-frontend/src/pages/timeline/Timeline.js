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

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import { Typography } from "../../components/Wrappers";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";

import { getFollowedSqueaks } from "../../squeakclient/requests"


export default function TimelinePage() {
  var classes = useStyles();
  var theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const [open, setOpen] = React.useState(false);
  const history = useHistory();

  const getSqueaks = (setResponse) => {
    console.log("called getSqueaks with setResponse");
    getFollowedSqueaks(setResponse);
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
     setOpen(false);
  };

  useEffect(()=>{
    getSqueaks(setSqueaks)
  },[setSqueaks]);

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

  function SqueaksContent() {
    return (
      <>
        <div>
        {squeaks.map(squeak =>
          <Box
            p={1}
            key={squeak.getSqueakHash()}
            >
          <SqueakThreadItem
            key={squeak.getSqueakHash()}
            handleAddressClick={() => goToSqueakAddressPage(squeak.getAuthorAddress())}
            handleSqueakClick={() => goToSqueakPage(squeak.getSqueakHash())}
            squeak={squeak}>
          </SqueakThreadItem>
          </Box>
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
