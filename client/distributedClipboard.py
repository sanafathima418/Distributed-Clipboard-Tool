##
from flask import Flask, request, Response, jsonify
from multiprocessing import Process, Value
from pynput import keyboard
import flask
import platform
import io, os, sys
import pika, redis
import hashlib, requests
import json
import jsonpickle
import platform
import pyperclip
import requests
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import zlib
from urllib3.exceptions import InsecureRequestWarning
import getpass

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

_AUTH_PATH = 'https://localhost:6000/auth'
_COPY_PATH = 'https://localhost:6000/apiv1/copy'
_PASTE_PATH = 'https://localhost:6000/apiv1/paste'

AUTH_PATH = 'https://35.222.99.56.nip.io:443/auth'
COPY_PATH = 'https://35.222.99.56.nip.io:443/apiv1/copy'
PASTE_PATH = 'https://35.222.99.56.nip.io:443/apiv1/paste'

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

encryption_password = ""
token = ""

app = Flask(__name__)

def listenToCopy(token, encryption_password):
    while pyperclip.waitForNewPaste():
        text = pyperclip.paste()  # text will have the content of clipboard
        encrypted = encrypt(text, encryption_password)
        sendCopyData(encrypted, token)
        

def sendCopyData(txt, token):
    print('Encrypted clipboard data:', txt.decode("utf-8"))
    dictToSend = {'copy':txt.decode("utf-8")}
    res = requests.post(COPY_PATH, headers = {
        'Authorization': 'Bearer {}'.format(token)
        } ,json=dictToSend, verify=False)
    print('Response from server:',res)
    

def on_activate(token, encryption_password):
    res = requests.get(PASTE_PATH,headers = {
        'Authorization': 'Bearer {}'.format(token)
        }, verify=False)
    jsonData = res.json()
    encrypted = jsonData['paste']
    decrypted = decrypt(encrypted, encryption_password)
    print("Decrypted clipboard data:")
    print(bytes.decode(decrypted))
    pyperclip.copy(bytes.decode(decrypted))
    
def for_canonical(f):
    return lambda k: f(listner.canonical(k))

def listenToKeyboardInput(token, encryption_password):
    global listner
    on_activate_func = lambda : on_activate(token, encryption_password)
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<cmd>+g'), on_activate_func)
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release), suppress=False) as listner:
        listner.join()
 
def encrypt(raw, encryption_password):
    private_key = hashlib.sha256(encryption_password.encode("utf-8")).digest()
    raw = pad(raw).encode("utf-8")
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
def decrypt(enc, encryption_password):
    private_key = hashlib.sha256(encryption_password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

def signIn():
    global token
    global encryption_password
    username = input("Enter Username: ")
    password = getpass.getpass('Password: ')
    encryption_password = password
    r = requests.post(AUTH_PATH, data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        },verify=False)
    
    print('Response from server:',r.status_code)
    if r.status_code != 200:
        return json.dumps({
            'error': 'The authorization server returns an error: \n{}'.format(
                r.text)
                }), 500
    
    contents = json.loads(r.text)
    token = contents.get('access_token')
 
if __name__=='__main__':
    signIn()
    if token != "":
        print("Token received")
    p1 = Process(target = listenToCopy, args=(token, encryption_password,))
    p2 = Process(target = listenToKeyboardInput, args=(token, encryption_password,))
    p1.start()
    p2.start()
    # start flask app
    app.run(host="0.0.0.0", port=4000)