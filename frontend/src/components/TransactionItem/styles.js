import { makeStyles } from "@material-ui/styles";

export default makeStyles(theme => ({
  transactionItem: {
    border: "1px solid grey",
    borderRadius: "3px",

    // backgroundColor: ({amount}) =>
    //   amount > 0
    //      ? "#c8e6c9"
    //      : (amount < 0 ? "#ffcdd2" : "white")
    // ,
  },
  transactionContent: {
    whiteSpace: 'pre-line',
    overflow: "hidden",
    textOverflow: "ellipsis",
    marginBottom: "0.5em",
    // height: '3rem',
    color: ({amount}) => amount > 0
         ? "green"
         : "red"
  },
  transactionDetails: {
    whiteSpace: 'pre-line',
    overflow: "hidden",
    textOverflow: "ellipsis",
    fontSize: "small"
  },
  transactionDetailField: {
    // display: "table-cell",
    paddingRight: "4px"
  },
  transactionDetail: {
    // display: "table-cell",
    padding: "0px 2px",
    fontWeight: "bolder"
  },
  detailRow: {
    display: "table-row"
  },

  // unused
  widgetWrapper: {
    display: "flex",
    minHeight: "100%",
  },
  widgetHeader: {
    padding: theme.spacing(3),
    paddingBottom: theme.spacing(1),
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  widgetRoot: {
    boxShadow: theme.customShadows.widget,
  },
  widgetBody: {
    paddingBottom: theme.spacing(3),
    paddingRight: theme.spacing(3),
    paddingLeft: theme.spacing(3),
  },
  noPadding: {
    padding: 0,
  },
  paper: {
    display: "flex",
    flexDirection: "column",
    flexGrow: 1,
    overflow: "hidden",
  },
  moreButton: {
    margin: -theme.spacing(1),
    padding: 0,
    width: 40,
    height: 40,
    color: theme.palette.text.hint,
    "&:hover": {
      backgroundColor: theme.palette.primary.main,
      color: "rgba(255, 255, 255, 0.35)",
    },
  },
}));
