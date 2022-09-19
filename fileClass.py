import subprocess as sub
from time import sleep
from uuid import uuid1
import threading
import time
import os

class Files():
    def __init__(self, path: str, name: str, description: str = None, tag: list[str] = [None, None]):
        self.name = name
        self.folderPath = path
        self.path = path
        self.description = description
        self.tag = tag
        self.running = False
        self.terminal = []
        self.tmp = None
        self.pid = None
        self.ip = None
        self.url = f"http://localhost:8000/?folder={path}"
        self.files = [path for path in os.listdir(self.path) if path.endswith(".py")]
        
    def update_description(self, description: str):
        self.description = description
        return self.description
    
    def update_tag(self, tag: list[str]):
        self.tag = tag
        return self.tag
    
    def update_name(self, name: str):
        self.name = str(name)
        try:
            oldPath = self.path
            newPath = self.folderPath.split("/")
            newPath = "/".join(newPath[:-1]) + "/" + self.name
            os.rename(oldPath, newPath)
            self.path = newPath
            print("Renamed", oldPath, "to", newPath)
        except:
            print("Error: Could not rename file")
    
    def update_ip(self, ip: str):
        self.ip = ip
        
    def update_running(self, running: bool):
        self.running = running
    
    def edit(self):
        #open the file in vscode
        pass
        
    def run(self, fileName: str):    
        if fileName:
            self.path = os.path.join(self.folderPath, fileName)
        else:
            return
        scriptThreat = threading.Thread(self.__run_script(), name=f"thread{str(uuid1())[:8]}")
        pidThreat = threading.Thread(self.__getPid(), name=f"thread{str(uuid1())[:8]}")
        
        scriptThreat.start()
        pidThreat.start()
     
    def kill(self):
        if self.running:
            thread = threading.Thread(self.__kill_script(), name=f"thread{str(uuid1())[:8]}")
            thread.start()
        else:
            self.terminal = ["Script not running"]
    
            
    def getTags(self):
        for tag in self.tag:
            tags += f"{tag} "
        return tags
    
    def remove(self):
        try:
            os.remove(self.path)
        except:
            sub.Popen(["rm", "-rf", self.path], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
        
    def __getPid(self):
        for _ in range(6):
            if not self.tmp == None:
                self.pid = self.tmp.pid
                break
            time.sleep(0.5)
    
    
    def __run_script(self):
        #run the script and add the output to the terminal attribute
        self.terminal.clear()
        try:
            self.running = True

            if os.path.exists(os.path.join(self.folderPath, "requirements.txt")):
                sub.Popen(["pip", "install", "requirements.txt"], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
            
            self.tmp = sub.Popen(["python", self.path], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
            
            while self.tmp.poll() is None:
                self.terminal.append(self.tmp.stdout.readline().replace("\n", ""))
                sleep(0.1)
                
        except Exception as e:
            self.terminal = [f"Error: {e}"]
            
        self.running = False
        
    def __kill_script(self):
        try:
            if self.pid:
                sub.Popen(["kill", self.pid], stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True)
                self.pid = None
                self.running = False
                self.terminal = ["Script stopped"]
        except Exception as e:
            self.running = False
            self.terminal = ["Script not running"]
    
class SSHConection():
    def __init__(self, name: str, host: str):
            self.name = name
            self.host = host
    
    def __ping(self):
         pass
    

    