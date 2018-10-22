#!/usr/bin/env python

from zaptestsuite import ZapTestSuite
import time

if __name__ == '__main__':
    testsuites = []
    testsuites.append(ZapTestSuite("ZAP", 'http://127.0.0.1', '7576', '7576'))

    for test in testsuites:
        print("Running Test Suite", test.engine_name)
        test.start()
        time.sleep(13)
        test.configure()
        test.import_policy("path/to/policy", "Default Policy")
        test.run_tests('http://127.0.0.1:8080')