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
import Select from 'react-select'


const SqueakPage = (props) => {
    let history = useHistory();

    const { state, actions } = useContext(StoreContext)
    const {squeak, ancestorSqueaks, replySqueaks, squeakOffers, network, session} = state

    const [modalOpen, setModalOpen] = useState(false)
    const [buyModalOpen, setBuyModalOpen] = useState(false)
    const [offer, setOffer] = useState(null)


    useEffect(()=>{
        window.scrollTo(0, 0)
        actions.getSqueak(props.match.params.id)
        actions.getAncestorSqueaks(props.match.params.id)
        actions.getReplySqueaks(props.match.params.id)
        actions.getNetwork()
    }, [props.match.params.id])
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
        <div className="squeak-wrapper">
            <div className="squeak-header-wrapper">
                <div className="profile-header-back">
                    <div onClick={()=>goBack()} className="header-back-wrapper">
                        <ICON_ARROWBACK/>
                    </div>
                </div>
                <div className="squeak-header-content"> Squeak </div>
            </div>

            {/* Unknown Ancestor squeak */}
            {ancestorSqueaks.length > 0 && ancestorSqueaks[0].getReplyTo() &&
              <SqueakCard squeak={null} key={ancestorSqueaks[0].getReplyTo()} id={ancestorSqueaks[0].getReplyTo()}
                replies={[]} hasReply={true} />
            }



            {/* Ancestor squeaks */}
            {ancestorSqueaks.slice(0, -1).map(r=>{
              // TODO: use replies instead of empty array.
              return <SqueakCard squeak={r} key={r.getSqueakHash()} id={r.getSqueakHash()} user={r.getAuthor()}
                replies={[]} hasReply={true} />
            })}

            {/* Current squeak */}
            <div className={squeak ? "squeak-body-wrapper" : "squeak-body-wrapper missing-squeak"}>

                {squeak ?
                <>
                <div className="squeak-header-content">
                    <div className="squeak-user-pic">
                        <Link to={`/app/profile/${squeak.getAuthorPubkey()}`}>
                            <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={author ? `${getProfileImageSrcString(author)}` : null}/>
                        </Link>
                    </div>
                    <div className="squeak-user-wrap">
                        <div className="squeak-user-name">
                            {author ?
                               author.getProfileName() :
                               'Unknown Author'
                             }
                        </div>
                        <div className="squeak-username">
                            @{squeak.getAuthorPubkey()}
                        </div>
                    </div>
                </div>

                {state.loading ?
                   <Loader /> :
                   <>
                   {squeak.getContentStr() ?
                     <div className="squeak-content">
                         {squeak.getContentStr()}
                     </div> :
                     <div className="squeak-content locked-content">
                         <ICON_LOCKFILL styles={{width:'48px', height:"48px", padding: "5px"}} />
                         <div onClick={()=>toggleBuyModal(props.match.params.id)}
                          className='squeak-unlock-button'>
                             <span>Unlock</span>
                         </div>
                     </div>
                   }
                   </>
                }



                <div className="squeak-date">
                    <a href={getBlockDetailUrl(squeak.getBlockHash(), network)}
                     target="_blank"
                     rel="noopener"
                     >
                        {moment(squeak.getBlockTime() * 1000).format("h:mm A · MMM D, YYYY")} (Block #{squeak.getBlockHeight()})
                    </a>
                </div>
                <div className="squeak-stats">
                    <div className="int-num"> 0 </div>
                    <div className="int-text"> Sats Spent </div>
                    <div className="int-num"> 0 </div>
                    <div className="int-text"> Sats Earned </div>
                </div>
                <div className="squeak-interactions">
                    <div onClick={()=>toggleModal()} className="squeak-int-icon">
                        <div className="card-icon reply-icon"> <ICON_REPLY /> </div>
                    </div>
                    <div onClick={()=>resqueak(squeak.getSqueakHash())} className="squeak-int-icon">
                        <div className="card-icon resqueak-icon">
                             <ICON_RETWEET styles={false ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                        </div>
                    </div>
                    <div onClick={()=>{
                      squeak.getLikedTimeMs() ?
                      unlikeSqueak(squeak.getSqueakHash()) :
                      likeSqueak(squeak.getSqueakHash())
                    }} className="squeak-int-icon">
                        <div className="card-icon heart-icon">
                        {squeak.getLikedTimeMs() ? <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}
                         /> : <ICON_HEART/>} </div>
                    </div>
                    <div onClick={()=>deleteSqueak(squeak.getSqueakHash())} className="squeak-int-icon">
                        <div className="card-icon delete-icon">
                            <ICON_DELETE styles={{fill:'rgb(101, 119, 134)'}} />
                        </div>
                    </div>
                </div>
                </> :
                <div className="squeak-header-content">
                    <div className="squeak-user-pic">
                            <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={null}/>
                    </div>
                    <div className="squeak-content">
                        Missing Squeak
                        <div onClick={()=>downloadSqueak(props.match.params.id)}
                         className='profiles-create-button'>
                            <span>Download Squeak</span>
                        </div>
                    </div>
                </div>
              }
            </div>

            {/* Reply squeaks */}
            {replySqueaks.map(r=>{
                // TODO: use replies instead of empty array.
                return <SqueakCard squeak={r}  key={r.getSqueakHash()} id={r.getSqueakHash()} user={r.getAuthor()}/>
            })}

        </div>

        {squeak ?
        <div onClick={()=>toggleModal()} style={{display: modalOpen ? 'block' : 'none'}} className="modal-edit">
            {modalOpen ?
            <div style={{minHeight: '379px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Reply</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                  <MakeSqueak replyToSqueak={squeak} submittedCallback={toggleModal} />
                </div>
            </div> : null}
        </div>:null}

        {squeak ?
        <div onClick={()=>toggleBuyModal()} style={{display: buyModalOpen ? 'block' : 'none'}} className="modal-edit">
            {buyModalOpen ?
            <div style={{minHeight: '379px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleBuyModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Buy Squeak</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                    {squeakOffers.length} offers.
                    <div className="Squeak-input-side">
                        <div className="inner-input-box">
                            <Select options={optionsFromOffers(squeakOffers)} onChange={handleChangeOffer} />
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
                              <b>Lightning Node</b>: {offer.getNodePubkey()}@{offer.getNodeHost()}:{offer.getNodePort()}
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
            </div> : null}
        </div>:null}
        </>
    )
}

export default withRouter(SqueakPage)
