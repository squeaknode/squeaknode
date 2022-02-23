import React, { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import axios from 'axios'
import moment from 'moment'
import ContentEditable from 'react-contenteditable'
import { ICON_IMGUPLOAD } from '../../Icons'
import { Link } from 'react-router-dom'
import { API_URL } from '../../config'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import Select from 'react-select'

const MakeSqueak = (props) => {
    const { state, actions } = useContext(StoreContext)
    const { signingProfiles, session } = state
    useEffect(() => {
        actions.getSigningProfiles()
    }, [])

    //used for contenteditable divs on react hooks
    const squeakT = useRef('');
    const handleChange = (evt, e) => {
        if (squeakT.current.trim().length <= 280
            && squeakT.current.split(/\r\n|\r|\n/).length <= 30) {
            squeakT.current = evt.target.value;
            setTweetText(squeakT.current)
        }
        // document.getElementById('squeak-box').innerHTML = document.getElementById('squeak-box').innerHTML.replace(/(\#\w+)/g, '<span class="blue">$1</span>')
    };
    const [signingProfile, setSigningProfile] = useState(null)
    const [squeakText, setTweetText] = useState("")

    const optionsFromProfiles = (profiles) => {
      return profiles.map((p) => {
          return { value: p, label: p.getProfileName() }
          // return { value: 'chocolate', label: 'Chocolate' }
        });
    }

    const handleChangeSigningProfile = (e) => {
      setSigningProfile(e.value);
    }

    const submitTweet = () => {
        // TODO: toggle modal off here.

        if (!signingProfile) {
          alert('Signing profile must be set.');
          return;
        }

        if (!squeakText.length) { return }

        let hashtags = squeakText.match(/#(\w+)/g)

        const values = {
            signingProfile: signingProfile.getProfileId(),
            description: squeakText,
            replyTo: props.replyToTweet ? props.replyToTweet.getSqueakHash() : null,
            hasRecipient: null,
            recipientProfileId: -1
        }
        actions.squeak(values)
        squeakT.current = ''
        setTweetText('')
        if (props.submittedCallback) {
          props.submittedCallback();
        }
    }

    const author = props.replyToTweet && props.replyToTweet.getAuthor();

    return (
      <>

      {/* Squeak being replied to. */}
      {props.replyToTweet ?
      <div className="reply-content-wrapper">
          <div className="card-userPic-wrapper">
              <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.replyToTweet.getAuthorPubkey()}`}>
                  <img alt="" style={{borderRadius:'50%', minWidth:'49px'}} width="100%" height="49px" src={author ? `${getProfileImageSrcString(props.replyToTweet.getAuthor())}`: null}/>
              </Link>
          </div>
          <div className="card-content-wrapper">
              <div className="card-content-header">
                  <div className="card-header-detail">
                      <span className="card-header-user">
                          <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.replyToTweet.getAuthorPubkey()}`}>{author ? author.getProfileName(): 'Unknown Author'}</Link>
                      </span>
                      <span className="card-header-username">
                          <Link onClick={(e)=>e.stopPropagation()} to={`/app/profile/${props.replyToTweet.getAuthorPubkey()}`}>{'@'+props.replyToTweet.getAuthorPubkey()}</Link>
                      </span>
                      <span className="card-header-dot">·</span>
                      <span className="card-header-date">
                                  {moment(props.replyToTweet.getBlockTime() * 1000).fromNow()}
                      </span>
                  </div>
              </div>
              <div className="card-content-info">
              {props.replyToTweet.getContentStr()}
              </div>
              <div className="reply-to-user">
                  <span className="reply-squeak-username">
                      Replying to
                  </span>
                  <span className="main-squeak-user">
                      @{props.replyToTweet.getAuthorPubkey()}
                  </span>
              </div>
          </div>
      </div> : null }


            {/* New squeak content input. */}
            <div className="Tweet-input-wrapper">
                <div className="Tweet-profile-wrapper">
                    <Link to={`/app/profile/${signingProfile && signingProfile.getPubkey()}`}>
                        {signingProfile && <img alt="" style={{ borderRadius: '50%', minWidth: '49px' }} width="100%" height="49px" src={`${getProfileImageSrcString(signingProfile)}`} />}
                    </Link>
                </div>
                <div className="Tweet-input-side">
                    <div className="inner-input-box">
                        <Select options={optionsFromProfiles(signingProfiles)} onChange={handleChangeSigningProfile} />
                    </div>
                    <div className="inner-input-box">
                        <ContentEditable onPaste={(e) => e.preventDefault()} id="squeak-box" className={squeakText.length ? 'squeak-input-active' : null} onKeyDown={(e)=>squeakT.current.length>279 ? e.keyCode !== 8 && e.preventDefault(): null} placeholder="What's happening?" html={squeakT.current} onChange={(e) => handleChange(e)} />
                    </div>
                    <div className="inner-input-links">
                        <div className="input-links-side">
                        </div>
                        <div className="squeak-btn-holder">
                            <div style={{ fontSize: '13px', color: squeakText.length >= 280 ? 'red' : null }}>
                                {squeakText.length > 0 && squeakText.length + '/280'}
                            </div>
                            <div onClick={submitTweet} className={squeakText.length ? 'squeak-btn-side squeak-btn-active' : 'squeak-btn-side'}>
                                Squeak
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            </>
    )
}

export default MakeSqueak
