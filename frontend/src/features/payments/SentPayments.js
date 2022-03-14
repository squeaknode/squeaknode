import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { withRouter } from 'react-router-dom'
import moment from 'moment'

import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


import {
  fetchSentPayments,
  clearSentPayments,
  selectSentPayments,
  selectSentPaymentsStatus,
  selectLastSentPaymentsSqueak,
} from './paymentsSlice'


const SentPayments = (props) => {
  const sentPayments = useSelector(selectSentPayments);
  const sentPaymentsStatus = useSelector(selectSentPaymentsStatus);
  const lastSentPayment = useSelector(selectLastSentPaymentsSqueak);
  const dispatch = useDispatch();

  useEffect(() => {
      window.scrollTo(0, 0)
      // actions.getSqueaks({lastSqueak: null})
      // reloadSqueaks();
      console.log('fetchSentPayments');
      dispatch(clearSentPayments());
      dispatch(fetchSentPayments(null));
  }, [])

  const goToSqueak = (id) => {
      // if(props.replyTo){ actions.getSqueak(id) }
      props.history.push(`/app/squeak/${id}`)
  }


  const renderedListItems = sentPayments.map(f=>{
    return <div onClick={()=>goToSqueak(f.getSqueakHash())} key={f.getPaymentHash()} className="search-result-wapper">
              <div className="search-user-details">
                <div className="search-user-warp">
                  <div className="search-user-info">
                    <div className="payment-price">{f.getPriceMsat() / 1000} sats</div>
                    <div className="payment-squeak-hash"><b>Squeak Hash</b>: {f.getSqueakHash()}</div>
                    <div className="payment-peer-address"><b>Peer</b>: {f.getPeerAddress().getHost()}:{f.getPeerAddress().getPort()}</div>
                    <div className="payment-lightning-node"><b>Lightning Node</b>: {f.getNodePubkey()}</div>
                    <div className="payment-time">{moment(f.getTimeMs()).format("h:mm A · MMM D, YYYY")}</div>
                  </div>
                </div>
              </div>
           </div>
    })

  return <>
          {renderedListItems}

          {sentPaymentsStatus === 'loading' ?
          <div className="todo-list">
            <Loader />
          </div>
          :
          <div onClick={() => dispatch(fetchSentPayments(lastSentPayment))} className='squeak-btn-side squeak-btn-active'>
            LOAD MORE
          </div>
          }

         </>
}

export default withRouter(SentPayments)
