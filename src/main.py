#!/usr/bin/env python

from testclient import testClient

if __name__ == '__main__':
    testclient = testClient()
    testclient.setPort("7070")
    testclient.setTarget("http://0.0.0.0:8080/")
    testclient.zapTest()
