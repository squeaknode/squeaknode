import React from 'react';
import {
  Box,
} from '@material-ui/core';

import Timeline from '@material-ui/lab/Timeline';
import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';

// styles
import useStyles from './styles';

import SqueakThreadItem from '../SqueakThreadItem';
import SqueakUserAvatar from '../SqueakUserAvatar';

import {
  getSqueakDisplayRequest,
} from '../../squeakclient/requests';

export default function SqueakReplies({
  squeaks,
  network,
  setSqueaksFn,
  ...props
}) {
  const classes = useStyles();

  function reloadSqueakItem(itemHash) {
    // Get the new squeak.
    getSqueakDisplayRequest(itemHash, (newSqueak) => {
      const newSqueaks = squeaks.map((item) => {
        // TODO: .hash or .getHash() ?
        if (item.getSqueakHash() === itemHash) {
          return newSqueak;
        }
        return item;
      });
      setSqueaksFn(newSqueaks);
    });
  }

  const handleReloadSqueakItem = (itemHash) => {
    const innerFunc = () => {
      reloadSqueakItem(itemHash);
    };
    return innerFunc;
  };

  return (
    <Timeline align="left">

      {squeaks
        .map((squeak) => (
          <TimelineItem
            key={squeak.getSqueakHash()}
          >
            <TimelineOppositeContent
              className={classes.oppositeContent}
              color="textSecondary"
            />
            <TimelineSeparator>
              <SqueakUserAvatar
                squeakAddress={squeak.getAuthorAddress()}
                squeakProfile={squeak.getAuthor()}
              />
            </TimelineSeparator>
            <TimelineContent>
              <Box
                p={1}
                key={squeak.getSqueakHash()}
              >
                <SqueakThreadItem
                  hash={squeak.getSqueakHash()}
                  key={squeak.getSqueakHash()}
                  squeak={squeak}
                  network={network}
                  reloadSqueak={handleReloadSqueakItem(squeak.getSqueakHash())}
                  showActionBar
                />
              </Box>
            </TimelineContent>
          </TimelineItem>
        ))}

    </Timeline>
  );
}
