# Leave this empty
from flask import Flask, request, send_from_directory
app = Flask(__name__,
    static_url_path='', 
    static_folder='web')


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello, World!"
