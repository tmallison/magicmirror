import traceback
from pprint import pprint
from tkinter import *
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.cElementTree as ET

from settings import medium_text_size, small_text_size

ns_credentials_user = "thomas68allison@hotmail.com"
ns_credentials_password = "8ozlr3V3JfyM-_eLfwUEpLGp12AX9rCds0DoPnhmIAmCtlIedaS_Cw"


class DelayedTrainInfo(Frame):
    def __init__(self, parent, event_name=""):
        Frame.__init__(self, parent, bg='black')

        self.eventName = event_name
        self.eventNameLbl = Label(self, text=self.eventName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.eventNameLbl.pack(side=LEFT, anchor=N)


class NSFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'NS'
        self.trains_lbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.trains_lbl.pack(side=TOP, anchor=W)
        self.trains_container = Frame(self, bg="black")
        self.trains_container.pack(side=TOP)
        self.display_all_delayed_trains()

    def display_all_delayed_trains(self):
        try:
            # remove all children
            for widget in self.trainsContainer.winfo_children():
                widget.destroy()

            delayed_trains = self.get_all_delayed_trains()

            for train in delayed_trains[0:5]:
                headline = NewsHeadline(self.headlinesContainer, post.title)
                headline.pack(side=TOP, anchor=W)

            # todo if count is more than 5 add dots
        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get NS info." % e)

        self.after(600000, self.get_headlines)

    def get_all_delayed_trains(self):
        xml = self.get_ns_departure()
        delayed_trains = []

        for train_info in xml:
            train_dict = {}
            add_to_list = False
            for train in train_info:
                train_dict[train.tag] = train.text
                if "vertraging" in train.tag.lower():
                    add_to_list = True

            if add_to_list:
                delayed_trains.append(train_dict)

        return delayed_trains

    def get_ns_departure(self):
        url = 'https://webservices.ns.nl/ns-api-avt?station=LEDN'

        response = requests.get(url, auth=self.get_ns_credentials(), stream=True)

        return ET.fromstring(response.content)

    def get_ns_credentials(self):
        return HTTPBasicAuth(ns_credentials_user, ns_credentials_password)
