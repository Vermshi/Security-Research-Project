#!/usr/bin/env python

from testsuite import TestSuite, Test
from sslyze.server_connectivity_tester import ServerConnectivityError, ServerConnectivityTester
from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.plugins.plugins_repository import PluginsRepository
from sslyze.synchronous_scanner import SynchronousScanner

from sslyze.plugins.openssl_cipher_suites_plugin import *
from sslyze.plugins.certificate_info_plugin import CertificateInfoPlugin
from sslyze.plugins.compression_plugin import CompressionPlugin
from sslyze.plugins.fallback_scsv_plugin import FallbackScsvPlugin
from sslyze.plugins.heartbleed_plugin import HeartbleedPlugin
from sslyze.plugins.http_headers_plugin import HttpHeadersPlugin
from sslyze.plugins.openssl_ccs_injection_plugin import OpenSslCcsInjectionPlugin
from sslyze.plugins.session_renegotiation_plugin import SessionRenegotiationPlugin
from sslyze.plugins.session_resumption_plugin import SessionResumptionPlugin
from sslyze.plugins.robot_plugin import RobotPlugin, RobotScanResultEnum
from sslyze.plugins.early_data_plugin import EarlyDataPlugin


class SSLyzeTestSuite(TestSuite):

    # Required to run tests, is set in "connect"
    server_info = None

    def start(self):
        print("SSLyze does not require to start since it is a python module")
        return True

    def connect(self, address, port=None, https=False):
        """

        :param targetURL:
        :return:
        """
        if not https:
            print("SSLyze cannot scan a http port")

        if port is None or len(port) == 0:
            print("https port not specified, SSLyze only runs on https")
            return False
        # Connect SSLyze to the specified target
        host = address
        port = int(port)
        try:
            server_tester = ServerConnectivityTester(
                hostname=host,
                port=port,
                tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS
            )
            print('Testing connectivity with', server_tester.hostname + ':' + str(server_tester.port))
            self.server_info = server_tester.perform()
            return True
        except ServerConnectivityError as e:
            # Could not establish an SSL connection to the server
            print('Could not connect to', e.server_info.hostname, e.error_message)
            return False

    def generate_test_list(self):
        """

        :return:
        """

        test_dictionary = self.get_tests_from_file("tests.csv", self.engine_name)

        tests = []
        for i, plugin in enumerate(PluginsRepository._PLUGIN_CLASSES):
            title = plugin.get_title()
            tests.append(Test(
                name=title,
                testid=i,
                description=plugin.get_description(),
                engine=self.engine_name,
                vulnerability=test_dictionary[title][0],
                mode='passive',
                difficulty=test_dictionary[title][1],
                passed=None,
                enabled=True))
        return tests

    def import_policy(self, path, name):
        # TODO: Make standard?
        raise NotImplementedError( "Should have implemented a method to import the test policy from a file" )

    def run_tests(self, tests):
        """

        :param tests:
        :return:
        """

        # Perform tests

        synchronous_scanner = SynchronousScanner()

        # Run all plugins and do individual checks to see if the tests passed
        for i, plugin in enumerate(PluginsRepository._PLUGIN_CLASSES):
            if tests[i].enabled is True:
                plugin_passed = True

                # Individual check for cipher suites
                if plugin is OpenSslCipherSuitesPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_open_ssl_cihper_suites_secure(command, scan_result):
                            # If one command fails the plugin fails as a whole
                            plugin_passed = False
                            break

                # Individual check for certificates
                elif plugin is CertificateInfoPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_certificate_info_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for compression
                elif plugin is CompressionPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_compression_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for fallback scsv
                elif plugin is FallbackScsvPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_fallback_scsv_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for heartbleed
                elif plugin is HeartbleedPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_heartbleed_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for secure http headers
                elif plugin is HttpHeadersPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_http_headers_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for openssl css injection
                elif plugin is OpenSslCcsInjectionPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_openssl_css_injection_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for session renegotiation
                elif plugin is SessionRenegotiationPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_session_renegotiation_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for session resumption
                elif plugin is SessionResumptionPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_session_resumption_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for the robot attack
                elif plugin is RobotPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_robot_secure(scan_result):
                            plugin_passed = False
                            break

                # Individual check for early data support
                elif plugin is EarlyDataPlugin:
                    for command in plugin.get_available_commands():
                        scan_result = synchronous_scanner.run_scan_command(self.server_info, command())
                        if not self.is_early_data_secure(scan_result):
                            plugin_passed = False
                            break

            else:
                plugin_passed = None
            tests[i].passed = plugin_passed

        return tests

    def is_open_ssl_cihper_suites_secure(self, command, scan_result):
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

    def is_certificate_info_secure(self, scan_result):
        for certificate in scan_result.path_validation_result_list:
            if not certificate.is_certificate_trusted:
                return False
        return True

    def is_compression_secure(self, scan_result):
        return not scan_result.compression_name

    def is_fallback_scsv_secure(self, scan_result):
        return scan_result.supports_fallback_scsv

    def is_heartbleed_secure(self, scan_result):
        return not scan_result.is_vulnerable_to_heartbleed

    def is_http_headers_secure(self, scan_result):
        return scan_result.hsts_header and scan_result.hpkp_header and scan_result.expect_ct_header and \
                scan_result.is_valid_pin_configured and scan_result.is_backup_pin_configured

    def is_openssl_css_injection_secure(self, scan_result):
        return not scan_result.is_vulnerable_to_ccs_injection

    def is_session_renegotiation_secure(self, scan_result):
        return scan_result.supports_secure_renegotiation

    def is_session_resumption_secure(self, scan_result):
        return scan_result.is_ticket_resumption_supported

    def is_robot_secure(self, scan_result):
        return not (scan_result.robot_result_enum == RobotScanResultEnum.VULNERABLE_WEAK_ORACLE or
                    scan_result.robot_result_enum == RobotScanResultEnum.VULNERABLE_STRONG_ORACLE)

    def is_early_data_secure(self, scan_result):
        return scan_result.is_early_data_supported

    def stop(self):
        print("Can SSLyze be stopped?")

    def shutdown(self):
        print("SSLyse does not require to shut down since it is a python module")
