from tkinter import *
from tkinter import ttk
import tkinter as tk

class Test_Time_UI():
    def __init__(self, frame, bg_color, label_color, Label_Font):
        self.Frame = frame

        self.ff_processing_time_label = Label(self.Frame, text="Std:", bg=label_color, fg=bg_color)
        self.ff_processing_time_label['font'] = Label_Font
        self.ff_processing_time_label.pack(side=LEFT, padx=6, anchor="s")
        self.ff_proc_hours_box = ttk.Combobox(self.Frame, value=list(range(24)), width=2)
        self.ff_proc_hours_box.pack(side=LEFT, padx=6, anchor="s")

        self.ff_processing_time_label = Label(self.Frame, text="Min:", bg=label_color, fg=bg_color)
        self.ff_processing_time_label.pack(side=LEFT, padx=6, anchor="s")
        self.ff_processing_time_label['font'] = Label_Font
        self.ff_proc_minutes_box = ttk.Combobox(self.Frame, value=list(range(60)), width=2)
        self.ff_proc_minutes_box.pack(side=LEFT, padx=6, anchor="s")

        self.ff_processing_time_label = Label(self.Frame, text="Sek:", bg=label_color, fg=bg_color)
        self.ff_processing_time_label.pack(side=LEFT, padx=6, anchor="s")
        self.ff_processing_time_label['font'] = Label_Font
        self.ff_proc_seconds_box = ttk.Combobox(self.Frame, value=list(range(60)), width=2)
        self.ff_proc_seconds_box.pack(side=LEFT, padx=6, anchor="s")

        self.set_time()


    def get_time(self):
        return("",self.ff_proc_hours_box.get(),":" ,self.ff_proc_minutes_box.get(),":", self.ff_proc_seconds_box.get(),"")

    def set_time(self, time="00:00:00"):

        self.ff_proc_hours_box.current(int(time[0:2]))
        self.ff_proc_minutes_box.current(int(time[3:5]))
        self.ff_proc_seconds_box.current(int(time[6:8]))