#! /usr/bin/python3
"""
Simple script to check the time and issue a shutdown command if the time is between
a given range

TODO:
Allow user to pass parameters from the CLI
"""

import datetime
import time
import os
import argparse
import syslog
from gi.repository import Notify

def send_notification(warning_period):
    """
    Create a notification and update it for the number of seconds passed to the function
    """

    Notify.init("shutdown cron")
    summary = "Time to go to sleep"
    body = "Computer will shut down in {} second(s)"
    seconds_to_shutdown = warning_period
    notification = Notify.Notification.new(summary, body.format(seconds_to_shutdown))
    notification.show()
    while seconds_to_shutdown > 1:
        time.sleep(1)
        seconds_to_shutdown -= 1
        notification.update(summary, body.format(seconds_to_shutdown))
        notification.show()
    notification.update(summary, "Computer shutting down now!")
    notification.show()
    notification.close()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description=\
"""Small utility to shutdown linux computers if the current time is after a given time.
Also creates a notification to inform the user that the computer will be shutdown.
(Should be used with a root cronjob)""",\
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    PARSER.add_argument("--timeout", type=int, help=\
        "Notification timeout (negative number for no notification).",\
        default=60)
    PARSER.add_argument("--start", help="Bounding start time to shutdown the computer from",\
        default="23:15")
    PARSER.add_argument("--end",\
        help="Bounding end time for when the computer should be shutdown",\
        default="07:00")
    ARGS = PARSER.parse_args()

    START_TIME = ARGS.start.split(":")
    END_TIME = ARGS.end.split(":")

    TIME_NOW = datetime.datetime.now()
    HOURS = TIME_NOW.hour
    MINUTES = TIME_NOW.minute

    if TIME_NOW.time() < datetime.time(int(START_TIME[0]), int(START_TIME[1])) and\
        TIME_NOW.time() > datetime.time(int(END_TIME[0]), int(END_TIME[1])):
        exit()

    if ARGS.timeout >= 0:
        syslog.syslog("Shutting down computer in {} seconds!".format(ARGS.timeout))
        send_notification(ARGS.timeout)
    syslog.syslog("Exucting shutdown command now!")
    os.system("/sbin/shutdown now -h")
