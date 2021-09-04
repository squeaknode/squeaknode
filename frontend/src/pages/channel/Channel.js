import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
} from '@material-ui/core';

// styles
import useStyles from './styles';

// components
import Widget from '../../components/Widget';
import { Typography } from '../../components/Wrappers';
import CloseChannelDialog from '../../components/CloseChannelDialog';

import {
  lndListChannelsRequest,
} from '../../squeakclient/requests';

export default function LightningNodePage() {
  const classes = useStyles();

  const { txId, outputIndex } = useParams();
  const [value, setValue] = useState(0);
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

  const getChannelPoint = () => `${txId}:${outputIndex}`;

  const handleCloseCloseChannelDialog = () => {
    setCloseChannelDialogOpen(false);
  };

  const isChannelOpen = () => {
    if (channels == null) {
      return false;
    }
    let i;
    for (i = 0; i < channels.length; i++) {
      if (getChannelPoint() === channels[i].getChannelPoint()) {
        return true;
      }
    }
    return false;
  };

  const listChannels = () => {
    lndListChannelsRequest(setChannels);
  };

  const handleClickCloseChannel = () => {
    console.log('Handle click close channel.');
    setCloseChannelDialogOpen(true);
  };

  useEffect(() => {
    listChannels();
  }, []);

  function CloseChannelButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickCloseChannel();
              }}
            >
              Close Channel
            </Button>
          </div>
        </Grid>
      </>
    );
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
              <Typography size="md">{`${txId}:${outputIndex}`}</Typography>
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
              <Typography size="md">
              {isChannelOpen()
                ? 'open'
                : 'closed'}
              </Typography>
              {isChannelOpen()
                ? CloseChannelButton()
                : 'no'}
            </Grid>
          </Grid>

        </Widget>
      </Grid>
    );
  }

  function TabPanel(props) {
    const {
      children, value, index, ...other
    } = props;

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
    );
  }

  function CloseChannelDialogContent() {
    return (
      <>
        <CloseChannelDialog
          open={closeChannelDialogOpen}
          txId={txId}
          outputIndex={outputIndex}
          handleClose={handleCloseCloseChannelDialog}
        />
      </>
    );
  }

  return (
    <>
      {ChannelTabs()}
      {CloseChannelDialogContent()}
    </>
  );
}
