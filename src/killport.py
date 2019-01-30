#!/usr/bin/env python
import os
import subprocess


def kill_port(port):

    errMsg = None

    try:
        errMsg = 'Enter integer value for port number'
        port = port
        cmd = 'lsof -t -i:{0}'.format(port)
        pid = subprocess.check_output(cmd, shell=True)
        pid = int(pid)
        isKilled = os.system('kill -9 {0}'.format(pid)) if pid else None
        if isKilled == 0:
            print("Port {0} is free. Processs {1} killed successfully".format(port, pid))
        else:
            print("Cannot free port {0}.Failed to kill process {1}, err code:{2}".format(port, pid, isKilled))
    #except ValueError:
    #    print(errMsg)
    #    exit()
    except Exception as e:
        print("No process running on port {0}".format(port))
        pass

