from flask import Flask, render_template, request
from fileClass import Files
from RPIClass import Master, Node
from sys import platform
import json
import os

app = Flask(__name__)

def fileSearcher():
    glo = globals()
    tmp = [path for path in os.listdir(scripPath) if os.path.isdir(os.path.join(scripPath, path))]
    tmp = [Files(os.path.join(scripPath, path), path) for path in tmp]
    glo.update({"pythonScripts": tmp})
    
def updateSetings():
     pass

@app.route('/', methods=['GET', 'POST'])
def index():
    glo = globals()
    states = {"cpu": 0, "ram": 0, "disk": 0, "temp": 0}
    if request.method == 'POST':                
        for idx, pyFile in enumerate(pythonScripts):
            if request.form.get("but") == f"run{idx}":
                if not str(request.form.get(f"mainFile{idx}")) == "None":
                    pyFile.run(request.form.get(f"mainFile{idx}"))
                
            elif request.form.get("but") == f"stop{idx}":
                pyFile.kill()
                                        
    return render_template('index.html', files=enumerate(pythonScripts), settings=settings, states=states)


if __name__ == '__main__':

    match platform:
        case "linux" | "linux2":
            scripPath = r"/home/pi/code/serverFiles"
        case "win32":
            if not os.path.exists(f"{os.environ['USERPROFILE']}\\Documents\\serverFiles"):
                os.makedirs(f"{os.environ['USERPROFILE']}\\Documents\\serverFiles")
            scripPath = f"{os.environ['USERPROFILE']}\\Documents\\serverFiles"
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
    
    pythonScripts = []
    
    fileSearcher()
    
    app.run(debug=True, port=8080, host="0.0.0.0") 