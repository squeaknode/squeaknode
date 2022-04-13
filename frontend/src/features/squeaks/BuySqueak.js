import React, { useEffect, useState, useContext, useRef } from 'react'
import { withRouter } from 'react-router-dom'
import { unwrapResult } from '@reduxjs/toolkit'

import moment from 'moment'
import ContentEditable from 'react-contenteditable'
import { Link } from 'react-router-dom'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../../components/Loader'

import { Form, Input, Checkbox, Relevant, Debug, TextArea, Option } from 'informed';

import Select from 'react-select'

import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'


import {
  setBuySqueak,
  selectBuySqueakStatus,
} from '../squeaks/squeaksSlice'
import {
  fetchPaymentSummaryForSqueak,
  selectPaymentSummaryForSqueak,
} from '../../features/payments/paymentsSlice'
import {
  selectSigningProfiles,
  fetchSigningProfiles,
} from '../../features/profiles/profilesSlice'

const BuySqueak = (props) => {
  console.log(props.squeakHash);
  console.log(props.squeakOffers);

  const signingProfiles = useSelector(selectSigningProfiles);
  const buySqueakStatus = useSelector(selectBuySqueakStatus);
  const dispatch = useDispatch();

  const [offer, setOffer] = useState(null)


  useEffect(() => {
    dispatch(fetchSigningProfiles());
  }, [])

  const buySqueak = (id) => {
    const offerId = offer && offer.getOfferId();
    if (!offerId) {
      return;
    }
    const values = {
      offerId: offerId,
      squeakHash: props.squeakHash,
    }
    console.log('Buy clicked.');
    dispatch(setBuySqueak(values))
    .then(unwrapResult)
    .then(() => {
      dispatch(fetchPaymentSummaryForSqueak({squeakHash: props.squeakHash}));
    })
    .catch((err) => {
      alert(err.message);
    });
    if (props.submittedCallback) {
      props.submittedCallback();
    }
  }

  const handleChangeOffer = (e) => {
    setOffer(e.value);
  }

  const optionsFromOffers = (offers) => {
    console.log("optionsFromOffers");
    console.log(offers);
    return offers.map((offer) => {
      return { value: offer, label: `${offer.getPriceMsat() / 1000} sats (${offer.getPeerAddress().getHost()}:${offer.getPeerAddress().getPort()})` }
    });
  }

  return (
    <>


    <div className="Squeak-input-side">
      <div className="edit-input-wrap">
        {props.squeakOffers.length} offers
        <div className="inner-input-box">
          <Select options={optionsFromOffers(props.squeakOffers)} onChange={handleChangeOffer} />
        </div>
        {offer &&
          <>
          <div className="inner-input-box">
            <b>Price</b>: {offer.getPriceMsat() / 1000} sats
            </div>
            <div className="inner-input-box">
              <b>Peer</b>: {offer.getPeerAddress().getHost()}:{offer.getPeerAddress().getPort()}
              </div>
              <div className="inner-input-box">
                <b>Lightning Node</b>:&nbsp;
                  <a href={`https://amboss.space/node/${offer.getNodePubkey()}`}
                    target="_blank" rel="noopener noreferrer"
                    style={{color: "blue", fontWeight: 'bold'}}
                    >
                    {offer.getNodePubkey()}@{offer.getNodeHost()}:{offer.getNodePort()}
                  </a>
                </div>
                </>
            }
            <div className="inner-input-links">
              <div className="input-links-side">
              </div>
              <div className="squeak-btn-holder">
                <div onClick={buySqueak} className={offer ? 'squeak-btn-side squeak-btn-active' : 'squeak-btn-side'}>
                  Buy
                </div>
              </div>
            </div>
          </div>


        </div>


      </>
  )
}

export default withRouter(BuySqueak)
