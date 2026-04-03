from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from flask_migrate import Migrate
# Import db และ class ต่างๆ จากไฟล์ models.py
from models import db, TodoItem, Comment, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import click

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///todos.db')

# เชื่อม db เข้ากับ app (แก้อาการ RuntimeError)
db.init_app(app)
migrate = Migrate(app, db)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fdsjkfjioi2rjshr2345hrsh043j5oij5545')
jwt = JWTManager(app)

# สร้าง Table และข้อมูลเริ่มต้น
# with app.app_context():
#     db.create_all()  # มั่นใจว่า table ถูกสร้าง
#     if TodoItem.query.count() == 0:
#         db.session.add(TodoItem(title='Learn Flask'))
#         db.session.add(TodoItem(title='Build a Flask App'))
#         db.session.commit()

@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)

@app.route('/api/todos/', methods=['GET'])
@jwt_required()
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos/', methods=['POST'])
@jwt_required()
def add_todo():
    data = request.get_json()
    todo = TodoItem(title=data['title'], done=data.get('done', False))
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
@jwt_required()
def toggle_todo(id):
    todo = TodoItem.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

@app.route('/api/todos/<int:todo_id>/comments/', methods=['POST'])
@jwt_required()
def add_comment(todo_id):
    # ตรวจสอบว่ามี Todo นี้อยู่จริงไหม
    todo = TodoItem.query.get_or_404(todo_id)
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400

    # สร้าง Comment ใหม่
    new_comment = Comment(message=data['message'], todo_id=todo.id)
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify(new_comment.to_dict()), 201

@app.route('/api/todos/<int:todo_id>/comments', methods=['POST'])
@jwt_required()
def add_comment_v2(todo_id):
    data = request.get_json()
    todo = TodoItem.query.get_or_404(todo_id)
    comment = Comment(message=data['message'], todo=todo)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@app.cli.command("create-user")
@click.argument("username")
@click.argument("full_name")
@click.argument("password")
def create_user(username, full_name, password):
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo("User already exists.")
        return
    user = User(username=username, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} created successfully.")

if __name__ == '__main__':
    app.run(debug=True)