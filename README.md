# Security-Research-Project

Welcome to the web-application security testing suite

### Prerequisites:

OWASP Zed Attack Proxy 2.7

Java jre 1.8

Python 3.x

### Dependencies

Python dependencies: requirements.txt

### Documentation

Pull the project to read the detailed documentation of the code located in src/docs/_build/html/index.html

A model for the programflow is available in currentprogramflow.svg

### Demo run

As superuser:

    $ python3 src/main2.py
 
To automatically  run the test engine and execute all tests against the target defined in main2.py ('http://127.0.0.1:8080'). If the tests successfully runs against the locally running target it will print the test results achieved. The GUI for the new code is not available yet. But a preview can be seen by running simpleZAP.py.


### Tests

Review all running tests and corresponding vulnerabilities in the testsrunning.pdf file

### TODO:

1. Support https for all engines
2. Disable passed tests button
3. Login to session
4. Installation guide /docker
5. Try a java app
6. Test mac
7. Make simple solution for categories

### Windows installation:
Install docker compose, download toolbox if you have win 10 home, reg installation for Enterprice and Pro:
https://docs.docker.com/compose/install/

