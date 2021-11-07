
from backend.main.models import TODOSes
from flask import jsonify, request
from flask import Blueprint
from backend.main import db

apps = Blueprint("apps", __name__)

@apps.route('/')
def one():
    return "one"


@apps.route('/check', methods=['GET'])
def check():
    return jsonify('Проверка передачи из vue')


@apps.route('/todos', methods=['GET', 'POST'])
def all_todos():
    response_object = {'status': 'success'}
    todo = TODOSes.query.all()
    if request.method == 'POST':
        post_data = request.get_json()
        todo = TODOSes(content=post_data.get('content'), boss=post_data.get('boss'), important=post_data.get('important'))
        db.session.add(todo)
        db.session.commit()

        response_object['message'] = 'Задача добавлена'
    else:
        todos = []
        for item in todo:
            todos.append(item.get_dict())
            response_object['todos'] = todos
    return jsonify(response_object)


@apps.route('/todos/<todo_id>', methods=['PUT', 'DELETE'])
def single_todo(todo_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        todo_object = TODOSes.query.get(todo_id)
        todo_object.content = post_data.get("content")
        todo_object.boss = post_data.get("boss")
        todo_object.important = post_data.get("important")
        current_session = db.session.object_session(todo_object)
        current_session.add(todo_object) # чтоб в той же сессии все делать
        #db.session.add(todo_object)
        current_session.commit()

        response_object['message'] = 'Задача обновлена'
    if request.method == 'DELETE':
        todo_object = TODOSes.query.get(todo_id)
        current_session = db.session.object_session(todo_object)
        current_session.delete(todo_object)  # чтоб в той же сессии все делать
        # db.session.add(todo_object)
        current_session.commit()

        response_object['message'] = 'Задача удалена'
    return jsonify(response_object)
