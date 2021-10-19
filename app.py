from flask import Flask,render_template,request,send_file
from flask_wtf.csrf import CSRFProtect

from pywhatkit import text_to_handwriting
from uuid import uuid4
from os import remove

app = Flask(__name__,template_folder="templates",static_folder="static")
app.secret_key = uuid4().hex

CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert',methods=['POST'])
def convert():
    text_to_handwriting(request.form["text"],save_to="static/" + request.form["filename"])
    return {
        "status":200,
        "message":"success",
        "link":"static/" + request.form["filename"]
    }

@app.route('/delete',methods=['POST'])
def delete():    
    if request.form["link"] == "":
        return {
            "status":400,
            "message":"No file name provided"
        }
    try:
        remove(request.form["link"])
        return {
            "status":200,
            "message":"success"
        }
    except:
        return {
            "status":400,
            "message":"File not found"
        }

@app.route('/download',methods=['POST'])
def download():
    return send_file(request.form["link"])

if __name__ == '__main__':
    app.run()