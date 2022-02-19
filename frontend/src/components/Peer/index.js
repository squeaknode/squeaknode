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
    console.log("props.match.params");
    console.log(props.match.params);
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


const handleModalClick = (e) => {
    e.stopPropagation()
}

const uploadImage = (file) => {
    let bodyFormData = new FormData()
    bodyFormData.append('image', file)
    axios.post(`${API_URL}/tweet/upload`, bodyFormData, { headers: { Authorization: `Bearer ${localStorage.getItem('Twittertoken')}`}})
        .then(res=>{
            setBanner(res.data.imageUrl)
            setBannerLoading(false)
        })
        .catch(err=>alert('error uploading image'))
}

const changeBanner = () => {
    setBannerLoading(true)
    let file = document.getElementById('banner').files[0];
    uploadImage(file)
}

const deleteList = () => {
    actions.deleteList(props.match.params.id)
    props.history.push('/lists')
}

const goToUser = (id) => {
    props.history.push(`/profile/${id}`)
}

const searchOnChange = (param) => {
    if(param.length>0){
        actions.searchUsers({username: param})
    }
}

const addToList = (e,username,userId, profileImg,name) => {
    e.stopPropagation()
    let values = {id: props.match.params.id, username, userId, profileImg,name}
    actions.addToList(values)
}

console.log(peer);
console.log(peerConnection);

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
                    @{peer.getPeerAddress().getHost()}
                </div>
            </div>
        </div>
        <div className="listp-details-wrap">
            <div className="bookmarks-header-name">{saved && false ? editName : peer.getPeerName()}</div>
            {''.length> 0 || saved ? <div className="list-description">{saved && false ? editDescription : '' }</div> : null }
            <div className="list-owner-wrap">
                <h4>{peer.getPeerName()}</h4>
                <div>@{peer.getPeerAddress().getHost()}</div>
            </div>
            <div onClick={()=>console.log('members')} className="list-owner-wrap Members">
                    <h4>{[]}</h4>
                    <div>Members</div>
             </div>
             <div onClick={()=>console.log('edit')} className="listp-edit-btn">
                    Edit List
             </div>
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
