
import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)
#TestObjekt:
# name, testid, description, engine, vulnerability, mode, passed, enabled
test1 = ["SQL injextion", "00:25", "SQL injection test bla bla vulnerabaility bla bla bla", "zap", "SQl injection", 2, False, True]
test2 = ["XSS attack", "00:32", "XSS injection can be done by bla bla bla", "XSS", 0, True,True]

data = {"test1":{
  "name": "Sql injection",
  "testid": "00:25",
  "description":"SQL injection test bla bla vulnerabaility bla bla bla" ,
   "engine": "zap",
    "vulnerability": "SQl injection",
    "mode": 2,
    "passed": True,
    "enabled": True
},
"test2":{
  "name": "XSS",
  "testid": "00:32",
  "description":"XSSS test bla bla vulnerabaility bla bla bla" ,
   "engine": "zap",
    "vulnerability": "SQl injection",
    "mode": 2,
    "passed": False,
    "enabled": True
},

}

@app.route('/')
def output():

    # serve index template
    return render_template('index.html', name='Joe', data = data)

@app.route('/', methods=['POST'])
def attack():
    address = request.form["attackAddress"]
    print(address)
    runTest(address)
    return render_template('index.html', name='Joe', data=data)

def runTest(address):
    #TODO sett inn logikk for å kjøre testene her
    result = []
    return result

if __name__ == '__main__':
    # run!
    app.run()