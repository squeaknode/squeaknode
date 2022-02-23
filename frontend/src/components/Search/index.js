import React, { useEffect, useState, useContext, useRef, useMemo } from 'react'
import { withRouter, useLocation } from 'react-router-dom';
import { StoreContext } from '../../store/store'
import './style.scss'
import axios from 'axios'
import ContentEditable from 'react-contenteditable'
import { ICON_IMGUPLOAD, ICON_SEARCH } from '../../Icons'
import { Link } from 'react-router-dom'
import { API_URL } from '../../config'
import Loader from '../Loader'
import SqueakCard from '../SqueakCard'
import MakeSqueak from '../MakeSqueak'


const Search = (props) => {
    const { state, actions } = useContext(StoreContext);
    const { search } = useLocation();
    const { searchSqueaks, session } = state;
    const [searchText, setSearchText] = useState('');

    const q = useMemo(() => {
      const p = new URLSearchParams(search);
      const q = p.get('q');
      return q ? decodeURIComponent(q) : '';
    }, [search]);


    useEffect(() => {
        window.scrollTo(0, 0)
        // actions.getSqueaks({lastSqueak: null})
        if (q && q.length > 1) {
          setSearchText(q);
          reloadSqueaks(q);
        }
    }, [q])

    const changeSearchText = (param) => {
        setSearchText(param);
    }

    const searchOnEnter = (e) => {
        if (e.keyCode === 13) {
          if(searchText.length>0){
            goToNewSearch(searchText);
          }
        }
    }

    const getLastSqueak = (squeakLst) => {
      if (squeakLst == null) {
        return null;
      } if (squeakLst.length === 0) {
        return null;
      }
      return squeakLst.slice(-1)[0];
    };

    const getMoreSqueaks = () => {
        let lastSqueak = getLastSqueak(state.searchSqueaks);
        actions.search({
          searchText: searchText,
          lastSqueak: lastSqueak
        });
    }

    const reloadSqueaks = (s) => {
        actions.clearSearch();
        actions.search({
          searchText: s,
          lastSqueak: null
        });
    }

    const goToNewSearch = (newSearchText) => {
        props.history.push(`/app/search?q=${newSearchText}`);
    }

    return (
        <div className="Home-wrapper">
            <div className="explore-header">
            <div className="explore-search-wrapper">
                <div className="explore-search-icon">
                    <ICON_SEARCH/>
                </div>
                <div className="explore-search-input">
                    <input value={searchText} onKeyDown={(e)=>searchOnEnter(e)} onChange={(e)=>changeSearchText(e.target.value)} placeholder="Search Squeaks" type="text" name="search"/>
                </div>
            </div>
            </div>
            <div className="Squeak-input-divider"></div>
            {searchSqueaks.map(t => {
                return <SqueakCard squeak={t} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} />
            })}

            {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
            {searchSqueaks.length > 0 &&
              <>
              {state.loading ? <Loader /> : <div onClick={() => getMoreSqueaks()} className='squeak-btn-side squeak-btn-active'>
                  Load more
              </div>}
              </>
            }

        </div>
    )
}

export default withRouter(Search)
