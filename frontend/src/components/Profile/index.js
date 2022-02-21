import React , { useEffect, useState, useContext, useRef} from 'react'
import './style.scss'
import { ICON_ARROWBACK, ICON_MARKDOWN, ICON_DATE, ICON_CLOSE, ICON_UPLOAD, ICON_NEWMSG, ICON_SETTINGS, ICON_DARK } from '../../Icons'
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
    const [moreMenu, setMoreMenu] = useState(false)
    const [editName, setName] = useState('')
    // const [privateKey, setPrivateKey] = useState('')
    const [editModalOpen, setEditModalOpen] = useState(false)
    const [deleteModalOpen, setDeleteModalOpen] = useState(false)
    const [exportModalOpen, setExportModalOpen] = useState(false)
    const [spendingModalOpen, setSpendingModalOpen] = useState(false)
    const [createModalOpen, setCreateModalOpen] = useState(false)
    const [saved, setSaved] = useState(false)
    const [tab, setTab] = useState('Sats Spent')
    const [styleBody, setStyleBody] = useState(false)
    const {account, user, userTweets, privateKey, session} = state
    const userParam = props.match.params.username

    useEffect(() => {
        window.scrollTo(0, 0)
        actions.getUser(props.match.params.username)
        reloadTweets();
        //preventing edit modal from apprearing after clicking a user on memOpen
        setEditModalOpen(false)
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
        toggleEditModal()
    }

    const deleteProfile = () => {
        let values = {
            profileId: user.getProfileId(),
        }
        actions.deleteUser(values);
        toggleDeleteModal();
    }


    const exportPrivateKey = () => {
        let values = {
            profileId: user.getProfileId(),
        }
        actions.exportPrivateKey(values);
        // toggleExportModal();
    }

    const createContactProfile = () => {
        actions.createContactProfile({profileName: editName, pubkey: userParam});
        toggleCreateModal();
    }

    const toggleEditModal = (param, type) => {
        setStyleBody(!styleBody)
        setSaved(false)
        setName(user.getProfileName())
        setTimeout(()=>{ setEditModalOpen(!editModalOpen) },20)
    }

    const toggleDeleteModal = () => {
        setStyleBody(!styleBody)
        setSaved(false)
        setTimeout(()=>{ setDeleteModalOpen(!deleteModalOpen) },20)
    }

    const toggleExportModal = () => {
        setStyleBody(!styleBody)
        setSaved(false)
        setTimeout(()=>{ setExportModalOpen(!exportModalOpen) },20)
    }

    const toggleSpendingModal = (param, type) => {
        setStyleBody(!styleBody)
        if(type){setTab(type)}
        // TODO: fetch spending info
        // actions.getFollowers(props.match.params.username)
        if(type){setTab(type)}
        setTimeout(()=>{ setSpendingModalOpen(!spendingModalOpen) },20)
    }

    const toggleCreateModal = (param, type) => {
        setStyleBody(!styleBody)
        setSaved(false)
        setTimeout(()=>{ setCreateModalOpen(!createModalOpen) },20)
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
      toggleEditModal()
    };

    const goToUser = (id) => {
        setEditModalOpen(false)
        props.history.push(`/profile/${id}`)
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

    const openMore = () => { setMoreMenu(!moreMenu) }

    const handleMenuClick = (e) => { e.stopPropagation() }


    return(
        <div>
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
                            {userParam}
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
                        <img src={user ? `${getProfileImageSrcString(user)}` : null} alt=""/>
                    </div>

                    {user &&
                      <div id="moremenu" onClick={openMore} className="Nav-link">
                          <div className={"Nav-item-hover"}>
                              <ICON_SETTINGS  />
                          </div>
                          <div onClick={()=>openMore()} style={{display: moreMenu ? 'block' : 'none'}} className="more-menu-background">
                          <div className="more-modal-wrapper">
                              {moreMenu ?
                              <div style={{top: `${document.getElementById('moremenu').getBoundingClientRect().top - 40}px`, left: `${document.getElementById('moremenu').getBoundingClientRect().left}px`, height: '160px' }} onClick={(e)=>handleMenuClick(e)} className="more-menu-content">
                                      <div onClick={toggleDeleteModal} className="more-menu-item">
                                          <span>Delete Profile</span>
                                      </div>
                                      <div onClick={toggleEditModal} className="more-menu-item">
                                          <span>Edit Profile</span>
                                      </div>
                                      {user.getHasPrivateKey() &&
                                        <div onClick={toggleExportModal} className="more-menu-item">
                                            <span>Export Private Key</span>
                                        </div>
                                      }
                              </div> : null }
                          </div>
                          </div>
                      </div>
                    }

                    {account && user &&
                      <div onClick={(e)=>
                        user.getFollowing() ?
                        unfollowUser(e,user.getProfileId()) :
                        followUser(e,user.getProfileId())
                      }
                       className={user.getFollowing() ? 'unfollow-switch profile-edit-button' : 'profile-edit-button'}>
                          <span><span>{ account && user.getFollowing() ? 'Following' : 'Follow'}</span></span>
                      </div>
                    }

                    {account && !user &&
                      <div onClick={(e)=>toggleCreateModal('create')}
                       className='profiles-create-button'>
                          <span>Add Contact Profile</span>
                      </div>
                    }
                </div>
                <div className="profile-details-box">
                    <div className="profile-name">{user ? user.getProfileName() : ''}</div>
                    <div className="profile-username">@{userParam}</div>
                    <div className="profile-bio">
                        &nbsp;
                    </div>
                    <div className="profile-info-box">
                        &nbsp;
                    </div>
                </div>
                <div className="profile-social-box">
                        {/* TODO: Implement sats spent */}
                        <div onClick={()=>toggleSpendingModal('members','Sats Spent')}>
                            <p className="follow-num"> 0 </p>
                            <p className="follow-text"> sats spent </p>
                        </div>
                        {/* TODO: Implement sats eaned */}
                        <div onClick={()=>toggleSpendingModal('members', 'Sats Earned')}>
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
                return <TweetCard tweet={t} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} />
             }) : activeTab === 'Tweets&Replies' ?
            userTweets.map(t=>{
                return <TweetCard tweet={t} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} />
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

            {/* Modal for edit profile */}
            <div onClick={()=>toggleEditModal()} style={{display: editModalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className="modal-header">
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleEditModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">'Edit Profile'</p>
                        <div className="save-modal-wrapper">
                            <div onClick={editProfile} className="save-modal-btn">
                                Save
                            </div>
                        </div>
                    </div>
                    <div className="modal-body">
                        <div className="modal-banner">
                        </div>
                        <div className="modal-profile-pic">
                            <div className="modal-back-pic">
                                <img src={user ? `${getProfileImageSrcString(user)}` : null} alt="profile" />
                                <div>
                                    <ICON_UPLOAD/>
                                    <input onChange={()=>changeAvatar()} title=" " id="avatar" style={{opacity:'0'}} type="file"/>
                                </div>
                            </div>
                        </div>
                        {user ?
                          <form className="edit-form">
                              <div className="edit-input-wrap">
                                  <div className="edit-input-content">
                                      <label>Name</label>
                                      <input defaultValue={user.getProfileName()} onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                                  </div>
                              </div>
                          </form> :
                          <form className="create-form">
                              <div className="create-input-wrap">
                                  <div className="create-input-content">
                                      <label>Name</label>
                                      <input defaultValue={''} onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                                  </div>
                              </div>
                          </form>

                        }
                    </div>
                </div>
            </div>


            {/* Modal for delete profile */}
            <div onClick={()=>toggleDeleteModal()} style={{display: deleteModalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className="modal-header">
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleDeleteModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">'Delete Profile'</p>
                        <div className="save-modal-wrapper">
                            <div onClick={deleteProfile} className="save-modal-btn">
                                Delete
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Modal for export profile */}
            <div onClick={()=>toggleExportModal()} style={{display: exportModalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className="modal-header">
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleExportModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">'Export Private Key'</p>
                        <div className="save-modal-wrapper">
                            <div onClick={exportPrivateKey} className="save-modal-btn">
                                Export
                            </div>
                        </div>
                    </div>

                    <div className="modal-body">
                        <form className="edit-form">
                            <div className="edit-input-wrap">
                                <div className="edit-input-content">
                                    <label>Private Key</label>
                                    <input defaultValue={privateKey} readOnly type="text" name="name" className="edit-input"/>
                                </div>
                            </div>
                        </form>
                    </div>

                </div>
            </div>


            {/* Modal for sats spent and earned */}
            <div onClick={()=>toggleSpendingModal()} style={{display: spendingModalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className="modal-header no-b-border">
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleEditModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">{null}</p>
                    </div>
                    <div className="modal-body">
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
                    </div>
                </div>
            </div>

            {/* Modal for create signing profile */}
            <div onClick={()=>toggleCreateModal()} style={{display: createModalOpen ? 'block' : 'none'}} className="modal-edit">
                <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                    <div className="modal-header">
                        <div className="modal-closeIcon">
                            <div onClick={()=>toggleCreateModal()} className="modal-closeIcon-wrap">
                                <ICON_CLOSE />
                            </div>
                        </div>
                        <p className="modal-title">Add Contact Profile</p>

                        <div className="save-modal-wrapper">
                            <div onClick={createContactProfile} className="save-modal-btn">
                                Submit
                            </div>
                        </div>
                    </div>

                    <div className="modal-body">
                        <form className="edit-form">
                            <div className="edit-input-wrap">
                                <div className="edit-input-content">
                                    <label>Profile Name</label>
                                    <input defaultValue={''} onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                                </div>
                            </div>
                            <div className="edit-input-wrap">
                                <div className="edit-input-content">
                                    <label>Public Key</label>
                                    <input defaultValue={userParam} readOnly type="text" name="name" className="edit-input"/>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>


            </div>
        </div>
    )
}

export default withRouter(Profile)
