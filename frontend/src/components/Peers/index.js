import React, { useEffect, useState, useContext } from 'react'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import PeerCard from '../../features/peers/PeerCard'

import { Form, Input, Select, Checkbox, Relevant, Debug, TextArea, Option } from 'informed';

import { unwrapResult } from '@reduxjs/toolkit'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import {
  selectSavedPeers,
  fetchSavedPeers,
  setSavePeer,
} from '../../features/peers/peersSlice'
import {
  fetchExternalAddress,
  selectExternalAddress,
} from '../../features/externalAddress/externalAddressSlice'



const Peers = (props) => {
    const [tab, setTab] = useState('Saved Peers')
    const [savePeerModalOpen, setSavePeerModalOpen] = useState(false)
    const [showExternalAddressModalOpen, setShowExternalAddressModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [name, setName] = useState('')
    const [host, setHost] = useState('')
    const [port, setPort] = useState('')
    const [useTor, setUseTor] = useState(false)

    const externalAddress = useSelector(selectExternalAddress);
    const peers = useSelector(selectSavedPeers);
    const dispatch = useDispatch();


    useEffect(() => {
        window.scrollTo(0, 0)
        dispatch(fetchExternalAddress());
        dispatch(fetchSavedPeers());
    }, [])

    const goToUser = (id) => {
        props.history.push(`/app/profile/${id}`)
    }

    const peerUrl = (peerAddress) => {
        return `/app/peer/${peerAddress.getNetwork()}/${peerAddress.getHost()}/${peerAddress.getPort()}`;
    }

    const peerAddressToStr = (peerAddress) => {
      return `${peerAddress.getNetwork()}/${peerAddress.getHost()}:${peerAddress.getPort()}`;
    }

    const toggleSavePeerModal = (param, type) => {
        setStyleBody(!styleBody)
        setTimeout(()=>{ setSavePeerModalOpen(!savePeerModalOpen) },20)
    }

    const toggleShowExternalAddressModalOpen = () => {
        setStyleBody(!styleBody)
        setTimeout(()=>{ setShowExternalAddressModalOpen(!showExternalAddressModalOpen) },20)
    }

    const getNetwork = (useTor) => {
      if (useTor) {
        return 'TORV3';
      }
      return 'IPV4';
    };

    function removeHttp(url) {
      return url.replace(/^https?:\/\//, '');
    }

    const savePeer = ({values}) => {
        const network = getNetwork(values.useTor);
        const strippedHost = removeHttp(values.host);
        dispatch(setSavePeer({
            name: values.name,
            host: strippedHost,
            port: values.port,
            network: network,
        }));
        toggleSavePeerModal();
    }

    const handleChangeUseTor = () => {
      setUseTor(!useTor);
    };

    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const AddPeerForm = () => (
      <Form onSubmit={savePeer} className="Squeak-input-side">
        <div className="edit-input-wrap">
          <Input class="informed-input" name="name" label="Peer Name (not required)" />
        </div>
        <div className="edit-input-wrap">
          <Input class="informed-input" name="host" label="Host" />
        </div>
        <div className="edit-input-wrap">
          <Input class="informed-input" name="port" label="Port" />
        </div>
        <div className="edit-input-wrap">
          <Checkbox class="informed-input" name="useTor" label="Connect With Tor" />
        </div>

        <div className="inner-input-links">
          <div className="input-links-side">
          </div>
          <div className="squeak-btn-holder">
            <div style={{ fontSize: '13px', color: null }}>
            </div>
            <button type="submit" className={'squeak-btn-side squeak-btn-active'}>
              Submit
            </button>
          </div>
        </div>
      </Form>
    );


    return(
        <div>

        <div className="explore-wrapper">
            <div className="peers-header-wrapper">
                <div className="peers-header-content">
                    <div className="peers-header-name">
                        Peers
                    </div>
                </div>
            </div>
            <div className="profile-details-wrapper">
            <div className="profiles-options">
            <div onClick={(e)=>toggleShowExternalAddressModalOpen('edit')}
               className='profiles-create-button'>
                  <span>Show External Address</span>
            </div>
            <div onClick={(e)=>toggleSavePeerModal('edit')}
               className='profiles-create-button'>
                  <span>Add Peer</span>
            </div>
            </div>
            </div>
            <div>
                <div className="explore-nav-menu">
                    <div onClick={()=>setTab('Saved Peers')} className={tab === 'Saved Peers' ? `explore-nav-item activeTab` : `explore-nav-item`}>
                        Peers
                    </div>
                </div>
                {tab === 'Saved Peers' ?
                peers.map(sp=>{
                  return <PeerCard peer={sp}/>
                })
                :
                tab === 'Connected Peers' ?
                <></>
                : <div className="try-searching">
                        Nothing to see here ..
                        <div/>
                    Try searching for people, usernames, or keywords

                </div>
                }
            </div>
        </div>

        {/* Modal for show external address */}
        <div onClick={()=>toggleShowExternalAddressModalOpen()} style={{display: showExternalAddressModalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleShowExternalAddressModalOpen()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">'Show External Address'</p>
                </div>

                <div className="modal-body">
                    <form className="edit-form">
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Host</label>
                                <input defaultValue={externalAddress && externalAddress.getHost()} readOnly type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                        <div className="edit-input-wrap">
                            <div className="edit-input-content">
                                <label>Port</label>
                                <input defaultValue={externalAddress && externalAddress.getPort()} readOnly type="text" name="name" className="edit-input"/>
                            </div>
                        </div>
                    </form>
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
                    <p className="modal-title">Add Peer</p>

                </div>

                <div className="modal-body">
                    <AddPeerForm />
                </div>
            </div>
        </div>


        </div>
    )
}

export default withRouter(Peers)
