import React, {useEffect, useContext} from 'react'
import { StoreContext } from '../../store/store'
import {withRouter, Link} from 'react-router-dom'
import './style.scss'
import moment from 'moment'
import {useMediaQuery} from 'react-responsive'
import Chat from '../ChatPage'

const Messages = (props) => {
    const { state, actions } = useContext(StoreContext)
    const {account, conversations} = state
    const path = props.history.location.pathname

    useEffect(() => {
        actions.getConversations()
        document.getElementsByTagName("body")[0].style.cssText = "position:fixed; overflow-y: scroll;"
    },[path])

    useEffect( () => () => document.getElementsByTagName("body")[0].style.cssText = "", [] )

    const isTabletOrMobile = useMediaQuery({ query: '(max-width: 888px)' })
    return(
        <React.Fragment>
        {isTabletOrMobile && path !== '/messages' && account ?
        <Chat res={true}/> :
        <div className="messages-wrapper">
            <div className="messages-header-wrapper">
                Messages
            </div>
            <div className="messages-body">
            </div>
        </div>}
        </React.Fragment>
    )
}

export default withRouter(Messages)
