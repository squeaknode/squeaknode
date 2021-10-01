import React from 'react';
import moment from 'moment';

import {
  Typography,
  Box,
  Link,
  Tooltip,
  ButtonGroup,
} from '@material-ui/core';

import {
  getBlockDetailUrl,
} from '../../bitcoin/blockexplorer';

export default function SqueakTime({
  hash,
  squeak,
  network,
  ...props
}) {
  const blockDetailUrl = () => getBlockDetailUrl(squeak.getBlockHash(), network);

  if (!squeak) {
    return (
      <Box color="secondary.main" fontWeight="fontWeightBold">
        Unknown time
      </Box>
    );
  }
  const squeakBlockTime = moment(squeak.getBlockTime() * 1000);
  return (
    <Box color="secondary.main" fontWeight="fontWeightBold">
      <ButtonGroup>
        <Tooltip title={squeakBlockTime.toString()}>
          <Typography disabled style={{ fontWeight: 'bold' }}>
            {squeakBlockTime.fromNow()}
          </Typography>
        </Tooltip>
      </ButtonGroup>
      <span> </span>
      (Block
      <Link
        href={blockDetailUrl()}
        target="_blank"
        rel="noopener"
        onClick={(event) => event.stopPropagation()}
      >
        <span> </span>
        #
        {squeak.getBlockHeight()}
      </Link>
      )
    </Box>
  );
}
