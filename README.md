Welcome to the Security Testing Tool, please notice that the tool has been developed recently and is still work in progress. However all basic features required to get introduced to automatic penetration testing should be working. It is worth mentioning that the tool mostly depends on the open source project from OWASP: Zed Attack Proxy https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project. In addition the tool intends to combine different automated security tools to simplify the process of automated penetration testing. 

# EASY INSTALL

Follow this guide to install the tool
https://docs.google.com/document/d/1qplZh1OLGGU7RmATFsGFOtikVoqYmQfIlTEbuyVF-JE/edit?usp=sharing 

# Proposed testing target

Follow this guide to run a testing target with docker
https://docs.google.com/document/d/1Y3YV3POaJdohPlDcZCtEWIYE1J7qmCkkwmMvPTfthAU/edit?usp=sharing

# Security-Research-Project

Welcome to the web-application security testing suite

For extended user guidance and alternative installation, refer to the following manual: https://docs.google.com/document/d/14ctYlZG4iIHCMvTNi2JWvYJrRYK5ay7OvZyjGjLmO0w/edit?usp=sharing

### Prerequisites:

OWASP Zed Attack Proxy 2.7

Java jre 1.8

Python 3.6

### Dependencies

Python dependencies: src/requirements.txt

### Run

	$ cd src/
	$ sudo python flaskGUI.py
	
### Unit Tests
	$ cd src/tests
	$ sudo python -m pytest --target <testingTargetURL> test_flaskGUI.py 

### Docker

A docker image is available at https://cloud.docker.com/repository/docker/jakobsn/testtool2

### Code Documentation

Pull the project to read the detailed documentation of the code located in src/docs/_build/html/index.html

A model for the programflow is available in currentprogramflow.svg

### Security Tests

Review all running tests and corresponding vulnerabilities in the testcoverage.pdf file


