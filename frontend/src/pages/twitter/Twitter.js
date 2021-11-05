import React, { useState, useEffect } from 'react';
import {
  Grid,
  Button,
  Tabs,
  Tab,
  AppBar,
  Box,
  CircularProgress,
  Typography,
} from '@material-ui/core';

// styles

// styles
import useStyles from './styles';

// components
import Widget from '../../components/Widget';
import SetBearerTokenDialog from '../../components/SetBearerTokenDialog';
import AddTwitterAccountDialog from '../../components/AddTwitterAccountDialog';
import TwitterAccountListItem from '../../components/TwitterAccountListItem';


import {
  getTwitterBearerTokenRequest,
  getTwitterAccountsRequest,
} from '../../squeakclient/requests';

export default function Twitter() {
  const classes = useStyles();
  const [bearerToken, setBearerToken] = useState('');
  const [accounts, setAccounts] = useState([]);
  const [waitingForBearerToken, setWaitingForBearerToken] = useState(false);
  const [waitingForAccounts, setWaitingForAccounts] = useState(false);
  const [setBearerTokenDialogOpen, setSetBearerTokenDialogOpen] = useState(false);
  const [addAccountDialogOpen, setAddAccountDialogOpen] = useState(false);


  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const getBearerToken = () => {
    setWaitingForBearerToken(true);
    getTwitterBearerTokenRequest((resp) => {
      setWaitingForBearerToken(false);
      setBearerToken(resp);
    });
  };

  const getAccounts = () => {
    setWaitingForAccounts(true);
    getTwitterAccountsRequest((resp) => {
      setWaitingForAccounts(false);
      setAccounts(resp);
    });
  };

  const handleClickOpenSetBearerTokenDialog = () => {
    setSetBearerTokenDialogOpen(true);
  };

  const handleCloseSetBearerTokenDialog = () => {
    setSetBearerTokenDialogOpen(false);
  };

  const handleClickOpenAddAccountDialog = () => {
    setAddAccountDialogOpen(true);
  };

  const handleCloseAddAccountDialog = () => {
    setAddAccountDialogOpen(false);
  };

  useEffect(() => {
    getBearerToken();
  }, []);
  useEffect(() => {
    getAccounts();
  }, []);

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

  function BearerTokenSummary() {
    const bearerTokenText = (bearerToken ? bearerToken : 'not configured')
    return (
      <Grid item xs={12}>
        <Box
          p={1}
        >
          <Typography variant="h5" component="h5">
            {`Bearer Token: ${bearerTokenText}`}
          </Typography>
        </Box>
      </Grid>
    );
  }

  function AccountsGridItem(accounts) {
    return (
      <Grid item xs={12}>
        {accounts.map((account) => (
          <Box
            p={1}
            key={account.getTwitterAccountId()}
          >
            <TwitterAccountListItem
              key={account.getTwitterAccountId()}
              handlePeerClick={() => console.log('clicked account')}
              accountEntry={account}
              reloadAccountsFn={getAccounts}
            />
          </Box>
        ))}
      </Grid>
    );
  }

  function AccountsContent() {
    return (
      <Grid item xs={12}>
        <Box
          p={1}
        >
          <Typography variant="h5" component="h5">
            {`Number of accounts: ${accounts.length}`}
          </Typography>
          {AccountsGridItem(accounts)}
        </Box>
      </Grid>
    );
  }

  function SetBearerTokenButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenSetBearerTokenDialog();
              }}
            >
              Set Bearer Token
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function AddAccountButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenAddAccountDialog();
              }}
            >
              Add Twitter Account
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  function TwitterAccountsContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>
            {SetBearerTokenButton()}
            {AddAccountButton()}
            {BearerTokenSummary()}
            {AccountsContent()}
            </Widget>
          </Grid>
        </Grid>
      </>
    );
  }

  function TwitterTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={0} aria-label="simple tabs example">
            <Tab label="Twitter Accounts" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={0} index={0}>
        {(waitingForBearerToken || waitingForAccounts)
          ? WaitingIndicator()
          : TwitterAccountsContent()}
        </TabPanel>
      </>
    );
  }

  function SetBearerTokenDialogContent() {
    return (
      <>
        <SetBearerTokenDialog
          open={setBearerTokenDialogOpen}
          handleClose={handleCloseSetBearerTokenDialog}
          reloadBearerTokenFn={getBearerToken}
        />
      </>
    );
  }

  function AddAccountDialogContent() {
    return (
      <>
        <AddTwitterAccountDialog
          open={addAccountDialogOpen}
          handleClose={handleCloseAddAccountDialog}
          reloadAccountsFn={getAccounts}
        />
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {TwitterTabs()}
        </Grid>
        <Grid item xs={12} sm={3} />
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
      {SetBearerTokenDialogContent()}
      {AddAccountDialogContent()}
    < />
  );
}
