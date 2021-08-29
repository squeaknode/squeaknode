import React from 'react';
import {
  Typography,
  Box,
  Chip,
  Card,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';
import moment from 'moment';
import useStyles from '../../pages/wallet/styles';
import ChannelBalanceBar from './ChannelBalanceBar';

import {
  goToChannelPage,
} from '../../navigation/navigation';

export default function ChannelItem({
  channel,
  ...props
}) {
  const classes = useStyles({
    channelStatus: 'open',
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

  function ChannelDetailItemVertical(label, value) {
    return (
      <Box className={classes.detailItemVertical}>
        <Typography className={classes.detailItemLabel}>
          {label}
        </Typography>
        <Typography className={classes.detailItemValue}>
          {value}
        </Typography>
      </Box>
    );
  }

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
                label="Open"
                size="small"
                className={classes.channelStatusChip}
              />
            </Box>
          </Box>
          <Box className={classes.cardContentSection}>
            {ChannelDetailItem('Pubkey', `${channel.getRemotePubkey()}`)}
            {ChannelDetailItem('Channel Point', `${channel.getChannelPoint()}`)}
            {/* {ChannelDetailItem("Total sats sent", `${channel.getTotalSatoshisSent()}`)} */}
            {/* {ChannelDetailItem("Total sats received", `${channel.getTotalSatoshisReceived()}`)} */}
            {ChannelDetailItem('Lifetime', `${moment.duration(channel.getLifetime(), 'seconds').humanize()}`)}
            {ChannelDetailItem('Uptime', `${moment.duration(channel.getUptime(), 'seconds').humanize()}`)}
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
