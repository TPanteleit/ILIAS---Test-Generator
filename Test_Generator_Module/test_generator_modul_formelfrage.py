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
import re


### Eigene Dateien / Module
from Test_Generator_Module import test_generator_modul_datenbanken_anzeigen
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_test_struktur
from Test_Generator_Module import test_generator_modul_ilias_import_test_datei

class Formelfrage:
    def __init__(self, app, formelfrage_tab, project_root_path):

############## SET IMAGE VARIABLES

        # Die Variablen müssen am Anfang des Programms gesetzt werden, um diese an andere Funktionen weitergeben zu können

        self.formelfrage_tab = formelfrage_tab

        self.ff_description_img_name_1 = "EMPTY"
        self.ff_description_img_name_2 = "EMPTY"
        self.ff_description_img_name_3 = "EMPTY"

        self.ff_description_img_data_1 = "EMPTY"
        self.ff_description_img_data_2 = "EMPTY"
        self.ff_description_img_data_3 = "EMPTY"

        self.ff_description_img_path_1 = "EMPTY"
        self.ff_description_img_path_2 = "EMPTY"
        self.ff_description_img_path_3 = "EMPTY"



############## DEFINE FORMELFRAGE PATHS

        # Pfad des Projekts und des FF-Moduls
        self.project_root_path = project_root_path
        self.formelfrage_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Formelfrage"))
        self.formelfrage_files_path_pool_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_formelfrage_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_formelfrage_db.db"))

        # Pfad für ILIAS-Test Vorlage
        self.formelfrage_test_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.formelfrage_test_tst_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))


        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.formelfrage_test_qti_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.formelfrage_test_tst_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.formelfrage_test_img_file_path = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))


        # Pfad für ILIAS-Pool Vorlage
        self.formelfrage_pool_qti_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.formelfrage_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))


        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # Die Pfade für die qti.xml und qpl.xml werden erst zur Laufzeit bestimmt.
        # Die Deklaration ist daher unter "class Create_Formelfrage_Pool"
        self.formelfrage_pool_directory_output = os.path.normpath(os.path.join(self.formelfrage_files_path, "ff_ilias_pool_abgabe"))


###################### DATENBANK ENTRIES UND INDEX DICT ERSTELLEN  ###################


        # Dictionary aus zwei Listen erstellen
        # Auslesen der Formelfrage-Datenbank einträgen
        # Nur die erste Zeile auslesen um einen Zusammenhang zwischen Variablen und Indexen herzustellen
        self.ff_db_find_entries = []
        self.ff_db_find_indexes = []

        connect = sqlite3.connect(self.database_formelfrage_path)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM formelfrage_table LIMIT 1")

        ff_db_records = cursor.fetchall()
        for ff_db_record in ff_db_records:
            for k in range(len(ff_db_record)):
                self.ff_db_find_entries.append(str(ff_db_record[k]))
                self.ff_db_find_indexes.append(int(k))


        self.ff_db_entry_to_index_dict = dict(zip((self.ff_db_find_entries), (self.ff_db_find_indexes)))



        connect.commit()
        connect.close()



############## FRAMES
        self.ff_frame_ilias_test_title = LabelFrame(self.formelfrage_tab, text="Testname & Autor", padx=5, pady=5)
        self.ff_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame = LabelFrame(self.formelfrage_tab, text="Formelfrage", padx=5, pady=5)
        self.ff_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame_question_attributes = LabelFrame(self.formelfrage_tab, text="Fragen Attribute", padx=5, pady=5)
        self.ff_frame_question_attributes.grid(row=2, column=0, padx=10, pady=10, sticky="NE")

        self.ff_frame_database = LabelFrame(self.formelfrage_tab, text="Formelfrage-Datenbank", padx=5, pady=5)
        self.ff_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.ff_frame_create_formelfrage_test = LabelFrame(self.formelfrage_tab, text="FF-Test erstellen", padx=5, pady=5)
        self.ff_frame_create_formelfrage_test.grid(row=2, column=0, padx=105, pady=120, sticky="NE")


        self.ff_frame_taxonomy_settings = LabelFrame(self.formelfrage_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.ff_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.ff_frame_question_description_functions = LabelFrame(self.formelfrage_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.ff_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.ff_frame_excel_import_export = LabelFrame(self.formelfrage_tab, text="Excel Import/Export", padx=5, pady=5)
        self.ff_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")




        self.ff_frame_description_picture = LabelFrame(self.formelfrage_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.ff_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")


###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        self.ff_ilias_test_title_label = Label(self.ff_frame_ilias_test_title, text="Name des Tests")
        self.ff_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.ff_ilias_test_title_entry = Entry(self.ff_frame_ilias_test_title, width=60)
        self.ff_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.ff_ilias_test_autor_label = Label(self.ff_frame_ilias_test_title, text="Autor")
        self.ff_ilias_test_autor_label.grid(row=1, column=0, sticky=W)

        self.ff_ilias_test_autor_entry = Entry(self.ff_frame_ilias_test_title, width=60)
        self.ff_ilias_test_autor_entry.grid(row=1, column=1, sticky=W, padx=30)

###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.ff_var_use_image_1 = IntVar()
        self.ff_check_use_image_1_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.ff_var_use_image_1, onvalue=1, offvalue=0)
        self.ff_check_use_image_1_in_description.deselect()
        self.ff_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.ff_var_use_image_2 = IntVar()
        self.ff_check_use_image_2_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.ff_var_use_image_2, onvalue=1, offvalue=0)
        self.ff_check_use_image_2_in_description.deselect()
        self.ff_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.ff_var_use_image_3 = IntVar()
        self.ff_check_use_image_3_in_description = Checkbutton(self.ff_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.ff_var_use_image_3, onvalue=1, offvalue=0)
        self.ff_check_use_image_3_in_description.deselect()
        self.ff_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        #self.ff_add_img_to_description_btn = Button(self.ff_frame_question_description_functions, text="Bild hinzufügen", command=lambda: Formelfrage.ff_add_image_to_description(self, self.ff_var_use_image_1.get(), self.ff_var_use_image_2.get(), self.ff_var_use_image_3.get()))
       # self.ff_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))

        self.ff_add_img_to_description_btn = Button(self.ff_frame_question_description_functions, text="Bild hinzufügen", command=lambda: ff_add_image_to_description_and_create_labels())
        self.ff_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))

        # Bild zum Fragentext hinzufügen
        def ff_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.ff_question_description_img_1_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_1)
            self.ff_question_description_img_2_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_2)
            self.ff_question_description_img_3_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_3)


            self.ff_description_img_name_1, self.ff_description_img_name_2, self.ff_description_img_name_3, self.ff_description_img_path_1, self.ff_description_img_path_2, self.ff_description_img_path_3, self.ff_question_description_img_1_filename_label, self.ff_question_description_img_2_filename_label, self.ff_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.ff_var_use_image_1.get(),
                    self.ff_var_use_image_2.get(),
                    self.ff_var_use_image_3.get(),
                    self.ff_frame_description_picture,
                    self.ff_description_img_name_1,
                    self.ff_description_img_name_2,
                    self.ff_description_img_name_3,
                    self.ff_description_img_path_1,
                    self.ff_description_img_path_2,
                    self.ff_description_img_path_3,
                    )


        #self.ff_remove_img_from_description_btn = Button(self.ff_frame_question_description_functions, text="Bild entfernen", command=lambda: Formelfrage.ff_delete_image_from_description(self, self.ff_var_use_image_1.get(), self.ff_var_use_image_2.get(), self.ff_var_use_image_3.get()))
        #self.ff_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        self.ff_remove_img_from_description_btn = Button(self.ff_frame_question_description_functions, text="Bild entfernen", command=lambda: ff_add_image_to_description_and_delete_labels())
        self.ff_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        # Bild aus Fragentext entfernen
        def ff_add_image_to_description_and_delete_labels():
            self.ff_description_img_name_1, self.ff_description_img_name_2, self.ff_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self, self.ff_var_use_image_1.get(),
                 self.ff_var_use_image_2.get(),
                 self.ff_var_use_image_3.get(),
                 self.ff_question_description_img_1_filename_label,
                 self.ff_question_description_img_2_filename_label,
                 self.ff_question_description_img_3_filename_label,
                 self.ff_description_img_name_1,
                 self.ff_description_img_name_2,
                 self.ff_description_img_name_3,
            )



        ###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.ff_taxonomy_settings_btn = Button(self.ff_frame_taxonomy_settings, text="Taxonomie-Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.ff_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")


###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ff_question_difficulty_label = Label(self.ff_frame_question_attributes, text="Schwierigkeit")
        self.ff_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.ff_question_difficulty_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.ff_question_category_label = Label(self.ff_frame_question_attributes, text="Fragenkategorie")
        self.ff_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.ff_question_category_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.ff_question_type_label = Label(self.ff_frame_question_attributes, text="Fragen-Typ")
        self.ff_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.ff_question_type_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.ff_question_type_entry.insert(0, "Formelfrage")

        self.ff_question_pool_tag_label = Label(self.ff_frame_question_attributes, text="Pool-Tag")
        self.ff_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.ff_question_pool_tag_entry = Entry(self.ff_frame_question_attributes, width=15)
        self.ff_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)




###################### "FF-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # Button "Formelfrage-Test erstellen"
        self.create_formelfrage_test_btn = Button(self.ff_frame_create_formelfrage_test, text="FF-Test erstellen", command=lambda: Create_Formelfrage_Test.__init__(self, self.ff_db_entry_to_index_dict))
        self.create_formelfrage_test_btn.grid(row=0, column=0, sticky=W)
        self.create_formelfrage_test_entry = Entry(self.ff_frame_create_formelfrage_test, width=15)
        self.create_formelfrage_test_entry.grid(row=0, column=1, sticky=W, padx=0)

        # Checkbox "Test-Einstellungen übernehmen?"
        self.create_test_settings_label = Label(self.ff_frame_create_formelfrage_test, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)

        # Checkbox "Latex für Fragentext nutzen?"
        self.ff_use_latex_on_text_label = Label(self.ff_frame_create_formelfrage_test, text="Latex für Fragentext nutzen?")
        self.ff_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.ff_var_use_latex_on_text_check = IntVar()
        self.ff_use_latex_on_text_check = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.ff_use_latex_on_text_check.deselect()
        self.ff_use_latex_on_text_check.grid(row=2, column=1, sticky=W)




        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.ff_create_question_pool_all_label = Label(self.ff_frame_create_formelfrage_test, text="Alle Einträge aus der DB erzeugen?")
        self.ff_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.ff_var_create_question_pool_all_check = IntVar()
        self.ff_create_question_pool_all = Checkbutton(self.ff_frame_create_formelfrage_test, text="", variable=self.ff_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.ff_var_create_question_pool_all_check.set(0)
        self.ff_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))



        # Button "Formelfrage-Fragenpool erstellen"
        self.create_formelfrage_pool_btn = Button(self.ff_frame_create_formelfrage_test, text="FF-Pool erstellen", command=lambda: Create_Formelfrage_Pool.__init__(self, self.ff_db_entry_to_index_dict, self.ff_var_create_question_pool_all_check.get()))
        self.create_formelfrage_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_formelfrage_pool_entry = Entry(self.ff_frame_create_formelfrage_test, width=15)
        self.create_formelfrage_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))



###################### "Formelfrage-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################



        self.ff_database_show_db_formelfrage_btn = Button(self.ff_frame_database, text="FF - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_formelfrage_path, "formelfrage_table"))
        self.ff_database_show_db_formelfrage_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.ff_database_save_id_to_db_formelfrage_btn = Button(self.ff_frame_database, text="Speichern unter neuer ID", command=lambda: Formelfrage.ff_save_id_to_db(self))
        self.ff_database_save_id_to_db_formelfrage_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.ff_database_delete_id_from_db_btn = Button(self.ff_frame_database, text="ID Löschen", command=lambda: Formelfrage.ff_delete_id_from_db(self))
        self.ff_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.ff_delete_box = Entry(self.ff_frame_database, width=10)
        self.ff_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        self.ff_database_new_question_btn = Button(self.ff_frame_database, text="GUI Einträge leeren", command=lambda: Formelfrage.ff_clear_GUI(self))
        self.ff_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        self.ff_database_edit_btn = Button(self.ff_frame_database, text="Aktuellen Eintrag editieren", command=lambda: Formelfrage.ff_edit_id_from_db(self))
        self.ff_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.ff_database_load_id_btn = Button(self.ff_frame_database, text="ID Laden", command=lambda: Formelfrage.ff_load_id_from_db(self, self.ff_db_entry_to_index_dict))
        self.ff_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.ff_load_box = Entry(self.ff_frame_database, width=10)
        self.ff_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))


        # Checkbox - "Fragentext mit Highlighting?"
        self.ff_highlight_question_text_label = Label(self.ff_frame_database, text="Fragentext mit Highlighting?")
        self.ff_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.ff_var_highlight_question_text = IntVar()
        self.ff_check_highlight_question_text = Checkbutton(self.ff_frame_database, text="", variable=self.ff_var_highlight_question_text, onvalue=1, offvalue=0)
        self.ff_check_highlight_question_text.deselect()
        self.ff_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.ff_delete_all_label = Label(self.ff_frame_database, text="Alle DB Einträge löschen?")
        self.ff_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.ff_var_delete_all = IntVar()
        self.ff_check_delete_all = Checkbutton(self.ff_frame_database, text="", variable=self.ff_var_delete_all, onvalue=1, offvalue=0)
        self.ff_check_delete_all.deselect()
        self.ff_check_delete_all.grid(row=7, column=0, sticky=E)


###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.table_name = "Formelfrage_DB_export.xlsx"


        # excel_import_btn
        self.ff_excel_import_to_db_formelfrage_btn = Button(self.ff_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, "formelfrage", self.ff_db_entry_to_index_dict))
        self.ff_excel_import_to_db_formelfrage_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.ff_excel_export_to_xlsx_formelfrage_btn = Button(self.ff_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.ff_db_entry_to_index_dict, self.database_formelfrage_path, "formelfrage_db.db", "formelfrage_table", "Formelfrage_DB_export_file.xlsx", "Formelfrage - Database"))
        self.ff_excel_export_to_xlsx_formelfrage_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)


        # ILIAS_testfile_import
        self.ff_import_ilias_testfile_btn = Button(self.ff_frame_excel_import_export, text="ILIAS-Datei importieren",command=lambda: test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path))
        self.ff_import_ilias_testfile_btn.grid(row=2, column=1, sticky=W, pady=(20,0), padx=10)




###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.ff_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.ff_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.ff_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.ff_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.ff_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.ff_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.ff_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.ff_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.ff_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.ff_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")

###################### "Formelfrage" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.ff_question_author_label = Label(self.ff_frame, text="Fragen-Autor")
        self.ff_question_author_label.grid(row=0, column=0, sticky=W, pady=(10, 0), padx=10)
        self.ff_question_author_entry = Entry(self.ff_frame, width=20)
        self.ff_question_author_entry.grid(row=0, column=1, sticky=W, pady=(10, 0))

        self.ff_question_title_label = Label(self.ff_frame, text="Fragen-Titel")
        self.ff_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.ff_question_title_entry = Entry(self.ff_frame, width=60)
        self.ff_question_title_entry.grid(row=1, column=1,  sticky=W, pady=(10, 0))

        self.ff_question_description_title_label = Label(self.ff_frame, text="Fragen-Beschreibung")
        self.ff_question_description_title_label.grid(row=2, column=0, sticky=W, padx=10)
        self.ff_question_description_title_entry = Entry(self.ff_frame, width=60)
        self.ff_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.ff_question_textfield_label = Label(self.ff_frame, text="Fragen-Text")
        self.ff_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.ff_bar = Scrollbar(self.ff_frame)
        self.ff_question_description_main_entry = Text(self.ff_frame, height=6, width=65, font=('Helvetica', 9))
        self.ff_bar.grid(row=3, column=2, sticky=W)
        self.ff_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.ff_bar.config(command=self.ff_question_description_main_entry.yview)
        self.ff_question_description_main_entry.config(yscrollcommand=self.ff_bar.set)





        ################### BEARBEITUNGSDAUER


        self.ff_processing_time_label = Label(self.ff_frame, text="Bearbeitungsdauer")
        self.ff_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.ff_processing_time_label = Label(self.ff_frame, text="Std:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.ff_processing_time_label = Label(self.ff_frame, text="Min:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.ff_processing_time_label = Label(self.ff_frame, text="Sek:")
        self.ff_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        self.ff_processingtime_hours = list(range(24))
        self.ff_processingtime_minutes = list(range(60))
        self.ff_processingtime_seconds = list(range(60))

        self.ff_proc_hours_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_hours, width=2)
        self.ff_proc_minutes_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_minutes, width=2)
        self.ff_proc_seconds_box = ttk.Combobox(self.ff_frame, value=self.ff_processingtime_seconds, width=2)

        self.ff_proc_hours_box.current(23)
        self.ff_proc_minutes_box.current(0)
        self.ff_proc_seconds_box.current(0)

        def selected_hours(event):
            self.selected_hours = self.ff_proc_hours_box.get()


        def selected_minutes(event):
            self.selected_minutes = self.ff_proc_minutes_box.get()


        def selected_seconds(event):
            self.selected_seconds = self.ff_proc_seconds_box.get()


        self.ff_proc_hours_box.bind("<<ComboboxSelected>>", selected_hours)
        self.ff_proc_minutes_box.bind("<<ComboboxSelected>>", selected_minutes)
        self.ff_proc_seconds_box.bind("<<ComboboxSelected>>", selected_seconds)

        self.ff_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.ff_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.ff_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))





        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        self.var_min_label = Label(self.ff_frame, text=' Min.')
        self.var_min_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=60)

        self.var_max_label = Label(self.ff_frame, text=' Max.')
        self.var_max_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=100)

        self.var_prec_label = Label(self.ff_frame, text=' Präz.')
        self.var_prec_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=140)

        self.var_divby_label = Label(self.ff_frame, text=' Teilbar\ndurch')
        self.var_divby_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=180)

        self.variable1_label = Label(self.ff_frame, text='Variable 1')
        self.variable2_label = Label(self.ff_frame, text='Variable 2')
        self.variable3_label = Label(self.ff_frame, text='Variable 3')
        self.variable4_label = Label(self.ff_frame, text='Variable 4')
        self.variable5_label = Label(self.ff_frame, text='Variable 5')
        self.variable6_label = Label(self.ff_frame, text='Variable 6')
        self.variable7_label = Label(self.ff_frame, text='Variable 7')
        self.variable8_label = Label(self.ff_frame, text='Variable 8')
        self.variable9_label = Label(self.ff_frame, text='Variable 9')
        self.variable10_label = Label(self.ff_frame, text='Variable 10')
        self.variable11_label = Label(self.ff_frame, text='Variable 11')
        self.variable12_label = Label(self.ff_frame, text='Variable 12')
        self.variable13_label = Label(self.ff_frame, text='Variable 13')
        self.variable14_label = Label(self.ff_frame, text='Variable 14')
        self.variable15_label = Label(self.ff_frame, text='Variable 15')

        # Label für Var1 ist immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.variable1_label.grid(row=6, column=0, sticky=W, padx=20)



        



        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.var1_name_entry = Entry(self.ff_frame,  width=6)
        self.var1_min_entry = Entry(self.ff_frame,  width=6)
        self.var1_max_entry = Entry(self.ff_frame,  width=6)
        self.var1_prec_entry = Entry(self.ff_frame,  width=6)
        self.var1_divby_entry = Entry(self.ff_frame,  width=6)

        self.var2_name_entry = Entry(self.ff_frame,  width=6)
        self.var2_min_entry = Entry(self.ff_frame,  width=6)
        self.var2_max_entry = Entry(self.ff_frame,  width=6)
        self.var2_prec_entry = Entry(self.ff_frame,  width=6)
        self.var2_divby_entry = Entry(self.ff_frame,  width=6)

        self.var3_name_entry = Entry(self.ff_frame,  width=6)
        self.var3_min_entry = Entry(self.ff_frame,  width=6)
        self.var3_max_entry = Entry(self.ff_frame,  width=6)
        self.var3_prec_entry = Entry(self.ff_frame,  width=6)
        self.var3_divby_entry = Entry(self.ff_frame,  width=6)

        self.var4_name_entry = Entry(self.ff_frame,  width=6)
        self.var4_min_entry = Entry(self.ff_frame,  width=6)
        self.var4_max_entry = Entry(self.ff_frame,  width=6)
        self.var4_prec_entry = Entry(self.ff_frame,  width=6)
        self.var4_divby_entry = Entry(self.ff_frame,  width=6)

        self.var5_name_entry = Entry(self.ff_frame,  width=6)
        self.var5_min_entry = Entry(self.ff_frame,  width=6)
        self.var5_max_entry = Entry(self.ff_frame,  width=6)
        self.var5_prec_entry = Entry(self.ff_frame,  width=6)
        self.var5_divby_entry = Entry(self.ff_frame,  width=6)

        self.var6_name_entry = Entry(self.ff_frame,  width=6)
        self.var6_min_entry = Entry(self.ff_frame,  width=6)
        self.var6_max_entry = Entry(self.ff_frame,  width=6)
        self.var6_prec_entry = Entry(self.ff_frame,  width=6)
        self.var6_divby_entry = Entry(self.ff_frame,  width=6)

        self.var7_name_entry = Entry(self.ff_frame,  width=6)
        self.var7_min_entry = Entry(self.ff_frame,  width=6)
        self.var7_max_entry = Entry(self.ff_frame, width=6)
        self.var7_prec_entry = Entry(self.ff_frame,  width=6)
        self.var7_divby_entry = Entry(self.ff_frame,  width=6)

        self.var8_name_entry = Entry(self.ff_frame,  width=6)
        self.var8_min_entry = Entry(self.ff_frame,  width=6)
        self.var8_max_entry = Entry(self.ff_frame,  width=6)
        self.var8_prec_entry = Entry(self.ff_frame,  width=6)
        self.var8_divby_entry = Entry(self.ff_frame,  width=6)

        self.var9_name_entry = Entry(self.ff_frame,  width=6)
        self.var9_min_entry = Entry(self.ff_frame,  width=6)
        self.var9_max_entry = Entry(self.ff_frame,  width=6)
        self.var9_prec_entry = Entry(self.ff_frame,  width=6)
        self.var9_divby_entry = Entry(self.ff_frame,  width=6)

        self.var10_name_entry = Entry(self.ff_frame,  width=6)
        self.var10_min_entry = Entry(self.ff_frame, width=6)
        self.var10_max_entry = Entry(self.ff_frame, width=6)
        self.var10_prec_entry = Entry(self.ff_frame, width=6)
        self.var10_divby_entry = Entry(self.ff_frame, width=6)

        self.var11_name_entry = Entry(self.ff_frame,  width=6)
        self.var11_min_entry = Entry(self.ff_frame, width=6)
        self.var11_max_entry = Entry(self.ff_frame, width=6)
        self.var11_prec_entry = Entry(self.ff_frame, width=6)
        self.var11_divby_entry = Entry(self.ff_frame, width=6)

        self.var12_name_entry = Entry(self.ff_frame,  width=6)
        self.var12_min_entry = Entry(self.ff_frame, width=6)
        self.var12_max_entry = Entry(self.ff_frame, width=6)
        self.var12_prec_entry = Entry(self.ff_frame, width=6)
        self.var12_divby_entry = Entry(self.ff_frame, width=6)

        self.var13_name_entry = Entry(self.ff_frame,  width=6)
        self.var13_min_entry = Entry(self.ff_frame, width=6)
        self.var13_max_entry = Entry(self.ff_frame, width=6)
        self.var13_prec_entry = Entry(self.ff_frame, width=6)
        self.var13_divby_entry = Entry(self.ff_frame, width=6)

        self.var14_name_entry = Entry(self.ff_frame,  width=6)
        self.var14_min_entry = Entry(self.ff_frame, width=6)
        self.var14_max_entry = Entry(self.ff_frame, width=6)
        self.var14_prec_entry = Entry(self.ff_frame, width=6)
        self.var14_divby_entry = Entry(self.ff_frame, width=6)

        self.var15_name_entry = Entry(self.ff_frame,  width=6)
        self.var15_min_entry = Entry(self.ff_frame, width=6)
        self.var15_max_entry = Entry(self.ff_frame, width=6)
        self.var15_prec_entry = Entry(self.ff_frame, width=6)
        self.var15_divby_entry = Entry(self.ff_frame, width=6)



        # Eingabefelder für Var1 sind immer aktiv/ zu sehen. Var2-10 werden je nach Auswahl ein-/ausgeblendet
        self.var1_name_entry.grid(row=6, column=1, sticky=W)
        self.var1_min_entry.grid(row=6, column=1, sticky=W, padx=60)
        self.var1_max_entry.grid(row=6, column=1, sticky=W, padx=100)
        self.var1_prec_entry.grid(row=6, column=1, sticky=W, padx=140)
        self.var1_divby_entry.grid(row=6, column=1, sticky=W, padx=180)

        # Wertebereich berechnen für Formel aus Eingabefeld: formula 1
        self.calculate_value_range_btn = Button(self.ff_frame, text="Wertebereich berechnen",command=lambda: Formelfrage.ff_calculate_value_range_from_formula(self, self.res1_formula_entry.get()))
        #self.calculate_value_range_btn.grid(row=6, column=1, padx=50, sticky="E")




        ###########################  EINGABEFELDER-MATRIX (VARIABLEN)  EIN/AUSBLENDEN ##############################

        # Hier werden durch die Funktion "ff_answer_selected" die Variable - Eingabefelder (je nach Wert) ein-/ausgeblendet

        def ff_answer_selected(event):  # "variable" need for comboBox Binding


            if self.ff_numbers_of_answers_box.get() == '1':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '2':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '3':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '4':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '5':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '6':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '7':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '8':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '9':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '10':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '11':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '12':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '13':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "remove")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '14':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "remove")

            elif self.ff_numbers_of_answers_box.get() == '15':
                Formelfrage.ff_variable_show_or_remove(self, self.variable2_label, self.var2_name_entry, self.var2_min_entry, self.var2_max_entry, self.var2_prec_entry, self.var2_divby_entry, "7", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable3_label, self.var3_name_entry, self.var3_min_entry, self.var3_max_entry, self.var3_prec_entry, self.var3_divby_entry, "8", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable4_label, self.var4_name_entry, self.var4_min_entry, self.var4_max_entry, self.var4_prec_entry, self.var4_divby_entry, "9", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable5_label, self.var5_name_entry, self.var5_min_entry, self.var5_max_entry, self.var5_prec_entry, self.var5_divby_entry, "10", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable6_label, self.var6_name_entry, self.var6_min_entry, self.var6_max_entry, self.var6_prec_entry, self.var6_divby_entry, "11", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable7_label, self.var7_name_entry, self.var7_min_entry, self.var7_max_entry, self.var7_prec_entry, self.var7_divby_entry, "12", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable8_label, self.var8_name_entry, self.var8_min_entry, self.var8_max_entry, self.var8_prec_entry, self.var8_divby_entry, "13", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable9_label, self.var9_name_entry, self.var9_min_entry, self.var9_max_entry, self.var9_prec_entry, self.var9_divby_entry, "14", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable10_label, self.var10_name_entry, self.var10_min_entry, self.var10_max_entry, self.var10_prec_entry, self.var10_divby_entry, "15", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable11_label, self.var11_name_entry, self.var11_min_entry, self.var11_max_entry, self.var11_prec_entry, self.var11_divby_entry, "16", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable12_label, self.var12_name_entry, self.var12_min_entry, self.var12_max_entry, self.var12_prec_entry, self.var12_divby_entry, "17", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable13_label, self.var13_name_entry, self.var13_min_entry, self.var13_max_entry, self.var13_prec_entry, self.var13_divby_entry, "18", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable14_label, self.var14_name_entry, self.var14_min_entry, self.var14_max_entry, self.var14_prec_entry, self.var14_divby_entry, "19", "show")
                Formelfrage.ff_variable_show_or_remove(self, self.variable15_label, self.var15_name_entry, self.var15_min_entry, self.var15_max_entry, self.var15_prec_entry, self.var15_divby_entry, "20", "show")



        self.ff_numbers_of_answers_box_label = Label(self.ff_frame, text="Anzahl der Variablen: ")
        self.ff_numbers_of_answers_box_label.grid(row=5, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ff_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
        self.ff_numbers_of_answers_box = ttk.Combobox(self.ff_frame, value=self.ff_numbers_of_answers_value, width=3)
        self.ff_numbers_of_answers_box.bind("<<ComboboxSelected>>", ff_answer_selected)
        self.ff_numbers_of_answers_box.grid(row=5, column=1, sticky=W, pady=(20, 0))
        self.ff_numbers_of_answers_box.current(0)


        ###########################  AUSWAHL DER EINHEITEN FÜR VARIABLEN ---- DERZEIT NICHT AKTIV ##############################

        self.select_var_units = ["Unit", "H", "mH", "µH", "nH", "pH", "---", "F", "mF", "µF", "nF", "pF", "---", "MV", "kV", "V", "mV", "µV", "---"]

        self.var1_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var1_unit_myCombo.current(0)

        self.var2_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var2_unit_myCombo.current(0)

        self.var3_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var3_unit_myCombo.current(0)

        self.var4_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var4_unit_myCombo.current(0)

        self.var5_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var5_unit_myCombo.current(0)

        self.var6_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var6_unit_myCombo.current(0)

        self.var7_unit_myCombo = ttk.Combobox(self.ff_frame, value=self.select_var_units, width=5)
        self.var7_unit_myCombo.current(0)


        ########################### ÜBERSCHRIFTEN / LABELS FÜR EINGABEFELDER-MATRIX ##############################

        self.res_min_label = Label(self.ff_frame, text=' Min.')
        self.res_max_label = Label(self.ff_frame, text=' Max.')
        self.res_prec_label = Label(self.ff_frame, text=' Präz.')
        self.res_tol_label = Label(self.ff_frame, text='  Tol.')
        self.res_points_label = Label(self.ff_frame, text='Punkte')
        self.res_formula_label = Label(self.ff_frame, text='Formel')

        self.res_min_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=60)
        self.res_max_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=100)
        self.res_prec_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=140)
        self.res_tol_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=180)
        self.res_points_label.grid(row=40, column=1, sticky=W, pady=(10, 0), padx=220)
        self.res_formula_label.grid(row=40, column=1, sticky=E, pady=(10, 0), padx=100)



        self.result1_label = Label(self.ff_frame, text='Ergebnis 1')
        self.result2_label = Label(self.ff_frame, text='Ergebnis 2')
        self.result3_label = Label(self.ff_frame, text='Ergebnis 3')
        self.result4_label = Label(self.ff_frame, text='Ergebnis 4')
        self.result5_label = Label(self.ff_frame, text='Ergebnis 5')
        self.result6_label = Label(self.ff_frame, text='Ergebnis 6')
        self.result7_label = Label(self.ff_frame, text='Ergebnis 7')
        self.result8_label = Label(self.ff_frame, text='Ergebnis 8')
        self.result9_label = Label(self.ff_frame, text='Ergebnis 9')
        self.result10_label = Label(self.ff_frame, text='Ergebnis 10')

        # Label für Res1 ist immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.result1_label.grid(row=41, column=0, sticky=W, padx=20)

        


        ########################### EINGABEFELDER / ENTRYS FÜR EINGABEFELDER-MATRIX ##############################

        self.res1_name_entry = Entry(self.ff_frame, width=6)
        self.res1_min_entry = Entry(self.ff_frame, width=6)
        self.res1_max_entry = Entry(self.ff_frame, width=6)
        self.res1_prec_entry = Entry(self.ff_frame, width=6)
        self.res1_tol_entry = Entry(self.ff_frame, width=6)
        self.res1_points_entry = Entry(self.ff_frame, width=6)
        self.res1_formula_entry = Entry(self.ff_frame, width=30)

        self.res2_name_entry = Entry(self.ff_frame, width=6)
        self.res2_min_entry = Entry(self.ff_frame, width=6)
        self.res2_max_entry = Entry(self.ff_frame, width=6)
        self.res2_prec_entry = Entry(self.ff_frame, width=6)
        self.res2_tol_entry = Entry(self.ff_frame, width=6)
        self.res2_points_entry = Entry(self.ff_frame, width=6)
        self.res2_formula_entry = Entry(self.ff_frame, width=30)

        self.res3_name_entry = Entry(self.ff_frame, width=6)
        self.res3_min_entry = Entry(self.ff_frame, width=6)
        self.res3_max_entry = Entry(self.ff_frame, width=6)
        self.res3_prec_entry = Entry(self.ff_frame, width=6)
        self.res3_tol_entry = Entry(self.ff_frame, width=6)
        self.res3_points_entry = Entry(self.ff_frame, width=6)
        self.res3_formula_entry = Entry(self.ff_frame, width=30)

        self.res4_name_entry = Entry(self.ff_frame, width=6)
        self.res4_min_entry = Entry(self.ff_frame, width=6)
        self.res4_max_entry = Entry(self.ff_frame, width=6)
        self.res4_prec_entry = Entry(self.ff_frame, width=6)
        self.res4_tol_entry = Entry(self.ff_frame, width=6)
        self.res4_points_entry = Entry(self.ff_frame, width=6)
        self.res4_formula_entry = Entry(self.ff_frame, width=30)

        self.res5_name_entry = Entry(self.ff_frame, width=6)
        self.res5_min_entry = Entry(self.ff_frame, width=6)
        self.res5_max_entry = Entry(self.ff_frame, width=6)
        self.res5_prec_entry = Entry(self.ff_frame, width=6)
        self.res5_tol_entry = Entry(self.ff_frame,  width=6)
        self.res5_points_entry = Entry(self.ff_frame, width=6)
        self.res5_formula_entry = Entry(self.ff_frame, width=30)

        self.res6_name_entry = Entry(self.ff_frame, width=6)
        self.res6_min_entry = Entry(self.ff_frame, width=6)
        self.res6_max_entry = Entry(self.ff_frame, width=6)
        self.res6_prec_entry = Entry(self.ff_frame, width=6)
        self.res6_tol_entry = Entry(self.ff_frame, width=6)
        self.res6_points_entry = Entry(self.ff_frame, width=6)
        self.res6_formula_entry = Entry(self.ff_frame, width=30)

        self.res7_name_entry = Entry(self.ff_frame, width=6)
        self.res7_min_entry = Entry(self.ff_frame, width=6)
        self.res7_max_entry = Entry(self.ff_frame, width=6)
        self.res7_prec_entry = Entry(self.ff_frame, width=6)
        self.res7_tol_entry = Entry(self.ff_frame, width=6)
        self.res7_points_entry = Entry(self.ff_frame, width=6)
        self.res7_formula_entry = Entry(self.ff_frame, width=30)

        self.res8_name_entry = Entry(self.ff_frame,  width=6)
        self.res8_min_entry = Entry(self.ff_frame,  width=6)
        self.res8_max_entry = Entry(self.ff_frame,  width=6)
        self.res8_prec_entry = Entry(self.ff_frame,  width=6)
        self.res8_tol_entry = Entry(self.ff_frame,  width=6)
        self.res8_points_entry = Entry(self.ff_frame,  width=6)
        self.res8_formula_entry = Entry(self.ff_frame,  width=30)

        self.res9_name_entry = Entry(self.ff_frame, width=6)
        self.res9_min_entry = Entry(self.ff_frame, width=6)
        self.res9_max_entry = Entry(self.ff_frame, width=6)
        self.res9_prec_entry = Entry(self.ff_frame, width=6)
        self.res9_tol_entry = Entry(self.ff_frame, width=6)
        self.res9_points_entry = Entry(self.ff_frame, width=6)
        self.res9_formula_entry = Entry(self.ff_frame, width=30)

        self.res10_name_entry = Entry(self.ff_frame, width=6)
        self.res10_min_entry = Entry(self.ff_frame, width=6)
        self.res10_max_entry = Entry(self.ff_frame, width=6)
        self.res10_prec_entry = Entry(self.ff_frame, width=6)
        self.res10_tol_entry = Entry(self.ff_frame, width=6)
        self.res10_points_entry = Entry(self.ff_frame, width=6)
        self.res10_formula_entry = Entry(self.ff_frame, width=30)

        # Eingabefelder für Res1 sind immer aktiv/ zu sehen. Res2-10 werden je nach Auswahl ein-/ausgeblendet
        self.res1_name_entry.grid(row=41, column=1, sticky=W)
        self.res1_min_entry.grid(row=41, column=1, sticky=W, padx=60)
        self.res1_max_entry.grid(row=41, column=1, sticky=W, padx=100)
        self.res1_prec_entry.grid(row=41, column=1, sticky=W, padx=140)
        self.res1_tol_entry.grid(row=41, column=1, sticky=W, padx=180)
        self.res1_points_entry.grid(row=41, column=1, sticky=W, padx=220)
        self.res1_formula_entry.grid(row=41, column=1, sticky=E, padx=20)







        #################### EINHEITEN FÜR ERGEBNISSE DERZEIT DEAKTIVIERT

        # self.res1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res1_unit_myCombo.current(0)
        # self.res1_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        # #self.res1_unit_myCombo.grid(row=21, column=0, sticky=E, padx=10)
        #
        # self.res2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res2_unit_myCombo.current(0)
        # self.res2_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        #
        # self.res3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        # self.res3_unit_myCombo.current(0)
        # self.res3_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)




        def ff_result_selected(event):  # "variable" need for comboBox Binding

            if self.ff_numbers_of_results_box.get() == '1':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '2':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '3':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '4':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '5':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '6':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '7':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '8':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "remove")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '9':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "remove")


            elif self.ff_numbers_of_results_box.get() == '10':
                Formelfrage.ff_result_show_or_remove(self, self.result2_label, self.res2_name_entry, self.res2_min_entry, self.res2_max_entry, self.res2_prec_entry, self.res2_tol_entry, self.res2_points_entry, self.res2_formula_entry, "42", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result3_label, self.res3_name_entry, self.res3_min_entry, self.res3_max_entry, self.res3_prec_entry, self.res3_tol_entry, self.res3_points_entry, self.res3_formula_entry, "43", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result4_label, self.res4_name_entry, self.res4_min_entry, self.res4_max_entry, self.res4_prec_entry, self.res4_tol_entry, self.res4_points_entry, self.res4_formula_entry, "44", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result5_label, self.res5_name_entry, self.res5_min_entry, self.res5_max_entry, self.res5_prec_entry, self.res5_tol_entry, self.res5_points_entry, self.res5_formula_entry, "45", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result6_label, self.res6_name_entry, self.res6_min_entry, self.res6_max_entry, self.res6_prec_entry, self.res6_tol_entry, self.res6_points_entry, self.res6_formula_entry, "46", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result7_label, self.res7_name_entry, self.res7_min_entry, self.res7_max_entry, self.res7_prec_entry, self.res7_tol_entry, self.res7_points_entry, self.res7_formula_entry, "47", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result8_label, self.res8_name_entry, self.res8_min_entry, self.res8_max_entry, self.res8_prec_entry, self.res8_tol_entry, self.res8_points_entry, self.res8_formula_entry, "48", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result9_label, self.res9_name_entry, self.res9_min_entry, self.res9_max_entry, self.res9_prec_entry, self.res9_tol_entry, self.res9_points_entry, self.res9_formula_entry, "49", "show")
                Formelfrage.ff_result_show_or_remove(self, self.result10_label, self.res10_name_entry, self.res10_min_entry, self.res10_max_entry, self.res10_prec_entry, self.res10_tol_entry, self.res10_points_entry, self.res10_formula_entry, "50", "show")


        self.ff_numbers_of_results_box_label = Label(self.ff_frame, text="Anzahl der Ergebnisse: ")
        self.ff_numbers_of_results_box_label.grid(row=40, column=0, sticky=W, padx=10, pady=(20, 0))
        self.ff_numbers_of_results_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.ff_numbers_of_results_box = ttk.Combobox(self.ff_frame, value=self.ff_numbers_of_results_value, width=3)
        self.ff_numbers_of_results_box.current(0)
        self.ff_numbers_of_results_box.bind("<<ComboboxSelected>>", ff_result_selected)
        self.ff_numbers_of_results_box.grid(row=40, column=1, sticky=W, pady=(20, 0))

    def ff_variable_show_or_remove(self, var_label, var_name_entry, var_min_entry, var_max_entry, var_prec_entry, var_divby_entry, row_nr, var_status):

            if var_status == "show":
                var_label.grid(row=int(row_nr), column=0, sticky=W, padx=20)
                var_name_entry.grid(row=int(row_nr), column=1, sticky=W)
                var_min_entry.grid(row=int(row_nr), column=1, sticky=W, padx=60)
                var_max_entry.grid(row=int(row_nr), column=1, sticky=W, padx=100)
                var_prec_entry.grid(row=int(row_nr), column=1, sticky=W, padx=140)
                var_divby_entry.grid(row=int(row_nr), column=1, sticky=W, padx=180)
                #var_unit_myCombo.grid(row=int(row_nr), column=0, sticky=E, padx=10)


            else:
                var_label.grid_remove()
                var_name_entry.grid_remove()
                var_min_entry.grid_remove()
                var_max_entry.grid_remove()
                var_prec_entry.grid_remove()
                var_divby_entry.grid_remove()
                # var_unit_myCombo.grid_remove()

    def ff_result_show_or_remove(self, res_label, res_name_entry, res_min_entry, res_max_entry, res_prec_entry, res_tol_entry, res_points_entry, res_formula_entry, row_nr, res_status):

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


        self.var_selected_unit = selected_unit
        self.selected_unit = self.unit_to_ilias_code[self.var_selected_unit]
        return self.selected_unit

    def ff_replace_character_in_xml_file(self, file_path_qti_xml):
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
    def ff_add_image_to_description(self, check_use_img_1, check_use_img_2, check_use_img_3):

        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        # Bild 1 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_1 == 1:
            self.ff_description_img_path_1 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_1 = self.ff_description_img_path_1.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ff_description_img_name_1= self.ff_description_img_path_1[int(self.last_char_index_img_1) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_1 = self.ff_description_img_path_1[-4:]

            self.ff_question_description_img_1_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_1)
            self.ff_question_description_img_1_filename_label.grid(row=0, column=1, sticky=W)

            self.file_image_1 = ImageTk.PhotoImage(Image.open(self.ff_description_img_path_1).resize((100, 100)))
            self.file_image_1_raw = Image.open(self.ff_description_img_path_1)
            self.file_image_1_width, self.file_image_1_height = self.file_image_1_raw.size
            self.file_image_1_label = Label(self.ff_frame_description_picture, image=self.file_image_1)
            self.file_image_1_label.image = self.file_image_1
            self.file_image_1_label.grid(row=0, column=2)


        # Bild 2 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_2 == 1:
            self.ff_description_img_path_2 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_2 = self.ff_description_img_path_2.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ff_description_img_name_2= self.ff_description_img_path_2[int(self.last_char_index_img_2) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_2 = self.ff_description_img_path_2[-4:]

            self.ff_question_description_img_2_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_2)
            self.ff_question_description_img_2_filename_label.grid(row=1, column=1, sticky=W)


            self.file_image_2 = ImageTk.PhotoImage(Image.open(self.ff_description_img_path_2).resize((100, 100)))
            self.file_image_2_raw = Image.open(self.ff_description_img_path_2)
            self.file_image_2_width, self.file_image_2_height = self.file_image_2_raw.size
            self.file_image_2_label = Label(self.ff_frame_description_picture, image=self.file_image_2)
            self.file_image_2_label.image = self.file_image_2
            self.file_image_2_label.grid(row=1, column=2)


        # Bild 3 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_3 == 1:

            self.ff_description_img_path_3 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_3 = self.ff_description_img_path_3.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.ff_description_img_name_3 = self.ff_description_img_path_3[int(self.last_char_index_img_3) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_3 = self.ff_description_img_path_3[-4:]
            self.ff_question_description_img_3_filename_label = Label(self.ff_frame_description_picture, text=self.ff_description_img_name_3)
            self.ff_question_description_img_3_filename_label.grid(row=2, column=1, sticky=W)

            self.file_image_3 = ImageTk.PhotoImage(Image.open(self.ff_description_img_path_3).resize((100, 100)))
            self.file_image_3_raw = Image.open(self.ff_description_img_path_3)
            self.file_image_3_width, self.file_image_3_height = self.file_image_3_raw.size
            self.file_image_3_label = Label(self.ff_frame_description_picture, image=self.file_image_3)
            self.file_image_3_label.image = self.file_image_3
            self.file_image_3_label.grid(row=2, column=2)

    def ff_delete_image_from_description(self, check_use_img_1, check_use_img_2, check_use_img_3):
        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        if self.check_use_img_1 == 0:
            #print("0 in 1")
            self.ff_question_description_img_1_filename_label.grid_remove()
            self.file_image_1_label.grid_remove()
            self.ff_description_img_name_1="EMPTY"

        if self.check_use_img_2 == 0:
            self.ff_question_description_img_2_filename_label.grid_remove()
            self.file_image_2_label.grid_remove()
            self.ff_description_img_name_2="EMPTY"
            #print("0 in 2")
        if self.check_use_img_3 == 0:
            self.ff_question_description_img_3_filename_label.grid_remove()
            self.file_image_3_label.grid_remove()
            self.ff_description_img_name_3 ="EMPTY"
            #print("0 in 3")
    """
    # Wertebereich berechnen für bis zu 4 Variablen
    def ff_replace_symbols_in_formula(self, formula):

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

    def ff_calculate_value_range_from_formula(self, formula):

        self.var1_in_formula = 0
        self.var2_in_formula = 0
        self.var3_in_formula = 0
        self.var4_in_formula = 0
        self.var5_in_formula = 0

        # Number of values per range
        N = 21

        # Functions
        #self.calc_formula1 = "lambda row: " + str(self.calc_formula1) + ","

        self.expression_test = Formelfrage.ff_replace_symbols_in_formula(self, formula)

        if 'a' in self.expression_test:
            #print("$v1 in der Formel")
            self.var1_in_formula = 1

        if 'b' in self.expression_test:
            #print("$v2 in der Formel")
            self.var2_in_formula = 1

        if 'c' in self.expression_test:
            #print("$v3 in der Formel")
            self.var3_in_formula = 1

        if 'd' in self.expression_test:
            #print("$v4 in der Formel")
            self.var4_in_formula = 1

        if 'e' in self.expression_test:
            #print("$v5 in der Formel")
            self.var5_in_formula = 1


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
        if bool(re.search(r'\d', self.var1_min_entry.get()())) == True and bool(re.search(r'\d', self.var1_min_entry.get()())) == True:
            try:
                self.var1_lower, self.var1_upper = int(self.var1_min_entry.get()()), int(self.var1_max_entry.get()())
            except ValueError:
                self.var1_lower, self.var1_upper = float(self.var1_min_entry.get()()), float(self.var1_max_entry.get()())
        else: self.var1_lower, self.var1_upper = 1, 1


        if bool(re.search(r'\d', self.var2_min_entry.get()())) == True and bool(re.search(r'\d', self.var2_min_entry.get()())) == True:
            try:
                self.var2_lower, self.var2_upper = int(self.var2_min_entry.get()()), int(self.var2_max_entry.get()())
            except ValueError:
                self.var2_lower, self.var2_upper = float(self.var2_min_entry.get()()), float(self.var2_max_entry.get()())
        else: self.var2_lower, self.var2_upper = 1, 1


        if bool(re.search(r'\d', self.var3_min_entry.get()())) == True and bool(re.search(r'\d', self.var3_min_entry.get()())) == True:
            try:
                self.var3_lower, self.var3_upper = int(self.var3_min_entry.get()()), int(self.var3_max_entry.get()())
            except ValueError:
                self.var3_lower, self.var3_upper = float(self.var3_min_entry.get()()), float(self.var3_max_entry.get()())
        else: self.var3_lower, self.var3_upper = 1, 1


        if bool(re.search(r'\d', self.var4_min_entry.get()())) == True and bool(re.search(r'\d', self.var4_min_entry.get()())) == True:
            try:
                self.var4_lower, self.var4_upper = int(self.var4_min_entry.get()()), int(self.var4_max_entry.get()())
            except ValueError:
                self.var4_lower, self.var4_upper = float(self.var4_min_entry.get()()), float(self.var4_max_entry.get()())
        else: self.var4_lower, self.var4_upper = 1, 1










        a_lower, a_upper = self.var1_lower, self.var1_upper
        b_lower, b_upper = self.var2_lower, self.var2_upper
        c_lower, c_upper = self.var3_lower, self.var3_upper
        d_lower, d_upper = self.var4_lower, self.var4_upper
        #e_lower, e_upper = self.var5_lower, self.var5_upper


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

        #print(self.var1_in_formula, self.var2_in_formula, self.var3_in_formula, self.var4_in_formula, self.var5_in_formula)
        if self.var1_in_formula == 1 and self.var2_in_formula == 0 and self.var3_in_formula == 0 and self.var4_in_formula == 0 and self.var5_in_formula == 0:
             print("Berechne Formel mit 1 Variablen: ...")
             self.set_nr_of_var_index=['a']
             values = [
                 np.linspace(a_lower, a_upper, N),
             ]

        if self.var1_in_formula == 1 and self.var2_in_formula == 1 and self.var3_in_formula == 0 and self.var4_in_formula == 0 and self.var5_in_formula == 0:
            print("Berechne Formel mit 2 Variablen: ...")
            self.set_nr_of_var_index = ['a', 'b']
            values = [
                np.linspace(a_lower, a_upper, N),
                np.linspace(b_lower, b_upper, N),
            ]

        if self.var1_in_formula == 1 and self.var2_in_formula == 1 and self.var3_in_formula == 1 and self.var4_in_formula == 0 and self.var5_in_formula == 0:
            print("Berechne Formel mit 3 Variablen: ...")
            self.set_nr_of_var_index = ['a', 'b', 'c']
            values = [
                np.linspace(a_lower, a_upper, N),
                np.linspace(b_lower, b_upper, N),
                np.linspace(c_lower, c_upper, N),
            ]

        if self.var1_in_formula == 1 and self.var2_in_formula == 1 and self.var3_in_formula == 1 and self.var4_in_formula == 1 and self.var5_in_formula == 0:
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
    def ff_save_id_to_db(self):
        conn = sqlite3.connect(self.database_formelfrage_path)
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.ff_test_time = "P0Y0M0DT" + self.ff_proc_hours_box.get() + "H" + self.ff_proc_minutes_box.get() + "M" + self.ff_proc_seconds_box.get() + "S"


        # Bild 1
        if self.ff_description_img_name_1!= "EMPTY":
            # read image data in byte format
            with open(self.ff_description_img_path_1, 'rb') as image_file_1:
                self.ff_description_img_data_1 = image_file_1.read()


        else:
            self.ff_description_img_name_1= "EMPTY"
            self.ff_description_img_path_1 = "EMPTY"
            self.ff_description_img_data_1 = "EMPTY"


        # Bild 2
        if self.ff_description_img_name_2!= "EMPTY":
            # read image data in byte format
            with open(self.ff_description_img_path_2, 'rb') as image_file_2:
                self.ff_description_img_data_2 = image_file_2.read()


        else:
            self.ff_description_img_name_2= "EMPTY"
            self.ff_description_img_path_2 = "EMPTY"
            self.ff_description_img_data_2 = "EMPTY"


        # Bild 3
        if self.ff_description_img_name_3 != "EMPTY":

            # read image data in byte format
            with open(self.ff_description_img_path_3, 'rb') as image_file_3:
                self.ff_description_img_data_3 = image_file_3.read()


        else:
            self.ff_description_img_name_3 = "EMPTY"
            self.ff_description_img_path_3 = "EMPTY"
            self.ff_description_img_data_3 = "EMPTY"


        # Insert into Table
        c.execute(
            "INSERT INTO formelfrage_table VALUES ("
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
            ":var11_name, :var11_min, :var11_max, :var11_prec, :var11_divby, :var11_unit, "
            ":var12_name, :var12_min, :var12_max, :var12_prec, :var12_divby, :var12_unit, "
            ":var13_name, :var13_min, :var13_max, :var13_prec, :var13_divby, :var13_unit, "
            ":var14_name, :var14_min, :var14_max, :var14_prec, :var14_divby, :var14_unit, "
            ":var15_name, :var15_min, :var15_max, :var15_prec, :var15_divby, :var15_unit, "
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
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :res_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': self.ff_question_difficulty_entry.get(),
                'question_category': self.ff_question_category_entry.get(),
                'question_type': self.ff_question_type_entry.get(),

                'question_title': self.ff_question_title_entry.get(),
                'question_description_title': self.ff_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.ff_question_description_main_entry.get("1.0", 'end-1c'),

                'res1_formula': self.res1_formula_entry.get(),
                'res2_formula': self.res2_formula_entry.get(),
                'res3_formula': self.res3_formula_entry.get(),
                'res4_formula': self.res4_formula_entry.get(),
                'res5_formula': self.res5_formula_entry.get(),
                'res6_formula': self.res6_formula_entry.get(),
                'res7_formula': self.res7_formula_entry.get(),
                'res8_formula': self.res8_formula_entry.get(),
                'res9_formula': self.res9_formula_entry.get(),
                'res10_formula': self.res10_formula_entry.get(),

                'var1_name': self.var1_name_entry.get(),
                'var1_min': self.var1_min_entry.get(),
                'var1_max': self.var1_max_entry.get(),
                'var1_prec': self.var1_prec_entry.get(),
                'var1_divby': self.var1_divby_entry.get(),
                'var1_unit': "",

                'var2_name': self.var2_name_entry.get(),
                'var2_min': self.var2_min_entry.get(),
                'var2_max': self.var2_max_entry.get(),
                'var2_prec': self.var2_prec_entry.get(),
                'var2_divby': self.var2_divby_entry.get(),
                'var2_unit': "",

                'var3_name': self.var3_name_entry.get(),
                'var3_min': self.var3_min_entry.get(),
                'var3_max': self.var3_max_entry.get(),
                'var3_prec': self.var3_prec_entry.get(),
                'var3_divby': self.var3_divby_entry.get(),
                'var3_unit': "",

                'var4_name': self.var4_name_entry.get(),
                'var4_min': self.var4_min_entry.get(),
                'var4_max': self.var4_max_entry.get(),
                'var4_prec': self.var4_prec_entry.get(),
                'var4_divby': self.var4_divby_entry.get(),
                'var4_unit': "",

                'var5_name': self.var5_name_entry.get(),
                'var5_min': self.var5_min_entry.get(),
                'var5_max': self.var5_max_entry.get(),
                'var5_prec': self.var5_prec_entry.get(),
                'var5_divby': self.var5_divby_entry.get(),
                'var5_unit': "",

                'var6_name': self.var6_name_entry.get(),
                'var6_min': self.var6_min_entry.get(),
                'var6_max': self.var6_max_entry.get(),
                'var6_prec': self.var6_prec_entry.get(),
                'var6_divby': self.var6_divby_entry.get(),
                'var6_unit': "",

                'var7_name': self.var7_name_entry.get(),
                'var7_min': self.var7_min_entry.get(),
                'var7_max': self.var7_max_entry.get(),
                'var7_prec': self.var7_prec_entry.get(),
                'var7_divby': self.var7_divby_entry.get(),
                'var7_unit': "",

                'var8_name': self.var8_name_entry.get(),
                'var8_min': self.var8_min_entry.get(),
                'var8_max': self.var8_max_entry.get(),
                'var8_prec': self.var8_prec_entry.get(),
                'var8_divby': self.var8_divby_entry.get(),
                'var8_unit': "",

                'var9_name': self.var9_name_entry.get(),
                'var9_min': self.var9_min_entry.get(),
                'var9_max': self.var9_max_entry.get(),
                'var9_prec': self.var9_prec_entry.get(),
                'var9_divby': self.var9_divby_entry.get(),
                'var9_unit': "",

                'var10_name': self.var10_name_entry.get(),
                'var10_min': self.var10_min_entry.get(),
                'var10_max': self.var10_max_entry.get(),
                'var10_prec': self.var10_prec_entry.get(),
                'var10_divby': self.var10_divby_entry.get(),
                'var10_unit': "",

                'var11_name': self.var11_name_entry.get(),
                'var11_min': self.var11_min_entry.get(),
                'var11_max': self.var11_max_entry.get(),
                'var11_prec': self.var11_prec_entry.get(),
                'var11_divby': self.var11_divby_entry.get(),
                'var11_unit': "",

                'var12_name': self.var12_name_entry.get(),
                'var12_min': self.var12_min_entry.get(),
                'var12_max': self.var12_max_entry.get(),
                'var12_prec': self.var12_prec_entry.get(),
                'var12_divby': self.var12_divby_entry.get(),
                'var12_unit': "",

                'var13_name': self.var13_name_entry.get(),
                'var13_min': self.var13_min_entry.get(),
                'var13_max': self.var13_max_entry.get(),
                'var13_prec': self.var13_prec_entry.get(),
                'var13_divby': self.var13_divby_entry.get(),
                'var13_unit': "",

                'var14_name': self.var14_name_entry.get(),
                'var14_min': self.var14_min_entry.get(),
                'var14_max': self.var14_max_entry.get(),
                'var14_prec': self.var14_prec_entry.get(),
                'var14_divby': self.var14_divby_entry.get(),
                'var14_unit': "",

                'var15_name': self.var15_name_entry.get(),
                'var15_min': self.var15_min_entry.get(),
                'var15_max': self.var15_max_entry.get(),
                'var15_prec': self.var15_prec_entry.get(),
                'var15_divby': self.var15_divby_entry.get(),
                'var15_unit': "",


                'res1_name': self.res1_name_entry.get(),
                'res1_min': self.res1_min_entry.get(),
                'res1_max': self.res1_max_entry.get(),
                'res1_prec': self.res1_prec_entry.get(),
                'res1_tol': self.res1_tol_entry.get(),
                'res1_points': self.res1_points_entry.get(),
                'res1_unit': "",

                'res2_name': self.res2_name_entry.get(),
                'res2_min': self.res2_min_entry.get(),
                'res2_max': self.res2_max_entry.get(),
                'res2_prec': self.res2_prec_entry.get(),
                'res2_tol': self.res2_tol_entry.get(),
                'res2_points': self.res2_points_entry.get(),
                'res2_unit': "",

                'res3_name': self.res3_name_entry.get(),
                'res3_min': self.res3_min_entry.get(),
                'res3_max': self.res3_max_entry.get(),
                'res3_prec': self.res3_prec_entry.get(),
                'res3_tol': self.res3_tol_entry.get(),
                'res3_points': self.res3_points_entry.get(),
                'res3_unit': "",

                'res4_name': self.res4_name_entry.get(),
                'res4_min': self.res4_min_entry.get(),
                'res4_max': self.res4_max_entry.get(),
                'res4_prec': self.res4_prec_entry.get(),
                'res4_tol': self.res4_tol_entry.get(),
                'res4_points': self.res4_points_entry.get(),
                'res4_unit': "",

                'res5_name': self.res5_name_entry.get(),
                'res5_min': self.res5_min_entry.get(),
                'res5_max': self.res5_max_entry.get(),
                'res5_prec': self.res5_prec_entry.get(),
                'res5_tol': self.res5_tol_entry.get(),
                'res5_points': self.res5_points_entry.get(),
                'res5_unit': "",

                'res6_name': self.res6_name_entry.get(),
                'res6_min': self.res6_min_entry.get(),
                'res6_max': self.res6_max_entry.get(),
                'res6_prec': self.res6_prec_entry.get(),
                'res6_tol': self.res6_tol_entry.get(),
                'res6_points': self.res6_points_entry.get(),
                'res6_unit': "",

                'res7_name': self.res7_name_entry.get(),
                'res7_min': self.res7_min_entry.get(),
                'res7_max': self.res7_max_entry.get(),
                'res7_prec': self.res7_prec_entry.get(),
                'res7_tol': self.res7_tol_entry.get(),
                'res7_points': self.res7_points_entry.get(),
                'res7_unit': "",

                'res8_name': self.res8_name_entry.get(),

                'res8_min': self.res8_min_entry.get(),
                'res8_max': self.res8_max_entry.get(),
                'res8_prec': self.res8_prec_entry.get(),
                'res8_tol': self.res8_tol_entry.get(),
                'res8_points': self.res8_points_entry.get(),
                'res8_unit': "",

                'res9_name': self.res9_name_entry.get(),
                'res9_min': self.res9_min_entry.get(),
                'res9_max': self.res9_max_entry.get(),
                'res9_prec': self.res9_prec_entry.get(),
                'res9_tol': self.res9_tol_entry.get(),
                'res9_points': self.res9_points_entry.get(),
                'res9_unit': "",

                'res10_name': self.res10_name_entry.get(),
                'res10_min': self.res10_min_entry.get(),
                'res10_max': self.res10_max_entry.get(),
                'res10_prec': self.res10_prec_entry.get(),
                'res10_tol': self.res10_tol_entry.get(),
                'res10_points': self.res10_points_entry.get(),
                'res10_unit': "",

                'description_img_name_1': self.ff_description_img_name_1,
                'description_img_data_1': self.ff_description_img_data_1,
                'description_img_path_1': self.ff_description_img_path_1,

                'description_img_name_2': self.ff_description_img_name_2,
                'description_img_data_2': self.ff_description_img_data_2,
                'description_img_path_2': self.ff_description_img_path_2,

                'description_img_name_3': self.ff_description_img_name_3,
                'description_img_data_3': self.ff_description_img_data_3,
                'description_img_path_3': self.ff_description_img_path_3,

                'test_time': self.ff_test_time,
                'var_number': self.ff_numbers_of_answers_box.get(),
                'res_number': self.ff_numbers_of_results_box.get(),
                'question_pool_tag': self.ff_question_pool_tag_entry.get(),
                'question_author': self.ff_question_author_entry.get()
            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die Formelfrage-Datenbank --> Fragentitel: " + str(self.ff_question_title_entry.get()))

    def ff_load_id_from_db(self, entry_to_index_dict):
        self.ff_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_formelfrage_path)
        c = conn.cursor()
        record_id = self.ff_load_box.get()
        c.execute("SELECT * FROM formelfrage_table WHERE oid =" + record_id)
        ff_db_records = c.fetchall()


        Formelfrage.ff_clear_GUI(self)


        for ff_db_record in ff_db_records:
            self.ff_question_difficulty_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_difficulty']] )
            self.ff_question_category_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_category']])

            self.ff_question_type_entry.delete(0, END)
            self.ff_question_type_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_type']])

            self.ff_question_title_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_title']])
            self.ff_question_description_title_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_description_title']])
            self.ff_question_description_main_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['question_description_main']])

            self.res1_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_formula']])
            self.res2_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_formula']])
            self.res3_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_formula']])
            self.res4_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_formula']])
            self.res5_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_formula']])
            self.res6_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_formula']])
            self.res7_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_formula']])
            self.res8_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_formula']])
            self.res9_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_formula']])
            self.res10_formula_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_formula']])

            self.var1_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_name']])
            self.var1_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_min']])
            self.var1_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_max']])
            self.var1_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_prec']])
            self.var1_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var1_divby']])


            self.var2_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_name']])
            self.var2_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_min']])
            self.var2_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_max']])
            self.var2_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_prec']])
            self.var2_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var2_divby']])


            self.var3_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_name']])
            self.var3_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_min']])
            self.var3_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_max']])
            self.var3_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_prec']])
            self.var3_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var3_divby']])


            self.var4_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_name']])
            self.var4_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_min']])
            self.var4_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_max']])
            self.var4_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_prec']])
            self.var4_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var4_divby']])


            self.var5_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_name']])
            self.var5_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_min']])
            self.var5_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_max']])
            self.var5_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_prec']])
            self.var5_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var5_divby']])


            self.var6_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_name']])
            self.var6_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_min']])
            self.var6_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_max']])
            self.var6_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_prec']])
            self.var6_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var6_divby']])


            self.var7_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_name']])
            self.var7_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_min']])
            self.var7_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_max']])
            self.var7_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_prec']])
            self.var7_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var7_divby']])


            self.var8_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_name']])
            self.var8_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_min']])
            self.var8_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_max']])
            self.var8_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_prec']])
            self.var8_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var8_divby']])


            self.var9_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_name']])
            self.var9_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_min']])
            self.var9_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_max']])
            self.var9_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_prec']])
            self.var9_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var9_divby']])


            self.var10_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_name']])
            self.var10_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_min']])
            self.var10_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_max']])
            self.var10_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_prec']])
            self.var10_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var10_divby']])

            self.var11_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_name']])
            self.var11_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_min']])
            self.var11_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_max']])
            self.var11_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_prec']])
            self.var11_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var11_divby']])

            self.var12_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_name']])
            self.var12_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_min']])
            self.var12_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_max']])
            self.var12_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_prec']])
            self.var12_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var12_divby']])

            self.var13_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_name']])
            self.var13_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_min']])
            self.var13_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_max']])
            self.var13_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_prec']])
            self.var13_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var13_divby']])

            self.var14_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_name']])
            self.var14_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_min']])
            self.var14_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_max']])
            self.var14_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_prec']])
            self.var14_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var14_divby']])

            self.var15_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_name']])
            self.var15_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_min']])
            self.var15_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_max']])
            self.var15_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_prec']])
            self.var15_divby_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['var15_divby']])


            self.res1_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_name']])
            self.res1_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_min']])
            self.res1_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_max']])
            self.res1_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_prec']])
            self.res1_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_tol']])
            self.res1_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res1_points']])


            self.res2_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_name']])
            self.res2_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_min']])
            self.res2_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_max']])
            self.res2_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_prec']])
            self.res2_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_tol']])
            self.res2_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res2_points']])


            self.res3_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_name']])
            self.res3_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_min']])
            self.res3_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_max']])
            self.res3_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_prec']])
            self.res3_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_tol']])
            self.res3_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res3_points']])


            self.res4_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_name']])
            self.res4_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_min']])
            self.res4_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_max']])
            self.res4_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_prec']])
            self.res4_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_tol']])
            self.res4_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res4_points']])


            self.res5_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_name']])
            self.res5_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_min']])
            self.res5_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_max']])
            self.res5_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_prec']])
            self.res5_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_tol']])
            self.res5_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res5_points']])


            self.res6_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_name']])
            self.res6_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_min']])
            self.res6_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_max']])
            self.res6_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_prec']])
            self.res6_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_tol']])
            self.res6_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res6_points']])


            self.res7_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_name']])
            self.res7_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_min']])
            self.res7_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_max']])
            self.res7_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_prec']])
            self.res7_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_tol']])
            self.res7_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res7_points']])


            self.res8_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_name']])
            self.res8_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_min']])
            self.res8_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_max']])
            self.res8_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_prec']])
            self.res8_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_tol']])
            self.res8_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res8_points']])


            self.res9_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_name']])
            self.res9_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_min']])
            self.res9_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_max']])
            self.res9_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_prec']])
            self.res9_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_tol']])
            self.res9_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res9_points']])


            self.res10_name_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_name']])
            self.res10_min_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_min']])
            self.res10_max_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_max']])
            self.res10_prec_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_prec']])
            self.res10_tol_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_tol']])
            self.res10_points_entry.insert(END, ff_db_record[self.ff_db_entry_to_index_dict['res10_points']])


        conn.commit()
        conn.close()


        if self.ff_var_highlight_question_text.get() == 1:
            print("Frage wird MIT Text-Formatierung geladen. --> Fragen-ID: " + str(self.ff_load_box.get()))
            test_generator_modul_taxonomie_und_textformatierung.Textformatierung.reallocate_text(self, self.ff_question_description_main_entry)

        else:
            print("Frage wird OHNE Text-Formatierung geladen. --> Fragen-ID: " + str(self.ff_load_box.get()))

    def ff_edit_id_from_db(self):


        conn = sqlite3.connect(self.database_formelfrage_path)
        c = conn.cursor()
        record_id = self.ff_load_box.get()

        # format of duration P0Y0M0DT0H30M0S
        self.ff_test_time = "P0Y0M0DT" + self.ff_proc_hours_box.get() + "H" + self.ff_proc_minutes_box.get() + "M" + self.ff_proc_seconds_box.get() + "S"


        if self.ff_picture_name != "EMPTY":
            # read image data in byte format
            with open(self.ff_picture_name, 'rb') as image_file:
                self.ff_picture_data = image_file.read()


        else:
            self.ff_picture_name = "EMPTY"
            self.ff_picture_data = "EMPTY"

        c.execute("""UPDATE formelfrage_table SET
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
            
            var11_name = :var11_name,
            var11_min = :var11_min,
            var11_max = :var11_max,
            var11_prec = :var11_prec,
            var11_divby = :var11_divby,
            var11_unit = :var11_unit,
            
            var12_name = :var12_name,
            var12_min = :var12_min,
            var12_max = :var12_max,
            var12_prec = :var12_prec,
            var12_divby = :var12_divby,
            var12_unit = :var12_unit,
            
            var13_name = :var13_name,
            var13_min = :var13_min,
            var13_max = :var13_max,
            var13_prec = :var13_prec,
            var13_divby = :var13_divby,
            var13_unit = :var13_unit,
            
            var14_name = :var14_name,
            var14_min = :var14_min,
            var14_max = :var14_max,
            var14_prec = :var14_prec,
            var14_divby = :var14_divby,
            var14_unit = :var14_unit,
            
            var15_name = :var15_name,
            var15_min = :var15_min,
            var15_max = :var15_max,
            var15_prec = :var15_prec,
            var15_divby = :var15_divby,
            var15_unit = :var15_unit,
            
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
                {'question_difficulty': self.ff_question_difficulty_entry.get(),
                 'question_category': self.ff_question_category_entry.get(),
                 'question_type': self.ff_question_type_entry.get(),

                 'question_title': self.ff_question_title_entry.get(),
                 'question_description_title': self.ff_question_description_title_entry.get(),
                 'question_description_main': self.ff_question_description_main_entry.get("1.0", 'end-1c'),

                 'res1_formula': self.res1_formula_entry.get(),
                 'res2_formula': self.res2_formula_entry.get(),
                 'res3_formula': self.res3_formula_entry.get(),
                 'res4_formula': self.res4_formula_entry.get(),
                 'res5_formula': self.res5_formula_entry.get(),
                 'res6_formula': self.res6_formula_entry.get(),
                 'res7_formula': self.res7_formula_entry.get(),
                 'res8_formula': self.res8_formula_entry.get(),
                 'res9_formula': self.res9_formula_entry.get(),
                 'res10_formula': self.res10_formula_entry.get(),

                 'var1_name': self.var1_name_entry.get(),
                 'var1_min': self.var1_min_entry.get(),
                 'var1_max': self.var1_max_entry.get(),
                 'var1_prec': self.var1_prec_entry.get(),
                 'var1_divby': self.var1_divby_entry.get(),
                 'var1_unit': "",

                 'var2_name': self.var2_name_entry.get(),
                 'var2_min': self.var2_min_entry.get(),
                 'var2_max': self.var2_max_entry.get(),
                 'var2_prec': self.var2_prec_entry.get(),
                 'var2_divby': self.var2_divby_entry.get(),
                 'var2_unit': "",

                 'var3_name': self.var3_name_entry.get(),
                 'var3_min': self.var3_min_entry.get(),
                 'var3_max': self.var3_max_entry.get(),
                 'var3_prec': self.var3_prec_entry.get(),
                 'var3_divby': self.var3_divby_entry.get(),
                 'var3_unit': "",

                 'var4_name': self.var4_name_entry.get(),
                 'var4_min': self.var4_min_entry.get(),
                 'var4_max': self.var4_max_entry.get(),
                 'var4_prec': self.var4_prec_entry.get(),
                 'var4_divby': self.var4_divby_entry.get(),
                 'var4_unit': "",

                 'var5_name': self.var5_name_entry.get(),
                 'var5_min': self.var5_min_entry.get(),
                 'var5_max': self.var5_max_entry.get(),
                 'var5_prec': self.var5_prec_entry.get(),
                 'var5_divby': self.var5_divby_entry.get(),
                 'var5_unit': "",

                 'var6_name': self.var6_name_entry.get(),
                 'var6_min': self.var6_min_entry.get(),
                 'var6_max': self.var6_max_entry.get(),
                 'var6_prec': self.var6_prec_entry.get(),
                 'var6_divby': self.var6_divby_entry.get(),
                 'var6_unit': "",

                 'var7_name': self.var7_name_entry.get(),
                 'var7_min': self.var7_min_entry.get(),
                 'var7_max': self.var7_max_entry.get(),
                 'var7_prec': self.var7_prec_entry.get(),
                 'var7_divby': self.var7_divby_entry.get(),
                 'var7_unit': "",

                 'var8_name': self.var8_name_entry.get(),
                 'var8_min': self.var8_min_entry.get(),
                 'var8_max': self.var8_max_entry.get(),
                 'var8_prec': self.var8_prec_entry.get(),
                 'var8_divby': self.var8_divby_entry.get(),
                 'var8_unit': "",

                 'var9_name': self.var9_name_entry.get(),
                 'var9_min': self.var9_min_entry.get(),
                 'var9_max': self.var9_max_entry.get(),
                 'var9_prec': self.var9_prec_entry.get(),
                 'var9_divby': self.var9_divby_entry.get(),
                 'var9_unit': "",

                 'var10_name': self.var10_name_entry.get(),
                 'var10_min': self.var10_min_entry.get(),
                 'var10_max': self.var10_max_entry.get(),
                 'var10_prec': self.var10_prec_entry.get(),
                 'var10_divby': self.var10_divby_entry.get(),
                 'var10_unit': "",

                 'res1_name': self.res1_name_entry.get(),
                 'res1_min': self.res1_min_entry.get(),
                 'res1_max': self.res1_max_entry.get(),
                 'res1_prec': self.res1_prec_entry.get(),
                 'res1_tol': self.res1_tol_entry.get(),
                 'res1_points': self.res1_points_entry.get(),
                 'res1_unit': "",

                 'res2_name': self.res2_name_entry.get(),
                 'res2_min': self.res2_min_entry.get(),
                 'res2_max': self.res2_max_entry.get(),
                 'res2_prec': self.res2_prec_entry.get(),
                 'res2_tol': self.res2_tol_entry.get(),
                 'res2_points': self.res2_points_entry.get(),
                 'res2_unit': "",

                 'res3_name': self.res3_name_entry.get(),
                 'res3_min': self.res3_min_entry.get(),
                 'res3_max': self.res3_max_entry.get(),
                 'res3_prec': self.res3_prec_entry.get(),
                 'res3_tol': self.res3_tol_entry.get(),
                 'res3_points': self.res3_points_entry.get(),
                 'res3_unit': "",

                 'res4_name': self.res4_name_entry.get(),
                 'res4_min': self.res4_min_entry.get(),
                 'res4_max': self.res4_max_entry.get(),
                 'res4_prec': self.res4_prec_entry.get(),
                 'res4_tol': self.res4_tol_entry.get(),
                 'res4_points': self.res4_points_entry.get(),
                 'res4_unit': "",

                 'res5_name': self.res5_name_entry.get(),
                 'res5_min': self.res5_min_entry.get(),
                 'res5_max': self.res5_max_entry.get(),
                 'res5_prec': self.res5_prec_entry.get(),
                 'res5_tol': self.res5_tol_entry.get(),
                 'res5_points': self.res5_points_entry.get(),
                 'res5_unit': "",

                 'res6_name': self.res6_name_entry.get(),
                 'res6_min': self.res6_min_entry.get(),
                 'res6_max': self.res6_max_entry.get(),
                 'res6_prec': self.res6_prec_entry.get(),
                 'res6_tol': self.res6_tol_entry.get(),
                 'res6_points': self.res6_points_entry.get(),
                 'res6_unit': "",

                 'res7_name': self.res7_name_entry.get(),
                 'res7_min': self.res7_min_entry.get(),
                 'res7_max': self.res7_max_entry.get(),
                 'res7_prec': self.res7_prec_entry.get(),
                 'res7_tol': self.res7_tol_entry.get(),
                 'res7_points': self.res7_points_entry.get(),
                 'res7_unit': "",

                 'res8_name': self.res8_name_entry.get(),
                 'res8_min': self.res8_min_entry.get(),
                 'res8_max': self.res8_max_entry.get(),
                 'res8_prec': self.res8_prec_entry.get(),
                 'res8_tol': self.res8_tol_entry.get(),
                 'res8_points': self.res8_points_entry.get(),
                 'res8_unit': "",

                 'res9_name': self.res9_name_entry.get(),
                 'res9_min': self.res9_min_entry.get(),
                 'res9_max': self.res9_max_entry.get(),
                 'res9_prec': self.res9_prec_entry.get(),
                 'res9_tol': self.res9_tol_entry.get(),
                 'res9_points': self.res9_points_entry.get(),
                 'res9_unit': "",

                 'res10_name': self.res10_name_entry.get(),
                 'res10_min': self.res10_min_entry.get(),
                 'res10_max': self.res10_max_entry.get(),
                 'res10_prec': self.res10_prec_entry.get(),
                 'res10_tol': self.res10_tol_entry.get(),
                 'res10_points': self.res10_points_entry.get(),
                 'res10_unit': "",

                 'description_img_name_1': self.ff_description_img_name_1,
                 'description_img_data_1': self.ff_description_img_data_1,
                 'description_img_path_1': self.ff_description_img_path_1,

                 'description_img_name_2': self.ff_description_img_name_2,
                 'description_img_data_2': self.ff_description_img_data_2,
                 'description_img_path_2': self.ff_description_img_path_2,

                 'description_img_name_3': self.ff_description_img_name_3,
                 'description_img_data_3': self.ff_description_img_data_3,
                 'description_img_path_3': self.ff_description_img_path_3,

                 'test_time': self.ff_test_time,
                 'question_pool_tag': self.ff_question_pool_tag_entry.get(),
                 'question_author': self.ff_question_author_entry.get(),
                 'oid': record_id
                 })

        conn.commit()
        conn.close()

        print("Frage mit ID: '" + record_id + "' editiert")

    def ff_delete_id_from_db(self):

        self.ff_delete_box_id = ""
        self.ff_delete_box_id = self.ff_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.ff_delete_box_id, "formelfrage", self.ff_var_delete_all.get(), self.project_root_path, self.ff_db_entry_to_index_dict, self.database_formelfrage_path, "formelfrage_db.db", "formelfrage_table", "Formelfrage_DB_export_file.xlsx", "Formelfrage - Database")
        """
        self.sc_delete_box.delete(0, END)
        
        self.ff_delete_mult = self.ff_delete_box.get()
        self.ff_delete_mult_start = self.ff_delete_mult.split('-')[0]

        self.delete_box_split = self.ff_delete_box_id.split(",")
        self.delete_index_wrong = False

        for i in range(len(self.delete_box_split)):
             if "1" in self.delete_box_split[i] and len(self.delete_box_split[i])==1:
                 print("delete TRUE")
                 self.delete_index_wrong = True

        if self.ff_delete_box_id == "1":
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        elif self.delete_index_wrong == True:
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        elif self.ff_delete_mult_start == "1":
            print("ID \"1\" kann nicht gelöscht werden! Eintrag ist Datenbank-Vorlage!")

        else:

            # Variablen
            self.ff_delete_list = []
            self.ff_delete_all_list = []
            self.ff_delete_index = 0



            # Zur Datenbank connecten
            conn = sqlite3.connect('ilias_formelfrage_db.db')
            c = conn.cursor()

            # Wenn in das Eingabefeld Kommagetrenne ID's eingetragen wurden, dann ->
            # den String nehmen, nach Komma trennen "," und einzelne DB-ID's löschen
            self.ff_delete_list = self.ff_delete_box.get().split(",")


            # Wenn in das Eingabefeld z.B. "1-5" eingetragen wurde, dann ->
            # den String nehmen, und nach Bindestrick "-" splitten
            # ID in Fach 1 = Start, ID in Fach [-1] (letztes Fach)

            self.ff_delete_mult = self.ff_delete_box.get()
            self.ff_delete_mult_start = self.ff_delete_mult.split('-')[0]
            self.ff_delete_mult_end = self.ff_delete_mult.split('-')[-1]
            self.ff_delete_mult_symbol = "-" in self.ff_delete_mult


            if self.ff_var_delete_all.get() == 1:
                now = datetime.now()  # current date and time
                date_time = now.strftime("%d.%m.%Y_%Hh-%Mm")
                actual_time = str(date_time)
                #Database.sql_db_to_excel_export(self, "BACKUP_Export_from_SQL__" + str(actual_time) + ".xlsx")
                c.execute("SELECT *, oid FROM formelfrage_table")
                records = c.fetchall()
                for record in records:
                    self.ff_delete_all_list.append(int(record[len(record) - 1]))

                # Der Eintrag mit ID "1" dient als Vorlage für die Datenbank
                for i in range(len(self.ff_delete_all_list)):
                    if self.ff_delete_all_list[i] == 1:
                        self.ff_delete_index = i

                self.ff_delete_all_list.pop(self.ff_delete_index)


                for x in range(len(self.ff_delete_all_list)):
                    c.execute("DELETE from formelfrage_table WHERE oid= " + str(self.ff_delete_all_list[x]))
                print("All Entries removed!")


            elif self.ff_delete_mult_symbol == True:
                for x in range(int(self.ff_delete_mult_start), int(self.ff_delete_mult_end)+1):

                    c.execute("DELETE from formelfrage_table WHERE oid= " + str(x))
                    print("Entry with ID " + str(x) + " removed!")


            else:
                for x in range(len(self.ff_delete_list)):
                    c.execute("DELETE from formelfrage_table WHERE oid= " + str(self.ff_delete_list[x]))
                    print("Entry with ID " + str(self.ff_delete_list[x]) + " removed!")

            self.ff_delete_box.delete(0, END)

            conn.commit()
            conn.close()
        """

    def ff_clear_GUI(self):
        self.ff_question_difficulty_entry.delete(0, END)
        self.ff_question_category_entry.delete(0, END)
        #self.ff_question_type_entry.delete(0, END)

        self.ff_question_title_entry.delete(0, END)
        self.ff_question_description_title_entry.delete(0, END)
        self.ff_question_description_main_entry.delete('1.0', 'end-1c')

        self.res1_formula_entry.delete(0, END)
        self.res2_formula_entry.delete(0, END)
        self.res3_formula_entry.delete(0, END)
        self.res4_formula_entry.delete(0, END)
        self.res5_formula_entry.delete(0, END)
        self.res6_formula_entry.delete(0, END)
        self.res7_formula_entry.delete(0, END)
        self.res8_formula_entry.delete(0, END)
        self.res9_formula_entry.delete(0, END)
        self.res10_formula_entry.delete(0, END)

        self.var1_name_entry.delete(0, END)
        self.var1_min_entry.delete(0, END)
        self.var1_max_entry.delete(0, END)
        self.var1_prec_entry.delete(0, END)
        self.var1_divby_entry.delete(0, END)

        self.var2_name_entry.delete(0, END)
        self.var2_min_entry.delete(0, END)
        self.var2_max_entry.delete(0, END)
        self.var2_prec_entry.delete(0, END)
        self.var2_divby_entry.delete(0, END)

        self.var3_name_entry.delete(0, END)
        self.var3_min_entry.delete(0, END)
        self.var3_max_entry.delete(0, END)
        self.var3_prec_entry.delete(0, END)
        self.var3_divby_entry.delete(0, END)

        self.var4_name_entry.delete(0, END)
        self.var4_min_entry.delete(0, END)
        self.var4_max_entry.delete(0, END)
        self.var4_prec_entry.delete(0, END)
        self.var4_divby_entry.delete(0, END)

        self.var5_name_entry.delete(0, END)
        self.var5_min_entry.delete(0, END)
        self.var5_max_entry.delete(0, END)
        self.var5_prec_entry.delete(0, END)
        self.var5_divby_entry.delete(0, END)

        self.var6_name_entry.delete(0, END)
        self.var6_min_entry.delete(0, END)
        self.var6_max_entry.delete(0, END)
        self.var6_prec_entry.delete(0, END)
        self.var6_divby_entry.delete(0, END)

        self.var7_name_entry.delete(0, END)
        self.var7_min_entry.delete(0, END)
        self.var7_max_entry.delete(0, END)
        self.var7_prec_entry.delete(0, END)
        self.var7_divby_entry.delete(0, END)

        self.var8_name_entry.delete(0, END)
        self.var8_min_entry.delete(0, END)
        self.var8_max_entry.delete(0, END)
        self.var8_prec_entry.delete(0, END)
        self.var8_divby_entry.delete(0, END)

        self.var9_name_entry.delete(0, END)
        self.var9_min_entry.delete(0, END)
        self.var9_max_entry.delete(0, END)
        self.var9_prec_entry.delete(0, END)
        self.var9_divby_entry.delete(0, END)

        self.var10_name_entry.delete(0, END)
        self.var10_min_entry.delete(0, END)
        self.var10_max_entry.delete(0, END)
        self.var10_prec_entry.delete(0, END)
        self.var10_divby_entry.delete(0, END)

        self.var11_name_entry.delete(0, END)
        self.var11_min_entry.delete(0, END)
        self.var11_max_entry.delete(0, END)
        self.var11_prec_entry.delete(0, END)
        self.var11_divby_entry.delete(0, END)

        self.var12_name_entry.delete(0, END)
        self.var12_min_entry.delete(0, END)
        self.var12_max_entry.delete(0, END)
        self.var12_prec_entry.delete(0, END)
        self.var12_divby_entry.delete(0, END)

        self.var13_name_entry.delete(0, END)
        self.var13_min_entry.delete(0, END)
        self.var13_max_entry.delete(0, END)
        self.var13_prec_entry.delete(0, END)
        self.var13_divby_entry.delete(0, END)

        self.var14_name_entry.delete(0, END)
        self.var14_min_entry.delete(0, END)
        self.var14_max_entry.delete(0, END)
        self.var14_prec_entry.delete(0, END)
        self.var14_divby_entry.delete(0, END)

        self.var15_name_entry.delete(0, END)
        self.var15_min_entry.delete(0, END)
        self.var15_max_entry.delete(0, END)
        self.var15_prec_entry.delete(0, END)
        self.var15_divby_entry.delete(0, END)

        self.res1_name_entry.delete(0, END)
        self.res1_min_entry.delete(0, END)
        self.res1_max_entry.delete(0, END)
        self.res1_prec_entry.delete(0, END)
        self.res1_tol_entry.delete(0, END)
        self.res1_points_entry.delete(0, END)

        self.res2_name_entry.delete(0, END)
        self.res2_min_entry.delete(0, END)
        self.res2_max_entry.delete(0, END)
        self.res2_prec_entry.delete(0, END)
        self.res2_tol_entry.delete(0, END)
        self.res2_points_entry.delete(0, END)

        self.res3_name_entry.delete(0, END)
        self.res3_min_entry.delete(0, END)
        self.res3_max_entry.delete(0, END)
        self.res3_prec_entry.delete(0, END)
        self.res3_tol_entry.delete(0, END)
        self.res3_points_entry.delete(0, END)

        self.res4_name_entry.delete(0, END)
        self.res4_min_entry.delete(0, END)
        self.res4_max_entry.delete(0, END)
        self.res4_prec_entry.delete(0, END)
        self.res4_tol_entry.delete(0, END)
        self.res4_points_entry.delete(0, END)

        self.res5_name_entry.delete(0, END)
        self.res5_min_entry.delete(0, END)
        self.res5_max_entry.delete(0, END)
        self.res5_prec_entry.delete(0, END)
        self.res5_tol_entry.delete(0, END)
        self.res5_points_entry.delete(0, END)

        self.res6_name_entry.delete(0, END)
        self.res6_min_entry.delete(0, END)
        self.res6_max_entry.delete(0, END)
        self.res6_prec_entry.delete(0, END)
        self.res6_tol_entry.delete(0, END)
        self.res6_points_entry.delete(0, END)

        self.res7_name_entry.delete(0, END)
        self.res7_min_entry.delete(0, END)
        self.res7_max_entry.delete(0, END)
        self.res7_prec_entry.delete(0, END)
        self.res7_tol_entry.delete(0, END)
        self.res7_points_entry.delete(0, END)

        self.res8_name_entry.delete(0, END)
        self.res8_min_entry.delete(0, END)
        self.res8_max_entry.delete(0, END)
        self.res8_prec_entry.delete(0, END)
        self.res8_tol_entry.delete(0, END)
        self.res8_points_entry.delete(0, END)

        self.res9_name_entry.delete(0, END)
        self.res9_min_entry.delete(0, END)
        self.res9_max_entry.delete(0, END)
        self.res9_prec_entry.delete(0, END)
        self.res9_tol_entry.delete(0, END)
        self.res9_points_entry.delete(0, END)

        self.res10_name_entry.delete(0, END)
        self.res10_min_entry.delete(0, END)
        self.res10_max_entry.delete(0, END)
        self.res10_prec_entry.delete(0, END)
        self.res10_tol_entry.delete(0, END)
        self.res10_points_entry.delete(0, END)


class Create_Formelfrage_Questions(Formelfrage):


    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):

        self.ff_db_entry_to_index_dict = db_entry_to_index_dict
        self.ff_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path
        self.formelfrage_pool_qpl_file_path_output = xml_qpl_output_file_path
        self.ff_mytree = ET.parse(xml_read_qti_template_path)
        self.ff_myroot = self.ff_mytree.getroot()
        self.ff_question_type_test_or_pool = question_type
        self.formelfrage_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)

        self.all_entries_from_db_list = []
        self.number_of_entrys = []

        self.question_pool_id_list = []
        self.question_title_list = []

        self.ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.ff_file_max_id = max_id
        self.taxonomy_file_question_pool = taxonomy_file_question_pool
        self.ilias_id_pool_qti_xml = max_id_pool_qti_xml


        print("\n")


        if self.ff_question_type_test_or_pool == "question_test":
            print("FORMELFRAGE: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("FORMELFRAGE: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))


        # Mit FF_Datenbank verknüpfen
        connect_ff_db = sqlite3.connect(self.database_formelfrage_path)
        cursor = connect_ff_db.cursor()


        # Prüfen ob alle EInträge generiert werden sollen (checkbox gesetzt)
        if self.ff_var_create_question_pool_all_check.get() == 1:
            conn = sqlite3.connect(self.database_formelfrage_path)
            c = conn.cursor()
            c.execute("SELECT *, oid FROM formelfrage_table")

            ff_db_records = c.fetchall()

            for ff_db_record in ff_db_records:
                self.all_entries_from_db_list.append(int(ff_db_record[len(ff_db_record) - 1]))

            self.string_temp = ','.join(map(str, self.all_entries_from_db_list))
            self.ff_test_entry_splitted = self.string_temp.split(",")

            # Eintrag mit ID "1" entspricht der Vorlage und soll nicht mit erstellt werden
            self.ff_test_entry_splitted.pop(0)


        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM formelfrage_table")
        ff_db_records = cursor.fetchall()

        for i in range(len(self.ff_test_entry_splitted)):
            for ff_db_record in ff_db_records:
                if str(ff_db_record[len(ff_db_record) - 1]) == self.ff_test_entry_splitted[i]:
                    for t in range(len(ff_db_record)):
                        if ff_db_record[self.ff_db_entry_to_index_dict['question_type']].lower() == "formelfrage" or ff_db_record[self.ff_db_entry_to_index_dict['question_type']].lower() == "formel frage":
                            self.ff_question_difficulty                                                = ff_db_record[self.ff_db_entry_to_index_dict['question_difficulty']]
                            self.ff_question_category                                                  = ff_db_record[self.ff_db_entry_to_index_dict['question_category']]
                            self.ff_question_type                                                      = ff_db_record[self.ff_db_entry_to_index_dict['question_type']]
                            self.ff_question_title                                                     = ff_db_record[self.ff_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.ff_question_description_title                                         = ff_db_record[self.ff_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.ff_question_description_main                                          = ff_db_record[self.ff_db_entry_to_index_dict['question_description_main']]
                            self.ff_res1_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res1_formula']]
                            self.ff_res2_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res2_formula']]
                            self.ff_res3_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res3_formula']]
                            self.ff_res4_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res4_formula']]
                            self.ff_res5_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res5_formula']]
                            self.ff_res6_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res6_formula']]
                            self.ff_res7_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res7_formula']]
                            self.ff_res8_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res8_formula']]
                            self.ff_res9_formula                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res9_formula']]
                            self.ff_res10_formula                                                      = ff_db_record[self.ff_db_entry_to_index_dict['res10_formula']]

                            self.ff_var1_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_name']]
                            self.ff_var1_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var1_min']]
                            self.ff_var1_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var1_max']]
                            self.ff_var1_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_prec']]
                            self.ff_var1_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var1_divby']]
                            self.ff_var1_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var1_unit']]

                            self.ff_var2_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_name']]
                            self.ff_var2_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var2_min']]
                            self.ff_var2_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var2_max']]
                            self.ff_var2_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_prec']]
                            self.ff_var2_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var2_divby']]
                            self.ff_var2_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var2_unit']]

                            self.ff_var3_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_name']]
                            self.ff_var3_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var3_min']]
                            self.ff_var3_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var3_max']]
                            self.ff_var3_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_prec']]
                            self.ff_var3_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var3_divby']]
                            self.ff_var3_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var3_unit']]

                            self.ff_var4_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_name']]
                            self.ff_var4_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var4_min']]
                            self.ff_var4_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var4_max']]
                            self.ff_var4_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_prec']]
                            self.ff_var4_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var4_divby']]
                            self.ff_var4_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var4_unit']]

                            self.ff_var5_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_name']]
                            self.ff_var5_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var5_min']]
                            self.ff_var5_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var5_max']]
                            self.ff_var5_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_prec']]
                            self.ff_var5_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var5_divby']]
                            self.ff_var5_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var5_unit']]

                            self.ff_var6_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_name']]
                            self.ff_var6_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var6_min']]
                            self.ff_var6_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var6_max']]
                            self.ff_var6_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_prec']]
                            self.ff_var6_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var6_divby']]
                            self.ff_var6_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var6_unit']]

                            self.ff_var7_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_name']]
                            self.ff_var7_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var7_min']]
                            self.ff_var7_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var7_max']]
                            self.ff_var7_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_prec']]
                            self.ff_var7_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var7_divby']]
                            self.ff_var7_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var7_unit']]

                            self.ff_var8_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_name']]
                            self.ff_var8_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var8_min']]
                            self.ff_var8_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var8_max']]
                            self.ff_var8_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_prec']]
                            self.ff_var8_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var8_divby']]
                            self.ff_var8_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var8_unit']]

                            self.ff_var9_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_name']]
                            self.ff_var9_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var9_min']]
                            self.ff_var9_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['var9_max']]
                            self.ff_var9_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_prec']]
                            self.ff_var9_divby                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var9_divby']]
                            self.ff_var9_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var9_unit']]

                            self.ff_var10_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_name']]
                            self.ff_var10_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var10_min']]
                            self.ff_var10_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var10_max']]
                            self.ff_var10_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_prec']]
                            self.ff_var10_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var10_divby']]
                            self.ff_var10_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var10_unit']]

                            self.ff_var11_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_name']]
                            self.ff_var11_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var11_min']]
                            self.ff_var11_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var11_max']]
                            self.ff_var11_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_prec']]
                            self.ff_var11_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var11_divby']]
                            self.ff_var11_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var11_unit']]

                            self.ff_var12_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_name']]
                            self.ff_var12_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var12_min']]
                            self.ff_var12_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var12_max']]
                            self.ff_var12_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_prec']]
                            self.ff_var12_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var12_divby']]
                            self.ff_var12_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var12_unit']]

                            self.ff_var13_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_name']]
                            self.ff_var13_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var13_min']]
                            self.ff_var13_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var13_max']]
                            self.ff_var13_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_prec']]
                            self.ff_var13_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var13_divby']]
                            self.ff_var13_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var13_unit']]

                            self.ff_var14_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_name']]
                            self.ff_var14_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var14_min']]
                            self.ff_var14_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var14_max']]
                            self.ff_var14_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_prec']]
                            self.ff_var14_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var14_divby']]
                            self.ff_var14_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var14_unit']]

                            self.ff_var15_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_name']]
                            self.ff_var15_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var15_min']]
                            self.ff_var15_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['var15_max']]
                            self.ff_var15_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_prec']]
                            self.ff_var15_divby                                                        = ff_db_record[self.ff_db_entry_to_index_dict['var15_divby']]
                            self.ff_var15_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['var15_unit']]

                            self.ff_res1_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_name']]
                            self.ff_res1_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_min']]
                            self.ff_res1_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_max']]
                            self.ff_res1_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_prec']]
                            self.ff_res1_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res1_tol']]
                            self.ff_res1_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res1_points']]
                            self.ff_res1_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res1_unit']]

                            self.ff_res2_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_name']]
                            self.ff_res2_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_min']]
                            self.ff_res2_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_max']]
                            self.ff_res2_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_prec']]
                            self.ff_res2_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res2_tol']]
                            self.ff_res2_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res2_points']]
                            self.ff_res2_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res2_unit']]

                            self.ff_res3_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_name']]
                            self.ff_res3_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_min']]
                            self.ff_res3_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_max']]
                            self.ff_res3_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_prec']]
                            self.ff_res3_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res3_tol']]
                            self.ff_res3_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res3_points']]
                            self.ff_res3_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res3_unit']]

                            self.ff_res4_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_name']]
                            self.ff_res4_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_min']]
                            self.ff_res4_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_max']]
                            self.ff_res4_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_prec']]
                            self.ff_res4_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res4_tol']]
                            self.ff_res4_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res4_points']]
                            self.ff_res4_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res4_unit']]

                            self.ff_res5_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_name']]
                            self.ff_res5_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_min']]
                            self.ff_res5_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_max']]
                            self.ff_res5_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_prec']]
                            self.ff_res5_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res5_tol']]
                            self.ff_res5_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res5_points']]
                            self.ff_res5_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res5_unit']]

                            self.ff_res6_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_name']]
                            self.ff_res6_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_min']]
                            self.ff_res6_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_max']]
                            self.ff_res6_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_prec']]
                            self.ff_res6_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res6_tol']]
                            self.ff_res6_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res6_points']]
                            self.ff_res6_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res6_unit']]

                            self.ff_res7_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_name']]
                            self.ff_res7_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_min']]
                            self.ff_res7_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_max']]
                            self.ff_res7_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_prec']]
                            self.ff_res7_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res7_tol']]
                            self.ff_res7_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res7_points']]
                            self.ff_res7_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res7_unit']]

                            self.ff_es8_name                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_name']]
                            self.ff_res8_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_min']]
                            self.ff_res8_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_max']]
                            self.ff_res8_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res8_prec']]
                            self.ff_res8_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res8_tol']]
                            self.ff_res8_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res8_points']]
                            self.ff_res8_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res8_unit']]

                            self.ff_res9_name                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_name']]
                            self.ff_res9_min                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_min']]
                            self.ff_res9_max                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_max']]
                            self.ff_res9_prec                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_prec']]
                            self.ff_res9_tol                                                           = ff_db_record[self.ff_db_entry_to_index_dict['res9_tol']]
                            self.ff_res9_points                                                        = ff_db_record[self.ff_db_entry_to_index_dict['res9_points']]
                            self.ff_res9_unit                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res9_unit']]

                            self.ff_res10_name                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_name']]
                            self.ff_res10_min                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_min']]
                            self.ff_res10_max                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_max']]
                            self.ff_res10_prec                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_prec']]
                            self.ff_res10_tol                                                          = ff_db_record[self.ff_db_entry_to_index_dict['res10_tol']]
                            self.ff_res10_points                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res10_points']]
                            self.ff_res10_unit                                                         = ff_db_record[self.ff_db_entry_to_index_dict['res10_unit']]

                            self.ff_description_img_name_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_1']]
                            self.ff_description_img_data_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_1']]
                            self.ff_description_img_path_1	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_1']]
                            self.ff_description_img_name_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_2']]
                            self.ff_description_img_data_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_2']]
                            self.ff_description_img_path_2	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_2']]
                            self.ff_description_img_name_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_name_3']]
                            self.ff_description_img_data_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_data_3']]
                            self.ff_description_img_path_3	                                           = ff_db_record[self.ff_db_entry_to_index_dict['description_img_path_3']]

                            self.ff_test_time	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['test_time']]
                            self.ff_var_number	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['var_number']]
                            self.ff_res_number	                                                       = ff_db_record[self.ff_db_entry_to_index_dict['res_number']]
                            self.ff_question_pool_tag                                                  = ff_db_record[self.ff_db_entry_to_index_dict['question_pool_tag']]
                            self.ff_question_author                                                    = ff_db_record[self.ff_db_entry_to_index_dict['question_author']].replace('&', "&amp;")


            Create_Formelfrage_Questions.ff_question_structure(self, i)

    def ff_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""



        # VARIABLEN
        self.ff_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1

        self.ff_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.ff_var_use_latex_on_text_check.get(), self.ff_question_description_main)


        # Verbindung zur FF-Datenank
        ff_connect = sqlite3.connect(self.database_formelfrage_path)
        ff_cursor = ff_connect.cursor()

        # Alle Einträge auslesen
        ff_cursor.execute("SELECT *, oid FROM formelfrage_table")
        ff_db_records = ff_cursor.fetchall()



        for ff_db_record in ff_db_records:

            # Hier werden die Fragen anhand der ID's erstellt
            if str(ff_db_record[len(ff_db_record)-1]) == self.ff_test_entry_splitted[id_nr]:

                # Hier werden die Fragen anhand der ID's erstellt
                if str(ff_db_record[len(ff_db_record)-1]) == self.ff_test_entry_splitted[id_nr]:

                        test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_1, self.ff_description_img_data_1, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)
                        test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_2, self.ff_description_img_data_2, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)
                        test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.ff_description_img_name_3, self.ff_description_img_data_3, id_nr, self.ff_question_type_test_or_pool, self.formelfrage_test_img_file_path, self.formelfrage_pool_img_file_path)

                        # if self.ff_question_type_test_or_pool == "question_test":
                        #
                        #     if self.ff_description_img_name_1 != "EMPTY":
                        #         Create_Formelfrage_Questions.ff_createFolder(self, self.formelfrage_test_img_file_path + '/' + 'il_0_mob_000000' + str(id_nr) + '/')
                        #
                        #         #img wird immer als PNG Datei abgelegt.
                        #         with open(self.formelfrage_test_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png", 'wb') as image_file:
                        #             image_file.write(self.ff_description_img_data_1)
                        #
                        #         self.image = Image.open(self.formelfrage_test_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png")
                        #         self.image.save(self.formelfrage_test_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png")
                        #
                        # else:  # image pool
                        #     if self.ff_description_img_name_1 != "EMPTY":
                        #         Create_Formelfrage_Questions.ff_createFolder(self, self.formelfrage_pool_img_file_path + '/' + 'il_0_mob_000000' + str(id_nr) + '/')
                        #
                        #         #img wird immer als PNG Datei abgelegt.
                        #         with open(self.formelfrage_pool_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png", 'wb') as image_file:
                        #             image_file.write(self.ff_description_img_data_1)
                        #
                        #         self.image = Image.open(self.formelfrage_pool_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png")
                        #         self.image.save(self.formelfrage_pool_img_file_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.ff_description_img_name_1 + ".png")



                        r1_rating = "0"
                        r1_unit = ""
                        r1_unitvalue = ""
                        r1_resultunits = ""


                        # Aufbau für  Fragenstruktur "TEST"
                        if self.ff_question_type_test_or_pool == "question_test":
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

                            test_generator_modul_ilias_test_struktur.Additional_Funtions.set_taxonomy_for_question(self,
                                                                                                                   id_nr,
                                                                                                                   self.number_of_entrys,
                                                                                                                   item,
                                                                                                                   self.formelfrage_pool_qpl_file_path_template,
                                                                                                                   self.formelfrage_pool_qpl_file_path_output
                                                                                                                   )



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
                        item.set('title', self.ff_question_title)

                        # Fragen-Titel Beschreibung
                        qticomment.text = self.ff_question_description_title

                        # Testdauer -- "duration" in xml
                        # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                        duration.text = self.ff_test_time
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
                        fieldentry.text = self.ff_question_author
                        # -----------------------------------------------------------------------POINTS
                        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                        fieldlabel.text = "points"
                        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                        fieldentry.text = str(self.ff_res1_points)

                        # Fragentitel einsetzen -- "presentation label" in xml
                        presentation.set('label', self.ff_question_title)

                        # Fragen-Text (Format) einsetzen -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                        question_description_mattext.set('texttype', "text/html")

                        # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                        # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten
                        question_description_mattext.text = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_picture_to_description_main(
                                                            self, self.ff_description_img_name_1, self.ff_description_img_data_1,
                                                            self.ff_description_img_name_2, self.ff_description_img_data_2,
                                                            self.ff_description_img_name_3, self.ff_description_img_data_3,
                                                            self.ff_question_description_main, question_description_mattext, question_description_material, id_nr)




                        # ----------------------------------------------------------------------- Variable
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v1", self.ff_var1_min, self.ff_var1_max, self.ff_var1_prec, self.ff_var1_divby, self.ff_var1_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v2", self.ff_var2_min, self.ff_var2_max, self.ff_var2_prec, self.ff_var2_divby, self.ff_var2_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v3", self.ff_var3_min, self.ff_var3_max, self.ff_var3_prec, self.ff_var3_divby, self.ff_var3_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v4", self.ff_var4_min, self.ff_var4_max, self.ff_var4_prec, self.ff_var4_divby, self.ff_var4_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v5", self.ff_var5_min, self.ff_var5_max, self.ff_var5_prec, self.ff_var5_divby, self.ff_var5_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v6", self.ff_var6_min, self.ff_var6_max, self.ff_var6_prec, self.ff_var6_divby, self.ff_var6_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v7", self.ff_var7_min, self.ff_var7_max, self.ff_var7_prec, self.ff_var7_divby, self.ff_var7_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v8", self.ff_var8_min, self.ff_var8_max, self.ff_var8_prec, self.ff_var8_divby, self.ff_var8_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v9", self.ff_var9_min, self.ff_var9_max, self.ff_var9_prec, self.ff_var9_divby, self.ff_var9_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v10", self.ff_var10_min, self.ff_var10_max, self.ff_var10_prec, self.ff_var10_divby, self.ff_var10_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v11", self.ff_var11_min, self.ff_var11_max, self.ff_var11_prec, self.ff_var11_divby, self.ff_var11_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v12", self.ff_var12_min, self.ff_var12_max, self.ff_var12_prec, self.ff_var12_divby, self.ff_var12_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v13", self.ff_var13_min, self.ff_var13_max, self.ff_var13_prec, self.ff_var13_divby, self.ff_var13_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v14", self.ff_var14_min, self.ff_var14_max, self.ff_var14_prec, self.ff_var14_divby, self.ff_var14_unit)
                        Create_Formelfrage_Questions.ff_question_variables_structure(self, qtimetadata, "$v15", self.ff_var15_min, self.ff_var15_max, self.ff_var15_prec, self.ff_var15_divby, self.ff_var15_unit)



                        # ----------------------------------------------------------------------- Solution
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r1", self.ff_res1_formula, self.ff_res1_min, self.ff_res1_max, self.ff_res1_prec, self.ff_res1_tol, self.ff_res1_points, self.ff_res1_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r2", self.ff_res2_formula, self.ff_res2_min, self.ff_res2_max, self.ff_res2_prec, self.ff_res2_tol, self.ff_res2_points, self.ff_res2_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r3", self.ff_res3_formula, self.ff_res3_min, self.ff_res3_max, self.ff_res3_prec, self.ff_res3_tol, self.ff_res3_points, self.ff_res3_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r4", self.ff_res4_formula, self.ff_res4_min, self.ff_res4_max, self.ff_res4_prec, self.ff_res4_tol, self.ff_res4_points, self.ff_res4_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r5", self.ff_res5_formula, self.ff_res5_min, self.ff_res5_max, self.ff_res5_prec, self.ff_res5_tol, self.ff_res5_points, self.ff_res5_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r6", self.ff_res6_formula, self.ff_res6_min, self.ff_res6_max, self.ff_res6_prec, self.ff_res6_tol, self.ff_res6_points, self.ff_res6_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r7", self.ff_res7_formula, self.ff_res7_min, self.ff_res7_max, self.ff_res7_prec, self.ff_res7_tol, self.ff_res7_points, self.ff_res7_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r8", self.ff_res8_formula, self.ff_res8_min, self.ff_res8_max, self.ff_res8_prec, self.ff_res8_tol, self.ff_res8_points, self.ff_res8_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r9", self.ff_res9_formula, self.ff_res9_min, self.ff_res9_max, self.ff_res9_prec, self.ff_res9_tol, self.ff_res9_points, self.ff_res9_unit)
                        Create_Formelfrage_Questions.ff_question_results_structure(self, qtimetadata, "$r10", self.ff_res10_formula, self.ff_res10_min, self.ff_res10_max, self.ff_res10_prec, self.ff_res10_tol, self.ff_res10_points, self.ff_res10_unit)








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
                        # Der letzte "Zweig" --> "len(self.ff_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                        if self.ff_question_type_test_or_pool == "question_test":
                            self.ff_myroot[0][len(self.ff_myroot[0]) - 1].append(item)

                        # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                        # Die Frage kann einfach angehangen werden
                        else:
                            self.ff_myroot.append(item)

                        self.ff_mytree.write(self.qti_file_path_output)
                        print("Formelfrage Frage erstellt! --> Titel: " + str(self.ff_question_title))



        ff_connect.commit()
        ff_connect.close()

        if self.ff_question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.formelfrage_files_path,"ff_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.ff_file_max_id+1))
            self.mytree.write(self.qpl_file)

    def ff_question_variables_structure(self, xml_qtimetadata,  ff_var_name, ff_var_min, ff_var_max, ff_var_prec, ff_var_divby, ff_var_unit):

        self.ff_var_name = ff_var_name
        self.ff_var_min = str(ff_var_min)
        self.ff_var_max = str(ff_var_max)
        self.ff_var_prec = str(ff_var_prec)
        self.ff_var_divby = str(ff_var_divby)
        self.ff_var_divby_length = len(str(self.ff_var_divby))
        self.ff_var_unit = ff_var_unit
        self.ff_var_unit_length = len(str(self.ff_var_unit))

        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = ff_var_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

        if self.ff_var_unit != "":
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ff_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ff_var_divby_length) + ":\"" + self.ff_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ff_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ff_var_max + ";" \
                              "s:4:\"unit\";s:" + str(self.ff_var_unit_length) + ":\"" + self.ff_var_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.ff_var_unit))) + ":\"" + Formelfrage.unit_table(self, self.ff_var_unit) + "\";" \
                              "}"
        else:
            fieldentry.text = "a:6:{" \
                              "s:9:\"precision\";i:" + self.ff_var_prec + ";" \
                              "s:12:\"intprecision\";s:" + str(self.ff_var_divby_length) + ":\"" + self.ff_var_divby + "\";" \
                              "s:8:\"rangemin\";d:" + self.ff_var_min + ";" \
                              "s:8:\"rangemax\";d:" + self.ff_var_max + ";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "}"

    def ff_question_results_structure(self, xml_qtimetadata, ff_res_name, ff_res_formula, ff_res_min, ff_res_max, ff_res_prec, ff_res_tol, ff_res_points, ff_res_unit):

        def replace_words_in_formula(formula):

            self.replace_words_dict = {
                "$V": "$v",
                "$R": "$r",
                "=": " ",
                "SIN": "sin",
                "SINH": "sinh",
                "ARCSIN": "arcsin",
                "ASIN": "asin",
                "ARCSINH": "arcsinh",
                "ASINH": "asinh",
                "COS": "cos",
                "COSH": "cosh",
                "ARCCOS": "arccos",
                "ACOS": "acos",
                "ARCCOSH": "arccosh",
                "ACOSH": "acosh",
                "TAN": "tan",
                "TANH": "tanh",
                "ARCTAN": "arctan",
                "ATAN": "atan",
                "ARCTANH": "arctanh",
                "ATANH": "atanh",
                "SQRT": "sqrt",
                "ABS": "abs",
                "LN": "ln",
                "LOG": "log"
            }

            formula = ' '.join([self.replace_words_dict.get(i,i) for i in formula.split()])

            return formula

        self.ff_res_name = ff_res_name
        self.ff_res_formula = ff_res_formula
        self.ff_res_formula_length = len(str(self.ff_res_formula))
        self.ff_res_min = str(ff_res_min)
        self.ff_res_min_length = len(str(self.ff_res_min))
        self.ff_res_max = str(ff_res_max)
        self.ff_res_max_length = len(str(self.ff_res_max))
        self.ff_res_prec = str(ff_res_prec)
        self.ff_res_tol = str(ff_res_tol)
        self.ff_res_tol_length = len(str(self.ff_res_tol))

        self.ff_res_points = str(ff_res_points)
        self.ff_res_unit = ff_res_unit
        self.ff_res_unit_length = len(str(self.ff_res_unit))


        # ILIAS kann nicht mit "$Vx" statt "$vx" umgehen (kleines statt großes "V" für Variablen)
        # Ebenfalls gilt das für $Rx und $rx
        # In der Ergebnisgleichung darf kein "=" verwendet werden! Es erscheint keine Fehlermeldung, jedoch sind die Ergebnisse
        # aus der ILIAS-Berechnung dann immer "0"
        self.ff_res_formula = replace_words_in_formula(self.ff_res_formula)
        #self.ff_res_formula = self.ff_res_formula.replace('$V', "$v")
        #self.ff_res_formula = self.ff_res_formula.replace('$R', "$r")
        #self.ff_res_formula = self.ff_res_formula.replace('=', " ")



        # s for string length: "9" -> precision = "9" characters
        # rangemin: "i" for negative numbers, ...
        #           "d" for (negativ?) float numbers
        #           "i" for negativ whole numbers
        #           "s" for positiv whole numbers

        qtimetadatafield = ET.SubElement(xml_qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = self.ff_res_name
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

        if self.ff_res_unit != "":
            fieldentry.text = "a:10:{" \
                              "s:9:\"precision\";i:" + self.ff_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + self.ff_res_tol_length + ":\"" + self.ff_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + self.ff_res_min_length + ":\"" + self.ff_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + self.ff_res_max_length + ":\"" + self.ff_res_max + "\";" \
                              "s:6:\"points\";s:1:\"" + self.ff_res_points + "\";" \
                              "s:7:\"formula\";s:" + self.ff_res_formula_length + ":\"" + self.ff_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:" + str(self.ff_res_unit_length) + ":\"" + self.ff_res_unit + "\";" \
                              "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.ff_res_unit))) + ":\"" + Formelfrage.unit_table(self, self.ff_res_unit) + "\";" \
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
                              "s:9:\"precision\";i:" + self.ff_res_prec + ";" \
                              "s:9:\"tolerance\";s:" + str(self.ff_res_tol_length) + ":\"" + self.ff_res_tol + "\";" \
                              "s:8:\"rangemin\";s:" + str(self.ff_res_min_length) + ":\"" + self.ff_res_min + "\";" \
                              "s:8:\"rangemax\";s:" + str(self.ff_res_max_length) + ":\"" + self.ff_res_max + "\";" \
                              "s:6:\"points\";s:1:\"" + self.ff_res_points + "\";" \
                              "s:7:\"formula\";s:" + str(self.ff_res_formula_length) + ":\"" + self.ff_res_formula + "\";" \
                              "s:6:\"rating\";s:0:\"\";" \
                              "s:4:\"unit\";s:0:\"\";" \
                              "s:9:\"unitvalue\";s:0:\"\";" \
                              "s:11:\"resultunits\";a:0:{}" \
                              "}"



class Create_Formelfrage_Test(Formelfrage):
    def __init__(self, entry_to_index_dict):
        self.ff_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.ff_db_entry_to_index_dict,
                                                                            self.formelfrage_test_tst_file_path_template,
                                                                            self.formelfrage_test_tst_file_path_output,
                                                                            self.formelfrage_test_qti_file_path_template,
                                                                            self.formelfrage_test_qti_file_path_output,
                                                                            self.ff_ilias_test_title_entry.get(),
                                                                            self.create_formelfrage_test_entry.get(),
                                                                            self.ff_question_type_entry.get(),
                                                                            )



        # ##### Einlesen der "Formelfrage" _tst_.xml zum ändern des Test-Titel
        # self.ff_mytree = ET.parse(self.formelfrage_test_tst_file_path_template)
        # self.ff_myroot = self.ff_mytree.getroot()
        #
        # # Titel-Eintrag ändern (Voreinstellung in der Vorlage: Titel = ff_test_vorlage)
        # for ContentObject in self.ff_myroot.iter('ContentObject'):
        #     for MetaData in ContentObject.iter('MetaData'):
        #         for General in MetaData.iter('General'):
        #             for Title in General.iter('Title'):
        #                 Title.text = self.ff_ilias_test_title_entry.get()
        #                 print("Title - Text")
        #                 print(Title.text)
        #                 # .XML Datei kann keine "&" verarbeiten.
        #                 # "&" muss gegen "&amp" ausgetauscht werden sonst kann Ilias die Datei hinterher nicht verwerten.
        #                 Title.text = Title.text.replace('&', "&amp;")
        #
        #
        #
        #
        #
        #     # Sollte kein Namen vergeben werden, wird der Test-Titel auf "DEFAULT" gesetzt
        #     if Title.text == "ff_test_vorlage" or Title.text == "":
        #         Title.text = "DEFAULT"
        #
        #     # Änderungen der .XML in eine neue Datei schreiben
        #     # Die Datei wird nach dem ILIAS-Import "Standard" benannt "1604407426__0__tst_2040314.xml"
        #     # Die Ziffernfolge der 10 Ziffern am Anfang sowie der 7 Ziffern zum Schluss können nach belieben variiert werden.
        #     self.ff_mytree.write(self.formelfrage_test_tst_file_path_output)
        #
        #
        #     print("TST FILE aktualisiert!")
        #     print(self.formelfrage_test_tst_file_path_output)
        #
        #     # Hier wird der Fragen-Test geschrieben
        #     Create_Formelfrage_Questions.__init__(self,
        #                                           self.ff_db_entry_to_index_dict,
        #                                           self.create_formelfrage_test_entry.get(),
        #                                           "question_test",
        #                                           "img_pool_dir_not_used_for_test",
        #
        #                                           self.formelfrage_test_qti_file_path_template,
        #                                           self.formelfrage_test_qti_file_path_output,
        #                                           "xml_qpl_output_not_used_for_test",
        #
        #
        #
        #
        #     # Anschließend werden die "&amp;" in der XML wieder gegen "&" getauscht
        #     Formelfrage.ff_replace_character_in_xml_file(self, self.formelfrage_test_qti_file_path_output)
        #


class Create_Formelfrage_Pool(Formelfrage):

    def __init__(self, entry_to_index_dict, var_create_all_questions):
        self.ff_entry_to_index_dict = entry_to_index_dict
        self.ff_var_create_question_pool_all = var_create_all_questions

        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(self,
                                                                            self.project_root_path,
                                                                            self.formelfrage_pool_directory_output,
                                                                            self.formelfrage_files_path_pool_output,
                                                                            self.formelfrage_pool_qti_file_path_template,
                                                                            self.ff_ilias_test_title_entry.get(),
                                                                            self.create_formelfrage_pool_entry.get(),
                                                                            "Formelfrage",
                                                                            self.database_formelfrage_path,
                                                                            "formelfrage_table",
                                                                            self.ff_db_entry_to_index_dict,
                                                                            self.ff_var_create_question_pool_all
                                                                            )



    #
    # def __init__(self, entry_to_index_dict):
    #
    #     self.ff_entry_to_index_dict = entry_to_index_dict
    #     self.question_title_list = []
    #     self.question_pool_id_list = []
    #     self.all_entries_from_db_list = []
    #
    #
    #     # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
    #     # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
    #     #self.ff_folder_new_ID_dir = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_qpl_Daten'))
    #
    #     self.names = []
    #     self.filename_id = []
    #
    #
    #     self.ff_list_of_directories = []
    #     self.ff_list_of_file_IDs = []
    #     self.ff_filename_with_zip_index = []
    #
    #     self.question_title_list = []
    #     self.question_pool_id_list = []
    #     self.question_title_to_pool_id_dict = {}
    #     self.question_title_to_item_id_dict = {}
    #
    #
    #     # Ordnernamen in "self.formelfrage_pool_directory_output" auslesen
    #     self.ff_list_of_directories = os.listdir(self.formelfrage_pool_directory_output)
    #
    #
    #     for i in range(len(self.ff_list_of_directories)):
    #         if ".zip" in self.ff_list_of_directories[i]:
    #             self.ff_filename_with_zip_index.append(i)
    #
    #
    #
    #
    #
    #     for j in range(len(self.ff_filename_with_zip_index)):
    #         self.ff_list_of_directories.pop(self.ff_filename_with_zip_index[j]-j)
    #
    #
    #     #Die letzten sieben (7) Zeichen des Orndernamen in eine Liste packen. Die letzten 7 Zeichen geben die ID des Fragenpools an
    #     #Die Ordnernamen für ILIAS sind immer in dem Format: z.B.: 1604407426__0__tst_2040314
    #     #Die ID wird im nachhineie um "1" inkrementiert
    #     for k in range(len(self.ff_list_of_directories)):
    #         self.ff_list_of_file_IDs.append(self.ff_list_of_directories[k][-7:])
    #
    #
    #     # Alle String Einträge nach "INT" konvertieren um mit der max() funktion die höchste ID herauszufiltern
    #     self.ff_list_of_file_IDs = list(map(int, self.ff_list_of_file_IDs))
    #
    #     self.ff_file_max_id = str(max(self.ff_list_of_file_IDs)+1)
    #
    #
    #     #Pfad anpassungen - Die ID muss um +1 erhöht werden, wenn "Fragenpool erstellen" betätigt wird
    #     self.ilias_id_pool_qpl_dir = "1596569820__0__qpl_" + self.ff_file_max_id
    #     self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + self.ff_file_max_id + ".xml"
    #     self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + self.ff_file_max_id + ".xml"
    #     self.ilias_id_pool_img_dir = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, "objects"))
    #
    #     self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))
    #     self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))
    #     self.formelfrage_pool_img_file_path = os.path.normpath(os.path.join(self.formelfrage_files_path,"ff_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))
    #
    #     # Pfad für ILIAS-Taxonomie Dateien --> "export.xml"
    #     self.modules_export_file = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Modules', 'TestQuestionPool', 'set_1', 'export.xml'))
    #
    #
    #     self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #     self.taxonomy_file_writes = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #
    #     print("###")
    #     print(self.ilias_id_pool_qpl_dir)
    #
    #     # Neuen Ordner erstellen
    #     Create_Formelfrage_Questions.ff_createFolder(self, os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir)))
    #
    #
    #     # Hier wird das Verzeichnis kopiert, um die Struktur vom Fragenpool-Ordner zu erhalten
    #     # Die Struktur stammt aus einem Vorlage-Ordner. Die notwendigen XML Dateien werden im Anschluss ersetzt bzw. mit Werten aktualisiert
    #     Create_Formelfrage_Pool.ff_copytree(self, os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'orig_1596569820__0__qpl_2074808')),
    #              os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir)))
    #
    #     # Da durch "copytree" alle Daten kopiert werden, werden hier die qpl.xml und die qti.xml auf die aktuelle Nummer umbenannt und später dadurch überschrieben
    #     # Anpassung ID für "qti".xml
    #     os.rename(os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qti_2074808.xml")),
    #               os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml)))
    #
    #     # Anpassung ID für "qpl".xml
    #     os.rename(os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qpl_2074808.xml")),
    #               os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml)))
    #
    #
    #
    #     ###### Anpassung der Datei "Modul -> export". Akualisierung des Dateinamens
    #     self.mytree = ET.parse(self.modules_export_file)
    #     self.myroot = self.mytree.getroot()
    #
    #     for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
    #         TaxId.set('Id', self.ff_file_max_id)
    #
    #     self.mytree.write(self.modules_export_file)
    #
    #     with open(self.modules_export_file, 'r') as xml_file:
    #         xml_str = xml_file.read()
    #     xml_str = xml_str.replace('ns0:', 'exp:')
    #     with open(self.modules_export_file, 'w') as replaced_xml_file:
    #         replaced_xml_file.write(xml_str)
    #
    #
    #
    #     ######  Anpassung der Datei "Modules -> //... //  -> export.xml". Akualisierung des Dateinamens
    #     self.taxonomy_export_file = os.path.normpath(os.path.join(self.formelfrage_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #     self.mytree = ET.parse(self.taxonomy_export_file)
    #     self.myroot = self.mytree.getroot()
    #
    #     for ExportItem in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
    #         #print(ExportItem.attrib.get('Id'))
    #         if ExportItem.attrib.get('Id') != "":
    #             #print(ExportItem.attrib.get('Id'))
    #             ExportItem.set('Id', self.ff_file_max_id)
    #             break
    #
    #
    #
    #     for object_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ObjId'):
    #         object_id.text = self.ff_file_max_id
    #         break
    #
    #     self.mytree.write(self.taxonomy_export_file)
    #
    #     # Taxonomie-datei "refreshen"
    #     Create_Formelfrage_Pool.ff_taxonomy_file_refresh(self, self.taxonomy_export_file)
    #
    #
    #     # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
    #     # ilias_id_pol_
    #     self.formelfrage_pool_qti_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path,"ff_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))
    #     self.formelfrage_pool_qpl_file_path_output = os.path.normpath(os.path.join(self.formelfrage_files_path,"ff_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))
    #
    #
    #
    #     # Hier wird der Fragen_Pool erstellt
    #     Create_Formelfrage_Questions.__init__(self, self.ff_db_entry_to_index_dict, self.create_formelfrage_pool_entry.get(), "question_pool", self.ilias_id_pool_img_dir, self.ilias_id_pool_qpl_dir, self.formelfrage_pool_qti_file_path_template, self.formelfrage_pool_qti_file_path_output, self.formelfrage_pool_qpl_file_path_output, self.ilias_id_pool_qti_xml, self.ff_file_max_id, self.taxonomy_file_question_pool)
    #
    #
    #     # Anschließend werden die "&amp;" in der XML wieder gegen "&" getauscht
    #     Formelfrage.ff_replace_character_in_xml_file(self, self.formelfrage_pool_qti_file_path_output)
    #
    #
    #     # Hier wird die Taxonomie des Fragenpools bearbeitet / konfiguriert
    #     #
    #     # self.create_formelfrage_pool_entry.get(),  -- Nimmt die eingetragenen IDs aus der Eingabebox für Fragenpool
    #     # self.var_create_question_pool_all.get(),   --  Check-Box, "Alle Fragen erstellen?"
    #     # "formelfrage_db.db",                       -- Datenbank-Name
    #     # "formelfrage_table",                       -- Datenbank-Table-Name
    #     # self.ff_entry_to_index_dict,               -- Dictionionary
    #     # self.taxonomy_file_question_pool,          -- Taxonomie-Datei Ordner Pfad
    #     # self.formelfrage_pool_qti_file_path_output -- QTI-Datei - Pfad
    #
    #     test_generator_modul_taxonomie_und_textformatierung.Taxonomie.create_taxonomy_for_pool(self, self.create_formelfrage_pool_entry.get(), self.var_create_question_pool_all.get(), "formelfrage_db.db", "formelfrage_table", self.ff_entry_to_index_dict, self.taxonomy_file_question_pool, self.formelfrage_pool_qti_file_path_output)
    #
    # def ff_copytree(self, src, dst, symlinks=False, ignore=None):
    #         for item in os.listdir(src):
    #             s = os.path.join(src, item)
    #             d = os.path.join(dst, item)
    #             if os.path.isdir(s):
    #                 shutil.copytree(s, d, symlinks, ignore)
    #             else:
    #                 shutil.copy2(s, d)
    #
    # def ff_taxonomy_file_refresh(self, file_location):
    #     self.file_location = file_location
    #     self.file_location = file_locationf
    #     # print("refresh_file_location: " + str(self.file_location))
    #     with open(self.file_location, 'r') as xml_file:
    #         xml_str = xml_file.read()
    #     xml_str = xml_str.replace('ns0:', 'exp:')
    #     xml_str = xml_str.replace('ns2:', 'ds:')
    #     xml_str = xml_str.replace('ns3:', '')  # replace "x" with "new value for x"
    #     xml_str = xml_str.replace(
    #         '<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
    #         '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')
    #     xml_str = xml_str.replace(
    #         '<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Entity="tax" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
    #         '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')
    #
    #     with open(self.file_location, 'w') as replaced_xml_file:
    #         replaced_xml_file.write(xml_str)


