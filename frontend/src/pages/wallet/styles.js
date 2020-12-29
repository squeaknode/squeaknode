import { makeStyles } from "@material-ui/styles";

export default makeStyles(theme => ({
  root: {
    minWidth: 275,
    border: '1px solid #e8e8e8',
    '&:hover': {
      boxShadow: ({clickable}) => clickable ?
         '0px 4px 3px -1px rgba(0,0,0,0.2), 0 3px 3px -2px #B2B2B21A, 0 1px 8px 0 #9A9A9A1A' :
         null,
      cursor: ({clickable}) => clickable ? 'pointer' : 'default',
    }
  },
  cardContentContainer: {
    padding: '1rem',
  },
  cardContentContainerVertical: {
    display: 'flex',
  },
  cardHeaderContainer: {
    // padding: '1.5rem 1rem 0rem 1rem',
    flex: 1,
  },
  cardContentFlexColumn: {
    // flex: 1,
    width: '50%',
    alignSelf: 'center',
    padding: '1.5rem',
  },
  cardContentSection: {
    // alignSelf: 'center',
    // padding: '0 1rem',
    display: 'block',
  },
  cardHeaderRow: {
    display: 'flex',
    alignItems: 'center',
  },
  cardSubheaderText: {
    fontSize: '0.8rem',
    color: '#727272',
  },
  cardSubheaderTextLabel: {
    fontSize: '0.8rem',
    color: '#a5a5a5',
    fontWeight: '600',
    marginRight: '0.3rem',
  },
  cardSubheaderTextValue: {
    fontSize: '0.8rem',
    color: '#404040',
  },
  cardContent: {
    whiteSpace: 'pre-line',
    overflow: "hidden",
    textOverflow: "ellipsis",
    paddingTop: '0.5rem',
    backgroundColor: '#f5f5f5',
  },
  cardContentColumns: {
    whiteSpace: 'pre-line',
    overflow: "hidden",
    textOverflow: "ellipsis",
    paddingTop: '0.5rem',
    backgroundColor: '#f5f5f5',
    display: 'block',
  },

  // card detail item
  detailItem: {
    display: 'flex',
  },

  detailItemVertical: {
    flex: 1,
    // marginRight: '3rem',
    // position: 'absolute',
  },
  detailItemLabel: {
    // flex: 1,
    color: '#9a9a9a',
    fontSize: '0.8rem',
    fontWeight: '600',
    width: '8rem',
    // paddingBottom: '0'

  },
  detailItemValue: {
    flex: 1,
    paddingLeft: '0.5rem',
    fontSize: '0.8rem',
    display: 'table-cell',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },

  // Balance grid
  balanceGridItemLabel: {  // BalanceGridItem
    fontWeight: 'bolder',
    color: '#6e6e6e',
  },

  // buttons
  button: {   // ReceiveBitcoinButton
    marginTop: '1rem',
  },
  expandBtn: {
    padding: 0,
    transform: 'rotate(0deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  collapseBtn: {
    padding: 0,
    transform: 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },

  // ChannelItem.js
  channelIcon: {
    marginRight: '0.5rem',
    fontSize: '1rem',
    color: ({channelStatus}) => {
      if (channelStatus === 'open') {
        return '#00cd8a'
      } else if (channelStatus === 'pending-open') {
        // return '#febc50'
        return '#eae300'
      } else if (channelStatus === 'pending-closed') {
        return '#ef5a6b'
      }
    }
  },
  channelStatusChip: {
    // minWidth: '83px',
    height: '20px',
    padding: '0 0.5rem',
    marginBottom: '0.5rem',
    color: 'white',
    borderRadius: '4px',
    fontSize: 'smaller',
    backgroundColor: ({channelStatus}) => {
      if (channelStatus === 'open') {
        return '#00cd8a'
      } else if (channelStatus === 'pending-open') {
        // return '#febc50'
        return '#eae300'
      } else if (channelStatus === 'pending-closed') {
        return '#ef5a6b'
      }
    }
  },
  channelStatusText: {
    color: ({channelStatus}) => {
      if (channelStatus === 'open') {
        return '#00cd8a'
      } else if (channelStatus === 'pending-open') {
        // return '#febc50'
        return '#eae300'
      } else if (channelStatus === 'pending-closed') {
        return '#ef5a6b'
      }
    }
  },

  // ChannelBalanceBar
  channelBalanceBarContainer: {
    justifySelf: 'center',
  },
  // balance details
  channelBalanceDetailsContainer: {
    // position: 'relative',
    // height: '2rem',
    display: 'flex',
    justifyContent: 'center',
  },
  balanceContainerLocal: {
    textAlign: 'center',
    color: '#2f2fad',
    // color: '#4949bf',
  },
  balanceContainerRemote: {
    textAlign: 'center',
    color: '#c74040',
    // color: '#ff3434',
  },
  balanceContainerCapacity: {
    textAlign: 'center',
    color: '#444',
  },
  channelBalanceBarRow: {
    display: 'flex',
    alignItems: 'center',
  },
  balanceLabel: {
    fontSize: '0.6rem',
    textTransform: 'uppercase',
    opacity: '70%',
  },
  balanceValue: {
    fontSize: '0.85rem',
    fontWeight: '600',
  },
  // balance bar
  channelBalanceProgressBar: {
    flex: 1,
    margin: '0 1rem',
    height: '10px',
    borderRadius: 5,
  },
  channelBalanceBuffer: {
    color: "orange",
  },
  channelBalanceBar: {
  },
  channelBalanceBar1Buffer: {
    // backgroundImage: 'linear-gradient(90deg, #020024 0%, #2b2bbd 35%, #7894ff 100%)'
    backgroundImage: 'linear-gradient(90deg, #2f2fad 0%, #4949bf 35%, #6f6fda 100%)'
  },
  channelBalanceBar2Buffer: {
    backgroundImage: 'linear-gradient(90deg, #ff3434 0%, #c74040 80%, #ff5a5a 100%)'
  },
  channelBalanceDashed: {
    backgroundSize: 'auto',
    animation: 'none',
    backgroundImage: 'linear-gradient(90deg, #cccccc 0%, #cccccc 90%, #dddddd 100%)',
  },


  // TransactionItem.js
  transactionIcon: {
    marginRight: '0.35rem',
    fontSize: '1rem',
    color: ({amount}) => amount > 0
       ? 'green'
       : 'red'
  },
  transactionAmt: {
    color: ({amount}) => amount > 0
      ? 'green'
       : 'red'
  },
  inlineTimestamp: {
    marginLeft: '0.5rem',
    color: 'gray',
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