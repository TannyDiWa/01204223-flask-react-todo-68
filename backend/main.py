from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
# Import db และ class ต่างๆ จากไฟล์ models.py
from models import db, TodoItem, Comment

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

# เชื่อม db เข้ากับ app (แก้อาการ RuntimeError)
db.init_app(app)
migrate = Migrate(app, db)

# สร้าง Table และข้อมูลเริ่มต้น
with app.app_context():
    db.create_all()  # มั่นใจว่า table ถูกสร้าง
    if TodoItem.query.count() == 0:
        db.session.add(TodoItem(title='Learn Flask'))
        db.session.add(TodoItem(title='Build a Flask App'))
        db.session.commit()

@app.route('/api/todos/', methods=['GET'])
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos/', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = TodoItem(title=data['title'], done=data.get('done', False))
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
def toggle_todo(id):
    todo = TodoItem.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/', methods=['DELETE'])
def delete_todo(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)