import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import TweetCard from '../TweetCard'


const Payments = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { account, sentPayments, signingProfiles, contactProfiles, result, tagTweets} = state
    const [tab, setTab] = useState('Signing Profiles')
    const [styleBody, setStyleBody] = useState(false)
    const [newProfileName, setNewProfileName] = useState('')
    const [newProfilePubkey, setNewProfilePubkey] = useState('')


    useEffect(() => {
        window.scrollTo(0, 0)
        //actions.getSigningProfiles()
        //actions.getContactProfiles()

        reloadSentPayments();

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

    const goToUser = (id) => {
        props.history.push(`/profile/${id}`)
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const goToTweet = (id) => {
        if(props.replyTo){ actions.getTweet(id) }
        props.history.push(`/tweet/${id}`)
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
                    <div onClick={()=>setTab('Signing Profiles')} className={tab === 'Signing Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Signing Profiles
                    </div>
                    <div onClick={()=>setTab('Sent Payments')} className={tab === 'Sent Payments' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Sent Payments
                    </div>
                </div>
                {tab === 'Signing Profiles' ?
                signingProfiles.map(f=>{
                  return <div onClick={()=>goToUser(f.getPubkey())} key={f.getPubkey()} className="search-result-wapper">
                    <Link to={`/profile/${f.getPubkey()}`} className="search-userPic-wrapper">
                      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(f)}`}/>
                    </Link>
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{f.getProfileName()}</div>
                    <div className="search-user-username">@{f.getPubkey()}</div>
                    </div>
                    </div>
                    <div className="search-user-bio">
                      &nbsp;
                    </div>
                  </div>
                </div>
                })
                :
                tab === 'Sent Payments' ?
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
