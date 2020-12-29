import React from "react";
import {
  Box,
  LinearProgress,
  Typography
} from "@material-ui/core";
import useStyles from "../../pages/wallet/styles";

export default function ChannelBalanceBar({
  channel,
  ...props
}) {
  const classes = useStyles()

  return (
    <Box className={classes.channelBalanceBarContainer}>
      <Box className={classes.channelBalanceDetailsContainer}>
        <Box className={classes.balanceContainerCapacity}>
          <Typography className={classes.balanceLabel}>Capacity</Typography>
          <Typography className={classes.balanceValue}>{channel.getCapacity()}</Typography>
        </Box>
      </Box>
      <Box className={classes.channelBalanceBarRow}>
        <Box className={classes.balanceContainerLocal}>
          <Typography className={classes.balanceLabel}>Local</Typography>
          <Typography className={classes.balanceValue} style={{color: 'darkblue'}}>{channel.getLocalBalance()}</Typography>
        </Box>
        <LinearProgress
          variant="buffer"
          value={channel.getLocalBalance() / channel.getCapacity() * 100}
          valueBuffer={channel.getRemoteBalance() / channel.getCapacity() * 100}
          className={classes.channelBalanceProgressBar}
          classes={{
            buffer: classes.channelBalanceBuffer,
            dashed: classes.channelBalanceDashed,
            bar: classes.channelBalanceBar,
            bar1Buffer: classes.channelBalanceBar1Buffer,
            bar2Buffer: classes.channelBalanceBar2Buffer,
          }}
        />
        <Box className={classes.balanceContainerRemote}>
          <Typography className={classes.balanceLabel}>Remote</Typography>
          <Typography className={classes.balanceValue} style={{color: 'darkred'}}>{channel.getRemoteBalance()}</Typography>
        </Box>
      </Box>
    </Box>
  )
}