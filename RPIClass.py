import paramiko
import threading
     
class Node():
    def __init__(self, hostName: str, ip: str, password: str, name: str, port: int = 22):
        self.hostName = hostName
        self.type = "RaspberryPi"
        self.ip = ip
        self.password = password
        self.name = name
        self.port = port
        threading.Thread(target=self.__setup).start()
    
    def __setup(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username=self.hostName, password=self.password, port=self.port)
        self.ssh = ssh
        ssh.exec_command("mkdir -p /home/pi/serverFiles")
        self.sftp = ssh.open_sftp()
        self.sftp.chdir("/home/pi/serverFiles")
        
        self.sftp.put("/checkScripts/rpi.py", ".rpi.py")
        self.sftp.put("/checkScripts/requirements.txt", "requirements.txt")
        self.ssh.exec_command("pip install requirements.txt && nohup python3 .rpi.py &")
        
    def upload(self, file):
        self.sftp.put(file, file.name)
        
    def download(self, file):
        self.sftp.get(file, file.name)
        
    
        
    
class Win():
    def __init__(self, hostName: str, ip: str, password: str, name: str, port: int = 22):
        self.hostName = hostName
        self.type = "Windows"
        self.ip = ip
        self.password = password
        self.name = name
        self.port = port
        
    def get_states(self):
        pass
    
    
    
    
    
    

