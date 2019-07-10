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

    # Test if the page and engines launches
    def test_load(self, client):
        response = self.load(client)
        assert response.status_code == 200

    # Launch app
    def load(self, client):
        return client.get('/', follow_redirects=True)

    # Run application attacks against a target url
    def test_attack(self, client):
        if self.real_target == None:
            return False
        response = self.attack(client, self.real_target)
        assert response.status_code == 200

    def attack(self, client, target):
        return client.post('/atc', data=dict(attackAddress=target), follow_redirects=True)

    def main(self):
        # extract your arg here
        print('Extracted arg is ==> %s' % sys.argv[2])
        pytest.main([sys.argv[1]])

