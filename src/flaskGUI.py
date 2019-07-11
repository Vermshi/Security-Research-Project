from zaptestsuite import ZapTestSuite
from sslyzetestsuite import SSLyzeTestSuite
from json import *
import sys
import time
import math
from flask import Flask, render_template, request, redirect, Response
from urllib.parse import urlparse

app = Flask(__name__)

# data dictionary contains all the tests from all the testsuites
# variables:
# name, testid, description, engine, vulnerability, mode, difficulty, passed, enabled
data = {
}

testsuites = []
testsuites.append(ZapTestSuite("ZAP"))
testsuites.append(SSLyzeTestSuite("SSLyze"))
tests = []
testsLoaded = False
difficulty = 0
strength = 2
threshold = 0
zap_policy = "testpolicy.xml"
zap_policy_name = "test_policy4"


def suiteToDict(suits):
    """
    Convert python test object to dictionary
    """
    testDict = {}
    for test in suits:
        x = {}
        x["name"] = test.name
        x["description"] = test.description
        x["passed"] = test.passed
        x["enabled"] = test.enabled
        x["difficulty"] = test.difficulty
        x["vulnerability"] = test.vulnerability
        testDict[x["name"]] = x
    return testDict


@app.route('/atc')
@app.route('/reset')
@app.route('/stop')
@app.route('/check-change')
@app.route('/auto-enable')
@app.route('/diff-change')
@app.route('/strength-change')


def reDirect():
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


# Show all the tests of each test suite with the generate_test_list function as defined in the testsuite interface
@app.route('/')
def displayTests():
    """
    Load main page, show all tests
    """
    global testsLoaded
    if (testsLoaded == False):
        for test in testsuites:
            print("The tests are loading ...")
            test.start()

            # Import policy
            #if(test.engine_name == "ZAP"):
            #    test.import_policy(zap_policy, zap_policy_name)

            #time.sleep(5)
            for t in test.generate_test_list():
                tests.append(t)
        testsDict = suiteToDict(tests)
        for key, value in testsDict.items():
            data[key] = value
        testsLoaded = True
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


@app.route('/atc', methods=['POST'])
def attack():
    """
    Launch all enabled tests against target address
    """
    fullAddress = request.form["attackAddress"]

    if(len(fullAddress) == 0):
        return render_template('index.html', data=displayRightDifficulty(),
                               error="The attack address cannot be empty.", diff=difficulty, strength=strength, threshold=threshold), 201
    try:
         parse_object = urlparse(fullAddress)
         scheme = parse_object.scheme
         address = parse_object.hostname
         port = parse_object.port
    except:
        return render_template('index.html', data=displayRightDifficulty(),
                               error="The given address was not in the right format",  diff=difficulty, strength=strength, threshold=threshold), 201

    try:
        elapsed_time, test_amount, vulnerabilities = runTest(scheme, address, port)
        return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold, elapsed_time=elapsed_time, test_amount=test_amount, vulnerabilities=vulnerabilities)
    except:
        return render_template('index.html', data=displayRightDifficulty(), error= "The attack engine could not connect to that address", diff=difficulty, strength=strength, threshold=threshold), 201


@app.route('/stop', methods=['POST'])
def stop():
    """
    Stop a running test
    """
    for testsuite in testsuites:
        print("Stopping", testsuite.engine_name)
        testsuite.stop()
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset the test engines
    """
    for testsuite in testsuites:
        print("Restarting", testsuite.engine_name)
        testsuite.shutdown()
        testsuite.start()
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


def runTest(scheme, address, port):
    """
    Run all the tests against the target.

    :param scheme: http or https
    :type scheme: str
    :param: address
    :type: str 
    :param port:
    :type str: 
    """

    global data
    global tests
    test_results = []

    test_amount = 0
    vulnerabilities = 0
    start_time = time.time()

    for testsuite in testsuites:
        engine_tests = []
        # Collect all tests for the specific testsuite before running
        for test in tests:
            if testsuite.engine_name == test.engine:
                engine_tests.append(test)

        # Connect to keytarget
        try:
            testsuite.connect(scheme, address, port)
        except Exception as e:
            # The SSLyze tool will only run when a HTTPS port is specified
            if testsuite.engine_name == "SSLyze" and scheme == "http":
                pass
            else:
                return render_template('index.html', data=displayRightDifficulty(), error=e, diff=difficulty, strength=strength, threshold=threshold), 201

        # Run tests
        try:
            test_results.extend(testsuite.run_tests(engine_tests)) #Run when attack, show loading bar and update after finnished.
        except Exception as e:
            # The SSLyze tool will only run when a HTTPS port is specified
            if testsuite.engine_name == "SSLyze" and scheme == "http":
                test_results.extend(engine_tests)
            else:
                return render_template('index.html', data=displayRightDifficulty(), error=e, diff=difficulty, strength=strength, threshold=threshold), 201

    # Record statistics
    elapsed_time = math.ceil(time.time() - start_time)
    for test in tests:
        if test.enabled:
            test_amount += 1
            if not test.passed:
                vulnerabilities += 1

    # Save the test results
    res = suiteToDict(test_results)
    data = res
    changeDifficulty(difficulty)
    return elapsed_time, test_amount, vulnerabilities


@app.route('/check-change', methods=['POST'])
def checkChange():
    """
    Check if tests are enabled
    """
    check = request.form.getlist('check')
    for value in data:
        if(value in check):
            data[value]["enabled"] = True
        else:
            data[value]["enabled"] = False
    for t in tests:
         t.enabled = data[t.name]["enabled"]

    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)

@app.route('/auto-enable', methods=['POST'])
def enableDisableAll():
    """
    Enable or disable all tests
    """
    global difficulty
    val = request.form["sortAll"]
    if(val == "1"):
        if (difficulty == 0):
            for key, value in enumerate(data):
                if (data[value]["difficulty"] == 0):
                    data[value]["enabled"] = True
        elif (difficulty == 1):
            for key, value in enumerate(data):
                if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1):
                    data[value]["enabled"] = True
        elif (difficulty == 2):
            for key, value in enumerate(data):
                if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2):
                    data[value]["enabled"] = True
        elif (difficulty == 3):
            for key, value in enumerate(data):
                if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3):
                    data[value]["enabled"] = True
        elif (difficulty == 4):
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
                               error="Suspicious POST request received, hmmm", diff=difficulty, strength=strength, threshold=threshold)
    for t in tests:
        t.enabled = data[t.name]["enabled"]
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


def changeDifficulty(difficulty):
    if(difficulty == 0):
        for value in data:
            if(data[value]["difficulty"] == 0):
                pass
            else:
                data[value]["enabled"] = False
    elif(difficulty == 1):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1):
                pass
            else:
                data[value]["enabled"] = False
    elif(difficulty == 2):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2):
                pass
            else:
                data[value]["enabled"] = False
    elif(difficulty == 3):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3):
                pass
            else:
                data[value]["enabled"] = False
    elif(difficulty == 4):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3 or data[value]["difficulty"] == 4):
                pass
            else:
                data[value]["enabled"] = False

    for t in tests:
        t.enabled = data[t.name]["enabled"]


def displayRightDifficulty():
    """
    Get the correct difficulty for the application
    """
    displayDict = {}
    global difficulty
    if (difficulty == 0):
        for value in data:
            if (data[value]["difficulty"] == 0):
                displayDict[value] = data[value]
    elif (difficulty == 1):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1):
                displayDict[value] = data[value]
    elif (difficulty == 2):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2):
                displayDict[value] = data[value]
    elif (difficulty == 3):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3):
                displayDict[value] = data[value]
    elif (difficulty == 4):
        for value in data:
                displayDict[value] = data[value]
    return displayDict


@app.route('/diff-change', methods=['POST'])
def selectChange():
    global difficulty
    diffSelect = request.form["diffSelect"]
    if(diffSelect == "Novice"):
        difficulty = 0
    elif(diffSelect == "Apprentice"):
        difficulty = 1
    elif(diffSelect == "Adept"):
        difficulty = 2
    elif(diffSelect == "Expert"):
        difficulty = 3
    else:
        difficulty = 4
    changeDifficulty(difficulty)
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


@app.route('/strength-change' , methods=['POST'])
def selectStrength():
        global strength
        global threshold
        global testsuites
        global zap_policy_name
        strengthSelect = request.form["strengthSelect"]
        if(strengthSelect == "Low"):
            strength = 0
        elif(strengthSelect == "Medium"):
            strength = 1
        elif(strengthSelect == "High"):
            strength = 2

        thresholdSelect = request.form["thresholdSelect"]
        if(thresholdSelect == "Low"):
            threshold = 0
        elif(thresholdSelect == "Medium"):
            threshold = 1
        elif(thresholdSelect == "High"):
            threshold = 2

        for testsuite in testsuites:
            if testsuite.engine_name == "ZAP":
                testsuite.zap.ascan.update_scan_policy(zap_policy_name, thresholdSelect, strengthSelect)

        return render_template('index.html', data=data, diff=difficulty, strength=strength, threshold=threshold)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
