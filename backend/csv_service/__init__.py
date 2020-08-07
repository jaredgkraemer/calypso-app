import shelve
import werkzeug
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("local.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class Csv(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        csv_list = []

        for key in keys:
            csv_list.append(shelf[key])

        return {'message': 'Success', 'data': csv_list}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('data', type=werkzeug.datastructures.FileStorage, location='files')

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['name']] = args

        return {'message': 'Saved File', 'name': args['name']}, 201


api.add_resource(Csv, '/csv')
