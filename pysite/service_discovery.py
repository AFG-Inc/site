import datetime
import socket
import time
from contextlib import closing

from pysite.constants import RMQ_HOST, RMQ_PORT

THIRTY_SECONDS = datetime.timedelta(seconds=30)


def wait_for_rmq():
    start = datetime.datetime.now()

    while True:
        if datetime.datetime.now() - start > THIRTY_SECONDS:
            return False

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((RMQ_HOST, RMQ_PORT)) == 0:
                return True

        time.sleep(0.5)
