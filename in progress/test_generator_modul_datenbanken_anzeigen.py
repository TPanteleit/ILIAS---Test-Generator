import xml.etree.ElementTree as ET
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import pandas as pd
import sqlite3
import tkinter as tk
from tkscrolledframe import ScrolledFrame  #Bewegbares Fesnter (Scrollbalken)

class _setit:
    """Internal class. It wraps the command in the widget OptionMenu."""
    def __init__(self, var, value, callback=None):
        self.__value = value
        self.__var = var
        self.__callback = callback
    def __call__(self, *args):
        self.__var.set(self.__value)
        if self.__callback:
            self.__callback(self.__value, *args)

class MainGUI:
    def __init__(self, app, sql_database_name, sql_table_name):
        # self.master = master   + in übergabe (self, master)
        conn = sqlite3.connect(sql_database_name + '.db')
        df = pd.read_sql_query("SELECT *, oid FROM " + sql_table_name, conn)

        cursor = conn.cursor()
        cursor.execute("SELECT *, oid FROM " + sql_table_name)
        self.db_records = cursor.fetchall()

        self.db_records_listing = []
        for self.db_record in self.db_records:
            self.db_records_listing.append(len(self.db_records))

        print("Anzahl Einträge: " + str(len(self.db_records_listing)))

        conn.commit()
        conn.close()

        win = tk.Tk()

       # scrollable Frame
        self.sf_database = ScrolledFrame(win, width=500, height=500)
        self.sf_database.pack(expand=1, fill="both")

        # Create a frame within the ScrolledFrame
        self.db_inner_frame = self.sf_database.display_widget(Frame)

       #win.resizable(width=0, height=0)
        self.tree = ttk.Treeview(self.db_inner_frame, selectmode="browse", height=30)
        self.tree.pack(fill="both", expand = 1)
        #self.tree.pack(side='left')

        #vsb = ttk.Scrollbar(win, orient="vertical", command=self.tree.yview)
        #vsb.pack(side='right', fill='y')

        #self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(win, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')


        self.tree['show'] = 'headings'
        self.tree["columns"] = df.columns.values.tolist()
        for i, header in enumerate(df.columns.values.tolist()):
            self.tree.column(i, width=100)
            self.tree.heading(i, text=header)
        for row in df.iterrows():
            self.tree.insert("", 'end', values=list(row[1]))
        self.tree.bind("<Button-3>", self.preClick)
        self.tree.bind("<Button-1>", self.onLeft)

        self.tree["displaycolumns"] = df.columns.values.tolist()[0:(len(self.db_records_listing)-7)]


        def add_to_header(val):
            new = list(self.tree["displaycolumns"])
            new.append(val)
            self.tree["displaycolumns"] = new
            self.update_option_menu()


        def rem_from_header(val):
            print(val)
            new = list(self.tree["displaycolumns"])
            new.remove(val)
            self.tree["displaycolumns"] = new
            self.update_option_menu()

        add_var = StringVar(app)
        add_var.set(self.tree["columns"])
        add = OptionMenu(win, add_var, *self.tree["columns"], command=add_to_header)

        self.rem_var = StringVar(app)
        self.rem_var.set(self.tree["displaycolumns"])
        self.rem = OptionMenu(win, self.rem_var, *self.tree["displaycolumns"], command=rem_from_header)
        Label(win, text="Spalte ausblenden:", font=("bold", 11)).pack()
        add.pack(side="top")
        Label(win, text="Spalte einblenden:", font=("bold", 11)).pack()
        self.rem.pack(side="top")


    def update_option_menu(self):
        def rem_from_header(val):
            print(val)
            new = list(self.tree["displaycolumns"])
            new.remove(val)
            self.tree["displaycolumns"] = new
            self.update_option_menu()
        menu = self.rem["menu"]
        menu.delete(0, "end")
        for string in self.tree["displaycolumns"]:
            menu.add_command(label=string, command=_setit(self.rem_var, string, rem_from_header))


    def onRight(self):
        cursorx = int(self.master.winfo_pointerx() - self.master.winfo_rootx())
        cursory = int(self.master.winfo_pointery() - self.master.winfo_rooty())
        self.menu = Canvas(self.win, width=150, height=40, highlightthickness=1, highlightbackground="black")
        self.menu.place(x=cursorx, y=cursory)
        self.menu.pack_propagate(0)
        delLabel = Label(self.menu, text="  Markierte Zeile löschen", cursor="hand2", anchor="w")
        delLabel.pack(side="top", padx=1, pady=1, fill="x")
        loadLabel = Label(self.menu, text="  Markierte Frage in Tool laden", cursor="hand2", anchor="w")
        loadLabel.pack(side="top", padx=1, pady=1, fill="x")


        def destroy():
            self.menu.place_forget()

        def delete(*args):
            selection = self.tree.selection()
            self.tree.delete(selection)
            destroy()

        delLabel.bind("<Button-1>", delete)

    def preClick(self, *args):
        try:
            self.menu.place_forget()
            self.onRight()
        except AttributeError:
            self.onRight()

    def onLeft(self, *args):
        self.curItem = self.tree.focus()
        print(self.tree.item(self.curItem)["values"][-1])
        try:
            self.menu.place_forget()
        except AttributeError:
            pass

    def selectItem(self, a):
        curItem = self.tree.focus()
        print(self.tree.item(curItem)["values"][-1])



