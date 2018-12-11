from zaptestsuite import ZapTestSuite
from sslyzetestsuite import SSLyzeTestSuite

from json import *
import sys

import time
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)

# name, testid, description, engine, vulnerability, mode, passed, enabled
test1 = ["SQL injextion", "00:25", "SQL injection test bla bla vulnerabaility bla bla bla", "zap", "SQl injection", 2, False, True]
test2 = ["XSS attack", "00:32", "XSS injection can be done by bla bla bla", "XSS", 0, True,True]

data = {
    "test1":{
  "name": "Sql injection",
  "testid": "00:25",
  "description":"SQL injection test bla bla vulnerabaility bla bla bla" ,
   "engine": "zap",
    "vulnerability": "SQl injection",
    "mode": 2,
    "passed": True,
    "enabled": True,
    "diffculty": 0,
},
"test2":{
  "name": "XSS",
  "testid": "00:32",
  "description":"XSSS test bla bla vulnerabaility bla bla bla" ,
   "engine": "zap",
    "vulnerability": "SQl injection",
    "mode": 2,
    "passed": False,
    "enabled": False,
    "diffculty": 1,
},
"testinator":{
  "name": "XSS",
  "testid": "00:32",
  "description":"The test the myth the legend of all legends" ,
   "engine": "zasdfp",
    "vulnerability": "wups",
    "mode": 2,
    "passed": False,
    "enabled": True,
    "diffculty": 2
},

}
testsuites = []
testsuites.append(SSLyzeTestSuite("SSLyze"))
testsuites.append(ZapTestSuite("ZAP"))
tests = []
testsLoaded = False
difficulty = 0


def suiteToDict(suits):
    testDict = {}
    for test in suits:
        x = {}
        x["name"] = test.name
        x["description"] = test.description
        x["passed"] = test.passed
        x["enabled"] = test.enabled
        x["vulnerability"] = test.vulnerability
        testDict[x["name"]] = x
    return testDict

@app.route('/atc')
@app.route('/check-change')
@app.route('/auto-enable')
@app.route('/diff-change')
def reDirect():
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty)

@app.route('/')
def displayTests():

    global testsLoaded
    if (testsLoaded == False):
        for test in testsuites:
            print("The tests are loading ...")
            test.start()
            time.sleep(3)

            for t in test.generate_test_list():
                tests.append(t)
        testsDict = suiteToDict(tests)
        for key, value in testsDict.items():
            data[key] = value
        testsLoaded = True
    return render_template('index.html', data = data)

@app.route('/atc', methods=['POST'])
def attack():
    fullAddress = request.form["attackAddress"]

    # TODO: Handle format
    https_port = request.form["HTTPSport"]

    if(len(fullAddress) == 0):
        return render_template('index.html', data=displayRightDifficulty(),
                               error="The attack address cannot be empty.", diff=difficulty)
    try:
        address, http_port = fullAddress.split(":")
    except:
        return render_template('index.html', data=displayRightDifficulty(),
                               error="The given address was not in the right format",  diff=difficulty)

    Success = runTest(address, http_port, https_port)
    if(Success):
        return render_template('index.html', data=displayRightDifficulty(), diff=difficulty)
    else:
        return render_template('index.html', data=displayRightDifficulty(), error= "The attack engine could not connect to that address", diff=difficulty)



def runTest(address, http_port, https_port):
    global data
    global tests
    testresults = []

    for testsuite in testsuites:

        engine_tests = []
        # Collect all tests for the specific testsuite before running
        for test in tests:
            if testsuite.engine_name == test.engine:
                engine_tests.append(test)

        if(testsuite.connect(address, http_port=http_port, https_port=https_port)):
            # Run tests
            testresults.extend(testsuite.run_tests(engine_tests)) #Run when attack, show loading bar and update after finnished.
        elif testsuite.engine_name == "SSLyze" and not len(https_port):
            testresults.extend(engine_tests)
        else:
            return False

    res = suiteToDict(testresults)
    data = res
    changeDifficulty(difficulty)
    return True

@app.route('/check-change', methods=['POST'])
def checkChange():
    check = request.form.getlist('check')
    for key, value in enumerate(data):
        if(value in check):
            data[value]["enabled"] = True
        else:
            data[value]["enabled"] = False
    for t in tests:
         t.enabled = data[t.name]["enabled"]

    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty)

@app.route('/auto-enable', methods=['POST'])
def enableDisableAll():
    val = request.form["sortAll"]
    if(val == "1"):
        for key, value in enumerate(data):
            data[value]["enabled"] = True

    elif(val == "2"):
        for key, value in enumerate(data):
            data[value]["enabled"] = False
    elif(val == "3"):
        for key, value in enumerate(data):
            if(data[value]["passed"]):
                data[value]["enabled"] = False
    else:
        return render_template('index.html', data=displayRightDifficulty(),
                               error="Suspicious POST request received, hmmm", diff=difficulty)
    for t in tests:
        t.enabled = data[t.name]["enabled"]

    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty)

def changeDifficulty(difficulty):
    if(difficulty == 0):
        for key, value in enumerate(data):
            if(data[value]["diffculty"] == 0):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 1):
        for key, value in enumerate(data):
            if (data[value]["diffculty"] == 0  or  data[value]["diffculty"] == 1):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 2):
        for key, value in enumerate(data):
            if (data[value]["diffculty"] == 0  or  data[value]["diffculty"] == 1 or  data[value]["diffculty"] == 2):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    for t in tests:
        t.enabled = data[t.name]["enabled"]

def displayRightDifficulty():
    displayDict = {}
    global difficulty
    if (difficulty == 0):
        for key, value in enumerate(data):
            if (data[value]["diffculty"] == 0):
                displayDict[value] = data[value]
    if (difficulty == 1):
        for key, value in enumerate(data):
            if (data[value]["diffculty"] == 0 or data[value]["diffculty"] == 1):
                displayDict[value] = data[value]
    if (difficulty == 2):
        for key, value in enumerate(data):
                displayDict[value] = data[value]
    return displayDict


@app.route('/diff-change', methods=['POST'])
def selectChange():
    global difficulty
    diffSelect = request.form["diffSelect"]
    if(diffSelect == "Min"):
        difficulty = 0
    elif(diffSelect == "Med"):
        difficulty = 1
    else:
        difficulty = 2
    changeDifficulty(difficulty)


    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty)


if __name__ == '__main__':
    app.run()

