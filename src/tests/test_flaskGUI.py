import os
import tempfile
import sys
import pytest
import flaskGUI
import time


# Retrive commandline argument --target as an url
def pytest_generate_tests(metafunc):
    ''' just to attach the cmd-line args to a test-class that needs them '''
    target_from_cmd_line = metafunc.config.getoption("target")
    print('command line passed for --target ({})'.format(target_from_cmd_line))
    
    # check if this function is in a test-class that needs the cmd-line args
    if target_from_cmd_line and hasattr(metafunc.cls, 'real_target'):
        # now set the cmd-line args to the test class
        metafunc.cls.real_target = target_from_cmd_line[0]
    
class TestServerCode(object):

    # URL of target to run tests with
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

    # Test application attacks against a target url specified by --target commandline option
    def test_attack(self, client):
        if self.real_target == None:
            return False
        response = self.attack(client, self.real_target)
        assert response.status_code == 200

    # Run attack against target, use --target flag when running test
    def attack(self, client, target):
        return client.post('/atc', data=dict(attackAddress=target), follow_redirects=True)

    # Enable all tests
    def enable(self, client): 
        return client.post('/auto-enable', data=dict(sortAll='1'), follow_redirects=True)

    # Test enable all tests
    def test_enable(self, client):
        response = self.enable(client)
        assert response.status_code == 200

    # Disable all tests
    def disable(self, client): 
        return client.post('/auto-enable', data=dict(sortAll='0'), follow_redirects=True)

    # Test disable all tests
    def test_disable(self, client):
        response = self.disable(client)
        assert response.status_code == 200

    # Change difficulty
    def diff_change(self, client, difficulty):
        return client.post('/diff-change', data=dict(diffSelect=difficulty), follow_redirects=True)

    # Test change difficulty to master
    def test_diff_change(self, client):
        response = self.diff_change(client, 'Master')
        assert b'\"selected\">Master' in response.data

    # Check for changes in enabled tests
    def check_change(self, client):
        return client.post('/check-change', data=dict(check=True), follow_redirects=True) 

    # Test check change
    def test_check_change(self, client):
        response = self.check_change(client)
        assert response.status_code == 200

    # Change the test strength and threshold
    def strength_change(self, client, strength, threshold):
        return client.post('/strength-change', data=dict(strengthSelect=strength, thresholdSelect=threshold), follow_redirects=True)

    # Test changing strength and threshold to medium
    def test_strength_change(self, client):
        response = self.strength_change(client, 'Medium', 'Medium')
        assert response.data.count(b'<option selected=\"selected\">Medium</option>') == 2

    # Stop running  tests
    def stop(self, client):
        return client.post('/stop', follow_redirects=True)

    # Test starting and then stopping running tests
    def test_stop(self, client):
        self.attack(client, self.real_target)
        time.sleep(2)
        response = self.stop(client)
        assert response.status_code == 200

    def main(self):
        # extract target from command line
        print('Extracted arg is ==> %s' % sys.argv[1])
        pytest.main([sys.argv[1]])
