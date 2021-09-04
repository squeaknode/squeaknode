import React from 'react';

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

export default function SqueakList({
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
    <div>
      {squeaks.map((squeak) => (
        <Timeline
          align="left"
          key={squeak.getSqueakHash()}
        >

          <TimelineItem>
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
              <SqueakThreadItem
                key={squeak.getSqueakHash()}
                hash={squeak.getSqueakHash()}
                squeak={squeak}
                network={network}
                reloadSqueak={handleReloadSqueakItem(squeak.getSqueakHash())}
                showActionBar
              />
            </TimelineContent>
          </TimelineItem>

        </Timeline>
      ))}
    </div>
  );
}
