"""
Simple script to check the time and issue a shutdown command if the time is between
a given range

TODO:
Allow user to pass parameters from the CLI
"""
#! /usr/bin/python3

import datetime
import time
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
    TIME_NOW = datetime.datetime.now()
    HOURS = TIME_NOW.hour
    MINUTES = TIME_NOW.minute
    send_notification(60)

    if not (HOURS >= 23 and MINUTES >= 45) or (HOURS > 7 and MINUTES > 00):
        exit()
