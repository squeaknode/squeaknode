import React, { useEffect, useState, useContext } from 'react'
import './style.scss'
import { withRouter, Link } from 'react-router-dom'
import { ICON_SEARCH, ICON_ARROWBACK, ICON_CLOSE, ICON_LAPTOPFILL } from '../../Icons'
import { getProfileImageSrcString } from '../../squeakimages/images';
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'

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

    const goToPeer = (peerAddress) => {
        props.history.push(`/app/peer/${peerAddress.getNetwork()}/${peerAddress.getHost()}/${peerAddress.getPort()}`)
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

    const getNetwork = () => {
      if (useTor) {
        return 'TORV3';
      }
      return 'IPV4';
    };

    function removeHttp(url) {
      return url.replace(/^https?:\/\//, '');
    }

    const savePeer = () => {
        const network = getNetwork();
        const strippedHost = removeHttp(host);
        dispatch(setSavePeer({
            name: name,
            host: strippedHost,
            port: port,
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
                  const peerId = sp.getPeerId();
                  const savedPeerName = sp.getPeerName();
                  const peerAddress = sp.getPeerAddress();
                  const host = peerAddress.getHost();
                  const port = peerAddress.getPort();
                  const addrStr = host + ':' + port;

                  return <div onClick={()=>goToPeer(peerAddress)} key={peerId} className="search-result-wapper">
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
                            <label>Name (not required)</label>
                            <input onChange={(e)=>setName(e.target.value)} type="text" name="name" className="edit-input"/>
                        </div>
                    </div>
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
                    <div className="edit-input-wrap">
                        <div className="edit-input-content">
                        <label>
                        <input
                        type="checkbox"
                        checked={useTor}
                        onChange={handleChangeUseTor}
                        />
                        Use Tor
                        </label>
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
