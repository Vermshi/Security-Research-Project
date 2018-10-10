#!/usr/bin/env python

from testclient import TestClient
import time

if __name__ == '__main__':
    testclient = TestClient()
    testclient.zapStart()
    testclient.zapConfigure()
    testclient.setTarget("http://0.0.0.0:8080/")
    #testclient.runAllTests()
    print testclient.tests


