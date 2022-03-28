import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { withRouter, Link } from 'react-router-dom'
import moment from 'moment'
import { getProfileImageSrcString } from '../../squeakimages/images';


import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


const TwitterAccountCard = (props) => {
  const twitterAccount = props.twitterAccount;
  const profile = twitterAccount.getProfile();
  const dispatch = useDispatch();

  // const followUser = (e, id) => {
  //     e.stopPropagation()
  //     console.log('Follow clicked');
  //     dispatch(setFollowProfile(id));
  // }
  //
  // const unfollowUser = (e,id) => {
  //     e.stopPropagation()
  //     console.log('Unfollow clicked');
  //     dispatch(setUnfollowProfile(id));
  // }

  return <div onClick={(e)=>e.stopPropagation()} key={profile.getPubkey()} className="search-result-wapper">
    <div className="search-userPic-wrapper">
      <img style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={`${getProfileImageSrcString(profile)}`}/>
    </div>
    <div className="search-user-details">
      <div className="search-user-warp">
        <div className="search-user-info">
          <div className="search-user-name">{profile.getProfileName()}</div>
          <div className="search-user-username">@{profile.getPubkey()}</div>
        </div>
      </div>
      <div className="search-user-username"><b>Twitter Handle</b>: <a href={`https://twitter.com/${twitterAccount.getHandle()}`} style={{color: "blue", fontWeight: 'bold'}}>
        {twitterAccount.getHandle()}
      </a></div>
      <div className="search-user-bio">
        &nbsp;
      </div>
    </div>
  </div>
}

export default withRouter(TwitterAccountCard)
