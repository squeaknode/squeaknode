import React from 'react';
import {
  Box,
} from '@material-ui/core';

import TimelineItem from '@material-ui/lab/TimelineItem';
import TimelineSeparator from '@material-ui/lab/TimelineSeparator';
import TimelineConnector from '@material-ui/lab/TimelineConnector';
import TimelineContent from '@material-ui/lab/TimelineContent';
import TimelineOppositeContent from '@material-ui/lab/TimelineOppositeContent';

// styles
import useStyles from './styles';

import SqueakThreadItem from '../SqueakThreadItem';
import SqueakUserAvatar from '../SqueakUserAvatar';

import {
  getSqueakDisplayRequest,
} from '../../squeakclient/requests';

export default function SqueakThread({
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

  const unknownAncestorHash = () => {
    if (!squeaks) {
      return null;
    }
    const oldestKnownAncestor = squeaks[0];
    if (!oldestKnownAncestor) {
      return null;
    }
    return oldestKnownAncestor.getReplyTo();
  };

  function UnkownReplyToContent() {
    const squeakHash = unknownAncestorHash();
    if (!squeakHash) {
      return (
        <></>
      );
    }
    return (
      <TimelineItem>
        <TimelineOppositeContent
          className={classes.oppositeContent}
          color="textSecondary"
        />
        <TimelineSeparator>
          <SqueakUserAvatar
            squeakAddress={null}
            squeakProfile={null}
          />
          <TimelineConnector />
        </TimelineSeparator>
        <TimelineContent>
          <SqueakThreadItem
            hash={squeakHash}
            key={squeakHash}
            squeak={null}
          />
        </TimelineContent>
      </TimelineItem>
    );
  }

  return (
    <>
      {UnkownReplyToContent()}
      {squeaks
        .slice(0, -1)
        // .reverse()
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
                squeakAddress={squeak.getAuthorPubkey()}
                squeakProfile={squeak.getAuthor()}
              />
              <TimelineConnector />
            </TimelineSeparator>
            <TimelineContent>
              <Box
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
    </>
  );
}
