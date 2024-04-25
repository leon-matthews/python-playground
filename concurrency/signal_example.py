"""
Play around with the standard-library OS signal module.
"""

import os
import signal


def receive_alarm(signum, stack):
    """
    SIGALRM from OS received (not available on Windows).
    """
    print("Alarm from OS received", signum)


def receive_interupt(signum, stack):
    """
    Handle (and ignore!) SIGINT, ctrl+c.
    """
    print("Did you just try and ctrl-c me?", signum)


def receive_shutdown(signum, stack):
    """
    Intercep (not ignorable) SIGTERM, ctrl+\
    """
    print('Shutdown imminent:', signum)


signal.signal(signal.SIGALRM, receive_alarm)
signal.signal(signal.SIGINT, receive_interupt)
signal.signal(signal.SIGTERM, receive_shutdown)


if __name__ == '__main__':
    # Print the process ID so it can be used with 'kill'
    print('My PID is:', os.getpid())

    # Have OS send SIGALRM (14) in 5 seconds
    signal.alarm(1)

    while True:
        pass
