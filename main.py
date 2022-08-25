from subprocess import check_output
from flask import Flask, render_template, Response, request, redirect, url_for
import os

def getCpuTemp():
    cpu = check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']).decode("utf-8")
    return float(f"{cpu[:2]}.{cpu[2:]}")

app = Flask(__name__)

todoList = ["Egg", "Milk"]

@app.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        if request.form.get("but") == "addBut":
            for tmp in request.form.get('sub').split(","):
                todoList.append(tmp)
        if request.form.get("but") == "clear":
            todoList.clear()
        if request.form.get("but") == "delete":
            for idx in range(len(todoList), -1, -1):
                if request.form.get(f"check{idx}"):
                    todoList.pop(idx)

    return render_template('index.html', x=todoList, cpu=getCpuTemp())

app.run(debug=True, port=8080, host="0.0.0.0") 