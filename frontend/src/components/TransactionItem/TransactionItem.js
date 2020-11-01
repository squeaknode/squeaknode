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
   Card
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function TransactionItem({
  transaction,
  handleTransactionClick,
  ...props
}) {
  // const classes = useStyles();

  const history = useHistory();

  const onTransactionClick = (event) => {
    event.preventDefault();
    console.log("Handling transaction click...");
    if (handleTransactionClick) {
      handleTransactionClick();
    }
  }

  function TransactionContent() {
    const amount = transaction.getAmount()
    const plusMinusSign = amount > 0 ? "+" : "-"
    return (
      <Typography
         size="md"
         // style={{whiteSpace: 'pre-line', overflow: "hidden", textOverflow: "ellipsis", height: '6rem'}}
         className={classes.transactionContent}
      >{`${plusMinusSign}${transaction.getAmount()} satoshis`}
      </Typography>
    )
  }

  function TransactionDetails() {
    return (
      // <Typography
      //    size="xs"
      //    style={{whiteSpace: 'pre-line', overflow: "hidden", textOverflow: "ellipsis", height: '6rem'}}

       <div className={classes.transactionDetails}>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}># confirmations:</span>
             <span className={classes.transactionDetail}>{transaction.getNumConfirmations()}</span>
          </div>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}># dest addresses:</span>
             <span className={classes.transactionDetail}>{transaction.getDestAddressesList().length}</span>
          </div>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}>timestamp:</span>
             <span className={classes.transactionDetail}>{transaction.getTimeStamp()}</span>
          </div>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}>block height:</span>
             <span className={classes.transactionDetail}>{transaction.getBlockHeight()}</span>
          </div>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}>label:</span>
             <span className={classes.transactionDetail}>{transaction.getLabel()}</span>
          </div>
          <div className={classes.detailRow}>
             <span className={classes.transactionDetailLabel}>total fees:</span>
             <span className={classes.transactionDetail}>{transaction.getTotalFees()}</span>
          </div>
          {/*</Typography>*/}
       </div>
    )
  }

  const classes = useStyles({
    amount: transaction.getAmount(),
  })

  return (
    <Box
      p={1}
      m={0}
      className={classes.transactionItem}
      onClick={onTransactionClick}
      >
        <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {TransactionContent()}
            {TransactionDetails()}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box color="blue" fontSize={"small"}>
                  {moment(transaction.getTimeStamp()*1000).fromNow()} (Block #{transaction.getBlockHeight()})
                </Box>
            </Grid>
          </Grid>
    </Box>
  )
}
