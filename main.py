from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from RPIClass import Master, Node
from datetime import datetime
from fileClass import Files
from sys import platform
import subprocess as sub
import webbrowser
import threading
import psutil
import json
import time
import os

app = Flask(__name__)

def fileUpload():
    pass

def fileSearcher():
    glo = globals()
    tmp = []
    settings = glo.get("settings")
    for path in os.listdir(scripPath):
        if os.path.isdir(os.path.join(scripPath, path)) and path not in tmp:
            for idx, nameCheck in enumerate(settings["fileNames"]):
                if nameCheck[0] == path:
                    tmp.append(Files(os.path.join(scripPath, path), nameCheck[1]))
                    break
                if len(settings["fileNames"]) is idx + 1:
                    tmp.append(Files(os.path.join(scripPath, path), path))
                    
    glo.update({"pythonScripts": tmp})
    
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
            
            if request.form.get(f"but") == f"update{idx}":
                if not request.form.get(f"fileName{idx}") in [x.name for x in pythonScripts]:
                    pyFile.update_name(request.form.get(f"fileName{idx}"))
                fileSearcher()
                break

            if request.form.get("but") == f"run{idx}":
                if not str(request.form.get(f"mainFile{idx}")) == "None":
                    pyFile.run(request.form.get(f"mainFile{idx}"))
                    break
                
            elif request.form.get("but") == f"stop{idx}":
                pyFile.kill()
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
                    print(folderName)
                    print(request.files.getlist("file[]"))
                    for file in request.files.getlist("file[]"):
                        if not os.path.exists(os.path.join(scripPath, folderName)):
                            os.mkdir(os.path.join(scripPath, folderName))
                        print(os.path.join(app.config['UPLOAD_FOLDER'], folderName, secure_filename(file.filename)))
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], folderName, secure_filename(file.filename)))
                    fileSearcher()
                except Exception as e:
                    print("no files")
                print("Yess")
                break
            
            elif request.form.get("but") == f"edit{idx}":
                webbrowser.open_new_tab(pyFile.url)
                break
            
            elif request.form.get("but") == f"sync":
                print("sync")
                fileSearcher()
                break
                                        
    return render_template('index.html', files=enumerate(pythonScripts), settings=settings, states=updateStates(), log=log)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    
    if request.method == 'POST':
        if request.form.get("but") == f"save":
            pass
    return render_template('settings.html', settings=settings)

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
        except Exception as e:
            print(e)
            input("Press enter to exit")
            exit()
    
    if not os.path.exists(scripPath):
        os.makedirs(scripPath)
    
    states = {"cpu": 0, "ram": 0, "disk": 0, "temp": 0}
    
    pythonScripts = []
        
    log = [["System started", str(datetime.now())]]
    
    fileSearcher()
    
    app.config["UPLOAD_FOLDER"] = scripPath
    
    threading.Thread(target=codeServer).start()
    
    app.run(debug=True, port=8080, host="0.0.0.0") 