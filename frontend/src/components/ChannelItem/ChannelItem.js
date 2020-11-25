import React, {useState} from "react";
import {
  Typography,
  Grid,
  Box,
} from "@material-ui/core";
import {useHistory} from "react-router-dom";

// icons
import ImportExportIcon from '@material-ui/icons/ImportExport';
import SwapHorizontalCircleIcon from '@material-ui/icons/SwapHorizontalCircle';

// styles
import useStyles from "../../pages/wallet/styles";


import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import moment from "moment";
import CallReceivedIcon from "@material-ui/icons/CallReceived";
import CallMadeIcon from "@material-ui/icons/CallMade";
import IconButton from "@material-ui/core/IconButton";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Collapse from "@material-ui/core/Collapse";

export default function ChannelItem({
  channel,
  ...props
}) {
   const classes = useStyles({
      status: props.status,
      clickable: true,
   })

   const history = useHistory();

   const [expanded, setExpanded] = useState(false);

   const handleExpandClick = (evt) => {
      evt.stopPropagation()
      setExpanded(!expanded);
   };

   const getTxId = (channel) => {
      var channelPoint = channel.getChannelPoint();
      if (channelPoint == null) {
         return null;
      }
      var pieces = channelPoint.split(":");
      return pieces[0];
   }

   const getOutputIndex = (channel) => {
      var channelPoint = channel.getChannelPoint();
      if (channelPoint == null) {
         return null;
      }
      var pieces = channelPoint.split(":");
      if (pieces.length < 2) {
         return null;
      }
      return pieces[1];
   }

   const goToChannelPage = (txId, outputIndex) => {
      history.push("/app/channel/" + txId + "/" + outputIndex);
   };

   const onChannelClick = (event) => {
      event.preventDefault();
      console.log("Handling channel click...");
      var txId = getTxId(channel);
      var outputIndex = getOutputIndex(channel);
      goToChannelPage(txId, outputIndex);
   }

   function ChannelDetailItem(label, value) {
      return <Box display='flex'>
         <Typography className={classes.detailItemLabel}>
            {label}
         </Typography>
         <Typography className={classes.detailItemValue}>
            {value}
         </Typography>
      </Box>
   }
   function ChannelContent() {
      if (props.status !== 'open') {
         return <CardContent className={classes.cardContentRoot}/>
      }
      return (
         <CardContent className={classes.transactionMoreDetails}>
            {ChannelDetailItem("Capacity", `${channel.getCapacity()} sats`)}
            {ChannelDetailItem("Local Balance", `${channel.getLocalBalance()} sats`)}
            {ChannelDetailItem("Remote Balance", `${channel.getRemoteBalance()} sats`)}
            {ChannelDetailItem("Pubkey", channel.getRemotePubkey())}
            {ChannelDetailItem("Channel Point", channel.getChannelPoint())}
         </CardContent>
      )
   }

  function ChannelStatusText() {
     switch(props.status) {
        case 'open':
           return 'Open'
        case 'pending-open':
           return 'Opening'
        case 'pending-closed':
           return 'Closing'
        default:
           return 'Unknown'
     }
  }
  return (
     <Card
        className={classes.root}
        onClick={onChannelClick}
     >
        <CardHeader
            className={classes.transactionItemHeader}
            title={ChannelStatusText()}
            subheader={props.status === 'open' ? channel.getRemotePubkey(): null}
            avatar={<SwapHorizontalCircleIcon className={classes.channelIcon}/>}
            action={
               <IconButton
                  className={expanded ? classes.collapseBtn : classes.expandBtn}
                  onClick={handleExpandClick}
                  aria-expanded={expanded}
                  aria-label="show more"
               >
                  <ExpandMoreIcon />
               </IconButton>
            }
         />
         <Collapse in={expanded} timeout="auto" unmountOnExit>
            {ChannelContent()}
         </Collapse>
     </Card>
  )
}
