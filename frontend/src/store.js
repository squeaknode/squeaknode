import { configureStore } from '@reduxjs/toolkit'

import timelineReducer from './features/timeline/timelineSlice'
import squeakReducer from './features/squeak/squeakSlice'
import filtersReducer from './features/filters/filtersSlice'

const store = configureStore({
  reducer: {
    // Define a top-level state field named `todos`, handled by `todosReducer`
    timeline: timelineReducer,
    squeak: squeakReducer,
    filters: filtersReducer,
  },
})

export default store
