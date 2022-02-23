import React , { useEffect, useContext, useState } from 'react'
import './style.scss'
import {  withRouter, Link } from 'react-router-dom'
import { StoreContext } from '../../store/store'
import { ICON_SEARCH } from '../../Icons'
import Loader from '../Loader'


const Feed = (props) => {

const { state, actions } = useContext(StoreContext)

const {paymentSummary, trends, session} = state
const [searchText, setSearchText] = useState('');


useEffect(() => {
    actions.getPaymentSummary();
    actions.getTrend()
}, [])

const goToUser = (id) => {
    props.history.push(`/app/profile/${id}`)
}

const followUser = (e, id) => {
    e.stopPropagation()
    actions.followUser(id)
}

const changeSearchText = (param) => {
    setSearchText(param);
}

const searchOnEnter = (e) => {
    if (e.keyCode === 13) {
      if(searchText.length>0){
        console.log("Goto")
        console.log(searchText)
        goToNewSearch(searchText);
        setSearchText('');
      }
    }
}

const goToNewSearch = (newSearchText) => {
    props.history.push(`/app/search?q=${newSearchText}`);
}

return(
    <div className="feed-wrapper">

        <div className="explore-search-wrapper">
            <div className="explore-search-icon">
                <ICON_SEARCH/>
            </div>
            <div className="explore-search-input">
              <input value={searchText} onKeyDown={(e)=>searchOnEnter(e)} onChange={(e)=>changeSearchText(e.target.value)}  placeholder="Search Squeaks" type="text" name="search"/>
            </div>
        </div>


        {paymentSummary ?
          <div className="feed-trending-card">
              <h3 className="feed-card-header">Payments</h3>
              <div onClick={()=>props.history.push('/app/payments')}className="feed-card-trend">
                  <div>Amount Spent</div>
                  <div>{paymentSummary.getAmountSpentMsat() / 1000} sats</div>
                  <div>{paymentSummary.getNumSentPayments()} squeaks</div>
              </div>
              <div onClick={()=>props.history.push('/app/payments')}className="feed-card-trend">
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
