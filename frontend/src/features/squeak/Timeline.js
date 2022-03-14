import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


import {
  fetchTimeline,
  selectTimelineSqueaks,
  selectTimelineSqueaksStatus,
  selectLastTimelineSqueak,
  clearTimeline,
} from '../squeak/squeakSlice'

import store from '../../store'


const Timeline = () => {
  const squeaks = useSelector(selectTimelineSqueaks);
  const loadingStatus = useSelector(selectTimelineSqueaksStatus)
  const lastSqueak = useSelector(selectLastTimelineSqueak)
  const dispatch = useDispatch()

  useEffect(() => {
      window.scrollTo(0, 0)
      // actions.getSqueaks({lastSqueak: null})
      // reloadSqueaks();
      console.log('fetchTodos');
      dispatch(clearTimeline());
      dispatch(fetchTimeline(null));
  }, [])


  const renderedListItems = squeaks.map((squeak) => {
    return <SqueakCard squeak={squeak} key={squeak.getSqueakHash()} id={squeak.getSqueakHash()} user={squeak.getAuthor()} />
  })

  return <>
          <ul className="todo-list">{renderedListItems}</ul>

          {loadingStatus === 'loading' ?
          <div className="todo-list">
            <Loader />
          </div>
          :
          <div onClick={() => dispatch(fetchTimeline(lastSqueak))} className='squeak-btn-side squeak-btn-active'>
            LOAD MORE
          </div>
          }

         </>
}

export default Timeline
