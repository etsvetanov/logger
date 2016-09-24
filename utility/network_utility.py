import urllib2
import json


def internet_on():
    try:
        response=urllib2.urlopen('https://www.google.bg', timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False


def get_own_ip():
    try:
        content = urllib2.urlopen("https://api.ipify.org?format=json").read()
        ip_address = json.loads(content)
        return ip_address['ip']
    except:
        return ''