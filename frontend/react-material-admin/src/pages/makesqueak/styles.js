import { makeStyles } from "@material-ui/styles";

export default makeStyles(theme => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));
