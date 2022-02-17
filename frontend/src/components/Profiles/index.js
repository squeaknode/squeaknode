import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import TweetCard from '../TweetCard'


const Profiles = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { account, signingProfiles, contactProfiles, result, tagTweets} = state
    const [tab, setTab] = useState('Signing Profiles')
    const [modalOpen, setModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [newProfileName, setNewProfileName] = useState('')

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
        props.history.push(`/profile/${id}`)
    }

    const toggleModal = (param, type) => {
        setStyleBody(!styleBody)
        // if(param === 'edit'){setSaved(false)}
        // if(type){setTab(type)}
        // if(param === 'members'){
        //     setMemOpen(true)
        //     actions.getFollowers(props.match.params.username)
        // }
        // if(memOpen){setMemOpen(false)}
        setTimeout(()=>{ setModalOpen(!modalOpen) },20)
    }

    const createSigningProfile = () => {
        console.log(newProfileName);
        actions.createSigningProfile({profileName: newProfileName});
    }

    const handleModalClick = (e) => {
        e.stopPropagation()
    }


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
            {account &&
              <div onClick={(e)=>toggleModal('edit')}
               className='profiles-create-button'>
                  <span>Add Signing Profile</span>
              </div>
            }
            {account &&
              <div onClick={(e)=>toggleModal('edit')}
               className='profiles-create-button'>
                  <span>Add Contact Profile</span>
              </div>
            }
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
                    <Link to={`/profile/${f.getPubkey()}`} className="search-userPic-wrapper">
                      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(f)}`}/>
                    </Link>
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{f.getProfileName()}</div>
                    <div className="search-user-username">@{f.getPubkey()}</div>
                    </div>
                    {f._id === account && account._id ? null :
                      <div onClick={(e)=>{
                        f.getFollowing() ?
                        unfollowUser(e,f.getProfileId()) :
                        followUser(e,f.getProfileId())
                      }} className={account && f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
                        <span><span>{account && f.getFollowing() ? 'Following' : 'Follow'}</span></span>
                      </div>}
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
                    <Link to={`/profile/${f.getPubkey()}`} className="search-userPic-wrapper">
                      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(f)}`}/>
                    </Link>
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{f.getProfileName()}</div>
                    <div className="search-user-username">@{f.getPubkey()}</div>
                    </div>
                    {f._id === account && account._id ? null :
                      <div onClick={(e)=>{
                        f.getFollowing() ?
                        unfollowUser(e,f.getProfileId()) :
                        followUser(e,f.getProfileId())
                      }} className={account && f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
                        <span><span>{account && f.getFollowing() ? 'Following' : 'Follow'}</span></span>
                      </div>}
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


        <div onClick={()=>toggleModal()} style={{display: modalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleModal()} className="modal-closeIcon-wrap">
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
                    </form>
                </div>
            </div>
        </div>



        </div>
    )
}

export default withRouter(Profiles)
