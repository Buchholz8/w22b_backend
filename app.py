#i start with importing everything i need
from flask import Flask, request, jsonify, make_response
import dbcreds, dbhelpers

app = Flask(__name__)
#first post request will request a username email password and bio it will then call the insert_client_rid and set the results to the client_id that was returned from the procedure
@app.post("/api/client")
def post_client():
    error = dbhelpers.check_endpoint_info(request.json, ["username","email", "password", "image_url", "bio"])
    if(error != None):
        return make_response(jsonify(error), 500)
    results = dbhelpers.run_procedures("CALL insert_client_rid(?,?,?,?,?)", [request.json.get('username'), request.json.get('email'), request.json.get('password'), request.json.get('image_url'), request.json.get('bio')])
    if(type(results) == list):
        return make_response(jsonify({results == "client_id"}), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
#second post will need the username and password this will call the token_handler and this will then use my token and equal my token to the token sent back (this doesnt work and i would like to hear from you on how this actually works)
@app.post("/api/login")
def post_login():
    token = dbhelpers.generate_token()
    error = dbhelpers.check_endpoint_info(request.json, ["username","password"])
    if(error != None):
        return make_response(jsonify(error), 500)
    results = dbhelpers.run_procedures("CALL token_handler(?,?,?)", [request.json.get('username'), request.json.get('password'), token])
    if (type(token) == str):
        return make_response(jsonify({'token': token}), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
#the delete will request args of the token and it will call the delete_token and pass the inserted token in and the procedure will then delete that token
@app.delete("/api/login")
def delete_token():
    user_token_input = str(request.json.get("token"))
    results = dbhelpers.run_procedures("CALL delete_client(?)", [user_token_input])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
#the get request will require the token and it will call the return_user and pass the token in and send the information back and jsonify the results 
@app.get("/api/client")
def get_client():
    user_token_input = request.args.get("token")
    results = dbhelpers.run_procedures("CALL return_user(?)", [user_token_input])
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response(jsonify("sorry, something went wrong"))
#last i do the procedure mdoe app.run
if(dbcreds.production_mode == True):
    print("Runing in production mode")
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in developer mode")
    app.run(debug=True)