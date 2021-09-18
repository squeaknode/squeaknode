import { makeStyles } from '@material-ui/styles';
import { green } from '@material-ui/core/colors';

export default makeStyles((theme) => ({
  form: {
    margin: 'auto',
    width: 'fit-content',
    '& .MuiDialogContent-root': {
      overflow: 'hidden',
    },
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
    },
    '& .MuiDialogActions-root': {
      padding: '1rem',
    },
  },
  formControlLabel: {
    position: 'absolute',
    left: '2rem',
  },
  widgetWrapper: {
    display: 'flex',
    minHeight: '100%',
  },
  widgetHeader: {
    padding: theme.spacing(3),
    paddingBottom: theme.spacing(1),
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
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
    display: 'flex',
    flexDirection: 'column',
    flexGrow: 1,
    overflow: 'hidden',
  },
  moreButton: {
    margin: -theme.spacing(1),
    padding: 0,
    width: 40,
    height: 40,
    color: theme.palette.text.hint,
    '&:hover': {
      backgroundColor: theme.palette.primary.main,
      color: 'rgba(255, 255, 255, 0.35)',
    },
  },
  root: {
    display: 'flex',
    alignItems: 'center',
  },
  wrapper: {
    margin: theme.spacing(1),
    position: 'relative',
  },
  buttonSuccess: {
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
  fabProgress: {
    color: green[500],
    position: 'absolute',
    top: -6,
    left: -6,
    zIndex: 1,
  },
  buttonProgress: {
    color: green[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
}));
