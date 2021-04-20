import sqlite3
from tkinter import *

class DB_Interface():
    def __init__(self, dbname, tempdbname, root, table_dict, *args, **kwargs):
        self.root = root
        self.listeners = []
        self.all_data = []
        self.db_data = [self.all_data, None, None, False] #broadcast data 1:Datenbak auswahl 2:Einzelne Frage aus Datenbank 3: daten in Temp datenbank 4:
        self.table = 'formelfrage'
        self.table_dict = table_dict
        self.table_list = ['formelfrage', 'singlechoice', 'multiplechoice', 'zuordnungsfrage']
        #self.q = q
        # Insert Data from Database
        self.mydb = sqlite3.connect(dbname)
        self.cursor = self.mydb.cursor()
        self.mytempdb = sqlite3.connect(tempdbname)
        self.tempcursor = self.mytempdb.cursor()
        for table in self.table_list:# Temporäre Datenbank wird gelöscht
            self.tempcursor.execute("DELETE  FROM " + table + "")
        self.mytempdb.commit()
        self.cursorlist = [self.cursor, self.cursor, self.tempcursor]
        self.dblist = [self.mydb, None, self.mytempdb]

    def search_DB(self, q2, id): #todo hier wird zwar jeder Table durchsucht aber noch nicht jedes Erbgenis zurückgegeben
        zwischenspeicher = []
        for table in self.table_list:
            self.query = " SELECT " + self.index_list[0][1] + ", " + self.index_list[1][1] + ", " + self.index_list[2][1] + ", " + self.index_list[3][1] + ", " + self.index_list[4][1] + " FROM " + table + " Where " + self.index_list[0][1] + " LIKE '" + q2 + "' OR " + self.index_list[1][1] + " LIKE '" + q2 + "' OR " + self.index_list[2][1] + " LIKE '" + q2 + "' OR " + self.index_list[3][1] + " LIKE '" + q2 + "' "
            self.cursor.execute(self.query)
            #print(self.cursor.fetchall())
            zwischenspeicher.append(self.cursor.fetchall())
        print(zwischenspeicher)
        self.db_data[id] = zwischenspeicher
        self.notify()

    def does_title_exist(self, title): #todo testing required

        print("does title exist", title)
        for table in self.table_list:
            self.query = " SELECT * FROM " + table + " WHERE " + self.table_index_list[self.table_dict[table]][3][1] + " = '" + title + "' "
            self.cursor.execute(self.query)
            vergleich = self.cursor.fetchone()
            print("das wurde in der DB gesucht", title)
            print("das wurde in der DB gefunden", vergleich)
            if vergleich:
                return True
            else:
                return False



    def get_question(self, q2, id): #todo testing required
        zwischenspeicher = []
        for table in self.table_list:
            query = " SELECT * FROM " + table + " WHERE " + self.index_list[3][1] + " LIKE '" + q2 + "' "
       # print(self.query)
            self.cursor.execute(query)
            zwischenspeicher.append(self.cursor.fetchone())
        print("zwischenspeicher", zwischenspeicher)
        self.db_data[id] = zwischenspeicher
        #og_title = self.db_data[id][0][3]
        #print(og_title)
        print(self.db_data[id])
        self.notify()

    def empty_fragenauswahl(self):
        self.db_data[1] = None
        self.notify()

    def get_index_info(self):
        self.table_index_list = [None, None, None, None] #hier sind die index_list elemtente für jeden table die den Fragentypenentsprechen zusammengefasst
        self.table_index_dict = [None, None, None, None] #hier sind die index_dict elemente für jeden table zusammengefasst
        i = 0
        for table in self.table_list:
            self.index_list = []
            self.index_dict = {}
            index = 0
            self.cursor.execute("PRAGMA table_info( " + table + " ) ")
            for row in self.cursor:
                Var = StringVar()
                q = (Var, row[1])
                d = {row[1] : index}

                self.index_dict.update(d)
                self.index_list.append(q)
                index = index + 1

            self.table_index_dict[i] = self.index_dict
            self.table_index_list[i] = self.index_list
            i = i + 1
            #print("index aus ", self.index_dict['question_type'])

        return self.table_index_list, self.table_index_dict

    def add_question_to_temp(self, item_list):
        zwischenspeicher = []
        table = "singlechoice"
        #print(table)

        for item in item_list:
            table = item['values'][2]
            #print("Der Eintrag mit dem Titel: ", item['values'][2], ", soll kopiert werden")
            self.cursor.execute("SELECT * FROM " + table + " WHERE " + self.index_list[3][1] + " = '" + item['values'][3] + "' ")
            data = self.cursor.fetchone()
            #print("INSERT INTO " + table + " (" + self.table_index_list[self.table_dict[table]][3][1] + ") VALUES (:Titel)", {'Titel': data[3]})
            self.tempcursor.execute("INSERT INTO " + table + " (" + self.table_index_list[self.table_dict[table]][3][1] + ") VALUES (:Titel)", {'Titel': data[3]})
            i = 0
            for item in data:
                #print("this will be copied:", item)
                self.tempcursor.execute("UPDATE " + table + " SET '" + self.table_index_list[self.table_dict[table]][i][1] + "' = :Value WHERE " + self.table_index_list[self.table_dict[table]][3][1] + " = '" + data[3] + "'", {'Value': item})
                i = i + 1
        self.mytempdb.commit()

        for table in self.table_list:
        #todo das läuft hier nicht durch database is locked heißt es
            self.query = "SELECT " + self.table_index_list[self.table_dict[table]][0][1] + ", " + self.table_index_list[self.table_dict[table]][1][1] + ", " + self.table_index_list[self.table_dict[table]][2][1] + ", " + self.table_index_list[self.table_dict[table]][3][1] + ", " + self.table_index_list[self.table_dict[table]][4][1] + " FROM " + table + ""
        #print(self.query)
            self.tempcursor.execute(self.query)
            zwischenspeicher.append(self.tempcursor.fetchall())

        self.db_data[2] = zwischenspeicher
        self.notify()

    def delete_DB_content(self, item_list, ID):
        for item in item_list:
            self.cursorlist[ID].execute(
                "DELETE  FROM " + item['values'][
                    2] + " WHERE " + self.index_list[3][1] + " = '" + item['values'][
                    3] + "'") # item['values'][2] = Fragentyp und der entspricht dem Table in der Datenbank für diesen Fragentyp
            self.dblist[ID].commit()
        self.get_complete_DB(ID)
        self.notify()


    def Add_data_to_DB(self, q, title): #todo mus noch an multi Fragentyp angepasst werden
        if self.does_title_exist(title):
            print("title existiert bereits daher konnte die Frage nicht erstellt werden")
        else:
            print("title existiert noch nicht")
            table_name = q[2][0].get() #table name ist gleich dem FragentypA
            index = self.table_dict[table_name]
            self.cursor.execute("INSERT INTO " + table_name + " (" + self.index_list[3][1] + ") VALUES (:Titel)",
                                {'Titel': q[3][0].get()})
            # print("INSERT INTO " + self.table + " (" + self.index_list[3][1] + ") VALUES (:Titel)", {'Titel': q[3][0].get()})
            self.mydb.commit()
            for i in q:
                self.cursor.execute(
                    "UPDATE " + table_name + " SET '" + i[1] + "' = :Value WHERE " + self.index_list[3][1] + " = '" +
                    q[3][0].get() + "' ", {'Value': i[0].get()})
            self.mydb.commit()
            self.get_question(q[3][0].get(), 1)
            self.get_complete_DB(0)

    def add_Changes_to_DB(self, q): #todo mus noch an multi Fragentyp angepasst werden
        for i in q:
            # print("UPDATE " + self.table + " SET '" + i[1] + "' = :Value WHERE " + self.index_list[2][1] + " LIKE '%" + self.db_data[1][0][2] + "%'", {'Value': i[0].get()})
            self.cursor.execute(
                "UPDATE " + self.table + " SET '" + i[1] + "' = :Value WHERE " + self.index_list[3][
                    1] + " LIKE '%" + self.db_data[1][0][3] + "%'",
                {'Value': i[0].get()})
            self.mydb.commit()
        self.get_question(q[3][0].get(), 1)
        self.get_complete_DB(0)

    def Save_Change_to_DB(self, q): #todo mus noch an multi Fragentyp angepasst werden
        #print("titel?", self.db_data[1][0][3])
        title = q[3][0].get()
        if self.og_title == title:
               self.add_Changes_to_DB(q)
        elif self.does_title_exist(title):
            print("title existiert bereits, speichern nicht möglich")
        else:
            print("datenänderung konnte gespeichert werden")
            self.add_Changes_to_DB(q)

    def subscribe(self, listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        self.listeners.remove(listener)

    def get_complete_DB(self, id):
        all_data = []
        for table in self.table_list:
            self.query = "SELECT " + self.table_index_list[0][0][1] + ", " + self.table_index_list[0][1][1] + ", " + self.table_index_list[0][2][1] + ", " + self.table_index_list[0][3][1] + ", " + self.table_index_list[0][4][1] + ", " + self.table_index_list[0][189][1] + " FROM " + table + ""
            self.cursorlist[id].execute(self.query)
            all_data.append(self.cursorlist[id].fetchall())
        self.db_data[id] = all_data
        self.notify()

    def notify(self):
        for listener in self.listeners:
            listener(self.db_data)