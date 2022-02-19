import React , { useEffect, useContext } from 'react'
import './style.scss'
import {  withRouter, Link } from 'react-router-dom'
import { StoreContext } from '../../store/store'
import Loader from '../Loader'


const Feed = (props) => {

const { state, actions } = useContext(StoreContext)

const {account, trends, suggestions, session} = state
// const userParam = props.match.params.username

useEffect(() => {
    actions.getTrend()
    if(session){
        actions.whoToFollow()
    }
}, [])

const goToUser = (id) => {
    props.history.push(`/profile/${id}`)
}

const followUser = (e, id) => {
    e.stopPropagation()
    actions.followUser(id)
}


return(
    <div className="feed-wrapper">
        <div className="feed-trending-card">
            <h3 className="feed-card-header">Trending</h3>
            {trends.length>0 ? trends.slice(0,3).map((t,i)=>{
                return <div onClick={()=>props.history.push('/explore')} key={t._id} className="feed-card-trend">
                <div>{i+1} · Trending</div>
                <div>{t.content}</div>
                <div>{t.count} Tweets</div>
            </div>
            }) : <Loader/>}
            <div onClick={()=>props.history.push(`/explore`)} className="feed-more">
                Show more
            </div>
        </div>
    </div>
    )
}

export default withRouter(Feed)
