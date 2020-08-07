from csv_service import app
from flask_cors import CORS

# allows cross origin requests
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.run(host='0.0.0.0', port=80, debug=True)
