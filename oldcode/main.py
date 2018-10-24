#!/usr/bin/env python

from testclient import TestClient
from zaptestsuite import ZapTestSuite
import time

if __name__ == '__main__':
    zap = ZapTestSuite("ZAP")

    #testclient = TestClient()
    #testclient.setTarget("http://0.0.0.0:8080/")
    #testclient.runAllTests()
    #print(testclient.tests)
