import React , { useEffect, useContext } from 'react'
import './style.scss'
import {  withRouter, Link } from 'react-router-dom'
import { StoreContext } from '../../store/store'
import Loader from '../Loader'


const Feed = (props) => {

const { state, actions } = useContext(StoreContext)

const {account, paymentSummary, trends, suggestions, session} = state
// const userParam = props.match.params.username

useEffect(() => {
    actions.getPaymentSummary();
    actions.getTrend()
    if(session){
        actions.whoToFollow()
    }
}, [])

const goToUser = (id) => {
    props.history.push(`/profile/${id}`)
}

const followUser = (e, id) => {
    e.stopPropagation()
    actions.followUser(id)
}

console.log(paymentSummary)

return(
    <div className="feed-wrapper">
        {paymentSummary ?
          <div className="feed-trending-card">
              <h3 className="feed-card-header">Payments</h3>
              <div onClick={()=>props.history.push('/explore')}className="feed-card-trend">
                  <div>Amount Spent</div>
                  <div>{paymentSummary.getAmountSpentMsat() / 1000} sats</div>
                  <div>{paymentSummary.getNumSentPayments()} squeaks</div>
              </div>
              <div onClick={()=>props.history.push('/explore')}className="feed-card-trend">
                  <div>Amount Earned</div>
                  <div>{paymentSummary.getAmountEarnedMsat() / 1000} sats</div>
                  <div>{paymentSummary.getNumReceivedPayments()} squeaks</div>
              </div>
          </div> :
          <Loader/>
        }
    </div>
    )
}

export default withRouter(Feed)
