from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from datetime import datetime
from fileClass import Files
from RPIClass import Node, Win
from sys import platform
import subprocess as sub
from api import api
import webbrowser
import threading
import argparse
import psutil
import json
import time
import os

app = Flask(__name__, static_url_path="/static", template_folder="templates")
app.register_blueprint(api, url_prefix="/api")

def fileSearcher():
    glo = globals()
    tmp = []
    settings = glo.get("settings")
    for path in os.listdir(scripPath):  
        tmp.append(Files(os.path.join(scripPath, path), path))
    tmp.sort(key=lambda x: os.path.getctime(x.path), reverse=True)
    glo.update({"pythonScripts": tmp})
    
def nodeScarcher():
    glo = globals()
    settings = glo.get("settings")
    tmp = []
    for node in settings["Nodes"]:
        if node.type == "RaspberryPi":
            tmp.append(Node(node.hostName, node.ip, node.password, node.name, node.port))
        elif node.type == "Windows":
            tmp.append(Win(node.hostName, node.ip, node.password, node.name, node.port))
    glo.update({"servers": tmp})
    
def updateSetings(setting, value):
    with open("settings.json", "w+") as file:
        settings = json.load(file)
    settings[setting] = value
 
def codeServer():
    glo = globals()
    #code-server serve-local --port 8080 --host 0.0.0.0 --accept-server-license-terms            
    os.system("code-server serve-local --port 8000") 
    
def updateStates():
    states["cpu"] = psutil.cpu_percent()
    states["ram"] = psutil.virtual_memory().percent
    states["temp"] = round(psutil.sensors_temperatures()["cpu_thermal"][0].current, 2)
    states["disk"] = psutil.disk_usage("/").percent
    return states

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':                
        for idx, pyFile in enumerate(pythonScripts):
            """ scriptsNames = [x.name for x in pythonScripts]
            for file in request.form.getlist("fileName"):
                if not file in scriptsNames:
                    pyFile.update_name(secure_filename(str(request.form.get(f"fileName{idx}"))))
                    fileSearcher()
                    break """

            if request.form.get("but") == f"run{idx}":
                if not str(request.form.get(f"mainFile{idx}")) == "None":
                    pyFile.run(str(request.form.get(f"mainFile{idx}")))
                    break
                
            elif request.form.get("but") == f"stop{idx}":
                pyFile.kill()
                break
            
            elif request.form.get("but") == f"newFile":
                newFileName = os.path.join(scripPath, f"NewProject{0 if 'NewProject0' not in [names.name for names in pythonScripts] else -1}")
                os.mkdir(os.path.join(scripPath, newFileName))
                pythonScripts.append(Files(os.path.join(scripPath, newFileName), newFileName))
                with open(os.path.join(newFileName, "main.py"), "w") as file:
                    file.write("print('Hello World')")
                fileSearcher()
                break
            
            elif request.form.get("but") == f"upload":
                try:
                    folderName = "NewScript"
                    idx = 0
                    while True:
                        if not os.path.exists(os.path.join(scripPath, f"{folderName}{idx}")):
                            if idx == 0:
                                folderName = folderName
                                break
                            folderName = f"{folderName}{idx}"
                            break
                        idx += 1
                    for file in request.files.getlist("file[]"):
                        if not os.path.exists(os.path.join(scripPath, folderName)):
                            os.mkdir(os.path.join(scripPath, folderName))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], folderName, secure_filename(file.filename)))
                    fileSearcher()
                except Exception as e:
                    print("no files")
                print("Yess")
                break
            
            elif request.form.get("but") == f"update{idx}":
                print(request.form)
                pyFile.update_name(secure_filename(str(request.form.get(f"fileName{idx}"))))
                fileSearcher()
                break
            
            elif request.form.get("but") == f"edit{idx}":
                webbrowser.open_new_tab(pyFile.url)
                break
            
            elif request.form.get("but") == f"sync":
                fileSearcher()
                break
                                        
    return render_template('index.html', files=enumerate(pythonScripts), settings=settings, states=updateStates(), log=log)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if request.form.get("but") == f"save":
            with open("settings.json", "w") as file:
                settings["clusterName"] = request.form.get("serverName")
                json.dump(settings, file, indent=4)
                
    return render_template('settings.html', settings=settings)


@app.route('/nodes', methods=['GET', 'POST'])
def nodes():
    if request.method == 'POST':
        for idx in range(len(settings['Nodes'])):
            if request.form.get(f"but") == f"save{idx}":
                with open("settings.json", "w") as file:
                    settings['Nodes'][idx]['name'] = request.form.get(f"name{idx}")
                    settings['Nodes'][idx]['ip'] = request.form.get(f"ip{idx}")
                    settings['Nodes'][idx]['port'] = request.form.get(f"port{idx}")
                    settings['Nodes'][idx]['hostName'] = request.form.get(f"hostName{idx}")
                    settings['Nodes'][idx]['password'] = request.form.get(f"password{idx}")
                    settings['Nodes'][idx]['type'] = request.form.get(f"type{idx}")
                    json.dump(settings, file, indent=4)
                break
                    
            elif request.form.get(f"but") == f"delete{idx}":
                with open("settings.json", "w") as file:
                    settings['Nodes'].pop(idx)
                    json.dump(settings, file, indent=4)
                break
            
            elif request.form.get(f"but") == f"ssh{idx}":
                
                break
        else:         
            if request.form.get(f"but") == f"add":
                with open("settings.json", "w") as file:
                    settings['Nodes'].append({"name": request.form.get("newName"), "ip": request.form.get("newIp"), "port": request.form.get("newPort"), "hostName": request.form.get("newHostName"), "password": request.form.get("newPassword"), "type" : request.form.get("newType")})
                    json.dump(settings, file, indent=4)
            
            
    return render_template('nodes.html', files=enumerate(pythonScripts), settings=enumerate(settings["Nodes"]), baseSettings=settings)


@app.route('/scripts', methods=['GET', 'POST'])
def scripts():
    if request.method == 'PORT':
        for idx, file in enumerate(pythonScripts):
            if request.form.get(f"but") == f"delete{idx}":
                file.remove()
                pythonScripts.pop(idx)
                fileSearcher()
                break
            
            elif request.form.get(f"but") == f"edit{idx}":
                webbrowser.open_new_tab(file.url)
                break
            
            elif request.form.get(f"but") == f"run{idx}":
                file.run()
                break
            
            elif request.form.get(f"but") == f"update{idx}":
                file.update_name(secure_filename(str(request.form.get(f"fileName{idx}"))))
                fileSearcher()
                break
            
    return render_template('scripts.html', files=enumerate(pythonScripts), settings=settings["Nodes"])



if __name__ == '__main__':
    match platform:
        case "linux" | "linux2":
            scripPath = r"/home/pi/code/serverFiles"
            
        case _:
            input("Platform not supported press enter to exit")
            exit()
    try:
        settings = json.load(open("settings.json", "r"))
    except FileNotFoundError:
        try:
            settings = json.load(open("defult.json", "r")) 
            json.dump(settings, open("settings.json", "w"), indent=4)
        except Exception as e:
            print(e)
            input("Press enter to exit")
            exit()
            
    parser = argparse.ArgumentParser(description='Some simple server controlles for the raspberry pi')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Port to run the server on')
    parser.add_argument('-d', '--debug', type=bool, default=True, help='Run the server in debug mode')
    args = parser.parse_args()
    
    
    if not os.path.exists(scripPath):
        os.makedirs(scripPath)
    
    states = {"cpu": 0, "ram": 0, "disk": 0, "temp": 0}
    
    pythonScripts = []
    #servers = []
        
    log = [["System started", str(datetime.now())]]
    
    fileSearcher()
    
    #nodeScarcher()
    
    app.config["UPLOAD_FOLDER"] = scripPath
    
    #threading.Thread(target=codeServer).start()
    
    app.run(debug=args.debug, port=args.port, host="0.0.0.0") 