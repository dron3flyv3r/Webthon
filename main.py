from subprocess import check_output
from flask import Flask, render_template, Response, request, redirect, url_for
from flask_dropzone import Dropzone
import os

def getCpuTemp():
    cpu = check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']).decode("utf-8") 
    cpu = float(cpu) / 1000
    return float(f"{cpu:.2f}")

app = Flask(__name__)

todoList = []
visUp = "hidden"

if os.path.exists("todo.txt"):
    with open("todo.txt", "r") as f:
        todo = f.read()
        todoList = todo.split("\n")
        todoList.remove("")

@app.route('/', methods=['GET', 'POST'])
def index():
    glo = globals()
    if request.method == 'POST':
        match request.form.get("but"):
            
            case "addBut":
                for tmp in request.form.get('sub').split(","):
                    if tmp != "":
                        todoList.append(tmp)

            case "delete":
                for idx in range(len(todoList), -1, -1):
                    if request.form.get(f"check{idx}"):
                        todoList.pop(idx)

            case "clear":
                todoList.clear()

            case "save":
                    with open("todo.txt", "w") as f:
                        for item in todoList:
                            f.write(item + "\n")

            case "load":
                todoList.clear()
                with open("todo.txt", "r") as f:
                    for line in f:
                        todoList.append(line.strip())
            
            case "upload":
                global visUp
                if glo["visUp"] == "hidden":
                    visUp = "visible"
                else:
                    visUp = "hidden"
    
    return render_template('index.html', x=todoList, cpu=getCpuTemp(), visibility=glo["visUp"])



app.config.update(
    UPLOADED_PATH= r"upload",
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000)

dropzone = Dropzone(app)
@app.route('/test',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('drop.html')

app.run(debug=True, port=8080, host="0.0.0.0") 