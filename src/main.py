#!/usr/bin/env python

from testclient import testClient
import time

if __name__ == '__main__':
    testclient = testClient()
    testclient.setTarget("http://0.0.0.0:8080/")
    testclient.runAllTests()
    print testclient.tests
