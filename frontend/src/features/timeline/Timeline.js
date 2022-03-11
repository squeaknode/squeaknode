import React, { useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'


import {
  clearTimeline,
  selectTimelineSqueaks,
  selectTimelineSqueakIds,
  selectLastTimelineSqueak,
} from './timelineSlice'

import { fetchTimeline } from './timelineSlice'
import store from '../../store'


const Timeline = () => {
  const squeakIds = useSelector(selectTimelineSqueakIds)
  const squeaks = useSelector(selectTimelineSqueaks);
  const loadingStatus = useSelector((state) => state.timeline.status)
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


  console.log(squeakIds);

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
