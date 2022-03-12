import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import moment from 'moment'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import SentPayments from '../../features/payments/SentPayments'
import ReceivedPayments from '../../features/payments/ReceivedPayments'


const Payments = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { sentPayments, receivedPayments, signingProfiles, contactProfiles, result, tagSqueaks} = state
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
        actions.getSentPayments({lastSentPayment: lastSentPayment});
    }

    const reloadSentPayments = () => {
        actions.clearSentPayments();
        actions.getSentPayments({lastSentPayment: null});
    }

    const getMoreReceivedPayments = () => {
        let lastReceivedPayment = getLastSentPayment(state.receivedPayments);
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

    const goToSqueak = (id) => {
        if(props.replyTo){ actions.getSqueak(id) }
        props.history.push(`/app/squeak/${id}`)
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
                <SentPayments />
                </>

                :
                tab === 'Received Payments' ?
                  <>
                    <ReceivedPayments />
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
