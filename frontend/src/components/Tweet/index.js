import React , { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import { withRouter, useHistory , Link } from 'react-router-dom'
import './style.scss'
import moment from 'moment'
import Loader from '../Loader'
import { ICON_ARROWBACK, ICON_HEART, ICON_REPLY, ICON_RETWEET, ICON_HEARTFULL,
ICON_DELETE, ICON_IMGUPLOAD, ICON_CLOSE } from '../../Icons'
import axios from 'axios'
import {API_URL} from '../../config'
import { getProfileImageSrcString } from '../../squeakimages/images';
import ContentEditable from 'react-contenteditable'
import MakeSqueak from '../MakeSqueak'
import TweetCard from '../TweetCard'


const TweetPage = (props) => {
    let history = useHistory();

    const { state, actions } = useContext(StoreContext)
    const {tweet, ancestorTweets, replyTweets, account, session} = state

    const [modalOpen, setModalOpen] = useState(false)

    useEffect(()=>{
        window.scrollTo(0, 0)
        actions.getTweet(props.match.params.id)
        actions.getAncestorTweets(props.match.params.id)
        actions.getReplyTweets(props.match.params.id)
    }, [props.match.params.id])
    var image = new Image()

    let info
    const likeTweet = (id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        info = { dest: "tweet", id }
        actions.likeTweet(info)
    }
    const retweet = (id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        info = { dest: "tweet", id }
        actions.retweet(info)
    }
    const deleteTweet = (id) => {
        actions.deleteTweet(id)
    }

    const toggleModal = (e, type) => {
        if(e){ e.stopPropagation() }
        // if(param === 'edit'){setSaved(false)}
        // if(type === 'parent'){setParent(true)}else{setParent(false)}
        setModalOpen(!modalOpen)
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const goBack = () => {
        history.goBack()
    }

    return(
        <>
            {tweet ?
            <div className="tweet-wrapper">
            <div className="tweet-header-wrapper">
                <div className="profile-header-back">
                    <div onClick={()=>goBack()} className="header-back-wrapper">
                        <ICON_ARROWBACK/>
                    </div>
                </div>
                <div className="tweet-header-content"> Tweet </div>
            </div>

            {ancestorTweets.slice(0, -1).map(r=>{
              // TODO: use replies instead of empty array.
              return <TweetCard tweet={r} retweet={r.getReplyTo()} username={r.getAuthorPubkey()} name={r.getAuthorPubkey()} parent={null} key={r.getSqueakHash()} id={r.getSqueakHash()} user={r.getAuthor()} createdAt={r.getBlockTime()} description={r.getContentStr()}
                images={[]} replies={[]} retweets={[]} likes={[]} hasReply={true} />
            })}

            <div className="tweet-body-wrapper">
                <div className="tweet-header-content">
                    <div className="tweet-user-pic">
                        <Link to={`/profile/${tweet.getAuthor().getPubkey()}`}>
                            <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(tweet.getAuthor())}`}/>
                        </Link>
                    </div>
                    <div className="tweet-user-wrap">
                        <div className="tweet-user-name">
                            {tweet.getAuthor().getProfileName()}
                        </div>
                        <div className="tweet-username">
                            @{tweet.getAuthor().getPubkey()}
                        </div>
                    </div>
                </div>
                <div className="tweet-content">
                    {tweet.getContentStr()}
                </div>

                <div className="tweet-date">
                    {moment(tweet.getBlockTime() * 1000).format("h:mm A · MMM D, YYYY")}
                </div>
                <div className="tweet-stats">
                    <div className="int-num"> 0 </div>
                    <div className="int-text"> Retweets </div>
                    <div className="int-num"> 0 </div>
                    <div className="int-text"> Likes </div>
                </div>
                <div className="tweet-interactions">
                    <div onClick={()=>toggleModal()} className="tweet-int-icon">
                        <div className="card-icon reply-icon"> <ICON_REPLY /> </div>
                    </div>
                    <div onClick={()=>retweet(tweet.getSqueakHash())} className="tweet-int-icon">
                        <div className="card-icon retweet-icon">
                             <ICON_RETWEET styles={account && account.retweets.includes(tweet.getSqueakHash()) ? {stroke: 'rgb(23, 191, 99)'} : {fill:'rgb(101, 119, 134)'}}/>
                        </div>
                    </div>
                    <div onClick={()=>likeTweet(tweet.getSqueakHash())} className="tweet-int-icon">
                        <div className="card-icon heart-icon">
                        {account && account.likes.includes(tweet.getSqueakHash()) ? <ICON_HEARTFULL styles={{fill:'rgb(224, 36, 94)'}}
                         /> : <ICON_HEART/>} </div>
                    </div>
                    <div onClick={()=>deleteTweet(tweet.getSqueakHash())} className="tweet-int-icon">
                        <div className="card-icon delete-icon">
                            <ICON_DELETE styles={{fill:'rgb(101, 119, 134)'}} />
                        </div>
                    </div>
                </div>
            </div>

            {replyTweets.map(r=>{
                // TODO: use replies instead of empty array.
                return <TweetCard tweet={r} retweet={r.getReplyTo()} username={r.getAuthorPubkey()} name={r.getAuthorPubkey()} parent={null} key={r.getSqueakHash()} id={r.getSqueakHash()} user={r.getAuthor()} createdAt={r.getBlockTime()} description={r.getContentStr()}
                    images={[]} replies={[]} retweets={[]} likes={[]} />
            })}

        </div>:<div className="tweet-wrapper"><Loader /></div>}

        {tweet && account ?
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
                  <MakeSqueak replyToTweet={tweet} />
                </div>
            </div> : null}
        </div>:null}
        </>
    )
}

export default withRouter(TweetPage)
