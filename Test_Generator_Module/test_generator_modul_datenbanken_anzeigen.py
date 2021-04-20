import xml.etree.ElementTree as ET
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import numpy as np
import pandas as pd
import sqlite3
import tkinter as tk
from tkscrolledframe import ScrolledFrame  #Bewegbares Fesnter (Scrollbalken)


class MainGUI:
    def __init__(self, sql_database_name, sql_table_name):
        # self.master = master   + in übergabe (self, master)
        #conn = sqlite3.connect(sql_database_name + '.db')
        conn = sqlite3.connect(sql_database_name)
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
        win.title('Datenbank - Anzahl der Einträge: ' + str(len(self.db_records_listing)))

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

       # self.tree.bind("<Button-3>", self.preClick)
       # self.tree.bind("<Button-1>", self.onLeft)

        #self.tree["displaycolumns"] = df.columns.values.tolist()[0:(len(self.db_records_listing)-7)]

        # Alle Spalten-Einträge in Datenbank Übersicht zeigen
        self.tree["displaycolumns"] = df.columns.values.tolist()
