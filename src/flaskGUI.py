from main2 import *
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)

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

@app.route('/atc')
@app.route('/check-change')
@app.route('/auto-enable')
def reDirect():
    return render_template('index.html', data=data)

@app.route('/')
def displayTests():
    for test in testsuites:
        print("The tests are loading ...")
        test.start()
        time.sleep(3)
        for t in test.generate_test_list():
            tests.append(t)
    testsDict = suiteToDict(tests)
    for key, value in testsDict.items():
        data[key] = value
    return render_template('index.html', data = data)

#change to runTests
@app.route('/atc', methods=['POST'])
def attack():
    fullAddress = request.form["attackAddress"]
    if(len(fullAddress) == 0):
        return render_template('index.html', data=data,
                               error="The attack address cannot be empty.")
    try:
        address, port = fullAddress.split(":")
    except:
        return render_template('index.html', data=data,
                               error="The given address was not in the right format")

    Success = runTest(address,port)
    if(Success):
        return render_template('index.html', data=data)
    else:
        return render_template('index.html', data=data, error= "The attack engine could not connect to that address")



def runTest(address,port):
    global data
    global tests
    testresults = []
    for test in testsuites:
        if(test.connect(address,port)):
            testresults.extend(test.run_tests(tests)) #Run when attack, show loading bar and update after finnished.
        else:
            return False
        # test.import_policy("path/to/policy", "Default Policy")
    res = suiteToDict(testresults)
    data = res

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

    return render_template('index.html', data=data)

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
        return render_template('index.html', data=data,
                               error="Suspicious POST request received, hmmm")
    for t in tests:
        t.enabled = data[t.name]["enabled"]

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()