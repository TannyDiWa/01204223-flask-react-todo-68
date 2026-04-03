import { useState, useEffect } from 'react'
import TodoItem from './TodoItem';
import { useAuth } from './context/AuthContext.jsx';
import './App.css'

function TodoList({apiUrl}) {
  const TODOLIST_API_URL = apiUrl;
  const { username, accessToken, logout } = useAuth();

  const [todoList, setTodoList] = useState([]);
  const [newTitle, setNewTitle] = useState("");
  const [newComments, setNewComments] = useState({});

  useEffect(() => {
    fetchTodoList();
  }, [username]);

  async function fetchTodoList() {
    try {
      const response = await fetch(TODOLIST_API_URL, {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      if (!response.ok) { 
        throw new Error('Network error');
      }
      const data = await response.json();
      setTodoList(data);
    } catch (err) {
      setTodoList([]);
      // alert("Failed to fetch todo list from backend. Make sure the backend is running.");
    }
  }

  async function toggleDone(id) {
    const toggle_api_url = `${TODOLIST_API_URL}${id}/toggle/`
    try {
      const response = await fetch(toggle_api_url, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })
      if (response.ok) {
        const updatedTodo = await response.json();
        setTodoList(todoList.map(todo => todo.id === id ? updatedTodo : todo));
      }
    } catch (error) {
      console.error("Error toggling todo:", error);
    }
  }

  async function addNewTodo() {
    try {
      const response = await fetch(TODOLIST_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({ 'title': newTitle }),
      });
      if (response.ok) {
        const newTodo = await response.json();
        setTodoList([...todoList, newTodo]);
        setNewTitle("");
      }
    } catch (error) {
      console.error("Error adding new todo:", error);
    }
  }

  async function deleteTodo(id) {
    const delete_api_url = `${TODOLIST_API_URL}${id}/`
    try {
      const response = await fetch(delete_api_url, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      });
      if (response.ok) {
        setTodoList(todoList.filter(todo => todo.id !== id));
      }
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  }
  
  async function addNewComment(todoId, message) {
    try {
      const url = `${TODOLIST_API_URL}${todoId}/comments/`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({ message: message || "" }),
      });
      if (response.ok) {
        await fetchTodoList();
        setNewComments(prev => ({ ...prev, [todoId]: "" }));
      }
    } catch (error) {
      console.error("Error adding new comment:", error);
    }
  }

  return (
    <>
      <h1>Todo List {username && `for ${username}`}</h1>
      <ul>
        {todoList.map(todo => (
          <TodoItem 
            key={todo.id}
            todo={todo}
            toggleDone={toggleDone}
            deleteTodo={deleteTodo}
            addNewComment={addNewComment}
            newComments={newComments}
            setNewComments={setNewComments}
          />
        ))}
      </ul>
      <div className="add-new-todo">
        New: <input type="text" value={newTitle} onChange={(e) => {setNewTitle(e.target.value)}} />
        <button onClick={() => {addNewTodo()}}>Add Todo</button>
      </div>
      <br/>
      <a href="/about">About</a>
      <br/>
      {username ? (
        <a href="#" onClick={(e) => {e.preventDefault(); logout();}}>Logout</a>
      ) : (
        <a href="/login">Login</a>
      )}
    </>
  )
}

export default TodoList;
