from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from subprocess import check_output,STDOUT


app = Flask(__name__)
api = Api(app)


# Route for Parser Object
class Parser(Resource):
    def get(self):
        statusCode = 404
        res = ""
        flag = False
        try:
            command = ["python3","scripts/parser.py"]
            res = check_output(command,stderr=STDOUT).decode()
            print("This is result -> "+res)
            flag = True
        except Exception as err:
            res = str(err)

        if flag:
            statusCode = 200
        return {
            "statusCode":statusCode,
            "data":res
        }

    def post(self):
        req = request.json
        flag = False
        url = req["url"]
        statusCode = 404
        res = ""
        command = req["command"]
        try:
            ter_command = ["python3","scripts/parser.py",url,command]
            res = check_output(ter_command,stderr=STDOUT).decode()
            flag = True
        except Exception as err:
            res = str(err)

        if flag:
            statusCode = 200


        return {
            "data":res,
            "statusCode":statusCode
        }

# Route for Network Identification Object

api.add_resource(Parser,"/parser")
if __name__ == "__main__":
    app.run(debug=True)



