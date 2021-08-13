import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
// import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  AppBar,
  Tabs,
  Tab,
  Box,
} from "@material-ui/core";
// import { useTheme } from "@material-ui/styles";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import { Typography } from "../../components/Wrappers";
import ReceiveBitcoinDialog from "../../components/ReceiveBitcoinDialog";
import SendBitcoinDialog from "../../components/SendBitcoinDialog";
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
import FormLabel from "@material-ui/core/FormLabel";

export default function WalletPage() {
  const classes = useStyles();

  const [lndInfo, setLndInfo] = useState(null);
  const [walletBalance, setWalletBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [peers, setPeers] = useState(null);
  const [channels, setChannels] = useState(null);
  const [pendingChannels, setPendingChannels] = useState(null);
  const [value, setValue] = useState(0);
  const [receiveBitcoinDialogOpen, setReceiveBitcoinDialogOpen] = useState(false);
  const [sendBitcoinDialogOpen, setSendBitcoinDialogOpen] = useState(false);

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

  const handleClickOpenSendBitcoinDialog = () => {
    setSendBitcoinDialogOpen(true);
  };

  const handleCloseSendBitcoinDialog = () => {
     setSendBitcoinDialogOpen(false);
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

  const lndAvailable = () => {
    return lndInfo &&
      walletBalance &&
      transactions &&
      peers &&
      channels &&
      pendingChannels;
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
       <Button
          variant="contained"
          className={classes.button}
          onClick={() => {
            handleClickOpenReceiveBitcoinDialog();
          }}>Receive Bitcoin
       </Button>
    )
  }

  function SendBitcoinButton() {
    return (
       <Button
          variant="contained"
          className={classes.button}
          onClick={() => {
            handleClickOpenSendBitcoinDialog();
          }}>Send Bitcoin
       </Button>
    )
  }

  function NoBalanceContent() {
    return (
      <div>
        Unable to connect to lightning node. Make sure that lnd is running and reload the page.
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
          <Grid
             container
             direction="column"
             justify="flex-start"
             spacing={2}
          >
            <Grid item>
              <Typography variant="h1">
                {walletBalance.getTotalBalance()} sats
              </Typography>
            </Grid>
            <Grid item>
              <FormLabel>
                Unconfirmed Balance (sats)
              </FormLabel>
              <Typography size="md">
                {walletBalance.getUnconfirmedBalance()}
              </Typography>
            </Grid>
            <Grid item>
              <FormLabel>
                Confirmed Balance (sats)
              </FormLabel>
              <Typography size="md">
                {walletBalance.getConfirmedBalance()}
              </Typography>
            </Grid>
          </Grid>
          {ReceiveBitcoinButton()}
          {SendBitcoinButton()}
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
              direction="column"
              justify="flex-start"
              spacing={2}
           >
             <Grid item>
               <FormLabel>
                 Node Pubkey
               </FormLabel>
               <Typography size="md">{lndInfo.getIdentityPubkey()}</Typography>
             </Grid>
             <Grid item>
               <FormLabel>
                 Synced to Chain
               </FormLabel>
               <Typography size="md">{lndInfo.getSyncedToChain().toString()}</Typography>
             </Grid>
             <Grid item>
               <FormLabel>
                 Synced to Graph
               </FormLabel>
               <Typography size="md">{lndInfo.getSyncedToGraph().toString()}</Typography>
             </Grid>
             <Grid item>
               <FormLabel>
                 Block Height
               </FormLabel>
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
                  <Box p={1} key={pendingOpenChannel.getChannel().getChannelPoint()}>
                    <PendingOpenChannelItem pendingOpenChannel={pendingOpenChannel} />
                  </Box>
               )}
               {channels.map(channel =>
                  <Box p={1} key={channel.getChannelPoint()}>
                    <ChannelItem channel={channel} />
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
        {BalanceContent()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {NodeInfoContent()}
      </TabPanel>
      <TabPanel value={value} index={2}>
        {TransactionsContent()}
      </TabPanel>
      <TabPanel value={value} index={3}>
        {PeersContent()}
      </TabPanel>
      <TabPanel value={value} index={4}>
        {ChannelsGridItem()}
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

  function SendBitcoinDialogContent() {
    return (
      <>
        <SendBitcoinDialog
          open={sendBitcoinDialogOpen}
          handleClose={handleCloseSendBitcoinDialog}
          ></SendBitcoinDialog>
      </>
    )
  }

  return (
    <>
      {lndAvailable()
        ? LightningTabs()
        : NoBalanceContent()
      }
      {ReceiveBitcoinDialogContent()}
      {SendBitcoinDialogContent()}
    </>
  );
}
