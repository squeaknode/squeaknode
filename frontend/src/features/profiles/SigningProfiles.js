import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'
import { withRouter, Link } from 'react-router-dom'
import moment from 'moment'
import { getProfileImageSrcString } from '../../squeakimages/images';


import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


import {
  fetchSigningProfiles,
  clearSigningProfiles,
  selectSigningProfiles,
  selectSigningProfilesStatus,
} from './signingProfilesSlice'


const SigningProfiles = (props) => {
  const signingProfiles = useSelector(selectSigningProfiles);
  const signingProfilesStatus = useSelector(selectSigningProfilesStatus);
  const dispatch = useDispatch();

  useEffect(() => {
      window.scrollTo(0, 0)
      // actions.getSqueaks({lastSqueak: null})
      // reloadSqueaks();
      console.log('fetchSigningProfiles');
      dispatch(clearSigningProfiles());
      dispatch(fetchSigningProfiles(null));
  }, [])

  const goToSqueak = (id) => {
      // if(props.replyTo){ actions.getSqueak(id) }
      props.history.push(`/app/squeak/${id}`)
  }

  const goToUser = (id) => {
      props.history.push(`/app/profile/${id}`)
  }

  const followUser = (e, id) => {
      e.stopPropagation()
      // actions.followUser(id)
      console.log('Follow clicked');
  }

  const unfollowUser = (e,id) => {
      e.stopPropagation()
      // actions.unfollowUser(id)
      console.log('Unfollow clicked');
  }


  const renderedListItems = signingProfiles.map(f=>{
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

  return <>
            {renderedListItems}
         </>
}

export default withRouter(SigningProfiles)
