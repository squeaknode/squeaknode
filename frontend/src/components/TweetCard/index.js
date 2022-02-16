import React, { useContext, useState, useRef, useEffect } from 'react'
import './style.scss'
import moment from 'moment'
import { StoreContext } from '../../store/store'
import { getProfileImageSrcString } from '../../squeakimages/images';
import { Link, withRouter } from 'react-router-dom'
import { ICON_REPLY, ICON_RETWEET,
    ICON_HEART, ICON_BOOKMARK, ICON_HEARTFULL, ICON_BOOKMARKFILL, ICON_DELETE, ICON_CLOSE,ICON_IMGUPLOAD} from '../../Icons'
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
        e.stopPropagation()
        if(!session){ actions.alert('Please Sign In'); return }
        if(props.history.location.pathname.slice(1,5) === 'prof'){
            info = { dest: "profile", id }
        }else{ info = { id } }
        actions.likeTweet(info)
    }

    const bookmarkTweet = (e,id) => {
        e.stopPropagation()
        if(!session){ actions.alert('Please Sign In'); return }
        if(props.history.location.pathname.slice(1,5) === 'prof'){
            info = { dest: "profile", id }
        }else{ info = { id } }
        actions.bookmarkTweet(info)
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

    return (
        <div>

          {props.retweet && props.retweet._id ?
            <div onClick={()=>goToTweet(props.retweet._id)} key={props.retweet._id} className="Tweet-card-wrapper">
                <div className="card-userPic-wrapper">
                    <div className="user-retweet-icon">
                        <ICON_RETWEET />
                    </div>
                    <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.retweet.user.getPubkey()}`}>
                        <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(props.retweet.user)}`}/>
                    </Link>
                </div>
                <div className="card-content-wrapper">
                    {props.user._id === account && account._id ?
                    <div onClick={(e)=>goToUser(e,account.username)} className="user-retweeted"> You Retweeted </div> :
                    <div onClick={(e)=>goToUser(e,props.user.getPubkey())} className="user-retweeted"> {props.user.getPubkey()} Retweeted </div>}
                    <div className="card-content-header">
                        <div className="card-header-detail">
                            <span className="card-header-user">
                                <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.retweet.user.getPubkey()}`}>{props.retweet.user.getProfileName()}</Link>
                            </span>
                            <span className="card-header-username">
                                <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.retweet.user.getPubkey()}`}>{'@'+ props.retweet.user.getPubkey()}</Link>
                            </span>
                            <span className="card-header-dot">·</span>
                            <span className="card-header-date">
                                    {moment(props.retweet.createdAt).fromNow(true)}
                            </span>
                        </div>
                        <div className="card-header-more">

                        </div>
                    </div>
                    {props.retweet.replyTo ?
                    <div className="replyTo-wrapper">
                        <span className="reply-tweet-username">
                                Replying to
                            </span>
                            <span className="main-tweet-user">
                                @{props.retweet.replyTo}
                            </span>
                    </div> : null }
                    <div className="card-content-info">
                    {props.retweet.description}
                    </div>
                    {props.retweet.images[0] &&
                    <div className="card-content-images">
                        <div className="card-image-link">
                            <img alt="" src={props.retweet.images[0]}/>
                        </div>
                    </div> }
                    <div className="card-buttons-wrapper">
                        <div onClick={(e)=>toggleModal(e)} className="card-button-wrap reply-wrap">
                            <div className="card-icon reply-icon">
                                <ICON_REPLY styles={{fill:'rgb(101, 119, 134)'}}/>
                            </div>
                            <div className="card-icon-value">
                                {props.retweet.replies.length > 0 && props.retweet.replies.length}
                            </div>
                        </div>
                        <div onClick={(e)=>retweet(e, props.retweet._id, props.id)} className="card-button-wrap retweet-wrap">
                            <div className="card-icon retweet-icon">
                                <ICON_RETWEET styles={account && account.retweets.includes(props.retweet._id) ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                            </div>
                            <div style={{color: account && account.retweets.includes(props.retweet._id) && 'rgb(23, 191, 99)', opacity: props.retweet.retweets.length > 0 ? '1':'0'}} className="card-icon-value">
                                {props.retweet.retweets.length}
                            </div>
                        </div>
                        <div onClick={(e)=>likeTweet(e,props.retweet._id)} className="card-button-wrap heart-wrap">
                            <div className="card-icon heart-icon">
                                {account && account.likes.includes(props.retweet._id) ?
                                <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}/> :
                                <ICON_HEART styles={{fill:'rgb(101, 119, 134)'}}/>}
                            </div>
                            <div style={{color: account && account.likes.includes(props.retweet._id) && 'rgb(224, 36, 94)', opacity: props.retweet.likes.length > 0 ? '1':'0'}} className="card-icon-value">
                                {props.retweet.likes.length}
                            </div>
                        </div>
                        <div onClick={(e)=>account && account.username === props.retweet.user.getPubkey() ? deleteTweet(e,props.retweet._id): bookmarkTweet(e,props.retweet._id)} className="card-button-wrap">
                            <div className={account && account && account && account.username === props.retweet.user.getPubkey() ? "card-icon delete-icon" :"card-icon share-icon"}>
                                {account && account && account && account.username === props.retweet.user.getPubkey() ?
                                <ICON_DELETE styles={{fill:'rgb(101, 119, 134)'}} /> : account && account.bookmarks.includes(props.retweet._id) ?
                                <ICON_BOOKMARKFILL styles={{fill:'rgb(10, 113, 176)'}}/> :
                                <ICON_BOOKMARK styles={{fill:'rgb(101, 119, 134)'}}/>}
                            </div>
                        </div>
                    </div>
                </div>
            </div> : props.user ?
            <div onClick={()=>goToTweet(props.id)} key={props.id} className="Tweet-card-wrapper">
            <div className="card-userPic-wrapper">
                {/* <div className="user-retweet-icon">
                    <ICON_RETWEET />
                </div> */}
                <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.user.getPubkey()}`}>
                    <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(props.user)}`}/>
                </Link>
                {props.hasReply? <div className="tweet-reply-thread"></div> : null}
            </div>
            <div className="card-content-wrapper">
                {/* {props.username === account.username && props.retweets.includes(account._id) ?
                <div className="user-retweeted"> You Retweeted </div> :
                props.username !== account.username &&  */}
                <div className="card-content-header">
                    <div className="card-header-detail">
                        <span className="card-header-user">
                            <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.user.getPubkey()}`}>{props.user.getProfileName()}</Link>
                        </span>
                        <span className="card-header-username">
                            <Link onClick={(e)=>e.stopPropagation()} to={`/profile/${props.user.getPubkey()}`}>{'@'+ props.user.getPubkey()}</Link>
                        </span>
                        <span className="card-header-dot">·</span>
                        <span className="card-header-date">
                                {moment(props.createdAt * 1000).fromNow(true)}
                        </span>
                    </div>
                    <div className="card-header-more">

                    </div>
                </div>
                {props.replyTo ?
                <div className="replyTo-wrapper">
                    <span className="reply-tweet-username">
                            Replying to
                        </span>
                        <span className="main-tweet-user">
                            @{props.replyTo}
                        </span>
                </div> : null }
                <div className="card-content-info">
                {props.description}
                </div>
                {props.images[0] &&
                <div className="card-content-images">
                    <div className="card-image-link">
                        <img alt="" src={props.images[0]}/>
                    </div>
                </div> }
                <div className="card-buttons-wrapper">
                    <div onClick={(e)=>toggleModal(e)} className="card-button-wrap reply-wrap">
                        <div className="card-icon reply-icon">
                            <ICON_REPLY styles={{fill:'rgb(101, 119, 134)'}}/>
                        </div>
                        <div className="card-icon-value">
                            {props.replies.length > 0 && props.replies.length}
                        </div>
                    </div>
                    <div onClick={(e)=>retweet(e,props.id)} className="card-button-wrap retweet-wrap">
                        <div className="card-icon retweet-icon">
                            <ICON_RETWEET styles={account && account.retweets.includes(props.id) ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                        </div>
                        <div style={{color: account && account.retweets.includes(props.id) && 'rgb(23, 191, 99)', opacity: props.retweets.length > 0 ? '1':'0'}} className="card-icon-value">
                            {props.retweets.length}
                        </div>
                    </div>
                    <div onClick={(e)=>likeTweet(e,props.id)} className="card-button-wrap heart-wrap">
                        <div className="card-icon heart-icon">
                            {account && account.likes.includes(props.id) ?
                            <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}/> :
                            <ICON_HEART styles={{fill:'rgb(101, 119, 134)'}}/>}
                        </div>
                        <div style={{color: account && account.likes.includes(props.id) && 'rgb(224, 36, 94)', opacity: props.likes.length > 0 ? '1':'0'}} className="card-icon-value">
                            {props.likes.length}
                        </div>
                    </div>
                    <div onClick={(e)=>account && account.username === props.user.getPubkey() ? deleteTweet(e,props.id): bookmarkTweet(e,props.id)} className="card-button-wrap">
                        <div className={account && account && account && account.username === props.user.getPubkey() ? "card-icon delete-icon" :"card-icon share-icon"}>
                            {account && account && account && account.username === props.user.getPubkey() ?
                            <ICON_DELETE styles={{fill:'rgb(101, 119, 134)'}} /> : account && account.bookmarks.includes(props.id) ?
                            <ICON_BOOKMARKFILL styles={{fill:'rgb(10, 113, 176)'}}/> :
                            <ICON_BOOKMARK styles={{fill:'rgb(101, 119, 134)'}}/>}
                        </div>
                    </div>
                </div>
            </div>
        </div> : null}

                                                                                        {/* tweet modal */}
        {props.parent || props.user ?
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
                  <MakeSqueak replyTo={props.id} user={props.user} createdAt={props.createdAt} description={props.description} />
                </div>
            </div> : null}
        </div> : null}
        </div>
    )
});

export default withRouter(TweetCard)
