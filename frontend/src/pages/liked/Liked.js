import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Grid,
} from '@material-ui/core';
import { useTheme } from '@material-ui/styles';

import Paper from '@material-ui/core/Paper';

// styles
import useStyles from './styles';

// components
import SqueakList from '../../components/SqueakList';

import {
  getLikedSqueakDisplaysRequest,
  getNetworkRequest,
} from '../../squeakclient/requests';

export default function LikedPage() {
  const classes = useStyles();
  const theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const [network, setNetwork] = useState('');

  const history = useHistory();

  const getSqueaks = () => {
    getLikedSqueakDisplaysRequest(setSqueaks);
  };
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  useEffect(() => {
    getSqueaks(setSqueaks);
  }, []);
  useEffect(() => {
    getNetwork();
  }, []);

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    );
  }

  function SqueaksContent() {
    return (
      <>
        <SqueakList
          squeaks={squeaks}
          network={network}
          setSqueaksFn={setSqueaks}
        />
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          <Paper className={classes.paper}>
            {(squeaks)
              ? SqueaksContent()
              : NoSqueaksContent()}
          </Paper>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper className={classes.paper} />
        </Grid>
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
    </>
  );
}
