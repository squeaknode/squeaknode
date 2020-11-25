import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';

// styles
import useStyles from "../../pages/wallet/styles";

import Widget from "../../components/Widget";

import moment from 'moment';
import CardHeader from "@material-ui/core/CardHeader";
import SwapHorizontalCircleIcon from "@material-ui/icons/SwapHorizontalCircle";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Collapse from "@material-ui/core/Collapse";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

export default function PendingOpenChannelItem({
  pendingOpenChannel,
  ...props
}) {
  const classes = useStyles({
     channelStatus: 'pending-open',
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
    var channel = pendingOpenChannel.getChannel();
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
      const channel = pendingOpenChannel.getChannel();
      return (
         <CardContent className={classes.transactionMoreDetails}>
            {ChannelDetailItem("Capacity", `${channel.getCapacity()} sats`)}
            {ChannelDetailItem("Local Balance", `${channel.getLocalBalance()} sats`)}
            {ChannelDetailItem("Remote Balance", `${channel.getRemoteBalance()} sats`)}
            {ChannelDetailItem("Pubkey", channel.getRemoteNodePub())}
            {ChannelDetailItem("Channel Point", channel.getChannelPoint())}
         </CardContent>
      )
   }

  return (
     <Card
        className={classes.root}
        onClick={onChannelClick}
     >
       <CardHeader
          className={classes.transactionItemHeader}
          title={'Opening test'}
          // subheader={props.status === 'open' ? channel.getRemotePubkey(): null}
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
