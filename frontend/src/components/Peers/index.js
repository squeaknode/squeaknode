import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE, ICON_LAPTOPFILL } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import TweetCard from '../TweetCard'


const Peers = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { account, signingProfiles, connectedPeers, result, tagTweets} = state
    const [tab, setTab] = useState('Connected Peers')
    const [signingProfileModalOpen, setSigningProfileModalOpen] = useState(false)
    const [contactProfileModalOpen, setContactProfileModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [host, setHost] = useState('')
    const [port, setPort] = useState('')
    const [useTor, setUseTor] = useState(false)

    const searchOnChange = (param) => {
        if(tab !== 'Search'){setTab('Search')}
        if(param.length>0){
            actions.search({description: param})
        }
    }

    useEffect(() => {
        window.scrollTo(0, 0)
        // actions.getSigningProfiles()
        // actions.getContactProfiles()
        actions.getConnectedPeers()
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

    const goToPeer = (peerAddress) => {
        // TODO
        // props.history.push(`/profile/${id}`)
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
        // actions.createSigningProfile({profileName: newProfileName});
        toggleSigningProfileModal();
    }

    const connectPeer = () => {
        // TODO: get network from `useTor`
        const network = 'IPV4';
        actions.connectPeer({host: host, port: port, network: network});
        toggleContactProfileModal();
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
              <div onClick={(e)=>toggleContactProfileModal('edit')}
               className='profiles-create-button'>
                  <span>Connect Peer</span>
              </div>
            }
            {account &&
              <div onClick={(e)=>toggleSigningProfileModal('edit')}
               className='profiles-create-button'>
                  <span>Add Saved Peer</span>
              </div>
            }
            </div>
            </div>
            <div>
                <div className="explore-nav-menu">
                    <div onClick={()=>setTab('Connected Peers')} className={tab === 'Connected Peers' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Connected Peers
                    </div>
                    <div onClick={()=>setTab('Signing Profiles')} className={tab === 'Signing Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Saved Peers
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
                tab === 'Connected Peers' ?
                connectedPeers.map(p=>{
                  const peerAddress = p.getPeerAddress();
                  const host = peerAddress.getHost();
                  const port = peerAddress.getPort();
                  const addrStr = host + '@' + port;
                  const savedPeer = p.getSavedPeer();
                  const savedPeerName = savedPeer && savedPeer.getPeerName();
                  return <div onClick={()=>goToPeer(666)} key={addrStr} className="search-result-wapper">
                    <ICON_LAPTOPFILL styles={{fill:"rgb(0,128,0)", width:'48px', height:"48px"}} />
                    <div className="search-user-details">
                    <div className="search-user-warp">
                    <div className="search-user-info">
                    <div className="search-user-name">{savedPeerName}</div>
                    <div className="search-user-username">{addrStr}</div>
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
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        {/* Modal for connect peer */}
        <div onClick={()=>toggleContactProfileModal()} style={{display: contactProfileModalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleContactProfileModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Connect Peer</p>

                    <div className="save-modal-wrapper">
                        <div onClick={connectPeer} className="save-modal-btn">
                            Submit
                        </div>
                    </div>
                </div>

                <div className="modal-body">
                    <form className="edit-form">
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Host</label>
                                <input onChange={(e)=>setHost(e.target.value)} type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Port</label>
                                <input onChange={(e)=>setPort(e.target.value)} type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>


        </div>
    )
}

export default withRouter(Peers)
