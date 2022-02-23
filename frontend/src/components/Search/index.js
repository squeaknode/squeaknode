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
import TweetCard from '../TweetCard'
import MakeSqueak from '../MakeSqueak'


const Search = (props) => {
    const { state, actions } = useContext(StoreContext);
    const { search } = useLocation();
    const { searchTweets, session } = state;
    const [searchText, setSearchText] = useState('');

    const q = useMemo(() => {
      const p = new URLSearchParams(search);
      const q = p.get('q');
      return q ? decodeURIComponent(q) : '';
    }, [search]);


    useEffect(() => {
        window.scrollTo(0, 0)
        // actions.getTweets({lastTweet: null})
        if (q && q.length > 1) {
          setSearchText(q);
          reloadTweets(q);
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

    const getMoreTweets = () => {
        let lastTweet = getLastSqueak(state.searchTweets);
        actions.search({
          searchText: searchText,
          lastTweet: lastTweet
        });
    }

    const reloadTweets = (s) => {
        actions.clearSearch();
        actions.search({
          searchText: s,
          lastTweet: null
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
            <div className="Tweet-input-divider"></div>
            {searchTweets.map(t => {
                return <TweetCard tweet={t} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} />
            })}

            {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
            {searchTweets.length > 0 &&
              <>
              {state.loading ? <Loader /> : <div onClick={() => getMoreTweets()} className='tweet-btn-side tweet-btn-active'>
                  Load more
              </div>}
              </>
            }

        </div>
    )
}

export default withRouter(Search)
