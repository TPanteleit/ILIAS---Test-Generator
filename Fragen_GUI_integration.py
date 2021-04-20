from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3

class Fragen_GUI():
    def __init__(self, Frame, gesucht, dbname, *args, **kwargs):
        self.mydb = sqlite3.connect(dbname)
        self.gesucht = gesucht
        self.cursor = self.mydb.cursor()
        self.work_window = Toplevel()
        self.q = (StringVar(), 'Schwierigkeit'), (StringVar(), 'Typ'), (StringVar(), 'Titel'), (StringVar(), 'Author'), (StringVar(), 'Datum'), (StringVar(), 'Author2'), (StringVar(), 'Datum2')
        self.titel = StringVar()
        WIDTH = int(Frame.winfo_screenwidth() / 2)
        HEIGHT = int(Frame.winfo_screenheight() / 2)
        self.work_window.title("DB_List")
        self.work_window.resizable(False, False)
        self.work_window.geometry("%dx%d" % (WIDTH, HEIGHT))
        self.UI_Elemente()

        self.Read_Entry_btn = Button(self.work_window, text="read entry", command=self.display_entry)
        self.Read_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Add_Entry_btn = Button(self.work_window, text="Frage in DB erstellen", command=self.Add_data_to_DB)
        self.Add_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Save_btn = Button(self.work_window, text="Save Changes", command=self.Save_Change_to_DB)
        self.Save_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Search_Entry = Entry(self.work_window, textvariable=self.titel)
        self.Search_Entry.pack(side=tk.TOP, padx=6, anchor="s")

    def UI_Elemente(self):
        self.Schwierigkeit_label = Label(self.work_window, text="Schwierigkeit")
        self.Schwierigkeit_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Schwierigkeit_Entry = Entry(self.work_window, textvariable=self.q[0][0])
        self.Schwierigkeit_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Type_label = Label(self.work_window, text="Type" )
        self.Type_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Type_Entry = Entry(self.work_window, textvariable=self.q[1][0])
        self.Type_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Titel_label = Label(self.work_window, text="Titel:")
        self.Titel_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Titel_Entry = Entry(self.work_window, textvariable=self.q[2][0])
        self.Titel_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Author_label = Label(self.work_window, text="Author:")
        self.Author_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Author_Entry = Entry(self.work_window, textvariable=self.q[3][0])
        self.Author_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Datum_label = Label(self.work_window, text="Datum:")
        self.Datum_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Datum_Entry = Entry(self.work_window, textvariable=self.q[4][0])
        self.Datum_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Author2_label = Label(self.work_window, text="Author2:")
        self.Author2_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Author2_Entry = Entry(self.work_window, textvariable=self.q[5][0])
        self.Author2_Entry.pack(side=tk.TOP, padx=6, anchor="w")

        self.Datum2_label = Label(self.work_window, text="Datum2:")
        self.Datum2_label.pack(side=tk.TOP, padx=6, anchor="w")
        self.Datum2_Entry = Entry(self.work_window, textvariable=self.q[6][0])
        self.Datum2_Entry.pack(side=tk.TOP, padx=6, anchor="w")

    def display_entry(self):
        for i in self.q:
            #print(i[0].get(), i[1])

    def Add_data_to_DB(self):
        self.cursor.execute("INSERT INTO testdb (Titel) VALUES (:Titel)", {'Titel': self.q[2][0].get()})
        self.mydb.commit()
        for i in self.q:
            self.cursor.execute("UPDATE testdb SET '" + i[1] + "' = :Value WHERE Titel LIKE '%" + self.q[2][0].get() + "%'", {'Value': i[0].get()})
            self.mydb.commit()
        self.update()

    def Save_Change_to_DB(self):
        for i in self.q:
            self.cursor.execute("UPDATE testdb SET '" + i[1] + "' = :Value WHERE Titel LIKE '%" + self.current_ID_Titel + "%'", {'Value': i[0].get()})
            self.mydb.commit()
        self.update()

class Neue_Frage(Fragen_GUI):
    def __init__(self, Frame, gesucht, dbname, update, *args, **kwargs):
        self.update = update
        self.mydb = sqlite3.connect(dbname)
        self.gesucht = gesucht
        self.cursor = self.mydb.cursor()
        self.work_window = Toplevel()
        self.q = (StringVar(), 'Schwierigkeit'), (StringVar(), 'Typ'), (StringVar(), 'Titel'), (StringVar(), 'Author'), (StringVar(), 'Datum'), (StringVar(), 'Author2'), (StringVar(), 'Datum2')
        WIDTH = int(Frame.winfo_screenwidth() / 2)
        HEIGHT = int(Frame.winfo_screenheight() / 2)
        self.work_window.title("DB_List")
        self.work_window.resizable(False, False)
        self.work_window.geometry("%dx%d" % (WIDTH, HEIGHT))
        self.UI_Elemente()
        #self.Type_Entry.delete(0, 'end')#todo was macht das ich denke das kann weg
        #Db_cont = str(self.cursor.fetchone())#todo was macht das ich denke das kann weg
        #self.Titel_Entry.insert(0, Db_cont)#todo was macht das ich denke das kann weg
        self.Read_Entry_btn = Button(self.work_window, text="read entry", command=self.display_entry)
        self.Read_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Add_Entry_btn = Button(self.work_window, text="Frage in DB erstellen", command=self.Add_data_to_DB)
        self.Add_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

class Frage_bearbeiten(Fragen_GUI):
    def __init__(self, Frame, gesucht, dbname, update, *args, **kwargs):
        self.update = update
        self.mydb = sqlite3.connect(dbname)
        self.gesucht = gesucht
        self.cursor = self.mydb.cursor()
        self.work_window = Toplevel()
        self.q = (StringVar(), 'Schwierigkeit'), (StringVar(), 'Typ'), (StringVar(), 'Titel'), (StringVar(), 'Author'), (StringVar(), 'Datum'), (StringVar(), 'Author2'), (StringVar(), 'Datum2')
        self.titel = StringVar()
        WIDTH = int(Frame.winfo_screenwidth() / 2)
        HEIGHT = int(Frame.winfo_screenheight() / 2)
        self.work_window.title("DB_List")
        self.work_window.resizable(False, False)
        self.work_window.geometry("%dx%d" % (WIDTH, HEIGHT))
        self.UI_Elemente()
        self.Fill_Entrys_From_DB()
        self.Read_Entry_btn = Button(self.work_window, text="read entry", command=self.display_entry)
        self.Read_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Add_Entry_btn = Button(self.work_window, text="Frage in DB erstellen", command=self.Add_data_to_DB)
        self.Add_Entry_btn.pack(side=tk.TOP, padx=6, anchor="s")

        self.Save_btn = Button(self.work_window, text="Save Changes", command=self.Save_Change_to_DB)
        self.Save_btn.pack(side=tk.TOP, padx=6, anchor="s")

    def Fill_Entrys_From_DB(self):
        self.cursor.row_factory = lambda cursor, row: row[0]
        self.current_ID_Titel = self.gesucht['values'][2]
        for i in self.q:
            #i[0].delete(0, END)
            self.cursor.execute(
                "SELECT " + i[1] + " FROM testdb WHERE  Titel = '" + self.gesucht['values'][2] +"'")
            Db_cont = str(self.cursor.fetchone())
            #print(Db_cont)
            #print(i[1])
            i[0].set(Db_cont)
        self.cursor.row_factory = None

if __name__ == "__main__":
    root = tk.Tk()
    WIDTH = int(root.winfo_screenwidth() / 1.5)
    HEIGHT = int(root.winfo_screenheight() / 2)
    root.title("DB_List")
    root.resizable(False, False)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    gesucht = 'Spannungsteiler 2'
    dbname = '../testdb.db'
    lbl = tk.Label(text="Das ist das Main Window")
    Fragen_Frame = Fragen_GUI(root, gesucht, dbname)
    root.mainloop()