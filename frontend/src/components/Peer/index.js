import React , { useEffect, useState, useContext, useRef } from 'react'
import './style.scss'
import moment from 'moment'
import {  withRouter, Link } from 'react-router-dom'
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import {API_URL} from '../../config'
import axios from 'axios'
import {ICON_ARROWBACK, ICON_UPLOAD, ICON_CLOSE,ICON_SEARCH } from '../../Icons'

import { unwrapResult } from '@reduxjs/toolkit'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import {
  fetchPeer,
  selectCurrentPeer,
  selectCurrentPeerStatus,
  setSavePeer,
  setDeletePeer,
  setPeerAutoconnectEnabled,
  setPeerAutoconnectDisabled,
} from '../../features/peers/peersSlice'


const Peer = (props) => {

  const [modalOpen, setModalOpen] = useState(false)

  const [editName, setName] = useState('')
  const [editDescription, setDescription] = useState('')
  const [deleteModalOpen, setDeleteModalOpen] = useState(false)
  const [savePeerModalOpen, setSavePeerModalOpen] = useState(false)
  const [banner, setBanner] = useState('')
  const [saved, setSaved] = useState(false)
  const [tab, setTab] = useState('Members')
  const [bannerLoading, setBannerLoading] = useState(false)
  const [styleBody, setStyleBody] = useState(false)

  const peer = useSelector(selectCurrentPeer);
  const dispatch = useDispatch();


  useEffect(() => {
    window.scrollTo(0, 0)
    dispatch(fetchPeer({
      network: props.match.params.network,
      host: props.match.params.host,
      port: props.match.params.port,
    }));
  }, [])

  const isInitialMount = useRef(true);
  useEffect(() => {
    if (isInitialMount.current){ isInitialMount.current = false }
    else {
      document.getElementsByTagName("body")[0].style.cssText = styleBody && "overflow-y: hidden; margin-right: 17px"
    }
  }, [styleBody])

  useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )


  const deletePeer = () => {
    let values = {
      peerId: peer.getPeerId(),
    }
    dispatch(setDeletePeer(values));
    toggleDeleteModal();
  }

  function removeHttp(url) {
    return url.replace(/^https?:\/\//, '');
  }

  const savePeer = () => {
    const strippedHost = removeHttp(props.match.params.host);
    dispatch(setSavePeer({
      name: editName,
      host: strippedHost,
      port: props.match.params.port,
      network: props.match.params.network,
    }));
    toggleSavePeerModal();
  }

  const enable = (e,id) => {
    e.stopPropagation()
    console.log(id);
    console.log(peer.getPeerId());
    let values = {
      peerId: peer.getPeerId(),
    }

    dispatch(setPeerAutoconnectEnabled(values));
  }

  const disable = (e,id) => {
    e.stopPropagation()
    let values = {
      peerId: peer.getPeerId(),
    }
    dispatch(setPeerAutoconnectDisabled(values));
  }

  const toggleDeleteModal = () => {
    setStyleBody(!styleBody)
    setSaved(false)
    setTimeout(()=>{ setDeleteModalOpen(!deleteModalOpen) },20)
  }

  const toggleSavePeerModal = (param, type) => {
    setStyleBody(!styleBody)
    setTimeout(()=>{ setSavePeerModalOpen(!savePeerModalOpen) },20)
  }

  const handleModalClick = (e) => {
    e.stopPropagation()
  }


  return(
    <div>

      <div className="profile-wrapper">
        <div className="profile-header-wrapper">
          <div className="profile-header-back">
            <div onClick={()=>window.history.back()} className="header-back-wrapper">
              <ICON_ARROWBACK/>
            </div>
          </div>
          <div className="profile-header-content">
            <div className="profile-header-name">
              {props.match.params.host}:{props.match.params.port}
            </div>
          </div>
        </div>

        <div className="listp-details-wrap">
          <div className="bookmarks-header-name">{peer && peer.getPeerName()}</div>
          <div className="list-owner-wrap">
            <div>{props.match.params.host}:{props.match.params.port}</div>
          </div>

          <div className="profile-options">
            {peer &&
              <div onClick={(e)=>toggleDeleteModal()}
                className='peer-connect-button'>
                <span>Delete</span>
              </div>
            }
            {!peer &&
              <div onClick={(e)=>toggleSavePeerModal('edit')}
                className='profiles-create-button'>
                <span>Add Saved Peer</span>
              </div>
            }
          </div>

          <div className="profile-options">
            {peer &&
              <div onClick={(e)=>
                  peer.getAutoconnect() ?
                  disable(e,peer.getPeerId()) :
                  enable(e,peer.getPeerId())
                }
                className={peer.getAutoconnect() ? 'enable-btn-wrap disable-switch' : 'enable-btn-wrap'}>
                <span><span>{ peer.getAutoconnect() ? 'Enabled' : 'Disabled'}</span></span>
              </div>
            }
          </div>

        </div>

        <div className="feed-wrapper">
          <div className="feed-trending-card">
            <div className="feed-card-trend">
              <div>Number of downloads</div>
              <div>TODO</div>
            </div>
            <div className="feed-card-trend">
              <div>Number of purchases</div>
              <div>TODO</div>
            </div>
            <div className="feed-card-trend">
              <div>Last connection time</div>
              <div>TODO</div>
            </div>
          </div>
        </div>


      </div>

      {/* Modal for delete profile */}
      <div onClick={()=>toggleDeleteModal()} style={{display: deleteModalOpen ? 'block' : 'none'}} className="modal-edit">
        <div onClick={(e)=>handleModalClick(e)} className="modal-content">
          <div className="modal-header">
            <div className="modal-closeIcon">
              <div onClick={()=>toggleDeleteModal()} className="modal-closeIcon-wrap">
                <ICON_CLOSE />
              </div>
            </div>
            <p className="modal-title">'Delete Peer'</p>
            <div className="save-modal-wrapper">
              <div onClick={deletePeer} className="save-modal-btn">
                Delete
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal for create save peer */}
      <div onClick={()=>toggleSavePeerModal()} style={{display: savePeerModalOpen ? 'block' : 'none'}} className="modal-edit">
        <div onClick={(e)=>handleModalClick(e)} className="modal-content">
          <div className="modal-header">
            <div className="modal-closeIcon">
              <div onClick={()=>toggleSavePeerModal()} className="modal-closeIcon-wrap">
                <ICON_CLOSE />
              </div>
            </div>
            <p className="modal-title">Save Peer</p>

            <div className="save-modal-wrapper">
              <div onClick={savePeer} className="save-modal-btn">
                Submit
              </div>
            </div>
          </div>
          <div className="modal-body">
            <form className="edit-form">
              <div className="edit-input-wrap">
                <div className="edit-input-content">
                  <label>Name</label>
                  <input onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>


    </div>
  )
}

export default withRouter(Peer)
