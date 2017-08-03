#!test/bin/python
import uuid
import json
import datetime
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
from couchbase.n1ql import N1QLQuery
import pdb

app = Flask(__name__, static_url_path="")
api = Api(app)
cb = Bucket('couchbase:///task', username = 'prem.saha',password='untrodden123')
now = datetime.datetime.now()
# cluster = CouchbaseCluster.create('couchbase://localhost')

task_fields = {
    'title': fields.String,
    'description': fields.String,
}

class TaskListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
     
        super(TaskListAPI, self).__init__()
    
    def get(self):
        documents = [] 
        for row in cb.n1ql_query('SELECT * FROM task'):
            documents.append(row)

        return documents

    def post(self):
        
        store_id = uuid.uuid4().hex
        # a = store_id
        args = self.reqparse.parse_args()
        list1 = now.strftime("%Y-%m-%d ")
        list2 = now.strftime("%H:%M")
         
        task = {

            'title': args['title'],
            'description': args['description'],
            'created_at': list1,
            'time': list2,

        }

        # TaskListAPI.response = a 
        cb.upsert(store_id,{'id':store_id,'comn':[task]})
        rv = cb.get(store_id)
        return jsonify(rv.value)
              


class TaskAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')

    def get(self, todo_id):
        rv = cb.get(todo_id)
        return jsonify(rv.value)

    def put(self, todo_id): 
        args = self.reqparse.parse_args()
        
        list1 = now.strftime("%Y-%m-%d")
        list2 = now.strftime("%H:%M")
        
        task = {
            'title': args['title'],
            'description': args['description'],
            'created_at': list1,
            'time': list2,

        }

        cb.mutate_in(todo_id, SD.array_append('comn',task))
        rv = cb.get(todo_id)
        return jsonify(rv.value)
        

    def delete(self,todo_id):
        if todo_id == 0:
            abort(404)
        doc = cb.remove(todo_id);
        return {'result': True}

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

