import { configureStore } from '@reduxjs/toolkit'

import todosReducer from './features/todos/todosSlice'
import squeakReducer from './features/squeak/squeakSlice'
import filtersReducer from './features/filters/filtersSlice'

const store = configureStore({
  reducer: {
    // Define a top-level state field named `todos`, handled by `todosReducer`
    todos: todosReducer,
    squeak: squeakReducer,
    filters: filtersReducer,
  },
})

export default store
