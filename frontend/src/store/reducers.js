import type from './typeActions'

const initialState = {
    session: true,
    loggedin: false,
    network: null,
    tweets: [],
    tweet: null,
    ancestorTweets: [],
    replyTweets: [],
    tweetOffers: [],
    account: null,
    user: null,
    userTweets: [],
    bookmarks: [],
    recent_tweets: [],
    lists: [],
    list: null,
    trends: [],
    result: [],
    tagTweets: [],
    followers: [],
    following: [],
    resultUsers: [],
    suggestions: [],
    signingProfiles: [],
    contactProfiles: [],
    connectedPeers: [],
    peers: [],
    peer: null,
    peerConnection: null,
    top: '-100px',
    msg: '',
    conversations: null,
    conversation: null,
    paymentSummary: null,
    sentPayments: [],
    error: false
}

const reducer = (state = initialState, action) => {
    switch (action.type) {
        case type.SET_STATE:
            return {...state, ...action.payload }

        case type.ERROR:
            // message.error(action.payload.msg? action.payload.msg : action.payload == 'Unauthorized' ? 'You need to sign in' : 'error');
            return {...state, loading: false, error: true, msg: action.payload.msg}

        case type.LOGIN:
            localStorage.setItem("Twittertoken", action.payload.token)
            return {...state, ...action.payload, loggedin: true, loading: false, error: false}

        case type.REGISTER:
            setTimeout(()=>{action.data.func()},250)
            return {...state, ...action.payload, loading: false, error: false}

        case type.GET_NETWORK:
            return {...state, ...action.payload, loading: false, error: false}

        case type.TWEET:
            let recentT = state.tweets
            let s_tweet = state.tweet
            let replyT = state.replyTweets
            recentT.unshift(action.payload.tweet)
            if(s_tweet && s_tweet.getSqueakHash() === action.data.replyTo){
                // Update the replies if the current selected squeak is active.
                replyT.unshift(action.payload.tweet)
            }
            // TODO: update `state.userTweets` with the new tweet.
            return {...state, loading: false, error: false}

        case type.UPDATE_TWEET:
            let updatedTweetHash = action.payload.squeakHash
            let updatedTweet = action.payload.tweet
            let userTweetsU = state.userTweets
            let replyTweetsU = state.replyTweets
            let ancestorTweetsU = state.ancestorTweets
            let homeTweetsU = state.tweets
            let singleTweetU = state.tweet
            userTweetsU = userTweetsU.map((x)=>{
                return x.getSqueakHash() === updatedTweetHash ?
                updatedTweet : x
            })
            replyTweetsU = replyTweetsU.map((x)=>{
                return x.getSqueakHash() === updatedTweetHash ?
                updatedTweet : x
            })
            ancestorTweetsU = ancestorTweetsU.map((x)=>{
                return x.getSqueakHash() === updatedTweetHash ?
                updatedTweet : x
            })
            homeTweetsU = homeTweetsU.map((x)=>{
                return x.getSqueakHash() === updatedTweetHash ?
                updatedTweet : x
            })
            if (singleTweetU) {
              singleTweetU = singleTweetU.getSqueakHash() === updatedTweetHash ? updatedTweet : singleTweetU;
            }
            return {
                ...state,
                ...{tweet: singleTweetU},
                ...{userTweets: userTweetsU},
                ...{replyTweets: replyTweetsU},
                ...{ancestorTweets: ancestorTweetsU},
                ...{tweets: homeTweetsU},
            }

        // case type.LIKE_TWEET:
        //     console.log("action.payload")
        //     console.log(action.payload)
        //
        //     let account_likes = state.account
        //     let tweet_likes = state.tweets
        //     let user_likes = state.user
        //     let Stweet_likes = state.tweet
        //     if(action.payload.msg === "liked"){
        //
        //         if(Stweet_likes){
        //             Stweet_likes.likes.push(action.data.id)
        //         }
        //
        //         account_likes.likes.push(action.data.id)
        //         tweet_likes.length && tweet_likes.find(x=>x._id === action.data.id).likes.push(account_likes._id)
        //
        //         if(action.data.dest === 'profile'){
        //             user_likes.tweets.find(x=>x._id === action.data.id).likes.push(action.data.id)
        //             user_likes.likes = user_likes.tweets.filter(x=>x._id === action.data.id).concat(user_likes.likes)
        //         }
        //
        //     }else if(action.payload.msg === "unliked"){
        //
        //         if(Stweet_likes){
        //             Stweet_likes.likes = Stweet_likes.likes.filter((x)=>{
        //                 return x !== action.data.id
        //              });
        //         }
        //
        //         tweet_likes.length && tweet_likes.find(x=>x._id === action.data.id).likes.pop()
        //         let likeIndex = account_likes.likes.indexOf(action.data.id)
        //         likeIndex > -1 && account_likes.likes.splice(likeIndex, 1)
        //
        //         if(action.data.dest === 'profile'){
        //             user_likes.tweets.find(x=>x._id === action.data.id).likes.pop()
        //             user_likes.likes = user_likes.likes.filter((x)=>{
        //                return x._id !== action.data.id
        //             });
        //         }
        //     }
        //     return {...state, ...{account:account_likes}, ...{tweets:tweet_likes}, ...{user: user_likes}, ...{tweet: Stweet_likes}}

        case type.GET_TWEETS:
            let timelineT = state.tweets
            let newTweets = action.payload.tweets
            newTweets.forEach(t => timelineT.push(t));
            return {...state, loading: false, error: false}

        case type.CLEAR_TWEETS:
            return {...state, ...{tweets: []}}

        case type.GET_TWEET:
            return {...state, ...action.payload, loading: false, error: false}

        case type.GET_ACCOUNT:
            return {...state, ...action.payload}

        case type.BOOKMARK:
            let account_bookmarks = state.account
            if(action.payload.msg === "bookmarked"){
                account_bookmarks.bookmarks.push(action.data.id)
            }else if(action.payload.msg === "removed from bookmarks"){
                let bookIndex = account_bookmarks.bookmarks.indexOf(action.data.id)
                bookIndex > -1 && account_bookmarks.bookmarks.splice(bookIndex, 1)}
            return {...state, ...{account:account_bookmarks}}

        case type.GET_USER:
            return {...state, ...action.payload}

        case type.GET_USER_TWEETS:
            let userT = state.userTweets
            let newUserTweets = action.payload.userTweets
            newUserTweets.forEach(t => userT.push(t));
            return {...state, loading: false, error: false}

        case type.CLEAR_USER_TWEETS:
            return {...state, ...{userTweets: []}}

        case type.GET_ANCESTOR_TWEETS:
            return {...state, ...action.payload, loading: false, error: false}

        case type.GET_REPLY_TWEETS:
            return {...state, ...action.payload, loading: false, error: false}

        case type.GET_TWEET_OFFERS:
            return {...state, ...action.payload, loading: false, error: false}

        case type.GET_BOOKMARKS:
            return {...state, ...action.payload}

        case type.DELETE_USER:
            let deletedUserTweets = state.userTweets
            deletedUserTweets.forEach((item, i) => {
              item.setAuthor(null);
            });
            return {...state, ...{user:null}, loading: false, error: false}

        case type.UPDATE_USER:
            let updateUser = action.payload.user
            let updateUserTweets = state.userTweets
            updateUserTweets.forEach((item, i) => {
              item.setAuthor(updateUser);
            });
            return {...state, ...{user:updateUser}, loading: false, error: false}

        case type.RETWEET:
            let user_retweets = state.user
            let acc_retweets = state.account
            let t_retweets = state.tweets
            let Stweet_retweets = state.tweet
            if(action.payload.msg === "retweeted"){
                if(Stweet_retweets){ Stweet_retweets.retweets.push(action.data.id) }
                acc_retweets.retweets.push(action.data.id)
                for(let i = 0; i < t_retweets.length; i++){
                    if(t_retweets[i]._id === action.data.id){
                        t_retweets[i].retweets.push(state.account._id)
                    }
                }
            }else if(action.payload.msg === "undo retweet"){
                if(Stweet_retweets){
                    Stweet_retweets.retweets = Stweet_retweets.retweets.filter((x)=>{
                        return x !== action.data.id
                     });
                }
                let accRe_Index = acc_retweets.retweets.indexOf(action.data.id)
                accRe_Index > -1 && acc_retweets.retweets.splice(accRe_Index, 1)
                if(user_retweets){
                    user_retweets.tweets = user_retweets.tweets.filter((x)=>{
                        return x._id !== action.data.id})
                }
                for(let i = 0; i < t_retweets.length; i++){
                    if(t_retweets[i]._id === action.data.id){
                        t_retweets[i].retweets = t_retweets[i].retweets.filter((x)=>{
                            return x !== state.account._id})
                        }
                    }
                }
            return {...state, ...{user:user_retweets}, ...{account: acc_retweets}, ...{tweets: t_retweets}, ...{tweet: Stweet_retweets}}

        case type.DELETE_TWEET:
            let deletedTweetHash = action.payload.squeakHash
            let userTweetsD = state.userTweets
            let replyTweetsD = state.replyTweets
            let ancestorTweetsD = state.ancestorTweets
            let homeTweetsD = state.tweets
            let singleTweet = state.tweet
            userTweetsD = userTweetsD.filter((x)=>{
                    return x.getSqueakHash() !== deletedTweetHash
            })
            ancestorTweetsD = ancestorTweetsD.filter((x)=>{
                    return x.getSqueakHash() !== deletedTweetHash
            })
            replyTweetsD = replyTweetsD.filter((x)=>{
                    return x.getSqueakHash() !== deletedTweetHash
            })
            if(singleTweet && deletedTweetHash === singleTweet.getSqueakHash()){
                // window.location.replace('/home')
                singleTweet = null
            }
            homeTweetsD = homeTweetsD.filter((x)=>{
                return x.getSqueakHash() !== deletedTweetHash
            })
            return {
                ...state,
                ...{userTweets: userTweetsD},
                ...{replyTweets: replyTweetsD},
                ...{ancestorTweets: ancestorTweetsD},
                ...{tweets: homeTweetsD},
                ...{tweet: singleTweet}
            }

        case type.FOLLOW_USER:
            let followedUser = action.payload.user
            let followSP = state.signingProfiles
            let followCP = state.contactProfiles
            let newFollowSP = followSP.map(u => {
              return u.getPubkey() === followedUser.getPubkey() ?
              followedUser : u
            })
            let newFollowCP = followCP.map(u => {
              return u.getPubkey() === followedUser.getPubkey() ?
              followedUser : u
            })
            return {...state, ...{user: followedUser}, ...{signingProfiles: newFollowSP}, ...{contactProfiles: newFollowCP}}

        case type.UNFOLLOW_USER:
            let unfollowedUser = action.payload.user
            let unfollowSP = state.signingProfiles
            let unfollowCP = state.contactProfiles
            let newUnfollowSP = unfollowSP.map(u => {
              return u.getPubkey() === unfollowedUser.getPubkey() ?
              unfollowedUser : u
            })
            let newUnFollowCP = unfollowCP.map(u => {
              return u.getPubkey() === unfollowedUser.getPubkey() ?
              unfollowedUser : u
            })
            return {...state, ...{user: unfollowedUser}, ...{signingProfiles: newUnfollowSP}, ...{contactProfiles: newUnFollowCP}}

        case type.GET_LIST:
            return {...state, ...action.payload}

        case type.EDIT_LIST:
            ////
            return state

        case type.CREATE_LIST:
            let add_list = state.lists
            add_list.unshift(action.payload.list)
            return {...state, ...{lists: add_list}}

        case type.DELETE_LIST:
            ////
            return state

        case type.GET_LISTS:
            return {...state, ...action.payload}

        case type.GET_TREND:
            return {...state, ...action.payload}

        case type.SEARCH:
            return {...state, ...action.payload}

        case type.TREND_TWEETS:
        let t_tweets = action.payload.tagTweets.tweets
            return {...state, ...{tagTweets: t_tweets}}

        case type.ADD_TO_LIST:
            let added_list = state.list
            if(action.payload.msg === 'user removed'){
                added_list.users = added_list.users.filter(x=>{ return x._id !== action.data.userId })
            }else{
                added_list.users.push({username: action.data.username , _id: action.data.userId, name: action.data.name, profileImg: action.data.profileImg})
            }
            return {...state, ...{list: added_list}}

        case type.GET_FOLLOWERS:
            return {...state, ...action.payload}

        case type.GET_FOLLOWING:
            return {...state, ...action.payload}

        case type.CREATE_SIGNING_PROFILE:
            let createdSP = state.signingProfiles
            createdSP.push(action.payload.user)
            return {...state, loading: false, error: false}

        case type.CREATE_CONTACT_PROFILE:
            let createdContactUser = action.payload.user
            let createdCP = state.contactProfiles
            let updateCreatedContactUserTweets = state.userTweets
            createdCP.push(createdContactUser)
            updateCreatedContactUserTweets.forEach((item, i) => {
              item.setAuthor(createdContactUser);
            });
            return {...state, ...{user: createdContactUser}, loading: false, error: false}

        case type.GET_SIGNING_PROFILES:
            return {...state, ...action.payload}

        case type.GET_CONTACT_PROFILES:
            return {...state, ...action.payload}

        case type.GET_PAYMENT_SUMMARY:
            return {...state, ...action.payload}

        case type.GET_SENT_PAYMENTS:
            let paymentsSP = state.sentPayments
            let newSP = action.payload.sentPayments
            console.log(newSP);
            newSP.forEach(t => paymentsSP.push(t));
            return {...state, loading: false, error: false}

        case type.CLEAR_SENT_PAYMENTS:
            return {...state, ...{sentPayments: []}}

        case type.GET_CONNECTED_PEERS:
            return {...state, ...action.payload}

        case type.GET_PEERS:
            return {...state, ...action.payload}

        case type.GET_PEER_CONNECTION:
                return {...state, ...action.payload}

        case type.UPDATE_PEER:
            let updatePeer = action.payload.user
            return {...state, ...{peer: updatePeer}, loading: false, error: false}

        case type.SAVE_PEER:
            console.log(action.payload);
            let createdPeer = action.payload.savedPeer
            let createdPeers = state.peers
            createdPeers.push(createdPeer)
            return {...state, ...{peers: createdPeers}, ...{peer: createdPeer}, loading: false, error: false}

        case type.SEARCH_USERS:
            return {...state, ...action.payload}

        case type.WHO_TO_FOLLOW:
            return {...state, ...action.payload}

        case type.GET_CONVERSATIONS:
            return {...state, ...action.payload}
        case type.START_CHAT:
            setTimeout(()=>{action.data.func()},250)
            return {...state, ...action.payload}
        case type.GET_SINGLE_CONVERSATION:
            setTimeout(()=>{action.data.func(action.payload.conversation.messages)},250)
            return {...state, ...action.payload}

        default:
            return state
    }
  }

export { initialState, reducer }
