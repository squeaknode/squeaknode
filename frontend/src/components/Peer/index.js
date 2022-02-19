import React , { useEffect, useState, useContext, useRef } from 'react'
import './style.scss'
import {  withRouter, Link } from 'react-router-dom'
import { StoreContext } from '../../store/store'
import Loader from '../Loader'
import TweetCard from '../TweetCard'
import {API_URL} from '../../config'
import axios from 'axios'
import {ICON_ARROWBACK, ICON_UPLOAD, ICON_CLOSE,ICON_SEARCH } from '../../Icons'

const Peer = (props) => {

const { state, actions } = useContext(StoreContext)
const [modalOpen, setModalOpen] = useState(false)

const [editName, setName] = useState('')
const [editDescription, setDescription] = useState('')
const [banner, setBanner] = useState('')
const [saved, setSaved] = useState(false)
const [tab, setTab] = useState('Members')
const [bannerLoading, setBannerLoading] = useState(false)
const [styleBody, setStyleBody] = useState(false)
const {account, peer, peerConnection, list, listTweets, resultUsers} = state

useEffect(() => {
    window.scrollTo(0, 0)
    // actions.getList(props.match.params.id)
    actions.getPeer({
      network: props.match.params.network,
      host: props.match.params.host,
      port: props.match.params.port,
    });
    actions.getPeerConnection({
      network: props.match.params.network,
      host: props.match.params.host,
      port: props.match.params.port,
    });
}, [])

const isInitialMount = useRef(true);
useEffect(() => {
    if (isInitialMount.current){ isInitialMount.current = false }
    else {
        document.getElementsByTagName("body")[0].style.cssText = styleBody && "overflow-y: hidden; margin-right: 17px"
    }
}, [styleBody])

useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )


const deleteList = () => {
    actions.deleteList(props.match.params.id)
    props.history.push('/lists')
}

const goToUser = (id) => {
    props.history.push(`/profile/${id}`)
}

const connectPeer = (e) => {
    actions.connectPeer({
      host: props.match.params.host,
      port: props.match.params.port,
      network: props.match.params.network});
}

const disconnectPeer = (e) => {
  actions.disconnectPeer({
    host: props.match.params.host,
    port: props.match.params.port,
    network: props.match.params.network});
}


return(
    <div>
        {peer ?
    <div>
      <div className="bookmarks-wrapper">
        <div className="bookmarks-header-wrapper">
            <div className="profile-header-back">
                <div onClick={()=>window.history.back()} className="header-back-wrapper">
                    <ICON_ARROWBACK/>
                </div>
            </div>
            <div className="bookmarks-header-content">
                <div className="bookmarks-header-name">
                    {peer.getPeerName()}
                </div>
                <div className="bookmarks-header-tweets">
                    {peer.getPeerAddress().getHost()}:{peer.getPeerAddress().getPort()}
                </div>
            </div>
        </div>
        <div className="listp-details-wrap">
            <div className="bookmarks-header-name">{saved && false ? editName : peer.getPeerName()}</div>
            {''.length> 0 || saved ? <div className="list-description">{saved && false ? editDescription : '' }</div> : null }
            <div className="list-owner-wrap">
                <div>{peer.getPeerAddress().getHost()}:{peer.getPeerAddress().getPort()}</div>
            </div>
            {account &&
              <div onClick={(e)=>
                 peerConnection ?
                 disconnectPeer(e) :
                 connectPeer(e)
              }
                className={peerConnection ? 'disconnect peer-connect-button' : 'peer-connect-button'}>
                   <span><span>{ account && peerConnection ? 'Connected' : 'Connect'}</span></span>
              </div>
            }
        </div>
        {listTweets && listTweets.map(t=>{
            return <TweetCard retweet={t.retweet} username={t.username} name={t.name} parent={t.parent} key={t._id} id={t._id} user={t.user} createdAt={t.createdAt} description={t.description} images={t.images} replies={t.replies} retweets={t.retweets} likes={t.likes}  />
        })}
    </div>

    </div> : <div className="bookmarks-wrapper"><Loader/> </div> }
    </div>
    )
}

export default withRouter(Peer)
