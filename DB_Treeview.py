from tkinter import *
import tkinter as tk
from tkinter import ttk
from Fragen_GUI import formelfrage, singlechoice, multiplechoice, zuordnungsfrage
from ScrolledText_Functionality import Textformatierung

class UI():
    def __init__(self,table_dict , db_interface, frame, screenwidth, ID, table_index_list, table_index_dict, Title, bg_color, button_color, label_color, Button_Font, Label_Font, *args, **kwargs):
        # self.active = False
        self.table_dict = table_dict
        self.bg_color = bg_color
        self.button_color = button_color
        self.label_color = label_color
        self.Button_Font = Button_Font
        self.Label_Font = Label_Font
        rel_Top_Abstand = .15
        self.active = False # Aktivitätsflag für Such Eingabefeld
        self.rel_Top_Abstand = rel_Top_Abstand
        self.table_index_list = table_index_list #hier sind die header/index und die StringVar instanzen für jeden table
        self.table_index_dict = table_index_dict
        self.ScrText = Textformatierung()
        print("das ist in Treeview", table_index_list[0][1][1])
        self.ID = ID
        self.db_I = db_interface
        self.db_I.subscribe(self.update)
        self.Frame = frame
        self.trv_spec_Frame = Frame(frame)
        self.trv_spec_Frame.place(relx=0, rely=.1)
        #self.Width = screenwidth
        self.Width = int(frame.winfo_screenwidth() / 1.25)
        print("screenwidth of TRV Frame", self.Width)
        self.create_style()
        self.q = StringVar()
        self.create_trv()
        #self.Searchbox('blue')
        self.db_I.get_complete_DB(self.ID)
        self.trv.bind('<Double-Button-1>', self.Select_from_DB)
        self.Searchbox("blue", Title, rel_Top_Abstand)
        self.ent.bind('<Return>', self.search)
        self.ent.bind('<FocusIn>', self.delete_placeholder)
        self.ent.bind('<FocusOut>', self.delete_placeholder)
        #self.ent.bind('<Return>', self.search)
        print('init finished')

    def create_trv(self):
        # Create Treview Frame
        self.DB_frame = tk.Frame(self.Frame)
        self.DB_frame.place(relx=0, rely=self.rel_Top_Abstand)
        # create Scrollbar
        self.vsb = ttk.Scrollbar(self.DB_frame)
        self.vsb.pack(side=RIGHT, fill=Y)
        # create Treeview
        self.trv = ttk.Treeview(self.DB_frame, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height=9,
                                style="mystyle.Treeview")
        self.trv.configure(yscrollcommand=self.vsb.set)
        self.trv.tag_configure('odd', background='#ff5733')
        self.trv.pack(fill=BOTH)
        # Create Treeview Headings
        self.trv.heading(1, text=self.table_index_list[0][0][1])
        self.trv.heading(2, text=self.table_index_list[0][1][1])
        self.trv.heading(3, text=self.table_index_list[0][2][1])
        self.trv.heading(4, text=self.table_index_list[0][3][1])
        self.trv.heading(5, text=self.table_index_list[0][4][1])
        self.trv.heading(6, text=self.table_index_list[0][189][1])
        self.trv.heading(7, text="Datum")
        #self.trv.heading(8, text="Zuletzt verändert")
        # Format Columns
        self.trv.column(1, width=int(self.Width / 9), anchor=CENTER,
                        minwidth=int(self.Width / 30))
        self.trv.column(2, width=int(self.Width / 9), anchor=CENTER,
                        minwidth=int(self.Width / 30))
        self.trv.column(3, width=int(self.Width / 9), anchor=W,
                        minwidth=int(self.Width / 30))
        self.trv.column(4, width=int(self.Width / 9), anchor=W,
                        minwidth=int(self.Width / 30))
        self.trv.column(5, width=int(self.Width / 9), anchor=CENTER,
                        minwidth=int(self.Width / 30))
        self.trv.column(6, width=int(self.Width / 9), anchor=W,
                        minwidth=int(self.Width / 30))
        self.trv.column(7, width=int(self.Width / 10), anchor=CENTER,
                        minwidth=int(self.Width / 30))
        print('trv created')

    def create_style(self):
        # Create Stryle for treeview
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Verdana', 8))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Verdana', 10, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        print('style created')



    def Searchbox(self, color, Title, rel_Top_Abstand):
        bd_Frame = tk.Frame(self.Frame, bg=self.label_color)
        bd_Frame.place(relx=0, rely=0, relwidth=1, relheight=rel_Top_Abstand)
        SearchBox = tk.Frame(bd_Frame, bg=self.label_color)
        SearchBox.place(relx=0, rely=0.2, relwidth=1, relheight=.8)
        Title_Label = Label(bd_Frame, text=Title, anchor='w', bd=5, bg=self.label_color, fg=self.bg_color)
        Title_Label['font'] = self.Label_Font
        Title_Label.place(relx=0, rely=0, relwidth=.25, relheight=1)
        self.ent = Entry(SearchBox, textvariable=self.q, fg="grey")
        self.q.set("Suche")
        self.ent.place(relx=0.7, rely=0, relwidth=.1, relheight=1)
        cbtn = Button(SearchBox, text="zurücksetzen", command=self.clear, bg=self.button_color, fg=self.bg_color)
        cbtn['font'] = self.Button_Font
        cbtn.place(relx=0.80, rely=0, relwidth=.1, relheight=1)
        del_btn = Button(SearchBox, text="löschen", command=self.delete_selection, bg=self.button_color, fg=self.bg_color)
        del_btn['font'] = self.Button_Font
        del_btn.place(relx=0.90, rely=0, relwidth=.1, relheight=1)

    def clear(self):
        self.db_I.get_complete_DB(0)

    def search(self, a):
        q = self.q.get() #get search text from entry
        self.db_I.search_DB(q, 0)

    def delete_selection(self):
        i = 0
        item_list = []

        for selection in self.trv.selection():
            item_list.append(self.trv.item(selection))
            print(self.trv.item(selection))
            print(i)
            i = i + 1
        self.db_I.delete_DB_content(item_list, self.ID)

    def neue_fromelfrage(self, choice_window):
        choice_window.destroy()
        work_window = Toplevel()
        Work_on_question = formelfrage(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list, self.table_index_dict, self.bg_color, self.label_color, self.button_color)
        #self.db_I.empty_fragenauswahl()

    def neue_singlechoicefrage(self,choice_window):
        choice_window.destroy()
        work_window = Toplevel()
        work_on_question = singlechoice(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                        self.table_index_dict, self.bg_color, self.label_color, self.button_color)
    def neue_multiplechoicefrage(self,choice_window):
        choice_window.destroy()
        work_window = Toplevel()
        work_on_question = multiplechoice(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                        self.table_index_dict, self.bg_color, self.label_color, self.button_color)

    def neue_zuordnungsfrage(self,choice_window):
        choice_window.destroy()
        work_window = Toplevel()
        work_on_question = zuordnungsfrage(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                        self.table_index_dict, self.bg_color, self.label_color, self.button_color)

    def choose_qt_typ(self):
        work_window = Toplevel(bg=self.bg_color)
        work_window.geometry("%dx%d+%d+%d" % (self.Width/4, self.Width/10, self.Width/2, self.Width/4))
        Menu_lbl = Label(work_window, text="Wählen Sie einen Fragentyp um Fortzufahren", bg=self.label_color, fg=self.bg_color)
        Menu_lbl['font'] = self.Label_Font
        Menu_lbl.pack(side="top", fill=X)
        formelfrage = Button(work_window, text="Formelfrage", bg=self.button_color, fg=self.bg_color, command=lambda: self.neue_fromelfrage(work_window))
        formelfrage['font'] = self.Button_Font
        formelfrage.pack(side="top", fill=X)
        singlechoice = Button(work_window, text="Single Choice Frage", bg=self.button_color, fg=self.bg_color, command=lambda: self.neue_singlechoicefrage(work_window))
        singlechoice['font'] = self.Button_Font
        singlechoice.pack(side="top", fill=X)
        multiplechoice = Button(work_window, text="Multiple Choice Frage", bg=self.button_color, fg=self.bg_color, command=lambda: self.neue_multiplechoicefrage(work_window))
        multiplechoice['font'] = self.Button_Font
        multiplechoice.pack(side="top", fill=X)
        zuordnungsfrage = Button(work_window, text="Zuodnungsfrage", bg=self.button_color, fg=self.bg_color, command=lambda: self.neue_zuordnungsfrage(work_window))
        zuordnungsfrage['font'] = self.Button_Font
        zuordnungsfrage.pack(side="top", fill=X)

    def update(self, db_data):
        self.trv.delete(*self.trv.get_children())
        for table in db_data[self.ID]:
            for data in table:
                self.trv.insert('', 'end', values=data)
                #print("update", data)

    def add_data_to_testdb(self):
        i = 0
        item_list = []

        for selection in self.trv.selection():
            item_list.append(self.trv.item(selection))
            print(self.trv.item(selection))
            print(i)
            i = i + 1
        self.db_I.add_question_to_temp(item_list)

#selects correlating date from Treeview selection from the Original DB
    def Select_from_DB(self, a):

        Auswahl = self.trv.focus()
        gesucht = self.trv.item(self.trv.focus())
        result = str(self.trv.item(Auswahl))
        #print("Titel gesucht:", gesucht['values'][2])
        #print("Typ gesucht:", gesucht['values'][1])
        #print("das ist in Treeview", self.e[1][1])
        if gesucht['values'][2] == "formelfrage":
            work_window = Toplevel()
            work_window.title(gesucht['values'][3])
            Work_on_question = formelfrage(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list, self.table_index_dict, self.bg_color, self.label_color, self.button_color)
            self.db_I.get_question(gesucht['values'][3], 1)
        elif gesucht['values'][2] == "singlechoice":
            work_window = Toplevel()
            work_window.title(gesucht['values'][3])

            print("Hier wir in zukunft eine single Choice Frage geöffnet")
            work_on_question = singlechoice(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                          self.table_index_dict, self.bg_color, self.label_color, self.button_color)

            self.db_I.get_question(gesucht['values'][3], 1)
        elif gesucht['values'][2] == "multiplechoice":
            work_window = Toplevel()
            work_window.title(gesucht['values'][3])

            print("Hier wir in zukunft eine multiple Choice Frage geöffnet")
            work_on_question = multiplechoice(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                          self.table_index_dict, self.bg_color, self.label_color, self.button_color)

            self.db_I.get_question(gesucht['values'][3], 1)
        elif gesucht['values'][2] == "zuordnungsfrage":
            work_window = Toplevel()
            work_window.title(gesucht['values'][3])

            print("Hier wir in zukunft eine zuodnungsfrage Frage geöffnet")
            work_on_question = zuordnungsfrage(self.table_dict, work_window, self.db_I, self.ScrText, self.table_index_list,
                                          self.table_index_dict, self.bg_color, self.label_color, self.button_color)
            self.db_I.get_question(gesucht['values'][3], 1)
        else:
            print("der Fragentyp konnte nicht zugeornet werden ")


    def delete_placeholder(self, e):
        if len(self.q.get()) <1 & self.active == True:
            self.q.set("Suche")
            self.ent.configure(fg="grey")
            self.active = False
        elif  self.active == False:
            self.q.set("")
            self.ent.configure(fg="black")
            self.active = True


