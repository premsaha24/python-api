from flask import Flask
from flask import jsonify
import couchbase.subdocument as SD
from couchbase.bucket import Bucket

app = Flask(__name__)

# Connecting to DB          

cb = Bucket('couchbase:///test', username = 'prem.saha',password='untrodden123')

# Creating DB
cb.upsert('55',{'55':[{'{title': fields.String, 'description': fields.String, 'done': fields.Boolean,'uri': fields.Url('task')}]}) # only run once

# updating DB 
cb.mutate_in('55', SD.array_append('55',{'text':'text','user_id':'user_id','created_at':'created_at','time':'time'}))


if __name__ == '__main__':
    app.run(debug=True)