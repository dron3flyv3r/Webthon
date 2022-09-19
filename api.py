import json
from flask import Blueprint, render_template, request

api = Blueprint('api', __name__)

@api.route('/', methods=['GET', 'POST'])
def apiHW():
    return json.dumps({"hello world": "hello world"})

#TODO - Get files
#TODO - Get status of files
#TODO - Get status of files of specific file
#TODO - Get status of nodes
#TODO - Get terminal output 
#TODO - Get terminal output of specific file
#TODO - Get status of specific node
#TODO - 
#TODO - 
#TODO - 
#TODO - 