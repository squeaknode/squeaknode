import React, { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import axios from 'axios'
import ContentEditable from 'react-contenteditable'
import { ICON_IMGUPLOAD } from '../../Icons'
import { Link } from 'react-router-dom'
import { API_URL } from '../../config'
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import MakeSqueak from '../MakeSqueak'


const Home = () => {
    const { state, actions } = useContext(StoreContext)
    const { session } = state
    useEffect(() => {
        window.scrollTo(0, 0)
        // actions.getSqueaks({lastSqueak: null})
        reloadSqueaks();
    }, [])

    const getLastSqueak = (squeakLst) => {
      if (squeakLst == null) {
        return null;
      } if (squeakLst.length === 0) {
        return null;
      }
      return squeakLst.slice(-1)[0];
    };

    const getMoreSqueaks = () => {
        let lastSqueak = getLastSqueak(state.squeaks);
        actions.getSqueaks({lastSqueak: lastSqueak});
    }

    const reloadSqueaks = () => {
        actions.clearSqueaks();
        actions.getSqueaks({lastSqueak: null});
    }

    return (
        <div className="Home-wrapper">
            <div className="Home-header-wrapper">
                <h2 className="Home-header">
                    Latest Squeaks
                </h2>
            </div>
            {session ? <MakeSqueak /> : null }
            <div className="Squeak-input-divider"></div>
            {state.squeaks.map(t => {
                return <SqueakCard squeak={t} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} />
            })}

            {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
            {state.loading ? <Loader /> : <div onClick={() => getMoreSqueaks()} className='squeak-btn-side squeak-btn-active'>
                Load more
            </div>}

        </div>
    )
}

export default Home
