
# test:
# curl -X POST -H "Content-Type: application/json"  http://localhost:8180/ls
# curl -X POST -H "Content-Type: application/json" -d "{\"arguments\":[\"-la\"]}" http://localhost:8180/ls
# curl -X POST -H "Content-Type: application/json" -d "{\"arguments\":[\"myfile.txt\"]}" http://localhost:8180/cat
from bottle import route, run, template, request
import subprocess
import json

@route('/<command>', method='POST')
def index(command):
    # read in configuration
    configuration = json.load(open("rest2cliapi.config.json"))
    if command in configuration:
        cmd = configuration[command]["command"]
        try:
            req = json.load(request.body)
            if "arguments" in req:
                arguments = req["arguments"]
        except:
            arguments = configuration[command]["arguments"]
        if len(arguments)>0:
            cmd_arr = cmd.split(" ") + arguments
        else:
            cmd_arr = cmd.split(" ")
        print cmd_arr
        try:
            if len(cmd_arr)>1:
                result = subprocess.check_output(cmd_arr,stderr=subprocess.STDOUT)
            else:
                result = subprocess.check_output(cmd_arr[0],stderr=subprocess.STDOUT)
        except:
            result = '{"error": "an internal error occured"}'
        return template('{"response": "'+ result +'"}')
    else:
        return template('{"response": {"error":"No command found!"}}')

run(host='localhost', port=8180)
