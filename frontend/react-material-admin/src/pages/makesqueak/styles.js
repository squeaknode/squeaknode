import { makeStyles } from "@material-ui/styles";

export default makeStyles(theme => ({


    text: {
      marginBottom: theme.spacing(2),
    },
    formControl: {
      margin: theme.spacing(2),
      minWidth: 120,
    },
    selectEmpty: {
      marginTop: theme.spacing(2),
    },

  root: {
    '& > *': {
      margin: theme.spacing(0),
    },
  },
}));
