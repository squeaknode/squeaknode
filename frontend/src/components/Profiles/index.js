import React, { useEffect, useState, useContext } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import TweetCard from '../TweetCard'


const Profiles = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { account, signingProfiles, contactProfiles, result, tagTweets} = state
    const [tab, setTab] = useState('Signing Profiles')


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


    return(
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
    )
}

export default withRouter(Profiles)
