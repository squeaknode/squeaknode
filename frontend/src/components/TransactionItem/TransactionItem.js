import React, { useState } from 'react';

// icons
import CallMadeIcon from '@material-ui/icons/CallMade';
import CallReceivedIcon from '@material-ui/icons/CallReceived';

// styles

import moment from 'moment';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Collapse from '@material-ui/core/Collapse';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import useStyles from '../../pages/wallet/styles';

export default function TransactionItem({
  transaction,
  handleTransactionClick,
  ...props
}) {
  const [expanded, setExpanded] = useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const onTransactionClick = (event) => {
    event.preventDefault();
    console.log('Handling transaction click...');
    // if (handleTransactionClick) {
    //   handleTransactionClick();
    // }
    handleExpandClick();
  };

  function TransactionDetailItem(label, value) {
    return (
      <Box display="flex">
        <Typography className={classes.detailItemLabel}>
          {label}
        </Typography>
        <Typography className={classes.detailItemValue}>
          {value}
        </Typography>
      </Box>
    );
  }

  function TransactionMoreDetails() {
    return (
      <CardContent className={classes.cardContent}>
        {TransactionDetailItem('Tx Hash', transaction.getTxHash())}
        {TransactionDetailItem('Timestamp', moment.unix(transaction.getTimeStamp()).format('lll'))}
        {TransactionDetailItem('Block Height', transaction.getBlockHeight())}
        {TransactionDetailItem('Total Fees', transaction.getTotalFees())}
        {/* {TransactionDetailItem("Dest Addresses", transaction.getDestAddressesList().length)} */}
        {TransactionDetailItem('Confirmations', transaction.getNumConfirmations())}
      </CardContent>
    );
  }

  const classes = useStyles({
    amount: transaction.getAmount(),
    clickable: false,
  });

  const amountGtZero = transaction.getAmount() >= 0;

  function PlusMinusSymbol() {
    if (transaction.getAmount() > 0) {
      return '+';
    } if (transaction.getAmount() < 0) {
      return '-';
    }
  }

  function TransactionIcon() {
    if (amountGtZero) {
      return <CallReceivedIcon className={classes.transactionIcon} />;
    }
    return <CallMadeIcon className={classes.transactionIcon} />;
  }

  return (
    <Card
      className={classes.root}
      onClick={onTransactionClick}
    >
      <Box className={classes.cardContentContainer}>
        <Box className={classes.cardHeaderContainer}>
          <Box className={classes.cardHeaderRow}>
            {TransactionIcon()}
            <Typography className={classes.transactionAmt}>
              {PlusMinusSymbol()}
              {Math.abs(transaction.getAmount())}
              {' '}
              sats
            </Typography>
          </Box>
          <Box className={classes.cardHeaderRow}>
            <Typography className={classes.cardSubheaderText}>
              {moment.unix(transaction.getTimeStamp()).fromNow()}
            </Typography>
          </Box>
        </Box>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          {TransactionMoreDetails()}
        </Collapse>
      </Box>
    </Card>
  );
}
