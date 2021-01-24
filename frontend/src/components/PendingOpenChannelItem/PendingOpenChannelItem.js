import React, {useState} from "react";
import {Box, Chip, Typography,} from "@material-ui/core";
import {useHistory} from "react-router-dom";

// styles
import useStyles from "../../pages/wallet/styles";

import moment from 'moment';
import Card from "@material-ui/core/Card";
import ChannelBalanceBar from "../ChannelItem/ChannelBalanceBar";
import {CHANNEL_VIEW, navigateTo, PROFILE_VIEW} from "../../navigation/routes";

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

  const onChannelClick = (event) => {
    event.preventDefault();
    console.log("Handling channel click...");
    var channel = pendingOpenChannel.getChannel();
    var txId = getTxId(channel);
    var outputIndex = getOutputIndex(channel);
    navigateTo(history, CHANNEL_VIEW, [txId, outputIndex]);
  }

  function ChannelDetailItem(label, value) {
    return <Box className={classes.detailItem}>
      <Typography className={classes.detailItemLabel}>
        {label}
      </Typography>
      <Typography className={classes.detailItemValue}>
        {value}
      </Typography>
    </Box>
  }

  const channel = pendingOpenChannel.getChannel();
  return (
    <Card
      className={classes.root}
      onClick={onChannelClick}
    >
      <Box className={classes.cardContentContainerVertical}>
        <Box className={classes.cardContentFlexColumn}>
          <Box className={classes.cardHeaderContainer}>
            <Box className={classes.cardHeaderRow}>
              <Chip
                label="Opening"
                size="small"
                className={classes.channelStatusChip}/>
            </Box>
          </Box>
          <Box className={classes.cardContentSection}>
            {ChannelDetailItem("Pubkey", `${channel.getRemoteNodePub()}`)}
            {ChannelDetailItem("Channel Point", `${channel.getChannelPoint()}`)}
            {/*{ChannelDetailItem("Lifetime", `${moment.duration(channel.getLifetime(), 'seconds').humanize()}`)}*/}
            {/*{ChannelDetailItem("Uptime", `${moment.duration(channel.getUptime(), 'seconds').humanize()}`)}*/}
          </Box>
        </Box>
        <Box className={classes.cardContentFlexColumn}>
          <ChannelBalanceBar
            channel={channel}
          />
        </Box>
      </Box>
    </Card>
  )
}