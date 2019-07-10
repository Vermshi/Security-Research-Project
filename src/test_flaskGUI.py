import os
import tempfile
import sys
import pytest

import flaskGUI


def pytest_generate_tests(metafunc):
    ''' just to attach the cmd-line args to a test-class that needs them '''
    target_from_cmd_line = metafunc.config.getoption("target")
    print('command line passed for --target ({})'.format(target_from_cmd_line))
    
    # check if this function is in a test-class that needs the cmd-line args
    if target_from_cmd_line and hasattr(metafunc.cls, 'real_target'):
        # now set the cmd-line args to the test class
        metafunc.cls.real_target = target_from_cmd_line[0]
    
class TestServerCode(object):

    real_target=None


    @pytest.fixture
    def client(self):
        db_fd, flaskGUI.app.config['DATABASE'] = tempfile.mkstemp()
        flaskGUI.app.config['TESTING'] = True
        client = flaskGUI.app.test_client()

        #with flaskGUI.app.app_context():
        #    flaskGUI.init_db()

        yield client

        os.close(db_fd)
        os.unlink(flaskGUI.app.config['DATABASE'])

    def test_load(self, client):
        response = self.load(client)
        assert response.status_code == 200

    def load(self, client):
        return client.get('/', follow_redirects=True)


    def main(self):
        # extract your arg here
        print('Extracted arg is ==> %s' % sys.argv[2])
        pytest.main([sys.argv[1]])

