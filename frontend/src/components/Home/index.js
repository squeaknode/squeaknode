import React, { useEffect, useState, useContext, useRef } from 'react'
import { StoreContext } from '../../store/store'
import './style.scss'
import axios from 'axios'
import ContentEditable from 'react-contenteditable'
import { ICON_IMGUPLOAD } from '../../Icons'
import { Link } from 'react-router-dom'
import { API_URL } from '../../config'
import Loader from '../Loader'
import TweetCard from '../TweetCard'
import MakeSqueak from '../MakeSqueak'


const Home = () => {
    const { state, actions } = useContext(StoreContext)
    const { account, session } = state
    useEffect(() => {
        window.scrollTo(0, 0)
        // actions.getTweets({lastTweet: null})
        reloadTweets();
    }, [])

    const getLastSqueak = (squeakLst) => {
      if (squeakLst == null) {
        return null;
      } if (squeakLst.length === 0) {
        return null;
      }
      return squeakLst.slice(-1)[0];
    };

    const getMoreTweets = () => {
        let lastTweet = getLastSqueak(state.tweets);
        actions.getTweets({lastTweet: lastTweet});
    }

    const reloadTweets = () => {
        actions.clearTweets();
        actions.getTweets({lastTweet: null});
    }

    return (
        <div className="Home-wrapper">
            <div className="Home-header-wrapper">
                <h2 className="Home-header">
                    Latest Tweets
                </h2>
            </div>
            {session ? <MakeSqueak /> : null }
            <div className="Tweet-input-divider"></div>
            {/* { state.account && <TweetCard parent={t.parent} key={'1'} id={'1'} user={'1'} createdAt={'2019'} description={'t.description'}
                images={'t.images'} replies={[]} retweets={[]} likes={[]} style={{height:'0'}} />} */}
            {state.tweets.map(t => {
                return <TweetCard tweet={t} retweet={t.getReplyTo()} username={t.getAuthorPubkey()} name={t.getAuthorPubkey()} parent={null} key={t.getSqueakHash()} id={t.getSqueakHash()} user={t.getAuthor()} createdAt={t.getBlockTime()} description={t.getContentStr()}
                    images={[]} replies={[]} retweets={[]} likes={[]} />
            })}

            {/* TODO: fix get loading state by doing this: https://medium.com/stashaway-engineering/react-redux-tips-better-way-to-handle-loading-flags-in-your-reducers-afda42a804c6 */}
            {state.loading ? <Loader /> : <div onClick={() => getMoreTweets()} className='tweet-btn-side tweet-btn-active'>
                Load more
            </div>}

        </div>
    )
}

export default Home
