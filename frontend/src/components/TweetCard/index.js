import React, { useContext, useState, useRef, useEffect } from 'react'
import './style.scss'
import moment from 'moment'
import { StoreContext } from '../../store/store'
import { getProfileImageSrcString } from '../../squeakimages/images';
import { Link, withRouter } from 'react-router-dom'
import { ICON_REPLY, ICON_RETWEET,
    ICON_HEART, ICON_HEARTFULL, ICON_DELETE, ICON_CLOSE,ICON_IMGUPLOAD} from '../../Icons'
import axios from 'axios'
import {API_URL} from '../../config'
import MakeSqueak from '../MakeSqueak'
import ContentEditable from 'react-contenteditable'



const TweetCard = React.memo(function TweetCard(props) {
    const { state, actions } = useContext(StoreContext)
    const {account, session} = state

    const [modalOpen, setModalOpen] = useState(false)
    const [parent, setParent] = useState(false)
    const [styleBody, setStyleBody] = useState(false)

    let info
    const likeTweet = (e,id) => {
        if(e){ e.stopPropagation() }
        if(!session){ actions.alert('Please Sign In'); return }
        actions.likeTweet(id)
    }
    const unlikeTweet = (e,id) => {
        if(e){ e.stopPropagation() }
        if(!session){ actions.alert('Please Sign In'); return }
        actions.unlikeTweet(id)
    }

    const retweet = (e,id, retweetId) => {
        e.stopPropagation()
        if(!session){ actions.alert('Please Sign In'); return }
        if(props.history.location.pathname.slice(1,5) === 'prof'){
            info = { dest: "profile", id, retweetId }
        }else{ info = { id, retweetId } }
        actions.retweet(info)
    }

    const deleteTweet = (e,id) => {
        e.stopPropagation()
        actions.deleteTweet(id)
    }

    const goToTweet = (id) => {
        if(props.replyTo){ actions.getTweet(id) }
        props.history.push(`/tweet/${id}`)
    }
    const goToReply = (e,id) => {
        e.stopPropagation()
        if(props.replyTo){ actions.getTweet(id) }
        props.history.push(`/tweet/${id}`)
    }

    const toggleModal = (e, type) => {
        if(e){ e.stopPropagation() }
        if(!session){ actions.alert('Please Sign In'); return }
        setStyleBody(!styleBody)
        if(type === 'parent'){setParent(true)}else{setParent(false)}
        setTimeout(()=>{ setModalOpen(!modalOpen) },20)
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
      }, [modalOpen])

    const goToUser = (e,username) => {
        e.stopPropagation()
        props.history.push(`/profile/${username}`)
    }

    moment.updateLocale('en', {
        relativeTime: { future: 'in %s', past: '%s ago', s:  'few seconds ago', ss: '%ss',
          m:  '1m', mm: '%dm', h:  '1h', hh: '%dh', d:  'a day', dd: '%dd', M:  'a month',
          MM: '%dM', y:  'a year', yy: '%dY' }
      });

    const author = props.user;

    return (
        <div>

        <div onClick={()=>goToTweet(props.id)} key={props.id} className={props.tweet ? "Tweet-card-wrapper" : "Tweet-card-wrapper missing-tweet"} >

            {props.tweet ?
              <>
              <div className="card-userPic-wrapper">
                  <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.tweet.getAuthorPubkey()}`}>
                      <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={author ? `${getProfileImageSrcString(author)}` : null}/>
                  </Link>
                  {props.hasReply? <div className="tweet-reply-thread"></div> : null}
              </div>
              <div className="card-content-wrapper">
                  <div className="card-content-header">
                      <div className="card-header-detail">
                          <span className="card-header-user">
                              <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.tweet.getAuthorPubkey()}`}>{author ? author.getProfileName(): 'Unknown Author'}</Link>
                          </span>
                          <span className="card-header-username">
                              <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.tweet.getAuthorPubkey()}`}>{'@'+ props.tweet.getAuthorPubkey()}</Link>
                          </span>
                          <span className="card-header-dot">·</span>
                          <span className="card-header-date">
                                  {moment(props.tweet.getBlockTime() * 1000).fromNow(true)}
                          </span>
                      </div>
                      <div className="card-header-more">

                      </div>
                  </div>

                  {props.tweet.getContentStr() ?
                    <div className="card-content-info">
                        {props.tweet.getContentStr()}
                    </div> :
                    <div className="card-content-info card-content-locked-content">
                        Locked content
                    </div>
                  }

                  <div className="card-buttons-wrapper">
                      <div onClick={(e)=>toggleModal(e)} className="card-button-wrap reply-wrap">
                          <div className="card-icon reply-icon">
                              <ICON_REPLY styles={{fill:'rgb(101, 119, 134)'}}/>
                          </div>
                          <div className="card-icon-value">
                              0
                          </div>
                      </div>
                      <div onClick={(e)=>retweet(e,props.id)} className="card-button-wrap retweet-wrap">
                          <div className="card-icon retweet-icon">
                              <ICON_RETWEET styles={account && account.retweets.includes(props.id) ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                          </div>
                          <div className="card-icon-value">
                              0
                          </div>
                      </div>
                      <div onClick={(e)=>
                        props.tweet.getLikedTimeMs() ?
                        unlikeTweet(e, props.tweet.getSqueakHash()) :
                        likeTweet(e, props.tweet.getSqueakHash())
                      } className="card-button-wrap heart-wrap">
                          <div className="card-icon heart-icon">
                              {account && props.tweet.getLikedTimeMs() ?
                              <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}/> :
                              <ICON_HEART styles={{fill:'rgb(101, 119, 134)'}}/>}
                          </div>
                          <div className="card-icon-value">
                              0
                          </div>
                      </div>
                      <div onClick={(e)=>deleteTweet(e,props.id)} className="card-button-wrap">
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
                  {props.hasReply? <div className="tweet-reply-thread"></div> : null}
              </div>
              <div className="card-content-wrapper">
                  <div className="card-content-info">
                  Missing Tweet
                  </div>
              </div>
              </>
            }

        </div>

        {/* tweet modal */}
        {props.tweet ?
            <div onClick={()=>toggleModal()} style={{display: modalOpen ? 'block' : 'none'}} className="modal-edit">
            {modalOpen ?
            <div style={{minHeight: '350px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Reply</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                  <MakeSqueak replyToTweet={props.tweet} submittedCallback={toggleModal} />
                </div>
            </div> : null}
        </div> : null}
        </div>
    )
});

export default withRouter(TweetCard)
