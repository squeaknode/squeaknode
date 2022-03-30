import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { Link, withRouter } from 'react-router-dom'
import moment from 'moment'

import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


import {
  fetchReceivedPayments,
  clearReceivedPayments,
  selectReceivedPayments,
  selectReceivedPaymentsStatus,
  selectLastReceivedPaymentsSqueak,
} from './paymentsSlice'


const ReceivedPayments = (props) => {
  const receivedPayments = useSelector(selectReceivedPayments);
  const receivedPaymentsStatus = useSelector(selectReceivedPaymentsStatus);
  const lastReceivedPayment = useSelector(selectLastReceivedPaymentsSqueak);
  const dispatch = useDispatch();

  useEffect(() => {
    window.scrollTo(0, 0)
    console.log('fetchReceivedPayments');
    dispatch(clearReceivedPayments());
    dispatch(fetchReceivedPayments({
      limit: 10,
      lastReceivedPayment: null,
    }));
  }, [])

  const fetchMore = () => {
    dispatch(fetchReceivedPayments({
      limit: 10,
      lastReceivedPayment: lastReceivedPayment,
    }));
  }

  const goToSqueak = (id) => {
    props.history.push(`/app/squeak/${id}`)
  }

  const renderedListItems = receivedPayments.map(f=>{
    return <div key={f.getPaymentHash()} className="payment-wapper">
      <div className="search-user-details">
        <div className="search-user-warp">
          <div className="search-user-info">
            <div className="payment-price">
              {f.getPriceMsat() / 1000} sats
            </div>
            <div className="payment-squeak-hash">
              <b>Squeak Hash</b>:&nbsp;
                <Link  style={{color: "blue", fontWeight: 'bold'}} to={`/app/squeak/${f.getSqueakHash()}`}>{f.getSqueakHash()}
                </Link>
              </div>
              <div className="payment-peer-address">
                <b>Peer</b>:&nbsp;
                  {f.getPeerAddress().getHost()}:{f.getPeerAddress().getPort()}
                </div>
                <div className="payment-time">
                  {moment(f.getTimeMs()).format("h:mm A · MMM D, YYYY")}
                </div>
              </div>
            </div>
          </div>
        </div>
      })

      return <>
      {renderedListItems}

      {receivedPaymentsStatus === 'loading' ?
        <div className="todo-list">
          <Loader />
        </div>
        :
        <div onClick={() => fetchMore()} className='squeak-btn-side squeak-btn-active'>
          LOAD MORE
        </div>
      }

      </>
  }

  export default withRouter(ReceivedPayments)
