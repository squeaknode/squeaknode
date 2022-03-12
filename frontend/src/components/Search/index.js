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
import SearchResults from '../../features/search/SearchResults'



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
          <SearchResults />
        </div>
    )
}

export default withRouter(Search)
