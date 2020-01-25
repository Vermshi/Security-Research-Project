from zaptestsuite import ZapTestSuite
from sslyzetestsuite import SSLyzeTestSuite
from json import *
import sys
import time
import math
from flask import Flask, render_template, request, redirect, Response
from urllib.parse import urlparse

application = Flask(__name__)

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


@application.route('/atc')
@application.route('/reset')
@application.route('/stop')
@application.route('/check-change')
@application.route('/auto-enable')
@application.route('/diff-change')
@application.route('/strength-change')


def reDirect():
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


# Show all the tests of each test suite with the generate_test_list function as defined in the testsuite interface
@application.route('/')
def displayTests():
    """
    Load main page, show all tests
    """
    global testsLoaded
    global data
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

        disableAll()
        changeDifficulty(difficulty)
        enableAll()
        testsLoaded = True
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


@application.route('/atc', methods=['POST'])
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

    session_id = "No Active Session"
    if request.form["submit"] == "connect":
        for testsuite in testsuites:
            if testsuite.engine_name == "ZAP":
                testsuite.connect(scheme, address, port)
                active_session = False
                while not active_session:
                    print("Trying to connect")
                    print("Authenticate now")
                    time.sleep(20)

                    print('Sessions:', testsuite.zap.httpsessions.sites)
                    if (address + ':' + str(port)) in testsuite.zap.httpsessions.sites:
                        print('Opened site:', testsuite.zap.httpsessions.sessions(address + ':' + str(port)))
                        print(testsuite.zap.httpsessions.sessions(address + ':' + str(port)))
                        user_id = testsuite.set_active_session()
                        active_session = True
                        print("Connected successfully", testsuite.zap.httpsessions.sessions(address + ':' + str(port)))
                        print("User:", user_id)
                        print("Active session:", testsuite.zap.httpsessions.active_session(address + ':' + str(port)))
                        session_id = testsuite.zap.httpsessions.sessions(address + ':' + str(port))[0]['session'][1]['JSESSIONID']['value']
                        # TODO: Wait untill the session is activated
                    

    try:
        elapsed_time, test_amount, vulnerabilities = runTest(scheme, address, port)
        return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold, elapsed_time=elapsed_time, test_amount=test_amount, vulnerabilities=vulnerabilities, session_id = session_id)
    except Exception as e:
        print(e)
        return render_template('index.html', data=displayRightDifficulty(), error="Could not scan the target", diff=difficulty, strength=strength, threshold=threshold), 201


@application.route('/stop', methods=['POST'])
def stop():
    """
    Stop a running test
    """
    for testsuite in testsuites:
        print("Stopping", testsuite.engine_name)
        testsuite.stop()
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)


@application.route('/reset', methods=['POST'])
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
    :type address: str 
    :param port:
    :type port: str 
    """

    global data
    global tests
    test_results = []

    test_amount = 0
    vulnerabilities = 0
    start_time = time.time()
    session_id = None

    for testsuite in testsuites:
        engine_tests = []
        # Collect all tests for the specific testsuite before running
        for test in tests:
            if testsuite.engine_name == test.engine:
                engine_tests.append(test)

        # Connect to keytarget
        try:
            if testsuite.engine_name == "ZAP":
                if (address + ":" + str(port)) not in testsuite.zap.httpsessions.sites:
                    testsuite.connect(scheme, address, port)
                else:
                    testsuite.set_target_address(scheme + "://" + address + ":" + str(port))
            else:
                testsuite.connect(scheme, address, port)
        except Exception as e:
            # The SSLyze tool will only run when a HTTPS port is specified
            if testsuite.engine_name == "SSLyze" and scheme == "http":
                pass
            else:
                return render_template('index.html', data=displayRightDifficulty(), error=e, diff=difficulty, strength=strength, threshold=threshold), 201

        # Run tests
        try:              
            test_results.extend(testsuite.run_tests(engine_tests)) #Run when attack, show loading bar and update after finished.
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
    return elapsed_time, test_amount, vulnerabilities


@application.route('/check-change', methods=['POST'])
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

@application.route('/auto-enable', methods=['POST'])
def enableDisableAll():
    """
    Enable or disable all tests
    """
    global data
    val = request.form["sortAll"]
    if(val == "1"):
        enableAll()

    elif(val == "2"):
        disableAll()
    elif(val == "3"):
        disablePassed()
    else:
        return render_template('index.html', data=displayRightDifficulty(),
                               error="Suspicious POST request received, hmmm", diff=difficulty, strength=strength, threshold=threshold)
    for t in tests:
        t.enabled = data[t.name]["enabled"]
    return render_template('index.html', data=displayRightDifficulty(), diff=difficulty, strength=strength, threshold=threshold)

def disablePassed():
    """
    Disable all passed tests
    """
    global data
    for value in data:
        if(data[value]["passed"]):
            data[value]["enabled"] = False

def disableAll():
    """
    Disable all tests
    """
    global data
    for value in data:
            data[value]["enabled"] = False

def enableAll():
    """
    Enable all tests in the current difficulty
    """
    global difficulty
    global data
    if (difficulty == 0):
        for value in data:
            if (data[value]["difficulty"] == 0):
                data[value]["enabled"] = True
    elif (difficulty == 1):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1):
                data[value]["enabled"] = True
    elif (difficulty == 2):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2):
                data[value]["enabled"] = True
    elif (difficulty == 3):
        for value in data:
            if (data[value]["difficulty"] == 0 or data[value]["difficulty"] == 1 or data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3):
                data[value]["enabled"] = True
    elif (difficulty == 4):
        for value in data:
            data[value]["enabled"] = True

def changeDifficulty(difficulty):
    """
    Set difficulty, which is the amount of tests executed in one run
    
    :param difficulty: The difficulty level 0-4
    :type difficulty: int
    """
    if(difficulty == 0):
        for value in data:
            if(data[value]["difficulty"] == 0):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 1):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 2):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 3):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3):
                data[value]["enabled"] = True
            else:
                data[value]["enabled"] = False
    elif(difficulty == 4):
        for value in data:
            if (data[value]["difficulty"] == 0  or  data[value]["difficulty"] == 1 or  data[value]["difficulty"] == 2 or data[value]["difficulty"] == 3 or data[value]["difficulty"] == 4):
                data[value]["enabled"] = True
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


@application.route('/diff-change', methods=['POST'])
def selectChange():
    """
    Change difficulty - amount of tests to execute in one run
    """
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


@application.route('/strength-change' , methods=['POST'])
def selectStrength():
    """
    Change threshold or strength for zap
    """
    global testsuites
    global zap_policy_name
    strengthSelect = request.form["strengthSelect"]
    set_strength(strengthSelect)

    thresholdSelect = request.form["thresholdSelect"]
    set_threshold(thresholdSelect)

    for testsuite in testsuites:
        if testsuite.engine_name == "ZAP":
            testsuite.zap.ascan.update_scan_policy(zap_policy_name, thresholdSelect, strengthSelect)

    return render_template('index.html', data=data, diff=difficulty, strength=strength, threshold=threshold)


def set_strength(strengthSelect):
    """
    Set global strength variable

    :param strengthSelect: The strength of the ZAP engine tests Low, Medium, High
    :type strengthSelect: str
    """
    global strength
    if(strengthSelect == "Low"):
        strength = 0
    elif(strengthSelect == "Medium"):
        strength = 1
    elif(strengthSelect == "High"):
        strength = 2

def set_threshold(thresholdSelect):
    """
    Set global threshold variable

    :param strengthSelect: The threshold of the ZAP engine tests Low, Medium, High
    :type threshold: str
    """
    global threshold
    if(thresholdSelect == "Low"):
        threshold = 0
    elif(thresholdSelect == "Medium"):
        threshold = 1
    elif(thresholdSelect == "High"):
        threshold = 2

if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True)
