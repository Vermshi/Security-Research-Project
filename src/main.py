#!/usr/bin/env python

from testclient import testClient
import time

if __name__ == '__main__':
    testclient = testClient(zapPort="8080")
    testclient.setTarget("http://0.0.0.0:80/")
    testclient.runAllTests()
    print testclient.tests
