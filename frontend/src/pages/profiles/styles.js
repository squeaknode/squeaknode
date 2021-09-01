import { makeStyles } from '@material-ui/styles';
import { green } from '@material-ui/core/colors';

export default makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));
