from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
from sympy import *
import os
import datetime                             # wird benötigt für "Test-Einstellungen benutzen"
from datetime import datetime               # wird benötigt für "delete all entrys?" ??
import pathlib
import shutil                               # zum kopieren und zippen von Dateien
from PIL import ImageTk, Image          # Zur Preview von ausgewählten Bildern
import pandas as pd
from pandas.core.reshape.util import cartesian_product
import numpy as np
import re   # RegEx -> handle Regular Expressions
import decimal

### Eigene Dateien / Module
from Test_Generator_Module import test_generator_modul_datenbanken_anzeigen
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_test_struktur

class Formelfrage_Permutation:
    def __init__(self, app, formelfrage_permutation_tab, project_root_path):

############## SET IMAGE VARIABLES

        # Die Variablen müssen am Anfang des Programms gesetzt werden, um diese an andere Funktionen weitergeben zu können

        self.formelfrage_permutation_tab = formelfrage_permutation_tab

        self.ffperm_description_img_name_1 = ""
        self.ffperm_description_img_name_2 = ""
        self.ffperm_description_img_name_3 = ""

        self.ffperm_description_img_data_1 = ""
        self.ffperm_description_img_data_2 = ""
        self.ffperm_description_img_data_3 = ""

        self.ffperm_description_img_path_1 = ""
        self.ffperm_description_img_path_2 = ""
        self.ffperm_description_img_path_3 = ""



############## DEFINE FORMELFRAGE PATHS

        # Pfad des Projekts und des FF-Moduls
        self.project_root_path = project_root_path
        self.formelfrage_permutation_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Formelfrage_Permutation"))
        self.formelfrage_permutation_files_path_pool_output = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_formelfrage_permutation_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_permutation_db.db"))

        # Pfad für ILIAS-Test Vorlage
        self.formelfrage_permutation_test_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.formelfrage_permutation_test_tst_file_path_template = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))


        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.formelfrage_permutation_test_qti_file_path_output = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.formelfrage_permutation_test_tst_file_path_output = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.formelfrage_permutation_test_img_file_path = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))


        # Pfad für ILIAS-Pool Vorlage
        self.formelfrage_permutation_pool_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.formelfrage_permutation_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))


        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # Die Pfade für die qti.xml und qpl.xml werden erst zur Laufzeit bestimmt.
        # Die Deklaration ist daher unter "class Create_formelfrage_permutation_Pool"
        self.formelfrage_permutation_pool_directory_output = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path, "ffperm_ilias_pool_abgabe"))


###################### DATENBANK ENTRIES UND INDEX DICT ERSTELLEN  ###################


        # Dictionary aus zwei Listen erstellen
        # Auslesen der Formelfrage-Datenbank einträgen
        # Nur die erste Zeile auslesen um einen Zusammenhang zwischen Variablen und Indexen herzustellen
        self.ffperm_db_find_entries = []
        self.ffperm_db_find_indexes = []

        connect = sqlite3.connect(self.database_formelfrage_permutation_path)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM formelfrage_permutation_table LIMIT 1")

        ffperm_db_records = cursor.fetchall()
        for ffperm_db_record in ffperm_db_records:
            for k in range(len(ffperm_db_record)):
                self.ffperm_db_find_entries.append(str(ffperm_db_record[k]))
                self.ffperm_db_find_indexes.append(int(k))


        self.ffperm_db_entry_to_index_dict = dict(zip((self.ffperm_db_find_entries), (self.ffperm_db_find_indexes)))



        connect.commit()
        connect.close()



############## FRAMES
        self.ffperm_frame_ilias_test_title = LabelFrame(self.formelfrage_permutation_tab, text="Testname & Autor", padx=5, pady=5)
        self.ffperm_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.ffperm_frame = LabelFrame(self.formelfrage_permutation_tab, text="Formelfrage", padx=5, pady=5)
        self.ffperm_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.ffperm_frame_question_attributes = LabelFrame(self.formelfrage_permutation_tab, text="Fragen Attribute", padx=5, pady=5)
        self.ffperm_frame_question_attributes.grid(row=2, column=0, padx=10, pady=10, sticky="NE")

        self.ffperm_frame_database = LabelFrame(self.formelfrage_permutation_tab, text="Formelfrage-Datenbank", padx=5, pady=5)
        self.ffperm_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.ffperm_frame_create_formelfrage_permutation_test = LabelFrame(self.formelfrage_permutation_tab, text="FF-Test erstellen", padx=5, pady=5)
        self.ffperm_frame_create_formelfrage_permutation_test.grid(row=2, column=0, padx=105, pady=120, sticky="NE")


        self.ffperm_frame_taxonomy_settings = LabelFrame(self.formelfrage_permutation_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.ffperm_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.ffperm_frame_question_description_functions = LabelFrame(self.formelfrage_permutation_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.ffperm_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.ffperm_frame_excel_import_export = LabelFrame(self.formelfrage_permutation_tab, text="Excel Import/Export", padx=5, pady=5)
        self.ffperm_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")

        self.ffperm_frame_question_permutation = LabelFrame(self.formelfrage_permutation_tab, text="Fragen - Permutation", padx=5, pady=5)
        self.ffperm_frame_question_permutation.grid(row=2, column=1,padx=10, pady=120,   sticky="NW")


        self.ffperm_frame_description_picture = LabelFrame(self.formelfrage_permutation_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.ffperm_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")


###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        self.ffperm_ilias_test_title_label = Label(self.ffperm_frame_ilias_test_title, text="Name des Tests")
        self.ffperm_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.ffperm_ilias_test_title_entry = Entry(self.ffperm_frame_ilias_test_title, width=60)
        self.ffperm_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.ffperm_ilias_test_autor_label = Label(self.ffperm_frame_ilias_test_title, text="Autor")
        self.ffperm_ilias_test_autor_label.grid(row=1, column=0, sticky=W)

        self.ffperm_ilias_test_autor_entry = Entry(self.ffperm_frame_ilias_test_title, width=60)
        self.ffperm_ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)

###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.ffperm_var_use_image_1 = IntVar()
        self.ffperm_check_use_image_1_in_description = Checkbutton(self.ffperm_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.ffperm_var_use_image_1, onvalue=1, offvalue=0)
        self.ffperm_check_use_image_1_in_description.deselect()
        self.ffperm_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.ffperm_var_use_image_2 = IntVar()
        self.ffperm_check_use_image_2_in_description = Checkbutton(self.ffperm_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.ffperm_var_use_image_2, onvalue=1, offvalue=0)
        self.ffperm_check_use_image_2_in_description.deselect()
        self.ffperm_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.ffperm_var_use_image_3 = IntVar()
        self.ffperm_check_use_image_3_in_description = Checkbutton(self.ffperm_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.ffperm_var_use_image_3, onvalue=1, offvalue=0)
        self.ffperm_check_use_image_3_in_description.deselect()
        self.ffperm_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        #self.ffperm_add_img_to_description_btn = Button(self.ffperm_frame_question_description_functions, text="Bild hinzufügen", command=lambda: Formelfrage_Permutation.ffperm_add_image_to_description(self, self.ffperm_var_use_image_1.get(), self.ffperm_var_use_image_2.get(), self.ffperm_var_use_image_3.get()))
       # self.ffperm_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))

        self.ffperm_add_img_to_description_btn = Button(self.ffperm_frame_question_description_functions, text="Bild hinzufügen", command=lambda: ffperm_add_image_to_description_and_create_labels())
        self.ffperm_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))

        # Bild zum Fragentext hinzufügen
        def ffperm_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.ffperm_question_description_img_1_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_1)
            self.ffperm_question_description_img_2_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_2)
            self.ffperm_question_description_img_3_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_3)


            self.ffperm_description_img_name_1, self.ffperm_description_img_name_2, self.ffperm_description_img_name_3, self.ffperm_description_img_path_1, self.ffperm_description_img_path_2, self.ffperm_description_img_path_3, self.ffperm_question_description_img_1_filename_label, self.ffperm_question_description_img_2_filename_label, self.ffperm_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.ffperm_var_use_image_1.get(),
                    self.ffperm_var_use_image_2.get(),
                    self.ffperm_var_use_image_3.get(),
                    self.ffperm_frame_description_picture,
                    self.ffperm_description_img_name_1,
                    self.ffperm_description_img_name_2,
                    self.ffperm_description_img_name_3,
                    self.ffperm_description_img_path_1,
                    self.ffperm_description_img_path_2,
                    self.ffperm_description_img_path_3,
                    )


        #self.ffperm_remove_img_from_description_btn = Button(self.ffperm_frame_question_description_functions, text="Bild entfernen", command=lambda: Formelfrage_Permutation.ffperm_delete_image_from_description(self, self.ffperm_var_use_image_1.get(), self.ffperm_var_use_image_2.get(), self.ffperm_var_use_image_3.get()))
        #self.ffperm_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        self.ffperm_remove_img_from_description_btn = Button(self.ffperm_frame_question_description_functions, text="Bild entfernen", command=lambda: ffperm_add_image_to_description_and_delete_labels())
        self.ffperm_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        # Bild aus Fragentext entfernen
        def ffperm_add_image_to_description_and_delete_labels():
            self.ffperm_description_img_name_1, self.ffperm_description_img_name_2, self.ffperm_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self, self.ffperm_var_use_image_1.get(),
                 self.ffperm_var_use_image_2.get(),
                 self.ffperm_var_use_image_3.get(),
                 self.ffperm_question_description_img_1_filename_label,
                 self.ffperm_question_description_img_2_filename_label,
                 self.ffperm_question_description_img_3_filename_label,
                 self.ffperm_description_img_name_1,
                 self.ffperm_description_img_name_2,
                 self.ffperm_description_img_name_3,
            )



        ###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.ffperm_taxonomy_settings_btn = Button(self.ffperm_frame_taxonomy_settings, text="Taxonomie-Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.ffperm_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")


###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ffperm_question_difficulty_label = Label(self.ffperm_frame_question_attributes, text="Schwierigkeit")
        self.ffperm_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.ffperm_question_difficulty_entry = Entry(self.ffperm_frame_question_attributes, width=15)
        self.ffperm_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.ffperm_question_category_label = Label(self.ffperm_frame_question_attributes, text="Fragenkategorie")
        self.ffperm_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.ffperm_question_category_entry = Entry(self.ffperm_frame_question_attributes, width=15)
        self.ffperm_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.ffperm_question_type_label = Label(self.ffperm_frame_question_attributes, text="Fragen-Typ")
        self.ffperm_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.ffperm_question_type_entry = Entry(self.ffperm_frame_question_attributes, width=15)
        self.ffperm_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.ffperm_question_type_entry.insert(0, "Formelfrage_perm")

        self.ffperm_question_pool_tag_label = Label(self.ffperm_frame_question_attributes, text="Pool-Tag")
        self.ffperm_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.ffperm_question_pool_tag_entry = Entry(self.ffperm_frame_question_attributes, width=15)
        self.ffperm_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)




###################### "FF-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # Button "Formelfrage-Test erstellen"
        self.create_formelfrage_permutation_test_btn = Button(self.ffperm_frame_create_formelfrage_permutation_test, text="FFperm-Test erstellen", command=lambda: Create_formelfrage_permutation_Test.__init__(self, self.ffperm_db_entry_to_index_dict))
        self.create_formelfrage_permutation_test_btn.grid(row=0, column=0, sticky=W)
        self.create_formelfrage_permutation_test_entry = Entry(self.ffperm_frame_create_formelfrage_permutation_test, width=15)
        self.create_formelfrage_permutation_test_entry.grid(row=0, column=1, sticky=W, padx=0)

        # Checkbox "Test-Einstellungen übernehmen?"
        self.create_test_settings_label = Label(self.ffperm_frame_create_formelfrage_permutation_test, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.perm_var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.ffperm_frame_create_formelfrage_permutation_test, text="", variable=self.perm_var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)

        # Checkbox "Latex für Fragentext nutzen?"
        self.ffperm_use_latex_on_text_label = Label(self.ffperm_frame_create_formelfrage_permutation_test, text="Latex für Fragentext nutzen?")
        self.ffperm_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.ffperm_var_use_latex_on_text_check = IntVar()
        self.ffperm_use_latex_on_text_check = Checkbutton(self.ffperm_frame_create_formelfrage_permutation_test, text="", variable=self.ffperm_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.ffperm_use_latex_on_text_check.deselect()
        self.ffperm_use_latex_on_text_check.grid(row=2, column=1, sticky=W)




        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.ffperm_create_question_pool_all_label = Label(self.ffperm_frame_create_formelfrage_permutation_test, text="Alle Einträge aus der DB erzeugen?")
        self.ffperm_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.ffperm_var_create_question_pool_all_check = IntVar()
        self.ffperm_create_question_pool_all = Checkbutton(self.ffperm_frame_create_formelfrage_permutation_test, text="", variable=self.ffperm_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.ffperm_var_create_question_pool_all_check.set(0)
        self.ffperm_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))



        # Button "Formelfrage-Fragenpool erstellen"
        self.create_formelfrage_permutation_pool_btn = Button(self.ffperm_frame_create_formelfrage_permutation_test, text="FFperm-Pool erstellen", command=lambda: Create_formelfrage_permutation_Pool.__init__(self, self.ffperm_db_entry_to_index_dict, self.ffperm_var_create_question_pool_all_check.get()))
        self.create_formelfrage_permutation_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_formelfrage_permutation_pool_entry = Entry(self.ffperm_frame_create_formelfrage_permutation_test, width=15)
        self.create_formelfrage_permutation_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))



###################### "Formelfrage-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################



        self.ffperm_database_show_db_formelfrage_permutation_btn = Button(self.ffperm_frame_database, text="FFperm - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_formelfrage_permutation_path, "formelfrage_permutation_table"))
        self.ffperm_database_show_db_formelfrage_permutation_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.ffperm_database_save_id_to_db_formelfrage_permutation_btn = Button(self.ffperm_frame_database, text="Speichern unter neuer ID", command=lambda: Formelfrage_Permutation.ffperm_save_id_to_db(self))
        self.ffperm_database_save_id_to_db_formelfrage_permutation_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.ffperm_database_delete_id_from_db_btn = Button(self.ffperm_frame_database, text="ID Löschen", command=lambda: Formelfrage_Permutation.ffperm_delete_id_from_db(self))
        self.ffperm_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.ffperm_delete_box = Entry(self.ffperm_frame_database, width=10)
        self.ffperm_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        self.ffperm_database_new_question_btn = Button(self.ffperm_frame_database, text="GUI Einträge leeren", command=lambda: Formelfrage_Permutation.ffperm_clear_GUI(self))
        self.ffperm_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        self.ffperm_database_edit_btn = Button(self.ffperm_frame_database, text="Aktuellen Eintrag editieren", command=lambda: Formelfrage_Permutation.ffperm_edit_id_from_db(self))
        self.ffperm_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.ffperm_database_load_id_btn = Button(self.ffperm_frame_database, text="ID Laden", command=lambda: Formelfrage_Permutation.ffperm_load_id_from_db(self, self.ffperm_db_entry_to_index_dict))
        self.ffperm_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.ffperm_load_box = Entry(self.ffperm_frame_database, width=10)
        self.ffperm_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))


        # Checkbox - "Fragentext mit Highlighting?"
        self.ffperm_highlight_question_text_label = Label(self.ffperm_frame_database, text="Fragentext mit Highlighting?")
        self.ffperm_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.ffperm_var_highlight_question_text = IntVar()
        self.ffperm_check_highlight_question_text = Checkbutton(self.ffperm_frame_database, text="", variable=self.ffperm_var_highlight_question_text, onvalue=1, offvalue=0)
        self.ffperm_check_highlight_question_text.deselect()
        self.ffperm_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.ffperm_delete_all_label = Label(self.ffperm_frame_database, text="Alle DB Einträge löschen?")
        self.ffperm_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.ffperm_var_delete_all = IntVar()
        self.ffperm_check_delete_all = Checkbutton(self.ffperm_frame_database, text="", variable=self.ffperm_var_delete_all, onvalue=1, offvalue=0)
        self.ffperm_check_delete_all.deselect()
        self.ffperm_check_delete_all.grid(row=7, column=0, sticky=E)


###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.table_name = "formelfrage_permutation_DB_export.xlsx"


        #excel_import_btn
        self.ffperm_excel_import_to_db_formelfrage_permutation_btn = Button(self.ffperm_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, "formelfrage", self.ffperm_db_entry_to_index_dict))
        self.ffperm_excel_import_to_db_formelfrage_permutation_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.ffperm_excel_export_to_xlsx_formelfrage_permutation_btn = Button(self.ffperm_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.ffperm_db_entry_to_index_dict, self.database_formelfrage_permutation_path, "formelfrage_permutation_table", "formelfrage_permutation_DB_export_file.xlsx", "Formelfrage - Database"))
        self.ffperm_excel_export_to_xlsx_formelfrage_permutation_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)


#################### "Fragen Permutation - FRAME
        self.ffperm_start_question_permutation_btn = Button(self.ffperm_frame_question_permutation, text="Permutation starten", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, "formelfrage", self.ffperm_db_entry_to_index_dict))
        #self.ffperm_start_question_permutation_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        self.ffperm_var_start_question_permutation = IntVar()
        self.ffperm_start_question_permutation = Checkbutton(self.ffperm_frame_question_permutation, text="Permutation verwenden?", variable=self.ffperm_var_start_question_permutation, onvalue=1, offvalue=0)
        self.ffperm_start_question_permutation.deselect()
        self.ffperm_start_question_permutation.grid(row=1, column=1, sticky=W)



###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.ffperm_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.ffperm_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.ffperm_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.ffperm_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.ffperm_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.ffperm_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.ffperm_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.ffperm_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.ffperm_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.ffperm_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.ffperm_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.ffperm_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.ffperm_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.ffperm_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")

###################### "Formelfrage" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ffperm_question_author_label = Label(self.ffperm_frame, text="Fragen-Autor")
        self.ffperm_question_author_label.grid(row=0, column=0, sticky=W, pady=(10, 0), padx=10)
        self.ffperm_question_author_entry = Entry(self.ffperm_frame, width=20)
        self.ffperm_question_author_entry.grid(row=0, column=1, sticky=W, pady=(10, 0))

        self.ffperm_question_title_label = Label(self.ffperm_frame, text="Fragen-Titel")
        self.ffperm_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.ffperm_question_title_entry = Entry(self.ffperm_frame, width=60)
        self.ffperm_question_title_entry.grid(row=1, column=1,  sticky=W, pady=(10, 0))

        self.ffperm_question_description_title_label = Label(self.ffperm_frame, text="Fragen-Beschreibung")
        self.ffperm_question_description_title_label.grid(row=2, column=0, sticky=W, padx=10)
        self.ffperm_question_description_title_entry = Entry(self.ffperm_frame, width=60)
        self.ffperm_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.ffperm_question_textfield_label = Label(self.ffperm_frame, text="Fragen-Text")
        self.ffperm_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.ffperm_bar = Scrollbar(self.ffperm_frame)
        self.ffperm_question_description_main_entry = Text(self.ffperm_frame, height=6, width=65, font=('Helvetica', 9))
        self.ffperm_bar.grid(row=3, column=2, sticky=W)
        self.ffperm_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.ffperm_bar.config(command=self.ffperm_question_description_main_entry.yview)
        self.ffperm_question_description_main_entry.config(yscrollcommand=self.ffperm_bar.set)





        ################### BEARBEITUNGSDAUER


        self.ffperm_processing_time_label = Label(self.ffperm_frame, text="Bearbeitungsdauer")
        self.ffperm_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.ffperm_processing_time_label = Label(self.ffperm_frame, text="Std:")
        self.ffperm_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.ffperm_processing_time_label = Label(self.ffperm_frame, text="Min:")
        self.ffperm_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.ffperm_processing_time_label = Label(self.ffperm_frame, text="Sek:")
        self.ffperm_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        self.ffperm_processingtime_hours = list(range(24))
        self.ffperm_processingtime_minutes = list(range(60))
        self.ffperm_processingtime_seconds = list(range(60))

        self.ffperm_proc_hours_box = ttk.Combobox(self.ffperm_frame, value=self.ffperm_processingtime_hours, width=2)
        self.ffperm_proc_minutes_box = ttk.Combobox(self.ffperm_frame, value=self.ffperm_processingtime_minutes, width=2)
        self.ffperm_proc_seconds_box = ttk.Combobox(self.ffperm_frame, value=self.ffperm_processingtime_seconds, width=2)

        self.ffperm_proc_hours_box.current(23)
        self.ffperm_proc_minutes_box.current(0)
        self.ffperm_proc_seconds_box.current(0)

        def selected_hours(event):
            self.selected_hours = self.ffperm_proc_hours_box.get()
            print(self.selected_hours)

        def selected_minutes(event):
            self.selected_minutes = self.ffperm_proc_minutes_box.get()
            print(self.selected_minutes)

        def selected_seconds(event):
            self.selected_seconds = self.ffperm_proc_seconds_box.get()
            print(self.selected_seconds)

        self.ffperm_proc_hours_box.bind("<<ComboboxSelected>>", selected_hours)
        self.ffperm_proc_minutes_box.bind("<<ComboboxSelected>>", selected_minutes)
        self.ffperm_proc_seconds_box.bind("<<ComboboxSelected>>", selected_seconds)

        self.ffperm_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.ffperm_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.ffperm_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))





        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        ########### PERMUTATION_VALUES

        self.perm_symbol_of_variable_label = Label(self.ffperm_frame, text='perm\nsymbol ')
        self.perm_symbol_of_variable_label.grid(row=5, column=1, sticky=E, pady=(20, 0), padx=116)

        self.perm_var_values_label = Label(self.ffperm_frame, text='perm\nwerte')
        self.perm_var_values_label.grid(row=5, column=1, sticky=E, pady=(20, 0), padx=50)


        
        
        
        

        self.perm_var_symbol_entry_1 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_2 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_3 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_4 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_5 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_6 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_7 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_8 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_9 = Entry(self.ffperm_frame,  width=6)
        self.perm_var_symbol_entry_10 = Entry(self.ffperm_frame,  width=6)
        

        self.perm_var_value_entry_1 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_2 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_3 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_4 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_5 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_6 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_7 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_8 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_9 = Entry(self.ffperm_frame, width=19)
        self.perm_var_value_entry_10 = Entry(self.ffperm_frame, width=19)
        
        
        
        self.perm_var_symbol_entry_1.grid(row=6, column=1,  sticky=E, padx=123)
        self.perm_var_value_entry_1.grid(row=6, column=1,  sticky=E, padx=0)
        ###########################


        self.perm_var_min_label = Label(self.ffperm_frame, text=' Min.')
        self.perm_var_min_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=60)

        self.perm_var_max_label = Label(self.ffperm_frame, text=' Max.')
        self.perm_var_max_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=100)

        self.perm_var_prec_label = Label(self.ffperm_frame, text=' Präz.')
        self.perm_var_prec_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=140)

        self.perm_var_divby_label = Label(self.ffperm_frame, text=' Teilbar\ndurch')
        self.perm_var_divby_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=180)

        self.perm_variable1_label = Label(self.ffperm_frame, text='Variable 1')
        self.perm_variable2_label = Label(self.ffperm_frame, text='Variable 2')
        self.perm_variable3_label = Label(self.ffperm_frame, text='Variable 3')
        self.perm_variable4_label = Label(self.ffperm_frame, text='Variable 4')
        self.perm_variable5_label = Label(self.ffperm_frame, text='Variable 5')
        self.perm_variable6_label = Label(self.ffperm_frame, text='Variable 6')
        self.perm_variable7_label = Label(self.ffperm_frame, text='Variable 7')
        self.perm_variable8_label = Label(self.ffperm_frame, text='Variable 8')
        self.perm_variable9_label = Label(self.ffperm_frame, text='Variable 9')
        self.perm_variable10_label = Label(self.ffperm_frame, text='Variable 10')

        # Label für Var1 ist immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.perm_variable1_label.grid(row=6, column=0, sticky=W, padx=20)



        ########################### VARIABLEN TEXTE DEKLARIEREN ##############################

        self.perm_var1_name_text, self.perm_var1_min_text, self.perm_var1_max_text, self.perm_var1_prec_text, self.perm_var1_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var2_name_text, self.perm_var2_min_text, self.perm_var2_max_text, self.perm_var2_prec_text, self.perm_var2_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var3_name_text, self.perm_var3_min_text, self.perm_var3_max_text, self.perm_var3_prec_text, self.perm_var3_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var4_name_text, self.perm_var4_min_text, self.perm_var4_max_text, self.perm_var4_prec_text, self.perm_var4_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var5_name_text, self.perm_var5_min_text, self.perm_var5_max_text, self.perm_var5_prec_text, self.perm_var5_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var6_name_text, self.perm_var6_min_text, self.perm_var6_max_text, self.perm_var6_prec_text, self.perm_var6_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var7_name_text, self.perm_var7_min_text, self.perm_var7_max_text, self.perm_var7_prec_text, self.perm_var7_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var8_name_text, self.perm_var8_min_text, self.perm_var8_max_text, self.perm_var8_prec_text, self.perm_var8_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var9_name_text, self.perm_var9_min_text, self.perm_var9_max_text, self.perm_var9_prec_text, self.perm_var9_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_var10_name_text, self.perm_var10_min_text, self.perm_var10_max_text, self.perm_var10_prec_text, self.perm_var10_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()



        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.perm_var1_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var1_name_text, width=6)
        self.perm_var1_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var1_min_text, width=6)
        self.perm_var1_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var1_max_text, width=6)
        self.perm_var1_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var1_prec_text, width=6)
        self.perm_var1_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var1_divby_text, width=6)

        self.perm_var2_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var2_name_text, width=6)
        self.perm_var2_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var2_min_text, width=6)
        self.perm_var2_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var2_max_text, width=6)
        self.perm_var2_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var2_prec_text, width=6)
        self.perm_var2_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var2_divby_text, width=6)

        self.perm_var3_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var3_name_text, width=6)
        self.perm_var3_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var3_min_text, width=6)
        self.perm_var3_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var3_max_text, width=6)
        self.perm_var3_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var3_prec_text, width=6)
        self.perm_var3_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var3_divby_text, width=6)

        self.perm_var4_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var4_name_text, width=6)
        self.perm_var4_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var4_min_text, width=6)
        self.perm_var4_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var4_max_text, width=6)
        self.perm_var4_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var4_prec_text, width=6)
        self.perm_var4_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var4_divby_text, width=6)

        self.perm_var5_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var5_name_text, width=6)
        self.perm_var5_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var5_min_text, width=6)
        self.perm_var5_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var5_max_text, width=6)
        self.perm_var5_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var5_prec_text, width=6)
        self.perm_var5_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var5_divby_text, width=6)

        self.perm_var6_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var6_name_text, width=6)
        self.perm_var6_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var6_min_text, width=6)
        self.perm_var6_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var6_max_text, width=6)
        self.perm_var6_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var6_prec_text, width=6)
        self.perm_var6_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var6_divby_text, width=6)

        self.perm_var7_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var7_name_text, width=6)
        self.perm_var7_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var7_min_text, width=6)
        self.perm_var7_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var7_max_text, width=6)
        self.perm_var7_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var7_prec_text, width=6)
        self.perm_var7_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var7_divby_text, width=6)

        self.perm_var8_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var8_name_text, width=6)
        self.perm_var8_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var8_min_text, width=6)
        self.perm_var8_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var8_max_text, width=6)
        self.perm_var8_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var8_prec_text, width=6)
        self.perm_var8_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var8_divby_text, width=6)

        self.perm_var9_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var9_name_text, width=6)
        self.perm_var9_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var9_min_text, width=6)
        self.perm_var9_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var9_max_text, width=6)
        self.perm_var9_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var9_prec_text, width=6)
        self.perm_var9_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var9_divby_text, width=6)

        self.perm_var10_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_var10_name_text, width=6)
        self.perm_var10_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_var10_min_text, width=6)
        self.perm_var10_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_var10_max_text, width=6)
        self.perm_var10_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_var10_prec_text, width=6)
        self.perm_var10_divby_entry = Entry(self.ffperm_frame, textvariable=self.perm_var10_divby_text, width=6)

        # Eingabefelder für Var1 sind immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.perm_var1_name_entry.grid(row=6, column=1, sticky=W)
        self.perm_var1_min_entry.grid(row=6, column=1, sticky=W, padx=60)
        self.perm_var1_max_entry.grid(row=6, column=1, sticky=W, padx=100)
        self.perm_var1_prec_entry.grid(row=6, column=1, sticky=W, padx=140)
        self.perm_var1_divby_entry.grid(row=6, column=1, sticky=W, padx=180)

        # Wertebereich berechnen für Formel aus Eingabefeld: formula 1
        self.calculate_value_range_btn = Button(self.ffperm_frame, text="Wertebereich berechnen",command=lambda: Formelfrage_Permutation.ffperm_calculate_value_range_from_formula(self, self.perm_res1_formula_entry.get()))
        #self.calculate_value_range_btn.grid(row=6, column=1, padx=50, sticky="E")




        ###########################  EINGABEFELDER-MATRIX (VARIABLEN)  EIN/AUSBLENDEN ##############################

        # Hier werden durch die Funktion "ffperm_answer_selected" die Variable - Eingabefelder (je nach Wert) ein-/ausgeblendet

        def ffperm_answer_selected(event):  # "variable" need for comboBox Binding


            if self.ffperm_numbers_of_answers_box.get() == '1':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "remove",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "remove",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "remove",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "remove",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "remove",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '2':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "remove",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "remove",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "remove",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "remove",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '3':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "remove",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "remove",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "remove",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '4':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "remove",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "remove",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '5':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "remove",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '6':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "show",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "remove",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '7':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "show",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "show",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "remove",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '8':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "show",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "show",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "show",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "remove",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '9':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "show",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "show",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "show",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "show",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "remove",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)

            elif self.ffperm_numbers_of_answers_box.get() == '10':
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable2_label, self.perm_var2_name_entry, self.perm_var2_min_entry, self.perm_var2_max_entry, self.perm_var2_prec_entry, self.perm_var2_divby_entry, "7", "show",  self.perm_var_symbol_entry_2, self.perm_var_value_entry_2)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable3_label, self.perm_var3_name_entry, self.perm_var3_min_entry, self.perm_var3_max_entry, self.perm_var3_prec_entry, self.perm_var3_divby_entry, "8", "show",  self.perm_var_symbol_entry_3, self.perm_var_value_entry_3)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable4_label, self.perm_var4_name_entry, self.perm_var4_min_entry, self.perm_var4_max_entry, self.perm_var4_prec_entry, self.perm_var4_divby_entry, "9", "show",  self.perm_var_symbol_entry_4, self.perm_var_value_entry_4)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable5_label, self.perm_var5_name_entry, self.perm_var5_min_entry, self.perm_var5_max_entry, self.perm_var5_prec_entry, self.perm_var5_divby_entry, "10", "show",  self.perm_var_symbol_entry_5, self.perm_var_value_entry_5)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable6_label, self.perm_var6_name_entry, self.perm_var6_min_entry, self.perm_var6_max_entry, self.perm_var6_prec_entry, self.perm_var6_divby_entry, "11", "show",  self.perm_var_symbol_entry_6, self.perm_var_value_entry_6)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable7_label, self.perm_var7_name_entry, self.perm_var7_min_entry, self.perm_var7_max_entry, self.perm_var7_prec_entry, self.perm_var7_divby_entry, "12", "show",  self.perm_var_symbol_entry_7, self.perm_var_value_entry_7)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable8_label, self.perm_var8_name_entry, self.perm_var8_min_entry, self.perm_var8_max_entry, self.perm_var8_prec_entry, self.perm_var8_divby_entry, "13", "show",  self.perm_var_symbol_entry_8, self.perm_var_value_entry_8)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable9_label, self.perm_var9_name_entry, self.perm_var9_min_entry, self.perm_var9_max_entry, self.perm_var9_prec_entry, self.perm_var9_divby_entry, "14", "show",  self.perm_var_symbol_entry_9, self.perm_var_value_entry_9)
                Formelfrage_Permutation.ffperm_variable_show_or_remove(self, self.perm_variable10_label, self.perm_var10_name_entry, self.perm_var10_min_entry, self.perm_var10_max_entry, self.perm_var10_prec_entry, self.perm_var10_divby_entry, "15", "show",  self.perm_var_symbol_entry_10, self.perm_var_value_entry_10)



        self.ffperm_numbers_of_answers_box_label = Label(self.ffperm_frame, text="Anzahl der Variablen: ")
        self.ffperm_numbers_of_answers_box_label.grid(row=5, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ffperm_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.ffperm_numbers_of_answers_box = ttk.Combobox(self.ffperm_frame, value=self.ffperm_numbers_of_answers_value, width=3)
        self.ffperm_numbers_of_answers_box.bind("<<ComboboxSelected>>", ffperm_answer_selected)
        self.ffperm_numbers_of_answers_box.grid(row=5, column=1, sticky=W, pady=(20, 0))
        self.ffperm_numbers_of_answers_box.current(0)


        ###########################  AUSWAHL DER EINHEITEN FÜR VARIABLEN ---- DERZEIT NICHT AKTIV ##############################

        self.select_var_units = ["Unit", "H", "mH", "µH", "nH", "pH", "---", "F", "mF", "µF", "nF", "pF", "---", "MV", "kV", "V", "mV", "µV", "---"]

        self.perm_var1_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var1_unit_myCombo.current(0)

        self.perm_var2_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var2_unit_myCombo.current(0)

        self.perm_var3_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var3_unit_myCombo.current(0)

        self.perm_var4_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var4_unit_myCombo.current(0)

        self.perm_var5_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var5_unit_myCombo.current(0)

        self.perm_var6_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var6_unit_myCombo.current(0)

        self.perm_var7_unit_myCombo = ttk.Combobox(self.ffperm_frame, value=self.select_var_units, width=5)
        self.perm_var7_unit_myCombo.current(0)


        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        self.perm_res_min_label = Label(self.ffperm_frame, text=' Min.')
        self.perm_res_max_label = Label(self.ffperm_frame, text=' Max.')
        self.perm_res_prec_label = Label(self.ffperm_frame, text=' Präz.')
        self.perm_res_tol_label = Label(self.ffperm_frame, text='  Tol.')
        self.perm_res_points_label = Label(self.ffperm_frame, text='Punkte')
        self.perm_res_formula_label = Label(self.ffperm_frame, text='Formel')

        self.perm_res_min_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=60)
        self.perm_res_max_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=100)
        self.perm_res_prec_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=140)
        self.perm_res_tol_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=180)
        self.perm_res_points_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=220)
        self.perm_res_formula_label.grid(row=20, column=1, sticky=E, pady=(10, 0), padx=100)



        self.perm_result1_label = Label(self.ffperm_frame, text='Ergebnis 1')
        self.perm_result2_label = Label(self.ffperm_frame, text='Ergebnis 2')
        self.perm_result3_label = Label(self.ffperm_frame, text='Ergebnis 3')
        self.perm_result4_label = Label(self.ffperm_frame, text='Ergebnis 4')
        self.perm_result5_label = Label(self.ffperm_frame, text='Ergebnis 5')
        self.perm_result6_label = Label(self.ffperm_frame, text='Ergebnis 6')
        self.perm_result7_label = Label(self.ffperm_frame, text='Ergebnis 7')
        self.perm_result8_label = Label(self.ffperm_frame, text='Ergebnis 8')
        self.perm_result9_label = Label(self.ffperm_frame, text='Ergebnis 9')
        self.perm_result10_label = Label(self.ffperm_frame, text='Ergebnis 10')

        # Label für Res1 ist immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.perm_result1_label.grid(row=21, column=0, sticky=W, padx=20)

        ########################### ERGEBNIS TEXTE DEKLARIEREN ##############################

        self.perm_res1_name_text, self.perm_res1_min_text, self.perm_res1_max_text, self.perm_res1_prec_text, self.perm_res1_tol_text, self.perm_res1_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res2_name_text, self.perm_res2_min_text, self.perm_res2_max_text, self.perm_res2_prec_text, self.perm_res2_tol_text, self.perm_res2_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res3_name_text, self.perm_res3_min_text, self.perm_res3_max_text, self.perm_res3_prec_text, self.perm_res3_tol_text, self.perm_res3_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res4_name_text, self.perm_res4_min_text, self.perm_res4_max_text, self.perm_res4_prec_text, self.perm_res4_tol_text, self.perm_res4_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res5_name_text, self.perm_res5_min_text, self.perm_res5_max_text, self.perm_res5_prec_text, self.perm_res5_tol_text, self.perm_res5_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res6_name_text, self.perm_res6_min_text, self.perm_res6_max_text, self.perm_res6_prec_text, self.perm_res6_tol_text, self.perm_res6_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res7_name_text, self.perm_res7_min_text, self.perm_res7_max_text, self.perm_res7_prec_text, self.perm_res7_tol_text, self.perm_res7_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res8_name_text, self.perm_res8_min_text, self.perm_res8_max_text, self.perm_res8_prec_text, self.perm_res8_tol_text, self.perm_res8_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res9_name_text, self.perm_res9_min_text, self.perm_res9_max_text, self.perm_res9_prec_text, self.perm_res9_tol_text, self.perm_res9_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.perm_res10_name_text, self.perm_res10_min_text, self.perm_res10_max_text, self.perm_res10_prec_text, self.perm_res10_tol_text, self.perm_res10_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        self.perm_res1_formula_text, self.perm_res2_formula_text, self.perm_res3_formula_text = StringVar(), StringVar(), StringVar()
        self.perm_res4_formula_text, self.perm_res5_formula_text, self.perm_res6_formula_text = StringVar(), StringVar(), StringVar()
        self.perm_res7_formula_text, self.perm_res8_formula_text, self.perm_res9_formula_text = StringVar(), StringVar(), StringVar()
        self.perm_res10_formula_text = StringVar()


        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.perm_res1_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_name_text, width=6)
        self.perm_res1_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_min_text, width=6)
        self.perm_res1_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_max_text, width=6)
        self.perm_res1_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_prec_text, width=6)
        self.perm_res1_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_tol_text, width=6)
        self.perm_res1_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_points_text, width=6)
        self.perm_res1_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res1_formula_text, width=30)

        self.perm_res2_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_name_text, width=6)
        self.perm_res2_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_min_text, width=6)
        self.perm_res2_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_max_text, width=6)
        self.perm_res2_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_prec_text, width=6)
        self.perm_res2_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_tol_text, width=6)
        self.perm_res2_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_points_text, width=6)
        self.perm_res2_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res2_formula_text, width=30)

        self.perm_res3_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_name_text, width=6)
        self.perm_res3_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_min_text, width=6)
        self.perm_res3_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_max_text, width=6)
        self.perm_res3_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_prec_text, width=6)
        self.perm_res3_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_tol_text, width=6)
        self.perm_res3_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_points_text, width=6)
        self.perm_res3_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res3_formula_text, width=30)

        self.perm_res4_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_name_text, width=6)
        self.perm_res4_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_min_text, width=6)
        self.perm_res4_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_max_text, width=6)
        self.perm_res4_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_prec_text, width=6)
        self.perm_res4_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_tol_text, width=6)
        self.perm_res4_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_points_text, width=6)
        self.perm_res4_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res4_formula_text, width=30)

        self.perm_res5_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_name_text, width=6)
        self.perm_res5_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_min_text, width=6)
        self.perm_res5_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_max_text, width=6)
        self.perm_res5_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_prec_text, width=6)
        self.perm_res5_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_tol_text, width=6)
        self.perm_res5_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_points_text, width=6)
        self.perm_res5_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res5_formula_text, width=30)

        self.perm_res6_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_name_text, width=6)
        self.perm_res6_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_min_text, width=6)
        self.perm_res6_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_max_text, width=6)
        self.perm_res6_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_prec_text, width=6)
        self.perm_res6_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_tol_text, width=6)
        self.perm_res6_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_points_text, width=6)
        self.perm_res6_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res6_formula_text, width=30)

        self.perm_res7_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_name_text, width=6)
        self.perm_res7_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_min_text, width=6)
        self.perm_res7_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_max_text, width=6)
        self.perm_res7_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_prec_text, width=6)
        self.perm_res7_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_tol_text, width=6)
        self.perm_res7_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_points_text, width=6)
        self.perm_res7_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res7_formula_text, width=30)

        self.perm_res8_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_name_text, width=6)
        self.perm_res8_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_min_text, width=6)
        self.perm_res8_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_max_text, width=6)
        self.perm_res8_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_prec_text, width=6)
        self.perm_res8_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_tol_text, width=6)
        self.perm_res8_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_points_text, width=6)
        self.perm_res8_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res8_formula_text, width=30)

        self.perm_res9_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_name_text, width=6)
        self.perm_res9_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_min_text, width=6)
        self.perm_res9_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_max_text, width=6)
        self.perm_res9_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_prec_text, width=6)
        self.perm_res9_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_tol_text, width=6)
        self.perm_res9_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_points_text, width=6)
        self.perm_res9_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res9_formula_text, width=30)

        self.perm_res10_name_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_name_text, width=6)
        self.perm_res10_min_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_min_text, width=6)
        self.perm_res10_max_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_max_text, width=6)
        self.perm_res10_prec_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_prec_text, width=6)
        self.perm_res10_tol_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_tol_text, width=6)
        self.perm_res10_points_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_points_text, width=6)
        self.perm_res10_formula_entry = Entry(self.ffperm_frame, textvariable=self.perm_res10_formula_text, width=30)

        # Eingabefelder für Res1 sind immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.perm_res1_name_entry.grid(row=21, column=1, sticky=W)
        self.perm_res1_min_entry.grid(row=21, column=1, sticky=W, padx=60)
        self.perm_res1_max_entry.grid(row=21, column=1, sticky=W, padx=100)
        self.perm_res1_prec_entry.grid(row=21, column=1, sticky=W, padx=140)
        self.perm_res1_tol_entry.grid(row=21, column=1, sticky=W, padx=180)
        self.perm_res1_points_entry.grid(row=21, column=1, sticky=W, padx=220)
        self.perm_res1_formula_entry.grid(row=21, column=1, sticky=E, padx=20)







        #################### EINHEITEN FÜR ERGEBNISSE DERZEIT DEAKTIVIERT

        # self.perm_res1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.perm_res1_unit_myCombo.current(0)
        # self.perm_res1_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        # #self.perm_res1_unit_myCombo.grid(row=21, column=0, sticky=E, padx=10)
        #
        # self.perm_res2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.perm_res2_unit_myCombo.current(0)
        # self.perm_res2_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        #
        # self.perm_res3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.perm_res3_unit_myCombo.current(0)
        # self.perm_res3_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)




        def ffperm_result_selected(event):  # "variable" need for comboBox Binding

            if self.ffperm_numbers_of_results_box.get() == '1':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '2':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '3':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '4':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '5':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '6':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '7':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '8':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "remove")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '9':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "remove")


            elif self.ffperm_numbers_of_results_box.get() == '10':
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result2_label, self.perm_res2_name_entry, self.perm_res2_min_entry, self.perm_res2_max_entry, self.perm_res2_prec_entry, self.perm_res2_tol_entry, self.perm_res2_points_entry, self.perm_res2_formula_entry, "22", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result3_label, self.perm_res3_name_entry, self.perm_res3_min_entry, self.perm_res3_max_entry, self.perm_res3_prec_entry, self.perm_res3_tol_entry, self.perm_res3_points_entry, self.perm_res3_formula_entry, "23", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result4_label, self.perm_res4_name_entry, self.perm_res4_min_entry, self.perm_res4_max_entry, self.perm_res4_prec_entry, self.perm_res4_tol_entry, self.perm_res4_points_entry, self.perm_res4_formula_entry, "24", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result5_label, self.perm_res5_name_entry, self.perm_res5_min_entry, self.perm_res5_max_entry, self.perm_res5_prec_entry, self.perm_res5_tol_entry, self.perm_res5_points_entry, self.perm_res5_formula_entry, "25", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result6_label, self.perm_res6_name_entry, self.perm_res6_min_entry, self.perm_res6_max_entry, self.perm_res6_prec_entry, self.perm_res6_tol_entry, self.perm_res6_points_entry, self.perm_res6_formula_entry, "26", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result7_label, self.perm_res7_name_entry, self.perm_res7_min_entry, self.perm_res7_max_entry, self.perm_res7_prec_entry, self.perm_res7_tol_entry, self.perm_res7_points_entry, self.perm_res7_formula_entry, "27", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result8_label, self.perm_res8_name_entry, self.perm_res8_min_entry, self.perm_res8_max_entry, self.perm_res8_prec_entry, self.perm_res8_tol_entry, self.perm_res8_points_entry, self.perm_res8_formula_entry, "28", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result9_label, self.perm_res9_name_entry, self.perm_res9_min_entry, self.perm_res9_max_entry, self.perm_res9_prec_entry, self.perm_res9_tol_entry, self.perm_res9_points_entry, self.perm_res9_formula_entry, "29", "show")
                Formelfrage_Permutation.ffperm_result_show_or_remove(self, self.perm_result10_label, self.perm_res10_name_entry, self.perm_res10_min_entry, self.perm_res10_max_entry, self.perm_res10_prec_entry, self.perm_res10_tol_entry, self.perm_res10_points_entry, self.perm_res10_formula_entry, "30", "show")


        self.ffperm_numbers_of_results_box_label = Label(self.ffperm_frame, text="Anzahl der Ergebnisse: ")
        self.ffperm_numbers_of_results_box_label.grid(row=20, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ffperm_numbers_of_results_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.ffperm_numbers_of_results_box = ttk.Combobox(self.ffperm_frame, value=self.ffperm_numbers_of_results_value, width=3)
        self.ffperm_numbers_of_results_box.current(0)
        self.ffperm_numbers_of_results_box.bind("<<ComboboxSelected>>", ffperm_result_selected)
        self.ffperm_numbers_of_results_box.grid(row=20, column=1, sticky=W, pady=(20, 0))

    def ffperm_variable_show_or_remove(self, var_label, var_name_entry, var_min_entry, var_max_entry, var_prec_entry, var_divby_entry, row_nr, var_status, perm_var_symbol_entry, perm_var_value_entry):

            if var_status == "show":
                var_label.grid(row=int(row_nr), column=0, sticky=W, padx=20)
                var_name_entry.grid(row=int(row_nr), column=1, sticky=W)
                var_min_entry.grid(row=int(row_nr), column=1, sticky=W, padx=60)
                var_max_entry.grid(row=int(row_nr), column=1, sticky=W, padx=100)
                var_prec_entry.grid(row=int(row_nr), column=1, sticky=W, padx=140)
                var_divby_entry.grid(row=int(row_nr), column=1, sticky=W, padx=180)
                # var_unit_myCombo.grid(row=int(row_nr), column=0, sticky=E, padx=10)


                perm_var_symbol_entry.grid(row=int(row_nr), column=1, sticky=E, padx=123)
                perm_var_value_entry.grid(row=int(row_nr), column=1, sticky=E, padx=0)



            else:
                var_label.grid_remove()
                var_name_entry.grid_remove()
                var_min_entry.grid_remove()
                var_max_entry.grid_remove()
                var_prec_entry.grid_remove()
                var_divby_entry.grid_remove()
                # var_unit_myCombo.grid_remove()


                perm_var_symbol_entry.grid_remove()
                perm_var_value_entry.grid_remove()


    def ffperm_result_show_or_remove(self, res_label, res_name_entry, res_min_entry, res_max_entry, res_prec_entry, res_tol_entry, res_points_entry, res_formula_entry, row_nr, res_status):

        if res_status == "show":
            res_label.grid(row=int(row_nr), column=0, sticky=W, padx=20)
            res_name_entry.grid(row=int(row_nr), column=1, sticky=W)
            res_min_entry.grid(row=int(row_nr), column=1, sticky=W, padx=60)
            res_max_entry.grid(row=int(row_nr), column=1, sticky=W, padx=100)
            res_prec_entry.grid(row=int(row_nr), column=1, sticky=W, padx=140)
            res_tol_entry.grid(row=int(row_nr), column=1, sticky=W, padx=180)
            res_points_entry.grid(row=int(row_nr), column=1, sticky=W, padx=220)
            res_formula_entry.grid(row=int(row_nr), column=1, sticky=E, padx=20)
            #res_unit_myCombo.grid(row=int(row_nr), column=0, sticky=E, padx=10)

        else:
            res_label.grid_remove()
            res_name_entry.grid_remove()
            res_min_entry.grid_remove()
            res_max_entry.grid_remove()
            res_prec_entry.grid_remove()
            res_tol_entry.grid_remove()
            res_points_entry.grid_remove()
            res_formula_entry.grid_remove()
            #var_unit_myCombo.grid_remove()

    def unit_table(self, selected_unit):
        self.unit_to_ilias_code = { "H" : "125", "mH" : "126", "µH" : "127", "nH" : "128", "kH" : "129", "pH" : "130",
                                    "F" : "131", "mF" : "132", "µF" : "133", "nF" : "134", "kF" : "135",
                                    "W" : "136", "kW" : "137", "MW" : "138", "mW" : "149",
                                    "V" : "139", "kV" : "140", "mV" : "141", "µV" : "142", "MV" : "143",
                                    "A" : "144", "mA" : "145", "µA" : "146", "kA" : "147",
                                    "Ohm" : "148", "kOhm" : "150", "mOhm" : "151"}


        self.perm_var_selected_unit = selected_unit
        self.selected_unit = self.unit_to_ilias_code[self.perm_var_selected_unit]
        return self.selected_unit

    def ffperm_replace_character_in_xml_file(self, file_path_qti_xml):
        # Im Nachgang werden alle "&amp;" wieder gegen "&" getauscht
        # "&" Zeichen kann XML nicht verarbeiten, daher wurde beim schreiben der Texte in die XML "&" gegen "&amp;" getauscht

        # XML Datei zum lesen öffnen 'r' -> "read"
        with open(file_path_qti_xml, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&') #replace 'x' with 'new_x'

        # In XML Datei schreiben 'w" -> "write"
        with open(file_path_qti_xml, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("...XML_DATEI_QTI --  \"&amp;\"-ZEICHEN ÜBERARBEITUNG ABGESCHLOSSEN!")

    """
    def ffperm_add_image_to_description(self, check_use_img_1, check_use_img_2, check_use_img_3):

        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        # Bild 1 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_1 == 1:
            self.ffperm_description_img_path_1 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_1 = self.ffperm_description_img_path_1.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ffperm_description_img_name_1= self.ffperm_description_img_path_1[int(self.last_char_index_img_1) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_1 = self.ffperm_description_img_path_1[-4:]

            self.ffperm_question_description_img_1_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_1)
            self.ffperm_question_description_img_1_filename_label.grid(row=0, column=1, sticky=W)

            self.file_image_1 = ImageTk.PhotoImage(Image.open(self.ffperm_description_img_path_1).resize((100, 100)))
            self.file_image_1_raw = Image.open(self.ffperm_description_img_path_1)
            self.file_image_1_width, self.file_image_1_height = self.file_image_1_raw.size
            self.file_image_1_label = Label(self.ffperm_frame_description_picture, image=self.file_image_1)
            self.file_image_1_label.image = self.file_image_1
            self.file_image_1_label.grid(row=0, column=2)


        # Bild 2 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_2 == 1:
            self.ffperm_description_img_path_2 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_2 = self.ffperm_description_img_path_2.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ffperm_description_img_name_2= self.ffperm_description_img_path_2[int(self.last_char_index_img_2) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_2 = self.ffperm_description_img_path_2[-4:]

            self.ffperm_question_description_img_2_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_2)
            self.ffperm_question_description_img_2_filename_label.grid(row=1, column=1, sticky=W)


            self.file_image_2 = ImageTk.PhotoImage(Image.open(self.ffperm_description_img_path_2).resize((100, 100)))
            self.file_image_2_raw = Image.open(self.ffperm_description_img_path_2)
            self.file_image_2_width, self.file_image_2_height = self.file_image_2_raw.size
            self.file_image_2_label = Label(self.ffperm_frame_description_picture, image=self.file_image_2)
            self.file_image_2_label.image = self.file_image_2
            self.file_image_2_label.grid(row=1, column=2)


        # Bild 3 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_3 == 1:

            self.ffperm_description_img_path_3 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_3 = self.ffperm_description_img_path_3.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ffperm_description_img_name_3 = self.ffperm_description_img_path_3[int(self.last_char_index_img_3) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_3 = self.ffperm_description_img_path_3[-4:]
            self.ffperm_question_description_img_3_filename_label = Label(self.ffperm_frame_description_picture, text=self.ffperm_description_img_name_3)
            self.ffperm_question_description_img_3_filename_label.grid(row=2, column=1, sticky=W)

            self.file_image_3 = ImageTk.PhotoImage(Image.open(self.ffperm_description_img_path_3).resize((100, 100)))
            self.file_image_3_raw = Image.open(self.ffperm_description_img_path_3)
            self.file_image_3_width, self.file_image_3_height = self.file_image_3_raw.size
            self.file_image_3_label = Label(self.ffperm_frame_description_picture, image=self.file_image_3)
            self.file_image_3_label.image = self.file_image_3
            self.file_image_3_label.grid(row=2, column=2)

    def ffperm_delete_image_from_description(self, check_use_img_1, check_use_img_2, check_use_img_3):
        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        if self.check_use_img_1 == 0:
            #print("0 in 1")
            self.ffperm_question_description_img_1_filename_label.grid_remove()
            self.file_image_1_label.grid_remove()
            self.ffperm_description_img_name_1="EMPTY"

        if self.check_use_img_2 == 0:
            self.ffperm_question_description_img_2_filename_label.grid_remove()
            self.file_image_2_label.grid_remove()
            self.ffperm_description_img_name_2="EMPTY"
            #print("0 in 2")
        if self.check_use_img_3 == 0:
            self.ffperm_question_description_img_3_filename_label.grid_remove()
            self.file_image_3_label.grid_remove()
            self.ffperm_description_img_name_3 ="EMPTY"
            #print("0 in 3")
    """
    # Wertebereich berechnen für bis zu 4 Variablen
    def ffperm_replace_symbols_in_formula(self, formula):

        self.formula = formula

        print("----------------------")
        print("Übernehme Formel aus Eingabefeld")

        print(self.formula)
        print("Ersetze alle Symbole mit numpy-symoblik")

        self.np_translator_dict = {"pi": "np.pi",
                                  ",": ".",
                                  "^": "**",
                                  "e": "np.e",
                                  "sin": "np.sin",
                                  "sinh": "np.sinh",
                                  "arcsin": "np.arcsin",
                                  "asin": "np.asin",
                                  "asinh": "np.asinh",
                                  "arcsinh": "np.arcsinh",
                                  "cos": "np.cos",
                                  "cosh": "np.cosh",
                                  "cossin": "np.cossin",
                                  "acos": "np.acos",
                                  "acosh": "np.acosh",
                                  "arccosh": "np.arccosh",
                                  "tan": "np.tan",
                                  "tanh": "np.tanh",
                                  "arctan": "np.arctan",
                                  "atan": "np.atan",
                                  "atanh": "np.atanh",
                                  "arctanh": "np.arctanh",
                                  "sqrt": "np.sqrt",
                                  "abs": "np.abs",
                                  "ln": "np.ln",
                                  "log": "np.log",
                                  "$v1": "row['a']",
                                  "$v2": "row['b']",
                                  "$v3": "row['c']",
                                  "$v4": "row['d']",
                                  "$v5": "row['e']"}

        for item in self.np_translator_dict.keys():
            self.formula = self.formula.replace(item, self.np_translator_dict[item])

        print()
        print(self.formula)
        print("----------------------")
        return self.formula

    def ffperm_calculate_value_range_from_formula(self, formula):

        self.perm_var1_in_formula = 0
        self.perm_var2_in_formula = 0
        self.perm_var3_in_formula = 0
        self.perm_var4_in_formula = 0
        self.perm_var5_in_formula = 0

        # Number of values per range
        N = 21

        # Functions
        #self.calc_formula1 = "lambda row: " + str(self.calc_formula1) + ","

        self.expression_test = Formelfrage_Permutation.ffperm_replace_symbols_in_formula(self, formula)

        if 'a' in self.expression_test:
            #print("$v1 in der Formel")
            self.perm_var1_in_formula = 1

        if 'b' in self.expression_test:
            #print("$v2 in der Formel")
            self.perm_var2_in_formula = 1

        if 'c' in self.expression_test:
            #print("$v3 in der Formel")
            self.perm_var3_in_formula = 1

        if 'd' in self.expression_test:
            #print("$v4 in der Formel")
            self.perm_var4_in_formula = 1

        if 'e' in self.expression_test:
            #print("$v5 in der Formel")
            self.perm_var5_in_formula = 1


        self.exp_as_func = eval('lambda row: ' + self.expression_test)

        functions = [
            #  a * sqrt(b/c)
            #lambda row: row['a'] * np.sqrt(row['b'] / row['c']),
            #lambda row: row['a'] * np.sqrt(row['b']),
            #lambda row: row['a'] ** 2,
            #eval(self.calc_formula1),
            self.exp_as_func

        ]



        # Lower and upper bounds
        if bool(re.search(r'\d', self.perm_var1_min_text.get())) == True and bool(re.search(r'\d', self.perm_var1_min_text.get())) == True:
            try:
                self.perm_var1_lower, self.perm_var1_upper = int(self.perm_var1_min_text.get()), int(self.perm_var1_max_text.get())
            except ValueError:
                self.perm_var1_lower, self.perm_var1_upper = float(self.perm_var1_min_text.get()), float(self.perm_var1_max_text.get())
        else: self.perm_var1_lower, self.perm_var1_upper = 1, 1


        if bool(re.search(r'\d', self.perm_var2_min_text.get())) == True and bool(re.search(r'\d', self.perm_var2_min_text.get())) == True:
            try:
                self.perm_var2_lower, self.perm_var2_upper = int(self.perm_var2_min_text.get()), int(self.perm_var2_max_text.get())
            except ValueError:
                self.perm_var2_lower, self.perm_var2_upper = float(self.perm_var2_min_text.get()), float(self.perm_var2_max_text.get())
        else: self.perm_var2_lower, self.perm_var2_upper = 1, 1


        if bool(re.search(r'\d', self.perm_var3_min_text.get())) == True and bool(re.search(r'\d', self.perm_var3_min_text.get())) == True:
            try:
                self.perm_var3_lower, self.perm_var3_upper = int(self.perm_var3_min_text.get()), int(self.perm_var3_max_text.get())
            except ValueError:
                self.perm_var3_lower, self.perm_var3_upper = float(self.perm_var3_min_text.get()), float(self.perm_var3_max_text.get())
        else: self.perm_var3_lower, self.perm_var3_upper = 1, 1


        if bool(re.search(r'\d', self.perm_var4_min_text.get())) == True and bool(re.search(r'\d', self.perm_var4_min_text.get())) == True:
            try:
                self.perm_var4_lower, self.perm_var4_upper = int(self.perm_var4_min_text.get()), int(self.perm_var4_max_text.get())
            except ValueError:
                self.perm_var4_lower, self.perm_var4_upper = float(self.perm_var4_min_text.get()), float(self.perm_var4_max_text.get())
        else: self.perm_var4_lower, self.perm_var4_upper = 1, 1










        a_lower, a_upper = self.perm_var1_lower, self.perm_var1_upper
        b_lower, b_upper = self.perm_var2_lower, self.perm_var2_upper
        c_lower, c_upper = self.perm_var3_lower, self.perm_var3_upper
        d_lower, d_upper = self.perm_var4_lower, self.perm_var4_upper
        #e_lower, e_upper = self.perm_var5_lower, self.perm_var5_upper


        def min_max(col):
            return pd.Series(index=['min', 'max'], data=[col.min(), col.max()])

        #values = [
        #    np.linspace(a_lower, a_upper, N),
        #    np.linspace(b_lower, b_upper, N),
        #    np.linspace(c_lower, c_upper, N),
        #    np.linspace(d_lower, d_upper, N),

        #]

        #print(values)
        print("---------------------------")
        print()



        #df = pd.DataFrame(cartesian_product(values), index=['a', 'b', 'c', 'd']).T

        self.set_nr_of_var_index = []

        #print(self.perm_var1_in_formula, self.perm_var2_in_formula, self.perm_var3_in_formula, self.perm_var4_in_formula, self.perm_var5_in_formula)
        if self.perm_var1_in_formula == 1 and self.perm_var2_in_formula == 0 and self.perm_var3_in_formula == 0 and self.perm_var4_in_formula == 0 and self.perm_var5_in_formula == 0:
             print("Berechne Formel mit 1 Variablen: ...")
             self.set_nr_of_var_index=['a']
             values = [
                 np.linspace(a_lower, a_upper, N),
             ]

        if self.perm_var1_in_formula == 1 and self.perm_var2_in_formula == 1 and self.perm_var3_in_formula == 0 and self.perm_var4_in_formula == 0 and self.perm_var5_in_formula == 0:
            print("Berechne Formel mit 2 Variablen: ...")
            self.set_nr_of_var_index = ['a', 'b']
            values = [
                np.linspace(a_lower, a_upper, N),
                np.linspace(b_lower, b_upper, N),
            ]

        if self.perm_var1_in_formula == 1 and self.perm_var2_in_formula == 1 and self.perm_var3_in_formula == 1 and self.perm_var4_in_formula == 0 and self.perm_var5_in_formula == 0:
            print("Berechne Formel mit 3 Variablen: ...")
            self.set_nr_of_var_index = ['a', 'b', 'c']
            values = [
                np.linspace(a_lower, a_upper, N),
                np.linspace(b_lower, b_upper, N),
                np.linspace(c_lower, c_upper, N),
            ]

        if self.perm_var1_in_formula == 1 and self.perm_var2_in_formula == 1 and self.perm_var3_in_formula == 1 and self.perm_var4_in_formula == 1 and self.perm_var5_in_formula == 0:
            print("Berechne Formel mit 4 Variablen: ...")
            self.set_nr_of_var_index = ['a', 'b', 'c', 'd']
            values = [
                np.linspace(a_lower, a_upper, N),
                np.linspace(b_lower, b_upper, N),
                np.linspace(c_lower, c_upper, N),
                np.linspace(d_lower, d_upper, N),
            ]


        df = pd.DataFrame(cartesian_product(values), index=self.set_nr_of_var_index).T
        for i, f in enumerate(functions):
            df[f'f_{i + 1}'] = df.apply(f, axis=1)
        print()
        print(df.apply(min_max))

        print()
        print("Ergebnis berechnet!")


#############  DATENBANK FUNKTIONEN
    def ffperm_save_id_to_db(self):
        conn = sqlite3.connect(self.database_formelfrage_permutation_path)
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.ffperm_test_time = "P0Y0M0DT" + self.ffperm_proc_hours_box.get() + "H" + self.ffperm_proc_minutes_box.get() + "M" + self.ffperm_proc_seconds_box.get() + "S"


        # Bild 1
        if self.ffperm_description_img_name_1!= "":
            # read image data in byte format
            print(self.ffperm_description_img_name_1)
            print(self.ffperm_description_img_path_1)
            with open(self.ffperm_description_img_path_1, 'rb') as image_file_1:
                self.ffperm_description_img_data_1 = image_file_1.read()


        else:
            self.ffperm_description_img_name_1= ""
            self.ffperm_description_img_path_1 = ""
            self.ffperm_description_img_data_1 = ""


        # Bild 2
        if self.ffperm_description_img_name_2!= "":
            # read image data in byte format
            print(self.ffperm_description_img_name_2)
            print(self.ffperm_description_img_path_2)
            with open(self.ffperm_description_img_path_2, 'rb') as image_file_2:
                self.ffperm_description_img_data_2 = image_file_2.read()


        else:
            self.ffperm_description_img_name_2= ""
            self.ffperm_description_img_path_2 = ""
            self.ffperm_description_img_data_2 = ""


        # Bild 3
        if self.ffperm_description_img_name_3 != "":

            # read image data in byte format
            print(self.ffperm_description_img_name_3)
            print(self.ffperm_description_img_path_3)
            with open(self.ffperm_description_img_path_3, 'rb') as image_file_3:
                self.ffperm_description_img_data_3 = image_file_3.read()


        else:
            self.ffperm_description_img_name_3 = ""
            self.ffperm_description_img_path_3 = ""
            self.ffperm_description_img_data_3 = ""


        # Insert into Table
        c.execute(
            "INSERT INTO formelfrage_permutation_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":res1_formula, :res2_formula, :res3_formula,  "
            ":res4_formula, :res5_formula, :res6_formula,  "
            ":res7_formula, :res8_formula, :res9_formula, :res10_formula,  "
            ":var1_name, :var1_min, :var1_max, :var1_prec, :var1_divby, :var1_unit, "
            ":var2_name, :var2_min, :var2_max, :var2_prec, :var2_divby, :var2_unit, "
            ":var3_name, :var3_min, :var3_max, :var3_prec, :var3_divby, :var3_unit, "
            ":var4_name, :var4_min, :var4_max, :var4_prec, :var4_divby, :var4_unit, "
            ":var5_name, :var5_min, :var5_max, :var5_prec, :var5_divby, :var5_unit, "
            ":var6_name, :var6_min, :var6_max, :var6_prec, :var6_divby, :var6_unit, "
            ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby, :var7_unit, "
            ":var8_name, :var8_min, :var8_max, :var8_prec, :var8_divby, :var8_unit, "
            ":var9_name, :var9_min, :var9_max, :var9_prec, :var9_divby, :var9_unit, "
            ":var10_name, :var10_min, :var10_max, :var10_prec, :var10_divby, :var10_unit, "
            ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, :res1_unit, "
            ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, :res2_unit, "
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit, "
            ":res4_name, :res4_min, :res4_max, :res4_prec, :res4_tol, :res4_points, :res4_unit, "
            ":res5_name, :res5_min, :res5_max, :res5_prec, :res5_tol, :res5_points, :res5_unit, "
            ":res6_name, :res6_min, :res6_max, :res6_prec, :res6_tol, :res6_points, :res6_unit, "
            ":res7_name, :res7_min, :res7_max, :res7_prec, :res7_tol, :res7_points, :res7_unit, "
            ":res8_name, :res8_min, :res8_max, :res8_prec, :res8_tol, :res8_points, :res8_unit, "
            ":res9_name, :res9_min, :res9_max, :res9_prec, :res9_tol, :res9_points, :res9_unit, "
            ":res10_name, :res10_min, :res10_max, :res10_prec, :res10_tol, :res10_points, :res10_unit, "
            ":perm_var_symbol_1, :perm_var_value_1,"
            ":perm_var_symbol_2, :perm_var_value_2,"
            ":perm_var_symbol_3, :perm_var_value_3,"
            ":perm_var_symbol_4, :perm_var_value_4,"
            ":perm_var_symbol_5, :perm_var_value_5,"
            ":perm_var_symbol_6, :perm_var_value_6,"
            ":perm_var_symbol_7, :perm_var_value_7,"
            ":perm_var_symbol_8, :perm_var_value_8,"
            ":perm_var_symbol_9, :perm_var_value_9,"
            ":perm_var_symbol_10, :perm_var_value_10,"
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :res_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': self.ffperm_question_difficulty_entry.get(),
                'question_category': self.ffperm_question_category_entry.get(),
                'question_type': self.ffperm_question_type_entry.get(),

                'question_title': self.ffperm_question_title_entry.get(),
                'question_description_title': self.ffperm_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.ffperm_question_description_main_entry.get("1.0", 'end-1c'),

                'res1_formula': self.perm_res1_formula_entry.get(),
                'res2_formula': self.perm_res2_formula_entry.get(),
                'res3_formula': self.perm_res3_formula_entry.get(),
                'res4_formula': self.perm_res4_formula_entry.get(),
                'res5_formula': self.perm_res5_formula_entry.get(),
                'res6_formula': self.perm_res6_formula_entry.get(),
                'res7_formula': self.perm_res7_formula_entry.get(),
                'res8_formula': self.perm_res8_formula_entry.get(),
                'res9_formula': self.perm_res9_formula_entry.get(),
                'res10_formula': self.perm_res10_formula_entry.get(),

                'var1_name': self.perm_var1_name_entry.get(),
                'var1_min': self.perm_var1_min_entry.get(),
                'var1_max': self.perm_var1_max_entry.get(),
                'var1_prec': self.perm_var1_prec_entry.get(),
                'var1_divby': self.perm_var1_divby_entry.get(),
                'var1_unit': "",

                'var2_name': self.perm_var2_name_entry.get(),
                'var2_min': self.perm_var2_min_entry.get(),
                'var2_max': self.perm_var2_max_entry.get(),
                'var2_prec': self.perm_var2_prec_entry.get(),
                'var2_divby': self.perm_var2_divby_entry.get(),
                'var2_unit': "",

                'var3_name': self.perm_var3_name_entry.get(),
                'var3_min': self.perm_var3_min_entry.get(),
                'var3_max': self.perm_var3_max_entry.get(),
                'var3_prec': self.perm_var3_prec_entry.get(),
                'var3_divby': self.perm_var3_divby_entry.get(),
                'var3_unit': "",

                'var4_name': self.perm_var4_name_entry.get(),
                'var4_min': self.perm_var4_min_entry.get(),
                'var4_max': self.perm_var4_max_entry.get(),
                'var4_prec': self.perm_var4_prec_entry.get(),
                'var4_divby': self.perm_var4_divby_entry.get(),
                'var4_unit': "",

                'var5_name': self.perm_var5_name_entry.get(),
                'var5_min': self.perm_var5_min_entry.get(),
                'var5_max': self.perm_var5_max_entry.get(),
                'var5_prec': self.perm_var5_prec_entry.get(),
                'var5_divby': self.perm_var5_divby_entry.get(),
                'var5_unit': "",

                'var6_name': self.perm_var6_name_entry.get(),
                'var6_min': self.perm_var6_min_entry.get(),
                'var6_max': self.perm_var6_max_entry.get(),
                'var6_prec': self.perm_var6_prec_entry.get(),
                'var6_divby': self.perm_var6_divby_entry.get(),
                'var6_unit': "",

                'var7_name': self.perm_var7_name_entry.get(),
                'var7_min': self.perm_var7_min_entry.get(),
                'var7_max': self.perm_var7_max_entry.get(),
                'var7_prec': self.perm_var7_prec_entry.get(),
                'var7_divby': self.perm_var7_divby_entry.get(),
                'var7_unit': "",

                'var8_name': self.perm_var8_name_entry.get(),
                'var8_min': self.perm_var8_min_entry.get(),
                'var8_max': self.perm_var8_max_entry.get(),
                'var8_prec': self.perm_var8_prec_entry.get(),
                'var8_divby': self.perm_var8_divby_entry.get(),
                'var8_unit': "",

                'var9_name': self.perm_var9_name_entry.get(),
                'var9_min': self.perm_var9_min_entry.get(),
                'var9_max': self.perm_var9_max_entry.get(),
                'var9_prec': self.perm_var9_prec_entry.get(),
                'var9_divby': self.perm_var9_divby_entry.get(),
                'var9_unit': "",

                'var10_name': self.perm_var10_name_entry.get(),
                'var10_min': self.perm_var10_min_entry.get(),
                'var10_max': self.perm_var10_max_entry.get(),
                'var10_prec': self.perm_var10_prec_entry.get(),
                'var10_divby': self.perm_var10_divby_entry.get(),
                'var10_unit': "",

                'res1_name': self.perm_res1_name_entry.get(),
                'res1_min': self.perm_res1_min_entry.get(),
                'res1_max': self.perm_res1_max_entry.get(),
                'res1_prec': self.perm_res1_prec_entry.get(),
                'res1_tol': self.perm_res1_tol_entry.get(),
                'res1_points': self.perm_res1_points_entry.get(),
                'res1_unit': "",

                'res2_name': self.perm_res2_name_entry.get(),
                'res2_min': self.perm_res2_min_entry.get(),
                'res2_max': self.perm_res2_max_entry.get(),
                'res2_prec': self.perm_res2_prec_entry.get(),
                'res2_tol': self.perm_res2_tol_entry.get(),
                'res2_points': self.perm_res2_points_entry.get(),
                'res2_unit': "",

                'res3_name': self.perm_res3_name_entry.get(),
                'res3_min': self.perm_res3_min_entry.get(),
                'res3_max': self.perm_res3_max_entry.get(),
                'res3_prec': self.perm_res3_prec_entry.get(),
                'res3_tol': self.perm_res3_tol_entry.get(),
                'res3_points': self.perm_res3_points_entry.get(),
                'res3_unit': "",

                'res4_name': self.perm_res4_name_entry.get(),
                'res4_min': self.perm_res4_min_entry.get(),
                'res4_max': self.perm_res4_max_entry.get(),
                'res4_prec': self.perm_res4_prec_entry.get(),
                'res4_tol': self.perm_res4_tol_entry.get(),
                'res4_points': self.perm_res4_points_entry.get(),
                'res4_unit': "",

                'res5_name': self.perm_res5_name_entry.get(),
                'res5_min': self.perm_res5_min_entry.get(),
                'res5_max': self.perm_res5_max_entry.get(),
                'res5_prec': self.perm_res5_prec_entry.get(),
                'res5_tol': self.perm_res5_tol_entry.get(),
                'res5_points': self.perm_res5_points_entry.get(),
                'res5_unit': "",

                'res6_name': self.perm_res6_name_entry.get(),
                'res6_min': self.perm_res6_min_entry.get(),
                'res6_max': self.perm_res6_max_entry.get(),
                'res6_prec': self.perm_res6_prec_entry.get(),
                'res6_tol': self.perm_res6_tol_entry.get(),
                'res6_points': self.perm_res6_points_entry.get(),
                'res6_unit': "",

                'res7_name': self.perm_res7_name_entry.get(),
                'res7_min': self.perm_res7_min_entry.get(),
                'res7_max': self.perm_res7_max_entry.get(),
                'res7_prec': self.perm_res7_prec_entry.get(),
                'res7_tol': self.perm_res7_tol_entry.get(),
                'res7_points': self.perm_res7_points_entry.get(),
                'res7_unit': "",

                'res8_name': self.perm_res8_name_entry.get(),

                'res8_min': self.perm_res8_min_entry.get(),
                'res8_max': self.perm_res8_max_entry.get(),
                'res8_prec': self.perm_res8_prec_entry.get(),
                'res8_tol': self.perm_res8_tol_entry.get(),
                'res8_points': self.perm_res8_points_entry.get(),
                'res8_unit': "",

                'res9_name': self.perm_res9_name_entry.get(),
                'res9_min': self.perm_res9_min_entry.get(),
                'res9_max': self.perm_res9_max_entry.get(),
                'res9_prec': self.perm_res9_prec_entry.get(),
                'res9_tol': self.perm_res9_tol_entry.get(),
                'res9_points': self.perm_res9_points_entry.get(),
                'res9_unit': "",

                'res10_name': self.perm_res10_name_entry.get(),
                'res10_min': self.perm_res10_min_entry.get(),
                'res10_max': self.perm_res10_max_entry.get(),
                'res10_prec': self.perm_res10_prec_entry.get(),
                'res10_tol': self.perm_res10_tol_entry.get(),
                'res10_points': self.perm_res10_points_entry.get(),
                'res10_unit': "",

                
                'perm_var_symbol_1': self.perm_var_symbol_entry_1.get(),
                'perm_var_value_1': self.perm_var_value_entry_1.get(),
                
                'perm_var_symbol_2': self.perm_var_symbol_entry_2.get(),
                'perm_var_value_2': self.perm_var_value_entry_2.get(),
                
                'perm_var_symbol_3': self.perm_var_symbol_entry_3.get(),
                'perm_var_value_3': self.perm_var_value_entry_3.get(),
                
                'perm_var_symbol_4': self.perm_var_symbol_entry_4.get(),
                'perm_var_value_4': self.perm_var_value_entry_4.get(),
                
                'perm_var_symbol_5': self.perm_var_symbol_entry_5.get(),
                'perm_var_value_5': self.perm_var_value_entry_5.get(),
               
                'perm_var_symbol_6': self.perm_var_symbol_entry_6.get(),
                'perm_var_value_6': self.perm_var_value_entry_6.get(),
                
                'perm_var_symbol_7': self.perm_var_symbol_entry_7.get(),
                'perm_var_value_7': self.perm_var_value_entry_7.get(),
                
                'perm_var_symbol_8': self.perm_var_symbol_entry_8.get(),
                'perm_var_value_8': self.perm_var_value_entry_8.get(),
                
                'perm_var_symbol_9': self.perm_var_symbol_entry_9.get(),
                'perm_var_value_9': self.perm_var_value_entry_9.get(),
                
                'perm_var_symbol_10': self.perm_var_symbol_entry_10.get(),
                'perm_var_value_10': self.perm_var_value_entry_10.get(),



                'description_img_name_1': self.ffperm_description_img_name_1,
                'description_img_data_1': self.ffperm_description_img_data_1,
                'description_img_path_1': self.ffperm_description_img_path_1,

                'description_img_name_2': self.ffperm_description_img_name_2,
                'description_img_data_2': self.ffperm_description_img_data_2,
                'description_img_path_2': self.ffperm_description_img_path_2,

                'description_img_name_3': self.ffperm_description_img_name_3,
                'description_img_data_3': self.ffperm_description_img_data_3,
                'description_img_path_3': self.ffperm_description_img_path_3,

                'test_time': self.ffperm_test_time,
                'var_number': self.ffperm_numbers_of_answers_box.get(),
                'res_number': self.ffperm_numbers_of_results_box.get(),
                'question_pool_tag': self.ffperm_question_pool_tag_entry.get(),
                'question_author': self.ffperm_question_author_entry.get()
            }
        )
        conn.commit()
        conn.close()

        print("Neue Frage in DB gespeichert. --> Titel: " + str(self.ffperm_question_title_entry.get()))

    def ffperm_load_id_from_db(self, entry_to_index_dict):
        self.ffperm_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_formelfrage_permutation_path)
        c = conn.cursor()
        record_id = self.ffperm_load_box.get()
        c.execute("SELECT * FROM formelfrage_permutation_table WHERE oid =" + record_id)
        ffperm_db_records = c.fetchall()


        Formelfrage_Permutation.ffperm_clear_GUI(self)


        for ffperm_db_record in ffperm_db_records:
            self.ffperm_question_difficulty_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_difficulty']] )
            self.ffperm_question_category_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_category']])
            self.ffperm_question_type_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_type']])

            self.ffperm_question_title_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_title']])
            self.ffperm_question_description_title_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_description_title']])
            self.ffperm_question_description_main_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_description_main']])

            self.perm_res1_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_formula']])
            self.perm_res2_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_formula']])
            self.perm_res3_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_formula']])
            self.perm_res4_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_formula']])
            self.perm_res5_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_formula']])
            self.perm_res6_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_formula']])
            self.perm_res7_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_formula']])
            self.perm_res8_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_formula']])
            self.perm_res9_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_formula']])
            self.perm_res10_formula_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_formula']])

            self.perm_var1_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_name']])
            self.perm_var1_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_min']])
            self.perm_var1_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_max']])
            self.perm_var1_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_prec']])
            self.perm_var1_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_divby']])


            self.perm_var2_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_name']])
            self.perm_var2_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_min']])
            self.perm_var2_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_max']])
            self.perm_var2_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_prec']])
            self.perm_var2_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_divby']])


            self.perm_var3_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_name']])
            self.perm_var3_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_min']])
            self.perm_var3_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_max']])
            self.perm_var3_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_prec']])
            self.perm_var3_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_divby']])


            self.perm_var4_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_name']])
            self.perm_var4_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_min']])
            self.perm_var4_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_max']])
            self.perm_var4_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_prec']])
            self.perm_var4_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_divby']])


            self.perm_var5_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_name']])
            self.perm_var5_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_min']])
            self.perm_var5_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_max']])
            self.perm_var5_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_prec']])
            self.perm_var5_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_divby']])


            self.perm_var6_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_name']])
            self.perm_var6_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_min']])
            self.perm_var6_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_max']])
            self.perm_var6_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_prec']])
            self.perm_var6_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_divby']])


            self.perm_var7_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_name']])
            self.perm_var7_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_min']])
            self.perm_var7_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_max']])
            self.perm_var7_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_prec']])
            self.perm_var7_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_divby']])


            self.perm_var8_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_name']])
            self.perm_var8_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_min']])
            self.perm_var8_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_max']])
            self.perm_var8_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_prec']])
            self.perm_var8_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_divby']])


            self.perm_var9_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_name']])
            self.perm_var9_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_min']])
            self.perm_var9_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_max']])
            self.perm_var9_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_prec']])
            self.perm_var9_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_divby']])


            self.perm_var10_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_name']])
            self.perm_var10_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_min']])
            self.perm_var10_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_max']])
            self.perm_var10_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_prec']])
            self.perm_var10_divby_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_divby']])


            self.perm_res1_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_name']])
            self.perm_res1_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_min']])
            self.perm_res1_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_max']])
            self.perm_res1_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_prec']])
            self.perm_res1_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_tol']])
            self.perm_res1_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_points']])


            self.perm_res2_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_name']])
            self.perm_res2_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_min']])
            self.perm_res2_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_max']])
            self.perm_res2_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_prec']])
            self.perm_res2_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_tol']])
            self.perm_res2_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_points']])


            self.perm_res3_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_name']])
            self.perm_res3_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_min']])
            self.perm_res3_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_max']])
            self.perm_res3_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_prec']])
            self.perm_res3_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_tol']])
            self.perm_res3_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_points']])


            self.perm_res4_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_name']])
            self.perm_res4_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_min']])
            self.perm_res4_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_max']])
            self.perm_res4_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_prec']])
            self.perm_res4_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_tol']])
            self.perm_res4_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_points']])


            self.perm_res5_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_name']])
            self.perm_res5_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_min']])
            self.perm_res5_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_max']])
            self.perm_res5_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_prec']])
            self.perm_res5_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_tol']])
            self.perm_res5_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_points']])


            self.perm_res6_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_name']])
            self.perm_res6_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_min']])
            self.perm_res6_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_max']])
            self.perm_res6_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_prec']])
            self.perm_res6_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_tol']])
            self.perm_res6_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_points']])


            self.perm_res7_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_name']])
            self.perm_res7_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_min']])
            self.perm_res7_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_max']])
            self.perm_res7_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_prec']])
            self.perm_res7_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_tol']])
            self.perm_res7_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_points']])


            self.perm_res8_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_name']])
            self.perm_res8_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_min']])
            self.perm_res8_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_max']])
            self.perm_res8_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_prec']])
            self.perm_res8_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_tol']])
            self.perm_res8_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_points']])


            self.perm_res9_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_name']])
            self.perm_res9_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_min']])
            self.perm_res9_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_max']])
            self.perm_res9_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_prec']])
            self.perm_res9_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_tol']])
            self.perm_res9_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_points']])


            self.perm_res10_name_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_name']])
            self.perm_res10_min_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_min']])
            self.perm_res10_max_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_max']])
            self.perm_res10_prec_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_prec']])
            self.perm_res10_tol_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_tol']])
            self.perm_res10_points_entry.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_points']])

           
            self.perm_var_symbol_entry_1.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_1']])
            self.perm_var_value_entry_1.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_1']])
         
            self.perm_var_symbol_entry_2.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_2']])
            self.perm_var_value_entry_2.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_2']])
        
            self.perm_var_symbol_entry_3.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_3']])
            self.perm_var_value_entry_3.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_3']])
        
            self.perm_var_symbol_entry_4.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_4']])
            self.perm_var_value_entry_4.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_4']])
           
            self.perm_var_symbol_entry_5.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_5']])
            self.perm_var_value_entry_5.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_5']])
           
            self.perm_var_symbol_entry_6.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_6']])
            self.perm_var_value_entry_6.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_6']])
           
            self.perm_var_symbol_entry_7.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_7']])
            self.perm_var_value_entry_7.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_7']])
            
            self.perm_var_symbol_entry_8.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_8']])
            self.perm_var_value_entry_8.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_8']])
            
            self.perm_var_symbol_entry_9.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_9']])
            self.perm_var_value_entry_9.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_9']])
            
            self.perm_var_symbol_entry_10.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_10']])
            self.perm_var_value_entry_10.insert(END, ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_10']])

        conn.commit()
        conn.close()


        if self.ffperm_var_highlight_question_text.get() == 1:
            print("Frage wird MIT Text-Formatierung geladen. --> Fragen-ID: " + str(self.ffperm_load_box.get()))
            test_generator_modul_taxonomie_und_textformatierung.Textformatierung.reallocate_text(self, self.ffperm_question_description_main_entry)

        else:
            print("Frage wird OHNE Text-Formatierung geladen. --> Fragen-ID: " + str(self.ffperm_load_box.get()))

    def ffperm_edit_id_from_db(self):


        conn = sqlite3.connect(self.database_formelfrage_permutation_path)
        c = conn.cursor()
        record_id = self.ffperm_load_box.get()

        # format of duration P0Y0M0DT0H30M0S
        self.ffperm_test_time = "P0Y0M0DT" + self.ffperm_proc_hours_box.get() + "H" + self.ffperm_proc_minutes_box.get() + "M" + self.ffperm_proc_seconds_box.get() + "S"


        if self.ffperm_picture_name != "":
            # read image data in byte format
            with open(self.ffperm_picture_name, 'rb') as image_file:
                self.ffperm_picture_data = image_file.read()


        else:
            self.ffperm_picture_name = ""
            self.ffperm_picture_data = ""

        c.execute("""UPDATE formelfrage_permutation_table SET
            question_difficulty = :question_difficulty,
            question_category = :question_category,
            question_type = :question_type,
    
            question_title = :question_title,
            question_description_title = :question_description_title,
            question_description_main = :question_description_main,
    
            res1_formula = :res1_formula,
            res2_formula = :res2_formula,
            res3_formula = :res3_formula,
            res4_formula = :res4_formula,
            res5_formula = :res5_formula,
            res6_formula = :res6_formula,
            res7_formula = :res7_formula,
            res8_formula = :res8_formula,
            res9_formula = :res9_formula,
            res10_formula = :res10_formula,
             
            var1_name = :var1_name,
            var1_min = :var1_min,
            var1_max = :var1_max,
            var1_prec = :var1_prec,
            var1_divby = :var1_divby,
            var1_unit = :var1_unit,
            
            var2_name = :var2_name,
            var2_min = :var2_min,
            var2_max = :var2_max,
            var2_prec = :var2_prec,
            var2_divby = :var2_divby,
            var2_unit = :var2_unit,
            
            var3_name = :var3_name,
            var3_min = :var3_min,
            var3_max = :var3_max,
            var3_prec = :var3_prec,
            var3_divby = :var3_divby,
            var3_unit = :var3_unit,
    
            var4_name = :var4_name,
            var4_min = :var4_min,
            var4_max = :var4_max,
            var4_prec = :var4_prec,
            var4_divby = :var4_divby,
            var4_unit = :var4_unit,
            
            var5_name = :var5_name,
            var5_min = :var5_min,
            var5_max = :var5_max,
            var5_prec = :var5_prec,
            var5_divby = :var5_divby,
            var5_unit = :var5_unit,
            
            var6_name = :var6_name,
            var6_min = :var6_min,
            var6_max = :var6_max,
            var6_prec = :var6_prec,
            var6_divby = :var6_divby,
            var6_unit = :var6_unit,
            
            var7_name = :var7_name,
            var7_min = :var7_min,
            var7_max = :var7_max,
            var7_prec = :var7_prec,
            var7_divby = :var7_divby,
            var7_unit = :var7_unit,
            
            var8_name = :var8_name,
            var8_min = :var8_min,
            var8_max = :var8_max,
            var8_prec = :var8_prec,
            var8_divby = :var8_divby,
            var8_unit = :var8_unit,
            
            var9_name = :var9_name,
            var9_min = :var9_min,
            var9_max = :var9_max,
            var9_prec = :var9_prec,
            var9_divby = :var9_divby,
            var9_unit = :var9_unit,
            
            var10_name = :var10_name,
            var10_min = :var10_min,
            var10_max = :var10_max,
            var10_prec = :var10_prec,
            var10_divby = :var10_divby,
            var10_unit = :var10_unit,
            
            res1_name = :res1_name,
            res1_min = :res1_min,
            res1_max = :res1_max,
            res1_prec = :res1_prec,
            res1_tol = :res1_tol,
            res1_points = :res1_points,
            res1_unit = :res1_unit,
            
            res2_name = :res2_name,
            res2_min = :res2_min,
            res2_max = :res2_max,
            res2_prec = :res2_prec,
            res2_tol = :res2_tol,
            res2_points = :res2_points,
            res2_unit = :res2_unit,
            
            res3_name = :res3_name,
            res3_min = :res3_min,
            res3_max = :res3_max,
            res3_prec = :res3_prec,
            res3_tol = :res3_tol,
            res3_points = :res3_points,
            res3_unit = :res3_unit,
            
            res4_name = :res4_name,
            res4_min = :res4_min,
            res4_max = :res4_max,
            res4_prec = :res4_prec,
            res4_tol = :res4_tol,
            res4_points = :res4_points,
            res4_unit = :res4_unit,
            
            res5_name = :res5_name,
            res5_min = :res5_min,
            res5_max = :res5_max,
            res5_prec = :res5_prec,
            res5_tol = :res5_tol,
            res5_points = :res5_points,
            res5_unit = :res5_unit,
            
            res6_name = :res6_name,
            res6_min = :res6_min,
            res6_max = :res6_max,
            res6_prec = :res6_prec,
            res6_tol = :res6_tol,
            res6_points = :res6_points,
            res6_unit = :res6_unit,
            
            res7_name = :res7_name,
            res7_min = :res7_min,
            res7_max = :res7_max,
            res7_prec = :res7_prec,
            res7_tol = :res7_tol,
            res7_points = :res7_points,
            res7_unit = :res7_unit,
            
            res8_name = :res8_name,
            res8_min = :res8_min,
            res8_max = :res8_max,
            res8_prec = :res8_prec,
            res8_tol = :res8_tol,
            res8_points = :res8_points,
            res8_unit = :res8_unit,
            
            res9_name = :res9_name,
            res9_min = :res9_min,
            res9_max = :res9_max,
            res9_prec = :res9_prec,
            res9_tol = :res9_tol,
            res9_points = :res9_points,
            res9_unit = :res9_unit,
            
            res10_name = :res10_name,
            res10_min = :res10_min,
            res10_max = :res10_max,
            res10_prec = :res10_prec,
            res10_tol = :res10_tol,
            res10_points = :res10_points,
            res10_unit = :res10_unit,
            
            description_img_name_1 = :description_img_name_1,
            description_img_data_1 = :description_img_data_1,
            description_img_path_1 = :description_img_path_1,
            
            description_img_name_2 = :description_img_name_2,
            description_img_data_2 = :description_img_data_2,
            description_img_path_2 = :description_img_path_2,
            
            description_img_name_3 = :description_img_name_3,
            description_img_data_3 = :description_img_data_3,
            description_img_path_3 = :description_img_path_3,
            
            test_time= :test_time,
            question_pool_tag = :question_pool_tag,
            question_author = :question_author
            
            WHERE oid = :oid""",
                {'question_difficulty': self.ffperm_question_difficulty_entry.get(),
                 'question_category': self.ffperm_question_category_entry.get(),
                 'question_type': self.ffperm_question_type_entry.get(),

                 'question_title': self.ffperm_question_title_entry.get(),
                 'question_description_title': self.ffperm_question_description_title_entry.get(),
                 'question_description_main': self.ffperm_question_description_main_entry.get("1.0", 'end-1c'),

                 'res1_formula': self.perm_res1_formula_entry.get(),
                 'res2_formula': self.perm_res2_formula_entry.get(),
                 'res3_formula': self.perm_res3_formula_entry.get(),
                 'res4_formula': self.perm_res4_formula_entry.get(),
                 'res5_formula': self.perm_res5_formula_entry.get(),
                 'res6_formula': self.perm_res6_formula_entry.get(),
                 'res7_formula': self.perm_res7_formula_entry.get(),
                 'res8_formula': self.perm_res8_formula_entry.get(),
                 'res9_formula': self.perm_res9_formula_entry.get(),
                 'res10_formula': self.perm_res10_formula_entry.get(),

                 'var1_name': self.perm_var1_name_entry.get(),
                 'var1_min': self.perm_var1_min_entry.get(),
                 'var1_max': self.perm_var1_max_entry.get(),
                 'var1_prec': self.perm_var1_prec_entry.get(),
                 'var1_divby': self.perm_var1_divby_entry.get(),
                 'var1_unit': "",

                 'var2_name': self.perm_var2_name_entry.get(),
                 'var2_min': self.perm_var2_min_entry.get(),
                 'var2_max': self.perm_var2_max_entry.get(),
                 'var2_prec': self.perm_var2_prec_entry.get(),
                 'var2_divby': self.perm_var2_divby_entry.get(),
                 'var2_unit': "",

                 'var3_name': self.perm_var3_name_entry.get(),
                 'var3_min': self.perm_var3_min_entry.get(),
                 'var3_max': self.perm_var3_max_entry.get(),
                 'var3_prec': self.perm_var3_prec_entry.get(),
                 'var3_divby': self.perm_var3_divby_entry.get(),
                 'var3_unit': "",

                 'var4_name': self.perm_var4_name_entry.get(),
                 'var4_min': self.perm_var4_min_entry.get(),
                 'var4_max': self.perm_var4_max_entry.get(),
                 'var4_prec': self.perm_var4_prec_entry.get(),
                 'var4_divby': self.perm_var4_divby_entry.get(),
                 'var4_unit': "",

                 'var5_name': self.perm_var5_name_entry.get(),
                 'var5_min': self.perm_var5_min_entry.get(),
                 'var5_max': self.perm_var5_max_entry.get(),
                 'var5_prec': self.perm_var5_prec_entry.get(),
                 'var5_divby': self.perm_var5_divby_entry.get(),
                 'var5_unit': "",

                 'var6_name': self.perm_var6_name_entry.get(),
                 'var6_min': self.perm_var6_min_entry.get(),
                 'var6_max': self.perm_var6_max_entry.get(),
                 'var6_prec': self.perm_var6_prec_entry.get(),
                 'var6_divby': self.perm_var6_divby_entry.get(),
                 'var6_unit': "",

                 'var7_name': self.perm_var7_name_entry.get(),
                 'var7_min': self.perm_var7_min_entry.get(),
                 'var7_max': self.perm_var7_max_entry.get(),
                 'var7_prec': self.perm_var7_prec_entry.get(),
                 'var7_divby': self.perm_var7_divby_entry.get(),
                 'var7_unit': "",

                 'var8_name': self.perm_var8_name_entry.get(),
                 'var8_min': self.perm_var8_min_entry.get(),
                 'var8_max': self.perm_var8_max_entry.get(),
                 'var8_prec': self.perm_var8_prec_entry.get(),
                 'var8_divby': self.perm_var8_divby_entry.get(),
                 'var8_unit': "",

                 'var9_name': self.perm_var9_name_entry.get(),
                 'var9_min': self.perm_var9_min_entry.get(),
                 'var9_max': self.perm_var9_max_entry.get(),
                 'var9_prec': self.perm_var9_prec_entry.get(),
                 'var9_divby': self.perm_var9_divby_entry.get(),
                 'var9_unit': "",

                 'var10_name': self.perm_var10_name_entry.get(),
                 'var10_min': self.perm_var10_min_entry.get(),
                 'var10_max': self.perm_var10_max_entry.get(),
                 'var10_prec': self.perm_var10_prec_entry.get(),
                 'var10_divby': self.perm_var10_divby_entry.get(),
                 'var10_unit': "",

                 'res1_name': self.perm_res1_name_entry.get(),
                 'res1_min': self.perm_res1_min_entry.get(),
                 'res1_max': self.perm_res1_max_entry.get(),
                 'res1_prec': self.perm_res1_prec_entry.get(),
                 'res1_tol': self.perm_res1_tol_entry.get(),
                 'res1_points': self.perm_res1_points_entry.get(),
                 'res1_unit': "",

                 'res2_name': self.perm_res2_name_entry.get(),
                 'res2_min': self.perm_res2_min_entry.get(),
                 'res2_max': self.perm_res2_max_entry.get(),
                 'res2_prec': self.perm_res2_prec_entry.get(),
                 'res2_tol': self.perm_res2_tol_entry.get(),
                 'res2_points': self.perm_res2_points_entry.get(),
                 'res2_unit': "",

                 'res3_name': self.perm_res3_name_entry.get(),
                 'res3_min': self.perm_res3_min_entry.get(),
                 'res3_max': self.perm_res3_max_entry.get(),
                 'res3_prec': self.perm_res3_prec_entry.get(),
                 'res3_tol': self.perm_res3_tol_entry.get(),
                 'res3_points': self.perm_res3_points_entry.get(),
                 'res3_unit': "",

                 'res4_name': self.perm_res4_name_entry.get(),
                 'res4_min': self.perm_res4_min_entry.get(),
                 'res4_max': self.perm_res4_max_entry.get(),
                 'res4_prec': self.perm_res4_prec_entry.get(),
                 'res4_tol': self.perm_res4_tol_entry.get(),
                 'res4_points': self.perm_res4_points_entry.get(),
                 'res4_unit': "",

                 'res5_name': self.perm_res5_name_entry.get(),
                 'res5_min': self.perm_res5_min_entry.get(),
                 'res5_max': self.perm_res5_max_entry.get(),
                 'res5_prec': self.perm_res5_prec_entry.get(),
                 'res5_tol': self.perm_res5_tol_entry.get(),
                 'res5_points': self.perm_res5_points_entry.get(),
                 'res5_unit': "",

                 'res6_name': self.perm_res6_name_entry.get(),
                 'res6_min': self.perm_res6_min_entry.get(),
                 'res6_max': self.perm_res6_max_entry.get(),
                 'res6_prec': self.perm_res6_prec_entry.get(),
                 'res6_tol': self.perm_res6_tol_entry.get(),
                 'res6_points': self.perm_res6_points_entry.get(),
                 'res6_unit': "",

                 'res7_name': self.perm_res7_name_entry.get(),
                 'res7_min': self.perm_res7_min_entry.get(),
                 'res7_max': self.perm_res7_max_entry.get(),
                 'res7_prec': self.perm_res7_prec_entry.get(),
                 'res7_tol': self.perm_res7_tol_entry.get(),
                 'res7_points': self.perm_res7_points_entry.get(),
                 'res7_unit': "",

                 'res8_name': self.perm_res8_name_entry.get(),
                 'res8_min': self.perm_res8_min_entry.get(),
                 'res8_max': self.perm_res8_max_entry.get(),
                 'res8_prec': self.perm_res8_prec_entry.get(),
                 'res8_tol': self.perm_res8_tol_entry.get(),
                 'res8_points': self.perm_res8_points_entry.get(),
                 'res8_unit': "",

                 'res9_name': self.perm_res9_name_entry.get(),
                 'res9_min': self.perm_res9_min_entry.get(),
                 'res9_max': self.perm_res9_max_entry.get(),
                 'res9_prec': self.perm_res9_prec_entry.get(),
                 'res9_tol': self.perm_res9_tol_entry.get(),
                 'res9_points': self.perm_res9_points_entry.get(),
                 'res9_unit': "",

                 'res10_name': self.perm_res10_name_entry.get(),
                 'res10_min': self.perm_res10_min_entry.get(),
                 'res10_max': self.perm_res10_max_entry.get(),
                 'res10_prec': self.perm_res10_prec_entry.get(),
                 'res10_tol': self.perm_res10_tol_entry.get(),
                 'res10_points': self.perm_res10_points_entry.get(),
                 'res10_unit': "",

                 'description_img_name_1': self.ffperm_description_img_name_1,
                 'description_img_data_1': self.ffperm_description_img_data_1,
                 'description_img_path_1': self.ffperm_description_img_path_1,

                 'description_img_name_2': self.ffperm_description_img_name_2,
                 'description_img_data_2': self.ffperm_description_img_data_2,
                 'description_img_path_2': self.ffperm_description_img_path_2,

                 'description_img_name_3': self.ffperm_description_img_name_3,
                 'description_img_data_3': self.ffperm_description_img_data_3,
                 'description_img_path_3': self.ffperm_description_img_path_3,

                 'test_time': self.ffperm_test_time,
                 'question_pool_tag': self.ffperm_question_pool_tag_entry.get(),
                 'question_author': self.ffperm_question_author_entry.get(),
                 'oid': record_id
                 })

        conn.commit()
        conn.close()

        print("Frage mit ID: '" + record_id + "' editiert")

    def ffperm_delete_id_from_db(self):

        self.ffperm_delete_box_id = ""
        self.ffperm_delete_box_id = self.ffperm_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.ffperm_delete_box_id, "formelfrage_permutation", self.ffperm_var_delete_all.get(), self.project_root_path, self.ffperm_db_entry_to_index_dict, self.database_formelfrage_permutation_path, "formelfrage_permutation_table", "formelfrage_permutation_DB_export_file.xlsx", "FF_Permutation - Database")
      

    def ffperm_clear_GUI(self):
        self.ffperm_question_difficulty_entry.delete(0, END)
        self.ffperm_question_category_entry.delete(0, END)
        self.ffperm_question_type_entry.delete(0, END)

        self.ffperm_question_title_entry.delete(0, END)
        self.ffperm_question_description_title_entry.delete(0, END)
        self.ffperm_question_description_main_entry.delete('1.0', 'end-1c')

        self.perm_res1_formula_entry.delete(0, END)
        self.perm_res2_formula_entry.delete(0, END)
        self.perm_res3_formula_entry.delete(0, END)
        self.perm_res4_formula_entry.delete(0, END)
        self.perm_res5_formula_entry.delete(0, END)
        self.perm_res6_formula_entry.delete(0, END)
        self.perm_res7_formula_entry.delete(0, END)
        self.perm_res8_formula_entry.delete(0, END)
        self.perm_res9_formula_entry.delete(0, END)
        self.perm_res10_formula_entry.delete(0, END)

        self.perm_var1_name_entry.delete(0, END)
        self.perm_var1_min_entry.delete(0, END)
        self.perm_var1_max_entry.delete(0, END)
        self.perm_var1_prec_entry.delete(0, END)
        self.perm_var1_divby_entry.delete(0, END)

        self.perm_var2_name_entry.delete(0, END)
        self.perm_var2_min_entry.delete(0, END)
        self.perm_var2_max_entry.delete(0, END)
        self.perm_var2_prec_entry.delete(0, END)
        self.perm_var2_divby_entry.delete(0, END)

        self.perm_var3_name_entry.delete(0, END)
        self.perm_var3_min_entry.delete(0, END)
        self.perm_var3_max_entry.delete(0, END)
        self.perm_var3_prec_entry.delete(0, END)
        self.perm_var3_divby_entry.delete(0, END)

        self.perm_var4_name_entry.delete(0, END)
        self.perm_var4_min_entry.delete(0, END)
        self.perm_var4_max_entry.delete(0, END)
        self.perm_var4_prec_entry.delete(0, END)
        self.perm_var4_divby_entry.delete(0, END)

        self.perm_var5_name_entry.delete(0, END)
        self.perm_var5_min_entry.delete(0, END)
        self.perm_var5_max_entry.delete(0, END)
        self.perm_var5_prec_entry.delete(0, END)
        self.perm_var5_divby_entry.delete(0, END)

        self.perm_var6_name_entry.delete(0, END)
        self.perm_var6_min_entry.delete(0, END)
        self.perm_var6_max_entry.delete(0, END)
        self.perm_var6_prec_entry.delete(0, END)
        self.perm_var6_divby_entry.delete(0, END)

        self.perm_var7_name_entry.delete(0, END)
        self.perm_var7_min_entry.delete(0, END)
        self.perm_var7_max_entry.delete(0, END)
        self.perm_var7_prec_entry.delete(0, END)
        self.perm_var7_divby_entry.delete(0, END)

        self.perm_var8_name_entry.delete(0, END)
        self.perm_var8_min_entry.delete(0, END)
        self.perm_var8_max_entry.delete(0, END)
        self.perm_var8_prec_entry.delete(0, END)
        self.perm_var8_divby_entry.delete(0, END)

        self.perm_var9_name_entry.delete(0, END)
        self.perm_var9_min_entry.delete(0, END)
        self.perm_var9_max_entry.delete(0, END)
        self.perm_var9_prec_entry.delete(0, END)
        self.perm_var9_divby_entry.delete(0, END)

        self.perm_var10_name_entry.delete(0, END)
        self.perm_var10_min_entry.delete(0, END)
        self.perm_var10_max_entry.delete(0, END)
        self.perm_var10_prec_entry.delete(0, END)
        self.perm_var10_divby_entry.delete(0, END)

        self.perm_res1_name_entry.delete(0, END)
        self.perm_res1_min_entry.delete(0, END)
        self.perm_res1_max_entry.delete(0, END)
        self.perm_res1_prec_entry.delete(0, END)
        self.perm_res1_tol_entry.delete(0, END)
        self.perm_res1_points_entry.delete(0, END)

        self.perm_res2_name_entry.delete(0, END)
        self.perm_res2_min_entry.delete(0, END)
        self.perm_res2_max_entry.delete(0, END)
        self.perm_res2_prec_entry.delete(0, END)
        self.perm_res2_tol_entry.delete(0, END)
        self.perm_res2_points_entry.delete(0, END)

        self.perm_res3_name_entry.delete(0, END)
        self.perm_res3_min_entry.delete(0, END)
        self.perm_res3_max_entry.delete(0, END)
        self.perm_res3_prec_entry.delete(0, END)
        self.perm_res3_tol_entry.delete(0, END)
        self.perm_res3_points_entry.delete(0, END)

        self.perm_res4_name_entry.delete(0, END)
        self.perm_res4_min_entry.delete(0, END)
        self.perm_res4_max_entry.delete(0, END)
        self.perm_res4_prec_entry.delete(0, END)
        self.perm_res4_tol_entry.delete(0, END)
        self.perm_res4_points_entry.delete(0, END)

        self.perm_res5_name_entry.delete(0, END)
        self.perm_res5_min_entry.delete(0, END)
        self.perm_res5_max_entry.delete(0, END)
        self.perm_res5_prec_entry.delete(0, END)
        self.perm_res5_tol_entry.delete(0, END)
        self.perm_res5_points_entry.delete(0, END)

        self.perm_res6_name_entry.delete(0, END)
        self.perm_res6_min_entry.delete(0, END)
        self.perm_res6_max_entry.delete(0, END)
        self.perm_res6_prec_entry.delete(0, END)
        self.perm_res6_tol_entry.delete(0, END)
        self.perm_res6_points_entry.delete(0, END)

        self.perm_res7_name_entry.delete(0, END)
        self.perm_res7_min_entry.delete(0, END)
        self.perm_res7_max_entry.delete(0, END)
        self.perm_res7_prec_entry.delete(0, END)
        self.perm_res7_tol_entry.delete(0, END)
        self.perm_res7_points_entry.delete(0, END)

        self.perm_res8_name_entry.delete(0, END)
        self.perm_res8_min_entry.delete(0, END)
        self.perm_res8_max_entry.delete(0, END)
        self.perm_res8_prec_entry.delete(0, END)
        self.perm_res8_tol_entry.delete(0, END)
        self.perm_res8_points_entry.delete(0, END)

        self.perm_res9_name_entry.delete(0, END)
        self.perm_res9_min_entry.delete(0, END)
        self.perm_res9_max_entry.delete(0, END)
        self.perm_res9_prec_entry.delete(0, END)
        self.perm_res9_tol_entry.delete(0, END)
        self.perm_res9_points_entry.delete(0, END)

        self.perm_res10_name_entry.delete(0, END)
        self.perm_res10_min_entry.delete(0, END)
        self.perm_res10_max_entry.delete(0, END)
        self.perm_res10_prec_entry.delete(0, END)
        self.perm_res10_tol_entry.delete(0, END)
        self.perm_res10_points_entry.delete(0, END)


        
        self.perm_var_symbol_entry_1.delete(0, END)
        self.perm_var_value_entry_1.delete(0, END)
      
        self.perm_var_symbol_entry_2.delete(0, END)
        self.perm_var_value_entry_2.delete(0, END)

        self.perm_var_symbol_entry_3.delete(0, END)
        self.perm_var_value_entry_3.delete(0, END)
      
        self.perm_var_symbol_entry_4.delete(0, END)
        self.perm_var_value_entry_4.delete(0, END)
       
        self.perm_var_symbol_entry_5.delete(0, END)
        self.perm_var_value_entry_5.delete(0, END)
    
        self.perm_var_symbol_entry_6.delete(0, END)
        self.perm_var_value_entry_6.delete(0, END)
       
        self.perm_var_symbol_entry_7.delete(0, END)
        self.perm_var_value_entry_7.delete(0, END)
     
        self.perm_var_symbol_entry_8.delete(0, END)
        self.perm_var_value_entry_8.delete(0, END)
       
        self.perm_var_symbol_entry_9.delete(0, END)
        self.perm_var_value_entry_9.delete(0, END)
     
        self.perm_var_symbol_entry_10.delete(0, END)
        self.perm_var_value_entry_10.delete(0, END)

class Create_formelfrage_permutation_Questions(Formelfrage_Permutation):


    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):

        self.ffperm_db_entry_to_index_dict = db_entry_to_index_dict
        self.ffperm_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path
        self.formelfrage_permutation_pool_qpl_file_path_output = xml_qpl_output_file_path
        self.ffperm_mytree = ET.parse(xml_read_qti_template_path)
        self.ffperm_myroot = self.ffperm_mytree.getroot()
        self.ffperm_question_type_test_or_pool = question_type
        self.formelfrage_permutation_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)

        self.all_entries_from_db_list = []
        self.number_of_entrys = []

        self.question_pool_id_list = []
        self.question_title_list = []

        self.ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.ffperm_file_max_id = max_id
        self.taxonomy_file_question_pool = taxonomy_file_question_pool
        self.ilias_id_pool_qti_xml = max_id_pool_qti_xml


        print("\n")


        if self.ffperm_question_type_test_or_pool == "question_test":
            print("FORMELFRAGE_PERM: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("FORMELFRAGE_PERM: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))


        # Mit ffperm_Datenbank verknüpfen
        connect_ffperm_db = sqlite3.connect(self.database_formelfrage_permutation_path)
        cursor = connect_ffperm_db.cursor()


        # Prüfen ob alle EInträge generiert werden sollen (checkbox gesetzt)
        if self.ffperm_var_create_question_pool_all_check.get() == 1:
            conn = sqlite3.connect(self.database_formelfrage_permutation_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM formelfrage_permutation_table")

            ffperm_db_records = c.fetchall()

            for ffperm_db_record in ffperm_db_records:
                self.all_entries_from_db_list.append(int(ffperm_db_record[len(ffperm_db_record) - 1]))

            self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
            self.ffperm_test_entry_splitted = self.string_temp.split(",")

            # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
            self.ffperm_test_entry_splitted.pop(0)


        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM formelfrage_permutation_table")
        ffperm_db_records = cursor.fetchall()

        for i in range(len(self.ffperm_test_entry_splitted)):
            for ffperm_db_record in ffperm_db_records:
                if str(ffperm_db_record[len(ffperm_db_record) - 1]) == self.ffperm_test_entry_splitted[i]:
                    for t in range(len(ffperm_db_record)):
                        if ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_type']].lower() == "formelfrage_perm" or ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_type']].lower() == "formel frage_perm":
                            self.ffperm_question_difficulty                                                = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_difficulty']]
                            self.ffperm_question_category                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_category']]
                            self.ffperm_question_type                                                      = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_type']]
                            self.ffperm_question_title                                                     = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.ffperm_question_description_title                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.ffperm_question_description_main                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_description_main']]
                            self.ffperm_res1_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_formula']]
                            self.ffperm_res2_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_formula']]
                            self.ffperm_res3_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_formula']]
                            self.ffperm_res4_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_formula']]
                            self.ffperm_res5_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_formula']]
                            self.ffperm_res6_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_formula']]
                            self.ffperm_res7_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_formula']]
                            self.ffperm_res8_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_formula']]
                            self.ffperm_res9_formula                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_formula']]
                            self.ffperm_res10_formula                                                      = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_formula']]

                            self.ffperm_var1_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_name']]
                            self.ffperm_var1_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_min']]
                            self.ffperm_var1_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_max']]
                            self.ffperm_var1_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_prec']]
                            self.ffperm_var1_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_divby']]
                            self.ffperm_var1_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var1_unit']]

                            self.ffperm_var2_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_name']]
                            self.ffperm_var2_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_min']]
                            self.ffperm_var2_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_max']]
                            self.ffperm_var2_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_prec']]
                            self.ffperm_var2_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_divby']]
                            self.ffperm_var2_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var2_unit']]

                            self.ffperm_var3_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_name']]
                            self.ffperm_var3_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_min']]
                            self.ffperm_var3_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_max']]
                            self.ffperm_var3_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_prec']]
                            self.ffperm_var3_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_divby']]
                            self.ffperm_var3_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var3_unit']]

                            self.ffperm_var4_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_name']]
                            self.ffperm_var4_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_min']]
                            self.ffperm_var4_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_max']]
                            self.ffperm_var4_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_prec']]
                            self.ffperm_var4_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_divby']]
                            self.ffperm_var4_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var4_unit']]

                            self.ffperm_var5_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_name']]
                            self.ffperm_var5_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_min']]
                            self.ffperm_var5_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_max']]
                            self.ffperm_var5_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_prec']]
                            self.ffperm_var5_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_divby']]
                            self.ffperm_var5_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var5_unit']]

                            self.ffperm_var6_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_name']]
                            self.ffperm_var6_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_min']]
                            self.ffperm_var6_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_max']]
                            self.ffperm_var6_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_prec']]
                            self.ffperm_var6_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_divby']]
                            self.ffperm_var6_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var6_unit']]

                            self.ffperm_var7_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_name']]
                            self.ffperm_var7_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_min']]
                            self.ffperm_var7_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_max']]
                            self.ffperm_var7_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_prec']]
                            self.ffperm_var7_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_divby']]
                            self.ffperm_var7_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var7_unit']]

                            self.ffperm_var8_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_name']]
                            self.ffperm_var8_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_min']]
                            self.ffperm_var8_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_max']]
                            self.ffperm_var8_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_prec']]
                            self.ffperm_var8_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_divby']]
                            self.ffperm_var8_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var8_unit']]

                            self.ffperm_var9_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_name']]
                            self.ffperm_var9_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_min']]
                            self.ffperm_var9_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_max']]
                            self.ffperm_var9_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_prec']]
                            self.ffperm_var9_divby                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_divby']]
                            self.ffperm_var9_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var9_unit']]

                            self.ffperm_var10_name                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_name']]
                            self.ffperm_var10_min                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_min']]
                            self.ffperm_var10_max                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_max']]
                            self.ffperm_var10_prec                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_prec']]
                            self.ffperm_var10_divby                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_divby']]
                            self.ffperm_var10_unit                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var10_unit']]

                            self.ffperm_res1_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_name']]
                            self.ffperm_res1_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_min']]
                            self.ffperm_res1_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_max']]
                            self.ffperm_res1_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_prec']]
                            self.ffperm_res1_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_tol']]
                            self.ffperm_res1_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_points']]
                            self.ffperm_res1_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res1_unit']]

                            self.ffperm_res2_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_name']]
                            self.ffperm_res2_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_min']]
                            self.ffperm_res2_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_max']]
                            self.ffperm_res2_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_prec']]
                            self.ffperm_res2_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_tol']]
                            self.ffperm_res2_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_points']]
                            self.ffperm_res2_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res2_unit']]

                            self.ffperm_res3_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_name']]
                            self.ffperm_res3_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_min']]
                            self.ffperm_res3_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_max']]
                            self.ffperm_res3_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_prec']]
                            self.ffperm_res3_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_tol']]
                            self.ffperm_res3_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_points']]
                            self.ffperm_res3_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res3_unit']]

                            self.ffperm_res4_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_name']]
                            self.ffperm_res4_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_min']]
                            self.ffperm_res4_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_max']]
                            self.ffperm_res4_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_prec']]
                            self.ffperm_res4_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_tol']]
                            self.ffperm_res4_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_points']]
                            self.ffperm_res4_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res4_unit']]

                            self.ffperm_res5_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_name']]
                            self.ffperm_res5_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_min']]
                            self.ffperm_res5_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_max']]
                            self.ffperm_res5_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_prec']]
                            self.ffperm_res5_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_tol']]
                            self.ffperm_res5_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_points']]
                            self.ffperm_res5_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res5_unit']]

                            self.ffperm_res6_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_name']]
                            self.ffperm_res6_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_min']]
                            self.ffperm_res6_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_max']]
                            self.ffperm_res6_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_prec']]
                            self.ffperm_res6_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_tol']]
                            self.ffperm_res6_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_points']]
                            self.ffperm_res6_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res6_unit']]

                            self.ffperm_res7_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_name']]
                            self.ffperm_res7_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_min']]
                            self.ffperm_res7_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_max']]
                            self.ffperm_res7_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_prec']]
                            self.ffperm_res7_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_tol']]
                            self.ffperm_res7_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_points']]
                            self.ffperm_res7_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res7_unit']]

                            self.ffperm_res8_name                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_name']]
                            self.ffperm_res8_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_min']]
                            self.ffperm_res8_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_max']]
                            self.ffperm_res8_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_prec']]
                            self.ffperm_res8_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_tol']]
                            self.ffperm_res8_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_points']]
                            self.ffperm_res8_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res8_unit']]

                            self.ffperm_res9_name                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_name']]
                            self.ffperm_res9_min                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_min']]
                            self.ffperm_res9_max                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_max']]
                            self.ffperm_res9_prec                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_prec']]
                            self.ffperm_res9_tol                                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_tol']]
                            self.ffperm_res9_points                                                        = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_points']]
                            self.ffperm_res9_unit                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res9_unit']]

                            self.ffperm_res10_name                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_name']]
                            self.ffperm_res10_min                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_min']]
                            self.ffperm_res10_max                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_max']]
                            self.ffperm_res10_prec                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_prec']]
                            self.ffperm_res10_tol                                                          = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_tol']]
                            self.ffperm_res10_points                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_points']]
                            self.ffperm_res10_unit                                                         = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res10_unit']]


                            self.ff_perm_var_symbol_1                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_1']]
                            self.ff_perm_var_value_1                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_1']]

                            self.ff_perm_var_symbol_2                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_2']]
                            self.ff_perm_var_value_2                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_2']]

                            self.ff_perm_var_symbol_3                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_3']]
                            self.ff_perm_var_value_3                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_3']]

                            self.ff_perm_var_symbol_4                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_4']]
                            self.ff_perm_var_value_4                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_4']]

                            self.ff_perm_var_symbol_5                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_5']]
                            self.ff_perm_var_value_5                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_5']]

                            self.ff_perm_var_symbol_6                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_6']]
                            self.ff_perm_var_value_6                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_6']]

                            self.ff_perm_var_symbol_7                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_7']]
                            self.ff_perm_var_value_7                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_7']]

                            self.ff_perm_var_symbol_8                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_8']]
                            self.ff_perm_var_value_8                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_8']]

                            self.ff_perm_var_symbol_9                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_9']]
                            self.ff_perm_var_value_9                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_9']]

                            self.ff_perm_var_symbol_10                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_symbol_10']]
                            self.ff_perm_var_value_10                                                   = ffperm_db_record[self.ffperm_db_entry_to_index_dict['perm_var_value_10']]

                            self.ffperm_description_img_name_1	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_name_1']]
                            self.ffperm_description_img_data_1	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_data_1']]
                            self.ffperm_description_img_path_1	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_path_1']]
                            self.ffperm_description_img_name_2	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_name_2']]
                            self.ffperm_description_img_data_2	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_data_2']]
                            self.ffperm_description_img_path_2	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_path_2']]
                            self.ffperm_description_img_name_3	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_name_3']]
                            self.ffperm_description_img_data_3	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_data_3']]
                            self.ffperm_description_img_path_3	                                           = ffperm_db_record[self.ffperm_db_entry_to_index_dict['description_img_path_3']]

                            self.ffperm_test_time	                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['test_time']]
                            self.ffperm_var_number	                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['var_number']]
                            self.ffperm_res_number	                                                       = ffperm_db_record[self.ffperm_db_entry_to_index_dict['res_number']]
                            self.ffperm_question_pool_tag                                                  = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_pool_tag']]
                            self.ffperm_question_author                                                    = ffperm_db_record[self.ffperm_db_entry_to_index_dict['question_author']].replace('&', "&amp;")


            Create_formelfrage_permutation_Questions.ffperm_question_structure(self, i)

    def ffperm_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""





        # VARIABLEN
        self.ffperm_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1

        self.ffperm_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.ffperm_var_use_latex_on_text_check.get(), self.ffperm_question_description_main)

        ############# PERMUTATION_VALUES

        #_x1 = [1,3,2]
        #_x2 = ["u", "m", "k"]
        #_x3 = ["10^-6", "10^-3", "1000"]self.ff_perm_var_name_1

        self.exponential_to_number_dict = {
            "10^-30": "0.000000000000000000000000000001",
            "10^-29": "0.00000000000000000000000000001",
            "10^-28": "0.0000000000000000000000000001",
            "10^-27": "0.000000000000000000000000001",
            "10^-26": "0.00000000000000000000000001",
            "10^-25": "0.0000000000000000000000001",
            "10^-24": "0.000000000000000000000001",
            "10^-23": "0.00000000000000000000001",
            "10^-22": "0.0000000000000000000001",
            "10^-21": "0.000000000000000000001",
            "10^-20": "0.00000000000000000001",
            "10^-19": "0.0000000000000000001",
            "10^-18": "0.000000000000000001",
            "10^-17": "0.00000000000000001",
            "10^-16": "0.0000000000000001",
            "10^-15": "0.000000000000001",
            "10^-14": "0.00000000000001",
            "10^-13": "0.0000000000001",
            "10^-12": "0.000000000001",
            "10^-11": "0.00000000001",
            "10^-10": "0.0000000001",
            "10^-9": "0.000000001",
            "10^-8": "0.00000001",
            "10^-7": "0.0000001",
            "10^-6": "0.000001",
            "10^-5": "0.00001",
            "10^-4": "0.0001",
            "10^-3": "0.001",
            "10^-2": "0.01",
            "10^-1": "0.1",
            "10^1": "10",
            "10^2": "100",
            "10^3": "1000",
            "10^4": "10000",
            "10^5": "100000",
            "10^6": "1000000",
            "10^7": "10000000",
            "10^8": "100000000",
            "10^9": "1000000000",
            "10^10": "10000000000",
            "10^11": "100000000000",
            "10^12": "1000000000000",
            "10^13": "10000000000000",
            "10^14": "100000000000000",
            "10^15": "1000000000000000",
            "10^16": "10000000000000000",
            "10^17": "100000000000000000",
            "10^18": "1000000000000000000",
            "10^19": "10000000000000000000",
            "10^20": "100000000000000000000",
            "10^21": "1000000000000000000000",
            "10^22": "10000000000000000000000",
            "10^23": "100000000000000000000000",
            "10^24": "1000000000000000000000000",
            "10^25": "10000000000000000000000000",
            "10^26": "100000000000000000000000000",
            "10^27": "1000000000000000000000000000",
            "10^28": "10000000000000000000000000000",
            "10^29": "100000000000000000000000000000",
            "10^30": "1000000000000000000000000000000",
        }
        self.set_precision_from_negative_exponential_dict={
            "10^-30": "30",
            "10^-29": "29",
            "10^-28": "28",
            "10^-27": "27",
            "10^-26": "26",
            "10^-25": "25",
            "10^-24": "24",
            "10^-23": "23",
            "10^-22": "22",
            "10^-21": "21",
            "10^-20": "20",
            "10^-19": "19",
            "10^-18": "18",
            "10^-17": "17",
            "10^-16": "16",
            "10^-15": "15",
            "10^-14": "14",
            "10^-13": "13",
            "10^-12": "12",
            "10^-11": "11",
            "10^-10": "10",
            "10^-9": "9",
            "10^-8": "8",
            "10^-7": "7",
            "10^-6": "6",
            "10^-5": "5",
            "10^-4": "4",
            "10^-3": "3",
            "10^-2": "2",
            "10^-1": "1",

        }




        # Permutation Variablen initialisieren
        self.perm_symbol_sammlung = ""
        self.ffperm_var1_min_replaced, self.ffperm_var1_max_replaced, self.ffperm_var1_prec_replaced = "", "", ""
        self.ffperm_var2_min_replaced, self.ffperm_var2_max_replaced, self.ffperm_var2_prec_replaced = "", "", ""
        self.ffperm_var3_min_replaced, self.ffperm_var3_max_replaced, self.ffperm_var3_prec_replaced = "", "", ""
        self.ffperm_var4_min_replaced, self.ffperm_var4_max_replaced, self.ffperm_var4_prec_replaced = "", "", ""
        self.ffperm_var5_min_replaced, self.ffperm_var5_max_replaced, self.ffperm_var5_prec_replaced = "", "", ""
        
        self.ffperm_res1_min_replaced, self.ffperm_res1_max_replaced, self.ffperm_res1_prec_replaced = "", "", ""
        self.ffperm_res2_min_replaced, self.ffperm_res2_max_replaced, self.ffperm_res2_prec_replaced = "", "", ""


        # Die Eingabe der WErte von Permutation (kommagetrennt): z.B: "u,m,k" (für Einheiten im Text)
        perm_var_symbol_1, perm_var_value_1 =  self.ff_perm_var_symbol_1, self.ff_perm_var_value_1.split(',')
        perm_var_symbol_2, perm_var_value_2 =  self.ff_perm_var_symbol_2, self.ff_perm_var_value_2.split(',')
        perm_var_symbol_3, perm_var_value_3 =  self.ff_perm_var_symbol_3, self.ff_perm_var_value_3.split(',')
        perm_var_symbol_4, perm_var_value_4 =  self.ff_perm_var_symbol_4, self.ff_perm_var_value_4.split(',')
        perm_var_symbol_5, perm_var_value_5 =  self.ff_perm_var_symbol_5, self.ff_perm_var_value_5.split(',')


        # Hier wird das Permutation Symbol mit Permutation-Werten verknüpft
        self.perm_symbol_to_values_dict = {
            perm_var_symbol_1: perm_var_value_1,
            perm_var_symbol_2: perm_var_value_2,
            perm_var_symbol_3: perm_var_value_3,
            perm_var_symbol_4: perm_var_value_4,
            perm_var_symbol_5: perm_var_value_5
        }


        # Permutations-Symbole auslesen/sammeln
        self.perm_symbol_sammlung = [perm_var_symbol_1, perm_var_symbol_2, perm_var_symbol_3, perm_var_symbol_4, perm_var_symbol_5]

        # Alle Min/Max Werte auslesen
        self.var_res_min_max_sammlung = [self.ffperm_var1_min, self.ffperm_var1_max, self.ffperm_res1_min, self.ffperm_res1_max,
                                          self.ffperm_var2_min, self.ffperm_var2_max, self.ffperm_res2_min, self.ffperm_res2_max,
                                          self.ffperm_var3_min, self.ffperm_var3_max, self.ffperm_res3_min, self.ffperm_res3_max,
                                          self.ffperm_var4_min, self.ffperm_var4_max, self.ffperm_res4_min, self.ffperm_res4_max,
                                          self.ffperm_var5_min, self.ffperm_var5_max, self.ffperm_res5_min, self.ffperm_res5_max,
                                          ]

        self.var_res_min_max_sammlung_dict = {
            "ffperm_var1_min": 0, "ffperm_var1_max": 1, "ffperm_res1_min": 2, "ffperm_res1_max": 3,
            "ffperm_var2_min": 4, "ffperm_var2_max": 5, "ffperm_res2_min": 6, "ffperm_res2_max": 7,
            "ffperm_var3_min": 8, "ffperm_var3_max": 9, "ffperm_res3_min": 10, "ffperm_res3_max": 11,
            "ffperm_var4_min": 12, "ffperm_var4_max": 13, "ffperm_res4_min": 14, "ffperm_res4_max": 15,
            "ffperm_var5_min": 16, "ffperm_var5_max": 17, "ffperm_res5_min": 18, "ffperm_res5_max": 19

        }

        #print("??????????????????????????????")

        #print(self.perm_symbol_sammlung)
        #print("??????????????????????????????")
        #def perm_var_in_range(perm_var_min, perm_var_max, perm_symbol_sammlung):
        #    # 10*10^-6
        #    if "*" in str(perm_var_min):



        # _x2 = self.perm_var_value_entry_2.get()
        # _x3 = self.perm_var_value_entry_3.get()
        # _x4 = self.perm_var_value_entry_4.get()
        # _x5 = self.perm_var_value_entry_5.get()
        # _x6 = self.perm_var_value_entry_6.get()
        # _x7 = self.perm_var_value_entry_7.get()
        # _x8 = self.perm_var_value_entry_8.get()
        # _x9 = self.perm_var_value_entry_9.get()
        # _x10 = self.perm_var_value_entry_10.get()
        _index = 0


        ####################################
        # Verbindung zur FF-Datenank
        ffperm_connect = sqlite3.connect(self.database_formelfrage_permutation_path)
        ffperm_cursor = ffperm_connect.cursor()

        # Alle Einträge auslesen
        ffperm_cursor.execute("SELECT *, oid FROM formelfrage_permutation_table")
        ffperm_db_records = ffperm_cursor.fetchall()



        for ffperm_db_record in ffperm_db_records:

            # Hier werden die Fragen anhand der ID's erstellt
            if str(ffperm_db_record[len(ffperm_db_record)-1]) == self.ffperm_test_entry_splitted[id_nr]:
                # Permutation immer Aktiv

                ##########################
                print("Permutation aktiv!")
                print('''''''''''''''''''''''''''''''')
                print("\n")

                for k in range(len(perm_var_value_1)):
                    # Hier wird die perm_variable_1 durch einen Wert ersetzt. Z.B.: $x1=[1,3,2]  ..gegeben ist die Spannung U$x1 --> U1, U3, U2
                    self.ffperm_question_description_main_permutation = self.ffperm_question_description_main.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))

                    # Hier wird die perm_variable_2 durch einen Wert ersetzt. Z.B.: $x2=[µ,m,k] ..gegeben sind die Widerstände R1=10, R2=20, R3=30 --> R1=10µ, R2=20, R3=30  ;  R1=10, R2=20m, R3=30  ;  R1=10, R2=20, R3=30k
                    #self.ffperm_question_description_main_permutation = self.ffperm_question_description_main_permutation.replace('$v' + str(perm_var_value_1[k]), '$v' + str(perm_var_value_1[k]) + str(perm_var_value_2[k]))


                    #####
                    # Anpassung der Ranges

                    # Permutationsvariable in Variablen-Ranges suchen und ersetzen
                    for n in range(len(self.perm_symbol_sammlung)):

                        #VAR1 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var1_min):
                            self.ffperm_var1_min_replaced = self.ffperm_var1_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                        else:
                            self.ffperm_var1_min_replaced = self.ffperm_var1_min


                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var1_max):
                            self.ffperm_var1_max_replaced = self.ffperm_var1_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            # Wenn das Symbol in var_max_1 gefunden wurde, welches durch Werte ersetzt werden soll, dann die Werte die eingesetzt werden sollen durchsuchen
                            # Wird der Wert im Dictionary gefunden, dann wird die var1_prec (Präzision) entsprechend gesetzt und die Schleife beendet
                            # 10^-1 -> Präzision: 1, 10^-2 -> Präzision: 2,..., 10^-30 -> Präzision: 30 etc.
                            self.var1_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.var1_prec_temp:
                                    self.ffperm_var1_prec_replaced = self.var1_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_var1_prec_replaced = self.ffperm_var1_prec
                        else:
                            self.ffperm_var1_max_replaced = self.ffperm_var1_max




                        #VAR2 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var2_min):
                            self.ffperm_var2_min_replaced = self.ffperm_var2_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_var2_min_replaced = self.ffperm_var2_min

                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var2_max):
                            self.ffperm_var2_max_replaced = self.ffperm_var2_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.var2_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.var2_prec_temp:
                                    self.ffperm_var2_prec_replaced = self.var2_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_var2_prec_replaced = self.ffperm_var2_prec
                        else:
                            self.ffperm_var2_max_replaced = self.ffperm_var2_max
                        #VAR3 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var3_min):
                            self.ffperm_var3_min_replaced = self.ffperm_var3_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_var3_min_replaced = self.ffperm_var3_min

                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var3_max):
                            self.ffperm_var3_max_replaced = self.ffperm_var3_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.var3_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.var3_prec_temp:
                                    self.ffperm_var3_prec_replaced = self.var3_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_var3_prec_replaced = self.ffperm_var3_prec
                        else:
                            self.ffperm_var3_max_replaced = self.ffperm_var3_max

                        #VAR4 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var4_min):
                            self.ffperm_var4_min_replaced = self.ffperm_var4_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_var4_min_replaced = self.ffperm_var4_min

                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var4_max):
                            self.ffperm_var4_max_replaced = self.ffperm_var4_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.var4_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.var4_prec_temp:
                                    self.ffperm_var4_prec_replaced = self.var4_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_var4_prec_replaced = self.ffperm_var4_prec
                        else:
                            self.ffperm_var4_max_replaced = self.ffperm_var4_max

                        #VAR5 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var5_min):
                            self.ffperm_var5_min_replaced = self.ffperm_var5_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_var5_min_replaced = self.ffperm_var5_min
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_var5_max):
                            self.ffperm_var5_max_replaced = self.ffperm_var5_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.var5_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.var5_prec_temp:
                                    self.ffperm_var5_prec_replaced = self.var5_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_var5_prec_replaced = self.ffperm_var5_prec
                        else:
                            self.ffperm_var5_max_replaced = self.ffperm_var5_max
                        # PERMUTATION SYMBOLE in RESULT ERSETZEN



                        #RES1 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_res1_min):
                            self.ffperm_res1_min_replaced = self.ffperm_res1_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_res1_min_replaced = self.ffperm_res1_min
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_res1_max):
                            self.ffperm_res1_max_replaced = self.ffperm_res1_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.res1_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.res1_prec_temp:
                                    self.ffperm_res1_prec_replaced = self.res1_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_res1_prec_replaced = self.ffperm_res1_prec
                        else:
                            self.ffperm_res1_max_replaced = self.ffperm_res1_max
                        #RES2 - MIN / MAX
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_res2_min):
                            self.ffperm_res2_min_replaced = self.ffperm_res2_min.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])
                        else:
                            self.ffperm_res2_min_replaced = self.ffperm_res2_min
                        if str(self.perm_symbol_sammlung[n]) != "" and str(self.perm_symbol_sammlung[n]) in str(self.ffperm_res2_max):
                            self.ffperm_res2_max_replaced = self.ffperm_res2_max.replace(str(self.perm_symbol_sammlung[n]), self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k])

                            # Anpassung der Präzision (Nachkommastellen)
                            self.res2_prec_temp = self.perm_symbol_to_values_dict[self.perm_symbol_sammlung[n]][k]
                            for key in self.set_precision_from_negative_exponential_dict:
                                if key in self.res2_prec_temp:
                                    self.ffperm_res2_prec_replaced = self.res2_prec_temp.replace(key, self.set_precision_from_negative_exponential_dict[key])
                                    break
                                else:
                                    self.ffperm_res2_prec_replaced = self.ffperm_res2_prec
                        else:
                            self.ffperm_res2_max_replaced = self.ffperm_res2_max


                        # Anpassung der Formel

                        self.ffperm_res1_formula_permutation = self.ffperm_res1_formula.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))
                        #self.ffperm_res1_formula_permutation = self.ffperm_res1_formula_permutation.replace(str(perm_var_symbol_3), str(perm_var_value_3[k]))

                        #self.ffperm_res2_formula_permutation = self.ffperm_res2_formula.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))
                        #self.ffperm_res2_formula_permutation = self.ffperm_res2_formula_permutation.replace(str(perm_var_symbol_3), str(perm_var_value_3[k]))


                        # self.ffperm_res3_formula_permutation = self.ffperm_res3_formula.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))
                        # self.ffperm_res3_formula_permutation = self.ffperm_res3_formula_permutation.replace(str(perm_var_symbol_3), str(perm_var_value_3[k]))
                        #
                        # self.ffperm_res4_formula_permutation = self.ffperm_res4_formula.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))
                        # self.ffperm_res4_formula_permutation = self.ffperm_res4_formula_permutation.replace(str(perm_var_symbol_3), str(perm_var_value_3[k]))
                        #
                        # self.ffperm_res5_formula_permutation = self.ffperm_res5_formula.replace(str(perm_var_symbol_1), str(perm_var_value_1[k]))
                        # self.ffperm_res5_formula_permutation = self.ffperm_res5_formula_permutation.replace(str(perm_var_symbol_3), str(perm_var_value_3[k]))



                        # Formeln in der Berechnung, auf 0 setzen wenn nicht gebraucht
                        # "ID" die permutiert wird, MUSS in der Zeile 1 stehen
                        # U$x1 -> U1, U3, U2  [1,3,2] muss in Perm_zeile 1 definiert werden
                        for m in range(len(perm_var_value_1)):
                            if self.ffperm_res1_formula_permutation != "" and perm_var_value_1[m] != perm_var_value_1[k]:
                                self.ffperm_res1_formula_permutation += " + 0 * $v" + str(perm_var_value_1[m])

                            #if self.ffperm_res2_formula_permutation != "" and perm_var_value_1[m] != perm_var_value_1[k]:
                            #    self.ffperm_res2_formula_permutation += " + 0 * $v" + str(perm_var_value_1[m])

                       # print(self.ffperm_res1_formula_permutation)

                        # Anpassung Fragen-Titel
                        self.ffperm_question_title_replaced = self.ffperm_question_title + " " + str(k+1)





                    # print("====== NACHHER =============")
                    # print(self.ffperm_var1_min_replaced, self.ffperm_var1_max_replaced)
                    # print(self.ffperm_var2_min_replaced, self.ffperm_var2_max_replaced)
                    # print(self.ffperm_var3_min_replaced, self.ffperm_var3_max_replaced)
                    # print(self.ffperm_var4_min_replaced, self.ffperm_var4_max_replaced)
                    # print(self.ffperm_var5_min_replaced, self.ffperm_var5_max_replaced)
                    # print("xxxxxxxxxxxxxxxxxxxxxx")
                    # print(self.ffperm_res1_formula_permutation)
                    # print("xxxxxxxxxxxxxxxxxxxxxx")
                    #
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('$v1', self.ffperm_var1_max_replaced)
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('$v2', self.ffperm_var2_max_replaced)
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('$v3', self.ffperm_var3_max_replaced)
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('$v4', self.ffperm_var4_max_replaced)
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('$v5', self.ffperm_var5_max_replaced)
                    # self.ffperm_res1_formula_permutation_eval = self.ffperm_res1_formula_permutation_eval.replace('^', "**")
                    #
                    # print(self.ffperm_res1_formula_permutation_eval, " -----> ", eval(self.ffperm_res1_formula_permutation_eval)  )
                    # self.ffperm_res1_formula_permutation_eval_result = eval(self.ffperm_res1_formula_permutation_eval)
                    # if "e" in str(self.ffperm_res1_formula_permutation_eval_result):
                    #     self.exp_value = str(self.ffperm_res1_formula_permutation_eval_result).rsplit('e', 1)
                    #     self.exp_value = self.exp_value[1]
                    #     print("EXPONENT FOUND", "  ----> ", self.exp_value)
                    #     self.ffperm_res1_prec_replaced = abs(int(self.exp_value))+1
                    #     print("PREC: ", self.ffperm_res1_prec_replaced)
                    # else:
                    #
                    #     d = decimal.Decimal(str(self.ffperm_res1_formula_permutation_eval_result))
                    #     print(d.as_tuple().exponent,abs(d.as_tuple().exponent) )
                    #     self.ffperm_res1_prec_replaced = abs(d.as_tuple().exponent)



                    test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ffperm_description_img_name_1, self.ffperm_description_img_data_1, id_nr, self.ffperm_question_type_test_or_pool, self.formelfrage_permutation_test_img_file_path, self.formelfrage_permutation_pool_img_file_path)
                    test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ffperm_description_img_name_2, self.ffperm_description_img_data_2, id_nr, self.ffperm_question_type_test_or_pool, self.formelfrage_permutation_test_img_file_path, self.formelfrage_permutation_pool_img_file_path)
                    test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ffperm_description_img_name_3, self.ffperm_description_img_data_3, id_nr, self.ffperm_question_type_test_or_pool, self.formelfrage_permutation_test_img_file_path, self.formelfrage_permutation_pool_img_file_path)





                    r1_rating = "0"
                    r1_unit = ""
                    r1_unitvalue = ""
                    r1_resultunits = ""


                    # Aufbau für  Fragenstruktur "TEST"
                    if self.ffperm_question_type_test_or_pool == "question_test":
                        # XML Struktur aus XML Datei festlegen. Muss nur einmal angelegt werden
                        questestinterop = ET.Element('questestinterop')
                        assessment = ET.SubElement(questestinterop, 'assessment')
                        section = ET.SubElement(assessment, 'section')
                        item = ET.SubElement(section, 'item')

                    # Aufbau für  Fragenstruktur "POOL"
                    else:
                        # XML Struktur aus XML Datei festlegen. Muss nur einmal angelegt werden
                        questestinterop = ET.Element('questestinterop')
                        item = ET.SubElement(questestinterop, 'item')

                        # Zusatz für Taxonomie-Einstellungen

                        self.id_int_numbers = 400000 + id_nr

                        self.number_of_entrys.append(format(self.id_int_numbers, '06d')) #Zahlenfolge muss 6-stellig sein.

                        item.set('ident', "il_0_qst_" + self.number_of_entrys[id_nr])


                        # Hier wird die QPL bearbeitet - Taxonomie
                        self.mytree = ET.parse(self.formelfrage_permutation_pool_qpl_file_path_template)
                        self.myroot = self.mytree.getroot()

                        #self.loop_nr = id_nr+1

                        # Hinzufügen von Question QRef in qpl Datei
                        for i in range(id_nr):
                            ContentObject = ET.Element('ContentObject')
                            MetaData = ET.SubElement(ContentObject, 'MetaData')
                            Settings = ET.SubElement(ContentObject, 'Settings')
                            PageObject = ET.SubElement(ContentObject, 'PageObject')
                            PageContent = ET.SubElement(PageObject, 'PageContent')
                            Question = ET.SubElement(PageContent, 'Question')
                            Question.set('QRef', "il_0_qst_" + self.number_of_entrys[i])
                            QuestionSkillAssignments = ET.SubElement(ContentObject, 'QuestionSkillAssignments')
                            TriggerQuestion = ET.SubElement(QuestionSkillAssignments, 'TriggerQuestion')
                            TriggerQuestion.set('Id', self.number_of_entrys[i])


                            self.myroot.append(PageObject)
                            #self.myroot.append(QuestionSkillAssignments)

                            self.mytree.write(self.formelfrage_permutation_pool_qpl_file_path_output)


                        # Hinzufügen von TriggerQuestion ID in qpl Datei
                        for i in range(id_nr):
                            ContentObject = ET.Element('ContentObject')
                            MetaData = ET.SubElement(ContentObject, 'MetaData')
                            Settings = ET.SubElement(ContentObject, 'Settings')
                            PageObject = ET.SubElement(ContentObject, 'PageObject')
                            PageContent = ET.SubElement(PageObject, 'PageContent')
                            Question = ET.SubElement(PageContent, 'Question')
                            Question.set('QRef', "il_0_qst_" + self.number_of_entrys[i])
                            QuestionSkillAssignments = ET.SubElement(ContentObject, 'QuestionSkillAssignments')
                            TriggerQuestion = ET.SubElement(QuestionSkillAssignments, 'TriggerQuestion')
                            TriggerQuestion.set('Id', self.number_of_entrys[i])

                            self.myroot.append(QuestionSkillAssignments)

                            self.mytree.write(self.formelfrage_permutation_pool_qpl_file_path_output)

                    # Struktur für den Formelfragen - Variableen/Lösungen Teil
                    # Muss für jede Frage neu angelegt/hinzugefügt werden
                    qticomment = ET.SubElement(item, 'qticomment')
                    duration = ET.SubElement(item, 'duration')
                    itemmetadata = ET.SubElement(item, 'itemmetadata')
                    presentation = ET.SubElement(item, 'presentation')

                    flow = ET.SubElement(presentation, 'flow')
                    question_description_material = ET.SubElement(flow, 'material')
                    question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                    qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')


                    ### ------------------------------------------------------- XML Einträge mit Werten füllen
                     # Fragen-Titel -- "item title" in xml
                    item.set('title', self.ffperm_question_title_replaced)

                    # Fragen-Titel Beschreibung
                    qticomment.text = self.ffperm_question_description_title

                    # Testdauer -- "duration" in xml
                    # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                    duration.text = self.ffperm_test_time
                    if duration.text == "":
                        duration.text = "P0Y0M0DT1H0M0S"

                    # -----------------------------------------------------------------------ILIAS VERSION
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "ILIAS_VERSION"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "5.4.10 2020-03-04"
                    # -----------------------------------------------------------------------QUESTIONTYPE
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "QUESTIONTYPE"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "assFormulaQuestion"
                    # -----------------------------------------------------------------------AUTHOR
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "AUTHOR"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = self.ffperm_question_author
                    # -----------------------------------------------------------------------POINTS
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "points"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = str(self.ffperm_res1_points)

                    # Fragentitel einsetzen -- "presentation label" in xml
                    presentation.set('label', self.ffperm_question_title)

                    # Fragen-Text (Format) einsetzen -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                    question_description_mattext.set('texttype', "text/html")

                    # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                    # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten

                    question_description_mattext.text = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_picture_to_description_main(
                                                        self, self.ffperm_description_img_name_1, self.ffperm_description_img_data_1,
                                                        self.ffperm_description_img_name_2, self.ffperm_description_img_data_2,
                                                        self.ffperm_description_img_name_3, self.ffperm_description_img_data_3,
                                                        self.ffperm_question_description_main_permutation, question_description_mattext, question_description_material, id_nr)


                    # ----------------------------------------------------------------------- Variable
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v1", self.ffperm_var1_min_replaced, self.ffperm_var1_max_replaced, self.ffperm_var1_prec, self.ffperm_var1_divby, self.ffperm_var1_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v2", self.ffperm_var2_min_replaced, self.ffperm_var2_max_replaced, self.ffperm_var2_prec, self.ffperm_var2_divby, self.ffperm_var2_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v3", self.ffperm_var3_min_replaced, self.ffperm_var3_max_replaced, self.ffperm_var3_prec, self.ffperm_var3_divby, self.ffperm_var3_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v4", self.ffperm_var4_min_replaced, self.ffperm_var4_max_replaced, self.ffperm_var4_prec, self.ffperm_var4_divby, self.ffperm_var4_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v5", self.ffperm_var5_min_replaced, self.ffperm_var5_max_replaced, self.ffperm_var5_prec, self.ffperm_var5_divby, self.ffperm_var5_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v6", self.ffperm_var6_min, self.ffperm_var6_max, self.ffperm_var6_prec, self.ffperm_var6_divby, self.ffperm_var6_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v7", self.ffperm_var7_min, self.ffperm_var7_max, self.ffperm_var7_prec, self.ffperm_var7_divby, self.ffperm_var7_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v8", self.ffperm_var8_min, self.ffperm_var8_max, self.ffperm_var8_prec, self.ffperm_var8_divby, self.ffperm_var8_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v9", self.ffperm_var9_min, self.ffperm_var9_max, self.ffperm_var9_prec, self.ffperm_var9_divby, self.ffperm_var9_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_variables_structure(self, qtimetadata, "$v10", self.ffperm_var10_min, self.ffperm_var10_max, self.ffperm_var10_prec, self.ffperm_var10_divby, self.ffperm_var10_unit)



                    # ----------------------------------------------------------------------- Solution
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r1", self.ffperm_res1_formula_permutation, self.ffperm_res1_min_replaced, self.ffperm_res1_max_replaced, self.ffperm_res1_prec, self.ffperm_res1_tol, self.ffperm_res1_points, self.ffperm_res1_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r2", self.ffperm_res2_formula, self.ffperm_res2_min, self.ffperm_res2_max, self.ffperm_res2_prec, self.ffperm_res2_tol, self.ffperm_res2_points, self.ffperm_res2_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r3", self.ffperm_res3_formula, self.ffperm_res3_min, self.ffperm_res3_max, self.ffperm_res3_prec, self.ffperm_res3_tol, self.ffperm_res3_points, self.ffperm_res3_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r4", self.ffperm_res4_formula, self.ffperm_res4_min, self.ffperm_res4_max, self.ffperm_res4_prec, self.ffperm_res4_tol, self.ffperm_res4_points, self.ffperm_res4_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r5", self.ffperm_res5_formula, self.ffperm_res5_min, self.ffperm_res5_max, self.ffperm_res5_prec, self.ffperm_res5_tol, self.ffperm_res5_points, self.ffperm_res5_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r6", self.ffperm_res6_formula, self.ffperm_res6_min, self.ffperm_res6_max, self.ffperm_res6_prec, self.ffperm_res6_tol, self.ffperm_res6_points, self.ffperm_res6_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r7", self.ffperm_res7_formula, self.ffperm_res7_min, self.ffperm_res7_max, self.ffperm_res7_prec, self.ffperm_res7_tol, self.ffperm_res7_points, self.ffperm_res7_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r8", self.ffperm_res8_formula, self.ffperm_res8_min, self.ffperm_res8_max, self.ffperm_res8_prec, self.ffperm_res8_tol, self.ffperm_res8_points, self.ffperm_res8_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r9", self.ffperm_res9_formula, self.ffperm_res9_min, self.ffperm_res9_max, self.ffperm_res9_prec, self.ffperm_res9_tol, self.ffperm_res9_points, self.ffperm_res9_unit)
                    Create_formelfrage_permutation_Questions.ffperm_question_results_structure(self, qtimetadata, "$r10", self.ffperm_res10_formula, self.ffperm_res10_min, self.ffperm_res10_max, self.ffperm_res10_prec, self.ffperm_res10_tol, self.ffperm_res10_points, self.ffperm_res10_unit)








                    # -----------------------------------------------------------------------ADDITIONAL_CONT_EDIT_MODE
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "additional_cont_edit_mode"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "default"
                    # -----------------------------------------------------------------------EXTERNAL_ID
                    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                    fieldlabel.text = "externalId"
                    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                    fieldentry.text = "5ea15be69c1e96.43933468"



                    # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                    # Der letzte "Zweig" --> "len(self.ffperm_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                    if self.ffperm_question_type_test_or_pool == "question_test":
                        self.ffperm_myroot[0][len(self.ffperm_myroot[0]) - 1].append(item)

                    # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                    # Die Frage kann einfach angehangen werden
                    else:
                        self.ffperm_myroot.append(item)

                    self.ffperm_mytree.write(self.qti_file_path_output)
                    print("Formelfrage Frage erstellt! --> Titel: " + str(self.ffperm_question_title_replaced))








        ffperm_connect.commit()
        ffperm_connect.close()

        if self.ffperm_question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.formelfrage_permutation_files_path,"ffperm_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.ffperm_file_max_id+1))
            self.mytree.write(self.qpl_file)

    def ffperm_question_variables_structure(self, xml_qtimetadata,  ffperm_var_name, ffperm_var_min, ffperm_var_max, ffperm_var_prec, ffperm_var_divby, ffperm_var_unit):

        self.ffperm_var_name = ffperm_var_name
        self.ffperm_var_min = str(ffperm_var_min)
        self.ffperm_var_min_length = ""
        self.ffperm_var_max = str(ffperm_var_max)
        self.ffperm_var_max_length = ""
        self.ffperm_var_prec = str(ffperm_var_prec)
        self.ffperm_var_divby = str(ffperm_var_divby)
        self.ffperm_var_divby_length = len(str(self.ffperm_var_divby))
        self.ffperm_var_unit = ffperm_var_unit
        self.ffperm_var_unit_length = len(str(self.ffperm_var_unit))

        if self.ffperm_var_min.isdecimal() is False:
            self.ffperm_var_min_length = len(self.ffperm_var_min)


        if self.ffperm_var_max.isdecimal() is False:
            self.ffperm_var_max_length = len(self.ffperm_var_max)



        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = ffperm_var_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

        if self.ffperm_var_unit != "":
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ffperm_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ffperm_var_divby_length) + ":\"" + self.ffperm_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ffperm_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ffperm_var_max + ";" \
                              "s:4:\"unit\";s:" + str(self.ffperm_var_unit_length) + ":\"" + self.ffperm_var_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage_Permutation.unit_table(self, self.ffperm_var_unit))) + ":\"" + Formelfrage_Permutation.unit_table(self, self.ffperm_var_unit) + "\";" \
                              "}"
        elif self.ffperm_var_min.isdecimal() is False and self.ffperm_var_max.isdecimal() is False:
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ffperm_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ffperm_var_divby_length) + ":\"" + self.ffperm_var_divby + "\";" \
                              "s:8:\"rangemin\";s:" + str(self.ffperm_var_min_length) + ":\"" + self.ffperm_var_min + "\";" \
                              "s:8:\"rangemax\";s:" + str(self.ffperm_var_max_length) + ":\"" + self.ffperm_var_max + "\";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "}"
        else:
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ffperm_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ffperm_var_divby_length) + ":\"" + self.ffperm_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ffperm_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ffperm_var_max + ";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "}"

    def ffperm_question_results_structure(self, xml_qtimetadata, ffperm_res_name, ffperm_res_formula, ffperm_res_min, ffperm_res_max, ffperm_res_prec, ffperm_res_tol, ffperm_res_points, ffperm_res_unit):

        self.ffperm_res_name = ffperm_res_name
        self.ffperm_res_formula = ffperm_res_formula
        self.ffperm_res_formula_length = len(str(self.ffperm_res_formula))
        self.ffperm_res_min = str(ffperm_res_min)
        self.ffperm_res_min_length = len(str(self.ffperm_res_min))
        self.ffperm_res_max = str(ffperm_res_max)
        self.ffperm_res_max_length = len(str(self.ffperm_res_max))
        self.ffperm_res_prec = str(ffperm_res_prec)
        self.ffperm_res_tol = str(ffperm_res_tol)
        self.ffperm_res_tol_length = len(str(self.ffperm_res_tol))

        self.ffperm_res_points = str(ffperm_res_points)
        self.ffperm_res_unit = ffperm_res_unit
        self.ffperm_res_unit_length = len(str(self.ffperm_res_unit))




        # s for string length: "9" -> precision = "9" characters
        # rangemin: "i" for negative numbers, ...
        #           "d" for (negativ?) float numbers
        #           "i" for negativ whole numbers
        #           "s" for positiv whole numbers

        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = self.ffperm_res_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

        if self.ffperm_res_unit != "":
            fieldentry.text = "a:10:{" \
                              "s:9:\"precision\";i:" + self.ffperm_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + self.ffperm_res_tol_length + ":\"" + self.ffperm_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + self.ffperm_res_min_length + ":\"" + self.ffperm_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + self.ffperm_res_max_length + ":\"" + self.ffperm_res_max + "\";" \
                              "s:6:\"points\";s:1:\"" + self.ffperm_res_points + "\";" \
                              "s:7:\"formula\";s:" + self.ffperm_res_formula_length + ":\"" + self.ffperm_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:" + str(self.ffperm_res_unit_length) + ":\"" + self.ffperm_res_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage_Permutation.unit_table(self, self.ffperm_res_unit))) + ":\"" + Formelfrage_Permutation.unit_table(self, self.ffperm_res_unit) + "\";" \
                              "s:11:\"resultunits\";a:27:{i:0;a:2:{s:4:\"unit\";s:1:\"H\";s:9:\"unitvalue\";s:3:\"125\";}" \
                                                            "i:1;a:2:{s:4:\"unit\";s:2:\"mH\";s:9:\"unitvalue\";s:3:\"126\";}" \
                                                            "i:2;a:2:{s:4:\"unit\";s:3:\"µH\";s:9:\"unitvalue\";s:3:\"127\";}" \
                                                            "i:3;a:2:{s:4:\"unit\";s:2:\"nH\";s:9:\"unitvalue\";s:3:\"128\";}" \
                                                            "i:4;a:2:{s:4:\"unit\";s:2:\"kH\";s:9:\"unitvalue\";s:3:\"129\";}" \
                                                            "i:5;a:2:{s:4:\"unit\";s:2:\"pH\";s:9:\"unitvalue\";s:3:\"130\";}" \
                                                            "i:6;a:2:{s:4:\"unit\";s:1:\"F\";s:9:\"unitvalue\";s:3:\"131\";}" \
                                                            "i:7;a:2:{s:4:\"unit\";s:2:\"mF\";s:9:\"unitvalue\";s:3:\"132\";}" \
                                                            "i:8;a:2:{s:4:\"unit\";s:3:\"µF\";s:9:\"unitvalue\";s:3:\"133\";}" \
                                                            "i:9;a:2:{s:4:\"unit\";s:2:\"nF\";s:9:\"unitvalue\";s:3:\"134\";}" \
                                                            "i:10;a:2:{s:4:\"unit\";s:2:\"pF\";s:9:\"unitvalue\";s:3:\"135\";}" \
                                                            "i:11;a:2:{s:4:\"unit\";s:1:\"W\";s:9:\"unitvalue\";s:3:\"136\";}" \
                                                            "i:12;a:2:{s:4:\"unit\";s:2:\"kW\";s:9:\"unitvalue\";s:3:\"137\";}" \
                                                            "i:13;a:2:{s:4:\"unit\";s:2:\"MW\";s:9:\"unitvalue\";s:3:\"138\";}" \
                                                            "i:14;a:2:{s:4:\"unit\";s:1:\"V\";s:9:\"unitvalue\";s:3:\"139\";}" \
                                                            "i:15;a:2:{s:4:\"unit\";s:2:\"kV\";s:9:\"unitvalue\";s:3:\"140\";}" \
                                                            "i:16;a:2:{s:4:\"unit\";s:2:\"mV\";s:9:\"unitvalue\";s:3:\"141\";}" \
                                                            "i:17;a:2:{s:4:\"unit\";s:3:\"µV\";s:9:\"unitvalue\";s:3:\"142\";}" \
                                                            "i:18;a:2:{s:4:\"unit\";s:2:\"MV\";s:9:\"unitvalue\";s:3:\"143\";}" \
                                                            "i:19;a:2:{s:4:\"unit\";s:1:\"A\";s:9:\"unitvalue\";s:3:\"144\";}" \
                                                            "i:20;a:2:{s:4:\"unit\";s:2:\"mA\";s:9:\"unitvalue\";s:3:\"145\";}" \
                                                            "i:21;a:2:{s:4:\"unit\";s:3:\"µA\";s:9:\"unitvalue\";s:3:\"146\";}" \
                                                            "i:22;a:2:{s:4:\"unit\";s:2:\"kA\";s:9:\"unitvalue\";s:3:\"147\";}" \
                                                            "i:23;a:2:{s:4:\"unit\";s:3:\"Ohm\";s:9:\"unitvalue\";s:3:\"148\";}" \
                                                            "i:24;a:2:{s:4:\"unit\";s:2:\"mW\";s:9:\"unitvalue\";s:3:\"149\";}" \
                                                            "i:25;a:2:{s:4:\"unit\";s:4:\"kOhm\";s:9:\"unitvalue\";s:3:\"150\";}" \
                                                            "i:26;a:2:{s:4:\"unit\";s:4:\"mOhm\";s:9:\"unitvalue\";s:3:\"151\";}}" \
                              "}"

        else:
            fieldentry.text = "a:10:{" \
                              "s:9:\"precision\";i:" + self.ffperm_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + str(self.ffperm_res_tol_length) + ":\"" + self.ffperm_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + str(self.ffperm_res_min_length) + ":\"" + self.ffperm_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + str(self.ffperm_res_max_length) + ":\"" + self.ffperm_res_max + "\";" \
                              "s:6:\"points\";s:1:\"" + self.ffperm_res_points + "\";" \
                              "s:7:\"formula\";s:" + str(self.ffperm_res_formula_length) + ":\"" + self.ffperm_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "s:11:\"resultunits\";a:0:{}" \
                              "}"



class Create_formelfrage_permutation_Test(Formelfrage_Permutation):
    def __init__(self, entry_to_index_dict):
        self.ffperm_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.ffperm_db_entry_to_index_dict,
                                                                            self.formelfrage_permutation_test_tst_file_path_template,
                                                                            self.formelfrage_permutation_test_tst_file_path_output,
                                                                            self.formelfrage_permutation_test_qti_file_path_template,
                                                                            self.formelfrage_permutation_test_qti_file_path_output,
                                                                            self.ffperm_ilias_test_title_entry.get(),
                                                                            self.create_formelfrage_permutation_test_entry.get(),
                                                                            self.ffperm_question_type_entry.get(),
                                                                            )




class Create_formelfrage_permutation_Pool(Formelfrage_Permutation):

    def __init__(self, entry_to_index_dict, var_create_all_questions):
        self.ffperm_entry_to_index_dict = entry_to_index_dict
        self.ffperm_var_create_question_pool_all = var_create_all_questions

        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(self,
                                                                            self.project_root_path,
                                                                            self.formelfrage_permutation_pool_directory_output,
                                                                            self.formelfrage_permutation_files_path_pool_output,
                                                                            self.formelfrage_permutation_pool_qti_file_path_template,
                                                                            self.ffperm_ilias_test_title_entry.get(),
                                                                            self.create_formelfrage_permutation_pool_entry.get(),
                                                                            self.ffperm_question_type_entry.get(),
                                                                            self.database_formelfrage_permutation_path,
                                                                            "formelfrage_permutation_table",
                                                                            self.ffperm_db_entry_to_index_dict,
                                                                            self.ffperm_var_create_question_pool_all
                                                                            )


