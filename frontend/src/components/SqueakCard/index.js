import React, { useContext, useState, useRef, useEffect } from 'react'
import { useDispatch } from 'react-redux'

import './style.scss'
import moment from 'moment'
import { getProfileImageSrcString } from '../../squeakimages/images';
import { Link, withRouter } from 'react-router-dom'
import { ICON_REPLY, ICON_RETWEET,
    ICON_HEART, ICON_HEARTFULL, ICON_DELETE, ICON_CLOSE,ICON_IMGUPLOAD, ICON_LOCKFILL} from '../../Icons'
import axios from 'axios'
import {API_URL} from '../../config'
import MakeSqueak from '../../features/squeaks/MakeSqueak'
import DeleteSqueak from '../../features/squeaks/DeleteSqueak'
import BuySqueak from '../../features/squeaks/BuySqueak'
import ContentEditable from 'react-contenteditable'

import {
  setLikeSqueak,
  setUnlikeSqueak,
  fetchSqueakOffers,
} from '../../features/squeaks/squeaksSlice'


const SqueakCard = React.memo(function SqueakCard(props) {
    const [replyModalOpen, setModalOpen] = useState(false)
    const [deleteModalOpen, setDeleteModalOpen] = useState(false)
    const [buyModalOpen, setBuyModalOpen] = useState(false)
    const [parent, setParent] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const dispatch = useDispatch()


    let info
    const likeSqueak = (e,id) => {
        if(e){ e.stopPropagation() }
        console.log('Clicked like with id', id);
        dispatch(setLikeSqueak(id));
    }
    const unlikeSqueak = (e,id) => {
        if(e){ e.stopPropagation() }
        console.log('Clicked unlike with id', id);
        dispatch(setUnlikeSqueak(id));
    }

    const resqueak = (e,id, resqueakId) => {
        e.preventDefault();
        e.stopPropagation()
        if(props.history.location.pathname.slice(1,5) === 'prof'){
            info = { dest: "profile", id, resqueakId }
        }else{ info = { id, resqueakId } }
        alert('Re-Squeak not yet implemented!');
    }

    const toggleReplyModal = (e, type) => {
        if(e){
            e.preventDefault();
            e.stopPropagation();
        }
        setStyleBody(!styleBody)
        if(type === 'parent'){setParent(true)}else{setParent(false)}
        setTimeout(()=>{ setModalOpen(!replyModalOpen) },20)
    }

    const toggleDeleteModal = (e, type) => {
        if(e){
            e.preventDefault();
            e.stopPropagation();
        }
        setStyleBody(!styleBody)
        if(type === 'parent'){setParent(true)}else{setParent(false)}
        setTimeout(()=>{ setDeleteModalOpen(!deleteModalOpen) },20)
    }

    const toggleBuyModal = (e, type) => {
        if(e){
            e.preventDefault();
            e.stopPropagation();
        }
        setStyleBody(!styleBody)
        if(type === 'parent'){setParent(true)}else{setParent(false)}
        setTimeout(()=>{ setBuyModalOpen(!buyModalOpen) },20)
    }


    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const isInitialMount = useRef(true);

    useEffect(() => {
        if (isInitialMount.current){ isInitialMount.current = false }
        else {
            document.getElementsByTagName("body")[0].style.cssText = styleBody && "overflow-y: hidden; margin-right: 17px"
        }
      }, [styleBody])

    useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )

    useEffect(()=> {
        if (isInitialMount.current){ isInitialMount.current = false;}
        else if(document.getElementById("replyBox")) {
          document.getElementById("replyBox").focus(); }
      }, [replyModalOpen])

    const goToUser = (e,username) => {
        e.stopPropagation()
        props.history.push(`/app/profile/${username}`)
    }

    moment.updateLocale('en', {
        relativeTime: { future: 'in %s', past: '%s ago', s:  'few seconds ago', ss: '%ss',
          m:  '1m', mm: '%dm', h:  '1h', hh: '%dh', d:  'a day', dd: '%dd', M:  'a month',
          MM: '%dM', y:  'a year', yy: '%dY' }
      });

    const author = props.user;

    return (
        <div>

        <Link onClick={(e)=>e.stopPropagation()} to={`/app/squeak/${props.id}`} key={props.id} className={props.squeak ? "Squeak-card-wrapper" : "Squeak-card-wrapper missing-squeak"} >

            {props.squeak ?
              <>
              <div className="card-userPic-wrapper">
                  <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.squeak.getAuthorPubkey()}`}>
                      <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={author ? `${getProfileImageSrcString(author)}` : null}/>
                  </Link>
                  {props.hasReply? <div className="squeak-reply-thread"></div> : null}
              </div>
              <div className="card-content-wrapper">
                  <div className="card-content-header">
                      <div className="card-header-detail">
                          <span className="card-header-user">
                              <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.squeak.getAuthorPubkey()}`}>{author ? author.getProfileName(): 'Unknown Author'}</Link>
                          </span>
                          <span className="card-header-username">
                              <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.squeak.getAuthorPubkey()}`}>{'@'+ props.squeak.getAuthorPubkey()}</Link>
                          </span>
                          <span className="card-header-dot">·</span>
                          <span className="card-header-date">
                                  {moment(props.squeak.getBlockTime() * 1000).fromNow(true)}
                          </span>
                      </div>
                      <div className="card-header-more">

                      </div>
                  </div>

                  {props.squeak.getContentStr() ?
                    <div className="card-content-info">
                        {props.squeak.getContentStr()}
                    </div> :
                    <div onClick={(e)=> {
                      e.preventDefault();
                      dispatch(fetchSqueakOffers(props.id));
                      toggleBuyModal();
                    }
                  }
                       className="card-content-info card-content-locked-content">
                        <ICON_LOCKFILL styles={{width:'36px', height:"36px", padding: "5px"}} />
                        <div>
                        Locked content
                        </div>
                    </div>
                  }

                  <div className="card-buttons-wrapper">
                      <div onClick={(e)=>toggleReplyModal(e)} className="card-button-wrap reply-wrap">
                          <div className="card-icon reply-icon">
                              <ICON_REPLY styles={{fill:'rgb(101, 119, 134)'}}/>
                          </div>
                          <div className="card-icon-value">
                              {props.squeak.getNumReplies()}
                          </div>
                      </div>
                      <div onClick={(e)=>resqueak(e,props.id)} className="card-button-wrap resqueak-wrap">
                          <div className="card-icon resqueak-icon">
                              <ICON_RETWEET styles={false ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                          </div>
                          <div className="card-icon-value">
                              0
                          </div>
                      </div>
                      <div onClick={(e)=> {
                        e.preventDefault();
                        props.squeak.getLikedTimeMs() ?
                        unlikeSqueak(e, props.squeak.getSqueakHash()) :
                        likeSqueak(e, props.squeak.getSqueakHash())
                      }} className="card-button-wrap heart-wrap">
                          <div className="card-icon heart-icon">
                              {props.squeak.getLikedTimeMs() ?
                              <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}/> :
                              <ICON_HEART styles={{fill:'rgb(101, 119, 134)'}}/>}
                          </div>
                      </div>
                      <div onClick={(e)=>toggleDeleteModal(e)} className="card-button-wrap">
                          <div className="card-icon share-icon">
                              <ICON_DELETE styles={{fill:'rgb(101, 119, 134)'}} />
                          </div>
                      </div>
                  </div>
              </div>
              </> :
              <>
              <div className="card-userPic-wrapper">
                      <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={null}/>
                  {props.hasReply? <div className="squeak-reply-thread"></div> : null}
              </div>
              <div className="card-content-wrapper">
                  <div className="card-content-info">
                  Missing Squeak
                  </div>
              </div>
              </>
            }

        </Link>

        {/* reply modal */}
        {props.squeak ?
            <div onClick={()=>toggleReplyModal()} style={{display: replyModalOpen ? 'block' : 'none'}} className="modal-edit">
            {replyModalOpen ?
            <div style={{minHeight: '350px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleReplyModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Reply</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                  <MakeSqueak replyToSqueak={props.squeak} submittedCallback={toggleReplyModal} />
                </div>
            </div> : null}
        </div> : null}

        {/* delete modal */}
        {props.squeak ?
            <div onClick={()=>toggleDeleteModal()} style={{display: deleteModalOpen ? 'block' : 'none'}} className="modal-edit">
            {deleteModalOpen ?
            <div style={{minHeight: '350px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleDeleteModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Delete Squeak</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                  <DeleteSqueak squeakHash={props.id} submittedCallback={toggleDeleteModal} />
                </div>
            </div> : null}
        </div> : null}

        {/* buy modal */}
        {props.squeak ?
            <div onClick={()=>toggleBuyModal()} style={{display: buyModalOpen ? 'block' : 'none'}} className="modal-edit">
            {buyModalOpen ?
            <div style={{minHeight: '350px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleBuyModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Buy Squeak</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                  <BuySqueak squeak={props.squeak} submittedCallback={toggleBuyModal} />
                </div>
            </div> : null}
        </div> : null}


        </div>
    )
});

export default withRouter(SqueakCard)
