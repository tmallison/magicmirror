from tkinter import *
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.cElementTree as ET

ns_credentials_user = "thomas68allison@hotmail.com"
ns_credentials_password = "8ozlr3V3JfyM-_eLfwUEpLGp12AX9rCds0DoPnhmIAmCtlIedaS_Cw"


class NSFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        print(self.get_ns_departure())


def get_all_trains():
    xml = get_ns_departure()

    print(xml.tag)

    for train_info in xml:
        # print(train_info)
        print("=========")
        for train in train_info:
            print(vars(train))



def get_ns_departure():
    url = 'https://webservices.ns.nl/ns-api-avt?station=LEDN'

    response = requests.get(url, auth=get_ns_credentials(), stream=True)

    return ET.fromstring(response.content)


def get_ns_credentials():
    return HTTPBasicAuth(ns_credentials_user, ns_credentials_password)


get_all_trains()
