from flask import Flask
from flask_restful import Resource, Api, reqparse, abort 

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

TODOS = {
    1: {'task': 'build an API'},
    2: {'task': '?????'},
    3: {'task': 'profit'},
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def add_todo_id(todo_id):
    args = parser.parse_args()
    todo = {'task': args['task']}
    TODOS[todo_id] = todo
    return todo

class Todo(Resource):
    """Show a single todo item and lets you delete them"""
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204
    def put(self, todo_id):
        return add_todo_id(todo_id), 201

class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""
    def get(self):
        return TODOS
    def post(self):
        todo_id = max(TODOS.keys()) + 1
        return add_todo_id(todo_id), 201


api.add_resource(Todo, "/todos/<int:todo_id>")
api.add_resource(TodoList, "/todos")




if __name__ == "__main__":
    app.run(debug=True)