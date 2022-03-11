import React from 'react'
import { useSelector, useDispatch } from 'react-redux'

import { ReactComponent as TimesSolid } from './times-solid.svg'

import { availableColors, capitalize } from '../filters/colors'
import {
  selectTodoById,
} from './todosSlice'

// Destructure `props.id`, since we just need the ID value
const TodoListItem = ({ id }) => {
  // Call our `selectTodoById` with the state _and_ the ID value
  const todo = useSelector((state) => selectTodoById(state, id))
  // const { text, completed, color } = todo

  console.log(id);
  console.log(todo);

  const dispatch = useDispatch()

  const colorOptions = availableColors.map((c) => (
    <option key={c} value={c}>
      {capitalize(c)}
    </option>
  ))

  return (
    <li>
      <div className="view">
        <div className="segment label">
          <div className="todo-text">{todo && todo.getContentStr()}</div>
        </div>
        <div className="segment buttons">
          <button className="destroy" onClick={() => console.log('Delete.')}>
            <TimesSolid />
          </button>
        </div>
      </div>
    </li>
  )
}

export default TodoListItem
