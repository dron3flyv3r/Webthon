from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import spur
import os

def getCpuTemp():
    nodes = [['192.168.1.155', 'pi', 'Everest1', 'Master'],['192.168.1.62', 'pi', 'Everest1', 'Node1']]
    cmd = ['cat', '/sys/class/thermal/thermal_zone0/temp']
    cpuTemp = []
    
    for node in nodes:
        shell = spur.SshShell(hostname=node[0], username=node[1], password=node[2])
        tmp = shell.run(cmd).output.decode()
        cpuTemp.append(f"{node[3]}: {tmp[0:2]}.{tmp[2:4]}")
    
    return cpuTemp

app = Flask(__name__)

todoList = []
uploadState = "hidden"

if os.path.exists("todo.txt"):
    with open("todo.txt", "r") as f:
        todo = f.read()
        todoList = todo.split("\n")
        todoList.remove("")

@app.route('/', methods=['GET', 'POST'])
def index():
    glo = globals()
    cpuTemp = getCpuTemp()
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
                global uploadState
                if glo["uploadState"] == "hidden":
                    uploadState = "visible"
                else:
                    uploadState = "hidden"
                                        
    return render_template('drop.html', x=todoList, cpu=cpuTemp, visibility=glo["uploadState"])

app.config.update(
    UPLOADED_PATH= r"upload",
    DROPZONE_MAX_FILE_SIZE = 4096,
    DROPZONE_TIMEOUT = 5*60*1000)

dropzone = Dropzone(app)
@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        global uploadState 
        uploadState = "hidden"
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('drop.html')

app.run(debug=True, port=8080, host="0.0.0.0") 