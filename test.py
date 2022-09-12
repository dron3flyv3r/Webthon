

import json

settings = {
    "clusterName": "RPiCluster",
    "customFiles":{
        
    },
    "fileNames":[["", ""]]  
}

with open("settings.json", "w") as f:
    json.dump(settings, f, indent=4)
 
with open("defult.json", "w") as f:
    json.dump(settings, f, indent=4)   









""" ########### SSH COMANDS TEST 1 ############

import spur

user = "pi"
host = "192.168.1.62"
cmd = ['cat', '/sys/class/thermal/thermal_zone0/temp']

shell = spur.SshShell(hostname=host, username=user, password="Everest1")
result = shell.run(cmd).output.decode()

print(result) """