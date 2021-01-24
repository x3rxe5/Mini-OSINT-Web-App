from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from subprocess import check_output,STDOUT


app = Flask(__name__)
api = Api(app)


# Route for Parser Object
class Parser(Resource):
    def __init__(self,statusCode):
        self.statusCode =  statusCode

    def get(self):
        res =  ""
        flag = False
        try:
            command = ["python3","scripts/parser.py"]
            res =  check_output(command,stderr=STDOUT).decode()
            print("This is result -> "+res)
            flag = True
        except Exception as err:
            res =  str(err)

        if flag:
            self.statusCode =  200
        return {
            "statusCode":self.statusCode,
            "data":res
        }

    def post(self):
        req = request.json
        flag = False
        url = req["url"]
        res =  ""
        command = req["command"]
        try:
            ter_command = ["python3","scripts/parser.py",url,command]
            res =  check_output(ter_command,stderr=STDOUT).decode()
            flag = True
        except Exception as err:
            res =  str(err)

        if flag:
            self.statusCode =  200

        return {
            "data":res,
            "statusCode":self.statusCode
        }

class HostDiscover(Resource):
    def __init__(self):
        self.statusCode = statusCode

    def get(self):
        res =  ""
        flag = False
        try:
            command = ["python3","scripts/host_discover.py"]
            res =  check_output(command,stderr=STDOUT).decode()
            print("This is result -> "+res)
            flag = True
        except Exception as err:
            res =  str(err)

        if flag:
            self.statusCode =  200
        return {
            "statusCode":self.statusCode,
            "data":res
        }

    def post(self):
        req = request.json
        flag = False
        url = req["url"]
        res =  ""
        command = req["command"]
        try:
            ter_command = ["python3","scripts/host_discover.py",url,command]
            res =  check_output(ter_command,stderr=STDOUT).decode()
            flag = True
        except Exception as err:
            res =  str(err)

        if flag:
            self.statusCode =  200

        return {
            "data":res,
            "statusCode":self.statusCode
        }


# Route for Network Identification Object
parser = Parser(404)
host_discover = HostDiscover(404)
api.add_resource(Parser,"/parser",resource_class_kwargs={'statusCode': parser})
api.add_resource(HostDiscover,"/hostdiscover",resource_class_kwargs={'statusCode': host_discover})



if __name__ == "__main__":
    app.run(debug=True)



