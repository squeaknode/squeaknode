import React from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import TodoListItem from './TodoListItem'

import { selectTodoIds, selectLastTodo } from './todosSlice'

import { fetchTodos } from './todosSlice'
import store from '../../store'


const TodoList = () => {
  const todoIds = useSelector(selectTodoIds)
  const loadingStatus = useSelector((state) => state.todos.status)
  const lastSqueak = useSelector(selectLastTodo)
  const dispatch = useDispatch()


  console.log(todoIds);

  if (loadingStatus === 'loading') {
    return (
      <div className="todo-list">
        <div className="loader" />
      </div>
    )
  }

  const renderedListItems = todoIds.map((todoId) => {
    return <TodoListItem key={todoId} id={todoId} />
  })

  return <>
          <ul className="todo-list">{renderedListItems}</ul>
          <button onClick={() => dispatch(fetchTodos(lastSqueak))}>
            LOAD MORE
          </button>
         </>
}

export default TodoList
