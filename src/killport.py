#!/usr/bin/env python

from psutil import process_iter
from signal import SIGTERM  # or SIGKILL


def kill_port(port):

    for proc in process_iter():
        for conns in proc.connections():
            if conns.laddr.port == port:
                proc.send_signal(SIGTERM)  # or SIGKILL
