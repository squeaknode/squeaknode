import { makeStyles } from "@material-ui/styles";

export default makeStyles(theme => ({
  root: {
    paddingTop: '0.5rem',
    minWidth: 275,
    alignItems: 'center',   // LightningPeerListItem.js
  },
  balanceGridItemLabel: {  // BalanceGridItem
    fontWeight: 'bolder',
    color: '#6e6e6e',
  },
  channelItemLabel: {  // ChannelItem.js
    fontSize: '0.8rem',
    fontWeight: 'bolder',
    paddingBottom: '0'
  },
  channelItemDataField: {  // ChannelItem.js
    fontSize: '0.9rem',
    marginBottom: '0.5rem',
  },
  button: {   // ReceiveBitcoinButton
    marginTop: '1rem',
  },

  // ChannelItem.js
  cardHeaderContainer: {
    display: 'flex',
    alignItems: 'center',
    padding: '1.5rem 1rem 1rem 1rem',
  },
  channelIcon: {
    color: ({status}) => {
      if (status === 'open') {
        return 'green'
      } else if (status === 'pending-open') {
        return '#e2e200'
      } else if (status === 'pending-closed') {
        return 'red'
      }
    }
  },
  cardHeaderText: {
    paddingLeft: '0.2rem',
  },
  cardContentRoot: {
    paddingTop: '6px',
    paddingBottom: '12px',
  },
  title: {  // ChannelItem.js, LightningPeerListItem.js
    fontSize: 14,
  },
  pos: {  // ChannelItem.js, LightningPeerListItem.js
    marginBottom: 12,
  },

  // TransactionItem.js
  transactionItemHeader: {
    paddingLeft: '0.75rem',
    display: 'flex',
    alignItems: 'center',
  },
  transactionIcon: {
    color: ({amount}) => amount > 0
       ? "green"
       : "red"
  },
  transactionAmt: {
    marginLeft: '0.2rem',
    color: ({amount}) => amount > 0
       ? "green"
       : "red"
  },
  inlineTimestamp: {
    marginLeft: '0.5rem',
    color: 'gray',
  },
  transactionMoreDetails: {
    whiteSpace: 'pre-line',
    overflow: "hidden",
    textOverflow: "ellipsis",
    backgroundColor: '#f0f0f0',
  },
  detailItemLabel: {
    flex: 2,
    fontSize: '0.8rem',
    color: '#a0a0a0',
    paddingBottom: '0'
  },
  detailItemValue: {
    flex: 7,
    fontSize: '0.8rem',
  },
  expandBtn: {
    transform: 'rotate(0deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  collapseBtn: {
    transform: 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },


  // Widget.js
  widgetRoot: {
    backgroundColor: "#fafafa",
  },


  // LightningPeerListItem.js
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
}));