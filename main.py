from flask import Flask, render_template, Response, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        print(f"Value {request.form.get('but')}")
    return render_template('index.html')

@app.route("/forward/")
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('index.html', forward_message=forward_message);


app.run(debug=False, port=80)