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
import LndUnavailableDialog from "../../components/LndUnavailableDialog";
import TransactionItem from "../../components/TransactionItem";
import LightningPeerListItem from "../../components/LightningPeerListItem";
import ChannelItem from "../../components/ChannelItem";
import PendingOpenChannelItem from "../../components/PendingOpenChannelItem";

import {
  lndGetInfoRequest,
  lndWalletBalanceRequest,
  lndGetTransactionsRequest,
  lndListPeersRequest,
  lndListChannelsRequest,
  lndPendingChannelsRequest,
} from "../../squeakclient/requests"

export default function WalletPage() {
  var classes = useStyles();
  var theme = useTheme();

  const [lndInfo, setLndInfo] = useState(null);
  const [walletBalance, setWalletBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [pendingChannels, setPendingChannels] = useState(null);
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
    lndGetInfoRequest(setLndInfo);
  };
  const getWalletBalance = () => {
    lndWalletBalanceRequest(setWalletBalance);
  };
  const getTransactions = () => {
    lndGetTransactionsRequest(setTransactions)
  };
  const listPeers = () => {
    lndListPeersRequest(setPeers);
  };
  const listChannels = () => {
    lndListChannelsRequest(setChannels);
  };
  const getPendingChannels = () => {
    lndPendingChannelsRequest(setPendingChannels);
  };

  const lndUnavailableDialogOpen = () => {
    return lndInfo == null;
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
  useEffect(()=>{
    listPeers()
  },[]);
  useEffect(()=>{
    listChannels()
  },[]);
  useEffect(()=>{
    getPendingChannels()
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
        <Grid container spacing={4}>
          {TransactionsGridItem()}
        </Grid>
      </>
    )
  }

  function PeersContent() {
    return (
      <>
        <Grid container spacing={4}>
          {PeersGridItem()}
        </Grid>
      </>
    )
  }

  function BalanceGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
         <div>
           <Typography variant="h1" className={classes.text}>
             {walletBalance.getTotalBalance()} sats
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
               unconfirmed balance (sats)
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
               confirmed balance (sats):
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

  function TransactionsGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item xs={12}>
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
        </Grid>
      </Grid>
      </Widget>
      </Grid>

    )
  }

  function PeersGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item xs={12}>
        {peers.map(peer =>
          <Box
            p={1}
            key={peer.getPubKey()}
            >
          <LightningPeerListItem
            key={peer.getPubKey()}
            // handleTransactionClick={() => goToSqueakPage(transaction.getSqueakHash())}
            handlePeerClick={() => console.log("clicked peer")}
            peer={peer}>
          </LightningPeerListItem>
          </Box>
        )}
        </Grid>
      </Grid>
      </Widget>
      </Grid>

    )
  }

  function ChannelsGridItem() {
    return (
      <Grid item xs={12}>
      <Widget disableWidgetMenu>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="center"
      >
        <Grid item xs={12}>
        {pendingChannels.getPendingOpenChannelsList().map(pendingOpenChannel =>
          <Box
            p={1}
            key={pendingOpenChannel.getChannel().getChannelPoint()}
            >
          <PendingOpenChannelItem
            key={pendingOpenChannel.getChannel().getChannelPoint()}
            pendingOpenChannel={pendingOpenChannel}>
          </PendingOpenChannelItem>
          </Box>
        )}
        {channels.map(channel =>
          <Box
            p={1}
            key={channel.getChannelPoint()}
            >
          <ChannelItem
            key={channel.getChannelPoint()}
            channel={channel}>
          </ChannelItem>
          </Box>
        )}
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
          <Tab label="Peers" {...a11yProps(3)} />
          <Tab label="Channels" {...a11yProps(4)} />
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
      <TabPanel value={value} index={3}>
        {(peers != null)
          ? PeersContent()
          : NoBalanceContent()
        }
      </TabPanel>
      <TabPanel value={value} index={4}>
        {(channels != null && pendingChannels != null)
          ? ChannelsGridItem()
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

  function LndUnavailableDialogContent() {
    return (
      <>
        <LndUnavailableDialog
          open={lndUnavailableDialogOpen()}
          ></LndUnavailableDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Wallet" />
      {LightningTabs()}
      {ReceiveBitcoinDialogContent()}
      {LndUnavailableDialogContent()}
    </>
  );
}
