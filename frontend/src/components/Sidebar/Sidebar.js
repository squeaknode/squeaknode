import React, { useState, useEffect } from 'react';
import { Drawer, IconButton, List } from '@material-ui/core';
import {
  Home as HomeIcon,
  People as ProfilesIcon,
  AttachMoney as MoneyIcon,
  ArrowBack as ArrowBackIcon,
  CloudDownload as PeerIcon,
  History as HistoryIcon,
  Favorite as LikedIcon,
  Twitter as TwitterIcon,
} from '@material-ui/icons';
import { useTheme } from '@material-ui/styles';
import { withRouter } from 'react-router-dom';
import classNames from 'classnames';

// styles
import useStyles from './styles';

// components
import SidebarLink from './components/SidebarLink/SidebarLink';

// context
import {
  useLayoutState,
  useLayoutDispatch,
  toggleSidebar,
} from '../../context/LayoutContext';

const structure = [
  {
    id: 0, label: 'Timeline', link: '/app/timeline', icon: <HomeIcon />,
  },
  {
    id: 1, label: 'Profiles', link: '/app/profiles', icon: <ProfilesIcon />,
  },
  {
    id: 2, label: 'Liked', link: '/app/liked', icon: <LikedIcon />,
  },
  {
    id: 3, label: 'Wallet', link: '/app/wallet', icon: <MoneyIcon />,
  },
  {
    id: 4, label: 'Peers', link: '/app/peers', icon: <PeerIcon />,
  },
  {
    id: 5, label: 'Payments', link: '/app/payments', icon: <HistoryIcon />,
  },
  {
    id: 6, label: 'Twitter', link: '/app/twitter', icon: <TwitterIcon />,
  },
];

function Sidebar({ location }) {
  const classes = useStyles();
  const theme = useTheme();

  // global
  const { isSidebarOpened } = useLayoutState();
  const layoutDispatch = useLayoutDispatch();

  // local
  const [isPermanent, setPermanent] = useState(true);

  useEffect(() => {
    window.addEventListener('resize', handleWindowWidthChange);
    handleWindowWidthChange();
    return function cleanup() {
      window.removeEventListener('resize', handleWindowWidthChange);
    };
  });

  return (
    <Drawer
      variant={isPermanent ? 'permanent' : 'temporary'}
      className={classNames(classes.drawer, {
        [classes.drawerOpen]: isSidebarOpened,
        [classes.drawerClose]: !isSidebarOpened,
      })}
      classes={{
        paper: classNames({
          [classes.drawerOpen]: isSidebarOpened,
          [classes.drawerClose]: !isSidebarOpened,
        }),
      }}
      open={isSidebarOpened}
    >
      <div className={classes.toolbar} />
      <div className={classes.mobileBackButton}>
        <IconButton onClick={() => toggleSidebar(layoutDispatch)}>
          <ArrowBackIcon
            classes={{
              root: classNames(classes.headerIcon, classes.headerIconCollapse),
            }}
          />
        </IconButton>
      </div>
      <List className={classes.sidebarList}>
        {structure.map((link) => (
          <SidebarLink
            key={link.id}
            location={location}
            isSidebarOpened={isSidebarOpened}
            {...link}
          />
        ))}
      </List>
    </Drawer>
  );

  // ##################################################################
  function handleWindowWidthChange() {
    const windowWidth = window.innerWidth;
    const breakpointWidth = theme.breakpoints.values.md;
    const isSmallScreen = windowWidth < breakpointWidth;

    if (isSmallScreen && isPermanent) {
      setPermanent(false);
    } else if (!isSmallScreen && !isPermanent) {
      setPermanent(true);
    }
  }
}

export default withRouter(Sidebar);
