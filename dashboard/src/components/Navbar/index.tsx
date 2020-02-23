import React, { useState, useCallback, FunctionComponent } from 'react';
import './styles.scss';
import {
  Drawer,
  List,
  ListItem,
  ListItemText,
  Hidden,
  AppBar,
  Toolbar,
  IconButton,
} from '@material-ui/core';
import { Chat, Menu } from '@material-ui/icons';
import { bgColor, fontColor } from '../../shared/theme-colors';

const drawer = (
  <div
    className="drawer-container"
    style={{ backgroundColor: bgColor, color: fontColor }}
  >
    <div className="drawer-title-container">
      <a href="/" className="drawer-title" style={{ color: fontColor }}>
        C C A
      </a>
    </div>
    <List classes={{ root: 'drawer-menu' }}>
      <ListItem classes={{ root: 'drawer-subheader' }}>
        <ListItemText
          classes={{ primary: 'drawer-subheader-label' }}
          primary="CATEGORIES"
        />
      </ListItem>
      <ListItem classes={{ root: 'drawer-menu-item' }} button>
        <Chat className="drawer-menu-icon" style={{ color: fontColor }} />
        <ListItemText
          classes={{ primary: 'drawer-menu-label' }}
          primary="Comments"
        />
      </ListItem>
    </List>
  </div>
);

const Navbar: FunctionComponent<{}> = () => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = useCallback(() => {
    setMobileOpen(!mobileOpen);
  }, [mobileOpen]);

  return (
    <>
      <Hidden smUp implementation="css">
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
        >
          {drawer}
        </Drawer>
        <AppBar position="static">
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={handleDrawerToggle}
            >
              <Menu />
            </IconButton>
          </Toolbar>
        </AppBar>
      </Hidden>
      <Hidden xsDown implementation="css">
        <Drawer variant="permanent" open>
          {drawer}
        </Drawer>
      </Hidden>
    </>
  );
};

export default Navbar;
