import sys, csv, sqlite3, json
from datetime import datetime
from flask import Flask, Response, g, request, jsonify, current_app, send_from_directory, abort
from werkzeug.utils import secure_filename

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
    cursor = db.cursor()

    if request.method == "POST":

        f = request.files["csvFile"]
        name = secure_filename(f.filename)
        name_no_extension = name[:-4]
        path = "/usr/src/app/records/" + name
        f.save(path)

        drop_table_query = f"DROP TABLE IF EXISTS {name_no_extension}"
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {name_no_extension} (
                guid text NOT NULL,
                name text NOT NULL,
                first text NOT NULL,
                last text NOT NULL,
                email text NOT NULL,
                value text NOT NULL,
                date DATE NOT NULL,
                year YEAR NOT NULL,
                phone text NOT NULL,
                age int NOT NULL,
                state text,
                street text NOT NULL
            );
        """

        cursor.execute(drop_table_query)
        cursor.execute(create_table_query)

        reader = csv.reader(open(path, "r"), delimiter=",")
        next(reader)
        for row in reader:

            # If state is null make BLANK
            if not row[9]:
                row[9] = "BLANK"

            to_db = [
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6]),
                datetime.strptime(row[6], '%m/%d/%Y').year,
                str(row[7]),
                str(row[8]),
                str(row[9]),
                str(row[10])
            ]
            insert_query = f"""
                INSERT INTO {name_no_extension}
                (guid, name, first, last, email, value, date, year, phone, age, state, street)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, to_db)


        db.commit()
        cursor.close()

        return Response(json.dumps({"filename": name}), status=200, mimetype="application/json")

    elif request.method == "GET":
        get_tables_query = """
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
        """
        cursor.execute(get_tables_query)
        result = [ f"{row[0]}.csv" for row in cursor.fetchall()]
        cursor.close()
        return Response(json.dumps(result), status=200, mimetype="application/json")

@app.route("/records/<string:filename>", methods=["GET"])
def getRecord(filename):
    if request.method == "GET":
        db = get_db()
        cursor = db.cursor()
        get_table_query = f"SELECT * FROM {filename[:-4]} LIMIT 100;"
        cursor.execute(get_table_query)

        result = []

        for row in cursor.fetchall():
            col = []
            for el in row:
                col.append(el)
            result.append(col)

        return Response(json.dumps(result), status=200, mimetype="application/json")

@app.route("/records/year/<string:filename>", methods=["GET"])
def getSameYearStats(filename):
    if request.method == "GET":
        db = get_db()
        cursor = db.cursor()

        get_table_query = f"""
            SELECT year,
            COUNT(year) AS y
            FROM {filename[:-4]}
            GROUP BY year
            ORDER BY y DESC
            LIMIT 5;
        """

        cursor.execute(get_table_query)
        result = [ [row[0], row[1]] for row in cursor.fetchall() ]

        return Response(json.dumps(result), status=200, mimetype="application/json")

@app.route("/download/<string:filename>", methods=["GET"])
def download(filename):
    if request.method == "GET":
        try:
            return send_from_directory('/usr/src/app/records/', filename=filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)
