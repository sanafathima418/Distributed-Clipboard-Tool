import cryptography
import jwt
import time
import psycopg2
import os
import hashlib

ISSUER = 'sample-auth-server'
LIFE_SPAN = 1800

with open('private.pem', 'rb') as f:
  private_key = f.read()

conn = ""
cur = ""

postgresHost = os.getenv("POSTGRES_HOST") or "localhost"

def create_table():
  global conn
  global cur
  conn = psycopg2.connect(database = "postgres", user = "admin", password = "abc123", host = postgresHost, port = "5432")
  print ("Opened database successfully")
  cur = conn.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS USERS
      (USERID TEXT PRIMARY KEY     NOT NULL,
      PASSWORD           TEXT    NOT NULL);''')
  print ("Table created successfully")

def getmd5Password(password):
    encodedPassword = str.encode(password)
    result = hashlib.md5(encodedPassword)
    return result.hexdigest()


def create_new_user(username, password):
  md5Password = getmd5Password(password)
  print ("Record with " + username + " created successfully")
  cur.execute("INSERT INTO USERS (USERID, PASSWORD) VALUES (\'" + username  + "\',\'"  +  md5Password + "\')");
  conn.commit()


def authenticate_user_credentials(username, password):
  cur.execute("SELECT USERID, PASSWORD  from USERS WHERE USERID = "+ "\'" + username + "\'")
  rows = cur.fetchall()
  if not rows:
    create_new_user(username, password)
    return True
  for row in rows:
    md5Password = getmd5Password(password)
    if md5Password == row[1]:
      print("Authenticated successfully")
      return True
    else:
      return False

def generate_access_token(username):
  payload = {
    "username": username,
    "iss": ISSUER,
    "exp": time.time() + LIFE_SPAN,
  }

  access_token = jwt.encode(payload, private_key, algorithm = 'RS256')

  return access_token.decode()
