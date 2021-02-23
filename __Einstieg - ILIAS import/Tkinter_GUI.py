from tkinter import *
import sqlite3
import os

# Fenster erstellen, Größe und Namen setzen
GUI = Tk()
GUI.geometry = '800x710'
GUI.title('Test - GUI')

# Label definieren. Mit grid() wird das Label auf der GUI platziert.
# row = Zeile in der GUI
# column = Spalte in der GUI
# padx,pady = Label in Richtung X- oder Y-Richtung schieben
# sticky NW (NorthWest) = Schiebt das Label in NW Richtung
# width = Gibt die Breite des Eingabefeldes an
frame_ilias_test_title = LabelFrame(GUI, text="Testname & Autor", padx=5, pady=5)
frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

frame_question_attributes = LabelFrame(GUI, text="Fragen Attribute", padx=5, pady=5)
frame_question_attributes.grid(row=2, column=0, padx=200, pady=10, sticky="NW")

frame_database = LabelFrame(GUI, text="Datenbank", padx=5, pady=5)
frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")



###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
ilias_test_title_label = Label(frame_ilias_test_title, text="Name des Tests")
ilias_test_title_label.grid(row=0, column=0, sticky=W)

ilias_test_title_entry = Entry(frame_ilias_test_title, width=70)
ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

ilias_test_autor_label = Label(frame_ilias_test_title, text="Autor")
ilias_test_autor_label.grid(row=1, column=0, sticky=W)

ilias_test_autor_entry = Entry(frame_ilias_test_title, width=70)
ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)


###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
question_difficulty_label = Label(frame_question_attributes, text="Schwierigkeit")
question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

question_difficulty_entry = Entry(frame_question_attributes, width=15)
question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

question_category_label = Label(frame_question_attributes, text="Fragenkategorie")
question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

question_category_entry = Entry(frame_question_attributes, width=15)
question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

question_type_label = Label(frame_question_attributes, text="Fragen-Typ")
question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

question_type_entry = Entry(frame_question_attributes, width=15)
question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
question_type_entry.insert(0, "Formelfrage")

question_pool_tag_label = Label(frame_question_attributes, text="Pool-Tag")
question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

question_pool_tag_entry = Entry(frame_question_attributes, width=15)
question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)

###################### "Formelfrage-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

database_show_db_formelfrage_btn = Button(frame_database, text="In Datenbank speichern", command=lambda: save_to_db)
database_show_db_formelfrage_btn.grid(row=0, column=0, sticky=W, pady=5)



# Werte in die DB schreiben
def save_to_db():

    # Verbindung mit der Datenbank aufnehmen sqlite3.connect("Pfad")
    connect = sqlite3.connect(os.path.normpath(os.path.join("Datenbank", "Formelfrage_DB")))

    # cursor für die DB erstellen (ist immer notwendig)
    cursor = connect.cursor()

    # "Einträge aus den Eingabefeldern auslesen ( .get() )
    cursor.execute(
            # Eine Datenbank enthält immer eine Tabelle (hier: datenbank_table)
            # Die Daten werden in die Tabelle eingefügt
            "INSERT INTO datenbank_table VALUES ("
            
            # Im nächsten Schritt muss aufgelistet werden, welche Einträge die Tabelle haben soll (Spalten-Namen)
            ":question_difficulty, :question_category, :question_type, :question_pool_tag",

            # Dann wird definiert welche Werte in die jeweilige Spalte eingefügt werden
            {
                'question_difficulty': question_difficulty_entry.get(),
                'question_category': question_category_entry.get(),
                'question_type': question_type_entry.get(),
                'question_pool_tag': question_pool_tag_entry.get(),
            })

    # Datenbank Eintrag in DB übernehmen
    connect.commit()

    # Verbindung zur Datenbank schliessen
    connect.close()


GUI.mainloop()
