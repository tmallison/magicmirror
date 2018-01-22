import traceback
from tkinter import *
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.cElementTree as ET
import datetime

from settings import medium_text_size, small_text_size

REFRESH_RATE = 120000
KEYWORD = ["a'dam", "amsterdam"]

ns_credentials_user = "thomas68allison@hotmail.com"
ns_credentials_password = "8ozlr3V3JfyM-_eLfwUEpLGp12AX9rCds0DoPnhmIAmCtlIedaS_Cw"


class DelayedTrainInfo(Frame):
    def __init__(self, parent, trein_soort="", eind_bestemming="", vertrek_tijd="", vertraging_tekst=""):
        Frame.__init__(self, parent, bg='black')

        # self.event_name = trein_soort + " " + eind_bestemming + " " + vertrek_tijd + " " + vertraging_tekst
        self.event_name = "{} - {} naar {} {}".format(vertrek_tijd, trein_soort, eind_bestemming, vertraging_tekst)
        self.event_name_lbl = Label(self, text=self.event_name, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.event_name_lbl.pack(side=LEFT, anchor=N)

class GenericInfo(Frame):
    def __init__(self, parent, text, text_size=small_text_size):
        Frame.__init__(self, parent, bg='black')
        self.event_name_lbl = Label(self, text=text, font=('Helvetica', text_size), fg="white", bg="black")
        self.event_name_lbl.pack(side=LEFT, anchor=N)


class NSFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Leiden Centraal'
        self.trains_lbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.trains_lbl.pack(side=TOP, anchor=W)
        self.trains_container = Frame(self, bg="black")
        self.trains_container.pack(side=TOP)
        # self.display_all_delayed_trains()
        self.display_all_relevant_trains()

    def display_all_delayed_trains(self):
        try:
            # remove all children
            for widget in self.trains_container.winfo_children():
                widget.destroy()

            delayed_trains = self.get_all_delayed_trains()

            for train in delayed_trains[0:5]:
                ns_info = DelayedTrainInfo(self.trains_container,
                                            train.get("TreinSoort"),
                                            train.get("EindBestemming"),
                                            self.date_and_time_string_to_time(train["VertrekTijd"]),
                                            train.get("VertrekVertragingTekst"))
                ns_info.pack(side=TOP, anchor=W)

            # todo if count is more than 5 add dots
            # todo if no delays show text
            if len(delayed_trains) > 5:
                dots = GenericInfo(self.trains_container, "...")
                dots.pack(side=TOP, anchor=W)
            elif len(delayed_trains) == 0:
                dots = GenericInfo(self.trains_container, "Geen vertraging")
                dots.pack(side=TOP, anchor=W)

            # todo time it updated
        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get NS info." % e)

        self.after(REFRESH_RATE, self.display_all_delayed_trains)

    def display_all_relevant_trains(self):
        try:
            # remove all children
            for widget in self.trains_container.winfo_children():
                widget.destroy()

            all_relevant_trains = self.get_all_relevant_trains()

            for train in all_relevant_trains[0:7]:
                ns_info = DelayedTrainInfo(self.trains_container,
                                            train.get("TreinSoort"),
                                            train.get("EindBestemming"),
                                            self.date_and_time_string_to_time(train["VertrekTijd"]),
                                            train.get("VertrekVertragingTekst", ""))
                ns_info.pack(side=TOP, anchor=W)

            # todo if count is more than 5 add dots
            if len(all_relevant_trains) > 7:
                dots = GenericInfo(self.trains_container, "...")
                dots.pack(side=TOP, anchor=W)

        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get NS info." % e)

        self.after(REFRESH_RATE, self.display_all_delayed_trains)

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

    def get_all_relevant_trains(self):
        xml = self.get_ns_departure()
        relevant_trains = []

        for train_info in xml:
            train_dict = {}
            add_to_list = False
            for train in train_info:
                train_dict[train.tag] = train.text
                if any(w in train.text.lower() for w in KEYWORD):
                    add_to_list = True

            if add_to_list:
                relevant_trains.append(train_dict)

        return relevant_trains

    def get_ns_departure(self):
        url = 'https://webservices.ns.nl/ns-api-avt?station=LEDN'

        response = requests.get(url, auth=self.get_ns_credentials(), stream=True)

        return ET.fromstring(response.content)

    def get_ns_credentials(self):
        return HTTPBasicAuth(ns_credentials_user, ns_credentials_password)

    def date_and_time_string_to_time(self, date_time_string):
        date_time = datetime.datetime.strptime(date_time_string, '%Y-%m-%dT%H:%M:%S%z')

        return date_time.strftime('%H:%M')
