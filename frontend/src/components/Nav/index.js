import React , { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import { Link, withRouter, Redirect } from 'react-router-dom'
import './style.scss'
import { ICON_LOGO, ICON_HOME, ICON_HASH, ICON_BELL, ICON_INBOX
, ICON_LIST, ICON_USER, ICON_LAPTOP, ICON_SETTINGS, ICON_HOMEFILL, ICON_HASHFILL,
ICON_BELLFILL, ICON_LISTFILL, ICON_USERFILL, ICON_LAPTOPFILL, ICON_FEATHER,
ICON_CLOSE,ICON_IMGUPLOAD, ICON_INBOXFILL, ICON_LIGHT, ICON_DARK } from '../../Icons'
import { ReactComponent as YourSvg } from '../../icon.svg';
import axios from 'axios'
import {API_URL} from '../../config'
import MakeSqueak from '../../features/squeaks/MakeSqueak'
import ContentEditable from 'react-contenteditable'
import {
    enable as enableDarkMode,
    disable as disableDarkMode,
    setFetchMethod
} from 'darkreader';

import { unwrapResult } from '@reduxjs/toolkit'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import {
  fetchSellPrice,
  selectSellPriceDefault,
  selectSellPriceOverride,
  selectSellPriceUsingOverride,
  selectSellPriceInfo,
  setSellPrice,
  setClearSellPrice,
} from '../../features/sellPrice/sellPriceSlice'
import {
  setLogout,
} from '../../features/account/accountSlice'

const Nav = ({history}) => {
    const { state, actions } = useContext(StoreContext)

    // const { sellPrice, session } = state
    const [moreMenu, setMoreMenu] = useState(false)
    const [theme, setTheme] = useState(true)
    const [modalOpen, setModalOpen] = useState(false)
    const [sellPriceModalOpen, setSellPriceModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)
    const [newSellPriceMsat, setNewSellPriceMsat] = useState('')

    const session = true;
    const sellPrice = useSelector(selectSellPriceInfo);
    const dispatch = useDispatch();


    const isInitialMount = useRef(true);
    useEffect(() => {
        if (isInitialMount.current){ isInitialMount.current = false }
        else {
            document.getElementsByTagName("body")[0].style.cssText = styleBody && "overflow-y: hidden; margin-right: 17px"
        }
    }, [styleBody])

    useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )

    useEffect(()=>{
        let ran = false
        if(localStorage.getItem('Theme')=='dark'){
            setTheme('dark')
            setFetchMethod(window.fetch)
            enableDarkMode();
        }else if(!localStorage.getItem('Theme')){
            localStorage.setItem('Theme', 'light')
        }
        dispatch(fetchSellPrice());
      }, [])

      const path = history.location.pathname.slice(4,9)

      const openMore = () => { setMoreMenu(!moreMenu) }

      const handleMenuClick = (e) => { e.stopPropagation() }

    const toggleModal = (e, type) => {
        if(e){ e.stopPropagation() }
        setStyleBody(!styleBody)
        // TODO: Discard content on modal toggle off.
        setTimeout(()=>{ setModalOpen(!modalOpen) },20)
    }

    const toggleSellPriceModal = (param, type) => {
        setStyleBody(!styleBody)
        setTimeout(()=>{ setSellPriceModalOpen(!sellPriceModalOpen) },20)
    }


    const handleModalClick = (e) => {
        e.stopPropagation()
    }

    const changeTheme = () => {
        if(localStorage.getItem('Theme') === 'dark'){
            disableDarkMode()
            localStorage.setItem('Theme', 'light')
        }else if(localStorage.getItem('Theme') === 'light'){
            localStorage.setItem('Theme', 'dark')
            setFetchMethod(window.fetch)
            enableDarkMode();
        }
    }

    const updateSellPrice = () => {
        let values = {
            sellPriceMsat: newSellPriceMsat,
        }
        dispatch(setSellPrice(newSellPriceMsat));
        toggleSellPriceModal()
    }

    const setSellPriceToDefault = () => {
        dispatch(setClearSellPrice());
        toggleSellPriceModal()
    }

    console.log(sellPrice);

    return(
        <div className="Nav-component">
        <div className="Nav-width">
            <div className="Nav">
            <div className="Nav-Content">
                <nav className="Nav-wrapper">
                    <Link to={`/app/home`} className="logo-wrapper">
                        <YourSvg styles={{fill:"rgb(29,161,242)", width:'47px', height:"30px"}}/>
                    </Link>
                    <Link className="Nav-link" to={`/app/home`}>
                        <div className={path === '/home' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/home' ? <ICON_HOMEFILL /> : <ICON_HOME />}
                            <div className="Nav-item">Home</div>
                        </div>
                    </Link>
                    <Link to="/app/profiles" className="Nav-link">
                        <div className={path === '/prof' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/prof' ? <ICON_USERFILL /> : <ICON_USER />}
                            <div className="Nav-item">Profiles</div>
                        </div>
                    </Link>
                    {session ?
                    <>
                    <Link to="/app/peers" className="Nav-link">
                        <div className={path === '/peer' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/peer' ? <ICON_LAPTOPFILL /> : <ICON_LAPTOP />}
                            <div className="Nav-item">Peers</div>
                        </div>
                    </Link>
                    <Link to="/app/payments" className="Nav-link">
                        <div className={path === '/paym' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/paym' ?  <ICON_LISTFILL /> : <ICON_LIST />}
                            <div className="Nav-item">Payments</div>
                        </div>
                    </Link>
                    <Link to="/app/notifications" className="Nav-link">
                        <div className={path === '/noti' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/noti' ? <ICON_BELLFILL /> : <ICON_BELL />}
                            <div className="Nav-item">Notifications</div>
                        </div>
                    </Link>
                    </> : null}
                    <div id="moremenu" onClick={openMore} className="Nav-link">
                        <div className={"Nav-item-hover"}>
                            <ICON_SETTINGS  />
                            <div className="Nav-item">More</div>
                        </div>
                        <div onClick={()=>openMore()} style={{display: moreMenu ? 'block' : 'none'}} className="more-menu-background">
                        <div className="more-modal-wrapper">
                            {moreMenu ?
                            <div style={{top: `${document.getElementById('moremenu').getBoundingClientRect().top - 40}px`, left: `${document.getElementById('moremenu').getBoundingClientRect().left}px`, height: '154px' }} onClick={(e)=>handleMenuClick(e)} className="more-menu-content">
                                    <div onClick={changeTheme} className="more-menu-item">
                                        <span>Change Theme</span>
                                        <span>{theme ? <ICON_DARK/> : <ICON_LIGHT />}</span>
                                    </div>
                                    <div onClick={toggleSellPriceModal} className="more-menu-item">
                                        <span>Update Sell Price</span>
                                        <span><ICON_HASH /></span>
                                    </div>
                                    <div onClick={()=>actions.logout()} className="more-menu-item">
                                        Log out
                                    </div>
                            </div> : null }
                        </div>
                        </div>
                    </div>
                    {session ?
                    <div className="Nav-squeak">
                        <div onClick={()=>toggleModal()} className="Nav-squeak-link">
                            <div className="Nav-squeak-btn btn-hide">
                                Squeak
                            </div>
                            <div className="Nav-squeak-btn btn-show">
                                <span><ICON_FEATHER/></span>
                            </div>
                        </div>
                    </div> : null }
                </nav>
                <div>

                </div>
            </div>
            </div>
        </div>

        <div onClick={()=>toggleModal()} style={{display: modalOpen ? 'block' : 'none'}} className="modal-edit">
            <div style={{minHeight: '270px', height: 'initial'}} onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">Squeak</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                    <MakeSqueak submittedCallback={toggleModal} />
                </div>
            </div>
        </div>


        {/* Modal for set sell price */}
        <div onClick={()=>toggleSellPriceModal()} style={{display: sellPriceModalOpen ? 'block' : 'none'}} className="modal-edit">
            <div onClick={(e)=>handleModalClick(e)} className="modal-content">
                <div className="modal-header">
                    <div className="modal-closeIcon">
                        <div onClick={()=>toggleSellPriceModal()} className="modal-closeIcon-wrap">
                            <ICON_CLOSE />
                        </div>
                    </div>
                    <p className="modal-title">'Sell Price'</p>
                    <div className="save-modal-wrapper">
                        <div onClick={updateSellPrice} className="save-modal-btn">
                            Save
                        </div>
                    </div>
                    <div className="save-modal-wrapper">
                        <div onClick={setSellPriceToDefault} className="save-modal-btn">
                            Reset To Default
                        </div>
                    </div>
                </div>
                {sellPrice &&
                <div className="modal-body">
                      <form className="edit-form">
                          <div className="edit-input-wrap">
                              <div className="edit-input-content">
                                  <label>Sell Price (msats)</label>
                                  <input defaultValue={sellPrice.getPriceMsatIsSet() ? sellPrice.getPriceMsat() : sellPrice.getDefaultPriceMsat()} onChange={(e)=>setNewSellPriceMsat(e.target.value)} type="text" name="sellPrice" className="edit-input"/>
                              </div>
                          </div>
                      </form>
                </div>
                }
            </div>
        </div>



        </div>
    )
}

export default withRouter(Nav)
