// import pages from "../pages/index"
import pages from "../pages"
import paths from "./paths"

export function navigateTo(history, view, ...args) {
  history.push(view.goTo(...args))
}

export const TIMELINE_VIEW = {
  component: pages.Timeline,
  path: paths.TIMELINE_PATH,
  goTo: () => paths.TIMELINE_PATH,
};

export const DASHBOARD_VIEW = {
  component: pages.Dashboard,
  path: paths.DASHBOARD_PATH,
  goTo: () => paths.DASHBOARD_PATH,
};

export const SQUEAK_ADDRESS_VIEW = {
  component: pages.SqueakAddress,
  path: paths.SQUEAK_ADDRESS_PATH,
  goTo: (address) => (
    paths.SQUEAK_ADDRESS_PATH
      .replace(":address", address)
  )
};

export const SQUEAK_VIEW = {
  component: pages.Squeak,
  path: paths.SQUEAK_PATH,
  goTo: (hash) => (
    paths.SQUEAK_PATH
      .replace(":hash", hash)
  ),
};

export const SQUEAK_DETAIL_VIEW = {
  component: pages.SqueakDetail,
  path: paths.SQUEAK_DETAIL_PATH,
  goTo: (hash) => (
    paths.SQUEAK_DETAIL_PATH
      .replace(":hash", hash)
  )
};

export const BUY_VIEW = {
  component: pages.Buy,
  path: paths.BUY_PATH,
  goTo: (hash) => (
    paths.BUY_PATH
      .replace(":hash", hash)
  ),
};

export const OFFER_VIEW = {
  component: pages.Offer,
  path: paths.OFFER_PATH,
  goTo: (id) => (
    paths.OFFER_PATH
      .replace(":id", id)
  ),
};

export const PROFILE_VIEW = {
  component: pages.Profile,
  path: paths.PROFILE_PATH,
  goTo: (id) => (
    paths.PROFILE_PATH
    .replace(':id', id)
  ),
};

export const PROFILES_VIEW = {
  component: pages.Profiles,
  path: paths.PROFILES_PATH,
  goTo: () => paths.PROFILE_PATH,
};

export const WALLET_VIEW = {
  component: pages.Wallet,
  path: paths.WALLET_PATH,
  goTo: () => paths.WALLET_PATH,
};

export const LIGHTNING_NODE_PORT_VIEW = {
  component: pages.LightningNode,
  path: paths.LIGHTNING_NODE_PORT_PATH,
  goTo: ([pubkey, host, port]) => (
    paths.LIGHTNING_NODE_PORT_PATH
      .replace(":pubkey", pubkey)
      .replace(":host", host)
      .replace(":port", port)
  ),
};

export const LIGHTNING_NODE_HOST_VIEW = {
  component: pages.LightningNode,
  path: paths.LIGHTNING_NODE_HOST_PATH,
  goTo: ([pubkey, host]) => (
    paths.LIGHTNING_NODE_HOST_PATH
      .replace(":pubkey", pubkey)
      .replace(":host", host)
  ),
};

export const LIGHTNING_NODE_PUBKEY_VIEW = {
  component: pages.LightningNode,
  path: paths.LIGHTNING_NODE_PUBKEY_PATH,
  goTo: ([pubkey]) => (
    paths.LIGHTNING_NODE_PUBKEY_PATH
      .replace(":pubkey", pubkey)
  ),
};

export const CHANNEL_VIEW = {
  component: pages.Channel,
  path: paths.CHANNEL_PATH,
  goTo: ([txId, outputIndex]) => (
    paths.CHANNEL_PATH
      .replace(":txId", txId)
      .replace(":outputIndex", outputIndex)
  ),
};

export const PEERS_VIEW = {
  component: pages.Peers,
  path: paths.PEERS_PATH,
  goTo: () => paths.PEERS_PATH,
};

export const PEER_VIEW = {
  component: pages.Peer,
  path: paths.PEER_PATH,
  goTo: ([id]) => (
    paths.PEER_PATH
      .replace(":id", id)
  ),
};

export const NOTIFICATIONS_VIEW = {
  component: pages.Notifications,
  path: paths.NOTIFICATIONS_PATH,
  goTo: () => paths.NOTIFICATIONS_PATH,
};

export const UI_VIEW = {
  path: paths.UI_PATH,
  redirectPath: paths.ICONS_PATH,
  goTo: () => paths.ICONS_PATH,
  exact: true,
}

export const MAPS_VIEW = {
  component: pages.Maps,
  path: paths.MAPS_PATH,
  goTo: () => paths.MAPS_PATH,
};

export const PAYMENTS_VIEW = {
  component: pages.Payments,
  path: paths.PAYMENTS_PATH,
  goTo: () => paths.PAYMENTS_PATH,
};

export const ICONS_VIEW = {
  component: pages.Icons,
  path: paths.ICONS_PATH,
  goTo: () => paths.ICONS_PATH,
};

export const CHARTS_VIEW = {
  component: pages.Charts,
  path: paths.CHARTS_PATH,
  goTo: () => paths.CHARTS_PATH,
};

export default [
  BUY_VIEW,
  CHANNEL_VIEW,
  CHARTS_VIEW,
  DASHBOARD_VIEW,
  ICONS_VIEW,
  LIGHTNING_NODE_PUBKEY_VIEW,
  LIGHTNING_NODE_PORT_VIEW,
  LIGHTNING_NODE_HOST_VIEW,
  MAPS_VIEW,
  NOTIFICATIONS_VIEW,
  OFFER_VIEW,
  PAYMENTS_VIEW,
  PEERS_VIEW,
  PEER_VIEW,
  PROFILES_VIEW,
  PROFILE_VIEW,
  SQUEAK_VIEW,
  SQUEAK_ADDRESS_VIEW,
  SQUEAK_DETAIL_VIEW,
  TIMELINE_VIEW,
  UI_VIEW,
  WALLET_VIEW,
]