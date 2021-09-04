import React from 'react';
import { Box, Chip, Typography } from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles

import Card from '@material-ui/core/Card';
import useStyles from '../../pages/wallet/styles';
import ChannelBalanceBar from '../ChannelItem/ChannelBalanceBar';

import {
  goToChannelPage,
} from '../../navigation/navigation';

export default function PendingOpenChannelItem({
  pendingOpenChannel,
  ...props
}) {
  const classes = useStyles({
    channelStatus: 'pending-open',
    clickable: true,
  });

  const history = useHistory();

  const getTxId = (channel) => {
    const channelPoint = channel.getChannelPoint();
    if (channelPoint == null) {
      return null;
    }
    const pieces = channelPoint.split(':');
    return pieces[0];
  };

  const getOutputIndex = (channel) => {
    const channelPoint = channel.getChannelPoint();
    if (channelPoint == null) {
      return null;
    }
    const pieces = channelPoint.split(':');
    if (pieces.length < 2) {
      return null;
    }
    return pieces[1];
  };

  const onChannelClick = (event) => {
    event.preventDefault();
    console.log('Handling channel click...');
    const channel = pendingOpenChannel.getChannel();
    const txId = getTxId(channel);
    const outputIndex = getOutputIndex(channel);
    goToChannelPage(history, txId, outputIndex);
  };

  function ChannelDetailItem(label, value) {
    return (
      <Box className={classes.detailItem}>
        <Typography className={classes.detailItemLabel}>
          {label}
        </Typography>
        <Typography className={classes.detailItemValue}>
          {value}
        </Typography>
      </Box>
    );
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
                className={classes.channelStatusChip}
              />
            </Box>
          </Box>
          <Box className={classes.cardContentSection}>
            {ChannelDetailItem('Pubkey', `${channel.getRemoteNodePub()}`)}
            {ChannelDetailItem('Channel Point', `${channel.getChannelPoint()}`)}
            {/* {ChannelDetailItem("Lifetime", `${moment.duration(channel.getLifetime(), 'seconds').humanize()}`)} */}
            {/* {ChannelDetailItem("Uptime", `${moment.duration(channel.getUptime(), 'seconds').humanize()}`)} */}
          </Box>
        </Box>
        <Box className={classes.cardContentFlexColumn}>
          <ChannelBalanceBar
            channel={channel}
          />
        </Box>
      </Box>
    </Card>
  );
}
