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
import MakeSqueak from '../MakeSqueak'
import ContentEditable from 'react-contenteditable'
import {
    enable as enableDarkMode,
    disable as disableDarkMode,
    setFetchMethod
} from 'darkreader';

const Nav = ({history}) => {
    const { state, actions } = useContext(StoreContext)

    const { session } = state
    const [moreMenu, setMoreMenu] = useState(false)
    const [theme, setTheme] = useState(true)
    const [modalOpen, setModalOpen] = useState(false)
    const [styleBody, setStyleBody] = useState(false)

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
                        <div className={path === '/profiles' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
                            {path === '/prof' ? <ICON_USERFILL /> : <ICON_USER />}
                            <div className="Nav-item">Profiles</div>
                        </div>
                    </Link>
                    {session ?
                    <>
                    <Link to="/app/peers" className="Nav-link">
                        <div className={path === '/expl' ? "Nav-item-hover active-Nav" : "Nav-item-hover"}>
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
                            <div style={{top: `${document.getElementById('moremenu').getBoundingClientRect().top - 40}px`, left: `${document.getElementById('moremenu').getBoundingClientRect().left}px`, height: !session ? '104px' : null }} onClick={(e)=>handleMenuClick(e)} className="more-menu-content">
                                    <div onClick={changeTheme} className="more-menu-item">
                                        <span>Change Theme</span>
                                        <span>{theme ? <ICON_DARK/> : <ICON_LIGHT />}</span>
                                    </div>
                                    <div onClick={()=>actions.logout()} className="more-menu-item">
                                        Log out
                                    </div>
                            </div> : null }
                        </div>
                        </div>
                    </div>
                    {session ?
                    <div className="Nav-tweet">
                        <div onClick={()=>toggleModal()} className="Nav-tweet-link">
                            <div className="Nav-tweet-btn btn-hide">
                                Tweet
                            </div>
                            <div className="Nav-tweet-btn btn-show">
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
                    <p className="modal-title">Tweet</p>
                </div>
                <div style={{marginTop:'5px'}} className="modal-body">
                    <MakeSqueak submittedCallback={toggleModal} />
                </div>
            </div>
        </div>
        </div>
    )
}

export default withRouter(Nav)
