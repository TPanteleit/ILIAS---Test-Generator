
import xml.etree.ElementTree as ET
from tkinter import *                  # Stellt die Funktionen für z.B. Labels & Entrys zur Verfügung
from tkinter import ttk                # Stellt die Funktionen der Comboboxen (Auswahlboxen) zur Verfügung
from tkinter import filedialog
import base64
import pathlib
import sqlite3
import os
import pprint
import pandas as pd
from datetime import datetime
from PIL import ImageTk, Image          # Zur Preview von ausgewählten Bildern
import xlsxwriter                       # import/export von excel Dateien
import shutil                           # Wird verwendet um Verzeichnisse zu kopieren

### Eigene Dateien / Module
from Test_Generator_Module import test_generator_modul_datenbanken_anzeigen
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung
from Test_Generator_Module import test_generator_modul_ilias_test_struktur
from Test_Generator_Module import test_generator_modul_ilias_import_test_datei

class MultipleChoice:
    def __init__(self, app, multiplechoice_tab, project_root_path):
        self.multiplechoice_tab = multiplechoice_tab
        
        self.mc_description_img_name_1 = "EMPTY"
        self.mc_description_img_name_2 = "EMPTY"
        self.mc_description_img_name_3 = "EMPTY"

        self.mc_description_img_data_1 = "EMPTY"
        self.mc_description_img_data_2 = "EMPTY"
        self.mc_description_img_data_3 = "EMPTY"

        self.mc_description_img_path_1 = "EMPTY"
        self.mc_description_img_path_2 = "EMPTY"
        self.mc_description_img_path_3 = "EMPTY"

############## DEFINE MULTIPLECHOICE PATHS

        # Pfad des Projekts und des MC-Moduls
        self.project_root_path = project_root_path
        self.multiplechoice_files_path = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-MultipleChoice"))
        self.multiplechoice_files_path_pool_output = os.path.normpath(os.path.join(self.multiplechoice_files_path, "mc_ilias_pool_abgabe"))

        # Pfad für die Datenbank
        self.database_multiplechoice_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", "ilias_multiplechoice_db.db"))

        # Pfad für ILIAS-Test Vorlage
        self.multiplechoice_test_qti_file_path_template = os.path.normpath(os.path.join(self.multiplechoice_files_path, "mc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__qti__.xml"))
        self.multiplechoice_test_tst_file_path_template = os.path.normpath(os.path.join(self.multiplechoice_files_path, "mc_test_qti_und_tst_dateien_vorlage", "ilias_test_vorlage__tst__.xml"))

        # Pfad für ILIAS-Pool Vorlage
        self.multiplechoice_pool_qti_file_path_template = os.path.normpath(os.path.join(self.multiplechoice_files_path, "mc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qti__.xml"))
        self.multiplechoice_pool_qpl_file_path_template = os.path.normpath(os.path.join(self.multiplechoice_files_path, "mc_pool_qti_und_qpl_dateien_vorlage", "ilias_pool_vorlage__qpl__.xml"))

        # Pfad für ILIAS-Test Dateien (zum hochladen in ILIAS)
        self.multiplechoice_test_qti_file_path_output = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__qti_2040314.xml"))
        self.multiplechoice_test_tst_file_path_output = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_test_abgabe", "1604407426__0__tst_2040314", "1604407426__0__tst_2040314.xml"))
        self.multiplechoice_test_img_file_path = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_test_abgabe", "1604407426__0__tst_2040314", "objects"))

        
        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        self.multiplechoice_pool_directory_output = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_pool_abgabe"))


###################### "DATENBANK ENTRIES UND INDEX DICT  ###################


        # Dictionary aus zwei Listen erstellen
        # Auslesen der SingleChoice-Datenbank einträgen
        # Nur die erste Zeile auslesen um einen Zusammenhang zwischen Variablen und Indexen herzustellen
        self.mc_db_find_entries = []
        self.mc_db_find_indexes = []

        connect = sqlite3.connect(self.database_multiplechoice_path)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM multiplechoice_table LIMIT 1")

        mc_db_records = cursor.fetchall()
        for mc_db_record in mc_db_records:
            for k in range(len(mc_db_record)):
                self.mc_db_find_entries.append(str(mc_db_record[k]))
                self.mc_db_find_indexes.append(int(k))


        self.mc_db_entry_to_index_dict = dict(zip((self.mc_db_find_entries), (self.mc_db_find_indexes)))



        connect.commit()
        connect.close()

############## FRAMES
        # self.mc_frame_ilias_test_title = LabelFrame(self.multiplechoice_tab, text="Testname & Autor", padx=5, pady=5)
        # self.mc_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        # 
        # self.mc_frame = LabelFrame(self.multiplechoice_tab, text="Multiple Choice", padx=5, pady=5)
        # self.mc_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NW)
        # 
        # self.mc_frame_question_attributes = LabelFrame(self.multiplechoice_tab, text="Fragen Attribute", padx=5, pady=5)
        # self.mc_frame_question_attributes.grid(row=9, column=0, padx=170, pady=10, sticky="NW")
        # 
        # self.mc_frame_question_description_functions = LabelFrame(self.multiplechoice_tab, text="Fragentext Funktionen", padx=5, pady=5)
        # self.mc_frame_question_description_functions.grid(row=9, column=0, padx=10, pady=10, sticky="NW")
        # 
        # self.mc_frame_database = LabelFrame(self.multiplechoice_tab, text="MultipleChoice-Datenbank", padx=5, pady=5)
        # self.mc_frame_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)
        # 
        # self.mc_frame_create_multiplechoice_test = LabelFrame(self.multiplechoice_tab, text="MultipleChoice-Test erstellen", padx=5, pady=5)
        # self.mc_frame_create_multiplechoice_test.grid(row=10, column=0, padx=0, pady=10, sticky="NE")
        # 
        # self.mc_frame_excel_import_export = LabelFrame(self.multiplechoice_tab, text="Excel Import/Export", padx=5, pady=5)
        # self.mc_frame_excel_import_export.grid(row=9, column=0, padx=40, pady=10, sticky="NE")

        self.mc_frame_ilias_test_title = LabelFrame(self.multiplechoice_tab, text="Testname & Autor", padx=5, pady=5)
        self.mc_frame_ilias_test_title.grid(row=0, column=0, padx=10, pady=10, sticky="NW")

        self.mc_frame = LabelFrame(self.multiplechoice_tab, text="Multiplechoice", padx=5, pady=5)
        self.mc_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NW")

        self.mc_frame_question_attributes = LabelFrame(self.multiplechoice_tab, text="Fragen Attribute", padx=5, pady=5)
        self.mc_frame_question_attributes.grid(row=2, column=0, padx=155, pady=10, sticky="NE")

        self.mc_frame_database = LabelFrame(self.multiplechoice_tab, text="Multiplechoice-Datenbank", padx=5, pady=5)
        self.mc_frame_database.grid(row=2, column=0, padx=10, pady=10, sticky="NW")

        self.mc_frame_create_multiplechoice_test = LabelFrame(self.multiplechoice_tab, text="MC-Test erstellen", padx=5, pady=5)
        self.mc_frame_create_multiplechoice_test.grid(row=2, column=0, padx=250, pady=120, sticky="NE")


        self.mc_frame_taxonomy_settings = LabelFrame(self.multiplechoice_tab, text="Taxonomie Einstellungen", padx=5, pady=5)
        self.mc_frame_taxonomy_settings.grid(row=0, column=1, padx=10, pady=10, sticky="NW")

        self.mc_frame_question_description_functions = LabelFrame(self.multiplechoice_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.mc_frame_question_description_functions.grid(row=1, column=1, padx=10, pady=10, sticky="NW")

        self.mc_frame_excel_import_export = LabelFrame(self.multiplechoice_tab, text="Excel Import/Export", padx=5, pady=5)
        self.mc_frame_excel_import_export.grid(row=2, column=1, padx=10, pady=10, sticky="NW")

        self.mc_frame_question_permutation = LabelFrame(self.multiplechoice_tab, text="Fragen - Permutation", padx=5, pady=5)
        self.mc_frame_question_permutation.grid(row=2, column=1,padx=10, pady=120,   sticky="NW")


        self.mc_frame_description_picture = LabelFrame(self.multiplechoice_tab, text="Fragen-Text Bild", padx=5, pady=5)
        self.mc_frame_description_picture.grid(row=1, column=2, padx=10, pady=10, sticky="NW")


 ###################### "Testname & Autor" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        self.mc_ilias_test_title_label = Label(self.mc_frame_ilias_test_title, text="Name des Tests")
        self.mc_ilias_test_title_label.grid(row=0, column=0, sticky=W)

        self.mc_ilias_test_title_entry = Entry(self.mc_frame_ilias_test_title, width=60)
        self.mc_ilias_test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.mc_ilias_autor_label = Label(self.mc_frame_ilias_test_title, text="Autor")
        self.mc_ilias_autor_label.grid(row=1, column=0, sticky=W)

        self.mc_ilias_autor_entry = Entry(self.mc_frame_ilias_test_title, width=60)
        self.mc_ilias_autor_entry.grid(row=1, column=1, sticky=W, padx=30)


###################### "Fragen-Text Bild" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################

        # Hinzufügen Bild 1
        self.mc_var_use_image_1 = IntVar()
        self.mc_check_use_image_1_in_description = Checkbutton(self.mc_frame_question_description_functions, text="Bild 1 hochladen?", variable=self.mc_var_use_image_1, onvalue=1, offvalue=0)
        self.mc_check_use_image_1_in_description.deselect()
        self.mc_check_use_image_1_in_description.grid(row=5, column=0, sticky=W, padx=90, pady=(10, 0))

        # Hinzufügen Bild 2
        self.mc_var_use_image_2 = IntVar()
        self.mc_check_use_image_2_in_description = Checkbutton(self.mc_frame_question_description_functions, text="Bild 2 hochladen?", variable=self.mc_var_use_image_2, onvalue=1, offvalue=0)
        self.mc_check_use_image_2_in_description.deselect()
        self.mc_check_use_image_2_in_description.grid(row=6, column=0, sticky=W, padx=90)

        # Hinzufügen Bild 3
        self.mc_var_use_image_3 = IntVar()
        self.mc_check_use_image_3_in_description = Checkbutton(self.mc_frame_question_description_functions, text="Bild 3 hochladen?", variable=self.mc_var_use_image_3, onvalue=1, offvalue=0)
        self.mc_check_use_image_3_in_description.deselect()
        self.mc_check_use_image_3_in_description.grid(row=7, column=0, sticky=W, padx=90)

        # Buttons - Bild hinzufügen & Bild löschen
        self.mc_add_img_to_description_btn = Button(self.mc_frame_question_description_functions, text="Bild hinzufügen", command=lambda: mc_add_image_to_description_and_create_labels())
        self.mc_add_img_to_description_btn.grid(row=8, column=0, sticky=W, padx = 10, pady=(20,0))
        
        def mc_add_image_to_description_and_create_labels():
            # Erstelle Labels
            self.mc_question_description_img_1_filename_label = Label(self.mc_frame_description_picture, text=self.mc_description_img_name_1)
            self.mc_question_description_img_2_filename_label = Label(self.mc_frame_description_picture, text=self.mc_description_img_name_2)
            self.mc_question_description_img_3_filename_label = Label(self.mc_frame_description_picture, text=self.mc_description_img_name_3)

            self.mc_description_img_name_1, self.mc_description_img_name_2, self.mc_description_img_name_3, self.mc_description_img_path_1, self.mc_description_img_path_2, self.mc_description_img_path_3, self.mc_question_description_img_1_filename_label, self.mc_question_description_img_2_filename_label, self.mc_question_description_img_3_filename_label = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_image_to_description(
                    self,
                    self.mc_var_use_image_1.get(),
                    self.mc_var_use_image_2.get(),
                    self.mc_var_use_image_3.get(),
                    self.mc_frame_description_picture,
                    self.mc_description_img_name_1,
                    self.mc_description_img_name_2,
                    self.mc_description_img_name_3,
                    self.mc_description_img_path_1,
                    self.mc_description_img_path_2,
                    self.mc_description_img_path_3,
                    )


        self.mc_remove_img_from_description_btn = Button(self.mc_frame_question_description_functions, text="Bild entfernen", command=lambda: mc_add_image_to_description_and_delete_labels())
        self.mc_remove_img_from_description_btn.grid(row=8, column=0, sticky=W, padx=120, pady=(20,0))

        def mc_add_image_to_description_and_delete_labels():
            self.mc_description_img_name_1, self.mc_description_img_name_2, self.mc_description_img_name_3 = test_generator_modul_ilias_test_struktur.Additional_Funtions.delete_image_from_description(
                 self,
                 self.mc_var_use_image_1.get(),
                 self.mc_var_use_image_2.get(),
                 self.mc_var_use_image_3.get(),
                 self.mc_question_description_img_1_filename_label,
                 self.mc_question_description_img_2_filename_label,
                 self.mc_question_description_img_3_filename_label,
                 self.mc_description_img_name_1,
                 self.mc_description_img_name_2,
                 self.mc_description_img_name_3,
            )
            
###################### "Taxonomie Einstellungen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ################
        self.mc_taxonomy_settings_btn = Button(self.mc_frame_taxonomy_settings, text="Taxonomie-Einstellungen",command=lambda: test_generator_modul_taxonomie_und_textformatierung.Taxonomie.__init__(self))
        self.mc_taxonomy_settings_btn.grid(row=3, column=0, columnspan = 2, padx=10, sticky="W")
      
      
###################### "Fragentext Funktionen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.add_latex_term_btn = Button(self.mc_frame_question_description_functions, text="Text \"Latex\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_latex(self, self.mc_question_description_main_entry))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.mc_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sub(self, self.mc_question_description_main_entry))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_text_sup_btn = Button(self.mc_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_sup(self, self.mc_question_description_main_entry))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.mc_frame_question_description_functions, text="Text \"Kursiv\"", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.text_italic(self, self.mc_question_description_main_entry))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        self.set_postion_for_picture_1_btn = Button(self.mc_frame_question_description_functions, text="Pos. Bild 1", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_1(self, self.mc_question_description_main_entry))
        self.set_postion_for_picture_1_btn.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="W")

        self.set_postion_for_picture_2_btn = Button(self.mc_frame_question_description_functions, text="Pos. Bild 2", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_2(self, self.mc_question_description_main_entry))
        self.set_postion_for_picture_2_btn.grid(row=6, column=0, padx=10,  sticky="W")

        self.set_postion_for_picture_3_btn = Button(self.mc_frame_question_description_functions, text="Pos. Bild 3", command=lambda: test_generator_modul_taxonomie_und_textformatierung.Textformatierung.set_position_for_picture_3(self, self.mc_question_description_main_entry))
        self.set_postion_for_picture_3_btn.grid(row=7, column=0, padx=10,  sticky="W")



###################### "Fragen Attribute" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.mc_question_difficulty_label = Label(self.mc_frame_question_attributes, text="Schwierigkeit")
        self.mc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.mc_question_difficulty_entry = Entry(self.mc_frame_question_attributes, width=15)
        self.mc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.mc_question_category_label = Label(self.mc_frame_question_attributes, text="Fragenkategorie")
        self.mc_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.mc_question_category_entry = Entry(self.mc_frame_question_attributes, width=15)
        self.mc_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.mc_question_type_label = Label(self.mc_frame_question_attributes, text="Fragen-Typ")
        self.mc_question_type_label.grid(row=0, column=2, pady=5, padx=5, sticky=W)

        self.mc_question_type_entry = Entry(self.mc_frame_question_attributes, width=15)
        self.mc_question_type_entry.grid(row=0, column=3, pady=5, padx=5, sticky=W)
        self.mc_question_type_entry.insert(0, "Multiplechoice")

        self.mc_question_pool_tag_label = Label(self.mc_frame_question_attributes, text="Pool-Tag")
        self.mc_question_pool_tag_label.grid(row=1, column=2, pady=5, padx=5, sticky=W)

        self.mc_question_pool_tag_entry = Entry(self.mc_frame_question_attributes, width=15)
        self.mc_question_pool_tag_entry.grid(row=1, column=3, pady=5, padx=5, sticky=W)
      
      
###################### "Multiple Choice" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        self.mc_question_author_label = Label(self.mc_frame, text="Fragen-Autor")
        self.mc_question_author_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mc_question_author_entry = Entry(self.mc_frame, width=30)
        self.mc_question_author_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        self.mc_question_title_label = Label(self.mc_frame, text="Fragen-Titel")
        self.mc_question_title_label.grid(row=1, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mc_question_title_entry = Entry(self.mc_frame, width=60)
        self.mc_question_title_entry.grid(row=1, column=1, pady=(10, 0), sticky=W)

        self.mc_question_description_label = Label(self.mc_frame, text="Fragen-Beschreibung")
        self.mc_question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.mc_question_description_title_entry = Entry(self.mc_frame, width=60)
        self.mc_question_description_title_entry.grid(row=2, column=1, sticky=W)

        self.mc_question_textfield_label = Label(self.mc_frame, text="Fragen-Text")
        self.mc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.mc_bar = Scrollbar(self.mc_frame)
        self.mc_question_description_main_entry = Text(self.mc_frame, height=6, width=80, font=('Helvetica', 9))
        self.mc_bar.grid(row=3, column=2, sticky=W)
        self.mc_question_description_main_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.mc_bar.config(command=self.mc_question_description_main_entry.yview)
        self.mc_question_description_main_entry.config(yscrollcommand=self.mc_bar.set)

        self.mc_processing_time_label = Label(self.mc_frame, text="Bearbeitungsdauer")
        self.mc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.mc_processing_time_label = Label(self.mc_frame, text="Std:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.mc_processing_time_label = Label(self.mc_frame, text="Min:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.mc_processing_time_label = Label(self.mc_frame, text="Sek:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        self.mc_picture_preview_pixel_label = Label(self.mc_frame, text="Bild-Vorschaugröße (in Pixel)")
        self.mc_picture_preview_pixel_label.grid(row=4, column=1, sticky=E, padx=70)

        self.mc_picture_preview_pixel_entry = Entry(self.mc_frame, width=10)
        self.mc_picture_preview_pixel_entry.grid(row=4, column=1, sticky=E,  padx=0)
        self.mc_picture_preview_pixel_entry.insert(END, "300")

        ### Preview LaTeX
        # expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
        # preview(expr, viewer='file', filename='output.png')

        # file_image = ImageTk.PhotoImage(Image.open('output.png'))
        # file_image_label = Label(self.mc_frame, image=file_image)
        # file_image_label.image = file_image

        # def latex_preview():
        #    file_image_label.grid(row=20, column=1, pady=20)

        # self.myLatex_btn = Button(self.mc_frame, text="show LaTeX Preview", command=latex_preview)
        # self.myLatex_btn.grid(row=4, column=1, sticky=E)

        ###

        self.mc_processingtime_hours = list(range(24))
        self.mc_processingtime_minutes = list(range(60))
        self.mc_processingtime_seconds = list(range(60))

        self.mc_proc_hours_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_hours, width=2)
        self.mc_proc_minutes_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_minutes, width=2)
        self.mc_proc_seconds_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_seconds, width=2)

        self.mc_proc_hours_box.current(23)
        self.mc_proc_minutes_box.current(0)
        self.mc_proc_seconds_box.current(0)

        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.mc_proc_hours_box.bind("<<ComboboxSelected>>")

        self.mc_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.mc_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.mc_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.mc_mix_questions_label = Label(self.mc_frame, text="Fragen mischen")
        self.mc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.mc_var_mix_questions = StringVar()
        self.mc_check_mix_questions = Checkbutton(self.mc_frame, text="", variable=self.mc_var_mix_questions,
                                                  onvalue="1", offvalue="0")
        self.mc_check_mix_questions.deselect()
        self.mc_check_mix_questions.grid(row=5, column=1, sticky=W, pady=(5, 0))

        self.mc_response_limitation_label = Label(self.mc_frame, text="Antwortbeschränkung")
        self.mc_response_limitation_label.grid(row=6, column=0, sticky=W, padx=10, pady=(5, 0))

        self.mc_response_editor_label = Label(self.mc_frame, text="Antwort-Editor")
        self.mc_response_editor_label.grid(row=7, column=0, sticky=W, padx=10, pady=(5, 0))
        
        self.mc_response_editor_options = ["Einzeilige Antworten", "Mehrzeilige Antworten"]
        self.mc_response_editor_box = ttk.Combobox(self.mc_frame, value=self.mc_response_editor_options, width=20)
        self.mc_response_editor_box.current(0)
        self.mc_response_editor_value = 1
        def mc_selected_mix_answers_options(event):
            if self.mc_response_editor_box.get() == "Einzeilige Antworten":
                self.mc_response_editor_value = 1
            elif self.mc_response_editor_box.get() == "Mehrzeilige Antworten":
                self.mc_response_editor_value = 0

        self.mc_response_editor_box.bind("<<ComboboxSelected>>", mc_selected_mix_answers_options)
        self.mc_response_editor_box.grid(row=7, column=1, sticky=W, padx=0, pady=(5, 0))
        
        
        def mc_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

            if self.mc_numbers_of_answers_box.get() == '1':
                mc_var2_remove()
                mc_var3_remove()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()


            elif self.mc_numbers_of_answers_box.get() == '2':
                mc_var2_show()
                mc_var3_remove()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '3':
                mc_var2_show()
                mc_var3_show()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '4':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '5':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_remove()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '6':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_remove()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '7':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_show()
                mc_var8_remove()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '8':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_show()
                mc_var8_show()
                mc_var9_remove()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '9':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_show()
                mc_var8_show()
                mc_var9_show()
                mc_var10_remove()

            elif self.mc_numbers_of_answers_box.get() == '10':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_show()
                mc_var8_show()
                mc_var9_show()
                mc_var10_show()

        self.mc_numbers_of_answers_box_label = Label(self.mc_frame, text="Anzahl der Antworten")
        self.mc_numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.mc_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.mc_numbers_of_answers_box = ttk.Combobox(self.mc_frame, value=self.mc_numbers_of_answers_value, width=20)
        self.mc_numbers_of_answers_box.bind("<<ComboboxSelected>>", mc_answer_selected)
        self.mc_numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))
        self.mc_numbers_of_answers_box.current(0)

        # self.Label(self.mc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.mc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.mc_response_img_label = Label(self.mc_frame, text="Antwort-Grafik")
        self.mc_response_img_label.grid(row=8, column=1, sticky=E, padx=40)
        self.mc_response_points_correct_label = Label(self.mc_frame, text="Punkte\nausgewählt")
        self.mc_response_points_correct_label.grid(row=8, column=2, sticky=W, padx=20)
        self.mc_response_points_false_label = Label(self.mc_frame, text="Punkte\nnicht\nausgewählt")
        self.mc_response_points_false_label.grid(row=8, column=3, sticky=W, padx=20)

        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------
        
        self.mc_var1_img_data = ""
        self.mc_var2_img_data = ""
        self.mc_var3_img_data = ""
        self.mc_var3_img_data = ""
        self.mc_var4_img_data = ""
        self.mc_var5_img_data = ""
        self.mc_var6_img_data = ""
        self.mc_var7_img_data = ""
        self.mc_var8_img_data = ""
        self.mc_var9_img_data = ""
        self.mc_var10_img_data = ""
        
        self.mc_var1_img_data_encoded64_string = ""
        self.mc_var2_img_data_encoded64_string = ""
        self.mc_var3_img_data_encoded64_string = ""
        self.mc_var4_img_data_encoded64_string = ""
        self.mc_var5_img_data_encoded64_string = ""
        self.mc_var6_img_data_encoded64_string = ""
        self.mc_var7_img_data_encoded64_string = ""
        self.mc_var8_img_data_encoded64_string = ""
        self.mc_var9_img_data_encoded64_string = ""
        self.mc_var10_img_data_encoded64_string = ""

        self.mc_var1_img_data_encoded64_string = "Encoded1-Test"

        self.mc_var1_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var2_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var3_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var4_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var5_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var6_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var7_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var8_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var9_answer_entry = Entry(self.mc_frame, width=45)
        self.mc_var10_answer_entry = Entry(self.mc_frame, width=45)

        # Punkte für "Ausgewählt"
        self.mc_var1_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var2_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var3_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var4_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var5_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var6_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var7_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var8_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var9_points_correct_entry = Entry(self.mc_frame, width=8)
        self.mc_var10_points_correct_entry = Entry(self.mc_frame, width=8)

        # Punkte für "Nicht ausgewählt"
        self.mc_var1_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var2_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var3_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var4_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var5_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var6_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var7_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var8_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var9_points_false_entry = Entry(self.mc_frame, width=8)
        self.mc_var10_points_false_entry = Entry(self.mc_frame, width=8)

#######################
        
        
        self.mc_var1_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var2_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var3_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var4_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var5_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var6_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var7_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var8_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var9_img_data_entry = Entry(self.mc_frame, width=8)
        self.mc_var10_img_data_entry = Entry(self.mc_frame, width=8)
        
        


        self.mc_var1_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var2_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var3_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var4_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var5_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var6_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var7_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var8_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var9_img_path_entry = Entry(self.mc_frame, width=8)
        self.mc_var10_img_path_entry = Entry(self.mc_frame, width=8)
################
        
        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        self.mc_var1_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var1_img_label_entry, self.mc_var1_img_data_entry, self.mc_var1_img_path_entry))
        self.mc_var2_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var2_img_label_entry, self.mc_var2_img_data_entry, self.mc_var2_img_path_entry))
        self.mc_var3_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var3_img_label_entry, self.mc_var3_img_data_entry, self.mc_var3_img_path_entry))
        self.mc_var4_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var4_img_label_entry, self.mc_var4_img_data_entry, self.mc_var4_img_path_entry))
        self.mc_var5_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var5_img_label_entry, self.mc_var5_img_data_entry, self.mc_var5_img_path_entry))
        self.mc_var6_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var6_img_label_entry, self.mc_var6_img_data_entry, self.mc_var6_img_path_entry))
        self.mc_var7_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var7_img_label_entry, self.mc_var7_img_data_entry, self.mc_var7_img_path_entry))
        self.mc_var8_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var8_img_label_entry, self.mc_var8_img_data_entry, self.mc_var8_img_path_entry))
        self.mc_var9_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var9_img_label_entry, self.mc_var9_img_data_entry, self.mc_var9_img_path_entry))
        self.mc_var10_select_img_btn = Button(self.mc_frame, text="Datei wählen", command=lambda: MultipleChoice.mc_add_image_to_answer(self, self.mc_var10_img_label_entry, self.mc_var10_img_data_entry, self.mc_var10_img_path_entry))



###################### "MultipleChoice-Datenbank" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # ### LABELS
        # self.mc_delete_all_label = Label(self.mc_frame_database, text="Alle DB Einträge löschen?")
        # self.mc_delete_all_label.grid(row=5, column=0, pady=5, padx=5)
        # 
        # 
        # 
        # ### ENTRIES
        # self.mc_load_box = Entry(self.mc_frame_database, width=10)
        # self.mc_load_box.grid(row=3, column=1, sticky=W)
        # 
        # self.mc_delete_box = Entry(self.mc_frame_database, width=10)
        # self.mc_delete_box.grid(row=4, column=1, sticky=W)
        # 
        # 
        # 
        # ### BUTTONS
        # self.mc_database_save_id_to_db_multiplechoice_btn = Button(self.mc_frame_database, text="Speichern unter neuer ID", command=lambda: MultipleChoice.mc_save_id_to_db(self))
        # self.mc_database_save_id_to_db_multiplechoice_btn.grid(row=0, column=0, sticky=W, pady=5)
        # 
        # self.mc_database_save_id_to_db_multiplechoice_btn = Button(self.mc_frame_database, text="MC - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, "ilias_multiplechoice_db", "multiplechoice_table"))
        # self.mc_database_save_id_to_db_multiplechoice_btn.grid(row=1, column=0, sticky=W, pady=5)
        # 
        # self.mc_excel_import_to_db_multiplechoice_btn = Button(self.mc_frame_database, text="Excel-Datei importieren (MC)", command=lambda: MultipleChoice.mc_excel_import_to_db(self))
        # self.mc_excel_import_to_db_multiplechoice_btn.grid(row=2, column=0, sticky=W, pady=5)
        # 
        # self.mc_database_load_id_btn = Button(self.mc_frame_database, text="ID Laden", command=lambda: MultipleChoice.mc_load_id_from_db(self, self.mc_db_entry_to_index_dict))
        # self.mc_database_load_id_btn.grid(row=3, column=0, sticky=W, pady=5)
        # 
        # self.mc_database_delete_id_from_db_btn = Button(self.mc_frame_database, text="ID Löschen", command=lambda: MultipleChoice.mc_delete_id_from_db(self))
        # self.mc_database_delete_id_from_db_btn.grid(row=4, column=0, sticky=W, pady=5)
        # 
        # 
        # ### CHECKBOXES
        # self.mc_var_delete_all = IntVar()
        # self.mc_check_delete_all = Checkbutton(self.mc_frame_database, text="", variable=self.mc_var_delete_all, onvalue=1, offvalue=0)
        # self.mc_check_delete_all.deselect()
        # self.mc_check_delete_all.grid(row=5, column=1, sticky=W)

        self.mc_database_show_db_multiplechoice_btn = Button(self.mc_frame_database, text="MC - Datenbank anzeigen", command=lambda: test_generator_modul_datenbanken_anzeigen.MainGUI.__init__(self, self.database_multiplechoice_path, "multiplechoice_table"))
        self.mc_database_show_db_multiplechoice_btn.grid(row=0, column=0, sticky=W, pady=5)

        self.mc_database_save_id_to_db_multiplechoice_btn = Button(self.mc_frame_database, text="Speichern unter neuer ID", command=lambda: MultipleChoice.mc_save_id_to_db(self))
        self.mc_database_save_id_to_db_multiplechoice_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.mc_database_delete_id_from_db_btn = Button(self.mc_frame_database, text="ID Löschen", command=lambda: MultipleChoice.mc_delete_id_from_db(self))
        self.mc_database_delete_id_from_db_btn.grid(row=6, column=0, sticky=W, pady=5)
        self.mc_delete_box = Entry(self.mc_frame_database, width=10)
        self.mc_delete_box.grid(row=6, column=0, padx=80, sticky=W)

        # Noch keine Funktion
        self.mc_database_new_question_btn = Button(self.mc_frame_database, text="GUI Einträge leeren", command=lambda: MultipleChoice.mc_clear_GUI(self))
        self.mc_database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        # Noch keine Funktion
        self.mc_database_edit_btn = Button(self.mc_frame_database, text="Aktuellen Eintrag editieren", command=lambda: MultipleChoice.mc_edit_id_from_db(self))
        self.mc_database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)


        self.mc_database_load_id_btn = Button(self.mc_frame_database, text="ID Laden", command=lambda: MultipleChoice.mc_load_id_from_db(self, self.mc_db_entry_to_index_dict))
        self.mc_database_load_id_btn.grid(row=4, column=0, sticky=W, pady=(15,0))
        self.mc_load_box = Entry(self.mc_frame_database, width=10)
        self.mc_load_box.grid(row=4, column=0, sticky=W, padx=80, pady=(15,0))


        # Checkbox - "Fragentext mit Highlighting?"
        self.mc_highlight_question_text_label = Label(self.mc_frame_database, text="Fragentext mit Highlighting?")
        self.mc_highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.mc_var_highlight_question_text = IntVar()
        self.mc_check_highlight_question_text = Checkbutton(self.mc_frame_database, text="", variable=self.mc_var_highlight_question_text, onvalue=1, offvalue=0)
        self.mc_check_highlight_question_text.deselect()
        self.mc_check_highlight_question_text.grid(row=5, column=0, sticky=E)


        # Checkbox - "Alle DB Einträge löschen?"
        self.mc_delete_all_label = Label(self.mc_frame_database, text="Alle DB Einträge löschen?")
        self.mc_delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.mc_var_delete_all = IntVar()
        self.mc_check_delete_all = Checkbutton(self.mc_frame_database, text="", variable=self.mc_var_delete_all, onvalue=1, offvalue=0)
        self.mc_check_delete_all.deselect()
        self.mc_check_delete_all.grid(row=7, column=0, sticky=E)

###################### "Excel Import/Export" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################
        self.table_name = "MultipleChoice_DB_export.xlsx"


        #excel_import_btn
        self.excel_xlsx_import_btn = Button(self.mc_frame_excel_import_export, text="Excel-Datei importieren", command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_import_to_db(self, "multiplechoice", self.mc_db_entry_to_index_dict))
        self.excel_xlsx_import_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.excel_xlsx_export_btn = Button(self.mc_frame_excel_import_export, text="Datenbank exportieren",command=lambda: test_generator_modul_datenbanken_erstellen.Import_Export_Database.excel_export_to_xlsx(self, self.project_root_path, self.mc_db_entry_to_index_dict, self.database_multiplechoice_path, "multiplechoice_db.db", "multiplechoice_table", "MultipleChoice_DB_export_file.xlsx", "Multiplechoice - Database"))
        self.excel_xlsx_export_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)

        # ILIAS_testfile_import
        self.mc_import_ilias_testfile_btn = Button(self.mc_frame_excel_import_export, text="ILIAS-Datei importieren",command=lambda: test_generator_modul_ilias_import_test_datei.Import_ILIAS_Datei_in_DB.__init__(self, self.project_root_path))
        self.mc_import_ilias_testfile_btn.grid(row=2, column=1, sticky=W, pady=(20,0), padx=10)

        ##ilias test import_btn
        #self.ilias_test_import_btn = Button(self.mc_frame_excel_import_export, text="ILIAS-Test importieren",command=lambda: Database.ilias_test_to_sql_import(self))
        #self.ilias_test_import_btn.grid(row=2, column=1, sticky=W, pady=5, padx=10)


# ------------------------------- VARIABLES  - TEXT & ENTRY --------------------------------------------

        self.mc_var1_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var2_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var3_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var4_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var5_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var6_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var7_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var8_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var9_img_label_entry = Entry(self.mc_frame, width=30)
        self.mc_var10_img_label_entry = Entry(self.mc_frame, width=30)

        self.mc_answer1_label = Label(self.mc_frame, text="Antwort-Text 1")
        self.mc_answer2_label = Label(self.mc_frame, text="Antwort-Text 2")
        self.mc_answer3_label = Label(self.mc_frame, text="Antwort-Text 3")
        self.mc_answer4_label = Label(self.mc_frame, text="Antwort-Text 4")
        self.mc_answer5_label = Label(self.mc_frame, text="Antwort-Text 5")
        self.mc_answer6_label = Label(self.mc_frame, text="Antwort-Text 6")
        self.mc_answer7_label = Label(self.mc_frame, text="Antwort-Text 7")
        self.mc_answer8_label = Label(self.mc_frame, text="Antwort-Text 8")
        self.mc_answer9_label = Label(self.mc_frame, text="Antwort-Text 9")
        self.mc_answer10_label = Label(self.mc_frame, text="Antwort-Text 10")

        self.mc_answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.mc_var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.mc_var1_img_label_entry.grid(row=10, column=1, sticky=E, padx=0)
        self.mc_var1_points_correct_entry.grid(row=10, column=2)
        self.mc_var1_points_false_entry.grid(row=10, column=3)
        self.mc_var1_select_img_btn.grid(row=10, column=1, sticky=E, padx=200)


        def mc_var2_show():
            self.mc_answer2_label.grid(row=11, column=0, sticky=W, padx=30)
            self.mc_var2_answer_entry.grid(row=11, column=1, sticky=W)
            self.mc_var2_img_label_entry.grid(row=11, column=1, sticky=E, padx=0)
            self.mc_var2_points_correct_entry.grid(row=11, column=2)
            self.mc_var2_points_false_entry.grid(row=11, column=3)
            self.mc_var2_select_img_btn.grid(row=11, column=1, sticky=E, padx=200)

        def mc_var3_show():
            self.mc_answer3_label.grid(row=12, column=0, sticky=W, padx=30)
            self.mc_var3_answer_entry.grid(row=12, column=1, sticky=W)
            self.mc_var3_img_label_entry.grid(row=12, column=1, sticky=E, padx=0)
            self.mc_var3_points_correct_entry.grid(row=12, column=2)
            self.mc_var3_points_false_entry.grid(row=12, column=3)
            self.mc_var3_select_img_btn.grid(row=12, column=1, sticky=E, padx=200)

        def mc_var4_show():
            self.mc_answer4_label.grid(row=13, column=0, sticky=W, padx=30)
            self.mc_var4_answer_entry.grid(row=13, column=1, sticky=W)
            self.mc_var4_img_label_entry.grid(row=13, column=1, sticky=E, padx=0)
            self.mc_var4_points_correct_entry.grid(row=13, column=2)
            self.mc_var4_points_false_entry.grid(row=13, column=3)
            self.mc_var4_select_img_btn.grid(row=13, column=1, sticky=E, padx=200)

        def mc_var5_show():
            self.mc_answer5_label.grid(row=14, column=0, sticky=W, padx=30)
            self.mc_var5_answer_entry.grid(row=14, column=1, sticky=W)
            self.mc_var5_img_label_entry.grid(row=14, column=1, sticky=E, padx=0)
            self.mc_var5_points_correct_entry.grid(row=14, column=2)
            self.mc_var5_points_false_entry.grid(row=14, column=3)
            self.mc_var5_select_img_btn.grid(row=14, column=1, sticky=E, padx=200)

        def mc_var6_show():
            self.mc_answer6_label.grid(row=15, column=0, sticky=W, padx=30)
            self.mc_var6_answer_entry.grid(row=15, column=1, sticky=W)
            self.mc_var6_img_label_entry.grid(row=15, column=1, sticky=E, padx=0)
            self.mc_var6_points_correct_entry.grid(row=15, column=2)
            self.mc_var6_points_false_entry.grid(row=15, column=3)
            self.mc_var6_select_img_btn.grid(row=15, column=1, sticky=E, padx=200)

        def mc_var7_show():
            self.mc_answer7_label.grid(row=16, column=0, sticky=W, padx=30)
            self.mc_var7_answer_entry.grid(row=16, column=1, sticky=W)
            self.mc_var7_img_label_entry.grid(row=16, column=1, sticky=E, padx=0)
            self.mc_var7_points_correct_entry.grid(row=16, column=2 )
            self.mc_var7_points_false_entry.grid(row=16, column=3)
            self.mc_var7_select_img_btn.grid(row=16, column=1, sticky=E, padx=200)

        def mc_var8_show():
            self.mc_answer8_label.grid(row=17, column=0, sticky=W, padx=30)
            self.mc_var8_answer_entry.grid(row=17, column=1, sticky=W)
            self.mc_var8_img_label_entry.grid(row=17, column=1, sticky=E, padx=0)
            self.mc_var8_points_correct_entry.grid(row=17, column=2)
            self.mc_var8_points_false_entry.grid(row=17, column=3)
            self.mc_var8_select_img_btn.grid(row=17, column=1, sticky=E, padx=200)

        def mc_var9_show():
            self.mc_answer9_label.grid(row=18, column=0, sticky=W, padx=30)
            self.mc_var9_answer_entry.grid(row=18, column=1, sticky=W)
            self.mc_var9_img_label_entry.grid(row=18, column=1, sticky=E, padx=0)
            self.mc_var9_points_correct_entry.grid(row=18, column=2)
            self.mc_var9_points_false_entry.grid(row=18, column=3)
            self.mc_var9_select_img_btn.grid(row=18, column=1, sticky=E, padx=200)

        def mc_var10_show():
            self.mc_answer10_label.grid(row=19, column=0, sticky=W, padx=30)
            self.mc_var10_answer_entry.grid(row=19, column=1, sticky=W)
            self.mc_var10_img_label_entry.grid(row=19, column=1, sticky=E, padx=0)
            self.mc_var10_points_correct_entry.grid(row=19, column=2)
            self.mc_var10_points_false_entry.grid(row=19, column=3)
            self.mc_var10_select_img_btn.grid(row=19, column=1, sticky=E, padx=200)



        def mc_var2_remove():
            self.mc_answer2_label.grid_remove()
            self.mc_var2_answer_entry.grid_remove()
            self.mc_var2_img_label_entry.grid_remove()
            self.mc_var2_points_correct_entry.grid_remove()
            self.mc_var2_points_false_entry.grid_remove()
            self.mc_var2_select_img_btn.grid_remove()

        def mc_var3_remove():
            self.mc_answer3_label.grid_remove()
            self.mc_var3_answer_entry.grid_remove()
            self.mc_var3_img_label_entry.grid_remove()
            self.mc_var3_points_correct_entry.grid_remove()
            self.mc_var3_points_false_entry.grid_remove()
            self.mc_var3_select_img_btn.grid_remove()

        def mc_var4_remove():
            self.mc_answer4_label.grid_remove()
            self.mc_var4_answer_entry.grid_remove()
            self.mc_var4_img_label_entry.grid_remove()
            self.mc_var4_points_correct_entry.grid_remove()
            self.mc_var4_points_false_entry.grid_remove()
            self.mc_var4_select_img_btn.grid_remove()

        def mc_var5_remove():
            self.mc_answer5_label.grid_remove()
            self.mc_var5_answer_entry.grid_remove()
            self.mc_var5_img_label_entry.grid_remove()
            self.mc_var5_points_correct_entry.grid_remove()
            self.mc_var5_points_false_entry.grid_remove()
            self.mc_var5_select_img_btn.grid_remove()

        def mc_var6_remove():
            self.mc_answer6_label.grid_remove()
            self.mc_var6_answer_entry.grid_remove()
            self.mc_var6_img_label_entry.grid_remove()
            self.mc_var6_points_correct_entry.grid_remove()
            self.mc_var6_points_false_entry.grid_remove()
            self.mc_var6_select_img_btn.grid_remove()

        def mc_var7_remove():
            self.mc_answer7_label.grid_remove()
            self.mc_var7_answer_entry.grid_remove()
            self.mc_var7_img_label_entry.grid_remove()
            self.mc_var7_points_correct_entry.grid_remove()
            self.mc_var7_points_false_entry.grid_remove()
            self.mc_var7_select_img_btn.grid_remove()

        def mc_var8_remove():
            self.mc_answer8_label.grid_remove()
            self.mc_var8_answer_entry.grid_remove()
            self.mc_var8_img_label_entry.grid_remove()
            self.mc_var8_points_correct_entry.grid_remove()
            self.mc_var8_points_false_entry.grid_remove()
            self.mc_var8_select_img_btn.grid_remove()

        def mc_var9_remove():
            self.mc_answer9_label.grid_remove()
            self.mc_var9_answer_entry.grid_remove()
            self.mc_var9_img_label_entry.grid_remove()
            self.mc_var9_points_correct_entry.grid_remove()
            self.mc_var9_points_false_entry.grid_remove()
            self.mc_var9_select_img_btn.grid_remove()

        def mc_var10_remove():
            self.mc_answer10_label.grid_remove()
            self.mc_var10_answer_entry.grid_remove()
            self.mc_var10_img_label_entry.grid_remove()
            self.mc_var10_points_correct_entry.grid_remove()
            self.mc_var10_points_false_entry.grid_remove()
            self.mc_var10_select_img_btn.grid_remove()

 

        ######  VARIABLES
        self.mc_var1_img_data_encoded64_string = ""
        self.mc_var2_img_data_encoded64_string = ""
        self.mc_var3_img_data_encoded64_string = ""
        self.mc_var4_img_data_encoded64_string = ""
        self.mc_var5_img_data_encoded64_string = ""
        self.mc_var6_img_data_encoded64_string = ""
        self.mc_var7_img_data_encoded64_string = ""
        self.mc_var8_img_data_encoded64_string = ""
        self.mc_var9_img_data_encoded64_string = ""
        self.mc_var10_img_data_encoded64_string = ""




 ###################### "MultipleChoice-Test erstellen" - FRAME   -------- LABELS / ENTRYS / BUTTONS  ###################

        # self.create_multiplechoice_test_btn = Button(self.mc_frame_create_multiplechoice_test, text="MC-Test erstellen", command=lambda:  Create_MultipleChoice_Test.__init__(self, self.mc_db_entry_to_index_dict))
        # self.create_multiplechoice_test_btn.grid(row=2, column=0, sticky=W)
        # self.create_multiplechoice_test_entry = Entry(self.mc_frame_create_multiplechoice_test, width=15)
        # self.create_multiplechoice_test_entry.grid(row=2, column=1, sticky=W, padx=20)
        # 
        # self.create_multiplechoice_pool_btn = Button(self.mc_frame_create_multiplechoice_test, text="MC-Pool erstellen", command=lambda: Create_MultipleChoice_Pool.__init__(self, self.mc_db_entry_to_index_dict))
        # self.create_multiplechoice_pool_btn.grid(row=3, column=0, sticky=W, pady=10)
        # self.create_multiplechoice_pool_entry = Entry(self.mc_frame_create_multiplechoice_test, width=15)
        # self.create_multiplechoice_pool_entry.grid(row=3, column=1, sticky=W, padx=20, pady=10)
        
        # Button "multiplechoice-Test erstellen"
        self.create_multiplechoice_test_btn = Button(self.mc_frame_create_multiplechoice_test, text="MC-Test erstellen", command=lambda: Create_MultipleChoice_Test.__init__(self, self.mc_db_entry_to_index_dict))
        self.create_multiplechoice_test_btn.grid(row=0, column=0, sticky=W)
        self.create_multiplechoice_test_entry = Entry(self.mc_frame_create_multiplechoice_test, width=15)
        self.create_multiplechoice_test_entry.grid(row=0, column=1, sticky=W, padx=0)

        # Checkbox "Test-Einstellungen übernehmen?"
        self.create_test_settings_label = Label(self.mc_frame_create_multiplechoice_test, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)
        self.var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.mc_frame_create_multiplechoice_test, text="", variable=self.var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)

        # Checkbox "Latex für Fragentext nutzen?"
        self.mc_use_latex_on_text_label = Label(self.mc_frame_create_multiplechoice_test, text="Latex für Fragentext nutzen?")
        self.mc_use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)
        self.mc_var_use_latex_on_text_check = IntVar()
        self.mc_use_latex_on_text_check = Checkbutton(self.mc_frame_create_multiplechoice_test, text="", variable=self.mc_var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.mc_use_latex_on_text_check.deselect()
        self.mc_use_latex_on_text_check.grid(row=2, column=1, sticky=W)


        # Checkbox "Alle Einträge aus der DB erzeugen?"
        self.mc_create_question_pool_all_label = Label(self.mc_frame_create_multiplechoice_test, text="Alle Einträge aus der DB erzeugen?")
        self.mc_create_question_pool_all_label.grid(row=4, column=0, pady=(10,0), padx=5, sticky=W)
        self.mc_var_create_question_pool_all_check = IntVar()
        self.mc_create_question_pool_all = Checkbutton(self.mc_frame_create_multiplechoice_test, text="", variable=self.mc_var_create_question_pool_all_check, onvalue=1, offvalue=0)
        #self.mc_var_create_question_pool_all_check.set(0)
        self.mc_create_question_pool_all.grid(row=4, column=1, sticky=W, pady=(10,0))



        # Button "multiplechoice-Fragenpool erstellen"
        self.create_multiplechoice_pool_btn = Button(self.mc_frame_create_multiplechoice_test, text="MC-Pool erstellen", command=lambda: Create_MultipleChoice_Pool.__init__(self, self.mc_db_entry_to_index_dict, self.mc_var_create_question_pool_all_check.get()))
        self.create_multiplechoice_pool_btn.grid(row=3, column=0, sticky=W, pady=(30,0))
        self.create_multiplechoice_pool_entry = Entry(self.mc_frame_create_multiplechoice_test, width=15)
        self.create_multiplechoice_pool_entry.grid(row=3, column=1, sticky=W, padx=0, pady=(30,0))



    # Funktion dient zur Auswahl von Bildern für einzelne Antwortmöglichkeiten
    def mc_add_image_to_answer(self, picture_label_entry, picture_data_entry, picture_path_entry):


        ### Dateipfad auswählen
        self.mc_picture_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")

        # "rindex" sucht nach einem bestimmten Zeichen in einem String, beginnend von rechts
        self.mc_picture_name = self.mc_picture_path[self.mc_picture_path.rindex('/')+1:]        # Nach dem "/" befindet sich der Dateiname
        self.mc_image_format = self.mc_picture_path[self.mc_picture_path.rindex('.'):]          # Nach dem "." befindet sich das Dateiformat z.B. .jpg



        ### Bild-Namen in entsprechendes, geleertes, Eingabefeld übertragen
        picture_label_entry.delete(0, END)
        picture_label_entry.insert(0, str(self.mc_picture_name))
        
        ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
        # "encoded64_string_raw enthält die Daten als String in der Form b'String'
        # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
        # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen
        with open(self.mc_picture_path, "rb") as image_file:
            encoded64_string_raw = base64.b64encode(image_file.read())
            picture_data_entry.delete(0, END)
            picture_data_entry.insert(END, encoded64_string_raw.decode('utf-8'))
            picture_path_entry.delete(0, END)
            picture_path_entry.insert(END, self.mc_picture_path )




    # Funktion "läd" die Datei in die XML. Das Bild wird codiert und als String in die XML geschrieben.
    # Eine kleine Vorschau zeigt das ausgewählte Bild an

    def mc_save_id_to_db(self):
        conn = sqlite3.connect(self.database_multiplechoice_path)
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.mc_test_time = "P0Y0M0DT" + self.mc_proc_hours_box.get() + "H" + self.mc_proc_minutes_box.get() + "M" + self.mc_proc_seconds_box.get() + "S"
        
        # Bild 1
        if self.mc_description_img_name_1!= "EMPTY":
            # read image data in byte format
            print(self.mc_description_img_name_1)
            print(self.mc_description_img_path_1)
            with open(self.mc_description_img_path_1, 'rb') as image_file_1:
                self.mc_description_img_data_1 = image_file_1.read()

        else:
            self.mc_description_img_name_1= "EMPTY"
            self.mc_description_img_path_1 = "EMPTY"
            self.mc_description_img_data_1 = "EMPTY"


        # Bild 2
        if self.mc_description_img_name_2!= "EMPTY":
            # read image data in byte format
            print(self.mc_description_img_name_2)
            print(self.mc_description_img_path_2)
            with open(self.mc_description_img_path_2, 'rb') as image_file_2:
                self.mc_description_img_data_2 = image_file_2.read()

        else:
            self.mc_description_img_name_2 = "EMPTY"
            self.mc_description_img_path_2 = "EMPTY"
            self.mc_description_img_data_2 = "EMPTY"


        # Bild 3
        if self.mc_description_img_name_3 != "EMPTY":

            # read image data in byte format
            print(self.mc_description_img_name_3)
            print(self.mc_description_img_path_3)
            with open(self.mc_description_img_path_3, 'rb') as image_file_3:
                self.mc_description_img_data_3 = image_file_3.read()

        else:
            self.mc_description_img_name_3 = "EMPTY"
            self.mc_description_img_path_3 = "EMPTY"
            self.mc_description_img_data_3 = "EMPTY"
        
        def mc_bind_value_for_empty_answer_image(picture_label_entry, picture_data_entry, picture_path_entry):
            if picture_label_entry.get() == "":
                picture_label_entry.insert(0, "EMPTY")
                picture_data_entry.insert(0, "EMPTY")
                picture_path_entry.insert(0, "EMPTY")

        mc_bind_value_for_empty_answer_image(self.mc_var1_img_label_entry, self.mc_var1_img_data_entry, self.mc_var1_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var2_img_label_entry, self.mc_var2_img_data_entry, self.mc_var2_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var3_img_label_entry, self.mc_var3_img_data_entry, self.mc_var3_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var4_img_label_entry, self.mc_var4_img_data_entry, self.mc_var4_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var5_img_label_entry, self.mc_var5_img_data_entry, self.mc_var5_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var6_img_label_entry, self.mc_var6_img_data_entry, self.mc_var6_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var7_img_label_entry, self.mc_var7_img_data_entry, self.mc_var7_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var8_img_label_entry, self.mc_var8_img_data_entry, self.mc_var8_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var9_img_label_entry, self.mc_var9_img_data_entry, self.mc_var9_img_path_entry)
        mc_bind_value_for_empty_answer_image(self.mc_var10_img_label_entry, self.mc_var10_img_data_entry, self.mc_var10_img_path_entry)
        
        # Insert into Table
        # Reihenfolge muss mit der Datenbank übereinstimmen
        c.execute(
            "INSERT INTO multiplechoice_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":response_1_text, :response_1_pts_correct_answer, :response_1_pts_false_answer, :response_1_img_label, :response_1_img_string_base64_encoded, :response_1_img_path,"
            ":response_2_text, :response_2_pts_correct_answer, :response_2_pts_false_answer, :response_2_img_label, :response_2_img_string_base64_encoded, :response_2_img_path,"
            ":response_3_text, :response_3_pts_correct_answer, :response_3_pts_false_answer, :response_3_img_label, :response_3_img_string_base64_encoded, :response_3_img_path,"
            ":response_4_text, :response_4_pts_correct_answer, :response_4_pts_false_answer, :response_4_img_label, :response_4_img_string_base64_encoded, :response_4_img_path,"
            ":response_5_text, :response_5_pts_correct_answer, :response_5_pts_false_answer, :response_5_img_label, :response_5_img_string_base64_encoded, :response_5_img_path,"
            ":response_6_text, :response_6_pts_correct_answer, :response_6_pts_false_answer, :response_6_img_label, :response_6_img_string_base64_encoded, :response_6_img_path,"
            ":response_7_text, :response_7_pts_correct_answer, :response_7_pts_false_answer, :response_7_img_label, :response_7_img_string_base64_encoded, :response_7_img_path,"
            ":response_8_text, :response_8_pts_correct_answer, :response_8_pts_false_answer, :response_8_img_label, :response_8_img_string_base64_encoded, :response_8_img_path,"
            ":response_9_text, :response_9_pts_correct_answer, :response_9_pts_false_answer, :response_9_img_label, :response_9_img_string_base64_encoded, :response_9_img_path,"
            ":response_10_text, :response_10_pts_correct_answer, :response_10_pts_false_answer, :response_10_img_label, :response_10_img_string_base64_encoded, :response_10_img_path,"
            ":picture_preview_pixel, "
            ":description_img_name_1, :description_img_data_1, :description_img_path_1, "
            ":description_img_name_2, :description_img_data_2, :description_img_path_2, "
            ":description_img_name_3, :description_img_data_3, :description_img_path_3, "
            ":test_time, :var_number, :question_pool_tag, :question_author)",
            {
                'question_difficulty': self.mc_question_difficulty_entry.get(),
                'question_category': self.mc_question_category_entry.get(),
                'question_type': self.mc_question_type_entry.get(),

                'question_title': self.mc_question_title_entry.get(),
                'question_description_title': self.mc_question_description_title_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.mc_question_description_main_entry.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'response_1_text': self.mc_var1_answer_entry.get(),
                'response_1_pts_correct_answer': self.mc_var1_points_correct_entry.get(),
                'response_1_pts_false_answer': self.mc_var1_points_false_entry.get(),
                'response_1_img_label': self.mc_var1_img_label_entry.get(),
                'response_1_img_string_base64_encoded':  self.mc_var1_img_data_entry.get(),
                'response_1_img_path': self.mc_var1_img_path_entry.get(),

                'response_2_text': self.mc_var2_answer_entry.get(),
                'response_2_pts_correct_answer': self.mc_var2_points_correct_entry.get(),
                'response_2_pts_false_answer': self.mc_var2_points_false_entry.get(),
                'response_2_img_label': self.mc_var2_img_label_entry.get(),
                'response_2_img_string_base64_encoded':  self.mc_var2_img_data_entry.get(),
                'response_2_img_path': self.mc_var2_img_path_entry.get(),

                'response_3_text': self.mc_var3_answer_entry.get(),
                'response_3_pts_correct_answer': self.mc_var3_points_correct_entry.get(),
                'response_3_pts_false_answer': self.mc_var3_points_false_entry.get(),
                'response_3_img_label': self.mc_var3_img_label_entry.get(),
                'response_3_img_string_base64_encoded':  self.mc_var3_img_data_entry.get(),
                'response_3_img_path': self.mc_var3_img_path_entry.get(),

                'response_4_text': self.mc_var4_answer_entry.get(),
                'response_4_pts_correct_answer': self.mc_var4_points_correct_entry.get(),
                'response_4_pts_false_answer': self.mc_var4_points_false_entry.get(),
                'response_4_img_label': self.mc_var4_img_label_entry.get(),
                'response_4_img_string_base64_encoded':  self.mc_var4_img_data_entry.get(),
                'response_4_img_path': self.mc_var4_img_path_entry.get(),

                'response_5_text': self.mc_var5_answer_entry.get(),
                'response_5_pts_correct_answer': self.mc_var5_points_correct_entry.get(),
                'response_5_pts_false_answer': self.mc_var5_points_false_entry.get(),
                'response_5_img_label': self.mc_var5_img_label_entry.get(),
                'response_5_img_string_base64_encoded':  self.mc_var5_img_data_entry.get(),
                'response_5_img_path': self.mc_var5_img_path_entry.get(),

                'response_6_text': self.mc_var6_answer_entry.get(),
                'response_6_pts_correct_answer': self.mc_var6_points_correct_entry.get(),
                'response_6_pts_false_answer': self.mc_var6_points_false_entry.get(),
                'response_6_img_label': self.mc_var6_img_label_entry.get(),
                'response_6_img_string_base64_encoded':  self.mc_var6_img_data_entry.get(),
                'response_6_img_path': self.mc_var6_img_path_entry.get(),

                'response_7_text': self.mc_var7_answer_entry.get(),
                'response_7_pts_correct_answer': self.mc_var7_points_correct_entry.get(),
                'response_7_pts_false_answer': self.mc_var7_points_false_entry.get(),
                'response_7_img_label': self.mc_var7_img_label_entry.get(),
                'response_7_img_string_base64_encoded':  self.mc_var7_img_data_entry.get(),
                'response_7_img_path': self.mc_var7_img_path_entry.get(),

                'response_8_text': self.mc_var8_answer_entry.get(),
                'response_8_pts_correct_answer': self.mc_var8_points_correct_entry.get(),
                'response_8_pts_false_answer': self.mc_var8_points_false_entry.get(),
                'response_8_img_label': self.mc_var8_img_label_entry.get(),
                'response_8_img_string_base64_encoded':  self.mc_var8_img_data_entry.get(),
                'response_8_img_path': self.mc_var8_img_path_entry.get(),

                'response_9_text': self.mc_var9_answer_entry.get(),
                'response_9_pts_correct_answer': self.mc_var9_points_correct_entry.get(),
                'response_9_pts_false_answer': self.mc_var9_points_false_entry.get(),
                'response_9_img_label': self.mc_var9_img_label_entry.get(),
                'response_9_img_string_base64_encoded':  self.mc_var9_img_data_entry.get(),
                'response_9_img_path': self.mc_var9_img_path_entry.get(),

                'response_10_text': self.mc_var10_answer_entry.get(),
                'response_10_pts_correct_answer': self.mc_var10_points_correct_entry.get(),
                'response_10_pts_false_answer': self.mc_var10_points_false_entry.get(),
                'response_10_img_label': self.mc_var10_img_label_entry.get(),
                'response_10_img_string_base64_encoded':  self.mc_var10_img_data_entry.get(),
                'response_10_img_path': self.mc_var10_img_path_entry.get(),

                'picture_preview_pixel': self.mc_picture_preview_pixel_entry.get(),

                'description_img_name_1': self.mc_description_img_name_1,
                'description_img_data_1': self.mc_description_img_data_1,
                'description_img_path_1': self.mc_description_img_path_1,

                'description_img_name_2': self.mc_description_img_name_2,
                'description_img_data_2': self.mc_description_img_data_2,
                'description_img_path_2': self.mc_description_img_path_2,

                'description_img_name_3': self.mc_description_img_name_3,
                'description_img_data_3': self.mc_description_img_data_3,
                'description_img_path_3': self.mc_description_img_path_3,

                'test_time': self.mc_test_time,

                'var_number': "",
                'question_pool_tag': self.mc_question_pool_tag_entry.get(),
                'question_author': self.mc_question_author_entry.get()

            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die MultipleChoice-Datenbank --> Fragentitel: " + str(self.mc_question_title_entry.get()))


    def mc_load_id_from_db(self, entry_to_index_dict):
        self.mc_db_entry_to_index_dict = entry_to_index_dict
        conn = sqlite3.connect(self.database_multiplechoice_path)
        c = conn.cursor()
        record_id = self.mc_load_box.get()
        c.execute("SELECT * FROM multiplechoice_table WHERE oid =" + record_id)
        mc_db_records = c.fetchall()


        MultipleChoice.mc_clear_GUI(self)

        for mc_db_record in mc_db_records:
            print("TEST")
            print(mc_db_record)
            print(self.mc_db_entry_to_index_dict['question_difficulty'])
            print(mc_db_record[self.mc_db_entry_to_index_dict['question_difficulty']])

            self.mc_question_difficulty_entry.insert(END,  mc_db_record[self.mc_db_entry_to_index_dict['question_difficulty']] )
            self.mc_question_category_entry.insert(END,  mc_db_record[self.mc_db_entry_to_index_dict['question_category']] )
            self.mc_question_type_entry.insert(END,  mc_db_record[self.mc_db_entry_to_index_dict['question_type']] )

            self.mc_question_title_entry.insert(END,  mc_db_record[self.mc_db_entry_to_index_dict['question_title']] )
            self.mc_question_description_title_entry.insert(END,  mc_db_record[self.mc_db_entry_to_index_dict['question_description_title']] )
            self.mc_question_description_main_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['question_description_main']] )

            self.mc_var1_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_1_text']] )
            self.mc_var2_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_2_text']] )
            self.mc_var3_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_3_text']] )
            self.mc_var4_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_4_text']] )
            self.mc_var5_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_5_text']] )
            self.mc_var6_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_6_text']] )
            self.mc_var7_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_7_text']] )
            self.mc_var8_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_8_text']] )
            self.mc_var9_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_9_text']] )
            self.mc_var10_answer_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_10_text']])

            self.mc_var1_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_1_img_label']])
            self.mc_var2_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_2_img_label']])
            self.mc_var3_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_3_img_label']])
            self.mc_var4_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_4_img_label']])
            self.mc_var5_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_5_img_label']])
            self.mc_var6_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_6_img_label']])
            self.mc_var7_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_7_img_label']])
            self.mc_var8_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_8_img_label']])
            self.mc_var9_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_9_img_label']])
            self.mc_var10_img_label_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_10_img_label']])

            self.mc_var1_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_1_pts_correct_answer']])
            self.mc_var2_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_2_pts_correct_answer']])
            self.mc_var3_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_3_pts_correct_answer']])
            self.mc_var4_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_4_pts_correct_answer']])
            self.mc_var5_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_5_pts_correct_answer']])
            self.mc_var6_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_6_pts_correct_answer']])
            self.mc_var7_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_7_pts_correct_answer']])
            self.mc_var8_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_8_pts_correct_answer']])
            self.mc_var9_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_9_pts_correct_answer']])
            self.mc_var10_points_correct_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_10_pts_correct_answer']])
            
            self.mc_var1_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_1_pts_false_answer']])
            self.mc_var2_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_2_pts_false_answer']])
            self.mc_var3_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_3_pts_false_answer']])
            self.mc_var4_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_4_pts_false_answer']])
            self.mc_var5_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_5_pts_false_answer']])
            self.mc_var6_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_6_pts_false_answer']])
            self.mc_var7_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_7_pts_false_answer']])
            self.mc_var8_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_8_pts_false_answer']])
            self.mc_var9_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_9_pts_false_answer']])
            self.mc_var10_points_false_entry.insert(END, mc_db_record[self.mc_db_entry_to_index_dict['response_10_pts_false_answer']])


        conn.commit()
        conn.close()

    def mc_delete_id_from_db(self):

        self.mc_delete_box_id = ""
        self.mc_delete_box_id = self.mc_delete_box.get()

        test_generator_modul_datenbanken_erstellen.Delete_Entry_from_Database.__init__(self, self.mc_delete_box_id, "multiplechoice", self.mc_var_delete_all.get(), self.project_root_path, self.mc_db_entry_to_index_dict, self.database_multiplechoice_path, "multiplechoice_table", "MultipleChoice_DB_export_file.xlsx", "Multiplechoice - Database")
        
        self.mc_delete_box.delete(0, END)

    def mc_clear_GUI(self):
        self.mc_question_difficulty_entry.delete(0, END)
        self.mc_question_category_entry.delete(0, END)
        #self.mc_question_type_entry.delete(0, END)

        self.mc_question_title_entry.delete(0, END)
        self.mc_question_description_title_entry.delete(0, END)
        self.mc_question_description_main_entry.delete('1.0', 'end-1c')

        self.mc_var1_answer_entry.delete(0, END)
        self.mc_var2_answer_entry.delete(0, END)
        self.mc_var3_answer_entry.delete(0, END)
        self.mc_var4_answer_entry.delete(0, END)
        self.mc_var5_answer_entry.delete(0, END)
        self.mc_var6_answer_entry.delete(0, END)
        self.mc_var7_answer_entry.delete(0, END)
        self.mc_var8_answer_entry.delete(0, END)
        self.mc_var9_answer_entry.delete(0, END)
        self.mc_var10_answer_entry.delete(0, END)

        self.mc_var1_img_label_entry.delete(0, END)
        self.mc_var2_img_label_entry.delete(0, END)
        self.mc_var3_img_label_entry.delete(0, END)
        self.mc_var4_img_label_entry.delete(0, END)
        self.mc_var5_img_label_entry.delete(0, END)
        self.mc_var6_img_label_entry.delete(0, END)
        self.mc_var7_img_label_entry.delete(0, END)
        self.mc_var8_img_label_entry.delete(0, END)
        self.mc_var9_img_label_entry.delete(0, END)
        self.mc_var10_img_label_entry.delete(0, END)

        self.mc_var1_points_correct_entry.delete(0, END)
        self.mc_var2_points_correct_entry.delete(0, END)
        self.mc_var3_points_correct_entry.delete(0, END)
        self.mc_var4_points_correct_entry.delete(0, END)
        self.mc_var5_points_correct_entry.delete(0, END)
        self.mc_var6_points_correct_entry.delete(0, END)
        self.mc_var7_points_correct_entry.delete(0, END)
        self.mc_var8_points_correct_entry.delete(0, END)
        self.mc_var9_points_correct_entry.delete(0, END)
        self.mc_var10_points_correct_entry.delete(0, END)

        self.mc_var1_points_false_entry.delete(0, END)
        self.mc_var2_points_false_entry.delete(0, END)
        self.mc_var3_points_false_entry.delete(0, END)
        self.mc_var4_points_false_entry.delete(0, END)
        self.mc_var5_points_false_entry.delete(0, END)
        self.mc_var6_points_false_entry.delete(0, END)
        self.mc_var7_points_false_entry.delete(0, END)
        self.mc_var8_points_false_entry.delete(0, END)
        self.mc_var9_points_false_entry.delete(0, END)
        self.mc_var10_points_false_entry.delete(0, END)



class Create_MultipleChoice_Questions(MultipleChoice):
    def __init__(self, db_entry_to_index_dict, ids_in_entry_box, question_type_test_or_pool, pool_img_dir, ilias_id_pool_qpl_dir, xml_read_qti_template_path, xml_qti_output_file_path, xml_qpl_output_file_path, max_id_pool_qti_xml, max_id, taxonomy_file_question_pool):

        self.mc_db_entry_to_index_dict = db_entry_to_index_dict
        self.mc_test_entry_splitted = ids_in_entry_box.split(",")
        self.qti_file_path_output = xml_qti_output_file_path
        self.multiplechoice_pool_qpl_file_path_output = xml_qpl_output_file_path
        self.mc_mytree = ET.parse(xml_read_qti_template_path)
        self.mc_myroot = self.mc_mytree.getroot()
        self.mc_question_type_test_or_pool = question_type_test_or_pool
        self.multiplechoice_pool_img_file_path = pool_img_dir           # Wird nur bei Erstellung eines Fragen-Pool verwendet. Ordnername wird erst bei Laufzeit erstellt)
        
        self.all_entries_from_db_list = []
        self.number_of_entrys = []

        self.mc_question_pool_id_list = []
        self.mc_question_title_list = []

        self.mc_ilias_id_pool_qpl_dir = ilias_id_pool_qpl_dir
        self.mc_file_max_id = max_id
        self.mc_taxonomy_file_question_pool = taxonomy_file_question_pool
        self.mc_ilias_id_pool_qti_xml = max_id_pool_qti_xml



        print("\n")

        if self.mc_question_type_test_or_pool == "question_test":
            print("MULTIPLECHOICE: ILIAS-TEST WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))

        else:
            print("MULTIPLECHOICE: ILIAS-POOL WIRD ERSTELLT...  ID: " + str(ids_in_entry_box))



        # Mit MC_Datenbank verknüpfen
        connect_mc_db = sqlite3.connect(self.database_multiplechoice_path)
        cursor = connect_mc_db.cursor()


        # Sämtliche Datenbank Einträge auslesen mit der entsprechenden "oid" (Datenbank ID)
        # Datenbank ID wird automatisch bei einem neuen Eintrag erstellt (fortlaufend) und kann nicht beeinflusst werden
        cursor.execute("SELECT *, oid FROM multiplechoice_table")
        mc_db_records = cursor.fetchall()

        for i in range(len(self.mc_test_entry_splitted)):
            for mc_db_record in mc_db_records:
                if str(mc_db_record[len(mc_db_record) - 1]) == self.mc_test_entry_splitted[i]:
                    for t in range(len(mc_db_record)):
                        if mc_db_record[self.mc_db_entry_to_index_dict['question_type']].lower() == "multiplechoice" or mc_db_record[self.mc_db_entry_to_index_dict['question_type']].lower() == "multiple choice":
                            
                            # an "db_record[self.sc_db_entry_to_index_dict['question_description_main']]"
                            # darf kein extra "replace('&', "&amp;")",
                            # da bei der Bearbeitung der Frage noch die "&" replaced werden.
                            
                            self.mc_question_difficulty                     = mc_db_record[self.mc_db_entry_to_index_dict['question_difficulty']]
                            self.mc_question_category                       = mc_db_record[self.mc_db_entry_to_index_dict['question_category']]
                            self.mc_question_type                           = mc_db_record[self.mc_db_entry_to_index_dict['question_type']]
                            self.mc_question_title                          = mc_db_record[self.mc_db_entry_to_index_dict['question_title']].replace('&', "&amp;")
                            self.mc_question_description_title              = mc_db_record[self.mc_db_entry_to_index_dict['question_description_title']].replace('&', "&amp;")
                            self.mc_question_description_main               = mc_db_record[self.mc_db_entry_to_index_dict['question_description_main']]
                           
                            self.mc_response_1_text                         = mc_db_record[self.mc_db_entry_to_index_dict['response_1_text']].replace('&', "&amp;")
                            self.mc_response_1_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_1_pts_correct_answer']]
                            self.mc_response_1_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_1_pts_false_answer']]
                            self.mc_response_1_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_1_img_label']].replace('&', "&amp;")
                            self.mc_response_1_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_1_img_string_base64_encoded']]
                            self.mc_response_1_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_1_img_path']]
                            
                            self.mc_response_2_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_2_text']].replace('&', "&amp;")
                            self.mc_response_2_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_2_pts_correct_answer']]
                            self.mc_response_2_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_2_pts_false_answer']]
                            self.mc_response_2_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_2_img_label']].replace('&', "&amp;")
                            self.mc_response_2_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_2_img_string_base64_encoded']]
                            self.mc_response_2_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_2_img_path']]
                            
                            self.mc_response_3_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_3_text']].replace('&', "&amp;")
                            self.mc_response_3_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_3_pts_correct_answer']]
                            self.mc_response_3_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_3_pts_false_answer']]
                            self.mc_response_3_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_3_img_label']].replace('&', "&amp;")
                            self.mc_response_3_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_3_img_string_base64_encoded']]
                            self.mc_response_3_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_3_img_path']]
                            
                            self.mc_response_4_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_4_text']].replace('&', "&amp;")
                            self.mc_response_4_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_4_pts_correct_answer']]
                            self.mc_response_4_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_4_pts_false_answer']]
                            self.mc_response_4_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_4_img_label']].replace('&', "&amp;")
                            self.mc_response_4_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_4_img_string_base64_encoded']]
                            self.mc_response_4_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_4_img_path']]
                            
                            self.mc_response_5_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_5_text']].replace('&', "&amp;")
                            self.mc_response_5_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_5_pts_correct_answer']]
                            self.mc_response_5_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_5_pts_false_answer']]
                            self.mc_response_5_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_5_img_label']].replace('&', "&amp;")
                            self.mc_response_5_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_5_img_string_base64_encoded']]
                            self.mc_response_5_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_5_img_path']]
                            
                            self.mc_response_6_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_6_text']].replace('&', "&amp;")
                            self.mc_response_6_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_6_pts_correct_answer']]
                            self.mc_response_6_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_6_pts_false_answer']]
                            self.mc_response_6_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_6_img_label']].replace('&', "&amp;")
                            self.mc_response_6_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_6_img_string_base64_encoded']]
                            self.mc_response_6_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_6_img_path']]
                            
                            self.mc_response_7_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_7_text']].replace('&', "&amp;")
                            self.mc_response_7_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_7_pts_correct_answer']]
                            self.mc_response_7_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_7_pts_false_answer']]
                            self.mc_response_7_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_7_img_label']].replace('&', "&amp;")
                            self.mc_response_7_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_7_img_string_base64_encoded']]
                            self.mc_response_7_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_7_img_path']]
                            
                            self.mc_response_8_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_8_text']].replace('&', "&amp;")
                            self.mc_response_8_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_8_pts_correct_answer']]
                            self.mc_response_8_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_8_pts_false_answer']]
                            self.mc_response_8_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_8_img_label']].replace('&', "&amp;")
                            self.mc_response_8_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_8_img_string_base64_encoded']]
                            self.mc_response_8_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_8_img_path']]
                            
                            self.mc_response_9_text	                        = mc_db_record[self.mc_db_entry_to_index_dict['response_9_text']].replace('&', "&amp;")
                            self.mc_response_9_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_9_pts_correct_answer']]
                            self.mc_response_9_pts_false_answer	            = mc_db_record[self.mc_db_entry_to_index_dict['response_9_pts_false_answer']]
                            self.mc_response_9_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_9_img_label']].replace('&', "&amp;")
                            self.mc_response_9_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_9_img_string_base64_encoded']]
                            self.mc_response_9_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_9_img_path']]
                            
                            self.mc_response_10_text	                    = mc_db_record[self.mc_db_entry_to_index_dict['response_10_text']].replace('&', "&amp;")
                            self.mc_response_10_pts_correct_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_10_pts_correct_answer']]
                            self.mc_response_10_pts_false_answer	        = mc_db_record[self.mc_db_entry_to_index_dict['response_10_pts_false_answer']]
                            self.mc_response_10_img_label	                = mc_db_record[self.mc_db_entry_to_index_dict['response_10_img_label']].replace('&', "&amp;")
                            self.mc_response_10_img_string_base64_encoded	= mc_db_record[self.mc_db_entry_to_index_dict['response_10_img_string_base64_encoded']]
                            self.mc_response_10_img_path                 	= mc_db_record[self.mc_db_entry_to_index_dict['response_10_img_path']]
                            
                            self.mc_picture_preview_pixel                   = mc_db_record[self.mc_db_entry_to_index_dict['picture_preview_pixel']]
                            
                            self.mc_description_img_name_1	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_name_1']]
                            self.mc_description_img_data_1	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_data_1']]
                            self.mc_description_img_path_1	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_path_1']]
                            self.mc_description_img_name_2	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_name_2']]
                            self.mc_description_img_data_2	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_data_2']]
                            self.mc_description_img_path_2	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_path_2']]
                            self.mc_description_img_name_3	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_name_3']]
                            self.mc_description_img_data_3	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_data_3']]
                            self.mc_description_img_path_3	                = mc_db_record[self.mc_db_entry_to_index_dict['description_img_path_3']]
                           
                            self.mc_test_time	                            = mc_db_record[self.mc_db_entry_to_index_dict['test_time']]
                            self.mc_var_number	                            = mc_db_record[self.mc_db_entry_to_index_dict['var_number']]
                            self.mc_question_pool_tag                       = mc_db_record[self.mc_db_entry_to_index_dict['question_pool_tag']]
                            self.mc_question_author                         = mc_db_record[self.mc_db_entry_to_index_dict['question_author']].replace('&', "&amp;")

            Create_MultipleChoice_Questions.mc_question_structure(self, i)

    def mc_question_structure(self, id_nr):
        """Diese Funktion wandelt die SQL-Einträge in die .xml um, welche anschließend in ILIAS eingespielt werden kann"""


        # VARIABLEN
        self.mc_response_counter = 0    #wird verwendet zu zählen, wieviele Anworten pro Frage verwendet werden. Bei einer neuer Antwort -> +1
        self.mc_question_description_main = test_generator_modul_taxonomie_und_textformatierung.Textformatierung.format_description_text_in_xml(self, self.mc_var_use_latex_on_text_check.get(), self.mc_question_description_main)


        # Neuen Ordner erstellen um den Test darin abzulegen
        """ ... """


        # Verbindung zur MC-Datenank
        mc_connect = sqlite3.connect(self.database_multiplechoice_path)
        mc_cursor = mc_connect.cursor()

        # Alle Einträge auslesen
        mc_cursor.execute("SELECT *, oid FROM multiplechoice_table")
        mc_db_records = mc_cursor.fetchall()



        for mc_db_record in mc_db_records:

            if str(mc_db_record[len(mc_db_record)-1]) == self.mc_test_entry_splitted[id_nr]:
                
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mc_description_img_name_1, self.mc_description_img_data_1, id_nr, self.mc_question_type_test_or_pool, self.multiplechoice_test_img_file_path, self.multiplechoice_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mc_description_img_name_2, self.mc_description_img_data_2, id_nr, self.mc_question_type_test_or_pool, self.multiplechoice_test_img_file_path, self.multiplechoice_pool_img_file_path)
                test_generator_modul_ilias_test_struktur.Additional_Funtions.add_dir_for_images(self, self.mc_description_img_name_3, self.mc_description_img_data_3, id_nr, self.mc_question_type_test_or_pool, self.multiplechoice_test_img_file_path, self.multiplechoice_pool_img_file_path)
                  
                
                # Aufbau für  Fragenstruktur "TEST"
                if self.mc_question_type_test_or_pool == "question_test":
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
                                                                                                           self.multiplechoice_pool_qpl_file_path_template,
                                                                                                           self.multiplechoice_pool_qpl_file_path_output)

                # Struktur für den MultipleChoice - Fragen/Antworten Teil  -- HEADER
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                qticomment = ET.SubElement(item, 'qticomment')
                duration = ET.SubElement(item, 'duration')
                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                resprocessing = ET.SubElement(item, 'resprocessing')

                # Struktur für den MultipleChoice - Fragen/Antworten Teil  -- MAIN
                # Muss für jede Frage neu angelegt/hinzugefügt werden
                flow = ET.SubElement(presentation, 'flow')
                question_description_material = ET.SubElement(flow, 'material')
                question_description_mattext = ET.SubElement(question_description_material, 'mattext')
                response_lid = ET.SubElement(flow, 'response_lid')
                render_choice = ET.SubElement(response_lid, 'render_choice')


                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')

                ### ------------------------------------------------------- XML Einträge mit Werten füllen

                # Fragen-Titel -- "item title" in xml
                item.set('title', self.mc_question_title.replace('&', "&amp;"))

                # Fragen-Titel Beschreibung
                qticomment.text = self.mc_question_description_title

                # Testdauer -- "duration" in xml
                # wird keine Testzeit eingetragen, wird 1h vorausgewählt
                duration.text = self.mc_test_time
                if duration.text == "":
                    duration.text = "P0Y0M0DT1H0M0S"

                #self.mc_myroot[0][len(self.mc_myroot[0]) - 1].append(item)


                """ Prüfen ob ILIAS Version ausgelesen werden kann"""
                # -----------------------------------------------------------------------ILIAS VERSION
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "ILIAS_VERSION"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5.4.14 2020-07-31"
                # -----------------------------------------------------------------------QUESTIONTYPE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "QUESTIONTYPE"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "MULTIPLE CHOICE QUESTION"
                # -----------------------------------------------------------------------AUTHOR
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "AUTHOR"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = self.mc_question_author
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
                fieldentry.text = "5f11d3ed9af3e5.53678796"
                # -----------------------------------------------------------------------THUMB_SIZE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "thumb_size"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.mc_picture_preview_pixel)
                # -----------------------------------------------------------------------FEEDBACK_SETTING
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "feedback_setting"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "0"
                # -----------------------------------------------------------------------SINGLELINE
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "singleline"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.mc_response_editor_value)

                # Fragentitel einsetzen -- "presentation label" in xml
                presentation.set('label', self.mc_question_title)

                # Fragen-Text -- "mattext_texttype" in xml -- Gibt das Format des Textes an
                question_description_mattext.set('texttype', "text/html")



               # Fragen-Text (Text) einsetzen   -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
                # Wenn Bild enthalten ist, dann in Fragenbeschreibung einbetten
                question_description_mattext.text = test_generator_modul_ilias_test_struktur.Additional_Funtions.add_picture_to_description_main(
                                                                self, self.mc_description_img_name_1, self.mc_description_img_data_1,
                                                                self.mc_description_img_name_2, self.mc_description_img_data_2,
                                                                self.mc_description_img_name_3, self.mc_description_img_data_3,
                                                                self.mc_question_description_main, question_description_mattext, question_description_material, id_nr)



                # "MCMR --> Multiplechoice Identifier für xml datei
                response_lid.set('ident', "MCMR")
                response_lid.set('rcardinality', "Multiple")
                render_choice.set('shuffle', "Yes")


                # Hier die Question_answer_structure einfügen und Antworten erstellen
                #
                #
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_1_text, self.mc_response_1_pts_correct_answer, self.mc_response_1_pts_false_answer,self.mc_response_1_img_label, self.mc_response_1_img_string_base64_encoded, render_choice, resprocessing, item, "0")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_2_text, self.mc_response_2_pts_correct_answer, self.mc_response_2_pts_false_answer,self.mc_response_2_img_label, self.mc_response_2_img_string_base64_encoded, render_choice, resprocessing, item, "1")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_3_text, self.mc_response_3_pts_correct_answer, self.mc_response_3_pts_false_answer,self.mc_response_3_img_label, self.mc_response_3_img_string_base64_encoded, render_choice, resprocessing, item, "2")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_4_text, self.mc_response_4_pts_correct_answer, self.mc_response_4_pts_false_answer,self.mc_response_4_img_label, self.mc_response_4_img_string_base64_encoded, render_choice, resprocessing, item, "3")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_5_text, self.mc_response_5_pts_correct_answer, self.mc_response_5_pts_false_answer,self.mc_response_5_img_label, self.mc_response_5_img_string_base64_encoded, render_choice, resprocessing, item, "4")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_6_text, self.mc_response_6_pts_correct_answer, self.mc_response_6_pts_false_answer,self.mc_response_6_img_label, self.mc_response_6_img_string_base64_encoded, render_choice, resprocessing, item, "5")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_7_text, self.mc_response_7_pts_correct_answer, self.mc_response_7_pts_false_answer,self.mc_response_7_img_label, self.mc_response_7_img_string_base64_encoded, render_choice, resprocessing, item, "6")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_8_text, self.mc_response_8_pts_correct_answer, self.mc_response_8_pts_false_answer,self.mc_response_8_img_label, self.mc_response_8_img_string_base64_encoded, render_choice, resprocessing, item, "7")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_9_text, self.mc_response_9_pts_correct_answer, self.mc_response_9_pts_false_answer,self.mc_response_9_img_label, self.mc_response_9_img_string_base64_encoded, render_choice, resprocessing, item, "8")
                Create_MultipleChoice_Questions.mc_question_answer_structure(self, self.mc_response_10_text, self.mc_response_10_pts_correct_answer, self.mc_response_10_pts_false_answer, self.mc_response_10_img_label, self.mc_response_10_img_string_base64_encoded, render_choice, resprocessing, item, "9")

                # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                # Der letzte "Zweig" --> "len(self.mc_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                if self.mc_question_type_test_or_pool == "question_test":
                    self.mc_myroot[0][len(self.mc_myroot[0]) - 1].append(item)

                # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                # Die Frage kann einfach angehangen werden
                else:
                    self.mc_myroot.append(item)

                self.mc_mytree.write(self.qti_file_path_output)
                print("MultipleChoice Frage erstellt! --> Titel: " + str(self.mc_question_title))
                
                
                """
                # -----------------------------------------------------------------------AUFLISTUNG DER ANTWORTEN (MULTIPLECHOICE)

                # -----------------------------------------------------------------------ANTWORT 1
                #print("1," + str(self.mc_response_1_text + str(isinstance(self.mc_response_1_text, str))))
                if self.mc_response_1_text != "":
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                    response_label.set('ident', str(self.mc_response_counter))
                    question_answer_mattext.set('texttype', "text/plain")
                    question_answer_mattext.text = self.mc_response_1_text
                    if self.mc_response_1_img_string_base64_encoded != "":
                        question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                        if str(self.mc_response_1_img_label.rpartition('.')[-1]) == "jpg" or str(self.mc_response_1_img_label.rpartition('.')[-1]) == "jpeg":
                            question_answer_matimage.set('imagtype', "image/jpeg")
                        elif str(self.mc_response_1_img_label.rpartition('.')[-1]) == "png":
                            question_answer_matimage.set('imagtype', "image/png")
                        elif str(self.mc_response_1_img_label.rpartition('.')[-1]) == "gif":
                            question_answer_matimage.set('imagtype', "image/gif")
                        else:
                            print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")


                        question_answer_matimage.set('label', self.mc_response_1_img_label)
                        question_answer_matimage.set('embedded', "base64")
                        question_answer_matimage.text = self.mc_response_1_img_string_base64_encoded

                    # --------------------------------------------------------PUNKTE FÜR ANTWORT 1

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")

                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    varequal = ET.SubElement(conditionvar, 'varequal')
                    varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
                    varequal.text = str(self.mc_response_counter) # ID der Antwort inkrementiert für jede Antwort

                    setvar = ET.SubElement(respcondition, 'setvar')
                    setvar.set('action', "Add")
                    setvar.text = str(self.mc_response_1_pts) # Punktevergabe für die Antwort
                    displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                    displayfeedback.set('feedbacktype', "Response")
                    displayfeedback.set('linkrefid', "response_" + str(self.mc_response_counter))

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")
                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    conditionvar_not = ET.SubElement(conditionvar, 'not')
                    varequal_not = ET.SubElement(conditionvar_not, 'varequal')
                    varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
                    varequal_not.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar_not = ET.SubElement(respcondition, 'setvar')
                    setvar_not.set('action', "Add")

                    # Hier werden die gegenteiligen Punkte der Frage behandelt
                    if self.mc_response_1_pts == 0:
                        setvar_not.text = "1"
                    else:
                        setvar_not.text = "0"
                    # --------------------------------------------------------ZUSATZ FÜR ANTWORT 1

                    itemfeedback = ET.SubElement(item, 'itemfeedback')
                    itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                    itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
                    itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

                    itemfeedback.set('ident',"response_" + str(self.mc_response_counter))
                    itemfeedback.set('view', "All")
                    itemfeedback_mattext.set('texttype', "text/plain")

                    self.mc_response_counter = self.mc_response_counter + 1
                # -----------------------------------------------------------------------ANTWORT 2
                #print("2," + str(self.mc_response_2_text + str(isinstance(self.mc_response_2_text, str))))
                if self.mc_response_2_text != "":
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                    response_label.set('ident', str(self.mc_response_counter))
                    question_answer_mattext.set('texttype', "text/plain")
                    question_answer_mattext.text = self.mc_response_2_text

                    if self.mc_response_2_img_string_base64_encoded != "":
                        question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                        if str(self.mc_response_2_img_label.rpartition('.')[-1]) == "jpg" or str(self.mc_response_2_img_label.rpartition('.')[-1]) == "jpeg":
                            question_answer_matimage.set('imagtype', "image/jpeg")
                        elif str(self.mc_response_2_img_label.rpartition('.')[-1]) == "png":
                            question_answer_matimage.set('imagtype', "image/png")
                        elif str(self.mc_response_2_img_label.rpartition('.')[-1]) == "gif":
                            question_answer_matimage.set('imagtype', "image/gif")
                        else:
                            print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")


                        question_answer_matimage.set('label', self.mc_response_2_img_label)
                        question_answer_matimage.set('embedded', "base64")
                        question_answer_matimage.text = self.mc_response_2_img_string_base64_encoded
                    # --------------------------------------------------------PUNKTE FÜR ANTWORT 2

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")

                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    varequal = ET.SubElement(conditionvar, 'varequal')
                    varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
                    varequal.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar = ET.SubElement(respcondition, 'setvar')
                    setvar.set('action', "Add")
                    setvar.text = str(self.mc_response_2_pts)  # Punktevergabe für die Antwort
                    displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                    displayfeedback.set('feedbacktype', "Response")
                    displayfeedback.set('linkrefid', "response_" + str(self.mc_response_counter))

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")
                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    conditionvar_not = ET.SubElement(conditionvar, 'not')
                    varequal_not = ET.SubElement(conditionvar_not, 'varequal')
                    varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
                    varequal_not.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar_not = ET.SubElement(respcondition, 'setvar')
                    setvar_not.set('action', "Add")

                    # Hier werden die gegenteiligen Punkte der Frage behandelt
                    if self.mc_response_2_pts == 0:
                        setvar_not.text = "1"
                    else:
                        setvar_not.text = "0"
                    # --------------------------------------------------------ZUSATZ FÜR ANTWORT 2

                    itemfeedback = ET.SubElement(item, 'itemfeedback')
                    itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                    itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
                    itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

                    itemfeedback.set('ident', "response_" + str(self.mc_response_counter))
                    itemfeedback.set('view', "All")
                    itemfeedback_mattext.set('texttype', "text/plain")

                    self.mc_response_counter = self.mc_response_counter + 1


                    # -----------------------------------------------------------------------ANTWORT 3
                #print("3," + str(self.mc_response_3_text))
                if self.mc_response_3_text != "":
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                    response_label.set('ident', str(self.mc_response_counter))
                    question_answer_mattext.set('texttype', "text/plain")
                    question_answer_mattext.text = self.mc_response_3_text

                    if self.mc_response_3_img_string_base64_encoded != "":
                        question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                        if str(self.mc_response_3_img_label.rpartition('.')[-1]) == "jpg" or str(self.mc_response_3_img_label.rpartition('.')[-1]) == "jpeg":
                            question_answer_matimage.set('imagtype', "image/jpeg")
                        elif str(self.mc_response_3_img_label.rpartition('.')[-1]) == "png":
                            question_answer_matimage.set('imagtype', "image/png")
                        elif str(self.mc_response_3_img_label.rpartition('.')[-1]) == "gif":
                            question_answer_matimage.set('imagtype', "image/gif")
                        else:
                            print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")


                        question_answer_matimage.set('label', self.mc_response_3_img_label)
                        question_answer_matimage.set('embedded', "base64")
                        question_answer_matimage.text = self.mc_response_3_img_string_base64_encoded

                    # --------------------------------------------------------PUNKTE FÜR ANTWORT 3

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")

                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    varequal = ET.SubElement(conditionvar, 'varequal')
                    varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
                    varequal.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar = ET.SubElement(respcondition, 'setvar')
                    setvar.set('action', "Add")
                    setvar.text = str(self.mc_response_3_pts)  # Punktevergabe für die Antwort
                    displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                    displayfeedback.set('feedbacktype', "Response")
                    displayfeedback.set('linkrefid', "response_" + str(self.mc_response_counter))

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")
                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    conditionvar_not = ET.SubElement(conditionvar, 'not')
                    varequal_not = ET.SubElement(conditionvar_not, 'varequal')
                    varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
                    varequal_not.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar_not = ET.SubElement(respcondition, 'setvar')
                    setvar_not.set('action', "Add")

                    # Hier werden die gegenteiligen Punkte der Frage behandelt
                    if self.mc_response_3_pts == 0:
                        setvar_not.text = "1"
                    else:
                        setvar_not.text = "0"
                    # --------------------------------------------------------ZUSATZ FÜR ANTWORT 3

                    itemfeedback = ET.SubElement(item, 'itemfeedback')
                    itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                    itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
                    itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

                    itemfeedback.set('ident', "response_" + str(self.mc_response_counter))
                    itemfeedback.set('view', "All")
                    itemfeedback_mattext.set('texttype', "text/plain")

                    self.mc_response_counter = self.mc_response_counter + 1

                    # -----------------------------------------------------------------------ANTWORT 4
                #print("4," + str(self.mc_response_4_text + str(isinstance(self.mc_response_4_text, str))))
                if self.mc_response_4_text != "":
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                    response_label.set('ident', str(self.mc_response_counter))
                    question_answer_mattext.set('texttype', "text/plain")
                    question_answer_mattext.text = self.mc_response_4_text

                    if self.mc_response_4_img_string_base64_encoded != "":
                        question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                        if str(self.mc_response_4_img_label.rpartition('.')[-1]) == "jpg" or str(self.mc_response_4_img_label.rpartition('.')[-1]) == "jpeg":
                            question_answer_matimage.set('imagtype', "image/jpeg")
                        elif str(self.mc_response_4_img_label.rpartition('.')[-1]) == "png":
                            question_answer_matimage.set('imagtype', "image/png")
                        elif str(self.mc_response_4_img_label.rpartition('.')[-1]) == "gif":
                            question_answer_matimage.set('imagtype', "image/gif")
                        else:
                            print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")

                        question_answer_matimage.set('label', self.mc_response_4_img_label)
                        question_answer_matimage.set('embedded', "base64")
                        question_answer_matimage.text = self.mc_response_4_img_string_base64_encoded
                    # --------------------------------------------------------PUNKTE FÜR ANTWORT 4

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")

                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    varequal = ET.SubElement(conditionvar, 'varequal')
                    varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
                    varequal.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar = ET.SubElement(respcondition, 'setvar')
                    setvar.set('action', "Add")
                    setvar.text = str(self.mc_response_4_pts)  # Punktevergabe für die Antwort
                    displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                    displayfeedback.set('feedbacktype', "Response")
                    displayfeedback.set('linkrefid', "response_" + str(self.mc_response_counter))

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")
                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    conditionvar_not = ET.SubElement(conditionvar, 'not')
                    varequal_not = ET.SubElement(conditionvar_not, 'varequal')
                    varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
                    varequal_not.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar_not = ET.SubElement(respcondition, 'setvar')
                    setvar_not.set('action', "Add")

                    # Hier werden die gegenteiligen Punkte der Frage behandelt
                    if self.mc_response_4_pts == 0:
                        setvar_not.text = "1"
                    else:
                        setvar_not.text = "0"
                    # --------------------------------------------------------ZUSATZ FÜR ANTWORT 4

                    itemfeedback = ET.SubElement(item, 'itemfeedback')
                    itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                    itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
                    itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

                    itemfeedback.set('ident', "response_" + str(self.mc_response_counter))
                    itemfeedback.set('view', "All")
                    itemfeedback_mattext.set('texttype', "text/plain")

                    self.mc_response_counter = self.mc_response_counter + 1

                    # -----------------------------------------------------------------------ANTWORT 5
                #print("5," + str(self.mc_response_5_text + str(isinstance(self.mc_response_5_text, str))))
                if self.mc_response_5_text != "":
                    response_label = ET.SubElement(render_choice, 'response_label')
                    question_answer_material = ET.SubElement(response_label, 'material')
                    question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
                    response_label.set('ident', str(self.mc_response_counter))
                    question_answer_mattext.set('texttype', "text/plain")
                    question_answer_mattext.text = self.mc_response_5_text
                    if self.mc_response_5_img_string_base64_encoded != "":
                        question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                        if str(self.mc_response_5_img_label.rpartition('.')[-1]) == "jpg" or str(self.mc_response_5_img_label.rpartition('.')[-1]) == "jpeg":
                            question_answer_matimage.set('imagtype', "image/jpeg")
                        elif str(self.mc_response_5_img_label.rpartition('.')[-1]) == "png":
                            question_answer_matimage.set('imagtype', "image/png")
                        elif str(self.mc_response_5_img_label.rpartition('.')[-1]) == "gif":
                            question_answer_matimage.set('imagtype', "image/gif")
                        else:
                            print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")

                        question_answer_matimage.set('label', self.mc_response_5_img_label)
                        question_answer_matimage.set('embedded', "base64")
                        question_answer_matimage.text = self.mc_response_5_img_string_base64_encoded
                    # --------------------------------------------------------PUNKTE FÜR ANTWORT 5

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")

                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    varequal = ET.SubElement(conditionvar, 'varequal')
                    varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
                    varequal.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar = ET.SubElement(respcondition, 'setvar')
                    setvar.set('action', "Add")
                    setvar.text = str(self.mc_response_5_pts)  # Punktevergabe für die Antwort
                    displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                    displayfeedback.set('feedbacktype', "Response")
                    displayfeedback.set('linkrefid', "response_" + str(self.mc_response_counter))

                    respcondition = ET.SubElement(resprocessing, 'respcondition')
                    respcondition.set('continue', "Yes")
                    conditionvar = ET.SubElement(respcondition, 'conditionvar')
                    conditionvar_not = ET.SubElement(conditionvar, 'not')
                    varequal_not = ET.SubElement(conditionvar_not, 'varequal')
                    varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
                    varequal_not.text = str(self.mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

                    setvar_not = ET.SubElement(respcondition, 'setvar')
                    setvar_not.set('action', "Add")

                    # Hier werden die gegenteiligen Punkte der Frage behandelt
                    if self.mc_response_5_pts == 0:
                        setvar_not.text = "1"
                    else:
                        setvar_not.text = "0"
                    # --------------------------------------------------------ZUSATZ FÜR ANTWORT 5

                    itemfeedback = ET.SubElement(item, 'itemfeedback')
                    itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                    itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
                    itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

                    itemfeedback.set('ident', "response_" + str(self.mc_response_counter))
                    itemfeedback.set('view', "All")
                    itemfeedback_mattext.set('texttype', "text/plain")

                    self.mc_response_counter = self.mc_response_counter + 1

                    # Wenn es sich um einen ILIAS-Test handelt, beinhaltet die XML eine Struktur mit mehreren "Zweigen"
                    # Der letzte "Zweig" --> "len(self.mc_myroot[0]) - 1" (beschreibt das letze Fach) beinhaltet die eigentlichen Fragen
                    if self.question_type == "question_test":
                        self.mc_myroot[0][len(self.mc_myroot[0]) - 1].append(item)

                    # Wenn es sich um einen ILIAS-Pool handelt, beinhaltet die XML keine Struktur
                    # Die Frage kann einfach angehangen werden
                    else:
                        self.mc_myroot.append(item)


                self.mc_mytree.write(self.qti_file_path_output)
                print("MultipleChoice Frage erstellt! --> Titel: " + str(self.mc_question_title))
                """



        mc_connect.commit()
        mc_connect.close()
        
        if self.mc_question_type_test_or_pool == "question_pool":
            ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
            self.qpl_file = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_pool_abgabe", self.mc_ilias_id_pool_qpl_dir, self.mc_ilias_id_pool_qti_xml))

            self.mytree = ET.parse(self.qpl_file)
            self.myroot = self.mytree.getroot()

            for ident_id in self.myroot.iter('Identifier'):
                ident_id.set('Entry', "il_0_qpl_" + str(self.mc_file_max_id+1))
            self.mytree.write(self.qpl_file)

    def mc_question_answer_structure(self, mc_response_var_text, mc_correct_response_var_pts, mc_false_response_var_pts, mc_response_var_img_label, mc_response_var_img_string_base64_encoded, xml_render_choice, xml_resprocessing, xml_item, mc_response_counter):

        if mc_response_var_text != "":
            response_label = ET.SubElement(xml_render_choice, 'response_label')
            question_answer_material = ET.SubElement(response_label, 'material')
            question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
            response_label.set('ident', str(mc_response_counter))
            question_answer_mattext.set('texttype', "text/plain")
            question_answer_mattext.text = mc_response_var_text
            if mc_response_var_img_string_base64_encoded != "":
                question_answer_matimage = ET.SubElement(question_answer_material, 'matimage')

                if str(mc_response_var_img_label.rpartition('.')[-1]) == "jpg" or str(mc_response_var_img_label.rpartition('.')[-1]) == "jpeg":
                    question_answer_matimage.set('imagtype', "image/jpeg")
                elif str(mc_response_var_img_label.rpartition('.')[-1]) == "png":
                    question_answer_matimage.set('imagtype', "image/png")
                elif str(mc_response_var_img_label.rpartition('.')[-1]) == "gif":
                    question_answer_matimage.set('imagtype', "image/gif")
                else:
                    print("Bildformat ist nicht jpg/jpeg/png/gif und wird von ILIAS nicht unterstützt!")


                question_answer_matimage.set('label', mc_response_var_img_label)
                question_answer_matimage.set('embedded', "base64")
                question_answer_matimage.text = mc_response_var_img_string_base64_encoded

            # --------------------------------------------------------PUNKTE FÜR ANTWORT 1

            respcondition = ET.SubElement(xml_resprocessing, 'respcondition')
            respcondition.set('continue', "Yes")

            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            varequal = ET.SubElement(conditionvar, 'varequal')
            varequal.set('respident', "MCMR") # MCMR --> MultipleChoice Ident
            varequal.text = str(mc_response_counter) # ID der Antwort inkrementiert für jede Antwort

            setvar = ET.SubElement(respcondition, 'setvar')
            setvar.set('action', "Add")
            setvar.text = str(mc_correct_response_var_pts) # Punktevergabe für die richtige Antwort
            displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
            displayfeedback.set('feedbacktype', "Response")
            displayfeedback.set('linkrefid', "response_" + str(mc_response_counter))

            respcondition = ET.SubElement(xml_resprocessing, 'respcondition')
            respcondition.set('continue', "Yes")
            conditionvar = ET.SubElement(respcondition, 'conditionvar')
            conditionvar_not = ET.SubElement(conditionvar, 'not')
            varequal_not = ET.SubElement(conditionvar_not, 'varequal')
            varequal_not.set('respident', "MCMR")  # MCMR --> MultipleChoice Ident
            varequal_not.text = str(mc_response_counter)  # ID der Antwort inkrementiert für jede Antwort

            setvar_not = ET.SubElement(respcondition, 'setvar')
            setvar_not.set('action', "Add")
            setvar_not.text = str(mc_false_response_var_pts)

            # --------------------------------------------------------ZUSATZ FÜR ANTWORT 1

            itemfeedback = ET.SubElement(xml_item, 'itemfeedback')
            itemfeedback_flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
            itemfeedback_material = ET.SubElement(itemfeedback_flow_mat, 'material')
            itemfeedback_mattext = ET.SubElement(itemfeedback_material, 'mattext')

            itemfeedback.set('ident',"response_" + str(mc_response_counter))
            itemfeedback.set('view', "All")
            itemfeedback_mattext.set('texttype', "text/plain")

class Create_MultipleChoice_Test(MultipleChoice):
    def __init__(self, entry_to_index_dict):

        """
        Ein ILIAS-Test besteht immer aus den beiden Dateien "*_qti_*.xml" und "*_tst_*.xml".
        Die "tst" beinhaltelt eine Auflistung der Fragen und den Test-Titel, sowie die Test-id
        Die "qti" beinhaltet die Test-Einstellungen und die eigentliche Beschreibung der einzelnen Fragen
        Dazu gehört die Fragenbeschreibung, Lösungen, Punkte, Bilder etc.

        _________________________________________________________________

        Beispiel für einen Test, bestehend aus 3 Fragen für die _tst_:
        ...
        ...
        Test-Titel: <Title Language="de">SingleChoice</Title>
        ...
        ...
        Test-ID: <Identifier Catalog="ILIAS" Entry="il_0_tst_2040314"/>
        ...
        ...
        Auflistung der Fragen:
            <Question QRef="il_0_qst_457015"/>
            <Question QRef="il_0_qst_526726"/>
            <Question QRef="il_0_qst_457016"/>
            ...
            ...
            <TriggerQuestion Id="457015"/>
            <TriggerQuestion Id="526726"/>
		    <TriggerQuestion Id="457016"/>
        __________________________________________________________________

        Beispiel für einen Test, bestehend aus 3 Fragen für die _qti_:
        ...
        ...
        <assessment ident="il_0_tst_8869" title="SingleChoice">
        ...
        // diverse Test-Einstellungen //
        ...
        <item ident="il_0_qst_457015" title="Arbeitspunkt" maxattempts="0">                         -- Erste Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_526726" title="SingleChoice Test" maxattempts="0">                    -- Zweite Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...
        ...
        <item ident="il_0_qst_457016" title="Eigenschaften der Asynchronmaschine" maxattempts="0">  -- Dritte Frage
        // Fragenbeschreibung, Lösungen, Punktevergabe                                              -- Eigentliche Darstellung der Frage
        ...

        """

        self.mc_db_entry_to_index_dict = entry_to_index_dict

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Test.__init__(self,
                                                                            self.mc_db_entry_to_index_dict,
                                                                            self.multiplechoice_test_tst_file_path_template,
                                                                            self.multiplechoice_test_tst_file_path_output,
                                                                            self.multiplechoice_test_qti_file_path_template,
                                                                            self.multiplechoice_test_qti_file_path_output,
                                                                            self.mc_ilias_test_title_entry.get(),
                                                                            self.create_multiplechoice_test_entry.get(),
                                                                            self.mc_question_type_entry.get(),
                                                                            )

            # # Änderungen der .XML in eine neue Datei schreiben
            # # Die Datei wird nach dem ILIAS-Import "Standard" benannt "1604407426__0__tst_2040314.xml"
            # # Die Ziffernfolge der 10 Ziffern am Anfang sowie der 7 Ziffern zum Schluss können nach belieben variiert werden.
            # self.mc_mytree.write(self.multiplechoice_test_tst_file_path_output)
            #
            #
            # print("TST FILE aktualisiert!")
            # print(self.multiplechoice_test_tst_file_path_output)
            #
            # Create_MultipleChoice_Questions.__init__(self,
            #                           self.mc_db_entry_to_index_dict,
            #                           self.create_multiplechoice_test_entry.get(),
            #                           "question_test",
            #                           self.multiplechoice_test_qti_file_path_template,
            #                           self.multiplechoice_test_qti_file_path_output)
            #
            # # Anschließend werden die "&amp;" in der XML wieder gegen "&" getauscht
            # SingleChoice.sc_replace_character_in_xml_file(self, self.multiplechoice_test_qti_file_path_output)

class Create_MultipleChoice_Pool(MultipleChoice):
    def __init__(self, entry_to_index_dict, var_create_all_questions):

        self.entry_to_index_dict = entry_to_index_dict
        self.mc_var_create_question_pool_all = var_create_all_questions
        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.

        test_generator_modul_ilias_test_struktur.Create_ILIAS_Pool.__init__(self, self.project_root_path, self.multiplechoice_pool_directory_output, self.multiplechoice_files_path_pool_output,
                                                                            self.multiplechoice_pool_qti_file_path_template, self.mc_ilias_test_title_entry.get(), self.create_multiplechoice_pool_entry.get(),
                                                                            self.mc_question_type_entry.get(), self.database_multiplechoice_path, "multiplechoice_table", self.mc_db_entry_to_index_dict, self.mc_var_create_question_pool_all)



    #     self.names = []
    #     self.filename_id = []
    #
    #     self.mc_list_of_directories = []
    #     self.mc_list_of_file_IDs = []
    #     self.mc_filename_with_zip_index = []
    #
    #     self.question_title_list = []
    #     self.question_pool_id_list = []
    #     self.question_title_to_pool_id_dict = {}
    #     self.question_title_to_item_id_dict = {}
    #
    #
    #     # Ordnernamen in "self.multiplechoice_pool_directory_output" auslesen
    #     self.mc_list_of_directories = os.listdir(self.multiplechoice_pool_directory_output)
    #
    #
    #     for i in range(len(self.mc_list_of_directories)):
    #         if ".zip" in self.mc_list_of_directories[i]:
    #             self.mc_filename_with_zip_index.append(i)
    #
    #     for j in range(len(self.mc_filename_with_zip_index)):
    #         self.mc_list_of_directories.pop(self.mc_filename_with_zip_index[j])
    #
    #
    #     print
    #
    #     #Die letzten sieben (7) Zeichen des Orndernamen in eine Liste packen. Die letzten 7 Zeichen geben die ID des Fragenpools an
    #     #Die Ordnernamen für ILIAS sind immer in dem Format: z.B.: 1604407426__0__tst_2040314
    #     #Die ID wird im nachhineie um "1" inkrementiert
    #     for k in range(len(self.mc_list_of_directories)):
    #         self.mc_list_of_file_IDs.append(self.mc_list_of_directories[k][-7:])
    #
    #
    #     # Alle String Einträge nach "INT" konvertieren um mit der max() funktion die höchste ID herauszufiltern
    #     self.mc_list_of_file_IDs = list(map(int, self.mc_list_of_file_IDs))
    #
    #     self.mc_file_max_id = str(max(self.mc_list_of_file_IDs)+1)
    #
    #
    #     #Pfad anpassungen - Die ID muss um +1 erhöht werden, wenn "Fragenpool erstellen" betätigt wird
    #     self.ilias_id_pool_qpl_dir = "1596569820__0__qpl_" + self.mc_file_max_id
    #     self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + self.mc_file_max_id + ".xml"
    #     self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + self.mc_file_max_id + ".xml"
    #
    #     self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))
    #     self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))
    #
    #     # Pfad für ILIAS-Taxonomie Dateien --> "export.xml"
    #     self.modules_export_file = os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Modules', 'TestQuestionPool', 'set_1', 'export.xml'))
    #
    #
    #     self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #     self.taxonomy_file_writes = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #
    #     print("###")
    #     print(self.ilias_id_pool_qpl_dir)
    #
    #     # Neuen Ordner erstellen
    #     Create_MultipleChoice_Pool.mc_createFolder(self, os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir)))
    #
    #
    #     # Hier wird das Verzeichnis kopiert, um die Struktur vom Fragenpool-Ordner zu erhalten
    #     # Die Struktur stammt aus einem Vorlage-Ordner. Die notwendigen XML Dateien werden im Anschluss ersetzt bzw. mit Werten aktualisiert
    #     Create_MultipleChoice_Pool.mc_copytree(self, os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'orig_1596569820__0__qpl_2074808')),
    #              os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir)))
    #
    #     # Da durch "copytree" alle Daten kopiert werden, werden hier die qpl.xml und die qti.xml auf die aktuelle Nummer umbenannt und später dadurch überschrieben
    #     # Anpassung ID für "qti".xml
    #     os.rename(os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qti_2074808.xml")),
    #               os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml)))
    #
    #     # Anpassung ID für "qpl".xml
    #     os.rename(os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qpl_2074808.xml")),
    #               os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml)))
    #
    #
    #
    #     ###### Anpassung der Datei "Modul -> export". Akualisierung des Dateinamens
    #     self.mytree = ET.parse(self.modules_export_file)
    #     self.myroot = self.mytree.getroot()
    #
    #     for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
    #         TaxId.set('Id', self.mc_file_max_id)
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
    #     self.taxonomy_export_file = os.path.normpath(os.path.join(self.multiplechoice_pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
    #     self.mytree = ET.parse(self.taxonomy_export_file)
    #     self.myroot = self.mytree.getroot()
    #
    #     for ExportItem in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
    #         #print(ExportItem.attrib.get('Id'))
    #         if ExportItem.attrib.get('Id') != "":
    #             #print(ExportItem.attrib.get('Id'))
    #             ExportItem.set('Id', self.mc_file_max_id)
    #             break
    #
    #
    #
    #     for object_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ObjId'):
    #         object_id.text = self.mc_file_max_id
    #         break
    #
    #     self.mytree.write(self.taxonomy_export_file)
    #
    #     # Taxonomie-datei "refreshen"
    #     Create_MultipleChoice_Pool.mc_taxonomy_file_refresh(self, self.taxonomy_export_file)
    #
    #
    #     # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
    #     # ilias_id_pol_
    #     self.multiplechoice_pool_qti_file_path_output = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))
    #     self.multiplechoice_pool_qpl_file_path_output = os.path.normpath(os.path.join(self.multiplechoice_files_path,"mc_ilias_pool_abgabe", self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))
    #
    #
    #
    #     Create_MultipleChoice_Questions.__init__(self, self.mc_db_entry_to_index_dict, self.create_multiplechoice_pool_entry.get(), "question_pool", self.multiplechoice_pool_qti_file_path_template, self.multiplechoice_pool_qti_file_path_output)
    #
    #
    #
    #
    # def mc_createFolder(self, directory):
    #     try:
    #         if not os.path.exists(directory):
    #             os.makedirs(directory)
    #     except OSError:
    #         print('Error: Creating directory. ' + directory)
    #
    # def mc_copytree(self, src, dst, symlinks=False, ignore=None):
    #         for item in os.listdir(src):
    #             s = os.path.join(src, item)
    #             d = os.path.join(dst, item)
    #             if os.path.isdir(s):
    #                 shutil.copytree(s, d, symlinks, ignore)
    #             else:
    #                 shutil.copy2(s, d)
    #
    # def mc_taxonomy_file_refresh(self, file_location):
    #     self.file_location = file_location
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
    #
    #
    # def mc_create_pool_question(self):
    #     print("pool question")
    #
    # def mc_create_pool_file_qpl(self):
    #     print("create_pool")
    #
    # def mc_replace_characters_pool(self):
    #     # open xml file to replace specific characters
    #     with open(self.multiplechoice_pool_qpl_file_path_output, 'r') as xml_file:
    #         xml_str = xml_file.read()
    #     xml_str = xml_str.replace('&amp;', '&')  # replace 'x' with 'new_x'
    #
    #     # write to file
    #     with open(self.multiplechoice_pool_qpl_file_path_output, 'w') as replaced_xml_file:
    #         replaced_xml_file.write(xml_str)
"""
    # Diese Funktion fügt die möglichen Antworten in die XML Struktur ein
    # response_sql -> Der Antwort Text aus der SQL-Datenbank (z.B. aus der Spalte "response_1_text)
    # response_label_xml -> Eintrag gibt die "ID" der Antwort wider. Beginnt bei "0" und wird mit jeder zusätzlichen Antowort inkrementiert
    def mc_add_answer_to_xml(self, response_sql, section):

        # Struktur für den SingleChoice - Fragen/Antworten Teil  -- HEADER
        # Muss für jede Frage neu angelegt/hinzugefügt werden
        item = ET.SubElement(section, 'item')
        qticomment = ET.SubElement(item, 'qticomment')
        duration = ET.SubElement(item, 'duration')
        itemmetadata = ET.SubElement(item, 'itemmetadata')
        presentation = ET.SubElement(item, 'presentation')


        # Struktur für den SingleCHoice - Fragen/Antworten Teil  -- MAIN
        # Muss für jede Frage neu angelegt/hinzugefügt werden
        flow = ET.SubElement(presentation, 'flow')
        question_description_material = ET.SubElement(flow, 'material')
        question_description_mattext = ET.SubElement(question_description_material, 'mattext')
        response_lid = ET.SubElement(flow, 'response_lid')
        render_choice = ET.SubElement(response_lid, 'render_choice')
        response_label = ET.SubElement(render_choice, 'response_label')
        question_answer_material = ET.SubElement(response_label, 'material')
        question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')


        qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')



        ### ------------------------------------------------------- XML Einträge mit Werten füllen

        # Fragen-Titel -- "item title" in xml
        item.set('title', self.mc_question_title.replace('&', "&amp;"))

        # Fragen-Titel Beschreibung
        qticomment.text = self.mc_question_description_title

        # Testdauer -- "duration" in xml
        # wird keine Testzeit eingetragen, wird 1h vorausgewählt
        duration.text = self.mc_test_time
        if duration.text == "":
            duration.text = "P0Y0M0DT1H0M0S"




        # Prüfen ob ILIAS Version ausgelesen werden kann
        # -----------------------------------------------------------------------ILIAS VERSION
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "ILIAS_VERSION"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = "5.4.14 2020-07-31"
        # -----------------------------------------------------------------------QUESTIONTYPE
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "QUESTIONTYPE"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = "SINGLE CHOICE QUESTION"
        # -----------------------------------------------------------------------AUTHOR
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "AUTHOR"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        self.mc_autor_replaced = str(self.mc_autor_entry.get())
        fieldentry.text = self.mc_autor_replaced.replace('&', "&amp;")
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
        fieldentry.text = "5f11d3ed9af3e5.53678796"
        # -----------------------------------------------------------------------THUMB_SIZE
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "thumb_size"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = ""
        # -----------------------------------------------------------------------FEEDBACK_SETTING
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "feedback_setting"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = "2"
        # -----------------------------------------------------------------------SINGLELINE
        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "singleline"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = "1"


        # Fragentitel einsetzen -- "presentation label" in xml
        presentation.set('label', self.mc_question_title)




        #Fragen-Text -- "mattext_texttype" in xml -- Gibt das Format des Textes an
        question_description_mattext.set('texttype', "text/html")



        #Fragen-Text -- "mattext_texttype" in xml -- Gibt die eigentliche Fragen-Beschreibung an
        question_description_mattext.text = "<p>" + "TEST - Was kommt in der Natur vor?" + "</p>"


        # -----------------------------------------------------------------------AUFLISTUNG DER ANTWORTEN (SINGLECHOICE)
        ###### Auslesen der Anzahl der Antworten
        if isinstance(self.mc_response_1_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_2_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_3_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_4_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_5_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_6_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_7_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_8_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_9_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1
        elif isinstance(self.mc_response_1_text, str) == True:
            self.mc_response_counter = self.mc_response_counter + 1




        # "MCSR --> Singlechoice Identifier für xml datei
        response_lid.set('ident', "MCSR")
        response_lid.set('rcardinality', "Single")
        render_choice.set('shuffle', "Yes")


        for nr in range(self.mc_response_counter):
            #response_lid = ET.SubElement(flow, 'response_lid')
            #render_choice = ET.SubElement(response_lid, 'render_choice')
            response_label = ET.SubElement(render_choice, 'response_label')
            question_answer_material = ET.SubElement(response_label, 'material')
            question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')

            if response_sql != "":
                response_label.set('ident', str(nr+1))
                question_answer_mattext.set('texttype', "text/plain")
                question_answer_mattext.text = response_sql




        # Neues "Item" an xml anhängen
        self.mc_myroot[0][len(self.mc_myroot[0])-1].append(item)

    #mc_create_question.(self, self.mc_response_1_text)



        self.mc_mytree.write(self.multiplechoice_test_qti_file_path_output)
        print("SingleChoice Frage erstellt!")
"""



""" # Create_SingleChoice_Test.mc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.mc_response_1_text, response_label,  self.mc_response_counter, flow)
            # Create_SingleChoice_Test.mc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.mc_response_2_text, response_label,  self.mc_response_counter, flow)
            # Create_SingleChoice_Test.mc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.mc_response_3_text, response_label,  self.mc_response_counter, flow)
            # Create_SingleChoice_Test.mc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.mc_response_4_text, response_label,  self.mc_response_counter, flow)
            # Create_SingleChoice_Test.mc_add_answer_to_xml(self, presentation, question_description_mattext, response_lid, render_choice,  self.mc_response_5_text, response_label,  self.mc_response_counter, flow)



             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             #response_label = ET.SubElement(render_choice, 'response_label')
             #question_answer_material = ET.SubElement(response_label, 'material')
             #question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             #Create_SingleChoice_Test.mc_add_answer_to_xml(self, self.mc_response_1_text, response_label, question_answer_mattext, self.mc_response_counter)
             if self.mc_response_1_text != "":
                 response_label.set('ident', str(self.mc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.mc_response_1_text
                 self.mc_response_counter = self.mc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 2
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.mc_add_answer_to_xml(self, self.mc_response_1_text, response_label, question_answer_mattext, self.mc_response_counter)
             if self.mc_response_2_text != "":
                 response_label.set('ident', str(self.mc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.mc_response_2_text
                 self.mc_response_counter = self.mc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 3
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.mc_add_answer_to_xml(self, self.mc_response_1_text, response_label, question_answer_mattext, self.mc_response_counter)
             if self.mc_response_3_text != "":
                 response_label.set('ident', str(self.mc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.mc_response_3_text
                 self.mc_response_counter = self.mc_response_counter + 1
             # -----------------------------------------------------------------------ANTWORT 4
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.mc_add_answer_to_xml(self, self.mc_response_1_text, response_label, question_answer_mattext, self.mc_response_counter)
             if self.mc_response_4_text != "":
                 response_label.set('ident', str(self.mc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.mc_response_4_text
                 self.mc_response_counter = self.mc_response_counter + 1

             # -----------------------------------------------------------------------ANTWORT 4
             #response_lid = ET.SubElement(flow, 'response_lid')
             #render_choice = ET.SubElement(response_lid, 'render_choice')
             response_label = ET.SubElement(render_choice, 'response_label')
             question_answer_material = ET.SubElement(response_label, 'material')
             question_answer_mattext = ET.SubElement(question_answer_material, 'mattext')
             # Create_SingleChoice_Test.mc_add_answer_to_xml(self, self.mc_response_1_text, response_label, question_answer_mattext, self.mc_response_counter)
             if self.mc_response_4_text != "":
                 response_label.set('ident', str(self.mc_response_counter))
                 question_answer_mattext.set('texttype', "text/plain")
                 question_answer_mattext.text = self.mc_response_4_text
                 self.mc_response_counter = self.mc_response_counter + 1
"""