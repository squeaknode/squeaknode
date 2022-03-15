import React, { useEffect, useState, useContext } from 'react'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'

import { unwrapResult } from '@reduxjs/toolkit'
import { useDispatch } from 'react-redux'

import SigningProfiles from '../../features/profiles/SigningProfiles'
import ContactProfiles from '../../features/profiles/ContactProfiles'
import {
  setCreateSigningProfile,
  setImportSigningProfile,
  setCreateContactProfile,
} from '../../features/profiles/profilesSlice'


const Profiles = (props) => {
    const [tab, setTab] = useState('Signing Profiles')
    const [signingProfileModalOpen, setSigningProfileModalOpen] = useState(false)
    const [contactProfileModalOpen, setContactProfileModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [newProfileName, setNewProfileName] = useState('')
    const [newProfilePubkey, setNewProfilePubkey] = useState('')
    const [usePrivKey, setUsePrivKey] = useState(false)
    const [newProfilePrivkey, setNewProfilePrivkey] = useState('')

    const dispatch = useDispatch()

    const searchOnChange = (param) => {
        if(tab !== 'Search'){setTab('Search')}
        if(param.length>0){
            // TODO: search for a profile by name.
        }
    }

    const toggleSigningProfileModal = (param, type) => {
        setStyleBody(!styleBody)
        setTimeout(()=>{ setSigningProfileModalOpen(!signingProfileModalOpen) },20)
    }

    const toggleContactProfileModal = (param, type) => {
        setStyleBody(!styleBody)
        setTimeout(()=>{ setContactProfileModalOpen(!contactProfileModalOpen) },20)
    }

    const createSigningProfile = () => {
        if (usePrivKey) {
          console.log('Import signing profile with name:', newProfileName);
          dispatch(setImportSigningProfile({profileName: newProfileName, privateKey: newProfilePrivkey}))
          .then(unwrapResult)
          .then((pubkey) => {
            console.log('Created profile with pubkey', pubkey);
            props.history.push(`/app/profile/${pubkey}`);
          })
          .catch((err) => {
            alert(err.message);
          });
        } else {
          console.log('Create signing profile with name:', newProfileName);
          dispatch(setCreateSigningProfile({profileName: newProfileName}))
          .then(unwrapResult)
          .then((pubkey) => {
            console.log('Created profile with pubkey', pubkey);
            props.history.push(`/app/profile/${pubkey}`);
          })
          .catch((err) => {
            alert(err.message);
          });
        }
        toggleSigningProfileModal();
    }

    const createContactProfile = () => {
        dispatch(setCreateContactProfile({profileName: newProfileName, pubkey: newProfilePubkey}))
        .then(unwrapResult)
        .then((pubkey) => {
          console.log('Created profile with pubkey', pubkey);
          props.history.push(`/app/profile/${pubkey}`);
        })
        .catch((err) => {
          alert(err.message);
        });
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
                  <SigningProfiles />
                :
                tab === 'Contact Profiles' ?
                  <ContactProfiles />
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
