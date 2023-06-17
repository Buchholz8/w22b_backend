from flask import Flask, request, jsonify, make_response
import dbcreds, dbhelpers

app = Flask(__name__)



if(dbcreds.production_mode == True):
    print("Runing in production mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in developer mode")
    app.run(debug=True)