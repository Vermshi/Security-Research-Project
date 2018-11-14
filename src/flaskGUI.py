from main2 import *
from json import *
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
testsuites = []
testsuites.append(ZapTestSuite("ZAP"))
tests = []


def suiteToDict(suits):
    testDict = {}
    for test in suits:
        x = {}
        x["name"] = test.name
        x["description"] = test.description
        x["passed"] = test.passed
        x["enabled"] = test.enabled
        testDict[x["name"]] = x
    return testDict


@app.route('/')
def output():
    for test in testsuites:
        print("Siden lastes")
        test.start()
        time.sleep(3)
        test.configure()
        for t in test.generate_test_list():
            tests.append(t)
        testsDict = suiteToDict(tests)
        for key, value in testsDict.items():
            data[key] = value
    # serve index template
    return render_template('index.html', name='Joe', data = data)

@app.route('/', methods=['POST'])
def attack():
    address = request.form["attackAddress"]
    runTest(address)
    return render_template('index.html', name='Joe', data=data)

def runTest(address):
    #TODO sett inn logikk for å kjøre testene her
    global data
    global tests
    testresults = []
    for test in testsuites:
        # test.import_policy("path/to/policy", "Default Policy")
        testresults.extend(test.run_tests(tests, "http://"+address)) #Run when attack, show loading bar and update after finnished.
    tests = suiteToDict(testresults)
    data = tests


if __name__ == '__main__':
    # run!
    app.run()