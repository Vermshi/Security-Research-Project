#!/usr/bin/env python

from testsuite import TestSuite, Test
from sslyze.server_connectivity_tester import ServerConnectivityError, ServerConnectivityTester
from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.plugins.plugins_repository import PluginsRepository
from sslyze.synchronous_scanner import SynchronousScanner

from sslyze.plugins.openssl_cipher_suites_plugin import *
from sslyze.plugins.certificate_info_plugin import CertificateInfoPlugin
#from sslyze.plugins.compression_plugin import


class SSLyzeTestSuite(TestSuite):

    # Required to run tests, is set in "connect"
    server_info = None

    def start(self):
        print("SSLyze does not require to start since it is a python module")

    def connect(self, targetURL):
        """

        :param targetURL:
        :return:
        """
        self.targetURL = targetURL

        # Connect SSLyze to the specified target
        host = targetURL.split(":")[0]
        port = int(targetURL.split(":")[1])
        try:
            server_tester = ServerConnectivityTester(
                hostname=host,
                port=port,
                tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS
            )
            print(f'\nTesting connectivity with {server_tester.hostname}:{server_tester.port}...')
            self.server_info = server_tester.perform()
            return True
        except ServerConnectivityError as e:
            # Could not establish an SSL connection to the server
            print(f'Could not connect to {e.server_info.hostname}: {e.error_message}')
            return False

    def run_tests(self, tests):
        """

        :param tests:
        :return:
        """

        # Perform tests
        # TODO:

        synchronous_scanner = SynchronousScanner()

        # Run all plugins and do individual checks to see if the tests passed
        for i, plugin in enumerate(PluginsRepository._PLUGIN_CLASSES):
            if tests[i].enabled is True:
                plugin_passed = True

                # Individual check for cipher suites
                if plugin is OpenSslCipherSuitesPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.open_ssl_cihper_suites_secure(command, scan_result):
                            # If one command fails the plugin fails as a whole
                            plugin_passed = False
                            break

                # Individual check for cipher suites
                elif plugin is CertificateInfoPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.certificate_info_secure(command, scan_result):
                            # If one command fails the plugin fails as a whole
                            plugin_passed = False
                            break

            else:
                plugin_passed = None
            tests[i].passed = plugin_passed

        return tests

    def open_ssl_cihper_suites_secure(self, command, scan_result):
        """
        Return true if the given result shows a secure cipher suite, else return false

        :param command:
        :param scan_result:
        :return:
        """
        # Only TLS 1.1 or higher are considered secure
        if scan_result.accepted_cipher_list and \
                command is Tlsv11ScanCommand or command is Tlsv10ScanCommand or \
                command is Sslv30ScanCommand or command is Sslv20ScanCommand:
            return False
        elif ("INSECURE" in scan_result.as_text()):
            return False
        return True

    def certificate_info_secure(self, command, scan_result):
        return False

    def generate_test_list(self):
        """

        :return:
        """
        tests = []
        for i, plugin in enumerate(PluginsRepository._PLUGIN_CLASSES):
            tests.append(Test(plugin.get_title(), i, plugin.get_description(), self.engine_name, "UNKNOWN", 'passive', None, True))
        return tests

    def import_policy(self, path, name):
        # TODO: Make standard?
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )

    def shutdown(self):
        print("SSLyse does not require to shut down since it is a python module")
