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
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function TransactionItem({
  transaction,
  handleTransactionClick,
  ...props
}) {
  var classes = useStyles();

  const history = useHistory();

  const onTransactionClick = (event) => {
    event.preventDefault();
    console.log("Handling transaction click...");
    if (handleTransactionClick) {
      handleTransactionClick();
    }
  }

  function TransactionContent() {
    return (
      <Typography
        size="md"
        style={{whiteSpace: 'pre-line', overflow: "hidden", textOverflow: "ellipsis", height: '6rem'}}
        >{transaction.getAmount()}
      </Typography>
    )
  }

  function TransactionPositiveBackgroundColor() {
    return {backgroundColor: 'lightgreen'};
  }

  function TransactionNegativeBackgroundColor() {
    return {backgroundColor: 'lightred'};
  }

  function transactionBackgroundColor() {
    var amount = transaction.getAmount();
    if (amount == 0) {
      return 'white'
    } else if (amount < 0) {
      return '#ffcdd2';
    } else if (amount > 0) {
      return '#c8e6c9';
    }
  }

  function TransactionBackgroundColor() {
    return {backgroundColor: transactionBackgroundColor()};
  }

  return (
    <Box
      p={1}
      m={0}
      style={TransactionBackgroundColor()}
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
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
            <Grid item>
                <Box color="secondary.main" fontWeight="fontWeightBold">
                  {moment(transaction.getTimeStamp()*1000).fromNow()} (Block #{transaction.getBlockHeight()})
                </Box>
            </Grid>
          </Grid>
    </Box>
  )
}
