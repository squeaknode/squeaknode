import React , { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import { withRouter, useHistory , Link } from 'react-router-dom'
import './style.scss'
import moment from 'moment'
import Loader from '../Loader'
import { ICON_ARROWBACK, ICON_HEART, ICON_REPLY, ICON_RETWEET, ICON_HEARTFULL,
ICON_DELETE, ICON_IMGUPLOAD, ICON_CLOSE, ICON_LOCKFILL } from '../../Icons'
import axios from 'axios'
import {API_URL} from '../../config'
import { getProfileImageSrcString } from '../../squeakimages/images';
import ContentEditable from 'react-contenteditable'
import MakeSqueak from '../MakeSqueak'
import SqueakCard from '../SqueakCard'
import Squeak from '../../features/squeak/Squeak'
import Select from 'react-select'


const SqueakPage = (props) => {
    let history = useHistory();

    const { state, actions } = useContext(StoreContext)
    const {squeak, ancestorSqueaks, replySqueaks, squeakOffers, network, session} = state

    const [modalOpen, setModalOpen] = useState(false)
    const [buyModalOpen, setBuyModalOpen] = useState(false)
    const [offer, setOffer] = useState(null)


    // useEffect(()=>{
    //     window.scrollTo(0, 0)
    //     actions.getSqueak(props.match.params.id)
    //     actions.getAncestorSqueaks(props.match.params.id)
    //     actions.getReplySqueaks(props.match.params.id)
    //     actions.getNetwork()
    // }, [props.match.params.id])
    var image = new Image()

    let info
    const likeSqueak = (id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        actions.likeSqueak(id)
    }
    const unlikeSqueak = (id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        actions.unlikeSqueak(id)
    }
    const resqueak = (id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        info = { dest: "squeak", id }
        // actions.resqueak(info)
        alert('Re-Squeak not yet implemented!');
    }
    const deleteSqueak = (id) => {
        actions.deleteSqueak(id)
    }
    const downloadSqueak = (id) => {
        actions.downloadSqueak(id)
    }
    const buySqueak = (id) => {
        const offerId = offer && offer.getOfferId();
        if (!offerId) {
          return;
        }
        const values = {
          offerId: offerId,
          squeakHash: props.match.params.id,
        }
        actions.buySqueak(values)
        toggleBuyModal();
    }

    const toggleModal = (e, type) => {
        if(e){ e.stopPropagation() }
        // if(param === 'edit'){setSaved(false)}
        // if(type === 'parent'){setParent(true)}else{setParent(false)}
        setModalOpen(!modalOpen)
    }

    const toggleBuyModal = () => {
        actions.getSqueakOffers(props.match.params.id);
        // if(param === 'edit'){setSaved(false)}
        // if(type === 'parent'){setParent(true)}else{setParent(false)}
        setBuyModalOpen(!buyModalOpen)
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const goBack = () => {
        history.goBack()
    }

    const getBlockDetailUrl = (blockHash, network) => {
      switch (network) {
        case 'mainnet':
          return `https://blockstream.info/block/${blockHash}`;
        case 'testnet':
          return `https://blockstream.info/testnet/block/${blockHash}`;
        default:
          return '';
      }
    }

    const optionsFromOffers = (offers) => {
      return offers.map((offer) => {
          return { value: offer, label: `${offer.getPriceMsat() / 1000} sats (${offer.getPeerAddress().getHost()}:${offer.getPeerAddress().getPort()})` }
        });
    }

    const handleChangeOffer = (e) => {
      setOffer(e.value);
    }

    const author = squeak && squeak.getAuthor()


    return(
        <>
        <Squeak id={props.match.params.id} />
        </>
    )
}

export default withRouter(SqueakPage)
