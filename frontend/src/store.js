import { configureStore } from '@reduxjs/toolkit'

import timelineReducer from './features/timeline/timelineSlice'
import squeakReducer from './features/squeak/squeakSlice'

const store = configureStore({
  reducer: {
    // Define a top-level state field named `todos`, handled by `todosReducer`
    timeline: timelineReducer,
    squeak: squeakReducer,
  },
})

export default store
