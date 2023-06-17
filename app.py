from flask import Flask, request, jsonify, make_response
import dbcreds, dbhelpers

app = Flask(__name__)

@app.post("/api/client")
def post_client():
    error = dbhelpers.check_endpoint_info(request.json, ["username","email", "password", "image_url"])
    if(error != None):
        return make_response(jsonify(error), 500)
    results = dbhelpers.run_procedures("CALL insert_client_rid(?,?,?,?)", [request.json.get('username'), request.json.get('email'), request.json.get('password'), request.json.get('image_url')])
    if(type(results) == list):
        return make_response(jsonify(error), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
@app.post("/api/login")
def post_login():
    token = dbhelpers.generate_token
    error = dbhelpers.check_endpoint_info(request.json, ["username","password"])
    if(error != None):
        return make_response(jsonify(error), 500)
    results = dbhelpers.run_procedures("CALL token_handler(?,?)", [request.json.get('username'), request.json.get('password'), token])
    if(type(results) == list):
        return make_response(jsonify({'token': token}), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))

@app.delete("/api/login")
def delete_token():
    user_token_input = int(request.args.get("token"))
    results = dbhelpers.run_procedures("CALL delete_client(?)", [user_token_input])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
    
@app.get("/api/client")
def get_client():
    results = dbhelpers.run_procedures("CALL return_user()", [])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
    
if(dbcreds.production_mode == True):
    print("Runing in production mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in developer mode")
    app.run(debug=True)