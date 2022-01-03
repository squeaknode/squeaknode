import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  IconButton,
  InputBase,
  Menu,
  MenuItem,
} from '@material-ui/core';
import {
  Menu as MenuIcon,
  NotificationsNone as NotificationsIcon,
  Person as AccountIcon,
  Search as SearchIcon,
  ArrowBack as ArrowBackIcon,
} from '@material-ui/icons';
import classNames from 'classnames';

// styles
import useStyles from './styles';

// components
import { Badge, Typography } from '../Wrappers/Wrappers';
import Notification from '../Notification/Notification';

// context
import {
  useLayoutState,
  useLayoutDispatch,
  toggleSidebar,
} from '../../context/LayoutContext';
// import { useUserDispatch } from '../../context/UserContext';

import {
  logoutRequest,
  getUserRequest,
  getNetworkRequest,
} from '../../squeakclient/requests';
import {
  reloadRoute,
  goToSearchPage,
  goToSettingsPage,
} from '../../navigation/navigation';

const notifications = [];

export default function Header(props) {
  const classes = useStyles();

  const history = useHistory();

  // global
  const layoutState = useLayoutState();
  const layoutDispatch = useLayoutDispatch();
  // const userDispatch = useUserDispatch();

  // local
  const [notificationsMenu, setNotificationsMenu] = useState(null);
  const [isNotificationsUnread, setIsNotificationsUnread] = useState(true);
  const [profileMenu, setProfileMenu] = useState(null);
  const [username, setUsername] = useState('bob smith');
  const [network, setNetwork] = useState('');
  const [value, setValue] = useState();


  const isSearchOpen = true;

  const getUser = () => {
    getUserRequest(setUsername);
  };

  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const handleChangeSearchText = (event) => {
    setValue(event.target.value);
  };

  useEffect(() => {
    getUser();
  }, []);
  useEffect(() => {
    getNetwork();
  }, []);

  return (
    <AppBar position="fixed" className={classes.appBar}>
      <Toolbar className={classes.toolbar}>
        <IconButton
          color="inherit"
          onClick={() => toggleSidebar(layoutDispatch)}
          className={classNames(
            classes.headerMenuButton,
            classes.headerMenuButtonCollapse,
          )}
        >
          {layoutState.isSidebarOpened ? (
            <ArrowBackIcon
              classes={{
                root: classNames(
                  classes.headerIcon,
                  classes.headerIconCollapse,
                ),
              }}
            />
          ) : (
            <MenuIcon
              classes={{
                root: classNames(
                  classes.headerIcon,
                  classes.headerIconCollapse,
                ),
              }}
            />
          )}
        </IconButton>
        <Typography variant="h6" weight="medium" className={classes.logotype}>
          Squeaknode
        </Typography>
        <div className={classes.grow} />
        <div
          className={classNames(classes.search, {
            [classes.searchFocused]: isSearchOpen,
          })}
        >
          <div
            className={classNames(classes.searchIcon, {
              [classes.searchIconOpened]: isSearchOpen,
            })}
          >
            <SearchIcon classes={{ root: classes.headerIcon }} />
          </div>
          <InputBase
            classes={{
              root: classes.inputRoot,
              input: classes.inputInput,
            }}
            value={value}
            placeholder="Search…"
            inputProps={{ 'aria-label': 'search google maps' }}
            onChange={handleChangeSearchText}
            onKeyPress={(ev) => {
              if (ev.key === 'Enter') {
                ev.preventDefault();
                const encodedText = encodeURIComponent(ev.target.value);
                setValue('');
                goToSearchPage(history, encodedText);
              }
            }}
          />
        </div>
        <IconButton
          color="inherit"
          aria-haspopup="true"
          aria-controls="mail-menu"
          onClick={(e) => {
            setNotificationsMenu(e.currentTarget);
            setIsNotificationsUnread(false);
          }}
          className={classes.headerMenuButton}
        >
          <Badge
            badgeContent={isNotificationsUnread ? notifications.length : null}
            color="warning"
          >
            <NotificationsIcon classes={{ root: classes.headerIcon }} />
          </Badge>
        </IconButton>
        <IconButton
          aria-haspopup="true"
          color="inherit"
          className={classes.headerMenuButton}
          aria-controls="profile-menu"
          onClick={(e) => setProfileMenu(e.currentTarget)}
        >
          <AccountIcon classes={{ root: classes.headerIcon }} />
        </IconButton>
        <Menu
          id="notifications-menu"
          open={Boolean(notificationsMenu)}
          anchorEl={notificationsMenu}
          onClose={() => setNotificationsMenu(null)}
          className={classes.headerMenu}
          disableAutoFocusItem
        >
          {notifications.map((notification) => (
            <MenuItem
              key={notification.id}
              onClick={() => setNotificationsMenu(null)}
              className={classes.headerMenuItem}
            >
              <Notification {...notification} typographyVariant="inherit" />
            </MenuItem>
          ))}
        </Menu>

        <Menu
          id="profile-menu"
          open={Boolean(profileMenu)}
          anchorEl={profileMenu}
          onClose={() => setProfileMenu(null)}
          className={classes.headerMenu}
          classes={{ paper: classes.profileMenu }}
          disableAutoFocusItem
        >
          <div className={classes.profileMenuUser}>
            <Typography variant="h5" weight="medium">
              {username}
            </Typography>
          </div>
          <div className={classes.profileMenuUser}>
            <Typography variant="h6" weight="medium">
              {network}
            </Typography>
          </div>
          <div className={classes.profileMenuUser}>
            <Typography
              className={classes.settingsMenuLink}
              color="primary"
              onClick={() => {
                  goToSettingsPage(history)
                  setProfileMenu(null);
                }
              }
            >
              Settings
            </Typography>
          </div>
          <div className={classes.profileMenuUser}>
            <Typography
              className={classes.profileMenuLink}
              color="primary"
              onClick={() => logoutRequest(
                () => {
                  reloadRoute(history);
                },
              )}
            >
              Sign Out
            </Typography>
          </div>
        </Menu>

      </Toolbar>
    </AppBar>
  );
}
