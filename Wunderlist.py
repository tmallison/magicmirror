import json
import traceback
from tkinter import *
import requests

from settings import medium_text_size, small_text_size

REFRESH_RATE = 60000

ACCESS_TOKEN = "332c08cb64ad807d265bea88765f20ec6c843f81882aa57228b60ee0ca49"
CLIENT_ID = "8ea9ab3c56a5a558688a"
HOME_LIST_ID = 327759681
HEAD = {'X-Access-Token': ACCESS_TOKEN,
        'X-Client-ID': CLIENT_ID}


class TaskFrame(Frame):
    def __init__(self, parent, text, text_size=small_text_size):
        Frame.__init__(self, parent, bg='black')
        self.task_lbl = Label(self, text="- {}".format(text), font=('Helvetica', text_size), fg="white", bg="black")
        self.task_lbl.pack(side=LEFT, anchor=N)


class WunderlistFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.config(bg='black')
        self.title = 'Wunderlist'
        self.wunderlist_lbl = Label(self, text=self.title, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.wunderlist_lbl.pack(side=TOP, anchor=W)
        self.wunderlist_container = Frame(self, bg="black")
        self.wunderlist_container.pack(side=TOP)
        self.display_all_tasks()

    def display_all_tasks(self):
        try:
            # remove all children
            for widget in self.wunderlist_container.winfo_children():
                widget.destroy()

            tasks = self.get_tasks_in_list(HOME_LIST_ID)
            print(tasks)

            for task in tasks[0:10]:
                task_frame = TaskFrame(self.wunderlist_container, task)
                task_frame.pack(side=TOP, anchor=W)

        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get to Wunderlist." % e)

        self.after(REFRESH_RATE, self.display_all_tasks)

    def get_tasks_in_list(self, list_id):
        url = "http://a.wunderlist.com/api/v1/tasks"
        response = requests.get(url, headers=HEAD, params={"list_id": list_id})
        tasks = json.loads(response.text)

        return [t["title"] for t in tasks]
