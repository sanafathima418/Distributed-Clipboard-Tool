##
from flask import Flask, request, Response, jsonify
from auth import *
import platform
import io, os, sys
import pika, redis
import hashlib, requests
import json
import jsonpickle
import platform
import json
import ssl
import logging 
from authenticator import *
  
##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
redisDB = redis.Redis(host=redisHost, port=6379, db=1)
print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

infoKey = f"{platform.node()}.rest.info"
debugKey = f"{platform.node()}.rest.debug"
workerKey = "task"

# Initialize the Flask application
app = Flask(__name__)

@app.before_request
def before_request():
    if request.endpoint != 'auth':
        # Checks if the access token is present and valid. 
        auth_header = request.headers.get('Authorization')
        if 'Bearer' not in auth_header:
          return json.dumps({
            'error': 'Access token does not exist.'
          }), 400

        access_token = auth_header[7:]

        if access_token and verify_access_token(access_token):
          pass
        else:
          return json.dumps({
            'error': 'Access token is invalid.'
          }), 400

# route http posts to this method
@app.route('/apiv1/copy', methods=['POST'])
def copyData():
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='topic')

    def log_debug(message, key=debugKey):
        channel.basic_publish(
            exchange='logs', routing_key=key, body=message)

    auth_header = request.headers.get('Authorization')
    access_token = auth_header[7:]
    username = get_user_name(access_token)
    jsonPayload = {}
    r = request
    jsonData = json.loads(r.data)
    redisDB.set(username, jsonData['copy'])
    debug_str = "User: " + username + " Pushed encrypted Data to DB: " + jsonData['copy']
    log_debug(debug_str)
    connection.close()

    return Response(response=jsonPayload, status=200, mimetype="application/json")

@app.route('/apiv1/paste', methods=['GET'])
def pasteData():

    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='topic')

    def log_debug(message, key=debugKey):
        channel.basic_publish(
            exchange='logs', routing_key=key, body=message)

    jsonPayload = {}
    auth_header = request.headers.get('Authorization')
    access_token = auth_header[7:]
    username = get_user_name(access_token)
    encryptedData = redisDB.get(username)
    jsonPayload["paste"] = encryptedData.decode("utf-8")
    response = json.dumps(jsonPayload, indent=4, sort_keys=True)

    debug_str = "User: " + username + " requested clipboard data from DB: " + encryptedData.decode("utf-8")
    log_debug(debug_str)
    connection.close()

    return Response(response=response, status=200, mimetype="application/json")
    

@app.route('/auth', methods = ['POST'])
def auth():
  # Issues access token
  username = request.form.get('username')
  password = request.form.get('password')

  if None in [username, password]:
    return json.dumps({
      "error": "invalid_request"
    }), 400
  
  if not authenticate_user_credentials(username, password):
    return json.dumps({
      "error": "access_denied"
    }), 401

  access_token = generate_access_token(username)
  response = json.dumps({ 
    "access_token": access_token,
    "token_type": "JWT",
    "expires_in": LIFE_SPAN
  })
  return Response(response=response, status=200, mimetype="application/json")



if __name__ == '__main__':
  create_table()
  # start flask app
  app.run(host="0.0.0.0", port=6000)




