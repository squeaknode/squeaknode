// App
export const APP_PATH = "/app"
export const TIMELINE_PATH = APP_PATH + "/timeline"
export const DASHBOARD_PATH = APP_PATH + "/dashboard"
export const SQUEAK_ADDRESS_PATH = APP_PATH + "/squeakAddress/:address"
export const SQUEAK_PATH = APP_PATH + "/squeak/:hash"
export const SQUEAK_DETAIL_PATH = APP_PATH + "/squeakDetail/:hash"
export const BUY_PATH = APP_PATH + "/buy/:hash"
export const OFFER_PATH = APP_PATH + "/offer/:id"
export const PROFILES_PATH = APP_PATH + "/profiles"
export const PROFILE_PATH = APP_PATH + "/profile/:id"
export const PAYMENTS_PATH = APP_PATH + "/payments"
export const WALLET_PATH = APP_PATH + "/wallet"
export const LIGHTNING_NODE_PORT_PATH = APP_PATH + "/lightningnode/:pubkey/:host/:port"
export const LIGHTNING_NODE_HOST_PATH = APP_PATH + "/lightningnode/:pubkey/:host"
export const LIGHTNING_NODE_PUBKEY_PATH = APP_PATH + "/lightningnode/:pubkey"
export const CHANNEL_PATH = APP_PATH + "/channel/:txId/:outputIndex"
export const PEERS_PATH = APP_PATH + "/peers"
export const PEER_PATH = APP_PATH + "/peer/:id"
export const NOTIFICATIONS_PATH = APP_PATH + "/notifications"

// UI
export const UI_PATH = APP_PATH + "/ui"
export const MAPS_PATH = APP_PATH + "/ui/maps"
export const ICONS_PATH = APP_PATH + "/ui/icons"
export const CHARTS_PATH = APP_PATH + "/ui/charts"

export default {
  APP_PATH,
  TIMELINE_PATH,
  DASHBOARD_PATH,
  SQUEAK_ADDRESS_PATH,
  SQUEAK_PATH,
  SQUEAK_DETAIL_PATH,
  BUY_PATH,
  OFFER_PATH,
  PROFILES_PATH,
  PROFILE_PATH,
  PAYMENTS_PATH,
  WALLET_PATH,
  LIGHTNING_NODE_PORT_PATH,
  LIGHTNING_NODE_HOST_PATH,
  LIGHTNING_NODE_PUBKEY_PATH,
  CHANNEL_PATH,
  PEERS_PATH,
  PEER_PATH,
  NOTIFICATIONS_PATH,
  UI_PATH,
  MAPS_PATH,
  ICONS_PATH,
  CHARTS_PATH,
}