import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import moment from 'moment'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import TweetCard from '../TweetCard'


const Payments = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { sentPayments, receivedPayments, signingProfiles, contactProfiles, result, tagTweets} = state
    const [tab, setTab] = useState('Sent Payments')
    const [styleBody, setStyleBody] = useState(false)
    const [newProfileName, setNewProfileName] = useState('')
    const [newProfilePubkey, setNewProfilePubkey] = useState('')


    useEffect(() => {
        window.scrollTo(0, 0)
        //actions.getSigningProfiles()
        //actions.getContactProfiles()

        reloadSentPayments();
        reloadReceivedPayments();

        // if(props.history.location.search.length>0){
        //     goToTrend(props.history.location.search.substring(1))

        // }
    }, [])

    const getLastSentPayment = (squeakLst) => {
      if (squeakLst == null) {
        return null;
      } if (squeakLst.length === 0) {
        return null;
      }
      return squeakLst.slice(-1)[0];
    };

    const getMoreSentPayments = () => {
        let lastSentPayment = getLastSentPayment(state.sentPayments);
        console.log(lastSentPayment)
        actions.getSentPayments({lastSentPayment: lastSentPayment});
    }

    const reloadSentPayments = () => {
        actions.clearSentPayments();
        actions.getSentPayments({lastSentPayment: null});
    }

    const getMoreReceivedPayments = () => {
        let lastReceivedPayment = getLastSentPayment(state.receivedPayments);
        console.log(lastReceivedPayment)
        actions.getReceivedPayments({lastReceivedPayment: lastReceivedPayment});
    }

    const reloadReceivedPayments = () => {
        actions.clearReceivedPayments();
        actions.getReceivedPayments({lastReceivedPayment: null});
    }

    const goToUser = (id) => {
        props.history.push(`/app/profile/${id}`)
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const goToTweet = (id) => {
        if(props.replyTo){ actions.getTweet(id) }
        props.history.push(`/app/tweet/${id}`)
    }

    return(
        <div>

        <div className="explore-wrapper">
            <div className="payments-header-wrapper">
                <div className="payments-header-content">
                    <div className="payments-header-name">
                        Payments
                    </div>
                </div>
            </div>
            <div className="profile-details-wrapper">
            <div className="profiles-options">
            </div>
            </div>
            <div>
                <div className="explore-nav-menu">
                    <div onClick={()=>setTab('Sent Payments')} className={tab === 'Sent Payments' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Sent Payments
                    </div>
                    <div onClick={()=>setTab('Received Payments')} className={tab === 'Received Payments' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Received Payments
                    </div>
                </div>
                {tab === 'Sent Payments' ?
                <>
                {sentPayments.map(f=>{
                  return <div onClick={()=>goToTweet(f.getSqueakHash())} key={f.getPaymentHash()} className="search-result-wapper">
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
                })}
                {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
                {state.loading ? <Loader /> : <div onClick={() => getMoreSentPayments()} className='tweet-btn-side tweet-btn-active'>
                    Load more
                </div>}
                </>

                :
                tab === 'Received Payments' ?
                  <>
                  {receivedPayments.map(f=>{
                    return <div onClick={()=>goToTweet(f.getSqueakHash())} key={f.getPaymentHash()} className="search-result-wapper">
                      <div className="search-user-details">
                      <div className="search-user-warp">
                      <div className="search-user-info">
                      <div className="payment-price">{f.getPriceMsat() / 1000} sats</div>
                      <div className="payment-squeak-hash"><b>Squeak Hash</b>: {f.getSqueakHash()}</div>
                      <div className="payment-peer-address"><b>Peer</b>: {f.getPeerAddress().getHost()}:{f.getPeerAddress().getPort()}</div>
                      <div className="payment-time">{moment(f.getTimeMs()).format("h:mm A · MMM D, YYYY")}</div>
                      </div>
                      </div>
                    </div>
                  </div>
                  })}
                  {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
                  {state.loading ? <Loader /> : <div onClick={() => getMoreReceivedPayments()} className='tweet-btn-side tweet-btn-active'>
                      Load more
                  </div>}
                  </>
                : <div className="try-searching">
                        Nothing to see here ..
                        <div/>
                    Try searching for people, usernames, or keywords

                </div>
                }
            </div>
        </div>


        </div>
    )
}

export default withRouter(Payments)
