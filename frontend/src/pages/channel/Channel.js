import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
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

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import { Typography } from "../../components/Wrappers";
import CloseChannelDialog from "../../components/CloseChannelDialog";
import ChannelItem from "../../components/ChannelItem";

import {
  lndListPeersRequest,
  lndListChannelsRequest,
  lndPendingChannelsRequest,
} from "../../squeakclient/requests"


export default function LightningNodePage() {
  var classes = useStyles();
  var theme = useTheme();

  const history = useHistory();
  const { txId, outputIndex } = useParams();
  const [value, setValue] = useState(0);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [closeChannelDialogOpen, setCloseChannelDialogOpen] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const getChannelPoint = () => {
    return txId + ":" + outputIndex;
  };

  const handleCloseCloseChannelDialog = () => {
    setCloseChannelDialogOpen(false);
  };

  const isChannelOpen = () => {
    if (channels == null) {
      return false;
    }
    var i;
    for (i = 0; i < channels.length; i++) {
      if (getChannelPoint() == channels[i].getChannelPoint()) {
        return true;
      }
    }
    return false;
  };

  const listPeers = () => {
    lndListPeersRequest(setPeers);
  };

  const listChannels = () => {
    lndListChannelsRequest(setChannels);
  };

  const handleClickCloseChannel = () => {
    console.log("Handle click close channel.");
    setCloseChannelDialogOpen(true);
  };


  const reloadRoute = () => {
    history.go(0);
  };

  useEffect(()=>{
    listPeers()
  },[]);
  useEffect(()=>{
    listChannels()
  },[]);

  function CloseChannelButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickCloseChannel();
            }}>Close Channel
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ChannelInfoGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item>
          <Typography color="text" colorBrightness="secondary">
            channel point
          </Typography>
          <Typography size="md">{txId + ":" + outputIndex}</Typography>
        </Grid>
      </Grid>

      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item>
          <Typography color="text" colorBrightness="secondary">
            channel status
          </Typography>
          <Typography size="md">{"channel status here"}</Typography>
          {isChannelOpen()
            ? CloseChannelButton()
            : "no"
          }
        </Grid>
      </Grid>

       </Widget>
      </Grid>
    )
  }

  function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <div>{children}</div>
        )}
      </div>
    );
  }

  function ChannelTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Channel Info" {...a11yProps(0)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {ChannelInfoGridItem()}
      </TabPanel>
      </>
    )
  }

  function CloseChannelDialogContent() {
    return (
      <>
        <CloseChannelDialog
          open={closeChannelDialogOpen}
          txId={txId}
          outputIndex={outputIndex}
          handleClose={handleCloseCloseChannelDialog}
          ></CloseChannelDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Channel'} />
      {ChannelTabs()}
      {CloseChannelDialogContent()}
    </>
  );
}
