import React, { useState } from "react";

// icons
import CallMadeIcon from '@material-ui/icons/CallMade';
import CallReceivedIcon from '@material-ui/icons/CallReceived';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';


// styles
import useStyles from "../../pages/wallet/styles";

import moment from 'moment';
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardHeader from "@material-ui/core/CardHeader";
import IconButton from "@material-ui/core/IconButton";
import Collapse from "@material-ui/core/Collapse";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";

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
    console.log("Handling transaction click...");
    if (handleTransactionClick) {
      handleTransactionClick();
    }
  }

   function TransactionDetailItem(label, value) {
      return <Box display='flex'>
         <Typography className={classes.detailItemLabel}>
            {label}
         </Typography>
         <Typography className={classes.detailItemValue}>
            {value}
         </Typography>
      </Box>
   }

   function TransactionMoreDetails() {
      return (
         <CardContent className={classes.transactionMoreDetails}>
            {TransactionDetailItem("Timestamp", moment.unix(transaction.getTimeStamp()).format('lll'))}
            {TransactionDetailItem("Block Height", transaction.getBlockHeight())}
            {TransactionDetailItem("Total Fees", transaction.getTotalFees())}
            {/*{TransactionDetailItem("Dest Addresses", transaction.getDestAddressesList().length)}*/}
            {TransactionDetailItem("Confirmations", transaction.getNumConfirmations())}
         </CardContent>
    )
  }

  const classes = useStyles({
     amount: transaction.getAmount(),
     clickable: false,
  })

  const amountGtZero = transaction.getAmount() >= 0

   function PlusMinusSymbol() {
     if (transaction.getAmount() > 0) {
        return '+'
     } else if (transaction.getAmount() < 0) {
        return '-'
     }
   }

  function TransactionIcon() {
     if (amountGtZero) {
        return <CallReceivedIcon className={classes.transactionIcon}/>
     } else {
        return <CallMadeIcon className={classes.transactionIcon}/>
     }
  }

  return (
      <Card
         className={classes.root}
         onClick={onTransactionClick}
      >
         <CardHeader
            className={classes.transactionItemHeader}
            title={`${PlusMinusSymbol()}${Math.abs(transaction.getAmount())} sats`}
            subheader={moment.unix(transaction.getTimeStamp()).fromNow()}
            avatar={TransactionIcon()}
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
            {TransactionMoreDetails()}
         </Collapse>
      </Card>
)
}
