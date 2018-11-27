# from main2 import *
from zaptestsuite import ZapTestSuite
from sslyzetestsuite import SSLyzeTestSuite

from json import *
import sys

import time
from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)
#TestObjekt:
# name, testid, description, engine, vulnerability, mode, passed, enabled
test1 = ["SQL injextion", "00:25", "SQL injection test bla bla vulnerabaility bla bla bla", "zap", "SQl injection", 2, False, True]
test2 = ["XSS attack", "00:32", "XSS injection can be done by bla bla bla", "XSS", 0, True,True]

data = {
#     "test1":{
#   "name": "Sql injection",
#   "testid": "00:25",
#   "description":"SQL injection test bla bla vulnerabaility bla bla bla" ,
#    "engine": "zap",
#     "vulnerability": "SQl injection",
#     "mode": 2,
#     "passed": True,
#     "enabled": True
# },
# "test2":{
#   "name": "XSS",
#   "testid": "00:32",
#   "description":"XSSS test bla bla vulnerabaility bla bla bla" ,
#    "engine": "zap",
#     "vulnerability": "SQl injection",
#     "mode": 2,
#     "passed": False,
#     "enabled": False
# },

}
testsuites = []
testsuites.append(SSLyzeTestSuite("SSLyze"))
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

#change to displayTests
@app.route('/')
def output():
    for test in testsuites:
        print("The tests are loading ...")
        test.start()
        time.sleep(3)
        for t in test.generate_test_list():
            tests.append(t)
    testsDict = suiteToDict(tests)
    for key, value in testsDict.items():
        data[key] = value
    # serve index template
    return render_template('index.html', name='Joe', data = data)

#change to runTests
@app.route('/atc', methods=['POST'])
def attack():
    fullAddress = request.form["attackAddress"]

    # TODO: Handle format
    https_port = request.form["httpsport"]

    if(len(fullAddress) == 0):
        return render_template('index.html', name='Joe', data=data,
                               error="The attack address cannot be empty.")
    try:
        address, http_port = fullAddress.split(":")
    except:
        return render_template('index.html', name='Joe', data=data,
                               error="The given address was not in the right format")

    Success = runTest(address, http_port, https_port)
    if(Success):
        return render_template('index.html', name='Joe', data=data)
    else:
        return render_template('index.html', name='Joe', data=data, error= "The engine could not connect to that address")


def runTest(address, http_port, https_port):
    #TODO sett inn logikk for å kjøre testene her
    global data
    global tests
    testresults = []
    for test in testsuites:
        http_test = False
        https_test = False,


        if(test.connect(address, http_port=http_port)):
            http_test = testresults.extend(test.run_tests(tests)) #Run when attack, show loading bar and update after finnished.

        # Run tests for https port
        # TODO: The result must somehow be merged
        if(test.connect(address, https_port=https_port)):
            https_test = testresults.extend(test.run_tests(tests)) #Run when attack, show loading bar and update after finnished.

        # TODO: The break condition must be different because a test engine may only work on one kind of port
        # If none of the connection was a success
        # else:
        #    return False
    res = suiteToDict(testresults)
    data = res

@app.route('/checkChange', methods=['POST'])
def checkChange():
    check = request.form.getlist('check')
    for key, value in enumerate(data):
        if(value in check):
            data[value]["enabled"] = True
        else:
            data[value]["enabled"] = False
    # for t in tests:
    #     t.enabled = data[t.name]["enabled"]


    return render_template('index.html', name='Joe', data=data)


if __name__ == '__main__':
    # run!
    app.run()
