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
    const { account, signingProfiles, contactProfiles, trends, result, tagTweets} = state
    const [tab, setTab] = useState('Signing Profiles')
    const [trendOpen, setTrendOpen] = useState(false)


    const searchOnChange = (param) => {
        if(tab !== 'Search'){setTab('Search')}
        if(param.length>0){
            actions.search({description: param})
        }
    }

    useEffect(() => {
        window.scrollTo(0, 0)
        actions.getTrend()
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

    const goToUser = (id) => {
        props.history.push(`/profile/${id}`)
    }

    const goToTrend = (hash) => {
        setTrendOpen(true)
        let hashtag = hash.substring(1)
        actions.getTrendTweets(hashtag)
    }


    return(
        <div className="explore-wrapper">
            <div className={trendOpen ? "explore-header header-border" : "explore-header"}>
                {trendOpen &&
                <div className="explore-header-back">
                    <div onClick={()=>setTrendOpen(false)} className="explore-back-wrapper">
                        <ICON_ARROWBACK/>
                    </div>
                </div>}
                <div className="explore-search-wrapper">
                    <div className="explore-search-icon">
                        <ICON_SEARCH/>
                    </div>
                    <div className="explore-search-input">
                        <input onChange={(e)=>searchOnChange(e.target.value)} placeholder="Search for hashtags or people" type="text" name="search"/>
                    </div>
                </div>
            </div>
            {!trendOpen ?
            <div>
                <div className="explore-nav-menu">
                    <div onClick={()=>setTab('Signing Profiles')} className={tab === 'Signing Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Signing Profiles
                    </div>
                    <div onClick={()=>setTab('Contact Profiles')} className={tab === 'Contact Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Contact Profiles
                    </div>
                    <div onClick={()=>setTab('Trends')} className={tab === 'Trends' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Trending
                    </div>
                    <div onClick={()=>setTab('Search')} className={tab === 'Search' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Search
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
                      <div onClick={(e)=>followUser(e,f._id)} className={account && f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
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
                      <div onClick={(e)=>followUser(e,f._id)} className={account && f.getFollowing() ? "follow-btn-wrap unfollow-switch":"follow-btn-wrap"}>
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
                tab === 'Trends' ?
                    trends.length>0 ?
                    trends.map((t,i)=>{
                    return  <div onClick={()=>goToTrend(t.content)} key={t._id} className="trending-card-wrapper">
                                <div className="trending-card-header">{i+1} <span>·</span> Trending</div>
                                <div className="trending-card-content"> {t.content} </div>
                                <div className="trending-card-count"> {t.count} Tweets </div>
                            </div>
                    }) : <Loader/>
                :
                result.length ? result.map(r=>{
                    return <TweetCard retweet={r.retweet} username={r.username} name={r.name} parent={r.parent} key={r._id} id={r._id} user={r.user} createdAt={r.createdAt} description={r.description} images={r.images} replies={r.replies} retweets={r.retweets} likes={r.likes} />
                }) : <div className="try-searching">
                        Nothing to see here ..
                        <div/>
                    Try searching for people, usernames, or keywords

                </div>
                }
            </div> : <div>
            {tagTweets.length>0 && tagTweets.map(t=>{
            return <TweetCard retweet={t.retweet} username={t.username} name={t.name} parent={t.parent} key={t._id} id={t._id} user={t.user} createdAt={t.createdAt} description={t.description} images={t.images} replies={t.replies} retweets={t.retweets} likes={t.likes}  />
                })}
            </div>}
        </div>
    )
}

export default withRouter(Profiles)
