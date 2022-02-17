import React , { useEffect, useState, useContext, useRef} from 'react'
import './style.scss'
import { ICON_ARROWBACK, ICON_MARKDOWN, ICON_DATE, ICON_CLOSE, ICON_UPLOAD, ICON_NEWMSG } from '../../Icons'
import { withRouter, Link } from 'react-router-dom'
import { StoreContext } from '../../store/store'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import moment from 'moment'
import TweetCard from '../TweetCard'
import {API_URL} from '../../config'


const Profile = (props) => {
    const { state, actions } = useContext(StoreContext)
    const [activeTab, setActiveTab] = useState('Tweets')
    const [editName, setName] = useState('')
    const [modalOpen, setModalOpen] = useState(false)
    const [saved, setSaved] = useState(false)
    const [memOpen, setMemOpen] = useState(false)
    const [tab, setTab] = useState('Sats Spent')
    const [styleBody, setStyleBody] = useState(false)
    const {account, user, userTweets, session} = state
    const userParam = props.match.params.username

    useEffect(() => {
        window.scrollTo(0, 0)
        actions.getUser(props.match.params.username)
        reloadTweets();
        //preventing edit modal from apprearing after clicking a user on memOpen
        setMemOpen(false)
        setModalOpen(false)
        setName('')
    }, [props.match.params.username])

    const isInitialMount = useRef(true);
    useEffect(() => {
        if (isInitialMount.current){ isInitialMount.current = false }
        else {
            document.getElementsByTagName("body")[0].style.cssText = styleBody && "overflow-y: hidden; margin-right: 17px"
        }
      }, [styleBody])

      useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )

      const changeTab = (tab) => {
        setActiveTab(tab)
    }

    const editProfile = () => {
        let values = {
            profileId: user.getProfileId(),
            name: editName,
        }
        actions.updateUser(values)
        setSaved(true)
        toggleModal()
    }

    const toggleModal = (param, type) => {
        setStyleBody(!styleBody)
        if(param === 'edit'){setSaved(false)}
        if(type){setTab(type)}
        if(param === 'members'){
            setMemOpen(true)
            actions.getFollowers(props.match.params.username)
        }
        if(memOpen){setMemOpen(false)}
        setTimeout(()=>{ setModalOpen(!modalOpen) },20)
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const followUser = (e,id) => {
        if(!session){ actions.alert('Please Sign In'); return }
        e.stopPropagation()
        actions.followUser(id)
    }

    const unfollowUser = (e,id) => {
        e.stopPropagation()
        actions.unfollowUser(id)
    }

    const changeAvatar = () => {
        let file = document.getElementById('avatar').files[0];
        uploadAvatar(file);
    }

    const uploadAvatar = (file) => {
      if (file == null)
        return;
      const reader = new FileReader();
      reader.addEventListener('load', () => {
        // convert image file to base64 string
        // preview.src = reader.result;
        const imageBase64Stripped = reader.result.split(',')[1];
        uploadAvatarAsBase64(imageBase64Stripped);
      }, false);
      if (file) {
        reader.readAsDataURL(file);
      }
    };

    const uploadAvatarAsBase64 = (imageBase64) => {
      let values = {
          profileId: user.getProfileId(),
          profileImg: imageBase64,
      }
      actions.updateUserImage(values)
      setSaved(true)
      toggleModal()
    };

    const goToUser = (id) => {
        setModalOpen(false)
        props.history.push(`/profile/${id}`)
    }

    const startChat = () => {
        if(!session){ actions.alert('Please Sign In'); return }
        actions.startChat({id:user.getPubkey(), func: goToMsg})
    }

    const goToMsg = () => {
        props.history.push(`/messages`)
    }

    const getLastSqueak = (squeakLst) => {
      if (squeakLst == null) {
        return null;
      } if (squeakLst.length === 0) {
        return null;
      }
      return squeakLst.slice(-1)[0];
    };

    const getMoreTweets = () => {
        let lastTweet = getLastSqueak(userTweets);
        actions.getUserTweets({username: props.match.params.username, lastUserTweet: lastTweet})
    }

    const reloadTweets = () => {
        actions.clearUserTweets();
        actions.getUserTweets({username: props.match.params.username, lastTweet: null});
    }

    return(
        <div>
            {user ?
            <div>
            <div className="profile-wrapper">
            <div className="profile-header-wrapper">
                <div className="profile-header-back">
                    <div onClick={()=>window.history.back()} className="header-back-wrapper">
                        <ICON_ARROWBACK/>
                    </div>
                </div>
                <div className="profile-header-content">
                    <div className="profile-header-name">
                            {user.getPubkey()}
                    </div>
                    {/* <div className="profile-header-tweets">
                            82 Tweets
                    </div> */}
                </div>
            </div>
            <div className="profile-banner-wrapper">
                <img alt=""/>
            </div>
            <div className="profile-details-wrapper">
                <div className="profile-options">
                    <div className="profile-image-wrapper">
                        <img src={`${getProfileImageSrcString(user)}`} alt=""/>
                    </div>
                    {account &&
                      <div onClick={(e)=>toggleModal('edit')}
                       className='profile-edit-button'>
                          <span>Edit profile</span>
                      </div>
                    }
                    {account &&
                      <div onClick={(e)=>
                        user.getFollowing() ?
                        unfollowUser(e,user.getProfileId()) :
                        followUser(e,user.getProfileId())
                      }
                       className={user.getFollowing() ? 'unfollow-switch profile-edit-button' : 'profile-edit-button'}>
                          <span><span>{ account && user.getFollowing() ? 'Following' : 'Follow'}</span></span>
                      </div>
                    }
                </div>
                <div className="profile-details-box">
                    <div className="profile-name">{user.getProfileName()}</div>
                    <div className="profile-username">@{user.getPubkey()}</div>
                    <div className="profile-bio">
                        {user.description}
                    </div>
                    <div className="profile-info-box">
                        <ICON_DATE/>
                        <div className="profile-date"> Joined {moment(user.createdAt).format("MMMM YYYY")} </div>
                    </div>
                </div>
                <div className="profile-social-box">
                        {/* TODO: Implement sats spent */}
                        <div onClick={()=>toggleModal('members','Sats Earned')}>
                            <p className="follow-num"> 0 </p>
                            <p className="follow-text"> sats spent </p>
                        </div>
                        {/* TODO: Implement sats eaned */}
                        <div onClick={()=>toggleModal('members', 'Sats Spent')}>
                            <p className="follow-num"> 0 </p>
                            <p className="follow-text"> sats earned </p>
                        </div>
                </div>
            </div>
            <div className="profile-nav-menu">
                <div key={'tweets'} onClick={()=>changeTab('Tweets')} className={activeTab ==='Tweets' ? `profile-nav-item activeTab` : `profile-nav-item`}>
                    Tweets
                </div>
                <div key={'replies'} onClick={()=>changeTab('Tweets&Replies')} className={activeTab ==='Tweets&Replies' ? `profile-nav-item activeTab` : `profile-nav-item`}>
                    Tweets & replies
                </div>
                <div key={'media'} onClick={()=>changeTab('Media')} className={activeTab ==='Media' ? `profile-nav-item activeTab` : `profile-nav-item`}>
                    Media
                </div>
                <div key={'likes'} onClick={()=>changeTab('Likes')} className={activeTab ==='Likes' ? `profile-nav-item activeTab` : `profile-nav-item`}>
                    Likes
                </div>
            </div>
            {activeTab === 'Tweets' ?
            userTweets.map(t=>{
                if(!t.getReplyTo())
                return <TweetCard tweet={t} retweet={t.getReplyTo()} username={t.getAuthorPubkey()} name={t.getAuthorPubkey()} parent={null} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} createdAt={t.getBlockTime()} description={t.getContentStr()}
                    images={[]} replies={[]} retweets={[]} likes={[]} />
             }) : activeTab === 'Tweets&Replies' ?
            userTweets.map(t=>{
                return <TweetCard tweet={t} retweet={t.getReplyTo()} username={t.getAuthorPubkey()} name={t.getAuthorPubkey()} parent={null} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} createdAt={t.getBlockTime()} description={t.getContentStr()}
                    images={[]} replies={[]} retweets={[]} likes={[]} />
             }) :
            activeTab === 'Likes' ?
            null: activeTab === 'Media' ?
            null: null}
            {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
            {state.loading ?
                <Loader /> :
                <div onClick={() => getMoreTweets()} className='tweet-btn-side tweet-btn-active'>
                  Load more
                </div>}
            </div>
            <div onClick={()=>toggleModal()} style={{display: modalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className={memOpen ? "modal-header no-b-border" : "modal-header"}>
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">{memOpen ? null : 'Edit Profile'}</p>
                        {memOpen ? null :
                        <div className="save-modal-wrapper">
                            <div onClick={editProfile} className="save-modal-btn">
                                Save
                            </div>
                        </div>}
                    </div>
                    {memOpen ? <div className="modal-body">
                    <div className="explore-nav-menu">
                        <div onClick={()=>setTab('Sats Spent')} className={tab =='Sats Spent' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                            Sats Spent
                        </div>
                        <div onClick={()=>setTab('Sats Earned')} className={tab =='Sats Earned' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                            Sats Earned
                        </div>
                    </div>
                    <div className="modal-scroll">
                    </div>
                    </div> :
                    <div className="modal-body">
                        <div className="modal-banner">
                        </div>
                        <div className="modal-profile-pic">
                            <div className="modal-back-pic">
                                <img src={`${getProfileImageSrcString(user)}`} alt="profile" />
                                <div>
                                    <ICON_UPLOAD/>
                                    <input onChange={()=>changeAvatar()} title=" " id="avatar" style={{opacity:'0'}} type="file"/>
                                </div>
                            </div>
                        </div>
                        <form className="edit-form">
                            <div className="edit-input-wrap">
                                <div className="edit-input-content">
                                    <label>Name</label>
                                    <input defaultValue={user.getProfileName()} onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                                </div>
                            </div>
                        </form>
                    </div>}
                </div>
            </div>
            </div>: <div className="profile-wrapper"><Loader/> </div> }
        </div>
    )
}

export default withRouter(Profile)
