#!test/bin/python
import uuid
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
import pdb
app = Flask(__name__, static_url_path="")
api = Api(app)

cb = Bucket('couchbase:///task', username = 'prem.saha',password='untrodden123')

task_fields = {
    'text': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.String,
    'time': fields.String
}


class TaskListAPI(Resource):
   
    a = None


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

    def post(self):
        
        store_id = uuid.uuid4().hex
        
        
        a = store_id
        
       
        args = self.reqparse.parse_args()
         
        task = {
            'text': args['text'],
            'user_id': args['user_id'],
            'created_at': args['created_at'],
            'time': args['time'],
        }
        TaskListAPI.response = a 
        cb.upsert(store_id,{'id':store_id,'comn':[task]})
        rv = cb.get(store_id)
        return jsonify(rv.value)
       
  
       
    def put(self):  
        
        sub_id = TaskListAPI.response
      
        args = self.reqparse.parse_args()

        task = {
            'text': args['text'],
            'user_id': args['user_id'],
            'created_at': args['created_at'],
            'time': args['time'],

        }

        cb.mutate_in(sub_id, SD.array_append('comn',task))
       
        return {'task': marshal(task, task_fields,sub_id)}, 201

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')


if __name__ == '__main__':
    app.run(debug=True)