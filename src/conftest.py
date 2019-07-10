# this is just so we can pass --server and --port from the pytest command-line
def pytest_addoption(parser):
    ''' attaches optional cmd-line args to the pytest machinery '''
    parser.addoption("--target", action="append", default=[], help="real server URL")


