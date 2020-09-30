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
import ReceiveBitcoinDialog from "../../components/ReceiveBitcoinDialog";
import TransactionItem from "../../components/TransactionItem";

import {
  GetInfoRequest,
  WalletBalanceRequest,
  GetTransactionsRequest,
} from "../../proto/lnd_pb"
import { client } from "../../squeakclient/squeakclient"

export default function WalletPage() {
  var classes = useStyles();
  var theme = useTheme();

  const [lndInfo, setLndInfo] = useState(null);
  const [walletBalance, setWalletBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [value, setValue] = useState(0);
  const [receiveBitcoinDialogOpen, setReceiveBitcoinDialogOpen] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleClickOpenReceiveBitcoinDialog = () => {
    setReceiveBitcoinDialogOpen(true);
  };

  const handleCloseReceiveBitcoinDialog = () => {
     setReceiveBitcoinDialogOpen(false);
  };

  const getLndInfo = () => {
        console.log("called getLndInfo");

        var getInfoRequest = new GetInfoRequest()
        console.log(getInfoRequest);

        client.lndGetInfo(getInfoRequest, {}, (err, response) => {
          console.log(response);
          setLndInfo(response);
        });
  };
  const getWalletBalance = () => {
        console.log("called getWalletBalance");

        var walletBalanceRequest = new WalletBalanceRequest()
        console.log(walletBalanceRequest);

        client.lndWalletBalance(walletBalanceRequest, {}, (err, response) => {
          console.log(response);
          setWalletBalance(response);
        });
  };
  const getTransactions = () => {
        console.log("called getTransactions");

        var getTransactionsRequest = new GetTransactionsRequest()
        console.log(getTransactionsRequest);

        client.lndGetTransactions(getTransactionsRequest, {}, (err, response) => {
          console.log(response);
          console.log("response.getTransactionsList()");
          console.log(response.getTransactionsList());
          setTransactions(response.getTransactionsList());
        });
  };

  useEffect(()=>{
    getLndInfo()
  },[]);
  useEffect(()=>{
    getWalletBalance()
  },[]);
  useEffect(()=>{
    getTransactions()
  },[]);

  function ReceiveBitcoinButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenReceiveBitcoinDialog();
            }}>Receive Bitcoin
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function NoBalanceContent() {
    return (
      <div>
        Unable to fetch lightning info.
      </div>
    )
  }

  function InfoContentOld() {
    return (
      <div>
        <p>identity_pubkey: {lndInfo.getIdentityPubkey()}</p>
        <p>alias: {lndInfo.getAlias()}</p>
        <p>num_pending_channels: {lndInfo.getNumPendingChannels()}</p>
        <p>num_active_channels: {lndInfo.getNumActiveChannels()}</p>
        <p>num_inactive_channels: {lndInfo.getNumInactiveChannels()}</p>
        <p>num_peers: {lndInfo.getNumPeers()}</p>
        <p>block_height: {lndInfo.getBlockHeight()}</p>
        <p>block_hash: {lndInfo.getBlockHash()}</p>
        <p>synced_to_chain: {lndInfo.getSyncedToChain().toString()}</p>
        <p>synced_to_graph: {lndInfo.getSyncedToGraph().toString()}</p>
      </div>
    )
  }

  function BalanceContent() {
    return (
      <>
        <Grid container spacing={4}>
          {BalanceGridItem()}
        </Grid>
      </>
    )
  }

  function NodeInfoContent() {
    return (
      <>
        <Grid container spacing={4}>
          {StatusGridItem()}
        </Grid>
      </>
    )
  }

  function TransactionsContent() {
    return (
      <>
        <div>
        {transactions.map(transaction =>
          <Box
            p={1}
            key={transaction.getTxHash()}
            >
          <TransactionItem
            key={transaction.getTxHash()}
            // handleTransactionClick={() => goToSqueakPage(transaction.getSqueakHash())}
            handleTransactionClick={() => console.log("clicked transaction")}
            transaction={transaction}>
          </TransactionItem>
          </Box>
        )}
        </div>
      </>
    )
  }

  function BalanceGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
         <div>
           <Typography variant="h1" className={classes.text}>
             {walletBalance.getTotalBalance()} satoshis
           </Typography>
         </div>
         <Grid
           container
           direction="row"
           justify="flex-start"
           alignItems="center"
         >
           <Grid item>
             <Typography color="text" colorBrightness="secondary">
               unconfirmed balance (satoshis)
             </Typography>
             <Typography size="md">{walletBalance.getUnconfirmedBalance()}</Typography>
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
               confirmed balance (satoshis):
             </Typography>
             <Typography size="md">{walletBalance.getConfirmedBalance()}</Typography>
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
               receive bitcoin:
             </Typography>
             {ReceiveBitcoinButton()}
           </Grid>
         </Grid>
       </Widget>
      </Grid>
    )
  }

  function StatusGridItem() {
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
            node pubkey
          </Typography>
          <Typography size="md">{lndInfo.getIdentityPubkey()}</Typography>
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
            synced to chain
          </Typography>
          <Typography size="md">{lndInfo.getSyncedToChain().toString()}</Typography>
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
            synced to graph
          </Typography>
          <Typography size="md">{lndInfo.getSyncedToGraph().toString()}</Typography>
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
            block height
          </Typography>
          <Typography size="md">{lndInfo.getBlockHeight()}</Typography>
        </Grid>
      </Grid>
       </Widget>
      </Grid>
    )
  }

  function ChannelsGridItem() {
    return (
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Channels"
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
                <Typography color="text" colorBrightness="secondary">
                  num pending channels
                </Typography>
                <Typography size="md">{lndInfo.getNumPendingChannels()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  num active channels
                </Typography>
                <Typography size="md">{lndInfo.getNumActiveChannels()}</Typography>
              </Grid>
              <Grid item>
                <Typography color="text" colorBrightness="secondary">
                  num inactive channels
                </Typography>
                <Typography size="md">{lndInfo.getNumInactiveChannels()}</Typography>
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

  function LightningTabs() {
    return (
      <>
      <AppBar position="static" color="default">
        <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
          <Tab label="Balance" {...a11yProps(0)} />
          <Tab label="Node Info" {...a11yProps(1)} />
          <Tab label="Transactions" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {(lndInfo && walletBalance)
          ? BalanceContent()
          : NoBalanceContent()
        }
      </TabPanel>
      <TabPanel value={value} index={1}>
        {(lndInfo && walletBalance)
          ? NodeInfoContent()
          : NoBalanceContent()
        }
      </TabPanel>
      <TabPanel value={value} index={2}>
        {(lndInfo && walletBalance)
          ? TransactionsContent()
          : NoBalanceContent()
        }
      </TabPanel>
      </>
    )
  }

  function ReceiveBitcoinDialogContent() {
    return (
      <>
        <ReceiveBitcoinDialog
          open={receiveBitcoinDialogOpen}
          handleClose={handleCloseReceiveBitcoinDialog}
          ></ReceiveBitcoinDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Wallet" />
      {LightningTabs()}
      {ReceiveBitcoinDialogContent()}
    </>
  );
}
