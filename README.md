# Security-Research-Project

Welcome to the web-application security testing suite

Requirements:

OWASP Zed Attack Proxy 2.7 https://github.com/zaproxy/zaproxy/wiki/Downloads

Java jre 1.8: https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html

Python 3.x
    - Read 'requirements.txt' to see Python libraries

Run: python src/main2.py
 
to automaticly  run the test engine and execute all tests against the target defined in main2.py ('http://127.0.0.1:8080'). To let the engine start. For this current script the code pauses for 25 seconds to let ZAP initiate. This might be a little too long or too short. If the tests successfully runs against the locally running target it will print the test results achieved. The GUI for the new code is not available yet. But a preview can be seen by running simpleZAP.py.

Detailed documentation of the code is located in docs/_build/html/index.html
