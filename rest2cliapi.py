
# test:
# curl -X POST -H "user: user1" -H "Content-Type: application/json"  http://localhost:8180/ls
# curl -X POST -H "user: user1" -H "Content-Type: application/json" -d "{\"arguments\":[\"-la\"]}" http://localhost:8180/ls
# curl -X POST -H "user: user1" -H "Content-Type: application/json" -d "{\"arguments\":[\"myfile.txt\"]}" http://localhost:8180/cat
from bottle import route, run, template, request, response, abort
import subprocess
import json

host="127.0.0.1"
port=8180

@route('/<command>', method='POST')
def index(command):
    resp = {"response":"","error":True,"message":"something went wrong!"}
    # read in configuration
    configuration = json.load(open("rest2cliapi.config.json"))
    if command in configuration:
        response.content_type = 'application/json'
        cmd = configuration[command]["command"]
        # check if user is allowed for this action
        if request.headers.get('user') in configuration[command]["user"]:
            if configuration[command]["overwrite_arguments"]:
                try:
                    req = json.load(request.body)
                    if "arguments" in req:
                        arguments = req["arguments"]
                except:
                    arguments = configuration[command]["arguments"]
            else:
                arguments = ""
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
                result = result.split("\n")
            except:
                result = '{"error": "an internal error occured"}'
            resp["response"] = result
            resp["error"] = False
            resp["message"] = "All OK!"
        else:
            abort(401, "Sorry, access denied.")
    else:
        resp["message"] = "Command not defined!"
    return json.dumps(resp)
run(host=host, port=port)
