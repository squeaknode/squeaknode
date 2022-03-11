import React from 'react'
import { useSelector } from 'react-redux'
import { useDispatch } from 'react-redux'

import TodoListItem from './TodoListItem'
import SqueakCard from '../../components/SqueakCard'
import Loader from '../../components/Loader'



import { selectTodos, selectTodoIds, selectLastTodo } from './todosSlice'

import { fetchTodos } from './todosSlice'
import store from '../../store'


const TodoList = () => {
  const todoIds = useSelector(selectTodoIds)
  const todos = useSelector(selectTodos);
  const loadingStatus = useSelector((state) => state.todos.status)
  const lastSqueak = useSelector(selectLastTodo)
  const dispatch = useDispatch()


  console.log(todoIds);

  const renderedListItems = todos.map((todo) => {
    return <SqueakCard squeak={todo} key={todo.getSqueakHash()} id={todo.getSqueakHash()} user={todo.getAuthor()} />
  })

  return <>
          <ul className="todo-list">{renderedListItems}</ul>

          {loadingStatus === 'loading' ?
          <div className="todo-list">
            <Loader />
          </div>
          :
          <div onClick={() => dispatch(fetchTodos(lastSqueak))} className='squeak-btn-side squeak-btn-active'>
            LOAD MORE
          </div>
          }

         </>
}

export default TodoList
