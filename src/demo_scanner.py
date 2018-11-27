import sslyze
from sslyze.server_connectivity_tester import ServerConnectivityError, ServerConnectivityTester
import sslyze.server_connectivity_tester
from sslyze.ssl_settings import TlsWrappedProtocolEnum
from sslyze.synchronous_scanner import SynchronousScanner
from sslyze.plugins.openssl_cipher_suites_plugin import OpenSslCipherSuitesPlugin, Tlsv10ScanCommand
from sslyze.plugins.plugins_repository import PluginsRepository
from sslyze.plugins.certificate_info_plugin import CertificateInfoPlugin

class DemoScan(object):

    def demo_synchronous_scanner(self):
        # Run one scan command to list the server's TLS 1.0 cipher suites
        try:
            server_tester = ServerConnectivityTester(
                hostname='0.0.0.0',
                #ip_addr='0.0.0.0',
                port=8443,
                tls_wrapped_protocol=TlsWrappedProtocolEnum.HTTPS
            )
            print(f'\nTesting connectivity with {server_tester.hostname}:{server_tester.port}...')
            server_info = server_tester.perform()
        except ServerConnectivityError as e:
            # Could not establish an SSL connection to the server
            raise RuntimeError(f'Could not connect to {e.server_info.hostname}: {e.error_message}')

        command = Tlsv10ScanCommand()

        synchronous_scanner = SynchronousScanner()
        print("COMMAND")
        print(command)
        scan_result = synchronous_scanner.run_scan_command(server_info, command)
        for cipher in scan_result.accepted_cipher_list:
            print(f'    {cipher.name}')


        for plugin in PluginsRepository._PLUGIN_CLASSES:
            print("PLUGIN")
            print(plugin)
            for command in plugin.get_available_commands(): 
                print("COMMAND")
                print(command)
                scan_result = synchronous_scanner.run_scan_command(server_info, command())
                if plugin is OpenSslCipherSuitesPlugin:
                    for cipher in scan_result.accepted_cipher_list:
                        print(f'    {cipher.name}')
                elif plugin is CertificateInfoPlugin:
                    for certificate in scan_result.path_validation_result_list:
                        print(certificate.is_certificate_trusted)

