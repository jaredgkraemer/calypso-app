import sys, csv, sqlite3, json

from flask import Flask, Response, g, request, jsonify, current_app
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("local.db")
        g.db.row_factory = sqlite3.Row

    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/records", methods=["GET", "POST"])
def records():

    db = get_db()
    curs = db.cursor()

    if request.method == "POST":

        f = request.files["csvFile"]
        name = secure_filename(f.filename)
        path = "/usr/src/app/records/" + name
        f.save(path)

        drop_table_query = "DROP TABLE IF EXISTS {0}".format(name[:-4])
        create_table_query = """
            CREATE TABLE IF NOT EXISTS {0} (
                guid text NOT NULL,
                name text NOT NULL,
                date text NOT NULL
            )
        """.format(name[:-4])

        curs.execute(drop_table_query)
        curs.execute(create_table_query)

        reader = csv.reader(open(path, "r"), delimiter=",")

        for row in reader:
            to_db = [str(row[0]), str(row[1]), str(row[2])]
            insert_query = "INSERT INTO {0} (guid, name, date) VALUES (?, ?, ?);".format(name[:-4])
            curs.execute(insert_query, to_db)

        db.commit()
        curs.close()

        return jsonify({"filename": name[:-4]})

    elif request.method == "GET":
        get_tables_query = """
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
        """
        curs.execute(get_tables_query)
        result = [ row[0] for row in curs.fetchall()]
    
        print("GET ALL: ", result, file=sys.stderr)
        curs.close()
        return Response(json.dumps(result), status=200, mimetype="application/json")

@app.route("/records/<name>", methods=["GET"])
def getSingleRecord(name):
    return Response("{'message':'success'}", status=200, mimetype="application/json")
