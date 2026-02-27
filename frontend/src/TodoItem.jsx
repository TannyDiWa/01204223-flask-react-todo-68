import React from 'react';

// รับ props ผ่านการทำ Destructuring ในวงเล็บ
const TodoItem = ({ todo, toggleDone, deleteTodo, addNewComment }) => {
  return (
    <li className="todo-item-container">
      <span className={todo.done ? "done" : ""}>
        {todo.title}
      </span>
      
      <div className="actions">
        <button onClick={() => toggleDone(todo.id)}>Toggle</button>
        <button onClick={() => deleteTodo(todo.id)}>❌</button>
      </div>

      {/* ส่วนแสดงรายการ Comments */}
      {todo.comments && todo.comments.length > 0 && (
        <ul className="comment-list">
          {todo.comments.map(comment => (
            <li key={comment.id} className="comment-text">
              {comment.message}
            </li>
          ))}
        </ul>
      )}

      {/* ส่วนฟอร์มสำหรับเพิ่ม Comment ใหม่ */}
      <div className="new-comment-forms">
        <form onSubmit={(e) => {
          e.preventDefault();
          const input = e.target.elements.comment;
          addNewComment(todo.id, input.value);
          input.value = ""; // ล้างค่าในช่องกรอกหลังกดส่ง
        }}>
          <input 
            name="comment" 
            type="text" 
            placeholder="Write a comment..." 
            required 
          />
          <button type="submit">Add Comment</button>
        </form>
      </div>
    </li>
  );
};

export default TodoItem;