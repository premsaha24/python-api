#!test/bin/python

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal
from flask.ext.httpauth import HTTPBasicAuth
import couchbase.subdocument as SD
from couchbase.bucket import Bucket

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python123'
#     return None
cb = Bucket('couchbase:///new123', username = 'prem.saha',password='untrodden123')
# tas = (cb.get('56')).value
# tasks = tas['55']

# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'message': 'Unauthorized access'}), 403)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

task_fields = {
    'text': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.String,
    'time': fields.String
    # 'uri': fields.Url('task')
}


class TaskListAPI(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('user_id', type=int, default="",
                                   location='json')
        self.reqparse.add_argument('created_at', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('time', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    # def get(self):
        
    #     return jsonify(tasks)

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'text': args['text'],
            'user_id': args['user_id'],
            'created_at': args['created_at'],
            'time': args['time'],



            
            # 'title': args['title'],
            # 'description': args['description'],
            # 'done': False
        }
        # tasks.append(task)
        # cb.upsert('56',{'55': task})
        cb.mutate_in('56', SD.array_append('55': task))
        return {'task': marshal(task, task_fields)}, 201

# class TaskAPI(Resource):
#     # decorators = [auth.login_required]

#     def __init__(self):
#         self.reqparse = reqparse.RequestParser()
#         self.reqparse.add_argument('title', type=str, location='json')
#         self.reqparse.add_argument('description', type=str, location='json')
#         self.reqparse.add_argument('done', type=bool, location='json')
#         super(TaskAPI, self).__init__()

#     def get(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         return {'task': marshal(task[0], task_fields)}

#     def put(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         task = task[0]
#         args = self.reqparse.parse_args()
#         for k, v in args.items():
#             if v is not None:
#                 task[k] = v
#         return {'task': marshal(task, task_fields)}

#     def delete(self, id):
#         task = [task for task in tasks if task['id'] == id]
#         if len(task) == 0:
#             abort(404)
#         tasks.remove(task[0])
#         return {'result': True}

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
# api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True)