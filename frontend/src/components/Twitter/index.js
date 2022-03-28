import React, { useEffect, useState, useContext } from 'react'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import Select from 'react-select'


import { unwrapResult } from '@reduxjs/toolkit'
import { useDispatch } from 'react-redux'
import { useSelector } from 'react-redux'

import TwitterAccounts from '../../features/twitterAccounts/TwitterAccounts'
import {
  setCreateSigningProfile,
} from '../../features/profiles/profilesSlice'

import {
  setCreateTwitterAccount,
} from '../../features/twitterAccounts/twitterAccountsSlice'

import {
  selectSigningProfiles,
  fetchSigningProfiles,
} from '../../features/profiles/profilesSlice'


const Twitter = (props) => {
  const [tab, setTab] = useState('Signing Profiles')
  const [twitterAccountModalOpen, setTwitterAccountModalOpen] = useState(false)
  const [styleBody, setStyleBody] = useState(false)
  const [twitterHandle, setTwitterHandle] = useState('')
  const [newProfilePubkey, setNewProfilePubkey] = useState('')
  const [bearerToken, setBearerToken] = useState('')
  const [signingProfile, setSigningProfile] = useState(null)

  const signingProfiles = useSelector(selectSigningProfiles);

  const dispatch = useDispatch()

  const searchOnChange = (param) => {
    if(tab !== 'Search'){setTab('Search')}
    if(param.length>0){
      // TODO: search for a profile by name.
    }
  }

  const optionsFromProfiles = (profiles) => {
    return profiles.map((p) => {
        return { value: p, label: p.getProfileName() }
        // return { value: 'chocolate', label: 'Chocolate' }
      });
  }

  const toggleCreateTwitterAccountModal = (param, type) => {
    setStyleBody(!styleBody)
    setTimeout(()=>{ setTwitterAccountModalOpen(!twitterAccountModalOpen) },20)
  }

  const createTwitterAccount = () => {
    console.log('Create twitter account with handle:', twitterHandle);
    if (!signingProfile) {
      alert('Signing profile must be set.');
      return;
    }
    dispatch(setCreateTwitterAccount({
      twitterHandle: twitterHandle,
      profileId: signingProfile.getProfileId(),
      bearerToken: bearerToken,
    }))
    .then(unwrapResult)
    .then((pubkey) => {
      console.log('Created twitter account with handle', twitterHandle);
    })
    .catch((err) => {
      alert(err.message);
    });
    toggleCreateTwitterAccountModal();
  }

  const handleModalClick = (e) => {
    e.stopPropagation()
  }

  const handleChangeSigningProfile = (e) => {
    setSigningProfile(e.value);
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
            <div onClick={(e)=>toggleCreateTwitterAccountModal('edit')}
              className='profiles-create-button'>
              <span>Add Twitter Account</span>
            </div>
          </div>
        </div>
        <div>
          <div className="explore-nav-menu">
            <div onClick={()=>setTab('Signing Profiles')} className={tab === 'Signing Profiles' ? `explore-nav-item activeTab` : `explore-nav-item`}>
              Twitter Accounts
            </div>
          </div>
          <TwitterAccounts />
        </div>
      </div>


      {/* Modal for create signing profile */}
      <div onClick={()=>toggleCreateTwitterAccountModal()} style={{display: twitterAccountModalOpen ? 'block' : 'none'}} className="modal-edit">
        <div onClick={(e)=>handleModalClick(e)} className="modal-content">
          <div className="modal-header">
            <div className="modal-closeIcon">
              <div onClick={()=>toggleCreateTwitterAccountModal()} className="modal-closeIcon-wrap">
                <ICON_CLOSE />
              </div>
            </div>
            <p className="modal-title">Add Twitter Account</p>

            <div className="save-modal-wrapper">
              <div onClick={createTwitterAccount} className="save-modal-btn">
                Submit
              </div>
            </div>
          </div>

          <div className="modal-body">
            <form className="edit-form">
              <div className="edit-input-wrap">
                <div className="edit-input-content">
                  <label>Twitter Handle</label>
                  <input onChange={(e)=>setTwitterHandle(e.target.value)} type="text" name="name" className="edit-input"/>
                </div>
              </div>
              <div className="edit-input-wrap">
                <div className="edit-input-content">
                  <label>Twitter Bearer Token</label>
                  <input onChange={(e)=>setBearerToken(e.target.value)} type="text" name="name" className="edit-input"/>
                </div>
              </div>
              <div className="edit-input-wrap">
                <div className="edit-input-content">
                  <label>Signing Profile</label>
                  <div className="inner-input-box">
                      <Select options={optionsFromProfiles(signingProfiles)} onChange={handleChangeSigningProfile} />
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>


    </div>
  )
}

export default withRouter(Twitter)
