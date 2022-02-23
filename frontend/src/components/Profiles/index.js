import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'


const Profiles = (props) => {
    console.log(props);
    const { state, actions } = useContext(StoreContext)
    const { signingProfiles, contactProfiles, result, tagSqueaks} = state
    const [tab, setTab] = useState('Signing Profiles')
    const [signingProfileModalOpen, setSigningProfileModalOpen] = useState(false)
    const [contactProfileModalOpen, setContactProfileModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [newProfileName, setNewProfileName] = useState('')
    const [newProfilePubkey, setNewProfilePubkey] = useState('')
    const [usePrivKey, setUsePrivKey] = useState(false)
    const [newProfilePrivkey, setNewProfilePrivkey] = useState('')


    const searchOnChange = (param) => {
        if(tab !== 'Search'){setTab('Search')}
        if(param.length>0){
            actions.search({description: param})
        }
    }

    useEffect(() => {
        window.scrollTo(0, 0)
        actions.getSigningProfiles()
        actions.getContactProfiles()
        // if(props.history.location.search.length>0){
        //     goToTrend(props.history.location.search.substring(1))

        // }
    }, [])

    const followUser = (e, id) => {
        e.stopPropagation()
        actions.followUser(id)
    }

    const unfollowUser = (e,id) => {
        e.stopPropagation()
        actions.unfollowUser(id)
    }

    const goToUser = (id) => {
        props.history.push(`/app/profile/${id}`)
    }

    const toggleSigningProfileModal = (param, type) => {
        setStyleBody(!styleBody)
        // if(param === 'edit'){setSaved(false)}
        // if(type){setTab(type)}
        // if(param === 'members'){
        //     setMemOpen(true)
        //     actions.getFollowers(props.match.params.username)
        // }
        // if(memOpen){setMemOpen(false)}
        setTimeout(()=>{ setSigningProfileModalOpen(!signingProfileModalOpen) },20)
    }

    const toggleContactProfileModal = (param, type) => {
        setStyleBody(!styleBody)
        // if(param === 'edit'){setSaved(false)}
        // if(type){setTab(type)}
        // if(param === 'members'){
        //     setMemOpen(true)
        //     actions.getFollowers(props.match.params.username)
        // }
        // if(memOpen){setMemOpen(false)}
        setTimeout(()=>{ setContactProfileModalOpen(!contactProfileModalOpen) },20)
    }

    const createSigningProfile = () => {
        if (usePrivKey) {
          actions.importSigningProfile({profileName: newProfileName, privateKey: newProfilePrivkey});
        } else {
          actions.createSigningProfile({profileName: newProfileName});
        }
        toggleSigningProfileModal();
    }

    const createContactProfile = () => {
        actions.createContactProfile({profileName: newProfileName, pubkey: newProfilePubkey});
        toggleContactProfileModal();
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const handleChangeUsePrivKey = () => {
      setUsePrivKey(!usePrivKey);
    };


    return(
        <div>

        <div className="explore-wrapper">
            <div className="explore-header">
                <div className="explore-search-wrapper">
                    <div className="explore-search-icon">
                        <ICON_SEARCH/>
                    </div>
                    <div className="explore-search-input">
                        <input onChange={(e)=>searchOnChange(e.target.value)} placeholder="Search for people" type="text" name="search"/>
                    </div>
                </div>
            </div>
            <div className="profile-details-wrapper">
            <div className="profiles-options">
            <div onClick={(e)=>toggleSigningProfileModal('edit')}
               className='profiles-create-button'>
                  <span>Add Signing Profile</span>
            </div>
            <div onClick={(e)=>toggleContactProfileModal('edit')}
               className='profiles-create-button'>
                  <span>Add Contact Profile</span>
            </div>
            </div>
            </div>
            <div>
                <div className="explore-nav-menu">
                    <div onClick={()=>setTab('Signing Profiles')} className={tab === 'Signing Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Signing Profiles
                    </div>
                    <div onClick={()=>setTab('Contact Profiles')} className={tab === 'Contact Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Contact Profiles
                    </div>
                </div>
                {tab === 'Signing Profiles' ?
                signingProfiles.map(f=>{
                  return <div onClick={()=>goToUser(f.getPubkey())} key={f.getPubkey()} className="search-result-wapper">
                    <Link to={`/app/profile/${f.getPubkey()}`} className="search-userPic-wrapper">
                      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(f)}`}/>
                    </Link>
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{f.getProfileName()}</div>
                    <div className="search-user-username">@{f.getPubkey()}</div>
                    </div>
                    <div onClick={(e)=>{
                        f.getFollowing() ?
                        unfollowUser(e,f.getProfileId()) :
                        followUser(e,f.getProfileId())
                      }} className={f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
                        <span><span>{f.getFollowing() ? 'Following' : 'Follow'}</span></span>
                    </div>
                    </div>
                    <div className="search-user-bio">
                      &nbsp;
                    </div>
                  </div>
                </div>
                })
                :
                tab === 'Contact Profiles' ?
                contactProfiles.map(f=>{
                  return <div onClick={()=>goToUser(f.getPubkey())} key={f.getPubkey()} className="search-result-wapper">
                    <Link to={`/app/profile/${f.getPubkey()}`} className="search-userPic-wrapper">
                      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(f)}`}/>
                    </Link>
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{f.getProfileName()}</div>
                    <div className="search-user-username">@{f.getPubkey()}</div>
                    </div>
                    <div onClick={(e)=>{
                        f.getFollowing() ?
                        unfollowUser(e,f.getProfileId()) :
                        followUser(e,f.getProfileId())
                      }} className={f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
                        <span><span>{f.getFollowing() ? 'Following' : 'Follow'}</span></span>
                    </div>
                    </div>
                    <div className="search-user-bio">
                      &nbsp;
                    </div>
                  </div>
                </div>
                })
                : <div className="try-searching">
                        Nothing to see here ..
                        <div/>
                    Try searching for people, usernames, or keywords

                </div>
                }
            </div>
        </div>


        {/* Modal for create signing profile */}
        <div onClick={()=>toggleSigningProfileModal()} style={{display: signingProfileModalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleSigningProfileModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Add Signing Profile</p>

                    <div className="save-modal-wrapper">
                        <div onClick={createSigningProfile} className="save-modal-btn">
                            Submit
                        </div>
                    </div>
                </div>

                <div className="modal-body">
                    <form className="edit-form">
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Profile Name</label>
                                <input onChange={(e)=>setNewProfileName(e.target.value)} type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                            <label>
                            <input
                            type="checkbox"
                            checked={usePrivKey}
                            onChange={handleChangeUsePrivKey}
                            />
                              Import Existing Private Key
                            </label>
                            </div>
                        </div>
                        {usePrivKey &&
                          <div className="edit-input-wrap">
                              <div className="edit-input-content">
                                  <label>Private Key</label>
                                  <input onChange={(e)=>setNewProfilePrivkey(e.target.value)} type="text" name="name" className="edit-input"/>
                              </div>
                          </div>
                        }
                    </form>
                </div>
            </div>
        </div>

        {/* Modal for create contact profile */}
        <div onClick={()=>toggleContactProfileModal()} style={{display: contactProfileModalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleContactProfileModal()} className="modal-closeIcon-wrap">
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
                                <input onChange={(e)=>setNewProfileName(e.target.value)} type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Public Key</label>
                                <input onChange={(e)=>setNewProfilePubkey(e.target.value)} type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>


        </div>
    )
}

export default withRouter(Profiles)
