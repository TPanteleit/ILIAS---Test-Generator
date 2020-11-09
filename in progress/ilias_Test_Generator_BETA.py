#############################################################################################################
#                                                                                                           #
#    Ilias Test - Generator                                                                                 #
#    Version: 1.8.1 BETA                                                                                      #
#    Author:  Tobias Panteleit                                                                              #
#                                                                                                           #
#    Das Tool dient zur Erstellung von Fragen für die Ilias-Plattform.                                      #
#    In der derzeitigen Version (v1.8.1 BETA) wird sich auf die Erstellung von Formelfragen beschränkt        #
#############################################################################################################
#                                                                                                           #
#                                                                                                           #
#    BETA - STATUS ----- NOCH IN ENTWICKLUNG                                                                #
#    Das Tool wird für die Fragentypen "SingleChoice" und "MultipleChoice" erweitert.                       #
#    Dazu gehört die Erstellung einer neuen Datenbank, die Möglichkeit entsprechende Tests zu generieren    #
#    und die z.B. gemischte Fragenpools zu erstellen                                                        #
#                                                                                                           #
#                                                                                                           #
#############################################################################################################
#                                                                                                           #
#                                                                                                           #
#                                                                                                           #
#    Neuerungen:                                                                                            #
#    - Einlesen von exportierten ILIAS-Tests in die Datenbank                                               #
#    - Der ILIAS_Test darf hierfür folgende Fragentypen beinhalten:                                         #
#        Formelfrage, SingleChoice, MultipleChoice, MatchingQuestion                                        #
#                                                                                                           #
# -------------------------------------------------------------------------------------------------         #
#    Behandlung der Excel-Inhalte:                                                                          #
#    Unter der Kategorie "Fragen-Typ" MUSS "Formelfrage" oder "Multiple Choice" eingetragen werden, da      #
#    ansonsten die Frage vom Programm nicht verwertbar ist                                                  #
#                                                                                                           #
#    Wird ein "Result" (1..10) ausgefüllt MUSS auch die entsprechende Spalte für "Result-pts" ein Wert      #
#    enthalten, ansonsten schlägt der Import nach ILIAS fehl.                                               #
#                                                                                                           #
#    Die Ordner zum zippen und importieren nach ILIAS befinden sich derzeit in                              #
#        ILIAS-Fragenpool_zum_Import                                                                        #
#        ILIAS-Fragentest_tst_Daten                                                                         #
#    Jeweils der Ordner mit der höchsten Nummer am Ende. Bei Programmstart darf sich in diesen              #
#    Ordnern keine *.zip o.ä. befinden!                                                                     #
#                                                                                                           #
#    Bei der nachträglichen Ergänzung von Taxonomien MUSS ZWINGEND mit "Reallocate Text"                    #
#    die XML Datei neu sortiert werden. SONST ERKENNT ILIAS DIESEN NICHT!                                   #
#---------------------------------------------------------------------------------------------------------- #
#                                                                                                                  #
#    Für "Test-Einstellungen übernehmen" muss die Bibliothek "from datetime import datetime" auskommentiert werden #
#                                                                                                                  #
####################################################################################################################



import Pmw
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3                              #verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
from sympy import *
from tkscrolledframe import ScrolledFrame  #Bewegbares Fesnter (Scrollbalken)
import os
import io
import datetime                             # wird benötigt für "Test-Einstellungen benutzen"
from datetime import datetime               # wird benötigt für "delete all entrys?" ??
import pandas as pd                         # used for import excel (xlsx) to mySQL_DB
import pathlib
import xlsxwriter
import shutil                               # zum kopieren und zippen von Dateien
import openpyxl                             # zum excel import von Bildern
import numpy as np
from pandas.core.reshape.util import cartesian_product
import re
import base64
import xlrd

### Ilias-Tool Module
import import_ilias_test_file                      # Modul zum importieren von ILIAS-Test Ordnern in die Datenbank
import test_generator_modul_datenbanken_erstellen  # Modul zum erstellen von notwendigen Datenbanken
import test_generator_modul_singlechoice



class GuiMainWindow:


    def __init__(self, master):
        self.master = master
        master.geometry = '800x710'
        master.title('ilias - Test-Generator v1.8 BETA')


        # --------------------------    Set PATH for Project

        self.project_root_path = pathlib.Path().absolute()
        self.img_file_path_create_folder = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
        self.img_file_path = os.path.normpath(os.path.join(self.project_root_path,'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
        self.emtpy_xml_file_path_read = os.path.normpath(os.path.join(self.project_root_path, 'empty_xml_files', 'empty_xml.xml'))
        self.ilias_questionpool_for_import = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_zum_Import'))



        ### Ordner mit aufsteigender ID erstellen
        self.folder_new_ID_dir = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_qpl_Daten'))
        self.array_of_files_ID = os.listdir(self.folder_new_ID_dir)
        self.names = []
        self.filename_id = []
        for i in range(len(self.array_of_files_ID)):
            self.names.append(self.array_of_files_ID[i][-7:])
        for i in range(len(self.names)):
            self.filename_id.append(int(self.names[i]))









        # --------------------------    Static PATHs for Project
        # "orig"_tst and _qti files are empty file templates.
        #
        self.tst_file_path_read = os.path.normpath(os.path.join(self.project_root_path, 'orig_qti_tst_files', 'orig_1590475954__0__tst_1944463.xml'))
        self.qti_file_path_read = os.path.normpath(os.path.join(self.project_root_path, 'orig_qti_tst_files', 'orig_1590475954__0__qti_1944463.xml'))

        self.tst_file_path_write = os.path.normpath(os.path.join(self.project_root_path,'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', '1590475954__0__tst_1944463.xml'))
        self.qti_file_path_write = os.path.normpath(os.path.join(self.project_root_path,'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', '1590475954__0__qti_1944463.xml'))


        # Question Pool - Files

        self.ilias_id_pool_qpl = "1596569820__0__qpl_" + str(max(self.filename_id)+1)
        self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + str(max(self.filename_id)+1) + ".xml"
        self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + str(max(self.filename_id)+1) + ".xml"

        self.img_file_path_create_folder_pool = os.path.normpath(os.path.join(self.project_root_path,  'ILIAS-Fragenpool_qpl_Daten', self.ilias_id_pool_qpl, 'objects'))

        self.qpl_file_pool_path_read = os.path.normpath(os.path.join(self.project_root_path, 'orig_qpl_qti_files', 'orig_1594724569__0__qpl_1950628.xml'))
        self.qti_file_pool_path_read = os.path.normpath(os.path.join(self.project_root_path, 'orig_qpl_qti_files', 'orig_1594724569__0__qti_1950628.xml'))

        self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qpl_xml))
        self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qti_xml))


        # Taxonomy - Files
        self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.taxonomy_file_writes = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))


        # Export to Excel - Path
        self.table_name = "SQL_DB_export.xlsx"
        self.write_to_excel_path = os.path.normpath(os.path.join(self.project_root_path, self.table_name))


















        # --------------------------    Check if Files are in correct position
        print("\n")
        print("##    Project Files inside this Project Folder?")
        print("##")
        print("##    Testfragen -> orig_tst_file:                     " + str(os.path.exists(self.tst_file_path_read)))
        print("##    Testfragen -> orig_qti_file:                     " + str(os.path.exists(self.qti_file_path_read)))
        print("##    Testfragen -> 1590475954__0__tst_1944463.xml:    " + str(os.path.exists(self.tst_file_path_write)))
        print("##    Testfragen -> 1590475954__0__qti_1944463.xml:    " + str(os.path.exists(self.qti_file_path_write)))
        print("##    Poolfragen -> orig_qpl_file:                     " + str(os.path.exists(self.qpl_file_pool_path_read)))
        print("##    Poolfragen -> orig_qti_file:                     " + str(os.path.exists(self.qti_file_pool_path_read)))
        print("##    Poolfragen -> Vorlage_für_Fragenpool:            " + str(os.path.exists(os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'orig_1596569820__0__qpl_2074808')))))
        print("-------------------------------------------------------")





        # --------------------------   Set size of windows
        # Main-window
        self.formula_width = 800
        self.formula_height = 800

        # Main-window
        self.multiplechoice_width = 800
        self.multiplechoice_height = 800

        # Database-window
        self.database_width = 800
        self.database_height = 800

        # Settings-window
        self.settings_width = 800
        self.settings_height = 800

        # Taxonomy-window
        self.taxonomy_width = 1000
        self.taxonomy_height = 800



        # <------------ Define Tab Control for different Question-Tabs ----------->

        self.tabControl = ttk.Notebook(app)  # Create Tab Control


        # ---- Tab for Formula - Questions
        self.formula_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formula_tab_ttk, text='Formelfrage')  # Add the tab

        # Create a ScrolledFrame widget
        self.sf_formula = ScrolledFrame(self.formula_tab_ttk, width=self.formula_width, height=self.formula_height)
        self.sf_formula.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.sf_formula.bind_arrow_keys(app)
        #self.sf_formula.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.formula_tab = self.sf_formula.display_widget(Frame)


        # ---- Tab for Single Choice - Questions
        self.singlechoice_tab = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.singlechoice_tab, text='Single Choice')  # Add the tab


        # ---- Tab for Multiple Choice - Questions
        self.mc_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.mc_tab_ttk, text='Multiple Choice')  # Add the tab

        # Create a ScrolledFrame widget
        self.sf_mc = ScrolledFrame(self.mc_tab_ttk, width=self.multiplechoice_width, height=self.multiplechoice_height)
        self.sf_mc.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.sf_mc.bind_arrow_keys(app)
        #self.sf_mc.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.multipleChoice_tab = self.sf_mc.display_widget(Frame)


        #self.tabControl.grid()  # Pack to make visible
        self.tabControl.pack(expand=1, fill="both")

        self.frame_test_title = LabelFrame(self.formula_tab, text="Testname & Autor", padx=5, pady=5)
        self.frame_test_title.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.frame_formula = LabelFrame(self.formula_tab, text="Formelfrage", padx=5, pady=5)
        self.frame_formula.grid(row=1, column=0, padx=10, pady=10, sticky=NW)

        self.frame_question_difficulty = LabelFrame(self.formula_tab, text="Fragen Attribute", padx=5, pady=5)
        self.frame_question_difficulty.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.frame_question_category = LabelFrame(self.formula_tab, text="Category", padx=5, pady=5)
        self.frame_question_category.grid(row=9, column=0, padx=10, pady=10, sticky="NE")


        self.frame_question_type = LabelFrame(self.formula_tab, text="Type", padx=5, pady=5)
        self.frame_question_type.grid(row=9, column=1, padx=10, pady=10, sticky="NW")

        self.frame_database = LabelFrame(self.formula_tab, text="Formelfrage-Datenbank", padx=5, pady=5)
        self.frame_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)

        self.frame_picture = LabelFrame(self.formula_tab, text="Vorschau Bild", padx=5, pady=5)
        self.frame_picture.grid(row=1, column=1, padx=10, pady=10, sticky=NW)

        self.frame_db_picture = LabelFrame(self.formula_tab, text="DB Preview - Bild", padx=5, pady=5)
        self.frame_db_picture.grid(row=10, column=1, padx=10, pady=10, sticky="NW")

        self.frame_create_formelfrage = LabelFrame(self.formula_tab, text="Formelfrage erstellen", padx=5, pady=5)
        self.frame_create_formelfrage.grid(row=10, column=0, padx=0, pady=10, sticky="NE")

        self.frame_latex_preview = LabelFrame(self.formula_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.frame_latex_preview.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.frame_excel_sql = LabelFrame(self.formula_tab, text="Excel Import/Export", padx=5, pady=5)
        self.frame_excel_sql.grid(row=9, column=0, padx=40, pady=10, sticky="NE")




        # ----------------------------------------------------------  CREATING FRAMES FOR MultipleChoice TAB
        self.frame_mc_latex_preview = LabelFrame(self.multipleChoice_tab, text="MC: LaTeX Preview", padx=5, pady=5)
        self.frame_mc_latex_preview.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.frame_mc_question_difficulty = LabelFrame(self.multipleChoice_tab, text="MC: Difficulty", padx=5, pady=5)
        self.frame_mc_question_difficulty.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.frame_mc_question_category = LabelFrame(self.multipleChoice_tab, text="MC: Category", padx=5, pady=5)
        self.frame_mc_question_category.grid(row=9, column=0, padx=10, pady=10, sticky="NE")

        self.frame_mc_question_type = LabelFrame(self.multipleChoice_tab, text="MC: Type", padx=5, pady=5)
        self.frame_mc_question_type.grid(row=9, column=1, padx=10, pady=10, sticky="NW")

        self.frame_mc_database = LabelFrame(self.multipleChoice_tab, text="Datenbank", padx=5, pady=5)
        self.frame_mc_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)

        # ----------------------------------------------------------  CREATE SINGLE QUESTION WITH FROM OID
        self.create_formelfrage_btn = Button(self.frame_create_formelfrage, text="ILIAS-Test erstellen", command=lambda: create_formelfrage.__init__(self))
        self.create_formelfrage_btn.grid(row=0, column=0, sticky=W)

        self.create_question_pool_btn = Button(self.frame_create_formelfrage, text="ILIAS-Fragenpool erstellen", command=lambda: create_formelfrage_pool.__init__(self))
        self.create_question_pool_btn.grid(row=3, column=0, sticky=W, pady=(10,0))

        self.create_multiplechoice_btn = Button(self.frame_create_formelfrage, text="mc create", command=lambda: create_multiplechoice.__init__(self))
        #self.create_multiplechoice_btn.grid(row=1, column=0, sticky=W)


        self.create_formelfrage_entry = Entry(self.frame_create_formelfrage, width=15)
        self.create_formelfrage_entry.grid(row=0, column=1, sticky=W, padx=20)

        self.test_title_label = Label(self.frame_test_title, text="Name des Tests")
        self.test_title_label.grid(row=0, column=0, sticky=W)

        self.test_title_entry = Entry(self.frame_test_title, width=60)
        self.test_title_entry.grid(row=0, column=1, sticky=W, padx=30)

        self.autor_label = Label(self.frame_test_title, text="Autor")
        self.autor_label.grid(row=1, column=0, sticky=W)

        self.autor_entry = Entry(self.frame_test_title, width=60)
        self.autor_entry.grid(row=1, column=1, sticky=W, padx=30)

        self.show_frame_btn = Button(self.frame_database, text="Datenbank anzeigen", command=lambda: Database.__init__(self))
        self.show_frame_btn.grid(row=0, column=0, sticky=W)

        self.database_show_records_btn = Button(self.frame_database, text="Show Records",command=lambda: Database.show_records(self))
        #self.database_show_records_btn.grid(row=1, column=0, sticky=W, pady=5)

        self.database_submit_formelfrage_btn = Button(self.frame_database, text="Speichern unter neuer ID", command=lambda: Database.submit(self))
        self.database_submit_formelfrage_btn.grid(row=2, column=0, sticky=W, pady=5)

        self.database_new_question_btn = Button(self.frame_database, text="GUI Einträge entfernen", command=lambda: Database.new_question(self))
        self.database_new_question_btn.grid(row=8, column=0, sticky=W, pady=5)

        self.database_edit_btn = Button(self.frame_database, text="Speichern", command=lambda: Database.edit(self))
        self.database_edit_btn.grid(row=3, column=0, sticky=W, pady=5)

        self.edit_box = Entry(self.frame_database, width=10)
        #self.edit_box.grid(row=3, column=1, sticky=W)

        self.database_load_btn = Button(self.frame_database, text="ID Laden", command=lambda: Database.load(self))
        self.database_load_btn.grid(row=4, column=0, sticky=W, pady=5)

        self.load_box = Entry(self.frame_database, width=10)
        self.load_box.grid(row=4, column=1, sticky=W)

        self.highlight_question_text_label = Label(self.frame_database, text="Fragentext mit Highlighting?")
        self.highlight_question_text_label.grid(row=5, column=0, pady=5, padx=5)

        self.var_highlight_question_text = IntVar()
        self.check_highlight_question_text = Checkbutton(self.frame_database, text="", variable=self.var_highlight_question_text, onvalue=1, offvalue=0)
        self.check_highlight_question_text.deselect()
        self.check_highlight_question_text.grid(row=5, column=1, sticky=W)



        self.database_delete_btn = Button(self.frame_database, text="ID Löschen", command=lambda: Database.delete(self))
        self.database_delete_btn.grid(row=6, column=0, sticky=W, pady=5)

        self.delete_box = Entry(self.frame_database, width=10)
        self.delete_box.grid(row=6, column=1, sticky=W)

        self.delete_all_label = Label(self.frame_database, text="Alle DB Einträge löschen?")
        self.delete_all_label.grid(row=7, column=0, pady=5, padx=5)

        self.var_delete_all = IntVar()
        self.check_delete_all = Checkbutton(self.frame_database, text="", variable=self.var_delete_all, onvalue=1, offvalue=0)
        self.check_delete_all.deselect()
        self.check_delete_all.grid(row=7, column=1, sticky=W)




        #excel_import_btn
        self.excel_xlsx_import_btn = Button(self.frame_excel_sql, text="Excel-Datei importieren", command=lambda: Database.excel_xlsx_import(self))
        self.excel_xlsx_import_btn.grid(row=0, column=1, sticky=W, pady=5, padx=10)

        # excel_export_btn
        self.excel_xlsx_export_btn = Button(self.frame_excel_sql, text="Datenbank exportieren",command=lambda: Database.sql_db_to_excel_export(self, "SQL_DB_export.xlsx"))
        self.excel_xlsx_export_btn.grid(row=1, column=1, sticky=W, pady=5, padx=10)

        #ilias test import_btn
        self.ilias_test_import_btn = Button(self.frame_excel_sql, text="ILIAS-Test importieren",command=lambda: Database.ilias_test_to_sql_import(self))
        self.ilias_test_import_btn.grid(row=2, column=1, sticky=W, pady=5, padx=10)

        # still working?
        #self.show_test_settings_formula_tab = Button(self.formula_tab, text="Test-Einstellungen",command=lambda: GUI_settings_window.__init__(self.formula_tab))
        self.show_test_settings_formula_tab = Button(self.formula_tab, text="Test-Einstellungen",command=lambda: GUI_settings_window.__init__(self))
        self.show_test_settings_formula_tab.grid(row=0, column=0, pady=20, sticky=NE)

        self.img_select_btn = Button(self.frame_picture, text="Bild hinzufügen", command=lambda: Database.open_image(self))
        self.img_select_btn.grid(row=2, column=0, sticky=W)

        self.img_remove_btn = Button(self.frame_picture, text="Bild entfernen", command=lambda: Database.delete_image(self))
        self.img_remove_btn.grid(row=2, column=1, sticky=W)

        self.show_img_from_db_btn = Button(self.frame_db_picture, text="Bild aus der DB",command=lambda: Database.show_img_from_db(self))
        self.show_img_from_db_btn.grid(row=2, column=3, sticky=W)

        # Latex Preview
        #self.myLatex_btn = Button(self.frame_latex_preview, text="show LaTeX Preview", command=lambda: LatexPreview.__init__(self) )
        #self.myLatex_btn.grid(row=0, column=0, padx=10, sticky="W")

        self.question_difficulty_label = Label(self.frame_question_difficulty, text="Schwierigkeitsgrad der Frage")
        self.question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.question_difficulty_entry = Entry(self.frame_question_difficulty, width=10)
        self.question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.question_category_label = Label(self.frame_question_difficulty, text="Fragenkategorie")
        self.question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.question_category_entry = Entry(self.frame_question_difficulty, width=15)
        self.question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.question_type_label = Label(self.frame_question_difficulty, text="Fragen-Typ")
        self.question_type_label.grid(row=2, column=0, pady=5, padx=5, sticky=W)

        self.question_type_entry = Entry(self.frame_question_difficulty, width=15)
        self.question_type_entry.grid(row=2, column=1, pady=5, padx=5, sticky=W)
        self.question_type_entry.insert(0, "Formelfrage")

        self.add_latex_term_btn = Button(self.frame_latex_preview, text="Text \"Latex\"", command=lambda: Formelfrage.text_latex(self))
        self.add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.set_text_sub_btn = Button(self.frame_latex_preview, text="Text \"Tiefgestellt\"", command=lambda: Formelfrage.text_sub(self))
        self.set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10,0), sticky="W")

        self.set_text_sup_btn = Button(self.frame_latex_preview, text="Text \"Hochgestellt\"", command=lambda: Formelfrage.text_sup(self))
        self.set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.set_text_italic_btn = Button(self.frame_latex_preview, text="Text \"Kursiv\"",command=lambda: Formelfrage.text_italic(self))
        self.set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")

        # Read XML File
        self.show_taxonomy_btn = Button(self.frame_question_difficulty, text="Taxonomie-Einstellungen",command=lambda: Formelfrage.read_XML(self))
        self.show_taxonomy_btn.grid(row=5, column=0, columnspan = 2, padx=10, pady=(20,0), ipadx=40, sticky="W")

        # Wertebereich errechnen
        # self.res_formula_label.grid(row=20, column=1, sticky=E, pady=(10, 0), padx=100)
        self.calculate_valuerange_btn = Button(self.frame_formula, text="Wertebereich berechnen",command=lambda: Formelfrage.calc_value_range(self))
        self.calculate_valuerange_btn.grid(row=6, column=1, padx=50, sticky="E")

        #self.reallocate_text_btn = Button(self.frame_latex_preview, text=">>Reallocate Text<<", command=lambda: Formelfrage.reallocate_text(self))
        #self.reallocate_text_btn.grid()


        self.picture_name = "EMPTY"


        # ----------------------------- CREATING BUTTONS FOR MultipleChoice TAB
        #self.mc_myLatex_btn = Button(self.frame_mc_latex_preview, text="show LaTeX Preview", command=lambda: LatexPreview.__init__(self))
        #self.mc_myLatex_btn.grid(row=0, column=0, sticky=W)

        self.mc_question_difficulty_label = Label(self.frame_mc_question_difficulty, text="Schwierigkeitsgrad der Frage")
        self.mc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_difficulty_entry = Entry(self.frame_mc_question_difficulty, width=10)
        self.mc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5)

        self.mc_question_category_label = Label(self.frame_mc_question_category, text="Fragenkategorie")
        self.mc_question_category_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_category_entry = Entry(self.frame_mc_question_category, width=15)
        self.mc_question_category_entry.grid(row=0, column=1, pady=5, padx=5)

        self.mc_question_type_label = Label(self.frame_mc_question_type, text="Fragen-Typ")
        self.mc_question_type_label.grid(row=0, column=0, pady=5, padx=5)

        self.mc_question_type_entry = Entry(self.frame_mc_question_type, width=15)
        self.mc_question_type_entry.grid(row=0, column=1, pady=5, padx=5)
        self.mc_question_type_entry.insert(0, "Multiple Choice")

        self.database_submit_multiplechoice_btn = Button(self.frame_mc_database, text="Submit MC", command=lambda: MultipleChoice.submit_mc(self))
        self.database_submit_multiplechoice_btn.grid(row=2, column=0, sticky=W, pady=5)

        self.database_load_multiplechoice_btn = Button(self.frame_mc_database, text="Load MC", command=lambda: Database.load(self))
        self.database_load_multiplechoice_btn.grid(row=4, column=0, sticky=W, pady=5)

        self.load_multiplechoice_box = Entry(self.frame_mc_database, width=5)
        self.load_multiplechoice_box.grid(row=4, column=1, sticky=W)



        ##### checkboxes ###

        self.create_test_settings_label = Label(self.frame_create_formelfrage, text="Test-Einstellungen übernehmen?")
        self.create_test_settings_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.var_test_settings = IntVar()
        self.check_test_settings = Checkbutton(self.frame_create_formelfrage, text="", variable=self.var_test_settings, onvalue=1, offvalue=0)
        self.check_test_settings.deselect()
        self.check_test_settings.grid(row=1, column=1, sticky=W)


        self.create_question_pool_all_label = Label(self.frame_create_formelfrage, text="Alle Einträge aus der DB erzeugen?")
        self.create_question_pool_all_label.grid(row=4, column=0, pady=5, padx=5, sticky=W)

        self.var_create_question_pool_all = IntVar()
        self.create_question_pool_all = Checkbutton(self.frame_create_formelfrage, text="", variable=self.var_create_question_pool_all, onvalue=1, offvalue=0)
        self.create_question_pool_all.deselect()
        self.create_question_pool_all.grid(row=4, column=1, sticky=W)


        #self.use_question_pool_for_eAss_ilias_label = Label(self.frame_create_formelfrage, text="Fragenpool für Prüfungs-ILIAS verwenden?")
        #self.use_question_pool_for_eAss_ilias_label.grid(row=5, column=0, pady=5, padx=5)

        #self.var_use_question_pool_for_eAss_ilias = IntVar()
        #self.use_question_pool_for_eAss_ilias = Checkbutton(self.frame_create_formelfrage, text="", variable=self.var_use_question_pool_for_eAss_ilias, onvalue=1, offvalue=0)
        #self.use_question_pool_for_eAss_ilias.deselect()
        #self.use_question_pool_for_eAss_ilias.grid(row=5, column=1, sticky=W)

        self.use_latex_on_text_label = Label(self.frame_create_formelfrage, text="Latex für Fragentext nutzen?")
        self.use_latex_on_text_label.grid(row=2, column=0, sticky=W, padx=5)

        self.var_use_latex_on_text_check = IntVar()
        self.use_latex_on_text_check = Checkbutton(self.frame_create_formelfrage, text="", variable=self.var_use_latex_on_text_check, onvalue=1, offvalue=0)
        self.use_latex_on_text_check.deselect()
        self.use_latex_on_text_check.grid(row=2, column=1, sticky=W)

        # ---Init Variable Matrix
        Formelfrage.__init__(self)
        test_generator_modul_singlechoice.SingleChoice.__init__(self, app, self.singlechoice_tab, self.project_root_path)
        MultipleChoice.__init__(self)

    # ---Init MC-TAB
    # MultipleChoice.__init__(self, self.multipleChoice_tab)

    # ---Init SC-TAB
    # SingleChoice.__init__(self, self.singleChoice_tab)







class Formelfrage(GuiMainWindow):

    def __init__(self):


        ####    ----- Create Databases ---
        test_generator_modul_datenbanken_erstellen.CreateDatabases.__init__(self, self.project_root_path)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_formelfrage(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_singlechoice(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_test_settings_profiles(self)





        ###############

        self.question_title_label = Label(self.frame_formula, text="Titel")
        self.question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.question_title_entry = Entry(self.frame_formula, width=60)
        self.question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        self.question_description_label = Label(self.frame_formula, text="Beschreibung")
        self.question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.question_description_entry = Entry(self.frame_formula, width=60)
        self.question_description_entry.grid(row=2, column=1, sticky=W)

        self.question_description_textfield_label = Label(self.frame_formula, text="Frage")
        self.question_description_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.bar = Scrollbar(self.frame_formula)
        self.formula_question_entry = Text(self.frame_formula, height=6, width=65, font=('Helvetica', 9))
        self.bar.grid(row=3, column=2, sticky=W)
        self.formula_question_entry.grid(row=3, column=1, pady=10, sticky=W)
        self.bar.config(command=self.formula_question_entry.yview)
        self.formula_question_entry.config(yscrollcommand=self.bar.set)

        self.formula_processing_time_label = Label(self.frame_formula, text="Bearbeitungsdauer")
        self.formula_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)



        self.formula_processing_time_label = Label(self.frame_formula, text="Std:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.formula_processing_time_label = Label(self.frame_formula, text="Min:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.formula_processing_time_label = Label(self.frame_formula, text="Sek:")
        self.formula_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        #########

        self.processingtime_hours = list(range(24))
        self.processingtime_minutes = list(range(60))
        self.processingtime_seconds = list(range(60))

        self.proc_hours_box = ttk.Combobox(self.frame_formula, value=self.processingtime_hours, width=2)
        self.proc_minutes_box = ttk.Combobox(self.frame_formula, value=self.processingtime_minutes, width=2)
        self.proc_seconds_box = ttk.Combobox(self.frame_formula, value=self.processingtime_seconds, width=2)

        self.proc_hours_box.current(23)
        self.proc_minutes_box.current(0)
        self.proc_seconds_box.current(0)

        def selected_hours(event):
            self.selected_hours = self.proc_hours_box.get()
            print(self.selected_hours)

        def selected_minutes(event):
            self.selected_minutes = self.proc_minutes_box.get()
            print(self.selected_minutes)

        def selected_seconds(event):
            self.selected_seconds = self.proc_seconds_box.get()
            print(self.selected_seconds)

        self.proc_hours_box.bind("<<ComboboxSelected>>", selected_hours)
        self.proc_minutes_box.bind("<<ComboboxSelected>>", selected_minutes)
        self.proc_seconds_box.bind("<<ComboboxSelected>>", selected_seconds)

        self.proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        ################
        self.var_min_label = Label(self.frame_formula, text=' Min.')
        self.var_min_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=60)

        self.var_max_label = Label(self.frame_formula, text=' Max.')
        self.var_max_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=100)

        self.var_prec_label = Label(self.frame_formula, text=' Präz.')
        self.var_prec_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=140)

        self.var_divby_label = Label(self.frame_formula, text=' Teilbar\ndurch')
        self.var_divby_label.grid(row=5, column=1, sticky=W, pady=(20, 0), padx=180)

        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------
        self.var1_name_text, self.var1_min_text, self.var1_max_text, self.var1_prec_text, self.var1_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var2_name_text, self.var2_min_text, self.var2_max_text, self.var2_prec_text, self.var2_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var3_name_text, self.var3_min_text, self.var3_max_text, self.var3_prec_text, self.var3_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var4_name_text, self.var4_min_text, self.var4_max_text, self.var4_prec_text, self.var4_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var5_name_text, self.var5_min_text, self.var5_max_text, self.var5_prec_text, self.var5_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var6_name_text, self.var6_min_text, self.var6_max_text, self.var6_prec_text, self.var6_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var7_name_text, self.var7_min_text, self.var7_max_text, self.var7_prec_text, self.var7_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var8_name_text, self.var8_min_text, self.var8_max_text, self.var8_prec_text, self.var8_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var9_name_text, self.var9_min_text, self.var9_max_text, self.var9_prec_text, self.var9_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.var10_name_text, self.var10_min_text, self.var10_max_text, self.var10_prec_text, self.var10_divby_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()


        self.var1_name_entry = Entry(self.frame_formula, textvariable=self.var1_name_text, width=6)
        self.var1_min_entry = Entry(self.frame_formula, textvariable=self.var1_min_text, width=6)
        self.var1_max_entry = Entry(self.frame_formula, textvariable=self.var1_max_text, width=6)
        self.var1_prec_entry = Entry(self.frame_formula, textvariable=self.var1_prec_text, width=6)
        self.var1_divby_entry = Entry(self.frame_formula, textvariable=self.var1_divby_text, width=6)

        self.var2_name_entry = Entry(self.frame_formula, textvariable=self.var2_name_text, width=6)
        self.var2_min_entry = Entry(self.frame_formula, textvariable=self.var2_min_text, width=6)
        self.var2_max_entry = Entry(self.frame_formula, textvariable=self.var2_max_text, width=6)
        self.var2_prec_entry = Entry(self.frame_formula, textvariable=self.var2_prec_text, width=6)
        self.var2_divby_entry = Entry(self.frame_formula, textvariable=self.var2_divby_text, width=6)

        self.var3_name_entry = Entry(self.frame_formula, textvariable=self.var3_name_text, width=6)
        self.var3_min_entry = Entry(self.frame_formula, textvariable=self.var3_min_text, width=6)
        self.var3_max_entry = Entry(self.frame_formula, textvariable=self.var3_max_text, width=6)
        self.var3_prec_entry = Entry(self.frame_formula, textvariable=self.var3_prec_text, width=6)
        self.var3_divby_entry = Entry(self.frame_formula, textvariable=self.var3_divby_text, width=6)

        self.var4_name_entry = Entry(self.frame_formula, textvariable=self.var4_name_text, width=6)
        self.var4_min_entry = Entry(self.frame_formula, textvariable=self.var4_min_text, width=6)
        self.var4_max_entry = Entry(self.frame_formula, textvariable=self.var4_max_text, width=6)
        self.var4_prec_entry = Entry(self.frame_formula, textvariable=self.var4_prec_text, width=6)
        self.var4_divby_entry = Entry(self.frame_formula, textvariable=self.var4_divby_text, width=6)

        self.var5_name_entry = Entry(self.frame_formula, textvariable=self.var5_name_text, width=6)
        self.var5_min_entry = Entry(self.frame_formula, textvariable=self.var5_min_text, width=6)
        self.var5_max_entry = Entry(self.frame_formula, textvariable=self.var5_max_text, width=6)
        self.var5_prec_entry = Entry(self.frame_formula, textvariable=self.var5_prec_text, width=6)
        self.var5_divby_entry = Entry(self.frame_formula, textvariable=self.var5_divby_text, width=6)

        self.var6_name_entry = Entry(self.frame_formula, textvariable=self.var6_name_text, width=6)
        self.var6_min_entry = Entry(self.frame_formula, textvariable=self.var6_min_text, width=6)
        self.var6_max_entry = Entry(self.frame_formula, textvariable=self.var6_max_text, width=6)
        self.var6_prec_entry = Entry(self.frame_formula, textvariable=self.var6_prec_text, width=6)
        self.var6_divby_entry = Entry(self.frame_formula, textvariable=self.var6_divby_text, width=6)

        self.var7_name_entry = Entry(self.frame_formula, textvariable=self.var7_name_text, width=6)
        self.var7_min_entry = Entry(self.frame_formula, textvariable=self.var7_min_text, width=6)
        self.var7_max_entry = Entry(self.frame_formula, textvariable=self.var7_max_text, width=6)
        self.var7_prec_entry = Entry(self.frame_formula, textvariable=self.var7_prec_text, width=6)
        self.var7_divby_entry = Entry(self.frame_formula, textvariable=self.var7_divby_text, width=6)

        self.var8_name_entry = Entry(self.frame_formula, textvariable=self.var8_name_text, width=6)
        self.var8_min_entry = Entry(self.frame_formula, textvariable=self.var8_min_text, width=6)
        self.var8_max_entry = Entry(self.frame_formula, textvariable=self.var8_max_text, width=6)
        self.var8_prec_entry = Entry(self.frame_formula, textvariable=self.var8_prec_text, width=6)
        self.var8_divby_entry = Entry(self.frame_formula, textvariable=self.var8_divby_text, width=6)

        self.var9_name_entry = Entry(self.frame_formula, textvariable=self.var9_name_text, width=6)
        self.var9_min_entry = Entry(self.frame_formula, textvariable=self.var9_min_text, width=6)
        self.var9_max_entry = Entry(self.frame_formula, textvariable=self.var9_max_text, width=6)
        self.var9_prec_entry = Entry(self.frame_formula, textvariable=self.var9_prec_text, width=6)
        self.var9_divby_entry = Entry(self.frame_formula, textvariable=self.var9_divby_text, width=6)

        self.var10_name_entry = Entry(self.frame_formula, textvariable=self.var10_name_text, width=6)
        self.var10_min_entry = Entry(self.frame_formula, textvariable=self.var10_min_text, width=6)
        self.var10_max_entry = Entry(self.frame_formula, textvariable=self.var10_max_text, width=6)
        self.var10_prec_entry = Entry(self.frame_formula, textvariable=self.var10_prec_text, width=6)
        self.var10_divby_entry = Entry(self.frame_formula, textvariable=self.var10_divby_text, width=6)


        def selected_var(event):  # "variable" need for comboBox Binding

            if self.myCombo.get() == '1':
                Formelfrage.var2_remove(self)
                Formelfrage.var3_remove(self)
                Formelfrage.var4_remove(self)
                Formelfrage.var5_remove(self)
                Formelfrage.var6_remove(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '2':
                Formelfrage.var2_show(self)
                Formelfrage.var3_remove(self)
                Formelfrage.var4_remove(self)
                Formelfrage.var5_remove(self)
                Formelfrage.var6_remove(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '3':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_remove(self)
                Formelfrage.var5_remove(self)
                Formelfrage.var6_remove(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '4':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_remove(self)
                Formelfrage.var6_remove(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '5':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_remove(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '6':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_show(self)
                Formelfrage.var7_remove(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '7':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_show(self)
                Formelfrage.var7_show(self)
                Formelfrage.var8_remove(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '8':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_show(self)
                Formelfrage.var7_show(self)
                Formelfrage.var8_show(self)
                Formelfrage.var9_remove(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '9':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_show(self)
                Formelfrage.var7_show(self)
                Formelfrage.var8_show(self)
                Formelfrage.var9_show(self)
                Formelfrage.var10_remove(self)

            elif self.myCombo.get() == '10':
                Formelfrage.var2_show(self)
                Formelfrage.var3_show(self)
                Formelfrage.var4_show(self)
                Formelfrage.var5_show(self)
                Formelfrage.var6_show(self)
                Formelfrage.var7_show(self)
                Formelfrage.var8_show(self)
                Formelfrage.var9_show(self)
                Formelfrage.var10_show(self)



        self.num_of_vari_label = Label(self.frame_formula, text="Anzahl der Variablen: ")
        self.num_of_vari_label.grid(row=5, column=0, sticky=W, padx=10, pady=(20, 0))

        self.options_var = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.myCombo = ttk.Combobox(self.frame_formula, value=self.options_var, width=3)
        self.myCombo.current(0)
        self.myCombo.bind("<<ComboboxSelected>>", selected_var)
        self.myCombo.grid(row=5, column=1, sticky=W, pady=(20, 0))

        ###########################  ADD VARIABLE - UNITS ##############################

        self.select_var_units = ["Unit", "H", "mH", "µH", "nH", "pH", "---", "F", "mF", "µF", "nF", "pF", "---", "MV", "kV", "V", "mV", "µV", "---"]

        self.var1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var1_unit_myCombo.current(0)
        #self.var1_unit_myCombo.grid(row=6, column=0, sticky=E, padx=10)

        self.var2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var2_unit_myCombo.current(0)

        self.var3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var3_unit_myCombo.current(0)

        self.var4_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var4_unit_myCombo.current(0)

        self.var5_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var5_unit_myCombo.current(0)

        self.var6_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var6_unit_myCombo.current(0)

        self.var7_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.var7_unit_myCombo.current(0)





        ################################################################################

        self.variable1_label = Label(self.frame_formula, text='Variable 1')
        self.variable1_label.grid(row=6, column=0, sticky=W, padx=20)
        self.variable2_label = Label(self.frame_formula, text='Variable 2')
        self.variable3_label = Label(self.frame_formula, text='Variable 3')
        self.variable4_label = Label(self.frame_formula, text='Variable 4')
        self.variable5_label = Label(self.frame_formula, text='Variable 5')
        self.variable6_label = Label(self.frame_formula, text='Variable 6')
        self.variable7_label = Label(self.frame_formula, text='Variable 7')
        self.variable8_label = Label(self.frame_formula, text='Variable 8')
        self.variable9_label = Label(self.frame_formula, text='Variable 9')
        self.variable10_label = Label(self.frame_formula, text='Variable 10')

        # -----------------------Place Label & Entry-Boxes for Variable 1 on GUI

        self.var1_name_entry.grid(row=6, column=1, sticky=W)
        self.var1_min_entry.grid(row=6, column=1, sticky=W, padx=60)
        self.var1_max_entry.grid(row=6, column=1, sticky=W, padx=100)
        self.var1_prec_entry.grid(row=6, column=1, sticky=W, padx=140)
        self.var1_divby_entry.grid(row=6, column=1, sticky=W, padx=180)



        # ------------------------Result 1 - Min/Max Range / Precision / Tolerance / Points

        # res1_label = Label(self.frame_formula, text='Result 1')

        self.res1_name_text, self.res1_min_text, self.res1_max_text, self.res1_prec_text, self.res1_tol_text, self.res1_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res2_name_text, self.res2_min_text, self.res2_max_text, self.res2_prec_text, self.res2_tol_text, self.res2_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res3_name_text, self.res3_min_text, self.res3_max_text, self.res3_prec_text, self.res3_tol_text, self.res3_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res4_name_text, self.res4_min_text, self.res4_max_text, self.res4_prec_text, self.res4_tol_text, self.res4_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res5_name_text, self.res5_min_text, self.res5_max_text, self.res5_prec_text, self.res5_tol_text, self.res5_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res6_name_text, self.res6_min_text, self.res6_max_text, self.res6_prec_text, self.res6_tol_text, self.res6_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res7_name_text, self.res7_min_text, self.res7_max_text, self.res7_prec_text, self.res7_tol_text, self.res7_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res8_name_text, self.res8_min_text, self.res8_max_text, self.res8_prec_text, self.res8_tol_text, self.res8_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res9_name_text, self.res9_min_text, self.res9_max_text, self.res9_prec_text, self.res9_tol_text, self.res9_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.res10_name_text, self.res10_min_text, self.res10_max_text, self.res10_prec_text, self.res10_tol_text, self.res10_points_text = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        self.res1_formula_text, self.res2_formula_text, self.res3_formula_text = StringVar(), StringVar(), StringVar()
        self.res4_formula_text, self.res5_formula_text, self.res6_formula_text = StringVar(), StringVar(), StringVar()
        self.res7_formula_text, self.res8_formula_text, self.res9_formula_text = StringVar(), StringVar(), StringVar()
        self.res10_formula_text = StringVar()

        self.res_name_label = Label(self.frame_formula, text=' result')
        self.res_min_label = Label(self.frame_formula, text=' Min.')
        self.res_max_label = Label(self.frame_formula, text=' Max.')
        self.res_prec_label = Label(self.frame_formula, text=' Präz.')
        self.res_tol_label = Label(self.frame_formula, text='  Tol.')
        self.res_points_label = Label(self.frame_formula, text='Punkte')
        self.res_formula_label = Label(self.frame_formula, text='Formel')

        self.res_min_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=60)
        self.res_max_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=100)
        self.res_prec_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=140)
        self.res_tol_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=180)
        self.res_points_label.grid(row=20, column=1, sticky=W, pady=(10, 0), padx=220)
        self.res_formula_label.grid(row=20, column=1, sticky=E, pady=(10, 0), padx=100)

        self.res1_name_entry = Entry(self.frame_formula, textvariable=self.res1_name_text, width=6)
        self.res1_min_entry = Entry(self.frame_formula, textvariable=self.res1_min_text, width=6)
        self.res1_max_entry = Entry(self.frame_formula, textvariable=self.res1_max_text, width=6)
        self.res1_prec_entry = Entry(self.frame_formula, textvariable=self.res1_prec_text, width=6)
        self.res1_tol_entry = Entry(self.frame_formula, textvariable=self.res1_tol_text, width=6)
        self.res1_points_entry = Entry(self.frame_formula, textvariable=self.res1_points_text, width=6)
        self.res1_formula_entry = Entry(self.frame_formula, textvariable=self.res1_formula_text, width=30)

        self.res2_name_entry = Entry(self.frame_formula, textvariable=self.res2_name_text, width=6)
        self.res2_min_entry = Entry(self.frame_formula, textvariable=self.res2_min_text, width=6)
        self.res2_max_entry = Entry(self.frame_formula, textvariable=self.res2_max_text, width=6)
        self.res2_prec_entry = Entry(self.frame_formula, textvariable=self.res2_prec_text, width=6)
        self.res2_tol_entry = Entry(self.frame_formula, textvariable=self.res2_tol_text, width=6)
        self.res2_points_entry = Entry(self.frame_formula, textvariable=self.res2_points_text, width=6)
        self.res2_formula_entry = Entry(self.frame_formula, textvariable=self.res2_formula_text, width=30)

        self.res3_name_entry = Entry(self.frame_formula, textvariable=self.res3_name_text, width=6)
        self.res3_min_entry = Entry(self.frame_formula, textvariable=self.res3_min_text, width=6)
        self.res3_max_entry = Entry(self.frame_formula, textvariable=self.res3_max_text, width=6)
        self.res3_prec_entry = Entry(self.frame_formula, textvariable=self.res3_prec_text, width=6)
        self.res3_tol_entry = Entry(self.frame_formula, textvariable=self.res3_tol_text, width=6)
        self.res3_points_entry = Entry(self.frame_formula, textvariable=self.res3_points_text, width=6)
        self.res3_formula_entry = Entry(self.frame_formula, textvariable=self.res3_formula_text, width=30)

        self.res4_name_entry = Entry(self.frame_formula, textvariable=self.res4_name_text, width=6)
        self.res4_min_entry = Entry(self.frame_formula, textvariable=self.res4_min_text, width=6)
        self.res4_max_entry = Entry(self.frame_formula, textvariable=self.res4_max_text, width=6)
        self.res4_prec_entry = Entry(self.frame_formula, textvariable=self.res4_prec_text, width=6)
        self.res4_tol_entry = Entry(self.frame_formula, textvariable=self.res4_tol_text, width=6)
        self.res4_points_entry = Entry(self.frame_formula, textvariable=self.res4_points_text, width=6)
        self.res4_formula_entry = Entry(self.frame_formula, textvariable=self.res4_formula_text, width=30)

        self.res5_name_entry = Entry(self.frame_formula, textvariable=self.res5_name_text, width=6)
        self.res5_min_entry = Entry(self.frame_formula, textvariable=self.res5_min_text, width=6)
        self.res5_max_entry = Entry(self.frame_formula, textvariable=self.res5_max_text, width=6)
        self.res5_prec_entry = Entry(self.frame_formula, textvariable=self.res5_prec_text, width=6)
        self.res5_tol_entry = Entry(self.frame_formula, textvariable=self.res5_tol_text, width=6)
        self.res5_points_entry = Entry(self.frame_formula, textvariable=self.res5_points_text, width=6)
        self.res5_formula_entry = Entry(self.frame_formula, textvariable=self.res5_formula_text, width=30)

        self.res6_name_entry = Entry(self.frame_formula, textvariable=self.res6_name_text, width=6)
        self.res6_min_entry = Entry(self.frame_formula, textvariable=self.res6_min_text, width=6)
        self.res6_max_entry = Entry(self.frame_formula, textvariable=self.res6_max_text, width=6)
        self.res6_prec_entry = Entry(self.frame_formula, textvariable=self.res6_prec_text, width=6)
        self.res6_tol_entry = Entry(self.frame_formula, textvariable=self.res6_tol_text, width=6)
        self.res6_points_entry = Entry(self.frame_formula, textvariable=self.res6_points_text, width=6)
        self.res6_formula_entry = Entry(self.frame_formula, textvariable=self.res6_formula_text, width=30)

        self.res7_name_entry = Entry(self.frame_formula, textvariable=self.res7_name_text, width=6)
        self.res7_min_entry = Entry(self.frame_formula, textvariable=self.res7_min_text, width=6)
        self.res7_max_entry = Entry(self.frame_formula, textvariable=self.res7_max_text, width=6)
        self.res7_prec_entry = Entry(self.frame_formula, textvariable=self.res7_prec_text, width=6)
        self.res7_tol_entry = Entry(self.frame_formula, textvariable=self.res7_tol_text, width=6)
        self.res7_points_entry = Entry(self.frame_formula, textvariable=self.res7_points_text, width=6)
        self.res7_formula_entry = Entry(self.frame_formula, textvariable=self.res7_formula_text, width=30)

        self.res8_name_entry = Entry(self.frame_formula, textvariable=self.res8_name_text, width=6)
        self.res8_min_entry = Entry(self.frame_formula, textvariable=self.res8_min_text, width=6)
        self.res8_max_entry = Entry(self.frame_formula, textvariable=self.res8_max_text, width=6)
        self.res8_prec_entry = Entry(self.frame_formula, textvariable=self.res8_prec_text, width=6)
        self.res8_tol_entry = Entry(self.frame_formula, textvariable=self.res8_tol_text, width=6)
        self.res8_points_entry = Entry(self.frame_formula, textvariable=self.res8_points_text, width=6)
        self.res8_formula_entry = Entry(self.frame_formula, textvariable=self.res8_formula_text, width=30)

        self.res9_name_entry = Entry(self.frame_formula, textvariable=self.res9_name_text, width=6)
        self.res9_min_entry = Entry(self.frame_formula, textvariable=self.res9_min_text, width=6)
        self.res9_max_entry = Entry(self.frame_formula, textvariable=self.res9_max_text, width=6)
        self.res9_prec_entry = Entry(self.frame_formula, textvariable=self.res9_prec_text, width=6)
        self.res9_tol_entry = Entry(self.frame_formula, textvariable=self.res9_tol_text, width=6)
        self.res9_points_entry = Entry(self.frame_formula, textvariable=self.res9_points_text, width=6)
        self.res9_formula_entry = Entry(self.frame_formula, textvariable=self.res9_formula_text, width=30)

        self.res10_name_entry = Entry(self.frame_formula, textvariable=self.res10_name_text, width=6)
        self.res10_min_entry = Entry(self.frame_formula, textvariable=self.res10_min_text, width=6)
        self.res10_max_entry = Entry(self.frame_formula, textvariable=self.res10_max_text, width=6)
        self.res10_prec_entry = Entry(self.frame_formula, textvariable=self.res10_prec_text, width=6)
        self.res10_tol_entry = Entry(self.frame_formula, textvariable=self.res10_tol_text, width=6)
        self.res10_points_entry = Entry(self.frame_formula, textvariable=self.res10_points_text, width=6)
        self.res10_formula_entry = Entry(self.frame_formula, textvariable=self.res10_formula_text, width=30)

        self.res1_name_entry.grid(row=21, column=1, sticky=W)
        self.res1_min_entry.grid(row=21, column=1, sticky=W, padx=60)
        self.res1_max_entry.grid(row=21, column=1, sticky=W, padx=100)
        self.res1_prec_entry.grid(row=21, column=1, sticky=W, padx=140)
        self.res1_tol_entry.grid(row=21, column=1, sticky=W, padx=180)
        self.res1_points_entry.grid(row=21, column=1, sticky=W, padx=220)
        self.res1_formula_entry.grid(row=21, column=1, sticky=E, padx=20)

        self.res1_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res1_unit_myCombo.current(0)
        self.res1_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)
        #self.res1_unit_myCombo.grid(row=21, column=0, sticky=E, padx=10)

        self.res2_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res2_unit_myCombo.current(0)
        self.res2_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)

        self.res3_unit_myCombo = ttk.Combobox(self.frame_formula, value=self.select_var_units, width=5)
        self.res3_unit_myCombo.current(0)
        self.res3_unit_myCombo.bind("<<ComboboxSelected>>", selected_var)




        def selected_res(event):  # "variable" need for comboBox Binding

            if self.myCombo_res.get() == '1':
                Formelfrage.res2_remove(self)
                Formelfrage.res3_remove(self)
                Formelfrage.res4_remove(self)
                Formelfrage.res5_remove(self)
                Formelfrage.res6_remove(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '2':
                Formelfrage.res2_show(self)
                Formelfrage.res3_remove(self)
                Formelfrage.res3_remove(self)
                Formelfrage.res4_remove(self)
                Formelfrage.res5_remove(self)
                Formelfrage.res6_remove(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '3':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_remove(self)
                Formelfrage.res5_remove(self)
                Formelfrage.res6_remove(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '4':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_remove(self)
                Formelfrage.res6_remove(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '5':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_remove(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '6':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_show(self)
                Formelfrage.res7_remove(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '7':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_show(self)
                Formelfrage.res7_show(self)
                Formelfrage.res8_remove(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '8':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_show(self)
                Formelfrage.res7_show(self)
                Formelfrage.res8_show(self)
                Formelfrage.res9_remove(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '9':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_show(self)
                Formelfrage.res7_show(self)
                Formelfrage.res8_show(self)
                Formelfrage.res9_show(self)
                Formelfrage.res10_remove(self)

            elif self.myCombo_res.get() == '10':
                Formelfrage.res2_show(self)
                Formelfrage.res3_show(self)
                Formelfrage.res4_show(self)
                Formelfrage.res5_show(self)
                Formelfrage.res6_show(self)
                Formelfrage.res7_show(self)
                Formelfrage.res8_show(self)
                Formelfrage.res9_show(self)
                Formelfrage.res10_show(self)


        self.num_of_res_label = Label(self.frame_formula, text="Anzahl der Ergebnisse: ")
        self.num_of_res_label.grid(row=20, column=0, sticky=W, padx=10, pady=(20, 0))

        self.options_res = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.myCombo_res = ttk.Combobox(self.frame_formula, value=self.options_res, width=3)
        self.myCombo_res.current(0)
        self.myCombo_res.bind("<<ComboboxSelected>>", selected_res)
        self.myCombo_res.grid(row=20, column=1, sticky=W, pady=(20, 0))

        self.result1_label = Label(self.frame_formula, text='Ergebnis 1')
        self.result1_label.grid(row=21, column=0, sticky=W, padx=20)
        self.result2_label = Label(self.frame_formula, text='Ergebnis 2')
        self.result3_label = Label(self.frame_formula, text='Ergebnis 3')
        self.result4_label = Label(self.frame_formula, text='Ergebnis 4')
        self.result5_label = Label(self.frame_formula, text='Ergebnis 5')
        self.result6_label = Label(self.frame_formula, text='Ergebnis 6')
        self.result7_label = Label(self.frame_formula, text='Ergebnis 7')
        self.result8_label = Label(self.frame_formula, text='Ergebnis 8')
        self.result9_label = Label(self.frame_formula, text='Ergebnis 9')
        self.result10_label = Label(self.frame_formula, text='Ergebnis 10')

        #######  Create Tooltip balloons ##################
        self.tooltip = Pmw.Balloon(self.frame_formula)
        self.tooltip.bind(self.var1_name_entry, "Name der Variable für var1")
        self.tooltip.bind(self.var2_name_entry, "Name der Variable für var2")
        self.tooltip.bind(self.var3_name_entry, "Name der Variable für var3")
        self.tooltip.bind(self.var4_name_entry, "Name der Variable für var4")
        self.tooltip.bind(self.var5_name_entry, "Name der Variable für var5")
        self.tooltip.bind(self.var6_name_entry, "Name der Variable für var6")
        self.tooltip.bind(self.var7_name_entry, "Name der Variable für var7")
        self.tooltip.bind(self.res1_name_entry, "Name der Variable für res1")
        self.tooltip.bind(self.res2_name_entry, "Name der Variable für res2")
        self.tooltip.bind(self.res3_name_entry, "Name der Variable für res3")

        self.tooltip.bind(self.question_type_entry, "Hier MUSS \"Formelfrage\" oder \"Multiple Choice\" stehen.")
        self.tooltip.bind(self.question_category_entry, "Eintrag kann beliebig gewählt werden. Wird nur für die Datenbank verwendet und nicht für ILIAS.")
        self.tooltip.bind(self.question_difficulty_entry, "Eintrag kann beliebig gewählt werden. Wird nur für die Datenbank verwendet und nicht für ILIAS.")
        self.tooltip.bind(self.database_load_btn, "ID (Zahl) aus der Datenbank eintragen und mit \"ID Laden\" die Frage zur Bearbeitung laden.")
        self.tooltip.bind(self.load_box, "ID (Zahl) aus der Datenbank eintragen und mit \"ID Laden\" die Frage zur Bearbeitung laden.")
        self.tooltip.bind(self.database_delete_btn, "ID aus der Datenbank löschen: z.B. 1,2,3,4,5 oder 1-5. Wird \"Alle DB Einträge löschen?\" gewählt, wird die eingetragene Zahl nicht mehr beachtet.")
        self.tooltip.bind(self.delete_box, "ID aus der Datenbank löschen: z.B. 1,2,3,4,5 oder 1-5. Wird \"Alle DB Einträge löschen?\" gewählt, wird die eingetragene Zahl nicht mehr beachtet.")

        self.tooltip.bind(self.database_submit_formelfrage_btn, "Aktuelle Einträge unter neuer ID in der Datenbank speichern")
        self.tooltip.bind(self.database_edit_btn, "Aktuelle Einträge unter aktuell ausgewählter ID in der Datenbank speichern/überschreiben.\nEs muss zunächst eine Frage zur Bearbeitung mit \"ID Laden\" geladen werden.")


    def replace_symbols_in_formula(self):
        print("----------------------")
        print("Übernehme Formel aus Eingabefeld")



        self.formula1  =  self.res1_formula_entry.get()
        print(self.formula1)
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
            self.formula1 = self.formula1.replace(item, self.np_translator_dict[item])

        print()
        print(self.formula1)
        print("----------------------")
        return self.formula1

    def calc_value_range(self):

        self.var1_in_formula = 0
        self.var2_in_formula = 0
        self.var3_in_formula = 0
        self.var4_in_formula = 0
        self.var5_in_formula = 0

        # Number of values per range
        N = 21

        # Functions
        #self.calc_formula1 = "lambda row: " + str(self.calc_formula1) + ","

        self.expression_test = Formelfrage.replace_symbols_in_formula(self)

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
        if bool(re.search(r'\d', self.var1_min_text.get())) == True and bool(re.search(r'\d', self.var1_min_text.get())) == True:
            try:
                self.var1_lower, self.var1_upper = int(self.var1_min_text.get()), int(self.var1_max_text.get())
            except ValueError:
                self.var1_lower, self.var1_upper = float(self.var1_min_text.get()), float(self.var1_max_text.get())
        else: self.var1_lower, self.var1_upper = 1, 1


        if bool(re.search(r'\d', self.var2_min_text.get())) == True and bool(re.search(r'\d', self.var2_min_text.get())) == True:
            try:
                self.var2_lower, self.var2_upper = int(self.var2_min_text.get()), int(self.var2_max_text.get())
            except ValueError:
                self.var2_lower, self.var2_upper = float(self.var2_min_text.get()), float(self.var2_max_text.get())
        else: self.var2_lower, self.var2_upper = 1, 1


        if bool(re.search(r'\d', self.var3_min_text.get())) == True and bool(re.search(r'\d', self.var3_min_text.get())) == True:
            try:
                self.var3_lower, self.var3_upper = int(self.var3_min_text.get()), int(self.var3_max_text.get())
            except ValueError:
                self.var3_lower, self.var3_upper = float(self.var3_min_text.get()), float(self.var3_max_text.get())
        else: self.var3_lower, self.var3_upper = 1, 1


        if bool(re.search(r'\d', self.var4_min_text.get())) == True and bool(re.search(r'\d', self.var4_min_text.get())) == True:
            try:
                self.var4_lower, self.var4_upper = int(self.var4_min_text.get()), int(self.var4_max_text.get())
            except ValueError:
                self.var4_lower, self.var4_upper = float(self.var4_min_text.get()), float(self.var4_max_text.get())
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



    def unit_table(self, selected_unit):
        self.unit_to_ilias_code = { "H" : "125", "mH" : "126", "µH" : "127", "nH" : "128", "kH" : "129", "pH" : "130",
                                    "F" : "131", "mF" : "132", "µF" : "133", "nF" : "134", "kF" : "135",
                                    "W" : "136", "kW" : "137", "MW" : "138", "mW" : "149",
                                    "V" : "139", "kV" : "140", "mV" : "141", "µV" : "142", "MV" : "143",
                                    "A" : "144", "mA" : "145", "µA" : "146", "kA" : "147",
                                    "Ohm" : "148", "kOhm" : "150", "mOhm" : "151"}

        self.varTEST = selected_unit
        #print(self.varTEST)
        self.selected_unit = self.unit_to_ilias_code[self.varTEST]
        return self.selected_unit


    def text_latex(self):
        self.formula_question_entry.insert(SEL_FIRST, '\\(', 'RED')
        self.formula_question_entry.insert(SEL_LAST, '\\)', 'RED')
        self.formula_question_entry.tag_config('RED', foreground='red')

    def text_sub(self):
        self.formula_question_entry.insert(SEL_FIRST, '_', 'SUB')
        self.formula_question_entry.insert(SEL_LAST, ' ', 'SUB')
        self.formula_question_entry.tag_add('SUB', SEL_FIRST, SEL_LAST)
        self.formula_question_entry.tag_config('SUB', offset=-4)
        self.formula_question_entry.tag_config('SUB', foreground='blue')

    def text_sup(self):
        self.formula_question_entry.insert(SEL_FIRST, '^', 'SUP')
        self.formula_question_entry.insert(SEL_LAST, ' ', 'SUP')
        self.formula_question_entry.tag_add('SUP', SEL_FIRST, SEL_LAST)
        self.formula_question_entry.tag_config('SUP', offset=4)
        self.formula_question_entry.tag_config('SUP', foreground='green')

    def text_italic(self):
        self.formula_question_entry.insert(SEL_FIRST, '//', 'ITALIC')
        self.formula_question_entry.insert(SEL_LAST, '///', 'ITALIC')
        self.formula_question_entry.tag_add('ITALIC', SEL_FIRST, SEL_LAST)
        self.formula_question_entry.tag_config('ITALIC', font=('Helvetica', 9, 'italic'))
        #self.formula_question_entry.tag_config('ITALIC', foreground='green')

    def read_XML(self):

        app.filename = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.select_taxonomy_file = app.filename

        self.folder_name = self.select_taxonomy_file.rsplit('/', 1)[-1]
        self.folder_name_split1 = self.folder_name[:15]
        self.folder_name_split2 = self.folder_name.rsplit('_', 1)[-1]
        print(self.select_taxonomy_file)
        print(self.folder_name)
        print(self.folder_name_split1)
        print(self.folder_name_split2)


        self.taxonomy_exportXML_file = os.path.normpath(os.path.join(self.select_taxonomy_file, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.taxonomy_file_write = self.taxonomy_exportXML_file

        self.taxonomy_qtiXML_file = os.path.normpath(os.path.join(self.select_taxonomy_file, self.folder_name_split1 + "qti_" + self.folder_name_split2 + ".xml"))
        self.taxonomy_file_read = os.path.normpath(os.path.join(self.select_taxonomy_file, 'Services', 'Taxonomy', 'set_1', 'export.xml'))



        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)




        # New Window must be "Toplevel" not "Tk()" in order to get Radiobuttons to work properly
        self.taxonomy_window = Toplevel()
        self.taxonomy_window.title("Taxonomie")

        # Create a ScrolledFrame widget
        self.sf_taxonomy = ScrolledFrame(self.taxonomy_window, width=self.taxonomy_width, height=self.taxonomy_height)
        self.sf_taxonomy.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.sf_taxonomy.bind_arrow_keys(app)
        #self.sf_taxonomy.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.taxonomy = self.sf_taxonomy.display_widget(Frame)


        self.taxonomy_frame_labels_scroll= LabelFrame(self.taxonomy, text="Fragen ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        #self.taxonomy_frame_labels2.bind_arrow_keys(app)
        #self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)

        #self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        #self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.taxonomy_frame_boxes = LabelFrame(self.taxonomy, text="Fragen ID's", padx=5, pady=5)
        self.taxonomy_frame_boxes.grid(row=0, column=1, padx=20, pady=10, sticky=NW)

        self.taxonomy_frame_tree = LabelFrame(self.taxonomy, text="Taxonomie Baum", padx=5, pady=5)
        self.taxonomy_frame_tree.grid(row=0, column=1, padx=20, pady=200, sticky=NW)

        #self.taxonomy_frame_tree_picture = LabelFrame(self.taxonomy, text="Taxonomie Bild", padx=5, pady=5)
        #self.taxonomy_frame_tree_picture.grid(row=2, column=1, padx=20, pady=10, sticky=NW)

        # ---- Starting ID to End ID set to node
        self.label_starting_id = Label(self.taxonomy_frame_boxes, text="von Fragen ID")
        self.label_starting_id.grid(sticky=W, pady=5, row=0, column=0)

        self.starting_id_var = StringVar()
        self.ending_id_var = StringVar()

        self.taxonomy_name = StringVar()
        self.tax_node_name = StringVar()
        self.tax_node_parent = StringVar()

        self.entry_starting_id = Entry(self.taxonomy_frame_boxes, textvariable=self.starting_id_var, width=10)
        self.entry_starting_id.grid(sticky=W, pady=5, row=1, column=0)


        self.label_ending_id = Label(self.taxonomy_frame_boxes, text="bis Fragen ID")
        self.label_ending_id.grid(sticky=W, padx=10, pady=5, row=0, column=1)

        self.entry_ending_id = Entry(self.taxonomy_frame_boxes, textvariable=self.ending_id_var, width=10)
        self.entry_ending_id.grid(sticky=W, padx=10, pady=5, row=1, column=1)



        self.taxonomy_name_label = Label(self.taxonomy_frame_tree, text="Name für Taxonomie")
        self.taxonomy_name_label.grid(sticky=W, padx=10, pady=5, row=0, column=0)
        self.taxonomy_name_entry = Entry(self.taxonomy_frame_tree, textvariable=self.taxonomy_name, width=20)
        self.taxonomy_name_entry.grid(sticky=W, padx=10, pady=5, row=0, column=1)


        self.tax_node_name_label = Label(self.taxonomy_frame_tree, text="Name für Knoten")
        self.tax_node_name_label.grid(sticky=W, padx=10, pady=5, row=1, column=0)
        self.tax_node_name_entry = Entry(self.taxonomy_frame_tree, textvariable=self.tax_node_name, width=20)
        self.tax_node_name_entry.grid(sticky=W, padx=10, pady=5, row=1, column=1)

        self.tax_node_parent_label = Label(self.taxonomy_frame_tree, text="Vaterknoten")
        self.tax_node_parent_label.grid(sticky=W, padx=10, pady=5, row=2, column=0)
        self.tax_node_parent_entry = Entry(self.taxonomy_frame_tree, textvariable=self.tax_node_parent, width=20)
        self.tax_node_parent_entry.grid(sticky=W, padx=10, pady=5, row=2, column=1)



        # Button to assign questions to node
        self.assign_to_node_btn = Button(self.taxonomy_frame_boxes, text="Fragen dem Knoten\nhinzufügen", command=lambda: Formelfrage.assign_questions_to_node(self))
        self.assign_to_node_btn.grid(row=4, column=0, sticky=W, pady=(20, 0))

        self.remove_from_node_btn = Button(self.taxonomy_frame_boxes, text="Fragen von Knoten\nentfernen",command=lambda: Formelfrage.remove_question_from_node(self))
        self.remove_from_node_btn.grid(row=4, column=1, sticky=W, padx=5, pady=(20, 0))

        self.tax_add_node_btn = Button(self.taxonomy_frame_tree, text="Neuen Knoten hinzufügen",command=lambda: Formelfrage.add_node_to_tax(self))
        self.tax_add_node_btn.grid(row=6, column=0, sticky=W, padx=5, pady=(20, 0))

        self.scan_tax_tree_btn = Button(self.taxonomy_frame_tree, text="scan_tax_tree",command=lambda: Formelfrage.scan_tax_tree(self))
        self.scan_tax_tree_btn.grid(row=6, column=1, sticky=W, padx=5, pady=(20, 0))

        self.update_taxonomy_name_btn = Button(self.taxonomy_frame_tree, text="Taxonomie-Namen\naktualisieren", command=lambda: Formelfrage.update_taxonomy_name(self))
        self.update_taxonomy_name_btn.grid(row=0, column=2, sticky=E, padx=5, pady=(5, 0))

        self.tax_remove_node_btn = Button(self.taxonomy_frame_tree, text="Knoten entfernen",command=lambda: Formelfrage.remove_node_from_tax(self))
        self.tax_remove_node_btn.grid(row=6, column=2, sticky=W, padx=5, pady=(20, 0))

        self.tax_reallocate_btn = Button(self.taxonomy_frame_tree, text="Taxonomie-Datei\nneu anordnen",command=lambda: Formelfrage.tax_reallocate(self))
        self.tax_reallocate_btn.grid(row=5, column=2, sticky=W, padx=5, pady=(20, 0))



        Formelfrage.read_taxonomy_file(self)
        Formelfrage.scan_tax_tree(self)

    def read_taxonomy_file(self):

        self.mytree = ET.parse(self.taxonomy_qtiXML_file)
        self.myroot = self.mytree.getroot()


        self.item_id_list = []
        self.item_title_list = []
        self.item_id_var = 0
        self.item_title_var = 0
        self.item_labels_list = []
        self.combobox_list = []



        for item in self.myroot.iter('item'):
            self.item_id_raw = str(item.get('ident'))
            self.item_id = self.item_id_raw.rsplit('_', 1)[-1]
            self.item_title = str(item.get('title'))
            self.item_id_list.append(self.item_id)
            self.item_title_list.append(self.item_title)


        #print(len(self.ident))

        for id_text in self.item_id_list:
            label_id = Label(self.taxonomy_frame_labels, text=id_text)
            label_id.grid(sticky=W, pady=5, row=self.item_id_var, column=0)
            self.item_labels_list.append(str(label_id.cget("text")))
            #print("Label ID: " + str(label_id.cget("text")))

            label_placeholder = Label(self.taxonomy_frame_labels, text=" ---- ")
            label_placeholder.grid(sticky=W, pady=5, row=self.item_id_var, column=1)

            self.item_id_var = self.item_id_var+1



        for title_text in self.item_title_list:
            label_title = Label(self.taxonomy_frame_labels, text=title_text)
            label_title.grid(sticky=W, pady=5, row= self.item_title_var, column=2)
            self.item_title_var = self.item_title_var + 1




        ##### - Taxonomie Ebenen auslesen - ####
        print("\n")
        print("---- Taxonomie auslesen")
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        self.tax_title = []
        self.child_tag = []
        self.node_tag = []
        self.item_in_node = []
        self.item_tag = []
        self.root_node = "000000"
        self.id_to_node_dict = {}
        self.item_nr_list = []


        # Auslesen der Root-ID    Diese ID gibt den "Hauptstamm" der Taxonomie an
        # Root-ID wird vorher auf "000000" gesetzt um zu prüfen ob der Wert im nächsten Schritt überschrieben wurde
        for Tax in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
                self.root_node = Tax.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

                if self.root_node != "000000":
                    print("Root Node found: " + str(self.root_node))
                else:
                    print("No Root ID in File!")




        # ---- Alle Ebenen im Dokument suchen ---- #
        for TaxTree in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId').text == str(self.root_node):
                self.child_tag.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child').text)
                self.node_tag.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text)

        #print("Nodes found: " + str(self.node_tag))
        #print("with Child ID: " + str(self.child_tag))

        # convert list "child tag" and list "node_tag" to dictionary
        self.id_to_node_dict = dict(zip(self.child_tag, self.node_tag))
        self.node_to_id_dict = dict(zip(self.node_tag, self.child_tag))
        #print(self.id_to_node_dict)
        print("------------------------------------------------")




        print("\n")
        #print("------- Show Question assignments -------")
        for i in range(len(self.child_tag)):
            for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
                if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text == str(self.child_tag[i]):  #Bsp. für Ebene 1 ID
                    self.item_in_node.append(str(self.child_tag[i]))
                    self.item_tag.append(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)
                    self.item_nr_list.append(self.item_labels_list.index(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text))


        for i in range(len(self.item_nr_list)):
            label_taxnode = Label(self.taxonomy_frame_labels, text=" --- " + str(self.id_to_node_dict.get(self.item_in_node[i])))
            label_taxnode.grid(sticky=W, pady=5, row=self.item_labels_list.index(self.item_tag[i]), column=4)

        #PRüfen ob die Fragen im Fragenpool konsistent sind (fortlaufende ID's
        self.check_question_id_start = str(self.item_labels_list[0])
        self.check_question_id_end = str(self.item_labels_list[len(self.item_labels_list)-1])
        self.check_question_id_counter = int(self.check_question_id_start)

        #for i in range(len(self.item_labels_list)):
        #    if int(self.item_labels_list[i]) != int(self.check_question_id_counter):
        #        print("Error in Labels list", self.item_labels_list[i], self.check_question_id_counter)

        #    self.check_question_id_counter = self.check_question_id_counter + 1
        #print("Label-check DONE")

        Formelfrage.tax_combobox_refresh(self)

    def update_taxonomy_name(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        if self.taxonomy_name_entry.get != "":

            # Auslesen der Root-ID    Diese ID gibt den "Hauptstamm" der Taxonomie an
            # Root-ID wird vorher auf "000000" gesetzt um zu prüfen ob der Wert im nächsten Schritt überschrieben wurde
            for Tax in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
                Tax.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text = self.taxonomy_name_entry.get()

                if self.root_node != "000000":
                    print("Root Node found: " + str(self.root_node))
                else:
                    print("No Root ID in File!")

        self.mytree.write(self.taxonomy_file_write)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)

        self.taxonomy_frame_tree_picture.destroy()
        Formelfrage.scan_tax_tree(self)

    # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
    # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
    def tax_file_refresh(self, file_location):

        self.file_location = file_location
        #print("refresh_file_location: " + str(self.file_location))
        with open(self.file_location, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('ns0:', 'exp:')
        xml_str = xml_str.replace('ns2:', 'ds:')
        xml_str = xml_str.replace('ns3:', '')#replace "x" with "new value for x"
        xml_str = xml_str.replace('<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
                                  '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')
        xml_str = xml_str.replace('<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Entity="tax" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
	                              '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')

        #print(self.var_use_question_pool_for_eAss_ilias)
        # Anpassung Taxonomie Datei (export.xml) für das Prüfungsilias
        #if self.var_use_question_pool_for_eAss_ilias == 1:
        #    xml_str = xml_str.replace('<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://f07.eassessment.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://f07.eassessment.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_ds_4_3.xsd">',
        #                              '<exp:Export InstallationId="0" InstallationUrl="https://f07.eassessment.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://f07.eassessment.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')


        with open(self.file_location, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

            #print(self.file_location)
        #print("Taxonomie Datei editiert")

    def add_node_to_tax(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        self.collect_childs = []
        self.collect_title = []
        self.collect_depth = []
        self.collect_parent = []
        self.collect_order_nr = []


        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
             self.collect_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
             self.collect_parent.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
             self.collect_depth.append(depth.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
             self.collect_title.append(title.text)

        for order_nr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
             self.collect_order_nr.append(order_nr.text)

        # Taxonomie Datei nach Hauptebene (ID und Name) suchen
        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == "1970392":
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text


        self.collect_title.pop(0)
        self.title_to_id_dict = {}
        self.title_to_id_dict = dict(zip(self.collect_title, self.collect_childs))

        self.title_to_depth_dict = {}
        self.title_to_depth_dict = dict(zip(self.collect_title, self.collect_depth))



        Export = ET.Element('exp:Export')
        ExportItem = ET.SubElement(Export, 'exp:ExportItem')
        DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
        Rec = ET.SubElement(DataSet, 'ds:Rec')
        TaxTree = ET.SubElement(Rec, 'TaxTree')
        TaxId = ET.SubElement(TaxTree, 'TaxId')
        Child = ET.SubElement(TaxTree, 'Child')
        Parent = ET.SubElement(TaxTree, 'Parent')
        Depth = ET.SubElement(TaxTree, 'Depth')
        Type = ET.SubElement(TaxTree, 'Type')
        Title = ET.SubElement(TaxTree, 'Title')
        OrderNr = ET.SubElement(TaxTree, 'OrderNr')

        Rec.set('Entity', "tax_tree")



        TaxId.text = str(self.tax_root_id)
        Child.text = str(int(max(self.collect_childs))+1)

        if self.tax_node_parent_entry.get() == "":
            Parent.text = str(min(self.collect_childs))
            Depth.text = str(int(min(self.collect_depth)) + 1 )
            if Depth.text == "1":
                Type.text = ""
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)   #Änderung min() auf max()
            else:
                Type.text = "taxn"  # fix
                Title.text = str(self.tax_node_name_entry.get())
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)


        else:
            Parent.text = str(self.title_to_id_dict.get(self.tax_node_parent_entry.get()))
            Depth.text = str(int(self.title_to_depth_dict.get(self.tax_node_parent_entry.get())) + 1)
            Type.text = "taxn"  # fix
            Title.text = str(self.tax_node_name_entry.get())
            OrderNr.text = str(int(max(self.collect_order_nr))+1)

        self.myroot.append(ExportItem)
        self.mytree.write(self.taxonomy_file_write)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)

        self.taxonomy_frame_tree_picture.destroy()
        Formelfrage.scan_tax_tree(self)


        self.tax_nodes_myCombo.destroy()
        Formelfrage.tax_combobox_refresh(self)

    def add_node_to_tax_from_excel(self, file_location, new_node_name, parent_node_name):



        self.taxonomy_export_file = file_location
        Formelfrage.tax_file_refresh(self, self.taxonomy_export_file)

        self.mytree = ET.parse(self.taxonomy_export_file)
        self.myroot = self.mytree.getroot()

        self.collect_childs = []
        self.collect_title = []
        self.collect_depth = []
        self.collect_parent = []
        self.collect_order_nr = []


        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
             self.collect_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
             self.collect_parent.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
             self.collect_depth.append(depth.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
             self.collect_title.append(title.text)

        for order_nr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
             self.collect_order_nr.append(order_nr.text)

        #print(self.collect_order_nr)

        # Taxonomie Datei nach Hauptebene (ID und Name) suchen
        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == "1970392":
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

        #print(self.collect_childs)
        #print(self.collect_title)
        #print(self.collect_depth)
        #print(self.collect_parent)
        #print(self.collect_order_nr)



        self.collect_title.pop(0)
        self.title_to_id_dict = {}
        self.title_to_id_dict = dict(zip(self.collect_title, self.collect_childs))

        self.title_to_depth_dict = {}
        self.title_to_depth_dict = dict(zip(self.collect_title, self.collect_depth))


        #for i in range(len(self.collect_title)):
         #   print(self.collect_childs[i], self.collect_title[i], self.collect_depth[i], self.collect_parent[i], self.collect_order_nr[i])

        Export = ET.Element('exp:Export')
        ExportItem = ET.SubElement(Export, 'exp:ExportItem')
        DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
        Rec = ET.SubElement(DataSet, 'ds:Rec')
        TaxTree = ET.SubElement(Rec, 'TaxTree')
        TaxId = ET.SubElement(TaxTree, 'TaxId')
        Child = ET.SubElement(TaxTree, 'Child')
        Parent = ET.SubElement(TaxTree, 'Parent')
        Depth = ET.SubElement(TaxTree, 'Depth')
        Type = ET.SubElement(TaxTree, 'Type')
        Title = ET.SubElement(TaxTree, 'Title')
        OrderNr = ET.SubElement(TaxTree, 'OrderNr')

        Rec.set('Entity', "tax_tree")



        TaxId.text = str(self.tax_root_id)
        Child.text = str(int(max(self.collect_childs))+1)

        # Wenn kein "Parent"-Node existiert
        if parent_node_name == "EMPTY":
            Parent.text = str(min(self.collect_childs))
            Depth.text = str(int(min(self.collect_depth)) + 1)
            if Depth.text == "1":
                Type.text = ""
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)   #Änderung min() auf max()
                #print("ORderNr: " + OrderNr.text)
            else:
                Type.text = "taxn"  # fix
                Title.text = str(new_node_name)
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)
                #print("ORderNr: " + OrderNr.text)

        else:
            Parent.text = str(self.title_to_id_dict.get(parent_node_name))
            Depth.text = str(int(self.title_to_depth_dict.get(parent_node_name)) + 1)
            Type.text = "taxn"  # fix
            Title.text = str(new_node_name)
            OrderNr.text = str(int(max(self.collect_order_nr))+1)

        self.myroot.append(ExportItem)
        self.mytree.write(self.taxonomy_export_file)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_export_file)

    def assign_questions_to_node_from_excel(self, file_location, item_id, item_pool):

        self.taxonomy_export_file = file_location



        # Fragen einem Knoten hinzufügen
        self.mytree = ET.parse(self.taxonomy_export_file)
        self.myroot = self.mytree.getroot()

        self.node_to_id_dict = {}
        self.child_tag_assign = []
        self.node_tag_assign = []
        self.child_tag = []
        self.node_tag = []


        # Auslesen der Root-ID    Diese ID gibt den "Hauptstamm" der Taxonomie an
        # Root-ID wird vorher auf "000000" gesetzt um zu prüfen ob der Wert im nächsten Schritt überschrieben wurde
        self.root_node = "000000"
        for Tax in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
                self.root_node = Tax.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

                #if self.root_node != "000000":
                #    print("Root Node found: " + str(self.root_node))
                #else:
                #    print("No Root ID in File!")


        # ---- Alle Ebenen im Dokument suchen ---- #
        for TaxTree in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId').text == str(self.root_node):
                self.child_tag.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child').text)
                self.node_tag.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text)


        # ---- Alle Ebenen im Dokument suchen ---- #
        for TaxTree in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId').text == str(self.root_node):
                self.child_tag_assign.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child').text)
                self.node_tag_assign.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text)

        #print("Nodes found: " + str(self.node_tag))
        #print("with Child ID: " + str(self.child_tag))

        # convert list "child tag" and list "node_tag" to dictionary
        self.node_to_id_dict = dict(zip(self.node_tag_assign, self.child_tag_assign))
        #print("------------------------------------------------")

        # Export XML-File
        # xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1"
        # xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3"
        # xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3"
        # xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">
        # Bsp: tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)

        # -------- Struktur einer "assignment to node" in der XML
        # < ds: Rec Entity = "tax_node_assignment" >
        #    < TaxNodeAssignment >
        #        < NodeId > 21682 < / NodeId >
        #        < Component > qpl < / Component >
        #        < ItemType > quest < / ItemType >
        #        < ItemId > 470081 < / ItemId >
        #    < / TaxNodeAssignment >
        # < / ds: Rec >



        # Die Definition der Haupt- und Sub-Elemente muss in der Schleife für jede Frage neu erstellt werden
        # Sonst haben die angehängten Fragen alle die gleichen Werte, da es sich auf das Gleiche "Attribut" handelt
        Export = ET.Element('exp:Export')
        ExportItem = ET.SubElement(Export, 'exp:ExportItem')
        DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
        Rec = ET.SubElement(DataSet, 'ds:Rec')
        TaxNodeAssignment = ET.SubElement(Rec, 'TaxNodeAssignment')
        NodeId = ET.SubElement(TaxNodeAssignment, 'NodeId')
        Component = ET.SubElement(TaxNodeAssignment, 'Component')
        ItemType = ET.SubElement(TaxNodeAssignment, 'ItemType')
        ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')


        #Rec = ET.SubElement(DataSet, 'ds:Rec')
        Rec.set('Entity', "tax_node_assignment")
        #ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

        NodeId.text = self.node_to_id_dict.get(item_pool)

        Component.text = "qpl"  # fix
        ItemType.text = "quest" # fix
        ItemId.text = item_id     # Fragen ID üblicherweise > 100000, wenn Fragen ID z.B. 000001 dann ist der itemValue "nur" 1 und es fehlen nullen
        self.myroot[0][len(self.myroot[0]) - 1].append(Rec)

        #print("NodeId: " + NodeId.text)
        #print("ItemId: " + ItemId.text)

        self.mytree.write(file_location)



        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, file_location)

    def remove_node_from_tax(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        self.node_to_remove = self.tax_node_name_entry.get()

        self.taxTree_taxIds = []
        self.taxTree_childs = []
        self.taxTree_parents = []
        self.taxTree_depths = []
        self.taxTree_types = []
        self.taxTree_titles = []
        self.taxTree_orderNrs = []





        self.remove_node = self.tax_node_name_entry.get()
        for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text == self.remove_node:
                print("found node: " + str(self.remove_node))
                tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text = "delete"
                self.mytree.write(self.taxonomy_file_write)
                print("Node auf \"delete\"")


        # Alle Daten der Knoten speichern

        for taxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId'):
            self.taxTree_taxIds.append(taxId.text)
            # wert ist fix

        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
            self.taxTree_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
            self.taxTree_parents.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
            self.taxTree_depths.append(depth.text)

        for typ in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Type'):
            self.taxTree_types.append(typ.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
            self.taxTree_titles.append(title.text)

        for orderNr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
            self.taxTree_orderNrs.append(orderNr.text)

        # 1. Eintrag entfernen, da dieser Eintrag dem Taxonomie-Namen entspricht und nicht vom Knoten
        self.taxTree_titles.pop(0)


        # Alle TaxTree löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                if child.attrib['Entity'] == "tax_tree":
                    rec.remove(child)
        self.mytree.write(self.taxonomy_file_write)
        print("Deleted!")


        for i in range(len(self.taxTree_titles)):
            if self.taxTree_titles[i] != "delete":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxTree = ET.SubElement(Rec, 'TaxTree')
                TaxId = ET.SubElement(TaxTree, 'TaxId')
                Child = ET.SubElement(TaxTree, 'Child')
                Parent = ET.SubElement(TaxTree, 'Parent')
                Depth = ET.SubElement(TaxTree, 'Depth')
                Type = ET.SubElement(TaxTree, 'Type')
                Title = ET.SubElement(TaxTree, 'Title')
                OrderNr = ET.SubElement(TaxTree, 'OrderNr')


                Rec.set('Entity', "tax_tree")

                TaxId.text = str(self.tax_root_id)
                Child.text = str(self.taxTree_childs[i])
                Parent.text = str(self.taxTree_parents[i])
                Depth.text = str(self.taxTree_depths[i])
                if Depth.text == "1":
                    Type.text = ""
                    Title.text = str(self.taxTree_titles[i])
                    OrderNr.text = str(self.taxTree_orderNrs[i])
                else:
                    Type.text = "taxn"  # fix
                    Title.text = str(self.taxTree_titles[i])
                    OrderNr.text = str(self.taxTree_orderNrs[i])

                self.myroot.append(ExportItem)
                self.mytree.write(self.taxonomy_file_write)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)


        # Taxonomie Baum und Combobox aktualisieren
        self.taxonomy_frame_tree_picture.destroy()
        Formelfrage.scan_tax_tree(self)

        self.tax_nodes_myCombo.destroy()
        Formelfrage.tax_combobox_refresh(self)

    def tax_reallocate(self):
        print("REALLOCATE")
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == "1970392":
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

        self.reallocate_taxIds = []
        self.reallocate_childs = []
        self.reallocate_parents = []
        self.reallocate_depths = []
        self.reallocate_types = []
        self.reallocate_titles = []
        self.reallocate_orderNrs = []


        ##################################### Taxonomie Knoten löschen #####################################

        for taxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId'):
            self.reallocate_taxIds.append(taxId.text)
            # wert ist fix

        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
            self.reallocate_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
            self.reallocate_parents.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
            self.reallocate_depths.append(depth.text)

        for typ in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Type'):
            self.reallocate_types.append(typ.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
            self.reallocate_titles.append(title.text)

        for orderNr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
            self.reallocate_orderNrs.append(orderNr.text)

        # 1. Eintrag entfernen, da dieser Eintrag dem Taxonomie-Namen entspricht und nicht vom Knoten
        self.reallocate_titles.pop(0)



        # Alle TaxTree löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                if child.attrib['Entity'] == "tax_tree":
                    rec.remove(child)
        self.mytree.write(self.taxonomy_file_write)
        print("TaxTree Deleted!")

        ##############################
        # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
        # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)

        ############################



         # Alle Fragen im Array speichern bevor die XML gelöscht wird
        self.reallocate_child_id = []
        self.reallocate_node_id = []
        self.reallocate_item_id = []
        self.reallocate_item_list = []

        for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
            self.reallocate_child_id.append(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)

        for node_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId'):
            self.reallocate_node_id.append(node_id.text)

        for item_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId'):
            self.reallocate_item_id.append(item_id.text)

        self.reallocate_item_list =  list(zip(self.reallocate_item_id, self.reallocate_node_id))


        # Alle TaxNodeAssignments löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                if child.attrib['Entity'] == "tax_node_assignment":
                    rec.remove(child)
        self.mytree.write(self.taxonomy_file_write)
        print("Questions Deleted!")


        # TaxTree in Datei schreiben
        for i in range(len(self.reallocate_titles)):

            if self.reallocate_titles[i] != "delete":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxTree = ET.SubElement(Rec, 'TaxTree')
                TaxId = ET.SubElement(TaxTree, 'TaxId')
                Child = ET.SubElement(TaxTree, 'Child')
                Parent = ET.SubElement(TaxTree, 'Parent')
                Depth = ET.SubElement(TaxTree, 'Depth')
                Type = ET.SubElement(TaxTree, 'Type')
                Title = ET.SubElement(TaxTree, 'Title')
                OrderNr = ET.SubElement(TaxTree, 'OrderNr')


                Rec.set('Entity', "tax_tree")

                TaxId.text = str(self.tax_root_id)
                Child.text = str(self.reallocate_childs[i])
                Parent.text = str(self.reallocate_parents[i])
                Depth.text = str(self.reallocate_depths[i])
                if Depth.text == "1":
                    Type.text = ""
                    Title.text = str(self.reallocate_titles[i])
                    OrderNr.text = str(self.reallocate_orderNrs[i])
                else:
                    Type.text = "taxn"  # fix
                    Title.text = str(self.reallocate_titles[i])
                    OrderNr.text = str(self.reallocate_orderNrs[i])

                self.myroot.append(ExportItem)
                self.mytree.write(self.taxonomy_file_write)
        print("TaxTree's aktualisiert")

         # Wiederherstellen der Fragen die nicht auf "00000" gesetzt sind
        for i in range(len(self.reallocate_item_id)):
            if self.reallocate_node_id[i] != "00000":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxNodeAssignment = ET.SubElement(Rec, 'TaxNodeAssignment')
                NodeId = ET.SubElement(TaxNodeAssignment, 'NodeId')
                Component = ET.SubElement(TaxNodeAssignment, 'Component')
                ItemType = ET.SubElement(TaxNodeAssignment, 'ItemType')
                ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                # Rec = ET.SubElement(DataSet, 'ds:Rec')
                Rec.set('Entity', "tax_node_assignment")
                # ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                NodeId.text = self.reallocate_node_id[i]
                Component.text = "qpl"  # fix
                ItemType.text = "quest"  # fix
                ItemId.text = self.reallocate_item_id[i]

                self.myroot.append(ExportItem)
                self.mytree.write(self.taxonomy_file_write)
        print("Fragen in Nodes aktualisiert")

        # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
        # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)

    def tax_reallocate_from_excel(self, file_location):
        print("REALLOCATE")
        self.mytree = ET.parse(file_location)
        self.myroot = self.mytree.getroot()

        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == "1970392":
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

        self.reallocate_taxIds = []
        self.reallocate_childs = []
        self.reallocate_parents = []
        self.reallocate_depths = []
        self.reallocate_types = []
        self.reallocate_titles = []
        self.reallocate_orderNrs = []


        ##################################### Taxonomie Knoten löschen #####################################

        for taxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId'):
            self.reallocate_taxIds.append(taxId.text)
            # wert ist fix

        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
            self.reallocate_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
            self.reallocate_parents.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
            self.reallocate_depths.append(depth.text)

        for typ in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Type'):
            self.reallocate_types.append(typ.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
            self.reallocate_titles.append(title.text)

        for orderNr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
            self.reallocate_orderNrs.append(orderNr.text)

        # 1. Eintrag entfernen, da dieser Eintrag dem Taxonomie-Namen entspricht und nicht vom Knoten
        self.reallocate_titles.pop(0)



        # Alle TaxTree löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                if child.attrib['Entity'] == "tax_tree":
                    rec.remove(child)
        self.mytree.write(file_location)
        print("TaxTree Deleted!")

        ##############################
        # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
        # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, file_location)

        ############################



         # Alle Fragen im Array speichern bevor die XML gelöscht wird
        self.reallocate_child_id = []
        self.reallocate_node_id = []
        self.reallocate_item_id = []
        self.reallocate_item_list = []

        for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
            self.reallocate_child_id.append(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)

        for node_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId'):
            self.reallocate_node_id.append(node_id.text)

        for item_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId'):
            self.reallocate_item_id.append(item_id.text)

        self.reallocate_item_list =  list(zip(self.reallocate_item_id, self.reallocate_node_id))


        # Alle TaxNodeAssignments löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                if child.attrib['Entity'] == "tax_node_assignment":
                    rec.remove(child)
        self.mytree.write(file_location)
        print("Questions Deleted!")


        # TaxTree in Datei schreiben
        for i in range(len(self.reallocate_titles)):

            if self.reallocate_titles[i] != "delete":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxTree = ET.SubElement(Rec, 'TaxTree')
                TaxId = ET.SubElement(TaxTree, 'TaxId')
                Child = ET.SubElement(TaxTree, 'Child')
                Parent = ET.SubElement(TaxTree, 'Parent')
                Depth = ET.SubElement(TaxTree, 'Depth')
                Type = ET.SubElement(TaxTree, 'Type')
                Title = ET.SubElement(TaxTree, 'Title')
                OrderNr = ET.SubElement(TaxTree, 'OrderNr')


                Rec.set('Entity', "tax_tree")

                TaxId.text = str(self.tax_root_id)
                Child.text = str(self.reallocate_childs[i])
                Parent.text = str(self.reallocate_parents[i])
                Depth.text = str(self.reallocate_depths[i])
                if Depth.text == "1":
                    Type.text = ""
                    Title.text = str(self.reallocate_titles[i])
                    OrderNr.text = str(self.reallocate_orderNrs[i])
                else:
                    Type.text = "taxn"  # fix
                    Title.text = str(self.reallocate_titles[i])
                    OrderNr.text = str(self.reallocate_orderNrs[i])

                self.myroot.append(ExportItem)
                self.mytree.write(file_location)
        print("TaxTree's aktualisiert")

         # Wiederherstellen der Fragen die nicht auf "00000" gesetzt sind
        for i in range(len(self.reallocate_item_id)):
            if self.reallocate_node_id[i] != "00000":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxNodeAssignment = ET.SubElement(Rec, 'TaxNodeAssignment')
                NodeId = ET.SubElement(TaxNodeAssignment, 'NodeId')
                Component = ET.SubElement(TaxNodeAssignment, 'Component')
                ItemType = ET.SubElement(TaxNodeAssignment, 'ItemType')
                ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                # Rec = ET.SubElement(DataSet, 'ds:Rec')
                Rec.set('Entity', "tax_node_assignment")
                # ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                NodeId.text = self.reallocate_node_id[i]
                Component.text = "qpl"  # fix
                ItemType.text = "quest"  # fix
                ItemId.text = self.reallocate_item_id[i]

                self.myroot.append(ExportItem)
                self.mytree.write(file_location)
        print("Fragen in Nodes aktualisiert")

        # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
        # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, file_location)

    def tax_combobox_refresh (self):

        # ---- Alle Ebenen im Dokument suchen ---- #
        self.node_tag_update = []

        for TaxTree in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId').text == str(self.root_node):
                self.node_tag_update.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text)



        self.node_tag_update.sort(key=str.lower)


        self.tax_nodes_myCombo = ttk.Combobox(self.taxonomy_frame_boxes, value=self.node_tag_update, width=30)
        self.tax_nodes_myCombo.current(0)
        # self.tax_nodes_myCombo.bind("<<ComboboxSelected>>", selected_var)
        self.tax_nodes_myCombo.grid(row=1, column=2, sticky=W, padx=10, pady=5)

    def scan_tax_tree(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        self.taxonomy_frame_tree_picture_scroll = LabelFrame(self.taxonomy, text="Taxonomie Bild", padx=5, pady=5)
        self.taxonomy_frame_tree_picture_scroll.grid(row=0, column=1, padx=20, pady=450, sticky=NW)


        self.taxonomy_frame_tree_picture2 = ScrolledFrame(self.taxonomy_frame_tree_picture_scroll, height=250, width=200)
        self.taxonomy_frame_tree_picture2.pack(expand=1, fill="both")

        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.taxonomy_frame_tree_picture2.bind_arrow_keys(app)
        #self.taxonomy_frame_tree_picture2.bind_scroll_wheel(app)
        self.taxonomy_frame_tree_picture = self.taxonomy_frame_tree_picture2.display_widget(Frame)

        self.collect_childs = []
        self.collect_title = []
        self.collect_depth = []
        self.collect_parent = []
        self.collect_order_nr = []
        self.collect_labels_sorted = []

        self.tax_data = []
        self.id_to_depth_dict = {}
        self.parentId_to_title_dict = {}
        self.parentId_from_id_dict = {}
        self.title_to_id_dict = {}


        # Taxonomie Datei nach Hauptebene (ID und Name) suchen
        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == str(self.root_node):
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text
                self.tax_root_label = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text

               #print(self.parentId_to_title_dict)


        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
             self.collect_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
             self.collect_parent.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
             self.collect_depth.append(depth.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
             self.collect_title.append(title.text)
             #print(title.text)
        for order_nr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
             self.collect_order_nr.append(order_nr.text)








        self.tax_data =  list(zip( self.collect_childs, self.collect_parent, self.collect_depth, self.collect_title, self.collect_order_nr  ))



        # .pop(0) enfternt den 1. Eintrag aus der Liste. In Liste "Title" ist 1 Eintrag mehr enthalten, als in den restlichen Listen. Der Eintrag beschreibt den Taxonomie-Namen
        self.collect_title.pop(0)
        self.id_to_depth_dict = dict(zip(self.collect_childs, self.collect_depth))
        self.id_to_title_dict = dict(zip(self.collect_childs, self.collect_title))
        self.parentId_from_id_dict = dict(zip(self.collect_childs, self.collect_parent))




        # Bild in Labels erstellen
        self.tax_depth_0_label = Label(self.taxonomy_frame_tree_picture, text=str(self.tax_root_label))
        self.tax_depth_0_label.grid(sticky=W)


        # collect_title muss "i+1" da im '0'ten Fach der Hauptitel ist. Title[] ist 1 Fach größer als Child[]
        for i in range(len(self.collect_childs)):
            #print(self.collect_parent[i], self.collect_childs[i],self.id_to_depth_dict.get(self.collect_childs[i]), self.collect_title[i], self.collect_order_nr[i])


            if self.id_to_depth_dict.get(self.collect_childs[i]) == "2":
                self.tax_depth_1_label= Label(self.taxonomy_frame_tree_picture, text="     " + str(self.collect_title[i]))
                #self.tax_depth_1_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_1_label.cget("text"))

            if self.id_to_depth_dict.get(self.collect_childs[i]) == "3":
                self.tax_depth_2_label = Label(self.taxonomy_frame_tree_picture, text="         " + str(self.id_to_title_dict.get(self.collect_parent[i])) + "   ===>   " + str(self.collect_title[i]))
                #self.tax_depth_2_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_2_label.cget("text"))

            if self.id_to_depth_dict.get(self.collect_childs[i]) == "4":
                self.tax_depth_3_label = Label(self.taxonomy_frame_tree_picture, text="            " + str(self.id_to_title_dict.get(self.parentId_from_id_dict.get(self.collect_parent[i])))+ "  ===>    " +str(self.id_to_title_dict.get(self.collect_parent[i]))+ "   ===>   " + str(self.collect_title[i]))
                #self.tax_depth_3_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_3_label.cget("text"))



        for i in range(len(self.collect_labels_sorted)):
            self.collect_labels_sorted[i] = self.collect_labels_sorted[i].strip()

        self.collect_labels_sorted.sort()


        for i in range(len(self.collect_labels_sorted)):

            self.depth_count = "0"
            self.depth_count = self.collect_labels_sorted[i].count("==>")

            if self.depth_count == 0:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture, text="     " + self.collect_labels_sorted[i])
                self.sorted_labels.grid(sticky=W)

            if self.depth_count == 1:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture, text="         " + self.collect_labels_sorted[i])
                self.sorted_labels.grid(sticky=W)

            if self.depth_count == 2:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture, text="            " + self.collect_labels_sorted[i])
                self.sorted_labels.grid(sticky=W)

    def assign_questions_to_node(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()

        self.node_to_id_dict = {}
        self.child_tag_assign = []
        self.node_tag_assign = []

        # ---- Alle Ebenen im Dokument suchen ---- #
        for TaxTree in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxTree'):
            if TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxId').text == str(self.root_node):
                self.child_tag_assign.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child').text)
                self.node_tag_assign.append(TaxTree.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title').text)

        print("Nodes found: " + str(self.node_tag))
        print("with Child ID: " + str(self.child_tag))

        # convert list "child tag" and list "node_tag" to dictionary
        self.node_to_id_dict = dict(zip(self.node_tag_assign, self.child_tag_assign))
        print("------------------------------------------------")

        # Export XML-File
        # xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1"
        # xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3"
        # xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3"
        # xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">
        # Bsp: tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)

        # -------- Struktur einer "assignment to node" in der XML
        # < ds: Rec Entity = "tax_node_assignment" >
        #    < TaxNodeAssignment >
        #        < NodeId > 21682 < / NodeId >
        #        < Component > qpl < / Component >
        #        < ItemType > quest < / ItemType >
        #        < ItemId > 470081 < / ItemId >
        #    < / TaxNodeAssignment >
        # < / ds: Rec >


        if self.entry_starting_id.get() != "" and self.entry_ending_id.get() != "":
            self.starting_id = int(self.entry_starting_id.get()[:6])
            self.ending_id = int(self.entry_ending_id.get()[:6])

            for i in range(self.starting_id, self.ending_id+1):
                for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
                    if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text == str(i):
                        print("ID found: " + str(i))



        if self.node_to_id_dict.get(self.tax_nodes_myCombo.get()) != self.child_tag[0]:
            if self.entry_starting_id.get() != "" and self.entry_ending_id.get() != "":

                for i in range(self.starting_id, self.ending_id+1):
                    # Die Definition der Haupt- und Sub-Elemente muss in der Schleife für jede Frage neu erstellt werden
                    # Sonst haben die angehängten Fragen alle die gleichen Werte, da es sich auf das Gleiche "Attribut" handelt
                    Export = ET.Element('exp:Export')
                    ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                    DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                    Rec = ET.SubElement(DataSet, 'ds:Rec')
                    TaxNodeAssignment = ET.SubElement(Rec, 'TaxNodeAssignment')
                    NodeId = ET.SubElement(TaxNodeAssignment, 'NodeId')
                    Component = ET.SubElement(TaxNodeAssignment, 'Component')
                    ItemType = ET.SubElement(TaxNodeAssignment, 'ItemType')
                    ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')


                    #Rec = ET.SubElement(DataSet, 'ds:Rec')
                    Rec.set('Entity', "tax_node_assignment")
                    #ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                    NodeId.text = self.node_to_id_dict.get(self.tax_nodes_myCombo.get())

                    Component.text = "qpl"  # fix
                    ItemType.text = "quest" # fix
                    ItemId.text = str(i)     # Fragen ID üblicherweise > 100000, wenn Fragen ID z.B. 000001 dann ist der itemValue "nur" 1 und es fehlen nullen
                    self.myroot[0][len(self.myroot[0]) - 1].append(Rec)

                    #print("NodeId: " + NodeId.text)
                    #print("ItemId: " + ItemId.text)

                    self.mytree.write(self.taxonomy_file_write)

            else:
                print("Need starting/ending ID")
        else:
            print("Node for Questions not selected")


        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)


         # Taxonomie Fesnter wird "refreshed" um Text der Labels zu aktualisieren
        self.taxonomy_frame_labels.destroy()

        self.taxonomy_frame_labels_scroll= LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        #self.taxonomy_frame_labels2.bind_arrow_keys(app)
        #self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)

        #self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        #self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        Formelfrage.read_taxonomy_file(self)

    def test(self):
        self.taxonomy_qtiXML_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten",  self.ilias_id_pool_qpl, self.ilias_id_pool_qti_xml))


        # Fragen aus der qti Datei auslesen (FragenID, Fragentitel)
        self.mytree = ET.parse(self.taxonomy_qtiXML_file)
        self.myroot = self.mytree.getroot()

        self.item_id_list = []
        self.item_title_list = []

        for item in self.myroot.iter('item'):
            self.item_id_raw = str(item.get('ident'))
            self.item_id = self.item_id_raw.rsplit('_', 1)[-1]
            self.item_title = str(item.get('title'))
            self.item_id_list.append(self.item_id)
            self.item_title_list.append(self.item_title)

            print(self.item_id, self.item_title)

    def remove_question_from_node(self):
        self.mytree = ET.parse(self.taxonomy_file_read)
        self.myroot = self.mytree.getroot()



        # Alle Fragen im Array speichern bevor die XML gelöscht wird
        self.child_id = []
        self.node_id = []
        self.item_id = []
        self.item_list = []


        # Code setzt alle Node_Id's auf "00000" die in die Start/Ende Entry-Felder eingegeben wurden
        if self.entry_starting_id.get() != "" and self.entry_ending_id.get() != "":
            self.starting_id = int(self.entry_starting_id.get()[:6])
            self.ending_id = int(self.entry_ending_id.get()[:6])

            for i in range(self.starting_id, self.ending_id + 1):
                for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
                    if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text == str(i):
                        print("found ID: " + str(i))
                        print("removed from Node: " + str(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text))
                        tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text = "00000"
                        self.mytree.write(self.taxonomy_file_write)
                        #print("Code auf 00000")


        for node_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId'):
            self.node_id.append(node_id.text)

        for item_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId'):
            self.item_id.append(item_id.text)

        self.item_list =  list(zip(self.item_id, self.node_id))


        # Alle TaxNodeAssignments löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                #print(child)
                print(child.tag, child.text, child.attrib)

                if child.attrib['Entity'] == "tax_node_assignment":
                    rec.remove(child)
        self.mytree.write(self.taxonomy_file_write)
        print("Deleted!")




        # Wiederherstellen der Fragen die nicht auf "00000" gesetzt sind
        for i in range(len(self.item_id)):
            if self.node_id[i] != "00000":
                Export = ET.Element('exp:Export')
                ExportItem = ET.SubElement(Export, 'exp:ExportItem')
                DataSet = ET.SubElement(ExportItem, 'ds:DataSet')
                Rec = ET.SubElement(DataSet, 'ds:Rec')
                TaxNodeAssignment = ET.SubElement(Rec, 'TaxNodeAssignment')
                NodeId = ET.SubElement(TaxNodeAssignment, 'NodeId')
                Component = ET.SubElement(TaxNodeAssignment, 'Component')
                ItemType = ET.SubElement(TaxNodeAssignment, 'ItemType')
                ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                # Rec = ET.SubElement(DataSet, 'ds:Rec')
                Rec.set('Entity', "tax_node_assignment")
                # ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                NodeId.text = self.node_id[i]
                Component.text = "qpl"  # fix
                ItemType.text = "quest"  # fix
                ItemId.text = self.item_id[i]
                self.myroot[0][len(self.myroot[0]) - 1].append(Rec)

                self.mytree.write(self.taxonomy_file_write)
                print(ItemId.text + " with Node: " + NodeId.text + "... refreshed!")









        # Beim schreiben in die XML Datei müssen konvertierungen vorgenommen werden
        # Es wird automatisch "ns0" etc. durch Python geschrieben und muss in das ilias Format abgeändert werden
        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)



        # Taxonomie Fesnter wird "refreshed" um Text der Labels zu aktualisieren
        self.taxonomy_frame_labels.destroy()




        self.taxonomy_frame_labels_scroll= LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        #self.taxonomy_frame_labels2.bind_arrow_keys(app)
        #self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)


        #self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        #self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        Formelfrage.read_taxonomy_file(self)







    def reallocate_text(self):

        self.content = self.formula_question_entry.get("1.0", 'end-1c')
        self.numbers_of_searchterm_p = self.content.count("^")
        self.numbers_of_searchterm_b = self.content.count("_")
        self.numbers_of_searchterm_italic = self.content.count("//")
        self.search_index = '1.0'
        self.search_index_start = self.search_index
        self.search_index_end = self.search_index

        for x in range(self.numbers_of_searchterm_p):
            self.search_p1_begin = self.formula_question_entry.search('^', self.search_index_start, stopindex ="end")
            self.search_p1_end = self.formula_question_entry.search(" ", self.search_p1_begin, stopindex="end")
            self.formula_question_entry.tag_add('SUP', self.search_p1_begin, self.search_p1_end)
            self.formula_question_entry.tag_config('SUP', offset=4)
            self.formula_question_entry.tag_config('SUP', foreground='green')
            self.search_index_start = self.search_p1_end
            self.search_index_end = self.search_p1_begin


        self.search_index = '1.0'
        self.search_index_start = self.search_index
        self.search_index_end = self.search_index
        for y in range(self.numbers_of_searchterm_b):
            self.search_b1_begin = self.formula_question_entry.search('_', self.search_index_start, stopindex ="end")
            self.search_b1_end = self.formula_question_entry.search(" ", self.search_b1_begin, stopindex="end")
            self.formula_question_entry.tag_add('SUB', self.search_b1_begin, self.search_b1_end)
            self.formula_question_entry.tag_config('SUB', offset=-4)
            self.formula_question_entry.tag_config('SUB', foreground='blue')
            self.search_index_start = self.search_b1_end
            self.search_index_end = self.search_b1_begin





        self.search_index = '1.0'
        self.search_index_start = self.search_index
        print(self.search_index_start)
        self.search_index_end = self.search_index
        for z in range(self.numbers_of_searchterm_italic):
            try:
                self.search_italic1_begin = self.formula_question_entry.search('//', self.search_index_start, stopindex="end")
                self.search_italic1_end = self.formula_question_entry.search('///', self.search_italic1_begin , stopindex="end")
                self.formula_question_entry.tag_add('ITALIC', self.search_italic1_begin, self.search_italic1_end + '+3c')
                self.formula_question_entry.tag_config('ITALIC', foreground='brown')
                self.formula_question_entry.tag_config('ITALIC', font=('Times New Roman', 9, 'italic'))
                self.search_index_start = self.search_italic1_end + '+3c'
                self.search_index_end = self.search_italic1_begin

            except:
                print("Index error in italic-function -> can be ignored ")

        print("Question entry text... re-allocated!")
        # -----------------------Place Label & Entry-Boxes for Variable  on GUI
    def var2_show(self):
            self.variable2_label.grid(row=7, column=0, sticky=W, padx=20)
            self.var2_name_entry.grid(row=7, column=1, sticky=W)
            self.var2_min_entry.grid(row=7, column=1, sticky=W, padx=60)
            self.var2_max_entry.grid(row=7, column=1, sticky=W, padx=100)
            self.var2_prec_entry.grid(row=7, column=1, sticky=W, padx=140)
            self.var2_divby_entry.grid(row=7, column=1, sticky=W, padx=180)
            #self.var2_unit_myCombo.grid(row=7, column=0, sticky=E, padx=10)
    def var3_show(self):
            self.variable3_label.grid(row=8, column=0, sticky=W, padx=20)
            self.var3_name_entry.grid(row=8, column=1, sticky=W)
            self.var3_min_entry.grid(row=8, column=1, sticky=W, padx=60)
            self.var3_max_entry.grid(row=8, column=1, sticky=W, padx=100)
            self.var3_prec_entry.grid(row=8, column=1, sticky=W, padx=140)
            self.var3_divby_entry.grid(row=8, column=1, sticky=W, padx=180)
            #self.var3_unit_myCombo.grid(row=8, column=0, sticky=E, padx=10)
    def var4_show(self):
            self.variable4_label.grid(row=9, column=0, sticky=W, padx=20)
            self.var4_name_entry.grid(row=9, column=1, sticky=W)
            self.var4_min_entry.grid(row=9, column=1, sticky=W, padx=60)
            self.var4_max_entry.grid(row=9, column=1, sticky=W, padx=100)
            self.var4_prec_entry.grid(row=9, column=1, sticky=W, padx=140)
            self.var4_divby_entry.grid(row=9, column=1, sticky=W, padx=180)
            #self.var4_unit_myCombo.grid(row=9, column=0, sticky=E, padx=10)

    def var5_show(self):
        self.variable5_label.grid(row=10, column=0, sticky=W, padx=20)
        self.var5_name_entry.grid(row=10, column=1, sticky=W)
        self.var5_min_entry.grid(row=10, column=1, sticky=W, padx=60)
        self.var5_max_entry.grid(row=10, column=1, sticky=W, padx=100)
        self.var5_prec_entry.grid(row=10, column=1, sticky=W, padx=140)
        self.var5_divby_entry.grid(row=10, column=1, sticky=W, padx=180)
        #self.var5_unit_myCombo.grid(row=10, column=0, sticky=E, padx=10)

    def var6_show(self):
        self.variable6_label.grid(row=11, column=0, sticky=W, padx=20)
        self.var6_name_entry.grid(row=11, column=1, sticky=W)
        self.var6_min_entry.grid(row=11, column=1, sticky=W, padx=60)
        self.var6_max_entry.grid(row=11, column=1, sticky=W, padx=100)
        self.var6_prec_entry.grid(row=11, column=1, sticky=W, padx=140)
        self.var6_divby_entry.grid(row=11, column=1, sticky=W, padx=180)
        #self.var6_unit_myCombo.grid(row=11, column=0, sticky=E, padx=10)

    def var7_show(self):
        self.variable7_label.grid(row=12, column=0, sticky=W, padx=20)
        self.var7_name_entry.grid(row=12, column=1, sticky=W)
        self.var7_min_entry.grid(row=12, column=1, sticky=W, padx=60)
        self.var7_max_entry.grid(row=12, column=1, sticky=W, padx=100)
        self.var7_prec_entry.grid(row=12, column=1, sticky=W, padx=140)
        self.var7_divby_entry.grid(row=12, column=1, sticky=W, padx=180)
        #self.var7_unit_myCombo.grid(row=12, column=0, sticky=E, padx=10)

    def var8_show(self):
        self.variable8_label.grid(row=13, column=0, sticky=W, padx=20)
        self.var8_name_entry.grid(row=13, column=1, sticky=W)
        self.var8_min_entry.grid(row=13, column=1, sticky=W, padx=60)
        self.var8_max_entry.grid(row=13, column=1, sticky=W, padx=100)
        self.var8_prec_entry.grid(row=13, column=1, sticky=W, padx=140)
        self.var8_divby_entry.grid(row=13, column=1, sticky=W, padx=180)
        #self.var8_unit_myCombo.grid(row=13, column=0, sticky=E, padx=10)

    def var9_show(self):
        self.variable9_label.grid(row=14, column=0, sticky=W, padx=20)
        self.var9_name_entry.grid(row=14, column=1, sticky=W)
        self.var9_min_entry.grid(row=14, column=1, sticky=W, padx=60)
        self.var9_max_entry.grid(row=14, column=1, sticky=W, padx=100)
        self.var9_prec_entry.grid(row=14, column=1, sticky=W, padx=140)
        self.var9_divby_entry.grid(row=14, column=1, sticky=W, padx=180)
        #self.var9_unit_myCombo.grid(row=14, column=0, sticky=E, padx=10)

    def var10_show(self):
        self.variable10_label.grid(row=15, column=0, sticky=W, padx=20)
        self.var10_name_entry.grid(row=15, column=1, sticky=W)
        self.var10_min_entry.grid(row=15, column=1, sticky=W, padx=60)
        self.var10_max_entry.grid(row=15, column=1, sticky=W, padx=100)
        self.var10_prec_entry.grid(row=15, column=1, sticky=W, padx=140)
        self.var10_divby_entry.grid(row=15, column=1, sticky=W, padx=180)
        #self.var10_unit_myCombo.grid(row=15, column=0, sticky=E, padx=10)


    def var2_remove(self):
        self.variable2_label.grid_remove()
        self.var2_name_entry.grid_remove()
        self.var2_min_entry.grid_remove()
        self.var2_max_entry.grid_remove()
        self.var2_prec_entry.grid_remove()
        self.var2_divby_entry.grid_remove()
        #self.var2_unit_myCombo.grid_remove()
    def var3_remove(self):
        self.variable3_label.grid_remove()
        self.var3_name_entry.grid_remove()
        self.var3_min_entry.grid_remove()
        self.var3_max_entry.grid_remove()
        self.var3_prec_entry.grid_remove()
        self.var3_divby_entry.grid_remove()
        #self.var3_unit_myCombo.grid_remove()
    def var4_remove(self):
        self.variable4_label.grid_remove()
        self.var4_name_entry.grid_remove()
        self.var4_min_entry.grid_remove()
        self.var4_max_entry.grid_remove()
        self.var4_prec_entry.grid_remove()
        self.var4_divby_entry.grid_remove()
        #self.var4_unit_myCombo.grid_remove()
    def var5_remove(self):
        self.variable5_label.grid_remove()
        self.var5_name_entry.grid_remove()
        self.var5_min_entry.grid_remove()
        self.var5_max_entry.grid_remove()
        self.var5_prec_entry.grid_remove()
        self.var5_divby_entry.grid_remove()
        #self.var5_unit_myCombo.grid_remove()
    def var6_remove(self):
        self.variable6_label.grid_remove()
        self.var6_name_entry.grid_remove()
        self.var6_min_entry.grid_remove()
        self.var6_max_entry.grid_remove()
        self.var6_prec_entry.grid_remove()
        self.var6_divby_entry.grid_remove()
        #self.var6_unit_myCombo.grid_remove()
    def var7_remove(self):
        self.variable7_label.grid_remove()
        self.var7_name_entry.grid_remove()
        self.var7_min_entry.grid_remove()
        self.var7_max_entry.grid_remove()
        self.var7_prec_entry.grid_remove()
        self.var7_divby_entry.grid_remove()
        #self.var7_unit_myCombo.grid_remove()
    def var8_remove(self):
        self.variable8_label.grid_remove()
        self.var8_name_entry.grid_remove()
        self.var8_min_entry.grid_remove()
        self.var8_max_entry.grid_remove()
        self.var8_prec_entry.grid_remove()
        self.var8_divby_entry.grid_remove()
        #self.var8_unit_myCombo.grid_remove()
    def var9_remove(self):
        self.variable9_label.grid_remove()
        self.var9_name_entry.grid_remove()
        self.var9_min_entry.grid_remove()
        self.var9_max_entry.grid_remove()
        self.var9_prec_entry.grid_remove()
        self.var9_divby_entry.grid_remove()
        #self.var9_unit_myCombo.grid_remove()
    def var10_remove(self):
        self.variable10_label.grid_remove()
        self.var10_name_entry.grid_remove()
        self.var10_min_entry.grid_remove()
        self.var10_max_entry.grid_remove()
        self.var10_prec_entry.grid_remove()
        self.var10_divby_entry.grid_remove()
        #self.var10_unit_myCombo.grid_remove()


    def res2_show(self):
        self.result2_label.grid(row=22, column=0, sticky=W, padx=20)
        self.res2_name_entry.grid(row=22, column=1, sticky=W)
        self.res2_min_entry.grid(row=22, column=1, sticky=W, padx=60)
        self.res2_max_entry.grid(row=22, column=1, sticky=W, padx=100)
        self.res2_prec_entry.grid(row=22, column=1, sticky=W, padx=140)
        self.res2_tol_entry.grid(row=22, column=1, sticky=W, padx=180)
        self.res2_points_entry.grid(row=22, column=1, sticky=W, padx=220)
        self.res2_formula_entry.grid(row=22, column=1, sticky=E, padx=20)
        #self.res2_unit_myCombo.grid(row=22, column=0, sticky=E, padx=10)
    def res3_show(self):
        self.result3_label.grid(row=23, column=0, sticky=W, padx=20)
        self.res3_name_entry.grid(row=23, column=1, sticky=W)
        self.res3_min_entry.grid(row=23, column=1, sticky=W, padx=60)
        self.res3_max_entry.grid(row=23, column=1, sticky=W, padx=100)
        self.res3_prec_entry.grid(row=23, column=1, sticky=W, padx=140)
        self.res3_tol_entry.grid(row=23, column=1, sticky=W, padx=180)
        self.res3_points_entry.grid(row=23, column=1, sticky=W, padx=220)
        self.res3_formula_entry.grid(row=23, column=1, sticky=E, padx=20)
        #self.res3_unit_myCombo.grid(row=23, column=0, sticky=E, padx=10)
    def res4_show(self):
        self.result4_label.grid(row=24, column=0, sticky=W, padx=20)
        self.res4_name_entry.grid(row=24, column=1, sticky=W)
        self.res4_min_entry.grid(row=24, column=1, sticky=W, padx=60)
        self.res4_max_entry.grid(row=24, column=1, sticky=W, padx=100)
        self.res4_prec_entry.grid(row=24, column=1, sticky=W, padx=140)
        self.res4_tol_entry.grid(row=24, column=1, sticky=W, padx=180)
        self.res4_points_entry.grid(row=24, column=1, sticky=W, padx=220)
        self.res4_formula_entry.grid(row=24, column=1, sticky=E, padx=20)
        #self.res4_unit_myCombo.grid(row=24, column=0, sticky=E, padx=10)
    def res5_show(self):
        self.result5_label.grid(row=25, column=0, sticky=W, padx=20)
        self.res5_name_entry.grid(row=25, column=1, sticky=W)
        self.res5_min_entry.grid(row=25, column=1, sticky=W, padx=60)
        self.res5_max_entry.grid(row=25, column=1, sticky=W, padx=100)
        self.res5_prec_entry.grid(row=25, column=1, sticky=W, padx=140)
        self.res5_tol_entry.grid(row=25, column=1, sticky=W, padx=180)
        self.res5_points_entry.grid(row=25, column=1, sticky=W, padx=220)
        self.res5_formula_entry.grid(row=25, column=1, sticky=E, padx=20)
        #self.res5_unit_myCombo.grid(row=25, column=0, sticky=E, padx=10)
    def res6_show(self):
        self.result6_label.grid(row=26, column=0, sticky=W, padx=20)
        self.res6_name_entry.grid(row=26, column=1, sticky=W)
        self.res6_min_entry.grid(row=26, column=1, sticky=W, padx=60)
        self.res6_max_entry.grid(row=26, column=1, sticky=W, padx=100)
        self.res6_prec_entry.grid(row=26, column=1, sticky=W, padx=140)
        self.res6_tol_entry.grid(row=26, column=1, sticky=W, padx=180)
        self.res6_points_entry.grid(row=26, column=1, sticky=W, padx=220)
        self.res6_formula_entry.grid(row=26, column=1, sticky=E, padx=20)
        #self.res6_unit_myCombo.grid(row=26, column=0, sticky=E, padx=10)
    def res7_show(self):
        self.result7_label.grid(row=27, column=0, sticky=W, padx=20)
        self.res7_name_entry.grid(row=27, column=1, sticky=W)
        self.res7_min_entry.grid(row=27, column=1, sticky=W, padx=60)
        self.res7_max_entry.grid(row=27, column=1, sticky=W, padx=100)
        self.res7_prec_entry.grid(row=27, column=1, sticky=W, padx=140)
        self.res7_tol_entry.grid(row=27, column=1, sticky=W, padx=180)
        self.res7_points_entry.grid(row=27, column=1, sticky=W, padx=220)
        self.res7_formula_entry.grid(row=27, column=1, sticky=E, padx=20)
        #self.res7_unit_myCombo.grid(row=27, column=0, sticky=E, padx=10)
    def res8_show(self):
        self.result8_label.grid(row=28, column=0, sticky=W, padx=20)
        self.res8_name_entry.grid(row=28, column=1, sticky=W)
        self.res8_min_entry.grid(row=28, column=1, sticky=W, padx=60)
        self.res8_max_entry.grid(row=28, column=1, sticky=W, padx=100)
        self.res8_prec_entry.grid(row=28, column=1, sticky=W, padx=140)
        self.res8_tol_entry.grid(row=28, column=1, sticky=W, padx=180)
        self.res8_points_entry.grid(row=28, column=1, sticky=W, padx=220)
        self.res8_formula_entry.grid(row=28, column=1, sticky=E, padx=20)
        #self.res8_unit_myCombo.grid(row=28, column=0, sticky=E, padx=10)
    def res9_show(self):
        self.result9_label.grid(row=29, column=0, sticky=W, padx=20)
        self.res9_name_entry.grid(row=29, column=1, sticky=W)
        self.res9_min_entry.grid(row=29, column=1, sticky=W, padx=60)
        self.res9_max_entry.grid(row=29, column=1, sticky=W, padx=100)
        self.res9_prec_entry.grid(row=29, column=1, sticky=W, padx=140)
        self.res9_tol_entry.grid(row=29, column=1, sticky=W, padx=180)
        self.res9_points_entry.grid(row=29, column=1, sticky=W, padx=220)
        self.res9_formula_entry.grid(row=29, column=1, sticky=E, padx=20)
        #self.res9_unit_myCombo.grid(row=29, column=0, sticky=E, padx=10)
    def res10_show(self):
        self.result10_label.grid(row=30, column=0, sticky=W, padx=20)
        self.res10_name_entry.grid(row=30, column=1, sticky=W)
        self.res10_min_entry.grid(row=30, column=1, sticky=W, padx=60)
        self.res10_max_entry.grid(row=30, column=1, sticky=W, padx=100)
        self.res10_prec_entry.grid(row=30, column=1, sticky=W, padx=140)
        self.res10_tol_entry.grid(row=30, column=1, sticky=W, padx=180)
        self.res10_points_entry.grid(row=30, column=1, sticky=W, padx=220)
        self.res10_formula_entry.grid(row=30, column=1, sticky=E, padx=20)
        #self.res10_unit_myCombo.grid(row=30, column=0, sticky=E, padx=10)

    def res2_remove(self):
        self.result2_label.grid_remove()
        self.res2_name_entry.grid_remove()
        self.res2_min_entry.grid_remove()
        self.res2_max_entry.grid_remove()
        self.res2_prec_entry.grid_remove()
        self.res2_tol_entry.grid_remove()
        self.res2_points_entry.grid_remove()
        self.res2_formula_entry.grid_remove()
        self.res2_unit_myCombo.grid_remove()
    def res3_remove(self):
        self.result3_label.grid_remove()
        self.res3_name_entry.grid_remove()
        self.res3_min_entry.grid_remove()
        self.res3_max_entry.grid_remove()
        self.res3_prec_entry.grid_remove()
        self.res3_tol_entry.grid_remove()
        self.res3_points_entry.grid_remove()
        self.res3_formula_entry.grid_remove()
        self.res3_unit_myCombo.grid_remove()
    def res4_remove(self):
        self.result4_label.grid_remove()
        self.res4_name_entry.grid_remove()
        self.res4_min_entry.grid_remove()
        self.res4_max_entry.grid_remove()
        self.res4_prec_entry.grid_remove()
        self.res4_tol_entry.grid_remove()
        self.res4_points_entry.grid_remove()
        self.res4_formula_entry.grid_remove()
        #self.res4_unit_myCombo.grid_remove()
    def res5_remove(self):
        self.result5_label.grid_remove()
        self.res5_name_entry.grid_remove()
        self.res5_min_entry.grid_remove()
        self.res5_max_entry.grid_remove()
        self.res5_prec_entry.grid_remove()
        self.res5_tol_entry.grid_remove()
        self.res5_points_entry.grid_remove()
        self.res5_formula_entry.grid_remove()
       # self.res5_unit_myCombo.grid_remove()
    def res6_remove(self):
        self.result6_label.grid_remove()
        self.res6_name_entry.grid_remove()
        self.res6_min_entry.grid_remove()
        self.res6_max_entry.grid_remove()
        self.res6_prec_entry.grid_remove()
        self.res6_tol_entry.grid_remove()
        self.res6_points_entry.grid_remove()
        self.res6_formula_entry.grid_remove()
        #self.res6_unit_myCombo.grid_remove()
    def res7_remove(self):
        self.result7_label.grid_remove()
        self.res7_name_entry.grid_remove()
        self.res7_min_entry.grid_remove()
        self.res7_max_entry.grid_remove()
        self.res7_prec_entry.grid_remove()
        self.res7_tol_entry.grid_remove()
        self.res7_points_entry.grid_remove()
        self.res7_formula_entry.grid_remove()
        #self.res7_unit_myCombo.grid_remove()
    def res8_remove(self):
        self.result8_label.grid_remove()
        self.res8_name_entry.grid_remove()
        self.res8_min_entry.grid_remove()
        self.res8_max_entry.grid_remove()
        self.res8_prec_entry.grid_remove()
        self.res8_tol_entry.grid_remove()
        self.res8_points_entry.grid_remove()
        self.res8_formula_entry.grid_remove()
       # self.res8_unit_myCombo.grid_remove()
    def res9_remove(self):
        self.result9_label.grid_remove()
        self.res9_name_entry.grid_remove()
        self.res9_min_entry.grid_remove()
        self.res9_max_entry.grid_remove()
        self.res9_prec_entry.grid_remove()
        self.res9_tol_entry.grid_remove()
        self.res9_points_entry.grid_remove()
        self.res9_formula_entry.grid_remove()
        #self.res9_unit_myCombo.grid_remove()
    def res10_remove(self):
        self.result10_label.grid_remove()
        self.res10_name_entry.grid_remove()
        self.res10_min_entry.grid_remove()
        self.res10_max_entry.grid_remove()
        self.res10_prec_entry.grid_remove()
        self.res10_tol_entry.grid_remove()
        self.res10_points_entry.grid_remove()
        self.res10_formula_entry.grid_remove()
        #self.res10_unit_myCombo.grid_remove()

    def selected_var_from_db(self, nr):  # "variable" need for comboBox Binding
        if nr == '1':
            Formelfrage.var2_remove(self)
            Formelfrage.var3_remove(self)
            Formelfrage.var4_remove(self)
            Formelfrage.var5_remove(self)
            Formelfrage.var6_remove(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '2':
            Formelfrage.var2_show(self)
            Formelfrage.var3_remove(self)
            Formelfrage.var4_remove(self)
            Formelfrage.var5_remove(self)
            Formelfrage.var6_remove(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '3':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_remove(self)
            Formelfrage.var5_remove(self)
            Formelfrage.var6_remove(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '4':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_remove(self)
            Formelfrage.var6_remove(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '5':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_remove(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '6':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_show(self)
            Formelfrage.var7_remove(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '7':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_show(self)
            Formelfrage.var7_show(self)
            Formelfrage.var8_remove(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '8':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_show(self)
            Formelfrage.var7_show(self)
            Formelfrage.var8_show(self)
            Formelfrage.var9_remove(self)
            Formelfrage.var10_remove(self)

        elif nr == '9':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_show(self)
            Formelfrage.var7_show(self)
            Formelfrage.var8_show(self)
            Formelfrage.var9_show(self)
            Formelfrage.var10_remove(self)

        elif nr == '10':
            Formelfrage.var2_show(self)
            Formelfrage.var3_show(self)
            Formelfrage.var4_show(self)
            Formelfrage.var5_show(self)
            Formelfrage.var6_show(self)
            Formelfrage.var7_show(self)
            Formelfrage.var8_show(self)
            Formelfrage.var9_show(self)
            Formelfrage.var10_show(self)

    def selected_res_from_db(self, nr):

        if nr == '1':
            Formelfrage.res2_remove(self)
            Formelfrage.res3_remove(self)
            Formelfrage.res4_remove(self)
            Formelfrage.res5_remove(self)
            Formelfrage.res6_remove(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)

        elif nr == '2':
            Formelfrage.res2_show(self)
            Formelfrage.res3_remove(self)
            Formelfrage.res4_remove(self)
            Formelfrage.res5_remove(self)
            Formelfrage.res6_remove(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)

        elif nr == '3':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_remove(self)
            Formelfrage.res5_remove(self)
            Formelfrage.res6_remove(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '4':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_remove(self)
            Formelfrage.res6_remove(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '5':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_remove(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '6':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_show(self)
            Formelfrage.res7_remove(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '7':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_show(self)
            Formelfrage.res7_show(self)
            Formelfrage.res8_remove(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '8':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_show(self)
            Formelfrage.res7_show(self)
            Formelfrage.res8_show(self)
            Formelfrage.res9_remove(self)
            Formelfrage.res10_remove(self)
        elif nr == '9':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_show(self)
            Formelfrage.res7_show(self)
            Formelfrage.res8_show(self)
            Formelfrage.res9_show(self)
            Formelfrage.res10_remove(self)
        elif nr == '10':
            Formelfrage.res2_show(self)
            Formelfrage.res3_show(self)
            Formelfrage.res4_show(self)
            Formelfrage.res5_show(self)
            Formelfrage.res6_show(self)
            Formelfrage.res7_show(self)
            Formelfrage.res8_show(self)
            Formelfrage.res9_show(self)
            Formelfrage.res10_show(self)


"""
class SingleChoice(Formelfrage):
    def __init__(self):
        # self.my_frame = Frame(master)
        # self.my_frame.grid()

        self.sc_frame = LabelFrame(self.singleChoice_tab, text="Single Choice", padx=5, pady=5)
        self.sc_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.sc_question_title_label = Label(self.sc_frame, text="Titel")
        self.sc_question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.sc_question_title_entry = Entry(self.sc_frame, width=60)
        self.sc_question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        # sc_author_label = Label(sc_frame, text="Autor")
        # sc_author_label.grid(row=1, column=0, sticky=W, padx=10)
        # sc_author_entry = Entry(sc_frame, width=60)
        # sc_author_entry.grid(row=1, column=1, sticky=W)

        self.sc_question_description_label = Label(self.sc_frame, text="Beschreibung")
        self.sc_question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.sc_question_description_entry = Entry(self.sc_frame, width=60)
        self.sc_question_description_entry.grid(row=2, column=1, sticky=W)

        self.sc_question_textfield_label = Label(self.sc_frame, text="Frage")
        self.sc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.sc_bar = Scrollbar(self.sc_frame)
        self.sc_infobox = Text(self.sc_frame, height=6, width=80, font=('Helvetica', 9))
        self.sc_bar.grid(row=3, column=2, sticky=W)
        self.sc_infobox.grid(row=3, column=1, pady=10, sticky=W)
        self.sc_bar.config(command=self.sc_infobox.yview)
        self.sc_infobox.config(yscrollcommand=self.sc_bar.set)

        self.sc_processing_time_label = Label(self.sc_frame, text="Bearbeitungsdauer")
        self.sc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.sc_processing_time_label = Label(self.sc_frame, text="Std:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Min:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.sc_processing_time_label = Label(self.sc_frame, text="Sek:")
        self.sc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        ### Preview LaTeX
        #expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
        #preview(expr, viewer='file', filename='output.png')

        #file_image = ImageTk.PhotoImage(Image.open('output.png'))
        #file_image_label = Label(self.sc_frame, image=file_image)
        #file_image_label.image = file_image

        #def latex_preview():
        #    file_image_label.grid(row=20, column=1, pady=20)

        #self.myLatex_btn = Button(self.sc_frame, text="show LaTeX Preview", command=latex_preview)
        #self.myLatex_btn.grid(row=4, column=1, sticky=E)

        ###

        self.sc_processingtime_hours = list(range(24))
        self.sc_processingtime_minutes = list(range(60))
        self.sc_processingtime_seconds = list(range(60))

        self.sc_proc_hours_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_hours, width=2)
        self.sc_proc_minutes_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_minutes, width=2)
        self.sc_proc_seconds_box = ttk.Combobox(self.sc_frame, value=self.sc_processingtime_seconds, width=2)

        self.sc_proc_hours_box.current(0)
        self.sc_proc_minutes_box.current(0)
        self.sc_proc_seconds_box.current(0)

        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")
        self.sc_proc_hours_box.bind("<<ComboboxSelected>>")

        self.sc_proc_hours_box.grid(row=4, column=1, sticky=W, padx=25, pady=(5, 0))
        self.sc_proc_minutes_box.grid(row=4, column=1, sticky=W, padx=100, pady=(5, 0))
        self.sc_proc_seconds_box.grid(row=4, column=1, sticky=W, padx=170, pady=(5, 0))

        self.sc_mix_questions_label = Label(self.sc_frame, text="Fragen mischen")
        self.sc_mix_questions_label.grid(row=5, column=0, sticky=W, padx=10, pady=(5, 0))

        self.sc_var_mix_questions = StringVar()
        self.sc_check_mix_questions = Checkbutton(self.sc_frame, text="", variable=self.sc_var_mix_questions, onvalue="1", offvalue="0")
        self.sc_check_mix_questions.deselect()
        self.sc_check_mix_questions.grid(row=5, column=1, sticky=W, pady=(5, 0))

        

        def sc_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

            if self.sc_numbers_of_answers_box.get() == '1':
                sc_var2_remove()
                sc_var3_remove()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '2':
                sc_var2_show()
                sc_var3_remove()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '3':
                sc_var2_show()
                sc_var3_show()
                sc_var4_remove()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '4':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_remove()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '5':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_remove()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '6':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_remove()


            elif self.sc_numbers_of_answers_box.get() == '7':
                sc_var2_show()
                sc_var3_show()
                sc_var4_show()
                sc_var5_show()
                sc_var6_show()
                sc_var7_show()

        self.sc_numbers_of_answers_box_label = Label(self.sc_frame, text="Anzahl der Antworten")
        self.sc_numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.sc_numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7"]
        self.sc_numbers_of_answers_box = ttk.Combobox(self.sc_frame, value=self.sc_numbers_of_answers_value, width=20)
        self.sc_numbers_of_answers_box.bind("<<ComboboxSelected>>", sc_answer_selected)
        self.sc_numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))
        self.sc_numbers_of_answers_box.current(0)

        # self.Label(self.sc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.sc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.sc_response_img_label = Label(self.sc_frame, text="Antwort-Grafik")
        self.sc_response_img_label.grid(row=8, column=1, sticky=E, padx=40)
        self.sc_response_points_label = Label(self.sc_frame, text="Punkte")
        self.sc_response_points_label.grid(row=8, column=2, sticky=W, padx=20)
        

        # ------------------------------- VARIABLES RANGE: MINIMUM - TEXT & ENTRY --------------------------------------------
        self.sc_var1_answer_text, self.sc_var1_points_text, self.sc_var1_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var2_answer_text, self.sc_var2_points_text, self.sc_var2_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var3_answer_text, self.sc_var3_points_text, self.sc_var3_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var4_answer_text, self.sc_var4_points_text, self.sc_var4_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var5_answer_text, self.sc_var5_points_text, self.sc_var5_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var6_answer_text, self.sc_var6_points_text, self.sc_var6_img_label_text = StringVar(), StringVar(), StringVar()
        self.sc_var7_answer_text, self.sc_var7_points_text, self.sc_var7_img_label_text = StringVar(), StringVar(), StringVar()

        self.sc_var1_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var1_answer_text, width=40)
        self.sc_var2_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var2_answer_text, width=40)
        self.sc_var3_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var3_answer_text, width=40)
        self.sc_var4_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var4_answer_text, width=40)
        self.sc_var5_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var5_answer_text, width=40)
        self.sc_var6_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var6_answer_text, width=40)
        self.sc_var7_answer_entry = Entry(self.sc_frame, textvariable=self.sc_var7_answer_text, width=40)

        # ------------------------------- VARIABLES RANGE:  MAXIMUM - TEXT & ENTRY --------------------------------------------

        self.sc_var1_points_entry = Entry(self.sc_frame, textvariable=self.sc_var1_points_text, width=8)
        self.sc_var2_points_entry = Entry(self.sc_frame, textvariable=self.sc_var2_points_text, width=8)
        self.sc_var3_points_entry = Entry(self.sc_frame, textvariable=self.sc_var3_points_text, width=8)
        self.sc_var4_points_entry = Entry(self.sc_frame, textvariable=self.sc_var4_points_text, width=8)
        self.sc_var5_points_entry = Entry(self.sc_frame, textvariable=self.sc_var5_points_text, width=8)
        self.sc_var6_points_entry = Entry(self.sc_frame, textvariable=self.sc_var6_points_text, width=8)
        self.sc_var7_points_entry = Entry(self.sc_frame, textvariable=self.sc_var7_points_text, width=8)
        
        
        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        self.sc_var1_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var1_img_label_entry))
        self.sc_var2_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var2_img_label_entry))
        self.sc_var3_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var3_img_label_entry))
        self.sc_var4_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var4_img_label_entry))
        self.sc_var5_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var5_img_label_entry))
        self.sc_var6_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var6_img_label_entry))
        self.sc_var7_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var7_img_label_entry))
        
        
        
        
        
        
        
        
        


        # ------------------------------- VARIABLES PRECISION - TEXT & ENTRY --------------------------------------------

        self.sc_var1_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var1_img_label_text, width=30)
        self.sc_var2_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var2_img_label_text, width=30)
        self.sc_var3_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var3_img_label_text, width=30)
        self.sc_var4_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var4_img_label_text, width=30)
        self.sc_var5_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var5_img_label_text, width=30)
        self.sc_var6_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var6_img_label_text, width=30)
        self.sc_var7_img_label_entry = Entry(self.sc_frame, textvariable=self.sc_var7_img_label_text, width=30)

        self.sc_answer1_label = Label(self.sc_frame, text="Antwort-Text 1")
        self.sc_answer2_label = Label(self.sc_frame, text="Antwort-Text 2")
        self.sc_answer3_label = Label(self.sc_frame, text="Antwort-Text 3")
        self.sc_answer4_label = Label(self.sc_frame, text="Antwort-Text 4")
        self.sc_answer5_label = Label(self.sc_frame, text="Antwort-Text 5")
        self.sc_answer6_label = Label(self.sc_frame, text="Antwort-Text 6")
        self.sc_answer7_label = Label(self.sc_frame, text="Antwort-Text 7")

        self.sc_answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.sc_var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.sc_var1_img_label_entry.grid(row=10, column=1, sticky=E, padx=0)
        self.sc_var1_points_entry.grid(row=10, column=2,sticky = W, padx = 20)
        self.sc_var1_select_img_btn.grid(row=10, column=1, sticky=E, padx=200)
        
        def sc_var2_show():
            self.sc_answer2_label.grid(row=11, column=0, sticky=W, padx=30)
            self.sc_var2_answer_entry.grid(row=11, column=1, sticky=W)
            self.sc_var2_img_label_entry.grid(row=11, column=1, sticky=E, padx=0)
            self.sc_var2_points_entry.grid(row=11, column=2)
            self.sc_var2_select_img_btn.grid(row=11, column=1, sticky=E, padx=200)

        def sc_var3_show():
            self.sc_answer3_label.grid(row=12, column=0, sticky=W, padx=30)
            self.sc_var3_answer_entry.grid(row=12, column=1, sticky=W)
            self.sc_var3_img_label_entry.grid(row=12, column=1, sticky=E, padx=0)
            self.sc_var3_points_entry.grid(row=12, column=2)
            self.sc_var3_select_img_btn.grid(row=12, column=1, sticky=E, padx=200)
            
        def sc_var4_show():
            self.sc_answer4_label.grid(row=13, column=0, sticky=W, padx=30)
            self.sc_var4_answer_entry.grid(row=13, column=1, sticky=W)
            self.sc_var4_img_label_entry.grid(row=13, column=1, sticky=E, padx=0)
            self.sc_var4_points_entry.grid(row=13, column=2)
            self.sc_var4_select_img_btn.grid(row=13, column=1, sticky=E, padx=200)

        def sc_var5_show():
            self.sc_answer5_label.grid(row=14, column=0, sticky=W, padx=30)
            self.sc_var5_answer_entry.grid(row=14, column=1, sticky=W)
            self.sc_var5_img_label_entry.grid(row=14, column=1, sticky=E, padx=0)
            self.sc_var5_points_entry.grid(row=14, column=2)
            self.sc_var5_select_img_btn.grid(row=14, column=1, sticky=E, padx=200)
            
            
        def sc_var6_show():
            self.sc_answer6_label.grid(row=15, column=0, sticky=W, padx=30)
            self.sc_var6_answer_entry.grid(row=15, column=1, sticky=W)
            self.sc_var6_img_label_entry.grid(row=15, column=1, sticky=E, padx=0)
            self.sc_var6_points_entry.grid(row=15, column=2)
            self.sc_var6_select_img_btn.grid(row=15, column=1, sticky=E, padx=200)
            
        def sc_var7_show():
            self.sc_answer7_label.grid(row=16, column=0, sticky=W, padx=30)
            self.sc_var7_answer_entry.grid(row=16, column=1, sticky=W)
            self.sc_var7_img_label_entry.grid(row=16, column=1, sticky=E, padx=0)
            self.sc_var7_points_entry.grid(row=16, column=2, sticky = W, padx = 20)
            self.sc_var7_select_img_btn.grid(row=16, column=1, sticky=E, padx=200)
            
        def sc_var2_remove():
            self.sc_answer2_label.grid_remove()
            self.sc_var2_answer_entry.grid_remove()
            self.sc_var2_img_label_entry.grid_remove()
            self.sc_var2_points_entry.grid_remove()
            self.sc_var2_select_img_btn.grid_remove()

        def sc_var3_remove():
            self.sc_answer3_label.grid_remove()
            self.sc_var3_answer_entry.grid_remove()
            self.sc_var3_img_label_entry.grid_remove()
            self.sc_var3_points_entry.grid_remove()
            self.sc_var3_select_img_btn.grid_remove()

        def sc_var4_remove():
            self.sc_answer4_label.grid_remove()
            self.sc_var4_answer_entry.grid_remove()
            self.sc_var4_img_label_entry.grid_remove()
            self.sc_var4_points_entry.grid_remove()
            self.sc_var4_select_img_btn.grid_remove()

        def sc_var5_remove():
            self.sc_answer5_label.grid_remove()
            self.sc_var5_answer_entry.grid_remove()
            self.sc_var5_img_label_entry.grid_remove()
            self.sc_var5_points_entry.grid_remove()
            self.sc_var5_select_img_btn.grid_remove()

        def sc_var6_remove():
            self.sc_answer6_label.grid_remove()
            self.sc_var6_answer_entry.grid_remove()
            self.sc_var6_img_label_entry.grid_remove()
            self.sc_var6_points_entry.grid_remove()
            self.sc_var6_select_img_btn.grid_remove()

        def sc_var7_remove():
            self.sc_answer7_label.grid_remove()
            self.sc_var7_answer_entry.grid_remove()
            self.sc_var7_img_label_entry.grid_remove()
            self.sc_var7_points_entry.grid_remove()
            self.sc_var7_select_img_btn.grid_remove()



    def sc_open_image(self, var_img_labe_entry):
        
        ### Dateipfad auswählen 
        
        app.filename = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
        self.sc_picture_name = app.filename
        self.sc_sorted_picture_name = self.sc_picture_name
        self.sc_last_char_index = self.sc_sorted_picture_name.rfind("/")
        self.sc_foo = ([pos for pos, char in enumerate(self.sc_sorted_picture_name) if char == '/'])
        self.sc_foo_len = len(self.sc_foo)
        self.sc_picture_name_new = self.sc_sorted_picture_name[self.sc_foo[self.sc_foo_len - 1] + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
        self.sc_image_format_new = self.sc_picture_name[-4:]    
        
        
        ### Bild-Namen entsprechendes Eingabefeld übertragen
        var_img_labe_entry.insert(0, str(self.sc_picture_name_new) + str(self.sc_image_format_new))
        
        
        ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
        # "encoded64_string_raw enthält die Daten als String in der Form b'String'
        # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
        # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen
        with open(self.sc_picture_name, "rb") as image_file:
            encoded64_string_raw = base64.b64encode(image_file.read())
            encoded64_string = encoded64_string_raw.decode('utf-8')
            
       
        print(self.sc_picture_name)
        
    def sc_submit(self):
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.sc_test_time = "P0Y0M0DT" + self.sc_proc_hours_box.get() + "H" + self.sc_proc_minutes_box.get() + "M" + self.sc_proc_seconds_box.get() + "S"


        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":response_1_text, :response_1_text, :response_1_text, response_1_text, response_1_img_string_base64_encoded,"
            ":response_2_text, :response_2_text, :response_2_text, response_2_text, response_2_img_string_base64_encoded,"
            ":response_3_text, :response_3_text, :response_3_text, response_3_text, response_3_img_string_base64_encoded,"
            ":response_4_text, :response_4_text, :response_4_text, response_4_text, response_4_img_string_base64_encoded,"
            ":response_5_text, :response_5_text, :response_5_text, response_5_text, response_5_img_string_base64_encoded,"
            ":response_6_text, :response_6_text, :response_6_text, response_6_text, response_6_img_string_base64_encoded,"
            ":response_7_text, :response_7_text, :response_7_text, response_7_text, response_7_img_string_base64_encoded,"
            ":response_8_text, :response_8_text, :response_8_text, response_8_text, response_8_img_string_base64_encoded,"
            ":response_9_text, :response_9_text, :response_9_text, response_9_text, response_9_img_string_base64_encoded,"
            ":response_10_text, :response_10_text, :response_10_text, response_10_text, response_10_img_string_base64_encoded,"
            ":img_name, :img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
            {
                'question_difficulty': self.mc_question_difficulty_entry.get(),
                'question_category': self.mc_question_category_entry.get(),
                'question_type': self.mc_question_type_entry.get(),

                'question_title': self.mc_question_title_entry.get(),
                'question_description_title': self.mc_question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.mc_infobox.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'var1_name': self.var1_answer_text.get(),
                'var1_min': self.var1_points_picked_text.get(),
                'var1_max': self.var1_points_not_picked_text.get(),

                'var2_name': self.var2_answer_text.get(),
                'var2_min': self.var2_points_picked_text.get(),
                'var2_max': self.var2_points_not_picked_text.get(),

                'var3_name': self.var3_answer_text.get(),
                'var3_min': self.var3_points_picked_text.get(),
                'var3_max': self.var3_points_not_picked_text.get(),

                'var4_name': self.var4_answer_text.get(),
                'var4_min': self.var4_points_picked_text.get(),
                'var4_max': self.var4_points_not_picked_text.get(),

                'var5_name': self.var5_answer_text.get(),
                'var5_min': self.var5_points_picked_text.get(),
                'var5_max': self.var5_points_not_picked_text.get(),

                'var6_name': self.var6_answer_text.get(),
                'var6_min': self.var6_points_picked_text.get(),
                'var6_max': self.var6_points_not_picked_text.get(),

                'var7_name': self.var7_answer_text.get(),
                'var7_min': self.var7_points_picked_text.get(),
                'var7_max': self.var7_points_not_picked_text.get(),

                'test_time': self.mc_test_time,


                'res1_formula': "",
                'res2_formula': "",
                'res3_formula': "",
                'res4_formula': "",
                'res5_formula': "",
                'res6_formula': "",
                'res7_formula': "",
                'res8_formula': "",
                'res9_formula': "",
                'res10_formula': "",
                'var1_prec': "",
                'var1_divby': "",
                'var1_unit': "",
                'var2_prec': "",
                'var2_divby': "",
                'var2_unit': "",
                'var3_prec': "",
                'var3_divby': "",
                'var3_unit': "",
                'var4_prec': "",
                'var4_divby': "",
                'var4_unit': "",
                'var5_prec': "",
                'var5_divby': "",
                'var5_unit': "",
                'var6_prec': "",
                'var6_divby': "",
                'var6_unit': "",
                'var7_prec': "",
                'var7_divby': "",
                'var7_unit': "",

                'res1_name': "",
                'res1_min': "",
                'res1_max': "",
                'res1_prec': "",
                'res1_tol': "",
                'res1_points': "",
                'res1_unit': "",

                'res2_name': "",
                'res2_min': "",
                'res2_max': "",
                'res2_prec': "",
                'res2_tol': "",
                'res2_points': "",
                'res2_unit': "",

                'res3_name': "",
                'res3_min': "",
                'res3_max': "",
                'res3_prec': "",
                'res3_tol': "",
                'res3_points': "",
                'res3_unit': "",

                'img_name': "",
                'img_data': "",

                'var_number': "",
                'res_number': "",
                'question_pool_tag': ""

            }
        )
        conn.commit()
        conn.close()
        print("mc question in databank")
"""



class MultipleChoice(Formelfrage):
    def __init__(self):
        # self.my_frame = Frame(master)
        # self.my_frame.grid()

        self.mc_frame = LabelFrame(self.multipleChoice_tab, text="Multiple Choice", padx=5, pady=5)
        self.mc_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.mc_question_title_label = Label(self.mc_frame, text="Titel")
        self.mc_question_title_label.grid(row=0, column=0, sticky=W, padx=10, pady=(10, 0))
        self.mc_question_title_entry = Entry(self.mc_frame, width=60)
        self.mc_question_title_entry.grid(row=0, column=1, pady=(10, 0), sticky=W)

        # mc_author_label = Label(mc_frame, text="Autor")
        # mc_author_label.grid(row=1, column=0, sticky=W, padx=10)
        # mc_author_entry = Entry(mc_frame, width=60)
        # mc_author_entry.grid(row=1, column=1, sticky=W)

        self.mc_question_description_label = Label(self.mc_frame, text="Beschreibung")
        self.mc_question_description_label.grid(row=2, column=0, sticky=W, padx=10)
        self.mc_question_description_entry = Entry(self.mc_frame, width=60)
        self.mc_question_description_entry.grid(row=2, column=1, sticky=W)

        self.mc_question_textfield_label = Label(self.mc_frame, text="Frage")
        self.mc_question_textfield_label.grid(row=3, column=0, sticky=W, padx=10)

        self.mc_bar = Scrollbar(self.mc_frame)
        self.mc_infobox = Text(self.mc_frame, height=6, width=65, font=('Helvetica', 9))
        self.mc_bar.grid(row=3, column=2, sticky=W)
        self.mc_infobox.grid(row=3, column=1, pady=10, sticky=W)
        self.mc_bar.config(command=self.mc_infobox.yview)
        self.mc_infobox.config(yscrollcommand=self.mc_bar.set)

        self.mc_processing_time_label = Label(self.mc_frame, text="Bearbeitungsdauer")
        self.mc_processing_time_label.grid(row=4, column=0, sticky=W, pady=(5, 0), padx=10)

        self.mc_processing_time_label = Label(self.mc_frame, text="Std:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, pady=(5, 0))
        self.mc_processing_time_label = Label(self.mc_frame, text="Min:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=70, pady=(5, 0))
        self.mc_processing_time_label = Label(self.mc_frame, text="Sek:")
        self.mc_processing_time_label.grid(row=4, column=1, sticky=W, padx=145, pady=(5, 0))

        ### Preview LaTeX
        #expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
        #preview(expr, viewer='file', filename='output.png')

        #file_image = ImageTk.PhotoImage(Image.open('output.png'))
        #file_image_label = Label(self.mc_frame, image=file_image)
        #file_image_label.image = file_image

        #def latex_preview():
        #    file_image_label.grid(row=20, column=1, pady=20)

        #self.myLatex_btn = Button(self.mc_frame, text="show LaTeX Preview", command=latex_preview)
        #self.myLatex_btn.grid(row=4, column=1, sticky=E)

        ###

        self.mc_processingtime_hours = list(range(24))
        self.mc_processingtime_minutes = list(range(60))
        self.mc_processingtime_seconds = list(range(60))

        self.mc_proc_hours_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_hours, width=2)
        self.mc_proc_minutes_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_minutes, width=2)
        self.mc_proc_seconds_box = ttk.Combobox(self.mc_frame, value=self.mc_processingtime_seconds, width=2)

        self.mc_proc_hours_box.current(0)
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
        self.mc_check_mix_questions = Checkbutton(self.mc_frame, text="", variable=self.mc_var_mix_questions, onvalue="1", offvalue="0")
        self.mc_check_mix_questions.deselect()
        self.mc_check_mix_questions.grid(row=5, column=1, sticky=W, pady=(5, 0))

        self.mc_answer_limitation_label = Label(self.mc_frame, text="Antwortbeschränkung")
        self.mc_answer_limitation_label.grid(row=6, column=0, sticky=W, padx=10, pady=(5, 0))
        self.mc_answer_limitation_entry = Entry(self.mc_frame, width=10)
        self.mc_answer_limitation_entry.grid(row=6, column=1, sticky=W, pady=(5, 0))

        self.answer_editor_box_label = Label(self.mc_frame, text="Antwort-Editor")
        self.answer_editor_box_label.grid(row=7, column=0, sticky=W, padx=10, pady=(5, 0))
        self.answer_editor_value = ("Einzeilige Antwort", "Mehrzeilige Antwort")
        self.answer_editor_box = ttk.Combobox(self.mc_frame, value=self.answer_editor_value, width=20)
        self.answer_editor_box.bind("<<ComboboxSelected>>")
        self.answer_editor_box.grid(row=7, column=1, sticky=W, pady=(5, 0))

        def mc_answer_selected(event):  # "event" is necessary here to react, although it is not used "officially"

            if self.numbers_of_answers_box.get() == '1':
                mc_var2_remove()
                mc_var3_remove()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '2':
                mc_var2_show()
                mc_var3_remove()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '3':
                mc_var2_show()
                mc_var3_show()
                mc_var4_remove()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '4':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_remove()
                mc_var6_remove()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '5':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_remove()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '6':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_remove()


            elif self.numbers_of_answers_box.get() == '7':
                mc_var2_show()
                mc_var3_show()
                mc_var4_show()
                mc_var5_show()
                mc_var6_show()
                mc_var7_show()

        self.numbers_of_answers_box_label = Label(self.mc_frame, text="Anzahl der Antworten")
        self.numbers_of_answers_box_label.grid(row=8, column=0, sticky=W, padx=10, pady=(5, 0))
        self.numbers_of_answers_value = ["1", "2", "3", "4", "5", "6", "7"]
        self.numbers_of_answers_box = ttk.Combobox(self.mc_frame, value=self.numbers_of_answers_value, width=20)
        self.numbers_of_answers_box.bind("<<ComboboxSelected>>", mc_answer_selected)
        self.numbers_of_answers_box.grid(row=8, column=1, sticky=W, pady=(5, 0))
        self.numbers_of_answers_box.current(0)

        # self.Label(self.mc_frame, text="Antworten").grid(row=9, column=0, sticky=W, padx=10, pady=(5, 0))
        # self.Label(self.mc_frame, text="Antwort-Text").grid(row=9, column=1, sticky=W, pady=(5, 0))
        self.points_picked_label = Label(self.mc_frame, text="Punkte:\nAusgewählt")
        self.points_picked_label.grid(row=8, column=1, sticky=E, padx=30)
        self.points_not_picked_label = Label(self.mc_frame, text="Punkte:\nNicht ausgewählt")
        self.points_not_picked_label.grid(row=8, column=2)

        # ------------------------------- VARIABLES RANGE: MINIMUM - TEXT & ENTRY --------------------------------------------
        self.var1_answer_text, self.var1_points_picked_text, self.var1_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var2_answer_text, self.var2_points_picked_text, self.var2_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var3_answer_text, self.var3_points_picked_text, self.var3_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var4_answer_text, self.var4_points_picked_text, self.var4_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var5_answer_text, self.var5_points_picked_text, self.var5_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var6_answer_text, self.var6_points_picked_text, self.var6_points_not_picked_text = StringVar(), StringVar(), StringVar()
        self.var7_answer_text, self.var7_points_picked_text, self.var7_points_not_picked_text = StringVar(), StringVar(), StringVar()

        self.var1_answer_entry = Entry(self.mc_frame, textvariable=self.var1_answer_text, width=40)
        self.var2_answer_entry = Entry(self.mc_frame, textvariable=self.var2_answer_text, width=40)
        self.var3_answer_entry = Entry(self.mc_frame, textvariable=self.var3_answer_text, width=40)
        self.var4_answer_entry = Entry(self.mc_frame, textvariable=self.var4_answer_text, width=40)
        self.var5_answer_entry = Entry(self.mc_frame, textvariable=self.var5_answer_text, width=40)
        self.var6_answer_entry = Entry(self.mc_frame, textvariable=self.var6_answer_text, width=40)
        self.var7_answer_entry = Entry(self.mc_frame, textvariable=self.var7_answer_text, width=40)

        # ------------------------------- VARIABLES RANGE:  MAXIMUM - TEXT & ENTRY --------------------------------------------

        self.var1_points_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_picked_text, width=8)
        self.var2_points_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_picked_text, width=8)
        self.var3_points_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_picked_text, width=8)
        self.var4_points_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_picked_text, width=8)
        self.var5_points_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_picked_text, width=8)
        self.var6_points_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_picked_text, width=8)
        self.var7_points_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_picked_text, width=8)

        # ------------------------------- VARIABLES PRECISION - TEXT & ENTRY --------------------------------------------

        self.var1_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var1_points_not_picked_text, width=8)
        self.var2_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var2_points_not_picked_text, width=8)
        self.var3_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var3_points_not_picked_text, width=8)
        self.var4_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var4_points_not_picked_text, width=8)
        self.var5_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var5_points_not_picked_text, width=8)
        self.var6_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var6_points_not_picked_text, width=8)
        self.var7_points_not_picked_entry = Entry(self.mc_frame, textvariable=self.var7_points_not_picked_text, width=8)

        self.answer1_label = Label(self.mc_frame, text="Antwort 1")
        self.answer2_label = Label(self.mc_frame, text="Antwort 2")
        self.answer3_label = Label(self.mc_frame, text="Antwort 3")
        self.answer4_label = Label(self.mc_frame, text="Antwort 4")
        self.answer5_label = Label(self.mc_frame, text="Antwort 5")
        self.answer6_label = Label(self.mc_frame, text="Antwort 6")
        self.answer7_label = Label(self.mc_frame, text="Antwort 7")

        self.answer1_label.grid(row=10, column=0, sticky=W, padx=30)
        self.var1_answer_entry.grid(row=10, column=1, sticky=W)
        self.var1_points_picked_entry.grid(row=10, column=1, sticky=E, padx=40)
        self.var1_points_not_picked_entry.grid(row=10, column=2)

        def mc_var2_show():
            self.answer2_label.grid(row=11, column=0, sticky=W, padx=30)
            self.var2_answer_entry.grid(row=11, column=1, sticky=W)
            self.var2_points_picked_entry.grid(row=11, column=1, sticky=E, padx=30)
            self.var2_points_not_picked_entry.grid(row=11, column=2)

        def mc_var3_show():
            self.answer3_label.grid(row=12, column=0, sticky=W, padx=30)
            self.var3_answer_entry.grid(row=12, column=1, sticky=W)
            self.var3_points_picked_entry.grid(row=12, column=1, sticky=E, padx=30)
            self.var3_points_not_picked_entry.grid(row=12, column=2)

        def mc_var4_show():
            self.answer4_label.grid(row=13, column=0, sticky=W, padx=30)
            self.var4_answer_entry.grid(row=13, column=1, sticky=W)
            self.var4_points_picked_entry.grid(row=13, column=1, sticky=E, padx=30)
            self.var4_points_not_picked_entry.grid(row=13, column=2)

        def mc_var5_show():
            self.answer5_label.grid(row=14, column=0, sticky=W, padx=30)
            self.var5_answer_entry.grid(row=14, column=1, sticky=W)
            self.var5_points_picked_entry.grid(row=14, column=1, sticky=E, padx=30)
            self.var5_points_not_picked_entry.grid(row=14, column=2)

        def mc_var6_show():
            self.answer6_label.grid(row=15, column=0, sticky=W, padx=30)
            self.var6_answer_entry.grid(row=15, column=1, sticky=W)
            self.var6_points_picked_entry.grid(row=15, column=1, sticky=E, padx=30)
            self.var6_points_not_picked_entry.grid(row=15, column=2)

        def mc_var7_show():
            self.answer7_label.grid(row=16, column=0, sticky=W, padx=30)
            self.var7_answer_entry.grid(row=16, column=1, sticky=W)
            self.var7_points_picked_entry.grid(row=16, column=1, sticky=E, padx=30)
            self.var7_points_not_picked_entry.grid(row=16, column=2)

        def mc_var2_remove():
            self.answer2_label.grid_remove()
            self.var2_answer_entry.grid_remove()
            self.var2_points_picked_entry.grid_remove()
            self.var2_points_not_picked_entry.grid_remove()

        def mc_var3_remove():
            self.answer3_label.grid_remove()
            self.var3_answer_entry.grid_remove()
            self.var3_points_picked_entry.grid_remove()
            self.var3_points_not_picked_entry.grid_remove()

        def mc_var4_remove():
            self.answer4_label.grid_remove()
            self.var4_answer_entry.grid_remove()
            self.var4_points_picked_entry.grid_remove()
            self.var4_points_not_picked_entry.grid_remove()

        def mc_var5_remove():
            self.answer5_label.grid_remove()
            self.var5_answer_entry.grid_remove()
            self.var5_points_picked_entry.grid_remove()
            self.var5_points_not_picked_entry.grid_remove()

        def mc_var6_remove():
            self.answer6_label.grid_remove()
            self.var6_answer_entry.grid_remove()
            self.var6_points_picked_entry.grid_remove()
            self.var6_points_not_picked_entry.grid_remove()

        def mc_var7_remove():
            self.answer7_label.grid_remove()
            self.var7_answer_entry.grid_remove()
            self.var7_points_picked_entry.grid_remove()
            self.var7_points_not_picked_entry.grid_remove()

    def submit_mc(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.mc_test_time = "P0Y0M0DT" + self.mc_proc_hours_box.get() + "H" + self.mc_proc_minutes_box.get() + "M" + self.mc_proc_seconds_box.get() + "S"

        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
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
            ":var7_name, :var7_min, :var7_max, :var7_prec, :var7_divby, :var7_unit,"
            ":res1_name, :res1_min, :res1_max, :res1_prec, :res1_tol, :res1_points, :res1_unit, "
            ":res2_name, :res2_min, :res2_max, :res2_prec, :res2_tol, :res2_points, :res2_unit, "
            ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit,"
            ":img_name, :img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
            {
                'question_difficulty': self.mc_question_difficulty_entry.get(),
                'question_category': self.mc_question_category_entry.get(),
                'question_type': self.mc_question_type_entry.get(),

                'question_title': self.mc_question_title_entry.get(),
                'question_description_title': self.mc_question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.mc_infobox.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'var1_name': self.var1_answer_text.get(),
                'var1_min': self.var1_points_picked_text.get(),
                'var1_max': self.var1_points_not_picked_text.get(),

                'var2_name': self.var2_answer_text.get(),
                'var2_min': self.var2_points_picked_text.get(),
                'var2_max': self.var2_points_not_picked_text.get(),

                'var3_name': self.var3_answer_text.get(),
                'var3_min': self.var3_points_picked_text.get(),
                'var3_max': self.var3_points_not_picked_text.get(),

                'var4_name': self.var4_answer_text.get(),
                'var4_min': self.var4_points_picked_text.get(),
                'var4_max': self.var4_points_not_picked_text.get(),

                'var5_name': self.var5_answer_text.get(),
                'var5_min': self.var5_points_picked_text.get(),
                'var5_max': self.var5_points_not_picked_text.get(),

                'var6_name': self.var6_answer_text.get(),
                'var6_min': self.var6_points_picked_text.get(),
                'var6_max': self.var6_points_not_picked_text.get(),

                'var7_name': self.var7_answer_text.get(),
                'var7_min': self.var7_points_picked_text.get(),
                'var7_max': self.var7_points_not_picked_text.get(),

                'test_time': self.mc_test_time,


                'res1_formula': "",
                'res2_formula': "",
                'res3_formula': "",
                'res4_formula': "",
                'res5_formula': "",
                'res6_formula': "",
                'res7_formula': "",
                'res8_formula': "",
                'res9_formula': "",
                'res10_formula': "",
                'var1_prec': "",
                'var1_divby': "",
                'var1_unit': "",
                'var2_prec': "",
                'var2_divby': "",
                'var2_unit': "",
                'var3_prec': "",
                'var3_divby': "",
                'var3_unit': "",
                'var4_prec': "",
                'var4_divby': "",
                'var4_unit': "",
                'var5_prec': "",
                'var5_divby': "",
                'var5_unit': "",
                'var6_prec': "",
                'var6_divby': "",
                'var6_unit': "",
                'var7_prec': "",
                'var7_divby': "",
                'var7_unit': "",

                'res1_name': "",
                'res1_min': "",
                'res1_max': "",
                'res1_prec': "",
                'res1_tol': "",
                'res1_points': "",
                'res1_unit': "",

                'res2_name': "",
                'res2_min': "",
                'res2_max': "",
                'res2_prec': "",
                'res2_tol': "",
                'res2_points': "",
                'res2_unit': "",

                'res3_name': "",
                'res3_min': "",
                'res3_max': "",
                'res3_prec': "",
                'res3_tol': "",
                'res3_points': "",
                'res3_unit': "",

                'img_name': "",
                'img_data': "",

                'var_number': "",
                'res_number': "",
                'question_pool_tag': ""

            }
        )
        conn.commit()
        conn.close()
        print("mc question in databank")


class create_multiplechoice(MultipleChoice):

    def __init__(self):
        #self.mytree = ET.parse(self.qti_file_path_read)
        #self.myroot = self.mytree.getroot()

        self.frame_mc_create = LabelFrame(self.formula_tab, text="Create Multiplechoice", padx=5, pady=5)
        self.frame_mc_create.grid(row=1, column=2)

        #create_multiplechoice.create_mc_question(self)


    def create_mc_question(self,mytree, myroot, qti_file_path_read, qti_file_path_write, entry_split, x):

        #self.mytree = ET.parse(qti_file_path_read)
        #self.myroot = self.mytree.getroot()

        self.mytree = mytree
        self.myroot = myroot

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        for record in records:
            if str(record[len(record) - 1]) == entry_split[x]:

                self.answer1 = str(record[9])
                self.answer1_points_picked = str(record[10])
                self.answer1_points_not_picked = str(record[11])

                self.answer2 = str(record[15])
                self.answer2_points_picked = str(record[16])
                self.answer2_points_not_picked = str(record[17])

                self.answer3 = str(record[21])
                self.answer3_points_picked = str(record[22])
                self.answer3_points_not_picked = str(record[23])

                self.answer4 = str(record[27])
                self.answer4_points_picked = str(record[28])
                self.answer4_points_not_picked = str(record[29])

                self.answer5 = str(record[33])
                self.answer5_points_picked = str(record[34])
                self.answer5_points_not_picked = str(record[35])

                self.answer6 = str(record[39])
                self.answer6_points_picked = str(record[40])
                self.answer6_points_not_picked = str(record[41])

                self.answer7 = str(record[45])
                self.answer7_points_picked = str(record[46])
                self.answer7_points_not_picked = str(record[47])

                self.mc_test_time = str(record[74])






                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
                item = ET.SubElement(section, 'item')
                item.set('ident', "il_0_qst_000001")
                item.set('title', "MC: 1. Frage")
                item.set('maxattempts', "0")
                qticomment = ET.SubElement(item, 'qticomment')
                # qticomment.text = self.mc_question_description_title
                duration = ET.SubElement(item, 'duration')
                duration.text = self.mc_test_time

                # append ITEM in the last "myroot"-Element. Here it is Element "section" in myroot
                self.myroot[0][len(self.myroot[0]) - 1].append(item)


                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                flow = ET.SubElement(presentation, 'flow')
                material = ET.SubElement(flow, 'material')
                response_lid = ET.SubElement(flow, 'response_lid')
                render_choice = ET.SubElement(response_lid, 'render_choice')
                response_label = ET.SubElement(render_choice, 'response_label')







                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                # -----------------------------------------------------------------------ILIAS VERSION
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "ILIAS_VERSION"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5.4.10 2020-03-04"
                # -----------------------------------------------------------------------QUESTION_TYPE
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
                fieldentry.text = "Tobias Panteleit"
                # -----------------------------------------------------------------------additional_cont_edit_mode
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "additional_cont_edit_mode"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "default"
                # -----------------------------------------------------------------------externalId
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "externalId"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "59a32416e65da6.54228908"
                # -----------------------------------------------------------------------thumb_size
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "thumb_size"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = ""
                # -----------------------------------------------------------------------feedback_setting
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "feedback_setting"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "1"
                # -----------------------------------------------------------------------singleline
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "singleline"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "1"

                presentation.set('label', "MC: 1. Frage")
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/html")
                mattext.text = "<p>" + "TEST - Was kommt in der Natur vor?" + "</p>"

                response_lid.set('ident', "MCMR")
                response_lid.set('rcardinality', "Multiple")

                render_choice.set('shuffle', "Yes")
                # -------------------------- Antwort 1
                response_label.set('ident', "0")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer1

                # -------------------------- Antwort 2
                response_label = ET.SubElement(render_choice, 'response_label')
                response_label.set('ident', "1")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer2

                # -------------------------- Antwort 3
                response_label = ET.SubElement(render_choice, 'response_label')
                response_label.set('ident', "2")
                material = ET.SubElement(response_label, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")
                mattext.text = self.answer3

                resprocessing = ET.SubElement(item, 'resprocessing')
                outcomes = ET.SubElement(resprocessing, 'outcomes')
                decvar = ET.SubElement(outcomes, 'decvar')

                # -------------------------- Zusatz für Antwort 1
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "0"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_0")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "0"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"

                # -------------------------- Zusatz für Antwort 2
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "1"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_1")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "1"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"

                # -------------------------- Zusatz für Antwort 3
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                varequal = ET.SubElement(conditionvar, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "2"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "1"
                displayfeedback = ET.SubElement(respcondition, 'displayfeedback')
                displayfeedback.set('feedbacktype', "Response")
                displayfeedback.set('linkrefid', "response_2")
                respcondition = ET.SubElement(resprocessing, 'respcondition')
                respcondition.set('continue', "Yes")
                conditionvar = ET.SubElement(respcondition, 'conditionvar')
                mc_not = ET.SubElement(conditionvar, 'mc_not')
                varequal = ET.SubElement(mc_not, 'varequal')
                varequal.set('respident', "MCMR")
                varequal.text = "2"
                setvar = ET.SubElement(respcondition, 'setvar')
                setvar.set('action', "Add")
                setvar.text = "0"


                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_0")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")

                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_1")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")

                itemfeedback = ET.SubElement(item, 'itemfeedback')
                itemfeedback.set('ident', "response_2")
                itemfeedback.set('view', "All")
                flow_mat = ET.SubElement(itemfeedback, 'flow_mat')
                material = ET.SubElement(flow_mat, 'material')
                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/plain")


                self.mytree.write(qti_file_path_write)
                print("MC Question created")

        conn.commit()
        conn.close()

        create_multiplechoice.mc_replace_characters(self, qti_file_path_write)



    def mc_replace_characters(self, qti_file_path_write):
        # with open("xml_form_edit\\" + 'NEW_1590230409__0__qti_1948621.xml') as xml_file:
        with open(qti_file_path_write, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('mc_not', 'not')  #replace "x" with "new value for x"

        with open(qti_file_path_write, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("\"mc_not\" replaced with \"not\"... done ")

class Database(Formelfrage):

    def __init__(self):

        self.database_window = Tk()
        self.database_window.title("Datenbank")

        # Create a ScrolledFrame widget
        #self.sf_database = ScrolledFrame(self.database_window, width=600, height=600)
        self.sf_database = ScrolledFrame(self.database_window, width=self.database_width, height=self.database_height)
        self.sf_database.pack(expand=1, fill="both")

        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.sf_database.bind_arrow_keys(app)
        #self.sf_database.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.db_inner_frame = self.sf_database.display_widget(Frame)



        # CREATE LISTBOXES ON GUI

        self.oid_listbox_label = Label(self.db_inner_frame, text=" DB\nID")
        self.oid_listbox_label.grid(row=25, column=1, sticky=W)


        #self.listbox_oid_entrys_label.grid(row=40, column=1, sticky=W)

        self.question_difficulty_listbox_label = Label(self.db_inner_frame, text="Question\nDifficulty")
        self.question_difficulty_listbox_label.grid(row=25, column=2, sticky=W)

        self.question_category_listbox_label = Label(self.db_inner_frame, text="Question\nCategory")
        self.question_category_listbox_label.grid(row=25, column=3, sticky=W)

        self.question_type_listbox_label = Label(self.db_inner_frame, text="Question\nType")
        self.question_type_listbox_label.grid(row=25, column=4, sticky=W)

        self.question_title_listbox_label = Label(self.db_inner_frame, text="Question\nTitle", width=15)
        self.question_title_listbox_label.grid(row=25, column=5, sticky=W)

        self.question_description_title_listbox_label = Label(self.db_inner_frame, text="Description\nTitle", width=15)
        self.question_description_title_listbox_label.grid(row=25, column=6, sticky=W)

        self.question_description_main_listbox_label = Label(self.db_inner_frame, text="Description\nMain", width=15)
        self.question_description_main_listbox_label.grid(row=25, column=7, sticky=W)

        self.res1_formula_listbox_label = Label(self.db_inner_frame, text="Formula 1", width=15)
        self.res1_formula_listbox_label.grid(row=25, column=8, sticky=W)

        self.res2_formula_listbox_label = Label(self.db_inner_frame, text="Formula 2", width=15)
        self.res2_formula_listbox_label.grid(row=25, column=9, sticky=W)

        self.res3_formula_listbox_label = Label(self.db_inner_frame, text="Formula 3", width=15)
        self.res3_formula_listbox_label.grid(row=25, column=10, sticky=W)

        self.var1_name_listbox_label = Label(self.db_inner_frame, text="var1\nname")
        self.var1_name_listbox_label.grid(row=25, column=11, sticky=W)
        self.var1_min_listbox_label = Label(self.db_inner_frame, text="var1\nmin")
        self.var1_min_listbox_label.grid(row=25, column=12, sticky=W)
        self.var1_max_listbox_label = Label(self.db_inner_frame, text="var1\nmax")
        self.var1_max_listbox_label.grid(row=25, column=13, sticky=W)
        self.var1_prec_listbox_label = Label(self.db_inner_frame, text="var1\nprec")
        self.var1_prec_listbox_label.grid(row=25, column=14, sticky=W)
        self.var1_divby_listbox_label = Label(self.db_inner_frame, text="var1\ndivby")
        self.var1_divby_listbox_label.grid(row=25, column=15, sticky=W)
        self.var1_unit_listbox_label = Label(self.db_inner_frame, text="var1\nunit")
        self.var1_unit_listbox_label.grid(row=25, column=16, sticky=W)

        self.var2_name_listbox_label = Label(self.db_inner_frame, text="var2\nname")
        self.var2_name_listbox_label.grid(row=25, column=17, sticky=W)
        self.var2_min_listbox_label = Label(self.db_inner_frame, text="var2\nmin")
        self.var2_min_listbox_label.grid(row=25, column=18, sticky=W)
        self.var2_max_listbox_label = Label(self.db_inner_frame, text="var2\nmax")
        self.var2_max_listbox_label.grid(row=25, column=19, sticky=W)
        self.var2_prec_listbox_label = Label(self.db_inner_frame, text="var2\nprec")
        self.var2_prec_listbox_label.grid(row=25, column=20, sticky=W)
        self.var2_divby_listbox_label = Label(self.db_inner_frame, text="var2\ndivby")
        self.var2_divby_listbox_label.grid(row=25, column=21, sticky=W)
        self.var2_unit_listbox_label = Label(self.db_inner_frame, text="var2\nunit")
        self.var2_unit_listbox_label.grid(row=25, column=22, sticky=W)

        self.var3_name_listbox_label = Label(self.db_inner_frame, text="var3\nname")
        self.var3_name_listbox_label.grid(row=25, column=23, sticky=W)
        self.var3_min_listbox_label = Label(self.db_inner_frame, text="var3\nmin")
        self.var3_min_listbox_label.grid(row=25, column=24, sticky=W)
        self.var3_max_listbox_label = Label(self.db_inner_frame, text="var3\nmax")
        self.var3_max_listbox_label.grid(row=25, column=25, sticky=W)
        self.var3_prec_listbox_label = Label(self.db_inner_frame, text="var3\nprec")
        self.var3_prec_listbox_label.grid(row=25, column=26, sticky=W)
        self.var3_divby_listbox_label = Label(self.db_inner_frame, text="var3\ntol")
        self.var3_divby_listbox_label.grid(row=25, column=27, sticky=W)
        self.var3_unit_listbox_label = Label(self.db_inner_frame, text="var3\nunit")
        self.var3_unit_listbox_label.grid(row=25, column=28, sticky=W)

        self.var4_name_listbox_label = Label(self.db_inner_frame, text="var4\nname")
        self.var4_name_listbox_label.grid(row=25, column=29, sticky=W)
        self.var4_min_listbox_label = Label(self.db_inner_frame, text="var4\nmin")
        self.var4_min_listbox_label.grid(row=25, column=30, sticky=W)
        self.var4_max_listbox_label = Label(self.db_inner_frame, text="var4\nmax")
        self.var4_max_listbox_label.grid(row=25, column=31, sticky=W)
        self.var4_prec_listbox_label = Label(self.db_inner_frame, text="var4\nprec")
        self.var4_prec_listbox_label.grid(row=25, column=32, sticky=W)
        self.var4_divby_listbox_label = Label(self.db_inner_frame, text="var4\ntol")
        self.var4_divby_listbox_label.grid(row=25, column=33, sticky=W)
        self.var4_unit_listbox_label = Label(self.db_inner_frame, text="var4\nunit")
        self.var4_unit_listbox_label.grid(row=25, column=34, sticky=W)

        self.var5_name_listbox_label = Label(self.db_inner_frame, text="var5\nname")
        self.var5_name_listbox_label.grid(row=25, column=35, sticky=W)
        self.var5_min_listbox_label = Label(self.db_inner_frame, text="var5\nmin")
        self.var5_min_listbox_label.grid(row=25, column=36, sticky=W)
        self.var5_max_listbox_label = Label(self.db_inner_frame, text="var5\nmax")
        self.var5_max_listbox_label.grid(row=25, column=37, sticky=W)
        self.var5_prec_listbox_label = Label(self.db_inner_frame, text="var5\nprec")
        self.var5_prec_listbox_label.grid(row=25, column=38, sticky=W)
        self.var5_divby_listbox_label = Label(self.db_inner_frame, text="var5\ntol")
        self.var5_divby_listbox_label.grid(row=25, column=39, sticky=W)
        self.var5_unit_listbox_label = Label(self.db_inner_frame, text="var5\nunit")
        self.var5_unit_listbox_label.grid(row=25, column=40, sticky=W)

        self.var6_name_listbox_label = Label(self.db_inner_frame, text="var6\nname")
        self.var6_name_listbox_label.grid(row=25, column=41, sticky=W)
        self.var6_min_listbox_label = Label(self.db_inner_frame, text="var6\nmin")
        self.var6_min_listbox_label.grid(row=25, column=42, sticky=W)
        self.var6_max_listbox_label = Label(self.db_inner_frame, text="var6\nmax")
        self.var6_max_listbox_label.grid(row=25, column=43, sticky=W)
        self.var6_prec_listbox_label = Label(self.db_inner_frame, text="var6\nprec")
        self.var6_prec_listbox_label.grid(row=25, column=44, sticky=W)
        self.var6_divby_listbox_label = Label(self.db_inner_frame, text="var6\ntol")
        self.var6_divby_listbox_label.grid(row=25, column=45, sticky=W)
        self.var6_unit_listbox_label = Label(self.db_inner_frame, text="var6\nunit")
        self.var6_unit_listbox_label.grid(row=25, column=46, sticky=W)

        self.var7_name_listbox_label = Label(self.db_inner_frame, text="var1\nname")
        self.var7_name_listbox_label.grid(row=25, column=47, sticky=W)
        self.var7_min_listbox_label = Label(self.db_inner_frame, text="var7\nmin")
        self.var7_min_listbox_label.grid(row=25, column=48, sticky=W)
        self.var7_max_listbox_label = Label(self.db_inner_frame, text="var7\nmax")
        self.var7_max_listbox_label.grid(row=25, column=49, sticky=W)
        self.var7_prec_listbox_label = Label(self.db_inner_frame, text="var7\nprec")
        self.var7_prec_listbox_label.grid(row=25, column=50, sticky=W)
        self.var7_divby_listbox_label = Label(self.db_inner_frame, text="var7\ntol")
        self.var7_divby_listbox_label.grid(row=25, column=51, sticky=W)
        self.var7_unit_listbox_label = Label(self.db_inner_frame, text="var7\nunit")
        self.var7_unit_listbox_label.grid(row=25, column=52, sticky=W)

        self.res1_name_listbox_label = Label(self.db_inner_frame, text="res1\nname")
        self.res1_name_listbox_label.grid(row=25, column=53, sticky=W)
        self.res1_min_listbox_label = Label(self.db_inner_frame, text="res1\nmin")
        self.res1_min_listbox_label.grid(row=25, column=54, sticky=W)
        self.res1_max_listbox_label = Label(self.db_inner_frame, text="res1\nmax")
        self.res1_max_listbox_label.grid(row=25, column=55, sticky=W)
        self.res1_prec_listbox_label = Label(self.db_inner_frame, text="res1\nprec")
        self.res1_prec_listbox_label.grid(row=25, column=56, sticky=W)
        self.res1_tol_listbox_label = Label(self.db_inner_frame, text="res1\ntol")
        self.res1_tol_listbox_label.grid(row=25, column=57, sticky=W)
        self.res1_points_listbox_label = Label(self.db_inner_frame, text="res1\npts")
        self.res1_points_listbox_label.grid(row=25, column=58, sticky=W)
        self.res1_unit_listbox_label = Label(self.db_inner_frame, text="res1\nunit")
        self.res1_unit_listbox_label.grid(row=25, column=59, sticky=W)

        self.res2_name_listbox_label = Label(self.db_inner_frame, text="res2\nname")
        self.res2_name_listbox_label.grid(row=25, column=60, sticky=W)
        self.res2_min_listbox_label = Label(self.db_inner_frame, text="res2\nmin")
        self.res2_min_listbox_label.grid(row=25, column=61, sticky=W)
        self.res2_max_listbox_label = Label(self.db_inner_frame, text="res2\nmax")
        self.res2_max_listbox_label.grid(row=25, column=62, sticky=W)
        self.res2_prec_listbox_label = Label(self.db_inner_frame, text="res2\nprec")
        self.res2_prec_listbox_label.grid(row=25, column=63, sticky=W)
        self.res2_tol_listbox_label = Label(self.db_inner_frame, text="res2\ntol")
        self.res2_tol_listbox_label.grid(row=25, column=64, sticky=W)
        self.res2_points_listbox_label = Label(self.db_inner_frame, text="res2\npts")
        self.res2_points_listbox_label.grid(row=25, column=65, sticky=W)
        self.res2_unit_listbox_label = Label(self.db_inner_frame, text="res2\nunit")
        self.res2_unit_listbox_label.grid(row=25, column=66, sticky=W)

        self.res3_name_listbox_label = Label(self.db_inner_frame, text="res3\nname")
        self.res3_name_listbox_label.grid(row=25, column=67, sticky=W)
        self.res3_min_listbox_label = Label(self.db_inner_frame, text="res3\nmin")
        self.res3_min_listbox_label.grid(row=25, column=68, sticky=W)
        self.res3_max_listbox_label = Label(self.db_inner_frame, text="res3\nmax")
        self.res3_max_listbox_label.grid(row=25, column=69, sticky=W)
        self.res3_prec_listbox_label = Label(self.db_inner_frame, text="res3\nprec")
        self.res3_prec_listbox_label.grid(row=25, column=70, sticky=W)
        self.res3_tol_listbox_label = Label(self.db_inner_frame, text="res3\ntol")
        self.res3_tol_listbox_label.grid(row=25, column=71, sticky=W)
        self.res3_points_listbox_label = Label(self.db_inner_frame, text="res3\npts")
        self.res3_points_listbox_label.grid(row=25, column=72, sticky=W)
        self.res3_unit_listbox_label = Label(self.db_inner_frame, text="res3\nunit")
        self.res3_unit_listbox_label.grid(row=25, column=73, sticky=W)


        self.img_name_listbox_label = Label(self.db_inner_frame, text=" img\n name")
        self.img_name_listbox_label.grid(row=25, column=74, sticky=W)

        self.img_data_label = Label(self.db_inner_frame, text=" img\n data")
        #self.img_data_label.grid(row=25, column=55, sticky=W)


        self.test_time_listbox_label = Label(self.db_inner_frame, text="test\ntime", width=10)
        self.test_time_listbox_label.grid(row=25, column=75, sticky=W)



        # CREATE FULL-LISTBOX ENTRYS IN NEW WINDOW

        self.my_listbox_oid = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_oid.grid(row=30, column=1, sticky=W)

        self.my_listbox_question_difficulty = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_difficulty.grid(row=30, column=2, sticky=W)

        self.my_listbox_question_category = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_category.grid(row=30, column=3, sticky=W)

        self.my_listbox_question_type = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_type.grid(row=30, column=4, sticky=W)

        self.my_listbox_question_title = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_title.grid(row=30, column=5, sticky=W, pady=20)
        self.my_listbox_question_description_title = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_description_title.grid(row=30, column=6, sticky=W)
        self.my_listbox_question_description_main = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_question_description_main.grid(row=30, column=7, sticky=W)

        self.my_listbox_res1_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res1_formula.grid(row=30, column=8, sticky=W)
        self.my_listbox_res2_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res2_formula.grid(row=30, column=9, sticky=W)
        self.my_listbox_res3_formula = Listbox(self.db_inner_frame, width=15, height=30)
        self.my_listbox_res3_formula.grid(row=30, column=10, sticky=W)

        self.my_listbox_var1_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_name.grid(row=30, column=11, sticky=W)
        self.my_listbox_var1_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_min.grid(row=30, column=12, sticky=W)
        self.my_listbox_var1_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_max.grid(row=30, column=13, sticky=W)
        self.my_listbox_var1_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_prec.grid(row=30, column=14, sticky=W)
        self.my_listbox_var1_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_divby.grid(row=30, column=15, sticky=W)
        self.my_listbox_var1_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var1_unit.grid(row=30, column=16, sticky=W)

        self.my_listbox_var2_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_name.grid(row=30, column=17, sticky=W)
        self.my_listbox_var2_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_min.grid(row=30, column=18, sticky=W)
        self.my_listbox_var2_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_max.grid(row=30, column=19, sticky=W)
        self.my_listbox_var2_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_prec.grid(row=30, column=20, sticky=W)
        self.my_listbox_var2_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_divby.grid(row=30, column=21, sticky=W)
        self.my_listbox_var2_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var2_unit.grid(row=30, column=22, sticky=W)

        self.my_listbox_var3_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_name.grid(row=30, column=23, sticky=W)
        self.my_listbox_var3_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_min.grid(row=30, column=24, sticky=W)
        self.my_listbox_var3_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_max.grid(row=30, column=25, sticky=W)
        self.my_listbox_var3_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_prec.grid(row=30, column=26, sticky=W)
        self.my_listbox_var3_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_divby.grid(row=30, column=27, sticky=W)
        self.my_listbox_var3_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var3_unit.grid(row=30, column=28, sticky=W)

        self.my_listbox_var4_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_name.grid(row=30, column=29, sticky=W)
        self.my_listbox_var4_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_min.grid(row=30, column=30, sticky=W)
        self.my_listbox_var4_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_max.grid(row=30, column=31, sticky=W)
        self.my_listbox_var4_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_prec.grid(row=30, column=32, sticky=W)
        self.my_listbox_var4_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_divby.grid(row=30, column=33, sticky=W)
        self.my_listbox_var4_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var4_unit.grid(row=30, column=34, sticky=W)

        self.my_listbox_var5_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_name.grid(row=30, column=35, sticky=W)
        self.my_listbox_var5_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_min.grid(row=30, column=36, sticky=W)
        self.my_listbox_var5_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_max.grid(row=30, column=37, sticky=W)
        self.my_listbox_var5_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_prec.grid(row=30, column=38, sticky=W)
        self.my_listbox_var5_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_divby.grid(row=30, column=39, sticky=W)
        self.my_listbox_var5_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var5_unit.grid(row=30, column=40, sticky=W)

        self.my_listbox_var6_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_name.grid(row=30, column=41, sticky=W)
        self.my_listbox_var6_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_min.grid(row=30, column=42, sticky=W)
        self.my_listbox_var6_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_max.grid(row=30, column=43, sticky=W)
        self.my_listbox_var6_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_prec.grid(row=30, column=44, sticky=W)
        self.my_listbox_var6_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_divby.grid(row=30, column=45, sticky=W)
        self.my_listbox_var6_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var6_unit.grid(row=30, column=46, sticky=W)

        self.my_listbox_var7_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_name.grid(row=30, column=47, sticky=W)
        self.my_listbox_var7_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_min.grid(row=30, column=48, sticky=W)
        self.my_listbox_var7_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_max.grid(row=30, column=49, sticky=W)
        self.my_listbox_var7_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_prec.grid(row=30, column=50, sticky=W)
        self.my_listbox_var7_divby = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_divby.grid(row=30, column=51, sticky=W)
        self.my_listbox_var7_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_var7_unit.grid(row=30, column=52, sticky=W)

        self.my_listbox_res1_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_name.grid(row=30, column=53, sticky=W)
        self.my_listbox_res1_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_min.grid(row=30, column=54, sticky=W)
        self.my_listbox_res1_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_max.grid(row=30, column=55, sticky=W)
        self.my_listbox_res1_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_prec.grid(row=30, column=56, sticky=W)
        self.my_listbox_res1_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_tol.grid(row=30, column=57, sticky=W)
        self.my_listbox_res1_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_points.grid(row=30, column=58, sticky=W)
        self.my_listbox_res1_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res1_unit.grid(row=30, column=59, sticky=W)

        self.my_listbox_res2_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_name.grid(row=30, column=60, sticky=W)
        self.my_listbox_res2_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_min.grid(row=30, column=61, sticky=W)
        self.my_listbox_res2_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_max.grid(row=30, column=62, sticky=W)
        self.my_listbox_res2_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_prec.grid(row=30, column=63, sticky=W)
        self.my_listbox_res2_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_tol.grid(row=30, column=64, sticky=W)
        self.my_listbox_res2_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_points.grid(row=30, column=65, sticky=W)
        self.my_listbox_res2_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res2_unit.grid(row=30, column=66, sticky=W)

        self.my_listbox_res3_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_name.grid(row=30, column=67, sticky=W)
        self.my_listbox_res3_min = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_min.grid(row=30, column=68, sticky=W)
        self.my_listbox_res3_max = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_max.grid(row=30, column=69, sticky=W)
        self.my_listbox_res3_prec = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_prec.grid(row=30, column=70, sticky=W)
        self.my_listbox_res3_tol = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_tol.grid(row=30, column=71, sticky=W)
        self.my_listbox_res3_points = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_points.grid(row=30, column=72, sticky=W)
        self.my_listbox_res3_unit = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_res3_unit.grid(row=30, column=73, sticky=W)

        self.my_listbox_img_name = Listbox(self.db_inner_frame, width=5, height=30)
        self.my_listbox_img_name.grid(row=30, column=74, sticky=W)

        self.my_listbox_img_data = Listbox(self.db_inner_frame, width=10, height=30)
        # self.my_listbox_img_data.grid(row=30, column=50, sticky=W)          #IMG_data need to get a database_entry, but would not "grid()" the entry to GUI. Otherwise it is real slow

        self.my_listbox_test_time = Listbox(self.db_inner_frame, width=20, height=30)
        self.my_listbox_test_time.grid(row=30, column=75, sticky=W)

        # CREATE LISTBOX SCROLLBARS

        def yview (*args):

            self.my_listbox_question_difficulty.yview(*args)
            self.my_listbox_question_category.yview(*args)
            self.my_listbox_question_type.yview(*args)
            self.my_listbox_question_title.yview(*args)
            self.my_listbox_question_description_title.yview(*args)
            self.my_listbox_question_description_main.yview(*args)

            self.my_listbox_res1_formula.yview(*args)
            self.my_listbox_res2_formula.yview(*args)
            self.my_listbox_res3_formula.yview(*args)

            self.my_listbox_var1_name.yview(*args)
            self.my_listbox_var1_min.yview(*args)
            self.my_listbox_var1_max.yview(*args)
            self.my_listbox_var1_prec.yview(*args)
            self.my_listbox_var1_divby.yview(*args)
            self.my_listbox_var1_unit.yview(*args)

            self.my_listbox_var2_name.yview(*args)
            self.my_listbox_var2_min.yview(*args)
            self.my_listbox_var2_max.yview(*args)
            self.my_listbox_var2_prec.yview(*args)
            self.my_listbox_var2_divby.yview(*args)
            self.my_listbox_var2_unit.yview(*args)

            self.my_listbox_var3_name.yview(*args)
            self.my_listbox_var3_min.yview(*args)
            self.my_listbox_var3_max.yview(*args)
            self.my_listbox_var3_prec.yview(*args)
            self.my_listbox_var3_divby.yview(*args)
            self.my_listbox_var3_unit.yview(*args)

            self.my_listbox_var4_name.yview(*args)
            self.my_listbox_var4_min.yview(*args)
            self.my_listbox_var4_max.yview(*args)
            self.my_listbox_var4_prec.yview(*args)
            self.my_listbox_var4_divby.yview(*args)
            self.my_listbox_var4_unit.yview(*args)

            self.my_listbox_var5_name.yview(*args)
            self.my_listbox_var5_min.yview(*args)
            self.my_listbox_var5_max.yview(*args)
            self.my_listbox_var5_prec.yview(*args)
            self.my_listbox_var5_divby.yview(*args)
            self.my_listbox_var5_unit.yview(*args)

            self.my_listbox_var6_name.yview(*args)
            self.my_listbox_var6_min.yview(*args)
            self.my_listbox_var6_max.yview(*args)
            self.my_listbox_var6_prec.yview(*args)
            self.my_listbox_var6_divby.yview(*args)
            self.my_listbox_var6_unit.yview(*args)

            self.my_listbox_var7_name.yview(*args)
            self.my_listbox_var7_min.yview(*args)
            self.my_listbox_var7_max.yview(*args)
            self.my_listbox_var7_prec.yview(*args)
            self.my_listbox_var7_divby.yview(*args)
            self.my_listbox_var7_unit.yview(*args)

            self.my_listbox_res1_name.yview(*args)
            self.my_listbox_res1_min.yview(*args)
            self.my_listbox_res1_max.yview(*args)
            self.my_listbox_res1_prec.yview(*args)
            self.my_listbox_res1_tol.yview(*args)
            self.my_listbox_res1_points.yview(*args)
            self.my_listbox_res1_unit.yview(*args)

            self.my_listbox_res2_name.yview(*args)
            self.my_listbox_res2_min.yview(*args)
            self.my_listbox_res2_max.yview(*args)
            self.my_listbox_res2_prec.yview(*args)
            self.my_listbox_res2_tol.yview(*args)
            self.my_listbox_res2_points.yview(*args)
            self.my_listbox_res2_unit.yview(*args)

            self.my_listbox_res3_name.yview(*args)
            self.my_listbox_res3_min.yview(*args)
            self.my_listbox_res3_max.yview(*args)
            self.my_listbox_res3_prec.yview(*args)
            self.my_listbox_res3_tol.yview(*args)
            self.my_listbox_res3_points.yview(*args)
            self.my_listbox_res3_unit.yview(*args)

            self.my_listbox_img_name.yview(*args)
            #self.my_listbox_img_data.yview(*args)
            self.my_listbox_test_time.yview(*args)

            self.my_listbox_oid.yview(*args)

        self.listbox_entry_scrollbar_y = Scrollbar(self.db_inner_frame, command=yview)
        self.listbox_entry_scrollbar_y.grid(row=1, column=0)

        self.my_listbox_question_difficulty.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_category.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_type.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_title.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_description_title.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_question_description_main.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res1_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_formula.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var1_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var1_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var2_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var3_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var4_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var4_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var5_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var5_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var6_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var6_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_var7_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_divby.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_var7_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res1_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res1_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res2_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res2_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_res3_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_min.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_max.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_prec.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_tol.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_points.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_res3_unit.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.my_listbox_img_name.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        #self.my_listbox_img_data.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_test_time.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)
        self.my_listbox_oid.config(yscrollcommand=self.listbox_entry_scrollbar_y.set)

        self.searchbox_question_difficulty = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_difficulty.grid(row=1, column=2, sticky=E)
        self.tooltip.bind(self.searchbox_question_difficulty, "Nach \"Schwierigkeit\" filtern")

        self.searchbox_question_category = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_category.grid(row=1, column=3, sticky=E)
        self.tooltip.bind(self.searchbox_question_category, "Nach \"Kategorie\" filtern")

        self.searchbox_question_type = Entry(self.db_inner_frame, width=13)
        self.searchbox_question_type.grid(row=1, column=4, sticky=E)
        self.tooltip.bind(self.searchbox_question_type, "Nach \"Typ\" filtern")

        self.filter_btn = Button(self.db_inner_frame, text="Filtern", command=lambda: Database.filter_database(self))
        self.filter_btn.grid(row=2, column=4, sticky=E, ipadx = 23)

        Database.show_records(self)


    def remove_database(self):
        self.frame_database.grid_forget()

    def new_question(self):

        self.question_difficulty_entry.delete(0, END)
        self.question_category_entry.delete(0, END)
        self.question_type_entry.delete(0, END)

        self.question_title_entry.delete(0, END)
        self.question_description_entry.delete(0, END)
        self.formula_question_entry.delete('1.0', 'end-1c')

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

        self.proc_hours_box.current(23)
        self.proc_minutes_box.current(0)
        self.proc_seconds_box.current(0)

        self.var1_unit_myCombo.current(0)
        self.var2_unit_myCombo.current(0)
        self.var3_unit_myCombo.current(0)
        self.var4_unit_myCombo.current(0)
        self.var5_unit_myCombo.current(0)
        self.var6_unit_myCombo.current(0)
        self.var7_unit_myCombo.current(0)

        self.res1_unit_myCombo.current(0)
        self.res2_unit_myCombo.current(0)
        self.res3_unit_myCombo.current(0)

        self.myCombo.current(0)
        self.myCombo_res.current(0)

        Formelfrage.selected_var_from_db(self, self.myCombo.get())
        Formelfrage.selected_res_from_db(self, self.myCombo_res.get())

    def submit(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c =conn.cursor()



        # format of duration P0Y0M0DT0H30M0S
        self.test_time = "P0Y0M0DT" + self.proc_hours_box.get() + "H" + self.proc_minutes_box.get() + "M" + self.proc_seconds_box.get() + "S"

        #Dieser String muss modifiziert werden. In der xml ist ein Zeilenumbrauch als "&lt;/p&gt;&#13;&#10;&lt;p&gt;" definiert und nur 1 Zeile!

        #print(self.picture_name)

        if self.picture_name != "EMPTY":
            # read image data in byte format
            with open(self.picture_name, 'rb') as image_file:
                self.picture_data = image_file.read()


        else:
            self.picture_name_new = "EMPTY"
            self.picture_data = "EMPTY"


        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
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
            ":img_name, :img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
            {
                'question_difficulty': self.question_difficulty_entry.get(),
                'question_category': self.question_category_entry.get(),
                'question_type': self.question_type_entry.get(),

                'question_title': self.question_title_entry.get(),
                'question_description_title': self.question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.formula_question_entry.get("1.0", 'end-1c'),

                'res1_formula': self.res1_formula_text.get(),
                'res2_formula': self.res2_formula_text.get(),
                'res3_formula': self.res3_formula_text.get(),
                'res4_formula': self.res4_formula_text.get(),
                'res5_formula': self.res5_formula_text.get(),
                'res6_formula': self.res6_formula_text.get(),
                'res7_formula': self.res7_formula_text.get(),
                'res8_formula': self.res8_formula_text.get(),
                'res9_formula': self.res9_formula_text.get(),
                'res10_formula': self.res10_formula_text.get(),

                'var1_name': self.var1_name_text.get(),
                'var1_min': self.var1_min_text.get(),
                'var1_max': self.var1_max_text.get(),
                'var1_prec': self.var1_prec_text.get(),
                'var1_divby': self.var1_divby_text.get(),
                'var1_unit': self.var1_unit_myCombo.get(),

                'var2_name': self.var2_name_text.get(),
                'var2_min': self.var2_min_text.get(),
                'var2_max': self.var2_max_text.get(),
                'var2_prec': self.var2_prec_text.get(),
                'var2_divby': self.var2_divby_text.get(),
                'var2_unit': self.var2_unit_myCombo.get(),

                'var3_name': self.var3_name_text.get(),
                'var3_min': self.var3_min_text.get(),
                'var3_max': self.var3_max_text.get(),
                'var3_prec': self.var3_prec_text.get(),
                'var3_divby': self.var3_divby_text.get(),
                'var3_unit': self.var3_unit_myCombo.get(),

                'var4_name': self.var4_name_text.get(),
                'var4_min': self.var4_min_text.get(),
                'var4_max': self.var4_max_text.get(),
                'var4_prec': self.var4_prec_text.get(),
                'var4_divby': self.var4_divby_text.get(),
                'var4_unit': self.var4_unit_myCombo.get(),

                'var5_name': self.var5_name_text.get(),
                'var5_min': self.var5_min_text.get(),
                'var5_max': self.var5_max_text.get(),
                'var5_prec': self.var5_prec_text.get(),
                'var5_divby': self.var5_divby_text.get(),
                'var5_unit': self.var5_unit_myCombo.get(),

                'var6_name': self.var6_name_text.get(),
                'var6_min': self.var6_min_text.get(),
                'var6_max': self.var6_max_text.get(),
                'var6_prec': self.var6_prec_text.get(),
                'var6_divby': self.var6_divby_text.get(),
                'var6_unit': self.var6_unit_myCombo.get(),

                'var7_name': self.var7_name_text.get(),
                'var7_min': self.var7_min_text.get(),
                'var7_max': self.var7_max_text.get(),
                'var7_prec': self.var7_prec_text.get(),
                'var7_divby': self.var7_divby_text.get(),
                'var7_unit': self.var7_unit_myCombo.get(),

                'var8_name': self.var8_name_text.get(),
                'var8_min': self.var8_min_text.get(),
                'var8_max': self.var8_max_text.get(),
                'var8_prec': self.var8_prec_text.get(),
                'var8_divby': self.var8_divby_text.get(),
                'var8_unit': "Unit",

                'var9_name': self.var9_name_text.get(),
                'var9_min': self.var9_min_text.get(),
                'var9_max': self.var9_max_text.get(),
                'var9_prec': self.var9_prec_text.get(),
                'var9_divby': self.var9_divby_text.get(),
                'var9_unit': "Unit",

                'var10_name': self.var10_name_text.get(),
                'var10_min': self.var10_min_text.get(),
                'var10_max': self.var10_max_text.get(),
                'var10_prec': self.var10_prec_text.get(),
                'var10_divby': self.var10_divby_text.get(),
                'var10_unit': "Unit",


                'res1_name': self.res1_name_text.get(),
                'res1_min': self.res1_min_text.get(),
                'res1_max': self.res1_max_text.get(),
                'res1_prec': self.res1_prec_text.get(),
                'res1_tol': self.res1_tol_text.get(),
                'res1_points': self.res1_points_text.get(),
                'res1_unit': self.res1_unit_myCombo.get(),

                'res2_name': self.res2_name_text.get(),
                'res2_min': self.res2_min_text.get(),
                'res2_max': self.res2_max_text.get(),
                'res2_prec': self.res2_prec_text.get(),
                'res2_tol': self.res2_tol_text.get(),
                'res2_points': self.res2_points_text.get(),
                'res2_unit': self.res2_unit_myCombo.get(),

                'res3_name': self.res3_name_text.get(),
                'res3_min': self.res3_min_text.get(),
                'res3_max': self.res3_max_text.get(),
                'res3_prec': self.res3_prec_text.get(),
                'res3_tol': self.res3_tol_text.get(),
                'res3_points': self.res3_points_text.get(),
                'res3_unit': self.res3_unit_myCombo.get(),

                'res4_name': self.res4_name_text.get(),
                'res4_min': self.res4_min_text.get(),
                'res4_max': self.res4_max_text.get(),
                'res4_prec': self.res4_prec_text.get(),
                'res4_tol': self.res4_tol_text.get(),
                'res4_points': self.res4_points_text.get(),
                'res4_unit': "Unit",

                'res5_name': self.res5_name_text.get(),
                'res5_min': self.res5_min_text.get(),
                'res5_max': self.res5_max_text.get(),
                'res5_prec': self.res5_prec_text.get(),
                'res5_tol': self.res5_tol_text.get(),
                'res5_points': self.res5_points_text.get(),
                'res5_unit': "Unit",

                'res6_name': self.res6_name_text.get(),
                'res6_min': self.res6_min_text.get(),
                'res6_max': self.res6_max_text.get(),
                'res6_prec': self.res6_prec_text.get(),
                'res6_tol': self.res6_tol_text.get(),
                'res6_points': self.res6_points_text.get(),
                'res6_unit': "Unit",
                'res7_name': self.res7_name_text.get(),
                'res7_min': self.res7_min_text.get(),
                'res7_max': self.res7_max_text.get(),
                'res7_prec': self.res7_prec_text.get(),
                'res7_tol': self.res7_tol_text.get(),
                'res7_points': self.res7_points_text.get(),
                'res7_unit': "Unit",

                'res8_name': self.res8_name_text.get(),
                'res8_min': self.res8_min_text.get(),
                'res8_max': self.res8_max_text.get(),
                'res8_prec': self.res8_prec_text.get(),
                'res8_tol': self.res8_tol_text.get(),
                'res8_points': self.res8_points_text.get(),
                'res8_unit': "Unit",

                'res9_name': self.res9_name_text.get(),
                'res9_min': self.res9_min_text.get(),
                'res9_max': self.res9_max_text.get(),
                'res9_prec': self.res9_prec_text.get(),
                'res9_tol': self.res9_tol_text.get(),
                'res9_points': self.res9_points_text.get(),
                'res9_unit': "Unit",

                'res10_name': self.res10_name_text.get(),
                'res10_min': self.res10_min_text.get(),
                'res10_max': self.res10_max_text.get(),
                'res10_prec': self.res10_prec_text.get(),
                'res10_tol': self.res10_tol_text.get(),
                'res10_points': self.res10_points_text.get(),
                'res10_unit': "Unit",

                'img_name': self.picture_name_new,
                'img_data': self.picture_data,

                'test_time': self.test_time,
                'var_number': self.myCombo.get(),
                'res_number': self.myCombo_res.get(),
                'question_pool_tag': ""
            }
        )
        conn.commit()
        conn.close()


    def load(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        record_id = self.load_box.get()
        c.execute("SELECT * FROM my_table WHERE oid =" + record_id)
        records = c.fetchall()

        self.question_difficulty_entry.delete(0, END)
        self.question_category_entry.delete(0, END)
        self.question_type_entry.delete(0, END)

        self.question_title_entry.delete(0, END)
        self.question_description_entry.delete(0, END)
        self.formula_question_entry.delete('1.0', 'end-1c')

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


        for record in records:
            self.question_difficulty_entry.insert(END, record[0])
            self.question_category_entry.insert(END, record[1])
            self.question_type_entry.insert(END, record[2])

            self.question_title_entry.insert(END, record[3])
            self.question_description_entry.insert(END, record[4])
            self.formula_question_entry.insert(END, record[5])

            self.res1_formula_entry.insert(END, record[6])
            self.res2_formula_entry.insert(END, record[7])
            self.res3_formula_entry.insert(END, record[8])
            self.res4_formula_entry.insert(END, record[9])
            self.res5_formula_entry.insert(END, record[10])
            self.res6_formula_entry.insert(END, record[11])
            self.res7_formula_entry.insert(END, record[12])
            self.res8_formula_entry.insert(END, record[13])
            self.res9_formula_entry.insert(END, record[14])
            self.res10_formula_entry.insert(END, record[15])

            self.var1_name_entry.insert(END, record[16])
            self.var1_min_entry.insert(END, record[17])
            self.var1_max_entry.insert(END, record[18])
            self.var1_prec_entry.insert(END, record[19])
            self.var1_divby_entry.insert(END, record[20])
            self.var1_unit_myCombo.set(record[21])

            self.var2_name_entry.insert(END, record[22])
            self.var2_min_entry.insert(END, record[23])
            self.var2_max_entry.insert(END, record[24])
            self.var2_prec_entry.insert(END, record[25])
            self.var2_divby_entry.insert(END, record[26])
            self.var2_unit_myCombo.set(record[27])

            self.var3_name_entry.insert(END, record[28])
            self.var3_min_entry.insert(END, record[29])
            self.var3_max_entry.insert(END, record[30])
            self.var3_prec_entry.insert(END, record[31])
            self.var3_divby_entry.insert(END, record[32])
            self.var3_unit_myCombo.set(record[33])

            self.var4_name_entry.insert(END, record[34])
            self.var4_min_entry.insert(END, record[35])
            self.var4_max_entry.insert(END, record[36])
            self.var4_prec_entry.insert(END, record[37])
            self.var4_divby_entry.insert(END, record[38])
            self.var4_unit_myCombo.set(record[39])

            self.var5_name_entry.insert(END, record[40])
            self.var5_min_entry.insert(END, record[41])
            self.var5_max_entry.insert(END, record[42])
            self.var5_prec_entry.insert(END, record[43])
            self.var5_divby_entry.insert(END, record[44])
            self.var5_unit_myCombo.set(record[45])

            self.var6_name_entry.insert(END, record[46])
            self.var6_min_entry.insert(END, record[47])
            self.var6_max_entry.insert(END, record[48])
            self.var6_prec_entry.insert(END, record[49])
            self.var6_divby_entry.insert(END, record[50])
            self.var6_unit_myCombo.set(record[51])

            self.var7_name_entry.insert(END, record[52])
            self.var7_min_entry.insert(END, record[53])
            self.var7_max_entry.insert(END, record[54])
            self.var7_prec_entry.insert(END, record[55])
            self.var7_divby_entry.insert(END, record[56])
            self.var7_unit_myCombo.set(record[57])

            self.var8_name_entry.insert(END, record[58])
            self.var8_min_entry.insert(END, record[59])
            self.var8_max_entry.insert(END, record[60])
            self.var8_prec_entry.insert(END, record[61])
            self.var8_divby_entry.insert(END, record[62])
            #self.var8_unit_myCombo.set(record[63])

            self.var9_name_entry.insert(END, record[64])
            self.var9_min_entry.insert(END, record[65])
            self.var9_max_entry.insert(END, record[66])
            self.var9_prec_entry.insert(END, record[67])
            self.var9_divby_entry.insert(END, record[68])
            #self.var9_unit_myCombo.set(record[69])

            self.var10_name_entry.insert(END, record[70])
            self.var10_min_entry.insert(END, record[71])
            self.var10_max_entry.insert(END, record[72])
            self.var10_prec_entry.insert(END, record[73])
            self.var10_divby_entry.insert(END, record[74])
            #self.var10_unit_myCombo.set(record[75])

            self.res1_name_entry.insert(END, record[76])
            self.res1_min_entry.insert(END, record[77])
            self.res1_max_entry.insert(END, record[78])
            self.res1_prec_entry.insert(END, record[79])
            self.res1_tol_entry.insert(END, record[80])
            self.res1_points_entry.insert(END, record[81])
            self.res1_unit_myCombo.set(record[82])

            self.res2_name_entry.insert(END, record[83])
            self.res2_min_entry.insert(END, record[84])
            self.res2_max_entry.insert(END, record[85])
            self.res2_prec_entry.insert(END, record[86])
            self.res2_tol_entry.insert(END, record[87])
            self.res2_points_entry.insert(END, record[88])
            self.res2_unit_myCombo.set(record[89])

            self.res3_name_entry.insert(END, record[90])
            self.res3_min_entry.insert(END, record[91])
            self.res3_max_entry.insert(END, record[92])
            self.res3_prec_entry.insert(END, record[93])
            self.res3_tol_entry.insert(END, record[94])
            self.res3_points_entry.insert(END, record[95])
            self.res3_unit_myCombo.set(record[96])

            self.res4_name_entry.insert(END, record[97])
            self.res4_min_entry.insert(END, record[98])
            self.res4_max_entry.insert(END, record[99])
            self.res4_prec_entry.insert(END, record[100])
            self.res4_tol_entry.insert(END, record[101])
            self.res4_points_entry.insert(END, record[102])
            #self.res4_unit_myCombo.set(record[103])

            self.res5_name_entry.insert(END, record[104])
            self.res5_min_entry.insert(END, record[105])
            self.res5_max_entry.insert(END, record[106])
            self.res5_prec_entry.insert(END, record[107])
            self.res5_tol_entry.insert(END, record[108])
            self.res5_points_entry.insert(END, record[109])
            #self.res5_unit_myCombo.set(record[110])

            self.res6_name_entry.insert(END, record[111])
            self.res6_min_entry.insert(END, record[112])
            self.res6_max_entry.insert(END, record[113])
            self.res6_prec_entry.insert(END, record[114])
            self.res6_tol_entry.insert(END, record[115])
            self.res6_points_entry.insert(END, record[116])
            #self.res6_unit_myCombo.set(record[117])

            self.res7_name_entry.insert(END, record[118])
            self.res7_min_entry.insert(END, record[119])
            self.res7_max_entry.insert(END, record[120])
            self.res7_prec_entry.insert(END, record[121])
            self.res7_tol_entry.insert(END, record[122])
            self.res7_points_entry.insert(END, record[123])
            #self.res7_unit_myCombo.set(record[124])

            self.res8_name_entry.insert(END, record[125])
            self.res8_min_entry.insert(END, record[126])
            self.res8_max_entry.insert(END, record[127])
            self.res8_prec_entry.insert(END, record[128])
            self.res8_tol_entry.insert(END, record[129])
            self.res8_points_entry.insert(END, record[130])
            #self.res8_unit_myCombo.set(record[131])

            self.res9_name_entry.insert(END, record[132])
            self.res9_min_entry.insert(END, record[133])
            self.res9_max_entry.insert(END, record[134])
            self.res9_prec_entry.insert(END, record[135])
            self.res9_tol_entry.insert(END, record[136])
            self.res9_points_entry.insert(END, record[137])
            #self.res9_unit_myCombo.set(record[138])

            self.res10_name_entry.insert(END, record[139])
            self.res10_min_entry.insert(END, record[140])
            self.res10_max_entry.insert(END, record[141])
            self.res10_prec_entry.insert(END, record[142])
            self.res10_tol_entry.insert(END, record[143])
            self.res10_points_entry.insert(END, record[144])
            #self.res10_unit_myCombo.set(record[145])

            # self.img_name.insert(END, record[146])
            # self.img_data.insert(END, record[147])

            self.test_time_from_db = record[148]
            self.var_number = record[149]
            self.myCombo.set(record[149])
            self.res_number = record[150]
            self.myCombo_res.set(record[150])

        conn.commit()
        conn.close()

        Formelfrage.selected_var_from_db(self, self.myCombo.get())
        Formelfrage.selected_res_from_db(self, self.myCombo_res.get())

        #Database.selected_res_from_db(self.res_number)

        # format of duration P0Y0M0DT0H30M0S
        self.proc_hours_from_db_start = self.test_time_from_db.find('T') + 1
        self.proc_hours_from_db_end = self.test_time_from_db.find('H', self.proc_hours_from_db_start)
        self.proc_hours_from_db = self.test_time_from_db[self.proc_hours_from_db_start:self.proc_hours_from_db_end]

        self.proc_minutes_from_db_start = self.test_time_from_db.find('H') + 1
        self.proc_minutes_from_db_end = self.test_time_from_db.find('M', self.proc_minutes_from_db_start)
        self.proc_minutes_from_db = self.test_time_from_db[self.proc_minutes_from_db_start:self.proc_minutes_from_db_end]

        self.proc_seconds_from_db_start = self.test_time_from_db.find('M', 5) + 1
        self.proc_seconds_from_db_end = self.test_time_from_db.find('S', self.proc_seconds_from_db_start)
        self.proc_seconds_from_db = self.test_time_from_db[self.proc_seconds_from_db_start:self.proc_seconds_from_db_end]

        self.proc_hours_box.current(self.proc_hours_from_db)
        self.proc_minutes_box.current(self.proc_minutes_from_db)
        self.proc_seconds_box.current(self.proc_seconds_from_db)


        print("Load Question with ID: " + record_id)

        if self.var_highlight_question_text == 1:
            Database.reallocate_text(self)


    def edit(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        record_id = self.load_box.get()

        # format of duration P0Y0M0DT0H30M0S
        self.test_time = "P0Y0M0DT" + self.proc_hours_box.get() + "H" + self.proc_minutes_box.get() + "M" + self.proc_seconds_box.get() + "S"

        # Dieser String muss modifiziert werden. In der xml ist ein Zeilenumbrauch als "&lt;/p&gt;&#13;&#10;&lt;p&gt;" definiert und nur 1 Zeile!

        # print(self.picture_name)

        if self.picture_name != "EMPTY":
            # read image data in byte format
            with open(self.picture_name, 'rb') as image_file:
                self.picture_data = image_file.read()


        else:
            self.picture_name_new = "EMPTY"
            self.picture_data = "EMPTY"

        c.execute("""UPDATE my_table SET
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
            
            img_name = :img_name,
            img_data = :img_data,
            
            test_time= :test_time
    
            WHERE oid = :oid""",
                {'question_difficulty': self.question_difficulty_entry.get(),
                 'question_category': self.question_category_entry.get(),
                 'question_type': self.question_type_entry.get(),

                 'question_title': self.question_title_entry.get(),
                 'question_description_title': self.question_description_entry.get(),

                 'question_description_main': self.formula_question_entry.get("1.0", 'end-1c'),

                 'res1_formula': self.res1_formula_text.get(),
                 'res2_formula': self.res2_formula_text.get(),
                 'res3_formula': self.res3_formula_text.get(),
                 'res4_formula': self.res4_formula_text.get(),
                 'res5_formula': self.res5_formula_text.get(),
                 'res6_formula': self.res6_formula_text.get(),
                 'res7_formula': self.res7_formula_text.get(),
                 'res8_formula': self.res8_formula_text.get(),
                 'res9_formula': self.res9_formula_text.get(),
                 'res10_formula': self.res10_formula_text.get(),

                 'var1_name': self.var1_name_text.get(),
                 'var1_min': self.var1_min_text.get(),
                 'var1_max': self.var1_max_text.get(),
                 'var1_prec': self.var1_prec_text.get(),
                 'var1_divby': self.var1_divby_text.get(),
                 'var1_unit': self.var1_unit_myCombo.get(),

                 'var2_name': self.var2_name_text.get(),
                 'var2_min': self.var2_min_text.get(),
                 'var2_max': self.var2_max_text.get(),
                 'var2_prec': self.var2_prec_text.get(),
                 'var2_divby': self.var2_divby_text.get(),
                 'var2_unit': self.var2_unit_myCombo.get(),

                 'var3_name': self.var3_name_text.get(),
                 'var3_min': self.var3_min_text.get(),
                 'var3_max': self.var3_max_text.get(),
                 'var3_prec': self.var3_prec_text.get(),
                 'var3_divby': self.var3_divby_text.get(),
                 'var3_unit': self.var3_unit_myCombo.get(),

                 'var4_name': self.var4_name_text.get(),
                 'var4_min': self.var4_min_text.get(),
                 'var4_max': self.var4_max_text.get(),
                 'var4_prec': self.var4_prec_text.get(),
                 'var4_divby': self.var4_divby_text.get(),
                 'var4_unit': self.var4_unit_myCombo.get(),

                 'var5_name': self.var5_name_text.get(),
                 'var5_min': self.var5_min_text.get(),
                 'var5_max': self.var5_max_text.get(),
                 'var5_prec': self.var5_prec_text.get(),
                 'var5_divby': self.var5_divby_text.get(),
                 'var5_unit': self.var5_unit_myCombo.get(),

                 'var6_name': self.var6_name_text.get(),
                 'var6_min': self.var6_min_text.get(),
                 'var6_max': self.var6_max_text.get(),
                 'var6_prec': self.var6_prec_text.get(),
                 'var6_divby': self.var6_divby_text.get(),
                 'var6_unit': self.var6_unit_myCombo.get(),

                 'var7_name': self.var7_name_text.get(),
                 'var7_min': self.var7_min_text.get(),
                 'var7_max': self.var7_max_text.get(),
                 'var7_prec': self.var7_prec_text.get(),
                 'var7_divby': self.var7_divby_text.get(),
                 'var7_unit': self.var7_unit_myCombo.get(),

                 'var8_name': self.var8_name_text.get(),
                 'var8_min': self.var8_min_text.get(),
                 'var8_max': self.var8_max_text.get(),
                 'var8_prec': self.var8_prec_text.get(),
                 'var8_divby': self.var8_divby_text.get(),
                 'var8_unit': "Unit",

                 'var9_name': self.var9_name_text.get(),
                 'var9_min': self.var9_min_text.get(),
                 'var9_max': self.var9_max_text.get(),
                 'var9_prec': self.var9_prec_text.get(),
                 'var9_divby': self.var9_divby_text.get(),
                 'var9_unit': "Unit",

                 'var10_name': self.var10_name_text.get(),
                 'var10_min': self.var10_min_text.get(),
                 'var10_max': self.var10_max_text.get(),
                 'var10_prec': self.var10_prec_text.get(),
                 'var10_divby': self.var10_divby_text.get(),
                 'var10_unit': "Unit",

                 'res1_name': self.res1_name_text.get(),
                 'res1_min': self.res1_min_text.get(),
                 'res1_max': self.res1_max_text.get(),
                 'res1_prec': self.res1_prec_text.get(),
                 'res1_tol': self.res1_tol_text.get(),
                 'res1_points': self.res1_points_text.get(),
                 'res1_unit': self.res1_unit_myCombo.get(),

                 'res2_name': self.res2_name_text.get(),
                 'res2_min': self.res2_min_text.get(),
                 'res2_max': self.res2_max_text.get(),
                 'res2_prec': self.res2_prec_text.get(),
                 'res2_tol': self.res2_tol_text.get(),
                 'res2_points': self.res2_points_text.get(),
                 'res2_unit': self.res2_unit_myCombo.get(),

                 'res3_name': self.res3_name_text.get(),
                 'res3_min': self.res3_min_text.get(),
                 'res3_max': self.res3_max_text.get(),
                 'res3_prec': self.res3_prec_text.get(),
                 'res3_tol': self.res3_tol_text.get(),
                 'res3_points': self.res3_points_text.get(),
                 'res3_unit': self.res3_unit_myCombo.get(),

                 'res4_name': self.res4_name_text.get(),
                 'res4_min': self.res4_min_text.get(),
                 'res4_max': self.res4_max_text.get(),
                 'res4_prec': self.res4_prec_text.get(),
                 'res4_tol': self.res4_tol_text.get(),
                 'res4_points': self.res4_points_text.get(),
                 'res4_unit': "Unit",

                 'res5_name': self.res5_name_text.get(),
                 'res5_min': self.res5_min_text.get(),
                 'res5_max': self.res5_max_text.get(),
                 'res5_prec': self.res5_prec_text.get(),
                 'res5_tol': self.res5_tol_text.get(),
                 'res5_points': self.res5_points_text.get(),
                 'res5_unit': "Unit",

                 'res6_name': self.res6_name_text.get(),
                 'res6_min': self.res6_min_text.get(),
                 'res6_max': self.res6_max_text.get(),
                 'res6_prec': self.res6_prec_text.get(),
                 'res6_tol': self.res6_tol_text.get(),
                 'res6_points': self.res6_points_text.get(),
                 'res6_unit': "Unit",

                 'res7_name': self.res7_name_text.get(),
                 'res7_min': self.res7_min_text.get(),
                 'res7_max': self.res7_max_text.get(),
                 'res7_prec': self.res7_prec_text.get(),
                 'res7_tol': self.res7_tol_text.get(),
                 'res7_points': self.res7_points_text.get(),
                 'res7_unit': "Unit",

                 'res8_name': self.res8_name_text.get(),
                 'res8_min': self.res8_min_text.get(),
                 'res8_max': self.res8_max_text.get(),
                 'res8_prec': self.res8_prec_text.get(),
                 'res8_tol': self.res8_tol_text.get(),
                 'res8_points': self.res8_points_text.get(),
                 'res8_unit': "Unit",

                 'res9_name': self.res9_name_text.get(),
                 'res9_min': self.res9_min_text.get(),
                 'res9_max': self.res9_max_text.get(),
                 'res9_prec': self.res9_prec_text.get(),
                 'res9_tol': self.res9_tol_text.get(),
                 'res9_points': self.res9_points_text.get(),
                 'res9_unit': "Unit",

                 'res10_name': self.res10_name_text.get(),
                 'res10_min': self.res10_min_text.get(),
                 'res10_max': self.res10_max_text.get(),
                 'res10_prec': self.res10_prec_text.get(),
                 'res10_tol': self.res10_tol_text.get(),
                 'res10_points': self.res10_points_text.get(),
                 'res10_unit': "Unit",

                 'img_name': self.picture_name_new,
                 'img_data': self.picture_data,

                 'test_time': self.test_time,
                 'oid': record_id
                 })

        conn.commit()
        conn.close()

        print("Question with id: '" + record_id + "' edited")


    def show_records(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        # Clear List Boxes
        Database.clear_listboxes(self)

        self.Database_entrys = []

        # Loop thru Results
        for record in records:

            self.my_listbox_question_difficulty.insert(END, record[0])
            self.my_listbox_question_category.insert(END, record[1])
            self.my_listbox_question_type.insert(END, record[2])

            self.my_listbox_question_title.insert(END, record[3])
            self.my_listbox_question_description_title.insert(END, record[4])
            self.my_listbox_question_description_main.insert(END, record[5])

            self.my_listbox_res1_formula.insert(END, record[6])
            self.my_listbox_res2_formula.insert(END, record[7])
            self.my_listbox_res3_formula.insert(END, record[8])
            #self.my_listbox_res4_formula.insert(END, record[9])
            #self.my_listbox_res5_formula.insert(END, record[10])
            #self.my_listbox_res6_formula.insert(END, record[11])
            #self.my_listbox_res7_formula.insert(END, record[12])
            #self.my_listbox_res8_formula.insert(END, record[13])
            #self.my_listbox_res9_formula.insert(END, record[14])
            #self.my_listbox_res10_formula.insert(END, record[15])

            self.my_listbox_var1_name.insert(END, record[16])
            self.my_listbox_var1_min.insert(END, record[17])
            self.my_listbox_var1_max.insert(END, record[18])
            self.my_listbox_var1_prec.insert(END, record[19])
            self.my_listbox_var1_divby.insert(END, record[20])
            self.my_listbox_var1_unit.insert(END, record[21])

            self.my_listbox_var2_name.insert(END, record[22])
            self.my_listbox_var2_min.insert(END, record[23])
            self.my_listbox_var2_max.insert(END, record[24])
            self.my_listbox_var2_prec.insert(END, record[25])
            self.my_listbox_var2_divby.insert(END, record[26])
            self.my_listbox_var2_unit.insert(END, record[27])

            self.my_listbox_var3_name.insert(END, record[28])
            self.my_listbox_var3_min.insert(END, record[29])
            self.my_listbox_var3_max.insert(END, record[30])
            self.my_listbox_var3_prec.insert(END, record[31])
            self.my_listbox_var3_divby.insert(END, record[32])
            self.my_listbox_var3_unit.insert(END, record[33])

            self.my_listbox_var4_name.insert(END, record[34])
            self.my_listbox_var4_min.insert(END, record[35])
            self.my_listbox_var4_max.insert(END, record[36])
            self.my_listbox_var4_prec.insert(END, record[37])
            self.my_listbox_var4_divby.insert(END, record[38])
            self.my_listbox_var4_unit.insert(END, record[39])

            self.my_listbox_var5_name.insert(END, record[40])
            self.my_listbox_var5_min.insert(END, record[41])
            self.my_listbox_var5_max.insert(END, record[42])
            self.my_listbox_var5_prec.insert(END, record[43])
            self.my_listbox_var5_divby.insert(END, record[44])
            self.my_listbox_var5_unit.insert(END, record[45])

            self.my_listbox_var6_name.insert(END, record[46])
            self.my_listbox_var6_min.insert(END, record[47])
            self.my_listbox_var6_max.insert(END, record[48])
            self.my_listbox_var6_prec.insert(END, record[49])
            self.my_listbox_var6_divby.insert(END, record[50])
            self.my_listbox_var6_unit.insert(END, record[51])

            self.my_listbox_var7_name.insert(END, record[52])
            self.my_listbox_var7_min.insert(END, record[53])
            self.my_listbox_var7_max.insert(END, record[54])
            self.my_listbox_var7_prec.insert(END, record[55])
            self.my_listbox_var7_divby.insert(END, record[56])
            self.my_listbox_var7_unit.insert(END, record[57])

            self.my_listbox_res1_name.insert(END, record[76])
            self.my_listbox_res1_min.insert(END, record[77])
            self.my_listbox_res1_max.insert(END, record[78])
            self.my_listbox_res1_prec.insert(END, record[79])
            self.my_listbox_res1_tol.insert(END, record[80])
            self.my_listbox_res1_points.insert(END, record[81])
            self.my_listbox_res1_unit.insert(END, record[82])

            self.my_listbox_res2_name.insert(END, record[83])
            self.my_listbox_res2_min.insert(END, record[84])
            self.my_listbox_res2_max.insert(END, record[85])
            self.my_listbox_res2_prec.insert(END, record[86])
            self.my_listbox_res2_tol.insert(END, record[87])
            self.my_listbox_res2_points.insert(END, record[88])
            self.my_listbox_res2_unit.insert(END, record[89])

            self.my_listbox_res3_name.insert(END, record[90])
            self.my_listbox_res3_min.insert(END, record[91])
            self.my_listbox_res3_max.insert(END, record[92])
            self.my_listbox_res3_prec.insert(END, record[93])
            self.my_listbox_res3_tol.insert(END, record[94])
            self.my_listbox_res3_points.insert(END, record[95])
            self.my_listbox_res3_unit.insert(END, record[96])

            self.my_listbox_img_name.insert(END, record[146])
            #self.my_listbox_img_data.insert(END, record[147])
            #img_data slows "show records" down, therefore not inserted

            self.my_listbox_test_time.insert(END, record[148])
            self.my_listbox_oid.insert(END, record[len(record)-1])



            self.Database_entrys.append(record[len(record)-1])



        conn.commit()
        conn.close()


        self.var_oid_entrys = len(self.Database_entrys)
        self.listbox_oid_entrys_label = Label(self.db_inner_frame, text=self.var_oid_entrys)
        self.listbox_oid_entrys_label.grid(row=40, column=2, sticky=W)

        self.listbox_oid_label = Label(self.db_inner_frame, text="DB\nEinträge:")
        self.listbox_oid_label.grid(row=40, column=1, sticky=W)

    def delete(self):

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        self.delete_list = []
        self.delete_all_list = []
        self.delete_list = self.delete_box.get().split(",")
        self.delete_mult = self.delete_box.get()
        self.delete_mult_start = self.delete_mult.split('-')[0]
        self.delete_mult_end = self.delete_mult.split('-')[-1]
        self.delete_mult_symbol = "-" in self.delete_mult
        print(self.delete_mult_start)
        print(self.delete_mult_end)
        print(self.delete_mult_symbol)

        if self.var_delete_all.get() == 1:
            now = datetime.now()  # current date and time
            date_time = now.strftime("%d.%m.%Y_%Hh-%Mm")
            actual_time = str(date_time)
            Database.sql_db_to_excel_export(self, "BACKUP_Export_from_SQL__" + str(actual_time) + ".xlsx")
            c.execute("SELECT *, oid FROM my_table")
            records = c.fetchall()
            for record in records:
                self.delete_all_list.append(int(record[len(record) - 1]))

           #self.my_string = ','.join(map(str, self.delete_all_list))
            #print(self.my_string)
            #self.entry_split = self.my_string.split(",")


            for x in range(len(self.delete_all_list)):
                c.execute("DELETE from my_table WHERE oid= " + str(self.delete_all_list[x]))
            print("All Entries removed!")


        elif self.delete_mult_symbol == True:

            for x in range(int(self.delete_mult_start), int(self.delete_mult_end)+1):
                c.execute("DELETE from my_table WHERE oid= " + str(x))
                print("Entry with ID " + str(x) + " removed!")


        else:
            for x in range(len(self.delete_list)):
                c.execute("DELETE from my_table WHERE oid= " + str(self.delete_list[x]))
                print("Entry with ID " + str(self.delete_list[x]) + " removed!")

        self.delete_box.delete(0, END)

        conn.commit()
        conn.close()


    def excel_xlsx_import(self):

        self.xlsx_path = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
        self.xlsx_data = pd.read_excel(self.xlsx_path)


        self.last_char_index = self.xlsx_path.rfind("/")
        self.foo2 = ([pos for pos, char in enumerate(self.xlsx_path) if char == '/'])
        self.foo2_len = len(self.foo2)
        self.xlsx_name= self.xlsx_path[self.foo2[self.foo2_len - 1] + 1:]


        self.df = pd.DataFrame(self.xlsx_data, columns=['question_difficulty',
                                             'question_category',
                                             'question_type',
                                             'question_title',
                                             'question_description_title',
                                             'question_description_main',
                                             'res1_formula',
                                             'res2_formula',
                                             'res3_formula',
                                             'res4_formula',
                                             'res5_formula',
                                             'res6_formula',
                                             'res7_formula',
                                             'res8_formula',
                                             'res9_formula',
                                             'res10_formula',
                                             'var1_name',
                                             'var1_min',
                                             'var1_max',
                                             'var1_prec',
                                             'var1_divby',
                                             'var1_unit',
                                             'var2_name',
                                             'var2_min',
                                             'var2_max',
                                             'var2_prec',
                                             'var2_divby',
                                             'var2_unit',
                                             'var3_name',
                                             'var3_min',
                                             'var3_max',
                                             'var3_prec',
                                             'var3_divby',
                                             'var3_unit',
                                             'var4_name',
                                             'var4_min',
                                             'var4_max',
                                             'var4_prec',
                                             'var4_divby',
                                             'var4_unit',
                                             'var5_name',
                                             'var5_min',
                                             'var5_max',
                                             'var5_prec',
                                             'var5_divby',
                                             'var5_unit',
                                             'var6_name',
                                             'var6_min',
                                             'var6_max',
                                             'var6_prec',
                                             'var6_divby',
                                             'var6_unit',
                                             'var7_name',
                                             'var7_min',
                                             'var7_max',
                                             'var7_prec',
                                             'var7_divby',
                                             'var7_unit',
                                            'var8_name',
                                            'var8_min',
                                            'var8_max',
                                            'var8_prec',
                                            'var8_divby',
                                            'var8_unit',
                                            'var9_name',
                                            'var9_min',
                                            'var9_max',
                                            'var9_prec',
                                            'var9_divby',
                                            'var9_unit',
                                            'var10_name',
                                            'var10_min',
                                            'var10_max',
                                            'var10_prec',
                                            'var10_divby',
                                            'var10_unit',
                                             'res1_name',
                                             'res1_min',
                                             'res1_max',
                                             'res1_prec',
                                             'res1_tol',
                                             'res1_points',
                                             'res1_unit',
                                             'res2_name',
                                             'res2_min',
                                             'res2_max',
                                             'res2_prec',
                                             'res2_tol',
                                             'res2_points',
                                             'res2_unit',
                                             'res3_name',
                                             'res3_min',
                                             'res3_max',
                                             'res3_prec',
                                             'res3_tol',
                                             'res3_points',
                                             'res3_unit',
                                            'res4_name',
                                            'res4_min',
                                            'res4_max',
                                            'res4_prec',
                                            'res4_tol',
                                            'res4_points',
                                            'res4_unit',
                                            'res5_name',
                                            'res5_min',
                                            'res5_max',
                                            'res5_prec',
                                            'res5_tol',
                                            'res5_points',
                                            'res5_unit',
                                            'res6_name',
                                            'res6_min',
                                            'res6_max',
                                            'res6_prec',
                                            'res6_tol',
                                            'res6_points',
                                            'res6_unit',
                                            'res7_name',
                                            'res7_min',
                                            'res7_max',
                                            'res7_prec',
                                            'res7_tol',
                                            'res7_points',
                                            'res7_unit',
                                            'res8_name',
                                            'res8_min',
                                            'res8_max',
                                            'res8_prec',
                                            'res8_tol',
                                            'res8_points',
                                            'res8_unit',
                                            'res9_name',
                                            'res9_min',
                                            'res9_max',
                                            'res9_prec',
                                            'res9_tol',
                                            'res9_points',
                                            'res9_unit',
                                            'res10_name',
                                            'res10_min',
                                            'res10_max',
                                            'res10_prec',
                                            'res10_tol',
                                            'res10_points',
                                            'res10_unit',
                                             'img_name',
                                             'img_data',
                                             'test_time',
                                             'var_number',
                                             'res_number',
                                             'question_pool_tag'])

        self.df = self.df.fillna("")

        ########## Bilder auslesen
        self.foo = ([pos for pos, char in enumerate(self.xlsx_path) if char == '/'])
        self.foo_len = len(self.foo)
        self.xlsx_file_path = self.xlsx_path[self.foo[self.foo_len - 1] + 1:]
        print("Load File: \"" + self.xlsx_file_path + "\" in mySQL...done!")

        self.file_name = self.xlsx_name
        self.sheet_name = 'SQL - Database'
        self.workbook = openpyxl.load_workbook(self.file_name)
        self.worksheet = self.workbook[self.sheet_name]

        #df = pd.read_excel(self.file_name, sheet_name=self.sheet_name, dtype=object)

        for img in self.worksheet._images:
            img.ref.seek(0)
            self.df.iat[img.anchor.to.row - 1, img.anchor.to.col] = img.ref.read()

        ################## Bilder auslesen

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        conn.commit()

        for row in self.df.itertuples():
            c.execute(
                "INSERT INTO my_table VALUES ("
                ":question_difficulty, :question_category, :question_type, "
                ":question_title, :question_description_title, :question_description_main, "
                ":res1_formula, :res2_formula, :res3_formula,  "
                ":res4_formula, :res5_formula, :res6_formula,  "
                ":res7_formula, :res8_formula, :res9_formula, :res10_formula, "
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
                ":res3_name, :res3_min, :res3_max, :res3_prec, :res3_tol, :res3_points, :res3_unit,"
                ":res4_name, :res4_min, :res4_max, :res4_prec, :res4_tol, :res4_points, :res4_unit, "
                ":res5_name, :res5_min, :res5_max, :res5_prec, :res5_tol, :res5_points, :res5_unit, "
                ":res6_name, :res6_min, :res6_max, :res6_prec, :res6_tol, :res6_points, :res6_unit, "
                ":res7_name, :res7_min, :res7_max, :res7_prec, :res7_tol, :res7_points, :res7_unit, "
                ":res8_name, :res8_min, :res8_max, :res8_prec, :res8_tol, :res8_points, :res8_unit, "
                ":res9_name, :res9_min, :res9_max, :res9_prec, :res9_tol, :res9_points, :res9_unit, "
                ":res10_name, :res10_min, :res10_max, :res10_prec, :res10_tol, :res10_points, :res10_unit, "
                ":img_name, :img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
                {
                    'question_difficulty': row.question_difficulty,
                    'question_category': row.question_category,
                    'question_type': row.question_type,
                    'question_title': row.question_title,
                    'question_description_title': row.question_description_title,
                    'question_description_main': row.question_description_main,

                    'res1_formula': row.res1_formula,
                    'res2_formula': row.res2_formula,
                    'res3_formula': row.res3_formula,
                    'res4_formula': row.res4_formula,
                    'res5_formula': row.res5_formula,
                    'res6_formula': row.res6_formula,
                    'res7_formula': row.res7_formula,
                    'res8_formula': row.res8_formula,
                    'res9_formula': row.res9_formula,
                    'res10_formula': row.res10_formula,

                    'var1_name': row.var1_name,
                    'var1_min': row.var1_min,
                    'var1_max': row.var1_max,
                    'var1_prec': row.var1_prec,
                    'var1_divby': row.var1_divby,
                    'var1_unit': row.var1_unit,

                    'var2_name': row.var2_name,
                    'var2_min': row.var2_min,
                    'var2_max': row.var2_max,
                    'var2_prec': row.var2_prec,
                    'var2_divby': row.var2_divby,
                    'var2_unit': row.var2_unit,

                    'var3_name': row.var3_name,
                    'var3_min': row.var3_min,
                    'var3_max': row.var3_max,
                    'var3_prec': row.var3_prec,
                    'var3_divby': row.var3_divby,
                    'var3_unit': row.var3_unit,

                    'var4_name': row.var4_name,
                    'var4_min': row.var4_min,
                    'var4_max': row.var4_max,
                    'var4_prec': row.var4_prec,
                    'var4_divby': row.var4_divby,
                    'var4_unit': row.var4_unit,

                    'var5_name': row.var5_name,
                    'var5_min': row.var5_min,
                    'var5_max': row.var5_max,
                    'var5_prec': row.var5_prec,
                    'var5_divby': row.var5_divby,
                    'var5_unit': row.var5_unit,

                    'var6_name': row.var6_name,
                    'var6_min': row.var6_min,
                    'var6_max': row.var6_max,
                    'var6_prec': row.var6_prec,
                    'var6_divby': row.var6_divby,
                    'var6_unit': row.var6_unit,

                    'var7_name': row.var7_name,
                    'var7_min': row.var7_min,
                    'var7_max': row.var7_max,
                    'var7_prec': row.var7_prec,
                    'var7_divby': row.var7_divby,
                    'var7_unit': row.var7_unit,

                    'var8_name': row.var8_name,
                    'var8_min': row.var8_min,
                    'var8_max': row.var8_max,
                    'var8_prec': row.var8_prec,
                    'var8_divby': row.var8_divby,
                    'var8_unit': row.var8_unit,

                    'var9_name': row.var9_name,
                    'var9_min': row.var9_min,
                    'var9_max': row.var9_max,
                    'var9_prec': row.var9_prec,
                    'var9_divby': row.var9_divby,
                    'var9_unit': row.var9_unit,

                    'var10_name': row.var10_name,
                    'var10_min': row.var10_min,
                    'var10_max': row.var10_max,
                    'var10_prec': row.var10_prec,
                    'var10_divby': row.var10_divby,
                    'var10_unit': row.var10_unit,

                    'res1_name': row.res1_name,
                    'res1_min': row.res1_min,
                    'res1_max': row.res1_max,
                    'res1_prec': row.res1_prec,
                    'res1_tol': row.res1_tol,
                    'res1_points': row.res1_points,
                    'res1_unit': row.res1_unit,

                    'res2_name': row.res2_name,
                    'res2_min': row.res2_min,
                    'res2_max': row.res2_max,
                    'res2_prec': row.res2_prec,
                    'res2_tol': row.res2_tol,
                    'res2_points': row.res2_points,
                    'res2_unit': row.res2_unit,

                    'res3_name': row.res3_name,
                    'res3_min': row.res3_min,
                    'res3_max': row.res3_max,
                    'res3_prec': row.res3_prec,
                    'res3_tol': row.res3_tol,
                    'res3_points': row.res3_points,
                    'res3_unit': row.res3_unit,

                    'res4_name': row.res4_name,
                    'res4_min': row.res4_min,
                    'res4_max': row.res4_max,
                    'res4_prec': row.res4_prec,
                    'res4_tol': row.res4_tol,
                    'res4_points': row.res4_points,
                    'res4_unit': row.res4_unit,

                    'res5_name': row.res5_name,
                    'res5_min': row.res5_min,
                    'res5_max': row.res5_max,
                    'res5_prec': row.res5_prec,
                    'res5_tol': row.res5_tol,
                    'res5_points': row.res5_points,
                    'res5_unit': row.res5_unit,

                    'res6_name': row.res6_name,
                    'res6_min': row.res6_min,
                    'res6_max': row.res6_max,
                    'res6_prec': row.res6_prec,
                    'res6_tol': row.res6_tol,
                    'res6_points': row.res6_points,
                    'res6_unit': row.res6_unit,

                    'res7_name': row.res7_name,
                    'res7_min': row.res7_min,
                    'res7_max': row.res7_max,
                    'res7_prec': row.res7_prec,
                    'res7_tol': row.res7_tol,
                    'res7_points': row.res7_points,
                    'res7_unit': row.res7_unit,

                    'res8_name': row.res8_name,
                    'res8_min': row.res8_min,
                    'res8_max': row.res8_max,
                    'res8_prec': row.res8_prec,
                    'res8_tol': row.res8_tol,
                    'res8_points': row.res8_points,
                    'res8_unit': row.res8_unit,

                    'res9_name': row.res9_name,
                    'res9_min': row.res9_min,
                    'res9_max': row.res9_max,
                    'res9_prec': row.res9_prec,
                    'res9_tol': row.res9_tol,
                    'res9_points': row.res9_points,
                    'res9_unit': row.res9_unit,

                    'res10_name': row.res10_name,
                    'res10_min': row.res10_min,
                    'res10_max': row.res10_max,
                    'res10_prec': row.res10_prec,
                    'res10_tol': row.res10_tol,
                    'res10_points': row.res10_points,
                    'res10_unit': row.res10_unit,

                    'img_name': row.img_name,
                    'img_data': row.img_data,

                    'test_time': row.test_time,
                    'var_number': row.var_number,
                    'res_number': row.res_number,
                    'question_pool_tag': row.question_pool_tag
                }
            )
        conn.commit()
        conn.close()





    def sql_db_to_excel_export(self, table_name):


        self.table_name = table_name
        print("TABLENAME: " + str(table_name))

        # Wird benutzt um das Bild aus der DB in Excel skaliert darzustellen
        image_width = 140.0
        image_height = 182.0

        cell_width = 10.0
        cell_height = 10.0

        x_scale = cell_width / image_width
        y_scale = cell_height / image_height
        ##########################################

        conn = sqlite3.connect('ilias_questions_db.db')
        cursor = conn.cursor()
        cursor.execute('select * from my_table')


        header = [row[0] for row in cursor.description]
        rows = cursor.fetchall()

        # Create an new Excel file and add a worksheet.
        excel = xlsxwriter.Workbook(table_name)
        excel_sheet = excel.add_worksheet('SQL - Database')

        # Create style for cells
        header_cell_format = excel.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
        body_cell_format = excel.add_format({'border': True})

        row_index = 0
        column_index = 0

        for column_name in header:
            excel_sheet.write(row_index, column_index, column_name, header_cell_format)
            column_index += 1

        row_index += 1
        for row in rows:

            column_index = 0
            for column_data in row:
                # Prüfen ob der Inhalt vom Typ String / Integer / Float ist
                # Wenn die Prüfung "falsch" ergibt, handelt es sich um einen Bild-Eintrag
                self.check_if_string_data = isinstance(column_data, str)
                self.check_if_integer_data = isinstance(column_data, int)
                self.check_if_float_data = isinstance(column_data, float)

                if self.check_if_string_data == false and self.check_if_integer_data == false and self.check_if_float_data == false:

                    # Row[3] beinhaltet die Fragentitel.
                    # Hierdurch können exportierte Bilder den Fragen zugeordnet werden

                    with open('Export_Bilder\\IMG_' + str(row[3]) + '.png', 'wb') as image_file:
                        image_file.write(column_data)
                        excel_sheet.insert_image('ER' + str(row_index+1), str(self.project_root_path) + '\\Export_Bilder\\IMG_' + str(row[3]) + '.png', {'object_position': 2, 'x_scale': x_scale, 'y_scale': y_scale})





                else:

                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)
                column_index += 1
            row_index += 1

        print(str(row_index) + ' rows written successfully to ' + excel.filename)




        # Closing workbook
        excel.close()


        """"
        ### Nachfolgend werde die Bilder_Strings in *.png umgewandelt
        print("Convert picture-string to *.png data...")
        workbook = xlrd.open_workbook(excel.filename)
        worksheet = workbook.sheet_by_index(0)

        # For row 0 and column 0
        worksheet.cell_value(0, 0)

        for p in range(worksheet.nrows):
            if len(str(worksheet.cell_value(p, 19))) > 20:
                self.picture_data_string = base64.b64decode(worksheet.cell_value(p,19))
                print(str(self.project_root_path) + '\\Export_Bilder\\' + str(worksheet.cell_value(p, 17)))
                with open("Export_Bilder\\" + str(worksheet.cell_value(p, 17)), 'wb') as picture:
                    picture.write(self.picture_data_string)
                    worksheet.write('T' + str(p+1), str(self.project_root_path) + '\\Export_Bilder\\' + str(worksheet.cell_value(p, 17)), {'object_position': 2, 'x_scale': x_scale, 'y_scale': y_scale})





        # Closing workbook
        excel.close()

        """


        ### Nachfolgender Check ob die Anzahl der Variablen die definiert sind, auch mit der Anzahl der Variablen in der angegebenen Formel übereinstimmt (nur für Formelfragen)
        print("Excel-File  check...")
        wb = xlrd.open_workbook(excel.filename)
        sheet = wb.sheet_by_index(0)

        # For row 0 and column 0
        sheet.cell_value(0, 0)

        for k in range(sheet.nrows):
            if sheet.cell_value(k, 2) == "Formelfrage":




                self.check_res1 = sheet.cell_value(k, 6)
                self.check_res2 = sheet.cell_value(k, 7)
                self.check_res3 = sheet.cell_value(k, 8)
                self.check_res4 = sheet.cell_value(k, 9)
                self.check_res5 = sheet.cell_value(k, 10)
                self.check_res6 = sheet.cell_value(k, 11)
                self.check_res7 = sheet.cell_value(k, 12)
                self.check_res8 = sheet.cell_value(k, 13)
                self.check_res9 = sheet.cell_value(k, 14)
                self.check_res10 = sheet.cell_value(k, 15)

                self.check_var1 = sheet.cell_value(k, 17)
                self.check_var2 = sheet.cell_value(k, 23)
                self.check_var3 = sheet.cell_value(k, 29)
                self.check_var4 = sheet.cell_value(k, 35)
                self.check_var5 = sheet.cell_value(k, 41)
                self.check_var6 = sheet.cell_value(k, 47)
                self.check_var7 = sheet.cell_value(k, 53)
                self.check_var8 = sheet.cell_value(k, 59)
                self.check_var9 = sheet.cell_value(k, 65)
                self.check_var10 = sheet.cell_value(k, 71)

                self.check_if_variable_exists_in_res1 = []
                self.check_if_variable_exists_in_res2 = []
                self.check_if_variable_exists_in_res3 = []
                self.check_if_variable_exists_in_res4 = []
                self.check_if_variable_exists_in_res5 = []
                self.check_if_variable_exists_in_res6 = []
                self.check_if_variable_exists_in_res7 = []
                self.check_if_variable_exists_in_res8 = []
                self.check_if_variable_exists_in_res9 = []
                self.check_if_variable_exists_in_res10 = []

                self.max_var_in_formula = 0
                self.max_res_in_formula = 0

                self.check_lists_joined = []


                for i in range(1,10):
                    if '$v' + str(i) in self.check_res1:
                        self.check_if_variable_exists_in_res1.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res1:
                        self.check_if_variable_exists_in_res1.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res2:
                        self.check_if_variable_exists_in_res2.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res2:
                        self.check_if_variable_exists_in_res2.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res3:
                        self.check_if_variable_exists_in_res3.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res3:
                        self.check_if_variable_exists_in_res3.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res4:
                        self.check_if_variable_exists_in_res4.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res4:
                        self.check_if_variable_exists_in_res4.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res5:
                        self.check_if_variable_exists_in_res5.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res5:
                        self.check_if_variable_exists_in_res5.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res6:
                        self.check_if_variable_exists_in_res6.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res6:
                        self.check_if_variable_exists_in_res6.append("$r" + str(i))

                for i in range(1,10):
                    if '$v' + str(i) in self.check_res7:
                        self.check_if_variable_exists_in_res7.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res7:
                        self.check_if_variable_exists_in_res7.append("$r" + str(i))


                for i in range(1,10):
                    if '$v' + str(i) in self.check_res8:
                        self.check_if_variable_exists_in_res8.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res8:
                        self.check_if_variable_exists_in_res8.append("$r" + str(i))


                for i in range(1,10):
                    if '$v' + str(i) in self.check_res9:
                        self.check_if_variable_exists_in_res9.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res9:
                        self.check_if_variable_exists_in_res9.append("$r" + str(i))


                for i in range(1,10):
                    if '$v' + str(i) in self.check_res10:
                        self.check_if_variable_exists_in_res10.append("$v" + str(i))
                    elif '$r' + str(i) in self.check_res10:
                        self.check_if_variable_exists_in_res10.append("$r" + str(i))



                self.check_lists_joined = self.check_if_variable_exists_in_res1 + self.check_if_variable_exists_in_res2 + self.check_if_variable_exists_in_res3 \
                                          + self.check_if_variable_exists_in_res4 + self.check_if_variable_exists_in_res5 + self.check_if_variable_exists_in_res6 \
                                          + self.check_if_variable_exists_in_res7 + self.check_if_variable_exists_in_res8 + self.check_if_variable_exists_in_res9 + self.check_if_variable_exists_in_res10

                self.check_lists_joined = list(dict.fromkeys(self.check_lists_joined ))

                for i in range(1, 10):
                    if '$v' + str(i) in self.check_lists_joined:
                        self.max_var_in_formula += 1
                    if '$r' + str(i) in self.check_lists_joined:
                        self.max_res_in_formula += 1
                #print(self.check_lists_joined, self.max_var_in_formula, self.max_res_in_formula)
                #print(self.check_var5)



                if '$v1' in self.check_lists_joined:
                    if self.check_var1 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 1 passen nicht zusammen!")
                if '$v2' in self.check_lists_joined:
                    if self.check_var2 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 2 passen nicht zusammen!")
                if '$v3' in self.check_lists_joined:
                    if self.check_var3 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 3 passen nicht zusammen!")
                if '$v4' in self.check_lists_joined:
                    if self.check_var4 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 4 passen nicht zusammen!")
                if '$v5' in self.check_lists_joined:
                    if self.check_var5 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 5 passen nicht zusammen!")
                if '$v6' in self.check_lists_joined:
                    if self.check_var6 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 6 passen nicht zusammen!")
                if '$v7' in self.check_lists_joined:
                    if self.check_var7 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 7 passen nicht zusammen!")
                if '$v8' in self.check_lists_joined:
                    if self.check_var8 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 8 passen nicht zusammen!")
                if '$v9' in self.check_lists_joined:
                    if self.check_var9 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 9 passen nicht zusammen!")
                if '$v10' in self.check_lists_joined:
                    if self.check_var10 == " ":
                        print(sheet.cell_value(k, 3) + " ----> Formel und Variable 10 passen nicht zusammen!")
                #print()


                if self.max_var_in_formula == 0:
                    if self.check_var1 != " " or self.check_var2 != " " or self.check_var3 != " " or self.check_var4 != " " or self.check_var5 != " " or self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("0 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 1:
                    if  self.check_var2 != " " or self.check_var3 != " " or self.check_var4 != " " or self.check_var5 != " " or self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("1 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 2:
                    if  self.check_var3 != " " or self.check_var4 != " " or self.check_var5 != " " or self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("2 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 3:
                    if  self.check_var4 != " " or self.check_var5 != " " or self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("3 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 4:
                    if  self.check_var5 != " " or self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("4 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 5:
                    if  self.check_var6 != " " or self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("5 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 6:
                    if  self.check_var7 != " " or self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("6 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 7:
                    if  self.check_var8 != " " or self.check_var9 != " " or self.check_var10 != " ":
                        print("7 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 8:
                    if  self.check_var9 != " " or self.check_var10 != " ":
                        print("8 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")
                if self.max_var_in_formula == 9:
                    if  self.check_var10 != " ":
                        print("9 " + sheet.cell_value(k, 3) + " ----> Anzahl deklarierter Variablen ist zu hoch. Formel beinhaltet nicht alle deklarierten Variablen!")

        print("...done")
        #query = ("SELECT question_difficulty, question_category, question_type, question_title, question_description_title,question_description_main")

        # Closing workbook
        excel.close()

    def ilias_test_to_sql_import(self):
        #try:
        import_ilias_test_file.Import_ilias_test_file.__init__(self)

        #except:
        #    print("Modul nicht vorhanden!")



    def open_image(self):
        #global file_image  # needs to be global to print Image to Desktop
        #global filename_label
        #global file_image_label


        try:
            app.filename = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.picture_name = app.filename
            self.sorted_picture_name = self.picture_name
            self.last_char_index = self.sorted_picture_name.rfind("/")
            self.foo = ([pos for pos, char in enumerate(self.sorted_picture_name) if char == '/'])
            self.foo_len = len(self.foo)
            self.picture_name_new = self.sorted_picture_name[self.foo[self.foo_len - 1] + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new = self.picture_name[-4:]

            self.filename_label = Label(self.frame_picture, text=self.picture_name_new)
            self.filename_label.grid(row=0, column=0, sticky=W)

            self.file_image = ImageTk.PhotoImage(Image.open(app.filename).resize((250, 250)))
            self.file_image_label = Label(self.frame_picture, image=self.file_image)
            self.file_image_label.image = self.file_image
            self.file_image_label.grid(row=1, column=0)
        except:
            print("Error2")


    def delete_image(self):
        self.filename_label.grid_remove()
        self.file_image_label.grid_remove()
        self.picture_name ="EMPTY"



    #def save_image_to_db(self):
        #print("SAVE_to_IMG called")
        #conn = sqlite3.connect('ilias_questions_db.db')
        #c = conn.cursor()
        #self.img_name = self.app_filename
        #print("img1" + self.img_name)
        #self.s = self.img_name
        #self.last_char_index = self.s.rfind("/")
        #print(self.s)
        #self.foo = ([pos for pos, char in enumerate(self.s) if char == '/'])
        #print(self.foo)
        #print(len(self.s))
        #self.foo_len = len(self.foo)
       # print("NEW TRY")
        #self.img_name_new = self.s[self.foo[self.foo_len-1]+1:]
        #with open(self.img_name, 'rb') as f:
        #    self.img_data = f.read()
        #c.execute("""
        #    INSERT INTO my_table (img_name, img_data) VALUES (?,?)""", (self.img_name_new, self.img_data))
        #conn.commit()
        #conn.close()


    def show_img_from_db(self):



        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        records = c.execute("""
            SELECT *, oid FROM my_table
        """)


        for record in records:

            if str(record[len(record) - 1]) == self.create_formelfrage_entry.get():


                self.rec_data = record[147]  #record[147] -> img_data_raw (as byte)

                if self.rec_data == "EMPTY":
                    print("No Picture available")
                    self.db_file_image_label.grid_forget()
                else:

                    #Picture need to have the name"il_0_mob_xxxxxxx" for ilias to work
                    with open('il_0_mob_TEST.png', 'wb') as image_file:
                        image_file.write(self.rec_data)


                    self.picture_name = "il_0_mob_TEST.png"
                    self.db_file_image = ImageTk.PhotoImage(Image.open(self.picture_name).resize((250, 250)))
                    self.db_file_image_label = Label(self.frame_db_picture, image=self.db_file_image)
                    self.db_file_image_label.image = self.db_file_image
                    self.db_file_image_label.grid(row=2, column=0)

        conn.commit()
        conn.close()


    def filter_database(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        self.search_term_difficulty = self.searchbox_question_difficulty.get()
        self.search_term_category = self.searchbox_question_category.get()
        self.search_term_type = self.searchbox_question_type.get()

        Database.clear_listboxes(self)

        for record in records:

            if self.search_term_difficulty != "":
                if record[0].lower() == self.search_term_difficulty.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_category != "":
                if record[1].lower() == self.search_term_category.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_type != "":
                if record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_category != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[1].lower() == self.search_term_category.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_type != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_category != "" and self.search_term_type != "":
                if record[1].lower() == self.search_term_category.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            elif self.search_term_difficulty != "" and self.search_term_category != "" and self.search_term_type != "":
                if record[0].lower() == self.search_term_difficulty.lower() and record[1].lower() == self.search_term_category.lower() and record[2].lower() == self.search_term_type.lower():
                    Database.insert_to_database(self, record)

            else:
                Database.show_records(self)

        conn.commit()
        conn.close()

    def clear_listboxes(self):
        self.my_listbox_question_difficulty.delete(0, END)
        self.my_listbox_question_category.delete(0, END)
        self.my_listbox_question_type.delete(0, END)

        self.my_listbox_question_title.delete(0, END)
        self.my_listbox_question_description_title.delete(0, END)
        self.my_listbox_question_description_main.delete(0, END)

        self.my_listbox_res1_formula.delete(0, END)
        self.my_listbox_res2_formula.delete(0, END)
        self.my_listbox_res3_formula.delete(0, END)

        self.my_listbox_var1_name.delete(0, END)
        self.my_listbox_var1_min.delete(0, END)
        self.my_listbox_var1_max.delete(0, END)
        self.my_listbox_var1_prec.delete(0, END)
        self.my_listbox_var1_divby.delete(0, END)
        self.my_listbox_var1_unit.delete(0, END)

        self.my_listbox_var2_name.delete(0, END)
        self.my_listbox_var2_min.delete(0, END)
        self.my_listbox_var2_max.delete(0, END)
        self.my_listbox_var2_prec.delete(0, END)
        self.my_listbox_var2_divby.delete(0, END)
        self.my_listbox_var2_unit.delete(0, END)

        self.my_listbox_var3_name.delete(0, END)
        self.my_listbox_var3_min.delete(0, END)
        self.my_listbox_var3_max.delete(0, END)
        self.my_listbox_var3_prec.delete(0, END)
        self.my_listbox_var3_divby.delete(0, END)
        self.my_listbox_var3_unit.delete(0, END)

        self.my_listbox_var4_name.delete(0, END)
        self.my_listbox_var4_min.delete(0, END)
        self.my_listbox_var4_max.delete(0, END)
        self.my_listbox_var4_prec.delete(0, END)
        self.my_listbox_var4_divby.delete(0, END)
        self.my_listbox_var4_unit.delete(0, END)

        self.my_listbox_var5_name.delete(0, END)
        self.my_listbox_var5_min.delete(0, END)
        self.my_listbox_var5_max.delete(0, END)
        self.my_listbox_var5_prec.delete(0, END)
        self.my_listbox_var5_divby.delete(0, END)
        self.my_listbox_var5_unit.delete(0, END)

        self.my_listbox_var6_name.delete(0, END)
        self.my_listbox_var6_min.delete(0, END)
        self.my_listbox_var6_max.delete(0, END)
        self.my_listbox_var6_prec.delete(0, END)
        self.my_listbox_var6_divby.delete(0, END)
        self.my_listbox_var6_unit.delete(0, END)

        self.my_listbox_var7_name.delete(0, END)
        self.my_listbox_var7_min.delete(0, END)
        self.my_listbox_var7_max.delete(0, END)
        self.my_listbox_var7_prec.delete(0, END)
        self.my_listbox_var7_divby.delete(0, END)
        self.my_listbox_var7_unit.delete(0, END)

        self.my_listbox_res1_name.delete(0, END)
        self.my_listbox_res1_min.delete(0, END)
        self.my_listbox_res1_max.delete(0, END)
        self.my_listbox_res1_prec.delete(0, END)
        self.my_listbox_res1_tol.delete(0, END)
        self.my_listbox_res1_points.delete(0, END)
        self.my_listbox_res1_unit.delete(0, END)

        self.my_listbox_res2_name.delete(0, END)
        self.my_listbox_res2_min.delete(0, END)
        self.my_listbox_res2_max.delete(0, END)
        self.my_listbox_res2_prec.delete(0, END)
        self.my_listbox_res2_tol.delete(0, END)
        self.my_listbox_res2_points.delete(0, END)
        self.my_listbox_res2_unit.delete(0, END)

        self.my_listbox_res3_name.delete(0, END)
        self.my_listbox_res3_min.delete(0, END)
        self.my_listbox_res3_max.delete(0, END)
        self.my_listbox_res3_prec.delete(0, END)
        self.my_listbox_res3_tol.delete(0, END)
        self.my_listbox_res3_points.delete(0, END)
        self.my_listbox_res3_unit.delete(0, END)

        self.my_listbox_img_name.delete(0, END)
        self.my_listbox_img_data.delete(0, END)

        self.my_listbox_test_time.delete(0, END)
        self.my_listbox_oid.delete(0, END)

    def insert_to_database(self, record):

        self.my_listbox_question_difficulty.insert(END, record[0])
        self.my_listbox_question_category.insert(END, record[1])
        self.my_listbox_question_type.insert(END, record[2])

        self.my_listbox_question_title.insert(END, record[3])
        self.my_listbox_question_description_title.insert(END, record[4])
        self.my_listbox_question_description_main.insert(END, record[5])

        self.my_listbox_res1_formula.insert(END, record[6])
        self.my_listbox_res2_formula.insert(END, record[7])
        self.my_listbox_res3_formula.insert(END, record[8])
        # self.my_listbox_res4_formula.insert(END, record[9])
        # self.my_listbox_res5_formula.insert(END, record[10])
        # self.my_listbox_res6_formula.insert(END, record[11])
        # self.my_listbox_res7_formula.insert(END, record[12])
        # self.my_listbox_res8_formula.insert(END, record[13])
        # self.my_listbox_res9_formula.insert(END, record[14])
        # self.my_listbox_res10_formula.insert(END, record[15])

        self.my_listbox_var1_name.insert(END, record[16])
        self.my_listbox_var1_min.insert(END, record[17])
        self.my_listbox_var1_max.insert(END, record[18])
        self.my_listbox_var1_prec.insert(END, record[19])
        self.my_listbox_var1_divby.insert(END, record[20])
        self.my_listbox_var1_unit.insert(END, record[21])

        self.my_listbox_var2_name.insert(END, record[22])
        self.my_listbox_var2_min.insert(END, record[23])
        self.my_listbox_var2_max.insert(END, record[24])
        self.my_listbox_var2_prec.insert(END, record[25])
        self.my_listbox_var2_divby.insert(END, record[26])
        self.my_listbox_var2_unit.insert(END, record[27])

        self.my_listbox_var3_name.insert(END, record[28])
        self.my_listbox_var3_min.insert(END, record[29])
        self.my_listbox_var3_max.insert(END, record[30])
        self.my_listbox_var3_prec.insert(END, record[31])
        self.my_listbox_var3_divby.insert(END, record[32])
        self.my_listbox_var3_unit.insert(END, record[33])

        self.my_listbox_var4_name.insert(END, record[34])
        self.my_listbox_var4_min.insert(END, record[35])
        self.my_listbox_var4_max.insert(END, record[36])
        self.my_listbox_var4_prec.insert(END, record[37])
        self.my_listbox_var4_divby.insert(END, record[38])
        self.my_listbox_var4_unit.insert(END, record[39])

        self.my_listbox_var5_name.insert(END, record[40])
        self.my_listbox_var5_min.insert(END, record[41])
        self.my_listbox_var5_max.insert(END, record[42])
        self.my_listbox_var5_prec.insert(END, record[43])
        self.my_listbox_var5_divby.insert(END, record[44])
        self.my_listbox_var5_unit.insert(END, record[45])

        self.my_listbox_var6_name.insert(END, record[46])
        self.my_listbox_var6_min.insert(END, record[47])
        self.my_listbox_var6_max.insert(END, record[48])
        self.my_listbox_var6_prec.insert(END, record[49])
        self.my_listbox_var6_divby.insert(END, record[50])
        self.my_listbox_var6_unit.insert(END, record[51])

        self.my_listbox_var7_name.insert(END, record[52])
        self.my_listbox_var7_min.insert(END, record[53])
        self.my_listbox_var7_max.insert(END, record[54])
        self.my_listbox_var7_prec.insert(END, record[55])
        self.my_listbox_var7_divby.insert(END, record[56])
        self.my_listbox_var7_unit.insert(END, record[57])

        self.my_listbox_res1_name.insert(END, record[76])
        self.my_listbox_res1_min.insert(END, record[77])
        self.my_listbox_res1_max.insert(END, record[78])
        self.my_listbox_res1_prec.insert(END, record[79])
        self.my_listbox_res1_tol.insert(END, record[80])
        self.my_listbox_res1_points.insert(END, record[81])
        self.my_listbox_res1_unit.insert(END, record[82])

        self.my_listbox_res2_name.insert(END, record[83])
        self.my_listbox_res2_min.insert(END, record[84])
        self.my_listbox_res2_max.insert(END, record[85])
        self.my_listbox_res2_prec.insert(END, record[86])
        self.my_listbox_res2_tol.insert(END, record[87])
        self.my_listbox_res2_points.insert(END, record[88])
        self.my_listbox_res2_unit.insert(END, record[89])

        self.my_listbox_res3_name.insert(END, record[90])
        self.my_listbox_res3_min.insert(END, record[91])
        self.my_listbox_res3_max.insert(END, record[92])
        self.my_listbox_res3_prec.insert(END, record[93])
        self.my_listbox_res3_tol.insert(END, record[94])
        self.my_listbox_res3_points.insert(END, record[95])
        self.my_listbox_res3_unit.insert(END, record[96])

        self.my_listbox_img_name.insert(END, record[146])
        # self.my_listbox_img_data.insert(END, record[147])
        # img_data slows "show records" down, therefore not inserted

        self.my_listbox_test_time.insert(END, record[148])
        self.my_listbox_oid.insert(END, record[len(record) - 1])

#class LatexPreview(Formelfrage):
#
#    def __init__(self):
#        self.latex_preview_window = Toplevel()
#        self.latex_frame = LabelFrame(self.latex_preview_window, text="LaTeX-Preview", padx=5, pady=5)
#        self.latex_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

#        self.latex_textblock_1_label = Label(self.latex_frame, text="Textblock 1:", width=40)
#        self.latex_textblock_1_label.grid(row=0, column=0, pady=(10, 0))
#        self.latex_textblock_1_entry = Entry(self.latex_frame, width=60)
#        self.latex_textblock_1_entry.grid(row=1, column=0)

#        self.latex_formelblock_1_label = Label(self.latex_frame, text="Formelblock 1:", width=40)
#        self.latex_formelblock_1_label.grid(row=2, column=0, pady=(10, 0))
#        self.latex_formelblock_1_entry = Entry(self.latex_frame, width=60)
#        self.latex_formelblock_1_entry.grid(row=3, column=0)

#        self.latex_textblock_2_label = Label(self.latex_frame, text="Textblock 2:", width=40)
#        self.latex_textblock_2_label.grid(row=4, column=0, pady=(10, 0))
#        self.latex_textblock_2_entry = Entry(self.latex_frame, width=60)
#        self.latex_textblock_2_entry.grid(row=5, column=0)

#        self.latex_formelblock_2_label = Label(self.latex_frame, text="Formelblock 2:", width=40)
#        self.latex_formelblock_2_label.grid(row=6, column=0, pady=(10, 0))
#        self.latex_formelblock_2_entry = Entry(self.latex_frame, width=60)
#        self.latex_formelblock_2_entry.grid(row=7, column=0)

#        self.latex_preview_btn = Button(self.latex_frame, text="show LaTeX preview", command=lambda: LatexPreview.show_latex_preview(self))
#        self.latex_preview_btn.grid(row=10, ipadx=100, pady=10)

#        self.latex_preview_btn = Button(self.latex_frame, text="clear LaTeX preview",command=lambda: LatexPreview.clear_latex_preview(self))
#        self.latex_preview_btn.grid(row=11, ipadx=100, pady=10)



#    def show_latex_preview(self):
#        self.latex = r"{\text{" + str(self.latex_textblock_1_entry.get()) +"}}\ {"+ str(self.latex_formelblock_1_entry.get()) + "}\ {\\text{" + str(self.latex_textblock_2_entry.get()) + "}}\ {" + str(self.latex_formelblock_2_entry.get()) + "}"
#        self.expr = r'$$' + self.latex + '$$'
#        preview(self.expr, viewer='file', filename='LaTeX-Preview.png')

#        self.file_image = ImageTk.PhotoImage(Image.open('LaTeX-Preview.png'))
#        self.file_image_label = Label(self.latex_preview_window, image=self.file_image)
#        self.file_image_label.image = self.file_image

#        self.file_image_label.grid(row=20, column=0, pady=20)

#    def clear_latex_preview(self):
#        self.file_image_label.grid_forget()





class create_formelfrage(Formelfrage):

    def __init__(self):

        self.mytree = ET.parse(self.tst_file_path_read)
        self.myroot = self.mytree.getroot()

        for title in self.myroot.iter('Title'):
            title.text = self.test_title_entry.get()
            title.text = title.text.replace('&', "&amp;")

            if title.text == "":
                title.text = "DEFAULT"

        self.mytree.write(self.tst_file_path_write)



        # ----------------------------------- Datei .xml Einlesen
       
        self.mytree = ET.parse(self.qti_file_path_read)
        self.myroot = self.mytree.getroot()

        self.frame_create = LabelFrame(self.formula_tab, text="Create Formelfrage", padx=5, pady=5)
        self.frame_create.grid(row=1, column=2)

        self.entry_split = self.create_formelfrage_entry.get()
        self.entry_split = self.entry_split.split(",")

        #print(self.entry_split[0])
        #print(len(self.entry_split))

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()


        for x in range(len(self.entry_split)):
            for record in records:
                if str(record[len(record) - 1]) == self.entry_split[x]:

                    if record[2].lower() == "formelfrage":

                        self.question_difficulty = str(record[0])
                        self.question_category = str(record[1])
                        self.question_type = str(record[2])
                        self.question_title = str(record[3])
                        self.question_description_title = str(record[4])

                        self.question_type = self.question_type.replace('&', "&amp;")
                        self.question_title = self.question_title.replace('&', "&amp;")
                        self.question_description_title = self.question_description_title.replace('&', "&amp;")

                        self.question_description_main_raw = str(record[5])
                        self.index_list = []


                        if self.var_use_latex_on_text_check.get() == 0:
                            for i in range(1, len(self.question_description_main_raw)):
                                if self.question_description_main_raw[i] == '_':
                                    self.position_begin = i
                                    self.position_end = self.question_description_main_raw.find(" ", self.position_begin)
                                    self.index_list.append(self.position_end)
                                    self.question_description_main_raw= self.question_description_main_raw[:self.position_end] + ' </sub>' + self.question_description_main_raw[self.position_end:]
                            #print(self.question_description_main_raw)
                            for i in range(1, len(self.question_description_main_raw)):
                                if self.question_description_main_raw[i] == '^':
                                    self.position_begin = i
                                    self.position_end = self.question_description_main_raw.find(" ", self.position_begin)
                                    self.index_list.append(self.position_end)
                                    self.question_description_main_raw = self.question_description_main_raw[:self.position_end] + ' </sup>' + self.question_description_main_raw[self.position_end:]
                            #print(self.question_description_main_raw)


                            self.question_description_main_symbol_replaced = self.question_description_main_raw.replace('&', "&amp;")
                            self.question_description_main_multi_replaced = self.question_description_main_symbol_replaced.replace('\n', "&lt;/p&gt;&#13;&#10;&lt;p&gt;")
                            self.question_description_main_test = self.question_description_main_multi_replaced
                            self.question_description_main_latex_start = self.question_description_main_test.replace('\\)', " </span>")
                            self.question_description_main_latex_end = self.question_description_main_latex_start.replace('\\(', "<span class=\"latex\">")
                            self.question_description_main_sup = self.question_description_main_latex_end.replace('^', "<sup>")
                            #self.question_description_main_sup_end = self.question_description_main_sup_start.replace('</p>', "</sup>")
                            self.question_description_main_sub = self.question_description_main_sup.replace('_', "<sub>")
                            #self.question_description_main_sub_end = self.question_description_main_sub_start.replace('</b>', "</sub>")
                            self.question_description_main_italic_end = self.question_description_main_sub.replace('///', "</i> ")
                            self.question_description_main_italic_start = self.question_description_main_italic_end.replace('//', "<i>")
                            self.question_description_main_var_uppercase = self.question_description_main_italic_start.replace('$V', "$v")
                            self.question_description_main_res_uppercase = self.question_description_main_var_uppercase.replace('$R', "$r")

                            self.question_description_main = self.question_description_main_res_uppercase


                        elif self.var_use_latex_on_text_check.get() == 1:
                            self.question_description_main_symbol_replaced = self.question_description_main_raw.replace('&', "&amp;")
                            self.question_description_main_multi_replaced = self.question_description_main_symbol_replaced.replace('\n', "&lt;/p&gt;&#13;&#10;&lt;p&gt;")
                            self.question_description_main_test = self.question_description_main_multi_replaced
                            self.question_description_main_latex_start = self.question_description_main_test.replace('\\)', " </span>")
                            self.question_description_main_latex_end = self.question_description_main_latex_start.replace('\\(', "<span class=\"latex\">")
                            self.question_description_main = self.question_description_main_latex_end


                        self.res1_formula = str(record[6])
                        self.res1_formula_length = str(len(self.res1_formula))
                        self.res2_formula = str(record[7])
                        self.res2_formula_length = str(len(self.res2_formula))
                        self.res3_formula = str(record[8])
                        self.res3_formula_length = str(len(self.res3_formula))
                        self.res4_formula = str(record[9])
                        self.res4_formula_length = str(len(self.res4_formula))
                        self.res5_formula = str(record[10])
                        self.res5_formula_length = str(len(self.res5_formula))
                        self.res6_formula = str(record[11])
                        self.res6_formula_length = str(len(self.res6_formula))
                        self.res7_formula = str(record[12])
                        self.res7_formula_length = str(len(self.res7_formula))
                        self.res8_formula = str(record[13])
                        self.res8_formula_length = str(len(self.res8_formula))
                        self.res9_formula = str(record[14])
                        self.res9_formula_length = str(len(self.res9_formula))
                        self.res10_formula = str(record[15])
                        self.res10_formula_length = str(len(self.res10_formula))

                        self.var1_name = str(record[16])
                        self.var1_min = str(record[17])
                        self.var1_max = str(record[18])
                        self.var1_prec = str(record[19])
                        self.var1_divby = str(record[20])
                        self.var1_divby_length = str(len(self.var1_divby))
                        self.var1_unit = str(record[21])
                        self.var1_unit_length = str(len(self.var1_unit))

                        self.var2_name = str(record[22])
                        self.var2_min = str(record[23])
                        self.var2_max = str(record[24])
                        self.var2_prec = str(record[25])
                        self.var2_divby = str(record[26])
                        self.var2_divby_length = str(len(self.var2_divby))
                        self.var2_unit = str(record[27])
                        self.var2_unit_length = str(len(self.var2_unit))

                        self.var3_name = str(record[28])
                        self.var3_min = str(record[29])
                        self.var3_max = str(record[30])
                        self.var3_prec = str(record[31])
                        self.var3_divby = str(record[32])
                        self.var3_divby_length = str(len(self.var3_divby))
                        self.var3_unit = str(record[33])
                        self.var3_unit_length = str(len(self.var3_unit))

                        self.var4_name = str(record[34])
                        self.var4_min = str(record[35])
                        self.var4_max = str(record[36])
                        self.var4_prec = str(record[37])
                        self.var4_divby = str(record[38])
                        self.var4_divby_length = str(len(self.var4_divby))
                        self.var4_unit = str(record[39])
                        self.var4_unit_length = str(len(self.var4_unit))

                        self.var5_name = str(record[40])
                        self.var5_min = str(record[41])
                        self.var5_max = str(record[42])
                        self.var5_prec = str(record[43])
                        self.var5_divby = str(record[44])
                        self.var5_divby_length = str(len(self.var5_divby))
                        self.var5_unit = str(record[45])
                        self.var5_unit_length = str(len(self.var5_unit))

                        self.var6_name = str(record[46])
                        self.var6_min = str(record[47])
                        self.var6_max = str(record[48])
                        self.var6_prec = str(record[49])
                        self.var6_divby = str(record[50])
                        self.var6_divby_length = str(len(self.var6_divby))
                        self.var6_unit = str(record[51])
                        self.var6_unit_length = str(len(self.var6_unit))

                        self.var7_name = str(record[52])
                        self.var7_min = str(record[53])
                        self.var7_max = str(record[54])
                        self.var7_prec = str(record[55])
                        self.var7_divby = str(record[56])
                        self.var7_divby_length = str(len(self.var7_divby))
                        self.var7_unit = str(record[57])
                        self.var7_unit_length = str(len(self.var7_unit))

                        self.var8_name = str(record[58])
                        self.var8_min = str(record[59])
                        self.var8_max = str(record[60])
                        self.var8_prec = str(record[61])
                        self.var8_divby = str(record[62])
                        self.var8_divby_length = str(len(self.var7_divby))
                        self.var8_unit = str(record[63])
                        self.var8_unit_length = str(len(self.var7_unit))

                        self.var9_name = str(record[64])
                        self.var9_min = str(record[65])
                        self.var9_max = str(record[66])
                        self.var9_prec = str(record[67])
                        self.var9_divby = str(record[68])
                        self.var9_divby_length = str(len(self.var7_divby))
                        self.var9_unit = str(record[69])
                        self.var9_unit_length = str(len(self.var7_unit))

                        self.var10_name = str(record[70])
                        self.var10_min = str(record[71])
                        self.var10_max = str(record[72])
                        self.var10_prec = str(record[73])
                        self.var10_divby = str(record[74])
                        self.var10_divby_length = str(len(self.var7_divby))
                        self.var10_unit = str(record[75])
                        self.var10_unit_length = str(len(self.var7_unit))

                        self.res1_name = str(record[76])
                        self.res1_min = str(record[77])
                        self.res1_min_length = str(len(self.res1_min))
                        self.res1_max = str(record[78])
                        self.res1_max_length = str(len(self.res1_max))
                        self.res1_prec = str(record[79])
                        self.res1_tol = str(record[80])
                        self.res1_tol_length = str(len(self.res1_tol))
                        self.res1_points = str(record[81])
                        self.res1_unit = str(record[82])
                        self.res1_unit_length = str(len(self.res1_unit))


                        self.res2_name = str(record[83])
                        self.res2_min = str(record[84])
                        self.res2_min_length = str(len(self.res2_min))
                        self.res2_max = str(record[85])
                        self.res2_max_length = str(len(self.res2_max))
                        self.res2_prec = str(record[86])
                        self.res2_tol = str(record[87])
                        self.res2_tol_length = str(len(self.res2_tol))
                        self.res2_points = str(record[88])
                        self.res2_unit = str(record[89])
                        self.res2_unit_length = str(len(self.res2_unit))


                        self.res3_name = str(record[90])
                        self.res3_min = str(record[91])
                        self.res3_min_length = str(len(self.res3_min))
                        self.res3_max = str(record[92])
                        self.res3_max_length = str(len(self.res3_max))
                        self.res3_prec = str(record[93])
                        self.res3_tol = str(record[94])
                        self.res3_tol_length = str(len(self.res3_tol))
                        self.res3_points = str(record[95])
                        self.res3_unit = str(record[96])
                        self.res3_unit_length = str(len(self.res3_unit))

                        self.res4_name = str(record[97])
                        self.res4_min = str(record[98])
                        self.res4_min_length = str(len(self.res4_min))
                        self.res4_max = str(record[99])
                        self.res4_max_length = str(len(self.res4_max))
                        self.res4_prec = str(record[100])
                        self.res4_tol = str(record[101])
                        self.res4_tol_length = str(len(self.res4_tol))
                        self.res4_points = str(record[102])
                        self.res4_unit = str(record[103])
                        self.res4_unit_length = str(len(self.res4_unit))

                        self.res5_name = str(record[104])
                        self.res5_min = str(record[105])
                        self.res5_min_length = str(len(self.res5_min))
                        self.res5_max = str(record[106])
                        self.res5_max_length = str(len(self.res5_max))
                        self.res5_prec = str(record[107])
                        self.res5_tol = str(record[108])
                        self.res5_tol_length = str(len(self.res5_tol))
                        self.res5_points = str(record[109])
                        self.res5_unit = str(record[110])
                        self.res5_unit_length = str(len(self.res5_unit))

                        self.res6_name = str(record[111])
                        self.res6_min = str(record[112])
                        self.res6_min_length = str(len(self.res6_min))
                        self.res6_max = str(record[113])
                        self.res6_max_length = str(len(self.res6_max))
                        self.res6_prec = str(record[114])
                        self.res6_tol = str(record[115])
                        self.res6_tol_length = str(len(self.res6_tol))
                        self.res6_points = str(record[116])
                        self.res6_unit = str(record[117])
                        self.res6_unit_length = str(len(self.res6_unit))

                        self.res7_name = str(record[118])
                        self.res7_min = str(record[119])
                        self.res7_min_length = str(len(self.res7_min))
                        self.res7_max = str(record[120])
                        self.res7_max_length = str(len(self.res7_max))
                        self.res7_prec = str(record[121])
                        self.res7_tol = str(record[122])
                        self.res7_tol_length = str(len(self.res7_tol))
                        self.res7_points = str(record[123])
                        self.res7_unit = str(record[124])
                        self.res7_unit_length = str(len(self.res7_unit))

                        self.res8_name = str(record[125])
                        self.res8_min = str(record[126])
                        self.res8_min_length = str(len(self.res8_min))
                        self.res8_max = str(record[127])
                        self.res8_max_length = str(len(self.res8_max))
                        self.res8_prec = str(record[128])
                        self.res8_tol = str(record[129])
                        self.res8_tol_length = str(len(self.res8_tol))
                        self.res8_points = str(record[130])
                        self.res8_unit = str(record[131])
                        self.res8_unit_length = str(len(self.res8_unit))

                        self.res9_name = str(record[132])
                        self.res9_min = str(record[133])
                        self.res9_min_length = str(len(self.res9_min))
                        self.res9_max = str(record[134])
                        self.res9_max_length = str(len(self.res9_max))
                        self.res9_prec = str(record[135])
                        self.res9_tol = str(record[136])
                        self.res9_tol_length = str(len(self.res9_tol))
                        self.res9_points = str(record[137])
                        self.res9_unit = str(record[138])
                        self.res9_unit_length = str(len(self.res9_unit))

                        self.res10_name = str(record[139])
                        self.res10_min = str(record[140])
                        self.res10_min_length = str(len(self.res10_min))
                        self.res10_max = str(record[141])
                        self.res10_max_length = str(len(self.res10_max))
                        self.res10_prec = str(record[142])
                        self.res10_tol = str(record[143])
                        self.res10_tol_length = str(len(self.res10_tol))
                        self.res10_points = str(record[144])
                        self.res10_unit = str(record[145])
                        self.res10_unit_length = str(len(self.res10_unit))

                        self.img_name = str(record[146])
                        self.img_data_raw = record[147]
                        self.img_data = str(record[147])

                        self.test_time = str(record[148])

                        self.oid = str(record[len(record)-1]) #oid ist IMMER letztes Fach
                        
                        # "x"ist die ID-Nummer welche im Eingabefeld eingegeben wurde
                        create_formelfrage.create_question(self, x)  #
                        print("Formelfrage generated with Title --> \"" + self.question_title + "\"" )

                        print("\n")


                    elif record[2].lower() == "multiple choice":
                        print("Question type with 'multiple choice' found")
                        create_multiplechoice.create_mc_question(MultipleChoice,self.mytree, self.myroot, self.qti_file_path_read, self.qti_file_path_write, self.entry_split, x)

                    else:
                        #record[2].lower() != "formelfrage" or record[2].lower() != "multiple choice":
                        print("ERROR: FRAGENTEST KANN NICHT ERSTELLT WERDEN! --> Aufgabe ohne \"formelfrage\" bzw. \"multiple choice\"-Eintrag gefunden")
                # create_formelfrage.create_question(self, x)   LAST CHANGE
        conn.commit()
        conn.close()

        print("Testfragen geschrieben")


    def create_question(self, x):
        # print("IN CREATE QUESTION")
        # print(Formelfrage.unit_table(self, self.var1_unit_myCombo.get()))
        # print(self.var1_unit_myCombo.get())
        # print("IN CREATE QUESTION")

        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Error: Creating directory. ' + directory)




        for record in records:

            #Ohne If Abfrage werden ALLE Fragen aus der Datenbank erstellt
            if str(record[len(record)-1]) == self.entry_split[x]:

                if self.img_data_raw != "EMPTY":
                    createFolder(self.img_file_path_create_folder + '/' + 'il_0_mob_000000' + str(x) + '/')
                    #img wird immer als PNG Datei abgelegt.
                    with open(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png", 'wb') as image_file:
                        image_file.write(self.img_data_raw)

                    self.image = Image.open(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")
                    self.image.save(self.img_file_path + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")





                # print("q_titel: " + str(self.question_title))

                # cast int from len() function to string! cant use int in concatenated string
                # the string is used down below in "SOLUTION STRING"

                r1_rating = "0"
                r1_rating_length = len(r1_rating)
                # print(r1_rating_length)

                r1_unit = ""
                r1_unit_length = len(r1_unit)
                # print(r1_unit_length)

                r1_unitvalue = ""
                r1_unitv_length = len(r1_unitvalue)
                # print(r1_unitv_length)

                r1_resultunits = ""
                r1_resultu_length = len(r1_resultunits)
                # print(r1_resultu_length)

                question_name = str(self.question_title)

                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
                item = ET.SubElement(section, 'item')
                item.set('ident', "il_0_qst_000000")
                item.set('title', question_name)
                qticomment = ET.SubElement(item, 'qticomment')
                qticomment.text = self.question_description_title
                duration = ET.SubElement(item, 'duration')
                duration.text = self.test_time


                # append ITEM in the last "myroot"-Element. Here it is Element "section" in myroot
                self.myroot[0][len(self.myroot[0])-1].append(item)



                if duration.text == "":
                    duration.text = "P0Y0M0DT1H0M0S"


                for assessment in self.myroot.iter('assessment'):

                    self.title_replaced = str(self.test_title_entry.get())
                    assessment.set('title',self.title_replaced.replace('&', "&amp;"))

                    if assessment.get('title') == "":
                        assessment.set('title', "DEFAULT")


                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                presentation.set('label', question_name)
                flow = ET.SubElement(presentation, 'flow')
                material = ET.SubElement(flow, 'material')

                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/html")

                if self.img_data != "EMPTY":
                    #mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_0000000\" width=\"482\" /></p>"
                    mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_000000" + str(x) + "\" width=\"482\" /></p>"


                    matimage = ET.SubElement(material, 'matimage')
                    matimage.set('label', "il_0_mob_000000" + str(x))  # Object -> Filename
                    matimage.set('uri', "objects/il_0_mob_000000" + str(x) + "/" + self.img_name + ".png")


                else:
                    mattext.text = "<p>" + self.question_description_main + "</p>"  # + "<p><img height=\"378\" src=\"il_0_mob_1955056\" width=\"482\" /></p>"

                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
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
                self.autor_replaced = str(self.autor_entry.get())
                fieldentry.text = self.autor_replaced.replace('&', "&amp;")
                # -----------------------------------------------------------------------POINTS
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "points"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.res1_points)
                # -----------------------------------------------------------------------Variables and Results
                #
                # To prevent the program to crash when no units are selected for ALL variables and results
                # those will be by default selected as "H" - Henry

                if self.var1_unit == "Unit":
                    self.var1_unit = ""
                    self.var1_unit_length = len(self.var1_unit)


                if self.var2_unit == "Unit":
                    self.var2_unit = ""
                    self.var2_unit_length = len(self.var2_unit)


                if self.var3_unit == "Unit":
                    self.var3_unit = ""
                    self.var3_unit_length = len(self.var3_unit)


                if self.var4_unit == "Unit":
                    self.var4_unit = ""
                    self.var4_unit_length = len(self.var4_unit)


                if self.var5_unit == "Unit":
                    self.var5_unit = ""
                    self.var5_unit_length = len(self.var5_unit)


                if self.var6_unit == "Unit":
                    self.var6_unit = ""
                    self.var6_unit_length = len(self.var6_unit)


                if self.var7_unit == "Unit":
                    self.var7_unit = ""
                    self.var7_unit_length = len(self.var7_unit)

                if self.var8_unit == "Unit":
                    self.var8_unit = ""
                    self.var8_unit_length = len(self.var8_unit)

                if self.var9_unit == "Unit":
                    self.var9_unit = ""
                    self.var9_unit_length = len(self.var9_unit)

                if self.var10_unit == "Unit":
                    self.var10_unit = ""
                    self.var10_unit_length = len(self.var10_unit)


                if self.res1_unit == "Unit":
                    self.res1_unit = ""
                    self.res1_unit_length = len(self.res1_unit)

                if self.res2_unit == "Unit":
                    self.res2_unit = ""
                    self.res2_unit_length = len(self.res2_unit)

                if self.res3_unit == "Unit":
                    self.res3_unit = ""
                    self.res3_unit_length = len(self.res3_unit)

                if self.res4_unit == "Unit":
                    self.res4_unit = ""
                    self.res4_unit_length = len(self.res4_unit)

                if self.res5_unit == "Unit":
                    self.res5_unit = ""
                    self.res5_unit_length = len(self.res5_unit)

                if self.res6_unit == "Unit":
                    self.res6_unit = ""
                    self.res6_unit_length = len(self.res6_unit)

                if self.res7_unit == "Unit":
                    self.res7_unit = ""
                    self.res7_unit_length = len(self.res7_unit)

                if self.res8_unit == "Unit":
                    self.res8_unit = ""
                    self.res8_unit_length = len(self.res8_unit)

                if self.res9_unit == "Unit":
                    self.res9_unit = ""
                    self.res9_unit_length = len(self.res9_unit)

                if self.res10_unit == "Unit":
                    self.res10_unit = ""
                    self.res10_unit_length = len(self.res10_unit)




                # -----------------------------------------------------------------------Variable 1

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var1_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var1_unit_length) + ":\"" + self.var1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var1_unit))) + ":\"" + Formelfrage.unit_table(self, self.var1_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_1 no UNIT")
                # -----------------------------------------------------------------------Variable 2

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var2_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var2_unit_length) + ":\"" + self.var2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var2_unit))) + ":\"" + Formelfrage.unit_table(self, self.var2_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_2 no UNIT")

                # -----------------------------------------------------------------------Variable 3

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var3_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                       "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                       "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                       "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                       "s:4:\"unit\";s:" + str(self.var3_unit_length) + ":\"" + self.var3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var3_unit))) + ":\"" + Formelfrage.unit_table(self, self.var3_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_3 no UNIT")
                # -----------------------------------------------------------------------Variable 4

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var4_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var4_unit_length) + ":\"" + self.var4_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var4_unit))) + ":\"" + Formelfrage.unit_table(self, self.var4_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_4 no UNIT")
                # -----------------------------------------------------------------------Variable 5

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var5_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var5_unit_length) + ":\"" + self.var5_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var5_unit))) + ":\"" + Formelfrage.unit_table(self, self.var5_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_5 no UNIT")

                # -----------------------------------------------------------------------Variable 6

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var6_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var6_unit_length) + ":\"" + self.var6_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var6_unit))) + ":\"" + Formelfrage.unit_table(self, self.var6_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_6 no UNIT")

                # -----------------------------------------------------------------------Variable 7

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var7_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var7_unit_length) + ":\"" + self.var7_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var7_unit))) + ":\"" + Formelfrage.unit_table(self, self.var7_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_7 no UNIT")


                # -----------------------------------------------------------------------Variable 8

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v8"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var8_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var8_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var8_divby_length + ":\"" + self.var8_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var8_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var8_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var8_unit_length) + ":\"" + self.var8_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var8_unit))) + ":\"" + Formelfrage.unit_table(self, self.var8_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var8_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var8_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var8_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var8_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_8 no UNIT")

                # -----------------------------------------------------------------------Variable 9

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v9"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var9_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var9_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var9_divby_length + ":\"" + self.var9_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var9_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var9_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var9_unit_length) + ":\"" + self.var9_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var9_unit))) + ":\"" + Formelfrage.unit_table(self, self.var9_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var9_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var9_divby_length + ":\"" + self.var9_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var9_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var9_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_1 no UNIT")

            # -----------------------------------------------------------------------Variable 10

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v10"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var10_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var10_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var10_divby_length + ":\"" + self.var10_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var10_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var10_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var10_unit_length) + ":\"" + self.var10_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var10_unit))) + ":\"" + Formelfrage.unit_table(self, self.var10_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var10_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var10_divby_length + ":\"" + self.var10_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var10_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var10_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_10 no UNIT")

                # -----------------------------------------------------------------------Solution 1
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res1_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res1_unit_length) + ":\"" + self.res1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res1_unit))) + ":\"" + Formelfrage.unit_table(self, self.res1_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
                        # -----------------------------------------------------------------------Solution 2
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res2_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res2_unit_length) + ":\"" + self.res2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res2_unit))) + ":\"" + Formelfrage.unit_table(self, self.res2_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
                # -----------------------------------------------------------------------Solution 3
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res3_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res3_unit_length) + ":\"" + self.res3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res3_unit))) + ":\"" + Formelfrage.unit_table(self, self.res3_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 4
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res4_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res4_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res4_tol_length + ":\"" + self.res4_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res4_min_length + ":\"" + self.res4_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res4_max_length + ":\"" + self.res4_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res4_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res4_formula_length + ":\"" + self.res4_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res4_unit_length) + ":\"" + self.res4_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res4_unit))) + ":\"" + Formelfrage.unit_table(self, self.res4_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res4_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res4_tol_length + ":\"" + self.res4_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res4_min_length + ":\"" + self.res4_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res4_max_length + ":\"" + self.res4_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res4_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res4_formula_length + ":\"" + self.res4_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 5
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res5_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res5_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res5_tol_length + ":\"" + self.res5_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res5_min_length + ":\"" + self.res5_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res5_max_length + ":\"" + self.res5_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res5_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res5_formula_length + ":\"" + self.res5_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res5_unit_length) + ":\"" + self.res5_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res5_unit))) + ":\"" + Formelfrage.unit_table(self, self.res5_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res5_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res5_tol_length + ":\"" + self.res5_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res5_min_length + ":\"" + self.res5_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res5_max_length + ":\"" + self.res5_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res5_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res5_formula_length + ":\"" + self.res5_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 6
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res6_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res6_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res6_tol_length + ":\"" + self.res6_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res6_min_length + ":\"" + self.res6_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res6_max_length + ":\"" + self.res6_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res6_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res6_formula_length + ":\"" + self.res6_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res6_unit_length) + ":\"" + self.res6_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res6_unit))) + ":\"" + Formelfrage.unit_table(self, self.res6_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res6_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res6_tol_length + ":\"" + self.res6_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res6_min_length + ":\"" + self.res6_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res6_max_length + ":\"" + self.res6_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res6_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res6_formula_length + ":\"" + self.res6_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 7
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res7_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res7_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res7_tol_length + ":\"" + self.res7_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res7_min_length + ":\"" + self.res7_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res7_max_length + ":\"" + self.res7_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res7_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res7_formula_length + ":\"" + self.res7_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res7_unit_length) + ":\"" + self.res7_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res7_unit))) + ":\"" + Formelfrage.unit_table(self, self.res7_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res7_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res7_tol_length + ":\"" + self.res7_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res7_min_length + ":\"" + self.res7_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res7_max_length + ":\"" + self.res7_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res7_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res7_formula_length + ":\"" + self.res7_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 8
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r8"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res8_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res8_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res8_tol_length + ":\"" + self.res8_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res8_min_length + ":\"" + self.res8_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res8_max_length + ":\"" + self.res8_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res8_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res8_formula_length + ":\"" + self.res8_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res8_unit_length) + ":\"" + self.res8_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res8_unit))) + ":\"" + Formelfrage.unit_table(self, self.res8_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res8_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res8_tol_length + ":\"" + self.res8_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res8_min_length + ":\"" + self.res8_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res8_max_length + ":\"" + self.res8_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res8_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res8_formula_length + ":\"" + self.res8_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 9
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r9"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res9_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res9_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res9_tol_length + ":\"" + self.res9_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res9_min_length + ":\"" + self.res9_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res9_max_length + ":\"" + self.res9_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res9_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res9_formula_length + ":\"" + self.res9_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res9_unit_length) + ":\"" + self.res9_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res9_unit))) + ":\"" + Formelfrage.unit_table(self, self.res9_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res9_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res9_tol_length + ":\"" + self.res9_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res9_min_length + ":\"" + self.res9_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res9_max_length + ":\"" + self.res9_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res9_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res9_formula_length + ":\"" + self.res9_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 10
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r10"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res10_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res10_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res10_tol_length + ":\"" + self.res10_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res10_min_length + ":\"" + self.res10_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res10_max_length + ":\"" + self.res10_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res10_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res10_formula_length + ":\"" + self.res10_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res10_unit_length) + ":\"" + self.res10_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res10_unit))) + ":\"" + Formelfrage.unit_table(self, self.res10_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res10_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res10_tol_length + ":\"" + self.res10_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res10_min_length + ":\"" + self.res10_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res10_max_length + ":\"" + self.res10_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res10_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res10_formula_length + ":\"" + self.res10_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
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

                self.mytree.write(self.qti_file_path_write)
                print("Create Question..DONE")

        conn.commit()
        conn.close()


        create_formelfrage.replace_characters(self)


        if self.var_test_settings.get() == 1:
            GUI_settings_window.create_settings(self)
        else:
            print("No Test_settings used")



    def replace_characters(self):

        # open xml file to replace specific characters
        with open(self.qti_file_path_write, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&') #replace 'x' with 'new_x'

        # write to file
        with open(self.qti_file_path_write, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("WORKOVER FINISHED!")


class create_formelfrage_pool(Formelfrage):

    def __init__(self):

        # Die __init__ wird bei einem Knopfdruck auf "ILIAS-Fragenpool erstellen" ausgeführt
        # Es werden XML-Dateien und Ordner mit einer aufsteigenden ID erstellt.
        self.folder_new_ID_dir = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_qpl_Daten'))

        self.array_of_files_ID = os.listdir(self.folder_new_ID_dir)
        self.names = []
        self.filename_id = []
        self.question_title_list = []
        self.question_pool_id_list = []
        self.question_title_to_pool_id_dict = {}
        self.question_title_to_item_id_dict = {}

        for i in range(len(self.array_of_files_ID)):
            self.names.append(self.array_of_files_ID[i][-7:])
        for i in range(len(self.names)):
            self.filename_id.append(int(self.names[i]))




        # Pfad anpassungen - Die ID muss um +1 erhöht werden, wenn "Fragenpool erstellen" betätigt wird
        self.ilias_id_pool_qpl = "1596569820__0__qpl_" + str(max(self.filename_id)+1)
        self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + str(max(self.filename_id) + 1) + ".xml"
        self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + str(max(self.filename_id) + 1) + ".xml"
        self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qpl_xml))
        self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qti_xml))
        self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.taxonomy_file_writes = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))


        #self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))


        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Error: Creating directory. ' + directory)

        createFolder(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl)))

        def copytree(src, dst, symlinks=False, ignore=None):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

        # Hier wird das Verzeichnis kopiert, um die Struktur vom Fragenpool-Ordner zu erhalten
        copytree(os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'orig_1596569820__0__qpl_2074808')),
                 os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl)))

        # Da durch "copytree" alle Daten kopiert werden, werden hier die qpl.xml und die qti.xml auf die aktuelle Nummer umbenannt und später dadurch überschrieben
        os.rename(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten",  self.ilias_id_pool_qpl, "1596569820__0__qpl_2074808.xml")),
                  os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qpl_xml)))

        os.rename(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, "1596569820__0__qti_2074808.xml")),
                 os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, self.ilias_id_pool_qti_xml)))


        ###### Anpassung der Datei "Modul -> export". Akualisierung des Dateinamens
        self.modules_export_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Modules', 'TestQuestionPool', 'set_1', 'export.xml'))

        self.mytree = ET.parse(self.modules_export_file)
        self.myroot = self.mytree.getroot()

        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
            TaxId.set('Id', str(max(self.filename_id)+1))

        self.mytree.write(self.modules_export_file)

        with open(self.modules_export_file, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('ns0:', 'exp:')
        with open(self.modules_export_file, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)



        ######  Anpassung der Datei "taxonomy -> export". Akualisierung des Dateinamens
        self.taxonomy_export_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.mytree = ET.parse(self.taxonomy_export_file)
        self.myroot = self.mytree.getroot()

        for ExportItem in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
            #print(ExportItem.attrib.get('Id'))
            if ExportItem.attrib.get('Id') != "":
                #print(ExportItem.attrib.get('Id'))
                ExportItem.set('Id', str(max(self.filename_id) + 1))
                break



        for object_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ObjId'):
            object_id.text = str(max(self.filename_id)+1)
            break

        self.mytree.write(self.taxonomy_export_file)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_export_file)



        # ----------------------------------- Datei .xml Einlesen
        # self.mytree = ET.parse("xml_form_orig\\" + '1590230409__0__qti_1948621.xml')
        self.mytree = ET.parse(self.qti_file_pool_path_read)
        self.myroot = self.mytree.getroot()

        # Wird benutzt um ensprechend "oft" Fragen in die qpl Datei zu schreiben
        self.number_of_entrys = []

        #self.frame_create = LabelFrame(self.formula_tab, text="Create Formelfrage", padx=5, pady=5)
        #self.frame_create.grid(row=1, column=2)
        self.my_list = []
        self.entry_split = self.create_formelfrage_entry.get()
        self.entry_split = self.entry_split.split(",")

        # Alle Fragen aus der DB in Pool-XML schreiben
        if self.var_create_question_pool_all.get() == 1:
            conn = sqlite3.connect('ilias_questions_db.db')
            c = conn.cursor()
            c.execute("SELECT *, oid FROM my_table")

            records = c.fetchall()

            for record in records:
                self.my_list.append(int(record[len(record) - 1]))

            self.my_string = ','.join(map(str, self.my_list))
            self.entry_split = self.my_string.split(",")
            #print(self.my_string)
        # print(self.entry_split[0])
        # print(len(self.entry_split))

        # Einzelne Fragen aus der DB in Pool-XML schreiben
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        for x in range(len(self.entry_split)):
            for record in records:
                if str(record[len(record) - 1]) == self.entry_split[x]:


                    if record[2].lower() == "formelfrage":

                        self.question_difficulty = str(record[0])
                        self.question_category = str(record[1])
                        self.question_type = str(record[2])
                        self.question_title = str(record[3])
                        self.question_description_title = str(record[4])

                        self.question_type = self.question_type.replace('&', "&amp;")
                        self.question_title = self.question_title.replace('&', "&amp;")
                        self.question_description_title = self.question_description_title.replace('&', "&amp;")



                        self.question_description_main_raw = str(record[5])

                        self.index_list = []

                        #print(self.question_description_main_raw)

                        for i in range(1, len(self.question_description_main_raw)):
                            if self.question_description_main_raw[i] == '_':
                                self.position_begin = i
                                self.position_end = self.question_description_main_raw.find(" ", self.position_begin)
                                self.index_list.append(self.position_end)
                                self.question_description_main_raw= self.question_description_main_raw[:self.position_end] + ' </sub>' + self.question_description_main_raw[self.position_end:]
                        #print(self.question_description_main_raw)
                        for i in range(1, len(self.question_description_main_raw)):
                            if self.question_description_main_raw[i] == '^':
                                self.position_begin = i
                                self.position_end = self.question_description_main_raw.find(" ", self.position_begin)
                                self.index_list.append(self.position_end)
                                self.question_description_main_raw = self.question_description_main_raw[:self.position_end] + ' </sup>' + self.question_description_main_raw[self.position_end:]
                        #print(self.question_description_main_raw)


                        self.question_description_main_symbol_replaced = self.question_description_main_raw.replace('&', "&amp;")
                        self.question_description_main_multi_replaced = self.question_description_main_symbol_replaced.replace('\n', "&lt;/p&gt;&#13;&#10;&lt;p&gt;")
                        self.question_description_main_test = self.question_description_main_multi_replaced
                        self.question_description_main_latex_start = self.question_description_main_test.replace('\\)', " </span>")
                        self.question_description_main_latex_end = self.question_description_main_latex_start.replace('\\(', "<span class=\"latex\">")
                        self.question_description_main_sup = self.question_description_main_latex_end.replace('^', "<sup>")
                        #self.question_description_main_sup_end = self.question_description_main_sup_start.replace('</p>', "</sup>")
                        self.question_description_main_sub = self.question_description_main_sup.replace('_', "<sub>")
                        #self.question_description_main_sub_end = self.question_description_main_sub_start.replace('</b>', "</sub>")

                        self.question_description_main_italic_end = self.question_description_main_sub.replace('///', "</i> ")
                        self.question_description_main_italic_start = self.question_description_main_italic_end.replace('//', "<i>")
                        self.question_description_main_var_uppercase = self.question_description_main_italic_start.replace('$V', "$v")
                        self.question_description_main_res_uppercase = self.question_description_main_var_uppercase.replace('$R', "$r")

                        self.question_description_main = self.question_description_main_res_uppercase

                        #print(self.question_description_main)


                        self.res1_formula = str(record[6])
                        self.res1_formula_length = str(len(self.res1_formula))
                        self.res2_formula = str(record[7])
                        self.res2_formula_length = str(len(self.res2_formula))
                        self.res3_formula = str(record[8])
                        self.res3_formula_length = str(len(self.res3_formula))
                        self.res4_formula = str(record[9])
                        self.res4_formula_length = str(len(self.res4_formula))
                        self.res5_formula = str(record[10])
                        self.res5_formula_length = str(len(self.res5_formula))
                        self.res6_formula = str(record[11])
                        self.res6_formula_length = str(len(self.res6_formula))
                        self.res7_formula = str(record[12])
                        self.res7_formula_length = str(len(self.res7_formula))
                        self.res8_formula = str(record[13])
                        self.res8_formula_length = str(len(self.res8_formula))
                        self.res9_formula = str(record[14])
                        self.res9_formula_length = str(len(self.res9_formula))
                        self.res10_formula = str(record[15])
                        self.res10_formula_length = str(len(self.res10_formula))








                        # $V gegen $v tauschen, sonst enstehen Fehler beim ILIAS import
                        # Zusätzlich werden die Funktionen ILIAS-Konform angepasst
                        # Info aus ILIAS für die Eingabe einer Ergebnis-Formel:
                        # Erlaubt ist die Verwendung von bereits definierten Variablen ($v1 bis $vn), von bereits definierten Ergebnissen (z.B. $r1), das beliebige Klammern von Ausdrücken,
                        # die mathematischen Operatoren + (Addition), - (Subtraktion), * (Multiplikation), / (Division), ^ (Potenzieren),
                        # die Verwendung der Konstanten 'pi' für die Zahl Pi und 'e‘ für die Eulersche Zahl,
                        # sowie die mathematischen Funktionen 'sin', 'sinh', 'arcsin', 'asin', 'arcsinh', 'asinh', 'cos', 'cosh', 'arccos', 'acos', 'arccosh', 'acosh',
                        # 'tan', 'tanh', 'arctan', 'atan', 'arctanh', 'atanh', 'sqrt', 'abs', 'ln', 'log'.
                        self.res1_formula = self.res1_formula.lower()
                        self.res2_formula = self.res2_formula.lower()
                        self.res3_formula = self.res3_formula.lower()
                        self.res4_formula = self.res4_formula.lower()
                        self.res5_formula = self.res5_formula.lower()
                        self.res6_formula = self.res6_formula.lower()
                        self.res7_formula = self.res7_formula.lower()
                        self.res8_formula = self.res8_formula.lower()
                        self.res9_formula = self.res9_formula.lower()
                        self.res10_formula = self.res10_formula.lower()




                        self.var1_name = str(record[16])
                        self.var1_min = str(record[17])
                        self.var1_max = str(record[18])
                        self.var1_prec = str(record[19])
                        self.var1_divby = str(record[20])
                        self.var1_divby_length = str(len(self.var1_divby))
                        self.var1_unit = str(record[21])
                        self.var1_unit_length = str(len(self.var1_unit))

                        self.var2_name = str(record[22])
                        self.var2_min = str(record[23])
                        self.var2_max = str(record[24])
                        self.var2_prec = str(record[25])
                        self.var2_divby = str(record[26])
                        self.var2_divby_length = str(len(self.var2_divby))
                        self.var2_unit = str(record[27])
                        self.var2_unit_length = str(len(self.var2_unit))

                        self.var3_name = str(record[28])
                        self.var3_min = str(record[29])
                        self.var3_max = str(record[30])
                        self.var3_prec = str(record[31])
                        self.var3_divby = str(record[32])
                        self.var3_divby_length = str(len(self.var3_divby))
                        self.var3_unit = str(record[33])
                        self.var3_unit_length = str(len(self.var3_unit))

                        self.var4_name = str(record[34])
                        self.var4_min = str(record[35])
                        self.var4_max = str(record[36])
                        self.var4_prec = str(record[37])
                        self.var4_divby = str(record[38])
                        self.var4_divby_length = str(len(self.var4_divby))
                        self.var4_unit = str(record[39])
                        self.var4_unit_length = str(len(self.var4_unit))

                        self.var5_name = str(record[40])
                        self.var5_min = str(record[41])
                        self.var5_max = str(record[42])
                        self.var5_prec = str(record[43])
                        self.var5_divby = str(record[44])
                        self.var5_divby_length = str(len(self.var5_divby))
                        self.var5_unit = str(record[45])
                        self.var5_unit_length = str(len(self.var5_unit))

                        self.var6_name = str(record[46])
                        self.var6_min = str(record[47])
                        self.var6_max = str(record[48])
                        self.var6_prec = str(record[49])
                        self.var6_divby = str(record[50])
                        self.var6_divby_length = str(len(self.var6_divby))
                        self.var6_unit = str(record[51])
                        self.var6_unit_length = str(len(self.var6_unit))

                        self.var7_name = str(record[52])
                        self.var7_min = str(record[53])
                        self.var7_max = str(record[54])
                        self.var7_prec = str(record[55])
                        self.var7_divby = str(record[56])
                        self.var7_divby_length = str(len(self.var7_divby))
                        self.var7_unit = str(record[57])
                        self.var7_unit_length = str(len(self.var7_unit))

                        self.var8_name = str(record[58])
                        self.var8_min = str(record[59])
                        self.var8_max = str(record[60])
                        self.var8_prec = str(record[61])
                        self.var8_divby = str(record[62])
                        self.var8_divby_length = str(len(self.var7_divby))
                        self.var8_unit = str(record[63])
                        self.var8_unit_length = str(len(self.var7_unit))

                        self.var9_name = str(record[64])
                        self.var9_min = str(record[65])
                        self.var9_max = str(record[66])
                        self.var9_prec = str(record[67])
                        self.var9_divby = str(record[68])
                        self.var9_divby_length = str(len(self.var7_divby))
                        self.var9_unit = str(record[69])
                        self.var9_unit_length = str(len(self.var7_unit))

                        self.var10_name = str(record[70])
                        self.var10_min = str(record[71])
                        self.var10_max = str(record[72])
                        self.var10_prec = str(record[73])
                        self.var10_divby = str(record[74])
                        self.var10_divby_length = str(len(self.var7_divby))
                        self.var10_unit = str(record[75])
                        self.var10_unit_length = str(len(self.var7_unit))

                        self.res1_name = str(record[76])
                        self.res1_min = str(record[77])
                        self.res1_min_length = str(len(self.res1_min))
                        self.res1_max = str(record[78])
                        self.res1_max_length = str(len(self.res1_max))
                        self.res1_prec = str(record[79])
                        self.res1_tol = str(record[80])
                        self.res1_tol_length = str(len(self.res1_tol))
                        self.res1_points = str(record[81])
                        self.res1_unit = str(record[82])
                        self.res1_unit_length = str(len(self.res1_unit))


                        self.res2_name = str(record[83])
                        self.res2_min = str(record[84])
                        self.res2_min_length = str(len(self.res2_min))
                        self.res2_max = str(record[85])
                        self.res2_max_length = str(len(self.res2_max))
                        self.res2_prec = str(record[86])
                        self.res2_tol = str(record[87])
                        self.res2_tol_length = str(len(self.res2_tol))
                        self.res2_points = str(record[88])
                        self.res2_unit = str(record[89])
                        self.res2_unit_length = str(len(self.res2_unit))


                        self.res3_name = str(record[90])
                        self.res3_min = str(record[91])
                        self.res3_min_length = str(len(self.res3_min))
                        self.res3_max = str(record[92])
                        self.res3_max_length = str(len(self.res3_max))
                        self.res3_prec = str(record[93])
                        self.res3_tol = str(record[94])
                        self.res3_tol_length = str(len(self.res3_tol))
                        self.res3_points = str(record[95])
                        self.res3_unit = str(record[96])
                        self.res3_unit_length = str(len(self.res3_unit))

                        self.res4_name = str(record[97])
                        self.res4_min = str(record[98])
                        self.res4_min_length = str(len(self.res4_min))
                        self.res4_max = str(record[99])
                        self.res4_max_length = str(len(self.res4_max))
                        self.res4_prec = str(record[100])
                        self.res4_tol = str(record[101])
                        self.res4_tol_length = str(len(self.res4_tol))
                        self.res4_points = str(record[102])
                        self.res4_unit = str(record[103])
                        self.res4_unit_length = str(len(self.res4_unit))

                        self.res5_name = str(record[104])
                        self.res5_min = str(record[105])
                        self.res5_min_length = str(len(self.res5_min))
                        self.res5_max = str(record[106])
                        self.res5_max_length = str(len(self.res5_max))
                        self.res5_prec = str(record[107])
                        self.res5_tol = str(record[108])
                        self.res5_tol_length = str(len(self.res5_tol))
                        self.res5_points = str(record[109])
                        self.res5_unit = str(record[110])
                        self.res5_unit_length = str(len(self.res5_unit))

                        self.res6_name = str(record[111])
                        self.res6_min = str(record[112])
                        self.res6_min_length = str(len(self.res6_min))
                        self.res6_max = str(record[113])
                        self.res6_max_length = str(len(self.res6_max))
                        self.res6_prec = str(record[114])
                        self.res6_tol = str(record[115])
                        self.res6_tol_length = str(len(self.res6_tol))
                        self.res6_points = str(record[116])
                        self.res6_unit = str(record[117])
                        self.res6_unit_length = str(len(self.res6_unit))

                        self.res7_name = str(record[118])
                        self.res7_min = str(record[119])
                        self.res7_min_length = str(len(self.res7_min))
                        self.res7_max = str(record[120])
                        self.res7_max_length = str(len(self.res7_max))
                        self.res7_prec = str(record[121])
                        self.res7_tol = str(record[122])
                        self.res7_tol_length = str(len(self.res7_tol))
                        self.res7_points = str(record[123])
                        self.res7_unit = str(record[124])
                        self.res7_unit_length = str(len(self.res7_unit))

                        self.res8_name = str(record[125])
                        self.res8_min = str(record[126])
                        self.res8_min_length = str(len(self.res8_min))
                        self.res8_max = str(record[127])
                        self.res8_max_length = str(len(self.res8_max))
                        self.res8_prec = str(record[128])
                        self.res8_tol = str(record[129])
                        self.res8_tol_length = str(len(self.res8_tol))
                        self.res8_points = str(record[130])
                        self.res8_unit = str(record[131])
                        self.res8_unit_length = str(len(self.res8_unit))

                        self.res9_name = str(record[132])
                        self.res9_min = str(record[133])
                        self.res9_min_length = str(len(self.res9_min))
                        self.res9_max = str(record[134])
                        self.res9_max_length = str(len(self.res9_max))
                        self.res9_prec = str(record[135])
                        self.res9_tol = str(record[136])
                        self.res9_tol_length = str(len(self.res9_tol))
                        self.res9_points = str(record[137])
                        self.res9_unit = str(record[138])
                        self.res9_unit_length = str(len(self.res9_unit))

                        self.res10_name = str(record[139])
                        self.res10_min = str(record[140])
                        self.res10_min_length = str(len(self.res10_min))
                        self.res10_max = str(record[141])
                        self.res10_max_length = str(len(self.res10_max))
                        self.res10_prec = str(record[142])
                        self.res10_tol = str(record[143])
                        self.res10_tol_length = str(len(self.res10_tol))
                        self.res10_points = str(record[144])
                        self.res10_unit = str(record[145])
                        self.res10_unit_length = str(len(self.res10_unit))

                        self.img_name = str(record[146])
                        self.img_data_raw = record[147]
                        self.img_data = str(record[147])

                        self.test_time = str(record[148])


                        self.oid = str(record[len(record)-1]) #oid ist IMMER letztes Fach

                        create_formelfrage_pool.create_question_pool(self, x)  #

                        print("Formelfrage generated with Title --> \"" + self.question_title + "\"" + " mit pool tag: " + str(record[151]))   #Question_pool_tag

                        self.question_title_list.append(self.question_title)
                        self.question_pool_id_list.append(str(record[151]))





                    elif record[2].lower() == "multiple choice":
                        print("Question type with 'multiple choice' found")
                        create_multiplechoice.create_mc_question(MultipleChoice,self.mytree, self.myroot, self.qti_file_path_read, self.qti_file_path_write, self.entry_split, x)

                    else:
                        #record[2].lower() != "formelfrage" or record[2].lower() != "multiple choice":
                        print("ERROR: FRAGENPOOL KANN NICHT ERSTELLT WERDEN! --> Aufgabe ohne \"formelfrage\" bzw. \"multiple choice\"-Eintrag gefunden")


                # create_formelfrage.create_question(self, x)   LAST CHANGE
        conn.commit()
        conn.close()

        self.question_title_to_pool_id_dict = dict(zip(self.question_title_list, self.question_pool_id_list))

        print("\n")
        print("Fragenpool erstellt")
        print("Number of Questions generated: " + str(len(self.entry_split)))




        # ID und Fragen auflisten
        self.taxonomy_qtiXML_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten",  self.ilias_id_pool_qpl, self.ilias_id_pool_qti_xml))

        #Formelfrage.tax_file_refresh(self, self.taxonomy_qtiXML_file)


        # Fragen aus der qti Datei auslesen (FragenID, Fragentitel)
        self.mytree = ET.parse(self.taxonomy_qtiXML_file)
        self.myroot = self.mytree.getroot()

        self.item_id_list = []
        self.item_title_list = []
        self.item_pool_no_dublicates = []


        for item in self.myroot.iter('item'):
            self.item_id_raw = str(item.get('ident'))
            self.item_id = self.item_id_raw.rsplit('_', 1)[-1]
            self.item_title = str(item.get('title'))
            self.item_id_list.append(self.item_id)
            self.item_title_list.append(self.item_title)
            #print(self.item_id, self.item_title)

        self.question_title_to_item_id_dict = dict(zip(self.item_title_list, self.item_id_list))

        #print(self.question_title_to_item_id_dict)
        #print(self.question_title_to_pool_id_dict)

        #print("FOR-LOOP")
        #print("-----_")
        #print(self.taxonomy_file_question_pool)
        #print("------")
        for i in range(len(self.item_title_list)):
            self.item_pool_no_dublicates.append(self.question_title_to_pool_id_dict.get(self.item_title_list[i]))


        self.item_pool_no_dublicates = list(dict.fromkeys(self.item_pool_no_dublicates))


        # Knoten schreiben
        for i in range(len(self.item_pool_no_dublicates)):
            #print(self.question_title_to_item_id_dict.get(self.item_title_list[i]), self.question_title_to_pool_id_dict.get(self.item_title_list[i]))

            ### Taxonomie Datei schreiben: self, Pfad zur Datei, new_node_id, parent_node_id    parent_node auf "EMTPY" gesetzt, da nur 1 Ebene in der Taxonomie exisitieren soll
            Formelfrage.add_node_to_tax_from_excel(self, self.taxonomy_file_question_pool, self.item_pool_no_dublicates[i], "EMPTY")

        # Fragen zu Knoten hinzufügen
        for i in range(len(self.item_title_list)):
            # FUnktion starten mit: self, Pfad zur Datei, Item_ID, Item_Pool
            Formelfrage.assign_questions_to_node_from_excel(self, self.taxonomy_file_question_pool, self.question_title_to_item_id_dict.get(self.item_title_list[i]), self.question_title_to_pool_id_dict.get(self.item_title_list[i])  )



        # Taxonomie-Datei neu sortieren
        Formelfrage.tax_reallocate_from_excel(self, self.taxonomy_file_question_pool)



        for i in range(len(self.entry_split)):
            #print("ENTRY SPLIT: " + str(self.entry_split))
            create_formelfrage_pool.create_question_pool_qpl(self, i)


        ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
        self.qpl_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten",  self.ilias_id_pool_qpl, self.ilias_id_pool_qpl_xml))

        self.mytree = ET.parse(self.qpl_file)
        self.myroot = self.mytree.getroot()

        for ident_id in self.myroot.iter('Identifier'):
            ident_id.set('Entry', "il_0_qpl_" + str(max(self.filename_id)+1))
        self.mytree.write(self.qpl_file)







        # ILIAS Fragenpool Import Datei (Kopie)
        # Kopiert den Ordner aus "Fragenpool Daten" nach "Fragenpool zum Import
        createFolder(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_zum_Import", self.ilias_id_pool_qpl)))

        copytree(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl)),
                 os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_zum_Import", self.ilias_id_pool_qpl)))


        #shutil.make_archive(os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl)), 'zip', self.ilias_questionpool_for_import)

        print("Erstelle Ordner mit ID: 1596569820__0__qpl_" + str(max(self.filename_id)+1) + "...")
        print("ID Anpassung interner Dateien.. DONE")

        #print("old filename: " + str(max(self.filename_id)))
        self.filename_id.append(int(max(self.filename_id)+1))
        #print("new filename: " + str(max(self.filename_id)))






    def create_question_pool(self, x):



        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()



        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Error: Creating directory. ' + directory)

        print("FOLDER NAME FOR IMAGES")
        print(self.img_file_path_create_folder_pool + '/' + 'il_0_mob_000000' + str(x) + '/')
        createFolder(self.img_file_path_create_folder_pool + '/' + 'il_0_mob_000000' + str(x) + '/')

        for record in records:

            #Ohne If Abfrage werden ALLE Fragen aus der Datenbank erstellt
            if str(record[len(record)-1]) == self.entry_split[x]:
                #print("------------------------------")
                #print(str(record[len(record)-1]))
                #print("ENTRY SPLIT: " + str(self.entry_split[x]))
                #print("------------------------------")


                if self.img_data_raw != "EMPTY":
                    #img wird immer als PNG Datei abgelegt.
                    with open(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png", 'wb') as image_file:
                        image_file.write(self.img_data_raw)

                    self.image = Image.open(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")
                    self.image.save(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")





                # print("q_titel: " + str(self.question_title))

                # cast int from len() function to string! cant use int in concatenated string
                # the string is used down below in "SOLUTION STRING"

                r1_rating = "0"
                r1_rating_length = len(r1_rating)
                # print(r1_rating_length)

                r1_unit = ""
                r1_unit_length = len(r1_unit)
                # print(r1_unit_length)

                r1_unitvalue = ""
                r1_unitv_length = len(r1_unitvalue)
                # print(r1_unitv_length)

                r1_resultunits = ""
                r1_resultu_length = len(r1_resultunits)
                # print(r1_resultu_length)

                question_name = str(self.question_title)

                questestinterop = ET.Element('questestinterop')
                assessment = ET.SubElement(questestinterop, 'assessment')
                section = ET.SubElement(assessment, 'section')
                item = ET.SubElement(section, 'item')
                self.id_int_numbers = 400000 + x


                self.number_of_entrys.append(format(self.id_int_numbers, '06d')) #Zahlenfolge muss 6-stellig sein.
                item.set('ident', "il_0_qst_" + self.number_of_entrys[x])
                item.set('title', question_name)
                qticomment = ET.SubElement(item, 'qticomment')
                qticomment.text = self.question_description_title
                duration = ET.SubElement(item, 'duration')
                duration.text = self.test_time


                # append ITEM in the last "myroot"-Element. Here it is Element "section" in myroot
                self.myroot.append(item)



                if duration.text == "":
                    duration.text = "P0Y0M0DT1H0M0S"


                for assessment in self.myroot.iter('assessment'):

                    self.title_replaced = str(self.test_title_entry.get())
                    assessment.set('title', self.title_replaced.replace('&', "&amp;"))

                    if assessment.get('title') == "":
                        assessment.set('title', "DEFAULT")


                itemmetadata = ET.SubElement(item, 'itemmetadata')
                presentation = ET.SubElement(item, 'presentation')
                presentation.set('label', question_name)
                flow = ET.SubElement(presentation, 'flow')
                material = ET.SubElement(flow, 'material')

                mattext = ET.SubElement(material, 'mattext')
                mattext.set('texttype', "text/html")

                if self.img_data != "EMPTY":
                    #mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_0000000\" width=\"482\" /></p>"
                    mattext.text = "<p>" + self.question_description_main + "</p>" + "<p><img height=\"378\" src=\"il_0_mob_000000" + str(x) + "\" width=\"482\" /></p>"


                    matimage = ET.SubElement(material, 'matimage')
                    matimage.set('label', "il_0_mob_000000" + str(x))  # Object -> Filename
                    matimage.set('uri', "objects/il_0_mob_000000" + str(x) + "/" + self.img_name + ".png")


                else:
                    mattext.text = "<p>" + self.question_description_main + "</p>"  # + "<p><img height=\"378\" src=\"il_0_mob_1955056\" width=\"482\" /></p>"

                qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')
                # -----------------------------------------------------------------------ILIAS VERSION
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "ILIAS_VERSION"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = "5.4.10 2020-03-04"
                # -----------------------------------------------------------------------QUESTION_TYPE
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
                self.autor_replaced = str(self.autor_entry.get())
                fieldentry.text = self.autor_replaced.replace('&', "&amp;")
                # -----------------------------------------------------------------------POINTS
                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "points"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
                fieldentry.text = str(self.res1_points)
                # -----------------------------------------------------------------------Variables and Results
                #
                # To prevent the program to crash when no units are selected for ALL variables and results
                # those will be by default selected as "H" - Henry

                if self.var1_unit == "Unit":
                    self.var1_unit = ""
                    self.var1_unit_length = len(self.var1_unit)


                if self.var2_unit == "Unit":
                    self.var2_unit = ""
                    self.var2_unit_length = len(self.var2_unit)


                if self.var3_unit == "Unit":
                    self.var3_unit = ""
                    self.var3_unit_length = len(self.var3_unit)


                if self.var4_unit == "Unit":
                    self.var4_unit = ""
                    self.var4_unit_length = len(self.var4_unit)


                if self.var5_unit == "Unit":
                    self.var5_unit = ""
                    self.var5_unit_length = len(self.var5_unit)


                if self.var6_unit == "Unit":
                    self.var6_unit = ""
                    self.var6_unit_length = len(self.var6_unit)


                if self.var7_unit == "Unit":
                    self.var7_unit = ""
                    self.var7_unit_length = len(self.var7_unit)

                if self.var8_unit == "Unit":
                    self.var8_unit = ""
                    self.var8_unit_length = len(self.var8_unit)

                if self.var9_unit == "Unit":
                    self.var9_unit = ""
                    self.var9_unit_length = len(self.var9_unit)

                if self.var10_unit == "Unit":
                    self.var10_unit = ""
                    self.var10_unit_length = len(self.var10_unit)


                if self.res1_unit == "Unit":
                    self.res1_unit = ""
                    self.res1_unit_length = len(self.res1_unit)

                if self.res2_unit == "Unit":
                    self.res2_unit = ""
                    self.res2_unit_length = len(self.res2_unit)

                if self.res3_unit == "Unit":
                    self.res3_unit = ""
                    self.res3_unit_length = len(self.res3_unit)

                if self.res4_unit == "Unit":
                    self.res4_unit = ""
                    self.res4_unit_length = len(self.res4_unit)

                if self.res5_unit == "Unit":
                    self.res5_unit = ""
                    self.res5_unit_length = len(self.res5_unit)

                if self.res6_unit == "Unit":
                    self.res6_unit = ""
                    self.res6_unit_length = len(self.res6_unit)

                if self.res7_unit == "Unit":
                    self.res7_unit = ""
                    self.res7_unit_length = len(self.res7_unit)

                if self.res8_unit == "Unit":
                    self.res8_unit = ""
                    self.res8_unit_length = len(self.res8_unit)

                if self.res9_unit == "Unit":
                    self.res9_unit = ""
                    self.res9_unit_length = len(self.res9_unit)

                if self.res10_unit == "Unit":
                    self.res10_unit = ""
                    self.res10_unit_length = len(self.res10_unit)




                # -----------------------------------------------------------------------Variable 1

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var1_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var1_unit_length) + ":\"" + self.var1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var1_unit))) + ":\"" + Formelfrage.unit_table(self, self.var1_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var1_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var1_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var1_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var1_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_1 no UNIT")
                # -----------------------------------------------------------------------Variable 2

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var2_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var2_unit_length) + ":\"" + self.var2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var2_unit))) + ":\"" + Formelfrage.unit_table(self, self.var2_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var2_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var2_divby_length + ":\"" + self.var2_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var2_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var2_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_2 no UNIT")

                # -----------------------------------------------------------------------Variable 3

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var3_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                       "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                       "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                       "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                       "s:4:\"unit\";s:" + str(self.var3_unit_length) + ":\"" + self.var3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var3_unit))) + ":\"" + Formelfrage.unit_table(self, self.var3_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var3_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var3_divby_length + ":\"" + self.var3_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var3_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var3_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_3 no UNIT")
                # -----------------------------------------------------------------------Variable 4

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var4_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var4_unit_length) + ":\"" + self.var4_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var4_unit))) + ":\"" + Formelfrage.unit_table(self, self.var4_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var4_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var4_divby_length + ":\"" + self.var4_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var4_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var4_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_4 no UNIT")
                # -----------------------------------------------------------------------Variable 5

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var5_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var5_unit_length) + ":\"" + self.var5_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var5_unit))) + ":\"" + Formelfrage.unit_table(self, self.var5_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var5_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var5_divby_length + ":\"" + self.var5_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var5_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var5_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_5 no UNIT")

                # -----------------------------------------------------------------------Variable 6

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var6_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var6_unit_length) + ":\"" + self.var6_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var6_unit))) + ":\"" + Formelfrage.unit_table(self, self.var6_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var6_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var6_divby_length + ":\"" + self.var6_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var6_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var6_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_6 no UNIT")

                # -----------------------------------------------------------------------Variable 7

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var7_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var7_unit_length) + ":\"" + self.var7_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var7_unit))) + ":\"" + Formelfrage.unit_table(self, self.var7_unit) + "\";" \
                                      "}"

                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var7_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var7_divby_length + ":\"" + self.var7_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var7_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var7_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_7 no UNIT")


                # -----------------------------------------------------------------------Variable 8

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v8"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var8_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var8_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var8_divby_length + ":\"" + self.var8_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var8_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var8_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var8_unit_length) + ":\"" + self.var8_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var8_unit))) + ":\"" + Formelfrage.unit_table(self, self.var8_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var8_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var1_divby_length + ":\"" + self.var8_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var8_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var8_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_8 no UNIT")

                # -----------------------------------------------------------------------Variable 9

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v9"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var9_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var9_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var9_divby_length + ":\"" + self.var9_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var9_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var9_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var9_unit_length) + ":\"" + self.var9_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var9_unit))) + ":\"" + Formelfrage.unit_table(self, self.var9_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var9_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var9_divby_length + ":\"" + self.var9_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var9_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var9_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_1 no UNIT")

            # -----------------------------------------------------------------------Variable 10

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$v10"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.var10_unit != "":
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var10_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var10_divby_length + ":\"" + self.var10_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var10_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var10_max + ";" \
                                      "s:4:\"unit\";s:" + str(self.var10_unit_length) + ":\"" + self.var10_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.var10_unit))) + ":\"" + Formelfrage.unit_table(self, self.var10_unit) + "\";" \
                                      "}"
                else:
                    fieldentry.text = "a:6:{" \
                                      "s:9:\"precision\";i:" + self.var10_prec + ";" \
                                      "s:12:\"intprecision\";s:" + self.var10_divby_length + ":\"" + self.var10_divby + "\";" \
                                      "s:8:\"rangemin\";d:" + self.var10_min + ";" \
                                      "s:8:\"rangemax\";d:" + self.var10_max + ";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "}"
                    #print("VAR_10 no UNIT")

                # -----------------------------------------------------------------------Solution 1
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r1"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res1_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res1_unit_length) + ":\"" + self.res1_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res1_unit))) + ":\"" + Formelfrage.unit_table(self, self.res1_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res1_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res1_tol_length + ":\"" + self.res1_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res1_min_length + ":\"" + self.res1_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res1_max_length + ":\"" + self.res1_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res1_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res1_formula_length + ":\"" + self.res1_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
                        # -----------------------------------------------------------------------Solution 2
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r2"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res2_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res2_unit_length) + ":\"" + self.res2_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res2_unit))) + ":\"" + Formelfrage.unit_table(self, self.res2_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res2_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res2_tol_length + ":\"" + self.res2_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res2_min_length + ":\"" + self.res2_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res2_max_length + ":\"" + self.res2_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res2_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res2_formula_length + ":\"" + self.res2_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
                # -----------------------------------------------------------------------Solution 3
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r3"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res3_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res3_unit_length) + ":\"" + self.res3_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res3_unit))) + ":\"" + Formelfrage.unit_table(self, self.res3_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res3_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res3_tol_length + ":\"" + self.res3_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res3_min_length + ":\"" + self.res3_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res3_max_length + ":\"" + self.res3_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res3_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res3_formula_length + ":\"" + self.res3_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 4
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r4"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res4_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res4_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res4_tol_length + ":\"" + self.res4_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res4_min_length + ":\"" + self.res4_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res4_max_length + ":\"" + self.res4_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res4_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res4_formula_length + ":\"" + self.res4_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res4_unit_length) + ":\"" + self.res4_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res4_unit))) + ":\"" + Formelfrage.unit_table(self, self.res4_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res4_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res4_tol_length + ":\"" + self.res4_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res4_min_length + ":\"" + self.res4_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res4_max_length + ":\"" + self.res4_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res4_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res4_formula_length + ":\"" + self.res4_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 5
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r5"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res5_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res5_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res5_tol_length + ":\"" + self.res5_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res5_min_length + ":\"" + self.res5_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res5_max_length + ":\"" + self.res5_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res5_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res5_formula_length + ":\"" + self.res5_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res5_unit_length) + ":\"" + self.res5_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res5_unit))) + ":\"" + Formelfrage.unit_table(self, self.res5_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res5_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res5_tol_length + ":\"" + self.res5_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res5_min_length + ":\"" + self.res5_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res5_max_length + ":\"" + self.res5_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res5_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res5_formula_length + ":\"" + self.res5_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 6
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r6"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res6_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res6_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res6_tol_length + ":\"" + self.res6_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res6_min_length + ":\"" + self.res6_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res6_max_length + ":\"" + self.res6_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res6_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res6_formula_length + ":\"" + self.res6_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res6_unit_length) + ":\"" + self.res6_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res6_unit))) + ":\"" + Formelfrage.unit_table(self, self.res6_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res6_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res6_tol_length + ":\"" + self.res6_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res6_min_length + ":\"" + self.res6_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res6_max_length + ":\"" + self.res6_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res6_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res6_formula_length + ":\"" + self.res6_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 7
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r7"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res7_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res7_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res7_tol_length + ":\"" + self.res7_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res7_min_length + ":\"" + self.res7_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res7_max_length + ":\"" + self.res7_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res7_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res7_formula_length + ":\"" + self.res7_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res7_unit_length) + ":\"" + self.res7_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res7_unit))) + ":\"" + Formelfrage.unit_table(self, self.res7_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res7_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res7_tol_length + ":\"" + self.res7_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res7_min_length + ":\"" + self.res7_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res7_max_length + ":\"" + self.res7_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res7_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res7_formula_length + ":\"" + self.res7_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 8
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r8"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res8_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res8_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res8_tol_length + ":\"" + self.res8_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res8_min_length + ":\"" + self.res8_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res8_max_length + ":\"" + self.res8_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res8_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res8_formula_length + ":\"" + self.res8_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res8_unit_length) + ":\"" + self.res8_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res8_unit))) + ":\"" + Formelfrage.unit_table(self, self.res8_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res8_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res8_tol_length + ":\"" + self.res8_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res8_min_length + ":\"" + self.res8_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res8_max_length + ":\"" + self.res8_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res8_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res8_formula_length + ":\"" + self.res8_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"


                # -----------------------------------------------------------------------Solution 9
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r9"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res9_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res9_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res9_tol_length + ":\"" + self.res9_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res9_min_length + ":\"" + self.res9_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res9_max_length + ":\"" + self.res9_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res9_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res9_formula_length + ":\"" + self.res9_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res9_unit_length) + ":\"" + self.res9_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res9_unit))) + ":\"" + Formelfrage.unit_table(self, self.res9_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res9_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res9_tol_length + ":\"" + self.res9_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res9_min_length + ":\"" + self.res9_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res9_max_length + ":\"" + self.res9_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res9_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res9_formula_length + ":\"" + self.res9_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"

                # -----------------------------------------------------------------------Solution 10
                # s for string length: "9" -> precision = "9" characters
                # rangemin: "i" for negative numbers, ...
                #           "d" for (negativ?) float numbers
                #           "i" for negativ whole numbers
                #           "s" for positiv whole numbers

                qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
                fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
                fieldlabel.text = "$r10"
                fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')

                if self.res10_unit != "":
                    fieldentry.text = "a:10:{" \
                                      "s:9:\"precision\";i:" + self.res10_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res10_tol_length + ":\"" + self.res10_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res10_min_length + ":\"" + self.res10_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res10_max_length + ":\"" + self.res10_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res10_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res10_formula_length + ":\"" + self.res10_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:" + str(self.res10_unit_length) + ":\"" + self.res10_unit + "\";" \
                                      "s:9:\"unitvalue\";s:" + str(len(Formelfrage.unit_table(self, self.res10_unit))) + ":\"" + Formelfrage.unit_table(self, self.res10_unit) + "\";" \
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
                                      "s:9:\"precision\";i:" + self.res10_prec + ";" \
                                      "s:9:\"tolerance\";s:" + self.res10_tol_length + ":\"" + self.res10_tol + "\";" \
                                      "s:8:\"rangemin\";s:" + self.res10_min_length + ":\"" + self.res10_min + "\";" \
                                      "s:8:\"rangemax\";s:" + self.res10_max_length + ":\"" + self.res10_max + "\";" \
                                      "s:6:\"points\";s:1:\"" + self.res10_points + "\";" \
                                      "s:7:\"formula\";s:" + self.res10_formula_length + ":\"" + self.res10_formula + "\";" \
                                      "s:6:\"rating\";s:0:\"\";" \
                                      "s:4:\"unit\";s:0:\"\";" \
                                      "s:9:\"unitvalue\";s:0:\"\";" \
                                      "s:11:\"resultunits\";a:0:{}" \
                                      "}"
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

                self.mytree.write(self.qti_file_pool_path_write)



        conn.commit()
        conn.close()
        create_formelfrage_pool.replace_characters_pool(self)


    def create_question_pool_qpl(self, x):
        # Fragenpool - qpl bearbeiten

        self.loop_nr = x+1


        # ----------------------------------- Datei .xml Einlesen
        # self.mytree = ET.parse("xml_form_orig\\" + '1590230409__0__qti_1948621.xml')
        self.mytree = ET.parse(self.qpl_file_pool_path_read)
        self.myroot = self.mytree.getroot()

        # Hinzufügen von Question QRef in qpl Datei
        for i in range(self.loop_nr):
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

            self.mytree.write(self.qpl_file_pool_path_write)


        # Hinzufügen von TriggerQuestion ID in qpl Datei
        for i in range(self.loop_nr):
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

            self.mytree.write(self.qpl_file_pool_path_write)





    def replace_characters_pool(self):

        # open xml file to replace specific characters
        with open(self.qti_file_pool_path_write, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&')  # replace 'x' with 'new_x'

        # write to file
        with open(self.qti_file_pool_path_write, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)


"""
class create_singlechoice()
    def __init__(self):
        
        # Vorlage für einen Test einlesen mit "tst_file_path_read". Enthält eine *xml ohne Fragen
        self.mytree = ET.parse(self.tst_file_path_read)
        self.myroot = self.mytree.getroot()

        for title in self.myroot.iter('Title'):
            title.text = self.test_title_entry.get()
            title.text = title.text.replace('&', "&amp;")

            if title.text == "":
                title.text = "DEFAULT"

        self.mytree.write(self.tst_file_path_write)



        # ----------------------------------- Datei .xml Einlesen
       
        self.mytree = ET.parse(self.qti_file_path_read)
        self.myroot = self.mytree.getroot()

        self.entry_split = self.create_formelfrage_entry.get()
        self.entry_split = self.entry_split.split(",")


        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()
"""


class GUI_settings_window(Formelfrage):

    def __init__(self):


        # New Window must be "Toplevel" not "Tk()" in order to get Radiobuttons to work properly
        self.test_settings_window = Toplevel()
        self.test_settings_window.title("Test-Settings")

        # Create a ScrolledFrame widget
        self.sf_test_settings = ScrolledFrame(self.test_settings_window, width=self.settings_width, height=self.settings_height)
        self.sf_test_settings.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        #self.sf_test_settings.bind_arrow_keys(app)
        #self.sf_test_settings.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.test_settings = self.sf_test_settings.display_widget(Frame)



        self.frame1 = LabelFrame(self.test_settings, text="Test Settings Frame1...", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.frame2 = LabelFrame(self.test_settings, text="Test Settings Frame2...", padx=5, pady=5)
        self.frame2.grid(row=0, column=1, padx=20, pady=10, sticky=NW)

        self.frame3 = LabelFrame(self.test_settings, text="Test Settings Frame3...", padx=5, pady=5)
        self.frame3.grid(row=0, column=2, padx=20, pady=10, sticky=NW)


        self.res12_min_listbox_label = Label(self.frame1, text="EINSTELLUNGEN DES TESTS", font=('Helvetica', 10, 'bold'))
        self.res12_min_listbox_label.grid(row=0, column=0, sticky=W, padx=10, pady=(20, 0))

        self.res90_min_listbox_label = Label(self.frame1, text="Test-Titel")
        self.res90_min_listbox_label.grid(row=1, column=0, sticky=W, padx=10)
        self.res91_max_listbox_label = Label(self.frame1, text="Beschreibung")
        self.res91_max_listbox_label.grid(row=2, column=0, sticky=W, padx=10)

        self.res1_max_listbox_label = Label(self.frame1, text="Auswahl der Testfragen")
        self.res1_max_listbox_label.grid(row=4, column=0, sticky=W, padx=10)
        self.res1_prec_listbox_label = Label(self.frame1, text="Datenschutz")
        self.res1_prec_listbox_label.grid(row=7, column=0, sticky=W, padx=10)

        self.res1_tol_listbox_label = Label(self.frame1, text="VERFÜGBARKEIT", font=('Helvetica', 10, 'bold'))
        self.res1_tol_listbox_label.grid(row=9, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res1_points_listbox_label = Label(self.frame1, text="Online   ---   not working")
        self.res1_points_listbox_label.grid(row=10, column=0, sticky=W, padx=10)
        self.res13_points_listbox_label = Label(self.frame1, text="Zeitlich begrenzte Verfügbarkeit   ---   not working")
        self.res13_points_listbox_label.grid(row=11, column=0, sticky=W, padx=10)

        self.res22_tol_listbox_label = Label(self.frame1, text="INFORMATIONEN ZUM EINSTIEG", font=('Helvetica', 10, 'bold'))
        self.res22_tol_listbox_label.grid(row=14, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res23_points_listbox_label = Label(self.frame1, text="Einleitung")
        self.res23_points_listbox_label.grid(row=15, column=0, sticky=W, padx=10)
        self.res24_points_listbox_label = Label(self.frame1, text="Testeigenschaften anzeigen")
        self.res24_points_listbox_label.grid(row=16, column=0, sticky=W, padx=10)

        self.res31_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: ZUGANG", font=('Helvetica', 10, 'bold'))
        self.res31_tol_listbox_label.grid(row=17, column=0, sticky=W, padx=10, pady=(20, 0))

        self.test_time_year_label = Label(self.frame1, text="Jahr")
        self.test_time_year_label.grid(row=17, column=1, sticky=W)
        self.test_time_month_label = Label(self.frame1, text="Mon.")
        self.test_time_month_label.grid(row=17, column=1, sticky=W, padx=35)
        self.test_time_day_label = Label(self.frame1, text="Tag")
        self.test_time_day_label.grid(row=17, column=1, sticky=W, padx=70)
        self.test_time_hour_label = Label(self.frame1, text="Std.")
        self.test_time_hour_label.grid(row=17, column=1, sticky=W, padx=105)
        self.test_time_minute_label = Label(self.frame1, text="Min.")
        self.test_time_minute_label.grid(row=17, column=1, sticky=W, padx=140)



        self.res32_points_listbox_label = Label(self.frame1, text="Test-Start")
        self.res32_points_listbox_label.grid(row=18, column=0, sticky=W, padx=10)
        self.res33_points_listbox_label = Label(self.frame1, text="Test-Ende")
        self.res33_points_listbox_label.grid(row=19, column=0, sticky=W, padx=10)
        self.res34_tol_listbox_label = Label(self.frame1, text="Test-Passwort")
        self.res34_tol_listbox_label.grid(row=20, column=0, sticky=W, padx=10)
        self.res35_points_listbox_label = Label(self.frame1, text="Nur ausgewählte Teilnehmer")
        self.res35_points_listbox_label.grid(row=21, column=0, sticky=W, padx=10)
        self.res36_points_listbox_label = Label(self.frame1, text="Anzahl gleichzeitiger Teilnehmer begrenzen")
        self.res36_points_listbox_label.grid(row=22, column=0, sticky=W, padx=10)
        self.res37_points_listbox_label = Label(self.frame1, text="Inaktivitätszeit der Teilnehmner (in Sek.)")
        self.res37_points_listbox_label.grid(row=23, column=0, sticky=W, padx=30)

        self.res41_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: STEUERUNG TESTDURCHLAUF", font=('Helvetica', 10, 'bold'))
        self.res41_tol_listbox_label.grid(row=24, column=0, sticky=W, padx=10, pady=(20, 0))
        self.res42_points_listbox_label = Label(self.frame1, text="Anzahl von Testdurchläufen begrenzen")
        self.res42_points_listbox_label.grid(row=25, column=0, sticky=W, padx=10)
        self.res43_points_listbox_label = Label(self.frame1, text="Wartezeit zwischen Durchläufen erzwingen")
        self.res43_points_listbox_label.grid(row=26, column=0, sticky=W, padx=10)
        self.res44_tol_listbox_label = Label(self.frame1, text="Bearbeitungsdauer begrenzen")
        self.res44_tol_listbox_label.grid(row=27, column=0, sticky=W, padx=10)
        self.res44_tol_listbox_label = Label(self.frame1, text="Bearbeitungsdauer (in Min).")
        self.res44_tol_listbox_label.grid(row=28, column=0, sticky=W, padx=30)
        self.res44_tol_listbox_label = Label(self.frame1, text="Max. Bearbeitungsdauer für jeden Testlauf zurücksetzen")
        self.res44_tol_listbox_label.grid(row=29, column=0, sticky=W, padx=30)
        self.res45_points_listbox_label = Label(self.frame1, text="Prüfungsansicht")
        self.res45_points_listbox_label.grid(row=30, column=0, sticky=W, padx=10)
        self.res45_1_points_listbox_label = Label(self.frame1, text="Titel des Tests")
        self.res45_1_points_listbox_label.grid(row=31, column=0, sticky=W, padx=30)
        self.res45_2_points_listbox_label = Label(self.frame1, text="Name des Teilnehmers")
        self.res45_2_points_listbox_label.grid(row=32, column=0, sticky=W, padx=30)
        self.res46_points_listbox_label = Label(self.frame1, text="ILIAS-Prüfungsnummer anzeigen")
        self.res46_points_listbox_label.grid(row=33, column=0, sticky=W, padx=10)

        self.res51_tol_listbox_label = Label(self.frame2, text="DURCHFÜHRUNG: VERHALTEN DER FRAGE", font=('Helvetica', 10, 'bold'))
        self.res51_tol_listbox_label.grid(row=0, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res52_points_listbox_label = Label(self.frame2, text="Anzeige der Fragentitel")
        self.res52_points_listbox_label.grid(row=1, column=2, sticky=W, padx=10)
        self.res53_points_listbox_label = Label(self.frame2, text="Automatisches speichern")
        self.res53_points_listbox_label.grid(row=4, column=2, sticky=W, padx=10)
        self.res54_tol_listbox_label = Label(self.frame2, text="Fragen mischen")
        self.res54_tol_listbox_label.grid(row=5, column=2, sticky=W, padx=10)
        self.res55_points_listbox_label = Label(self.frame2, text="Lösungshinweise")
        self.res55_points_listbox_label.grid(row=6, column=2, sticky=W, padx=10)
        self.res56_points_listbox_label = Label(self.frame2, text="Direkte Rückmeldung   ---   not working")
        self.res56_points_listbox_label.grid(row=7, column=2, sticky=W, padx=10)
        self.res57_tol_listbox_label = Label(self.frame2, text="Teilnehmerantworten")
        self.res57_tol_listbox_label.grid(row=8, column=2, sticky=W, padx=10)
        self.res58_points_listbox_label = Label(self.frame2, text="Verpflichtende Fragen")
        self.res58_points_listbox_label.grid(row=12, column=2, sticky=W, padx=10)

        self.res61_tol_listbox_label = Label(self.frame2, text="DURCHFÜHRUNG: FUNKTIONEN FÜR TEILNEHMER",
                                        font=('Helvetica', 10, 'bold'))
        self.res61_tol_listbox_label.grid(row=13, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res62_points_listbox_label = Label(self.frame2, text="Verwendung vorheriger Lösungen")
        self.res62_points_listbox_label.grid(row=14, column=2, sticky=W, padx=10)
        self.res63_points_listbox_label = Label(self.frame2, text="\"Test unterbrechen\" anzeigen")
        self.res63_points_listbox_label.grid(row=15, column=2, sticky=W, padx=10)
        self.res64_tol_listbox_label = Label(self.frame2, text="Nicht beantwortete Fragen")
        self.res64_tol_listbox_label.grid(row=16, column=2, sticky=W, padx=10)
        self.res65_points_listbox_label = Label(self.frame2, text="Fragenliste und Bearbeitungsstand anzeigen")
        self.res65_points_listbox_label.grid(row=18, column=2, sticky=W, padx=10)
        self.res66_points_listbox_label = Label(self.frame2, text="Fragen markieren")
        self. res66_points_listbox_label.grid(row=19, column=2, sticky=W, padx=10)

        self.res71_tol_listbox_label = Label(self.frame2, text="TEST ABSCHLIESSEN", font=('Helvetica', 10, 'bold'))
        self.res71_tol_listbox_label.grid(row=20, column=2, sticky=W, padx=10, pady=(20, 0))
        self.res72_points_listbox_label = Label(self.frame2, text="Übersicht gegebener Antworten")
        self.res72_points_listbox_label.grid(row=21, column=2, sticky=W, padx=10)
        self.res73_points_listbox_label = Label(self.frame2, text="Abschließende Bemerkung")
        self.res73_points_listbox_label.grid(row=22, column=2, sticky=W, padx=10)
        self.res74_tol_listbox_label = Label(self.frame2, text="Weiterleitung")
        self.res74_tol_listbox_label.grid(row=23, column=2, sticky=W, padx=10)
        self.res75_points_listbox_label = Label(self.frame2, text="Benachrichtigung")
        self.res75_points_listbox_label.grid(row=24, column=2, sticky=W, padx=10)

        # --------------------------- DEFINE CHECKBOXES WITH ENTRYS ---------------------------------------



        # --------------------------- CHECKBOXES ---------------------------------------

        self.var_online = IntVar()
        self.check_online = Checkbutton(self.frame1, text="", variable=self.var_online, onvalue=1, offvalue=0)
        self.check_online.deselect()
        self.check_online.grid(row=10, column=1, sticky=W)

        self.var_time_limited = IntVar()
        self.time_limited_start_label = Label(self.frame1, text="Start")
        self.time_limited_start_day_label = Label(self.frame1, text="Tag")
        self.time_limited_start_day_entry = Entry(self.frame1, width=3)
        self.time_limited_start_month_label = Label(self.frame1, text="Mo")
        self.time_limited_start_month_entry = Entry(self.frame1, width=3)
        self.time_limited_start_year_label = Label(self.frame1, text="Jahr")
        self.time_limited_start_year_entry = Entry(self.frame1, width=4)
        self.time_limited_start_hour_label = Label(self.frame1, text="Std")
        self.time_limited_start_hour_entry = Entry(self.frame1, width=3)
        self.time_limited_start_minute_label = Label(self.frame1, text="Min")
        self.time_limited_start_minute_entry = Entry(self.frame1, width=3)

        self.time_limited_end_label = Label(self.frame1, text="Ende")
        self.time_limited_end_day_label = Label(self.frame1, text="Tag")
        self.time_limited_end_day_entry = Entry(self.frame1, width=3)
        self.time_limited_end_month_label = Label(self.frame1, text="Mo")
        self.time_limited_end_month_entry = Entry(self.frame1, width=3)
        self.time_limited_end_year_label = Label(self.frame1, text="Jahr")
        self.time_limited_end_year_entry = Entry(self.frame1, width=4)
        self.time_limited_end_hour_label = Label(self.frame1, text="Std")
        self.time_limited_end_hour_entry = Entry(self.frame1, width=3)
        self.time_limited_end_minute_label = Label(self.frame1, text="Min")
        self.time_limited_end_minute_entry = Entry(self.frame1, width=3)


        #self.entry.grid(row=11, column=1, sticky=W, padx=20)
        self.check_time_limited = Checkbutton(self.frame1, text="", variable=self.var_time_limited, onvalue=1, offvalue=0,
                                              command=lambda v=self.var_time_limited: GUI_settings_window.show_entry_time_limited_start(self, v))
        self.check_time_limited.deselect()
        self.check_time_limited.grid(row=11, column=1, sticky=W)

        self.var_introduction = IntVar()
        self.check_introduction = Checkbutton(self.frame1, text="", variable=self.var_introduction, onvalue=1, offvalue=0,
                                              command=lambda v=self.var_introduction: GUI_settings_window.show_introduction_textfield(self, v))
        self.check_introduction.deselect()
        self.check_introduction.grid(row=15, column=1, sticky=W)

        self.var_test_prop = IntVar()
        self.check_test_prop = Checkbutton(self.frame1, text="", variable=self.var_test_prop, onvalue=1, offvalue=0)
        self.check_test_prop.deselect()
        self.check_test_prop.grid(row=16, column=1, sticky=W)

        #self.var_test_password = IntVar()
        #self.check_test_password = Checkbutton(self.frame1, text="", variable=self.var_test_password, onvalue=1, offvalue=0)
        #self.check_test_password.deselect()
        #self.check_test_password.grid(row=20, column=1, sticky=W)

        self.var_specific_users = IntVar()
        self.check_specific_users = Checkbutton(self.frame1, text="", variable=self.var_specific_users, onvalue=1, offvalue=0)
        self.check_specific_users.deselect()
        self.check_specific_users.grid(row=21, column=1, sticky=W)

        #self.var_fixed_users = IntVar()
        #self.check_fixed_users = Checkbutton(self.frame1, text="", variable=self.var_fixed_users, onvalue=1, offvalue=0)
        #self.check_fixed_users.deselect()
        #self.check_fixed_users.grid(row=22, column=1, sticky=W)

        #self.var_limit_test_runs = IntVar()
        #self.check_limit_test_runs = Checkbutton(self.frame1, text="", variable=self.var_limit_test_runs, onvalue=1, offvalue=0)
        #self.check_limit_test_runs.deselect()
        #self.check_limit_test_runs.grid(row=22, column=1, sticky=W)

        #self.var_time_betw_test_runs = IntVar()
        #self.check_time_betw_test_runs = Checkbutton(self.frame1, text="", variable=self.var_time_betw_test_runs, onvalue=1, offvalue=0)
        #self.check_time_betw_test_runs.deselect()
        #self.check_time_betw_test_runs.grid(row=25, column=1, sticky=W)

        self.var_processing_time = IntVar()
        self.check_processing_time = Checkbutton(self.frame1, text="", variable=self.var_processing_time, onvalue=1, offvalue=0)
        self.check_processing_time.deselect()
        self.check_processing_time.grid(row=27, column=1, sticky=W)

        self.var_processing_time_reset = IntVar()
        self.check_processing_time_reset = Checkbutton(self.frame1, text="", variable=self.var_processing_time_reset, onvalue=1, offvalue=0)
        self.check_processing_time_reset.deselect()
        self.check_processing_time_reset.grid(row=29, column=1, sticky=W)

        self.var_examview = IntVar()
        self.check_examview = Checkbutton(self.frame1, text="", variable=self.var_examview, onvalue=1, offvalue=0)
        self.check_examview.deselect()
        self.check_examview.grid(row=30, column=1, sticky=W)

        self.var_examview_test_title = IntVar()
        self.check_examview_test_title = Checkbutton(self.frame1, text="", variable=self.var_examview_test_title, onvalue=1, offvalue=0)
        self.check_examview_test_title.deselect()
        self.check_examview_test_title.grid(row=31, column=1, sticky=W)

        self.var_examview_user_name = IntVar()
        self.check_examview_user_name = Checkbutton(self.frame1, text="", variable=self.var_examview_user_name, onvalue=1, offvalue=0)
        self.check_examview_user_name.deselect()
        self.check_examview_user_name.grid(row=32, column=1, sticky=W)

        self.var_show_ilias_nr = IntVar()
        self.check_show_ilias_nr = Checkbutton(self.frame1, text="", variable=self.var_show_ilias_nr, onvalue=1, offvalue=0)
        self.check_show_ilias_nr.deselect()
        self.check_show_ilias_nr.grid(row=33, column=1, sticky=W)

        self.var_autosave = IntVar()
        self.check_autosave = Checkbutton(self.frame2, text="", variable=self.var_autosave, onvalue=1, offvalue=0,
                                          command=lambda v=self.var_autosave: GUI_settings_window.enable_autosave(self, v))

        self.check_autosave_interval_label = Label(self.frame2, text="Speicherintervall (in Sek.):")
        self.check_autosave_interval_entry = Entry(self.frame2, width=10)
        self.check_autosave.deselect()
        self.check_autosave.grid(row=4, column=3, sticky=W)

        self.var_mix_questions = IntVar()
        self.check_mix_questions = Checkbutton(self.frame2, text="", variable=self.var_mix_questions, onvalue=1, offvalue=0)
        self.check_mix_questions.deselect()
        self.check_mix_questions.grid(row=5, column=3, sticky=W)

        self.var_show_solution_notes = IntVar()
        self.check_show_solution_notes = Checkbutton(self.frame2, text="", variable=self.var_show_solution_notes, onvalue=1, offvalue=0)
        self.check_show_solution_notes.deselect()
        self.check_show_solution_notes.grid(row=6, column=3, sticky=W)

        self.var_direct_response = IntVar()
        self.check_direct_response = Checkbutton(self.frame2, text="", variable=self.var_direct_response, onvalue=1, offvalue=0)
        self.check_direct_response.deselect()
        self.check_direct_response.grid(row=7, column=3, sticky=W)

        self.var_mandatory_questions = IntVar()
        self.check_mandatory_questions = Checkbutton(self.frame2, text="", variable=self.var_mandatory_questions, onvalue=1, offvalue=0)
        self.check_mandatory_questions.deselect()
        self.check_mandatory_questions.grid(row=12, column=3, sticky=W)

        self.var_use_previous_solution = IntVar()
        self.check_use_previous_solution = Checkbutton(self.frame2, text="", variable=self.var_use_previous_solution, onvalue=1, offvalue=0)
        self.check_use_previous_solution.deselect()
        self.check_use_previous_solution.grid(row=14, column=3, sticky=W)

        self.var_show_test_cancel = IntVar()
        self.check_show_test_cancel = Checkbutton(self.frame2, text="", variable=self.var_show_test_cancel, onvalue=1, offvalue=0)
        self.check_show_test_cancel.deselect()
        self.check_show_test_cancel.grid(row=15, column=3, sticky=W)

        self.var_show_question_list_process_status = IntVar()
        self.check_show_question_list_process_status = Checkbutton(self.frame2, text="", variable=self.var_show_question_list_process_status, onvalue=1, offvalue=0)
        self.check_show_question_list_process_status.deselect()
        self.check_show_question_list_process_status.grid(row=18, column=3, sticky=W)

        self.var_question_mark = IntVar()
        self.check_question_mark = Checkbutton(self.frame2, text="", variable=self.var_question_mark, onvalue=1, offvalue=0)
        self.check_question_mark.deselect()
        self.check_question_mark.grid(row=19, column=3, sticky=W)

        self.var_overview_answers = IntVar()
        self.check_overview_answers = Checkbutton(self.frame2, text="", variable=self.var_overview_answers, onvalue=1, offvalue=0)
        self.check_overview_answers.grid(row=21, column=3, sticky=W)

        self.var_show_end_comment = IntVar()
        self.check_show_end_comment = Checkbutton(self.frame2, text="", variable=self.var_show_end_comment, onvalue=1, offvalue=0,
                                                  command=lambda v=self.var_show_end_comment: GUI_settings_window.show_concluding_remarks(self, v))
        self.check_show_end_comment.deselect()
        self.check_show_end_comment.grid(row=22, column=3, sticky=W)

        self.var_forwarding = IntVar()
        self.check_forwarding = Checkbutton(self.frame2, text="", variable=self.var_forwarding, onvalue=1, offvalue=0)
        self.check_forwarding.deselect()
        self.check_forwarding.grid(row=23, column=3, sticky=W)

        self.var_notification = IntVar()
        self.check_notification = Checkbutton(self.frame2, text="", variable=self.var_notification, onvalue=1, offvalue=0)
        self.check_notification.deselect()
        self.check_notification.grid(row=24, column=3, sticky=W)

        # --------------------------- RADIO BUTTONS ---------------------------------------

        self.select_question = IntVar()
        self.select_question.set(0)
        self.select_question_radiobtn1 = Radiobutton(self.frame1, text="Fest definierte Fragenauswahl", variable=self.select_question, value=0)
        self.select_question_radiobtn1.grid(row=4, column=1, pady=0, sticky=W)          # FIXED_QUEST_SET
        self.select_question_radiobtn2 = Radiobutton(self.frame1, text="Zufällige Fragenauswahl", variable=self.select_question, value=1)
        self.select_question_radiobtn2.grid(row=5, column=1, pady=0, sticky=W)          # RANDOM_QUEST_SET
        self.select_question_radiobtn3 = Radiobutton(self.frame1, text="Wiedervorlagemodus - alle Fragen eines Fragenpools", variable=self.select_question, value=2)
        self.select_question_radiobtn3.grid(row=6, column=1, pady=0, sticky=W)          # DYNAMIC_QUEST_SET

        self.select_anonym = IntVar()
        self.select_anonym.set(0)
        self.select_anonym_radiobtn1 = Radiobutton(self.frame1, text="Testergebnisse ohne Namen", variable=self.select_anonym, value=0, borderwidth=0, command=self.select_anonym.get())
        self.select_anonym_radiobtn1.grid(row=7, column=1, pady=0, sticky=W)
        self.select_anonym_radiobtn2 = Radiobutton(self.frame1, text="Testergebnisse mit Namen", variable=self.select_anonym, value=1, borderwidth=0, command=self.select_anonym.get())
        self.select_anonym_radiobtn2.grid(row=8, column=1, pady=0, sticky=W)

        self.select_show_question_title = IntVar()
        self.select_show_question_title.set(0)
        self.select_show_question_title_radiobtn1 = Radiobutton(self.frame2, text="Fragentitel und erreichbare Punkte", variable=self.select_show_question_title, value=0, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn1.grid(row=1, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn2 = Radiobutton(self.frame2, text="Nur Fragentitel", variable=self.select_show_question_title, value=1, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn2.grid(row=2, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn3 = Radiobutton(self.frame2, text="Weder Fragentitel noch erreichbare Punkte", variable=self.select_show_question_title, value=2, borderwidth=0, command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn3.grid(row=3, column=3, pady=0, sticky=W)

        self.select_user_response = IntVar()
        self.select_user_response.set(0)
        self.select_user_response_radiobtn1 = Radiobutton(self.frame2, text="Antworten während des Testdurchlaufs nicht festschreiben", variable=self.select_user_response,value=0, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn1.grid(row=8, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn2 = Radiobutton(self.frame2, text="Antworten bei Anzeige der Rückmeldung festschreiben", variable=self.select_user_response, value=1, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn2.grid(row=9, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn3 = Radiobutton(self.frame2, text="Antworten bei Anzeige der Folgefrage festschreiben", variable=self.select_user_response, value=2, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn3.grid(row=10, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn4 = Radiobutton(self.frame2, text="Antworten mit der Anzeige von Rückmeldungen oder der Folgefrage festschreiben",variable=self.select_user_response, value=3, borderwidth=0, command=self.select_user_response.get())
        self.select_user_response_radiobtn4.grid(row=11, column=3,pady=0, sticky=W)

        self.select_not_answered_questions = IntVar()
        self.select_not_answered_questions.set(0)
        self.select_not_answered_questions_radiobtn1 = Radiobutton(self.frame2, text="Nicht beantwortete Fragen bleiben an ihrem Platz", variable=self.select_not_answered_questions,value=0, borderwidth=0, command=self.select_not_answered_questions.get())
        self.select_not_answered_questions_radiobtn1.grid(row=16, column=3, pady=0, sticky=W)
        self.select_not_answered_questions_radiobtn2 = Radiobutton(self.frame2, text="Nicht beantwortete Fragen werden ans Testende gesschoben", variable=self.select_not_answered_questions, value=1, borderwidth=0, command=self.select_not_answered_questions.get())
        self.select_not_answered_questions_radiobtn2.grid(row=17, column=3, pady=0, sticky=W)

        # --------------------------- ENTRY BOXES ---------------------------------------

        self.titel_entry = Entry(self.frame1, width=47)
        self.titel_entry.grid(row=1, column=1)
        self.introduction_bar = Scrollbar(self.frame1)
        self.introduction_infobox = Text(self.frame1, height=4, width=40, font=('Helvetica', 9))



        self.test_start_year_entry = Entry(self.frame1, width=5)
        self.test_start_year_entry.grid(row=18, column=1, sticky=W)
        self.test_start_year_entry.insert(0, "YYYY")
        self.test_start_month_entry = Entry(self.frame1, width=5)
        self.test_start_month_entry.grid(row=18, column=1, sticky=W, padx=35)
        self.test_start_month_entry.insert(0, "MM")
        self.test_start_day_entry = Entry(self.frame1, width=5)
        self.test_start_day_entry.grid(row=18, column=1, sticky=W, padx=70)
        self.test_start_day_entry.insert(0, "DD")
        self.test_start_hour_entry = Entry(self.frame1, width=5)
        self.test_start_hour_entry.grid(row=18, column=1, sticky=W, padx=105)
        self.test_start_hour_entry.insert(0, "HH")
        self.test_start_minute_entry = Entry(self.frame1, width=5)
        self.test_start_minute_entry.grid(row=18, column=1, sticky=W, padx=140)
        self.test_start_minute_entry.insert(0, "mm")

        self.test_end_year_entry = Entry(self.frame1, width=5)
        self.test_end_year_entry.grid(row=19, column=1, sticky=W, pady=5)
        self.test_end_year_entry.insert(0, "YYYY")
        self.test_end_month_entry = Entry(self.frame1, width=5)
        self.test_end_month_entry.grid(row=19, column=1, sticky=W, padx=35)
        self.test_end_month_entry.insert(0, "MM")
        self.test_end_day_entry = Entry(self.frame1, width=5)
        self.test_end_day_entry.grid(row=19, column=1, sticky=W, padx=70)
        self.test_end_day_entry.insert(0, "DD")
        self.test_end_hour_entry = Entry(self.frame1, width=5)
        self.test_end_hour_entry.grid(row=19, column=1, sticky=W, padx=105)
        self.test_end_hour_entry.insert(0, "HH")
        self.test_end_minute_entry = Entry(self.frame1, width=5)
        self.test_end_minute_entry.grid(row=19, column=1, sticky=W, padx=140)
        self.test_end_minute_entry.insert(0, "mm")




        self.test_password_entry = Entry(self.frame1, width=20)
        self.test_password_entry.grid(row=20, column=1, sticky=W, pady=3)

        self.description_bar = Scrollbar(self.frame1)
        self.description_infobox = Text(self.frame1, height=4, width=40, font=('Helvetica', 9))
        self.description_bar.grid(row=2, column=2)
        self.description_infobox.grid(row=2, column=1, pady=10)
        self.description_bar.config(command=self.description_infobox.yview)
        self.description_infobox.config(yscrollcommand=self.description_bar.set)

        self.limit_users_max_amount_entry = Entry(self.frame1, width=5)
        self.limit_users_max_amount_entry.grid(row=22, column=1, sticky=W)
        self.inactivity_time_for_users_entry = Entry(self.frame1, width=5)
        self.inactivity_time_for_users_entry.grid(row=23, column=1, sticky=W)
        self.inactivity_time_for_users_entry.insert(0, "300")

        self.limit_test_runs_entry = Entry(self.frame1, width=10)
        self.limit_test_runs_entry.grid(row=25, column=1, sticky=W)
        self.limit_test_runs_entry.insert(0, "3")


        self.limit_time_betw_test_runs_month_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_month_entry.grid(row=26, column=1, sticky=W, pady=5)
        self.limit_time_betw_test_runs_month_entry.insert(0, "MM")
        self.limit_time_betw_test_runs_day_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_day_entry.grid(row=26, column=1, sticky=W, padx=35)
        self.limit_time_betw_test_runs_day_entry.insert(0, "DD")
        self.limit_time_betw_test_runs_hour_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_hour_entry.grid(row=26, column=1, sticky=W, padx=70)
        self.limit_time_betw_test_runs_hour_entry.insert(0, "HH")
        self.limit_time_betw_test_runs_minute_entry = Entry(self.frame1, width=5)
        self.limit_time_betw_test_runs_minute_entry.grid(row=26, column=1, sticky=W, padx=105)
        self.limit_time_betw_test_runs_minute_entry.insert(0, "mm")

        self.limit_processing_time_minutes_entry = Entry(self.frame1, width=5)
        self.limit_processing_time_minutes_entry.grid(row=28, column=1, sticky=W)
        self.limit_processing_time_minutes_entry.insert(0, "90")


        self.concluding_remarks_bar = Scrollbar(self.frame2)
        self.concluding_remarks_infobox = Text(self.frame2, height=4, width=40, font=('Helvetica', 9))



        self.profile_name_label = Label(self.frame3, text="Choose Profilname to save")
        self.profile_name_label.grid(row=0, column=0)

        self.profile_name_entry = Entry(self.frame3, width=15)
        self.profile_name_entry.grid(row=0, column=1)



        #self.profile_oid_label = Label(self.frame3, text="Choose oid to delete")
        #self.profile_oid_label.grid(row=4, column=0)

        self.profile_oid_entry = Entry(self.frame3, width=10)
        self.profile_oid_entry.grid(row=4, column=1)




        self.load_settings_entry = Entry(self.frame3, width=10)
        self.load_settings_entry.grid(row=3, column=1)

        #self.delete_settings_btn = Button(self.frame3, text="Delete Profile from ID", command=GUI_settings_window.profile_save_settings(self))
        #self.delete_settings_btn.grid(row=4, column=0)





        self.profile_oid_listbox_label = Label(self.frame3, text=" DB\nID")
        self.profile_oid_listbox_label.grid(row=1, column=4, sticky=W)

        self.profile_name_listbox_label = Label(self.frame3, text="Name")
        self.profile_name_listbox_label.grid(row=1, column=5, sticky=W)

        self.my_listbox_profile_oid = Listbox(self.frame3, width=5)
        self.my_listbox_profile_oid.grid(row=2, column=4, sticky=W)


        self.my_listbox_profile_name = Listbox(self.frame3, width=15)
        self.my_listbox_profile_name.grid(row=2, column=5, sticky=W)


        self.show_profiles_btn = Button(self.frame3, text="Show Profile from ID", command=lambda: GUI_settings_window.profile_show_db(self))
        self.show_profiles_btn.grid(row=5, column=0)

        self.save_settings_btn = Button(self.frame3, text="Save Settings", command=lambda: GUI_settings_window.profile_save_settings(self))
        self.save_settings_btn.grid(row=2, column=0)

        self.load_settings_btn = Button(self.frame3, text="Load Settings", command=lambda: GUI_settings_window.profile_load_settings(self))
        self.load_settings_btn.grid(row=3, column=0)

        self.delete_profile_btn = Button(self.frame3, text="Delete Profile", command=lambda: GUI_settings_window.profile_delete(self))
        self.delete_profile_btn.grid(row=4, column=0)

        self.create_profile_btn = Button(self.frame3, text="Create Profile-Settings", command=lambda: GUI_settings_window.create_settings(self))
        self.create_profile_btn.grid(row=6, column=0)

    def show_entry_time_limited_start(self, var):
        if var.get() == 0:
            self.time_limited_start_label.grid_forget()
            self.time_limited_start_year_label.grid_forget()
            self.time_limited_start_year_entry.grid_forget()
            self.time_limited_start_month_label.grid_forget()
            self.time_limited_start_month_entry.grid_forget()
            self.time_limited_start_day_label.grid_forget()
            self.time_limited_start_day_entry.grid_forget()
            self.time_limited_start_hour_label.grid_forget()
            self.time_limited_start_hour_entry.grid_forget()
            self.time_limited_start_minute_label.grid_forget()
            self.time_limited_start_minute_entry.grid_forget()

            self.time_limited_end_label.grid_forget()
            self.time_limited_end_year_label.grid_forget()
            self.time_limited_end_year_entry.grid_forget()
            self.time_limited_end_month_label.grid_forget()
            self.time_limited_end_month_entry.grid_forget()
            self.time_limited_end_day_label.grid_forget()
            self.time_limited_end_day_entry.grid_forget()
            self.time_limited_end_hour_label.grid_forget()
            self.time_limited_end_hour_entry.grid_forget()
            self.time_limited_end_minute_label.grid_forget()
            self.time_limited_end_minute_entry.grid_forget()

        else:
            self.time_limited_start_label.grid(row=10, column=1, sticky=W, padx=50)
            self.time_limited_start_day_label.grid(row=11, column=1, sticky=W, padx=30)
            self.time_limited_start_month_label.grid(row=11, column=1, sticky=W, padx=55)
            self.time_limited_start_year_label.grid(row=11, column=1, sticky=W, padx=80)
            self.time_limited_start_hour_label.grid(row=11, column=1, sticky=W, padx=110)
            self.time_limited_start_minute_label.grid(row=11, column=1, sticky=W, padx=135)

            self.time_limited_end_label.grid(row=10, column=1, sticky=E, padx=50)
            self.time_limited_end_day_label.grid(row=11, column=1, sticky=E, padx=110)
            self.time_limited_end_month_label.grid(row=11, column=1, sticky=E, padx=85)
            self.time_limited_end_year_label.grid(row=11, column=1, sticky=E, padx=55)
            self.time_limited_end_hour_label.grid(row=11, column=1, sticky=E, padx=30)
            self.time_limited_end_minute_label.grid(row=11, column=1, sticky=E, padx=5)

            self.time_limited_start_day_entry.grid(row=12, column=1, sticky=W, padx=30)
            self.time_limited_start_month_entry.grid(row=12, column=1, sticky=W, padx=55)
            self.time_limited_start_year_entry.grid(row=12, column=1, sticky=W, padx=80)
            self.time_limited_start_hour_entry.grid(row=12, column=1, sticky=W, padx=110)
            self.time_limited_start_minute_entry.grid(row=12, column=1, sticky=W, padx=135)

            self.time_limited_end_day_entry.grid(row=12, column=1, sticky=E, padx=110)
            self.time_limited_end_month_entry.grid(row=12, column=1, sticky=E, padx=85)
            self.time_limited_end_year_entry.grid(row=12, column=1, sticky=E, padx=55)
            self.time_limited_end_hour_entry.grid(row=12, column=1, sticky=E, padx=30)
            self.time_limited_end_minute_entry.grid(row=12, column=1, sticky=E, padx=5)

    def show_introduction_textfield(self, introduction_var):
        print(introduction_var.get())
        if introduction_var.get() == 0:

            self.introduction_bar.grid_forget()
            self.introduction_infobox.grid_forget()

        else:
            self.introduction_bar.grid(row=15, column=1, sticky=E)
            self.introduction_infobox.grid(row=15, column=1, padx=30)
            self.introduction_bar.config(command=self.introduction_infobox.yview)
            self.introduction_infobox.config(yscrollcommand=self.introduction_bar.set)

    def enable_autosave(self, var):
        if var.get() == 0:
           self.check_autosave_interval_entry.grid_forget()
           self.check_autosave_interval_label.grid_forget()

        else:
            self.check_autosave_interval_entry.grid(row=4, column=3, padx=10)
            self.check_autosave_interval_label.grid(row=4, column=3, padx=50, sticky=W)

    def show_concluding_remarks(self, var):
        if var.get() == 0:
            self.concluding_remarks_bar.grid_forget()
            self.concluding_remarks_infobox.grid_forget()

        else:
            self.concluding_remarks_bar.grid(row=22, column=3, sticky=E)
            self.concluding_remarks_infobox.grid(row=22, column=3, padx=30)
            self.concluding_remarks_bar.config(command=self.concluding_remarks_infobox.yview)
            self.concluding_remarks_infobox.config(yscrollcommand=self.concluding_remarks_bar.set)

    def profile_show_db(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_profiles_table")
        profile_records = c.fetchall()

        # Clear List Boxes

        self.my_listbox_profile_name.delete(0, END)
        self.my_listbox_profile_oid.delete(0, END)

        # Loop thru Results
        for profile_record in profile_records:
            self.my_listbox_profile_name.insert(END, profile_record[0])
            self.my_listbox_profile_oid.insert(END, profile_record[len(profile_record)-1])



        self.profile_records_len = len(profile_records)
        #print(profile_records[len(profile_records)-1])

        conn.commit()
        conn.close()
        print("LOOP THROUGH... SHOW PROFILES!")



    def profile_save_settings(self):


        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        # Insert into Table
        c.execute(
            "INSERT INTO my_profiles_table VALUES ("
            ":profile_name, :entry_description, :radio_select_question, :radio_select_anonymous, :check_online, :check_time_limited, "
            ":check_introduction, :entry_introduction, :check_test_properties, "
            ":entry_test_start_year, :entry_test_start_month, :entry_test_start_day, :entry_test_start_hour, :entry_test_start_minute,"
            ":entry_test_end_year, :entry_test_end_month, :entry_test_end_day, :entry_test_end_hour, :entry_test_end_minute,"
            ":entry_test_password, :check_specific_users, :entry_limit_users, :entry_user_inactivity, :entry_limit_test_runs,"
            ":entry_limit_time_betw_test_run_month, :entry_limit_time_betw_test_run_day, :entry_limit_time_betw_test_run_hour, :entry_limit_time_betw_test_run_minute,"
            ":check_processing_time, :entry_processing_time_in_minutes, :check_processing_time_reset,"
            ":check_examview, :check_examview_titel, :check_examview_username, :check_show_ilias_nr,"
            ":radio_select_show_question_title, :check_autosave, :entry_autosave_interval, :check_mix_questions, :check_show_solution_notes, :check_direct_response,"
            ":radio_select_user_response, :check_mandatory_questions, :check_use_previous_solution, :check_show_test_cancel, :radio_select_not_answered_questions,"
            ":check_show_question_list_process_status, :check_question_mark, :check_overview_answers, :check_show_end_comment, :entry_end_comment, :check_forwarding, :check_notification)",
            {
                'profile_name': self.profile_name_entry.get(),
                'entry_description': self.description_infobox.get("1.0", 'end-1c'),
                'radio_select_question': self.select_question.get(),
                'radio_select_anonymous': self.select_anonym.get(),
                'check_online': self.var_online.get(),
                'check_time_limited': self.var_time_limited.get(),

                'check_introduction': self.var_introduction.get(),
                'entry_introduction': self.introduction_infobox.get("1.0", 'end-1c'),
                'check_test_properties': self.var_test_prop.get(),

                'entry_test_start_year': self.test_start_year_entry.get(),
                'entry_test_start_month': self.test_start_month_entry.get(),
                'entry_test_start_day': self.test_start_day_entry.get(),
                'entry_test_start_hour': self.test_start_hour_entry.get(),
                'entry_test_start_minute': self.test_start_minute_entry.get(),

                'entry_test_end_year': self.test_end_year_entry.get(),
                'entry_test_end_month': self.test_end_month_entry.get(),
                'entry_test_end_day': self.test_end_day_entry.get(),
                'entry_test_end_hour': self.test_end_hour_entry.get(),
                'entry_test_end_minute': self.test_end_minute_entry.get(),


                'entry_test_password': self.test_password_entry.get(),
                'check_specific_users': self.var_specific_users.get(),
                'entry_limit_users': self.limit_users_max_amount_entry.get(),
                'entry_user_inactivity': self.inactivity_time_for_users_entry.get(),
                'entry_limit_test_runs': self.limit_test_runs_entry.get(),

                'entry_limit_time_betw_test_run_month': self.limit_time_betw_test_runs_month_entry.get(),
                'entry_limit_time_betw_test_run_day': self.limit_time_betw_test_runs_day_entry.get(),
                'entry_limit_time_betw_test_run_hour': self.limit_time_betw_test_runs_hour_entry.get(),
                'entry_limit_time_betw_test_run_minute': self.limit_time_betw_test_runs_minute_entry.get(),

                'check_processing_time': self.var_processing_time.get(),
                'entry_processing_time_in_minutes': self.limit_processing_time_minutes_entry.get(),
                'check_processing_time_reset': self.var_processing_time_reset.get(),
                
                'check_examview': self.var_examview.get(),
                'check_examview_titel': self.var_examview_test_title.get(),
                'check_examview_username': self.var_examview_user_name.get(),
                'check_show_ilias_nr': self.var_show_ilias_nr.get(),

                'radio_select_show_question_title': self.select_show_question_title.get(),
                'check_autosave': self.var_autosave.get(),
                'entry_autosave_interval': self.check_autosave_interval_entry.get(),
                'check_mix_questions': self.var_mix_questions.get(),
                'check_show_solution_notes': self.var_show_solution_notes.get(),
                'check_direct_response': self.var_direct_response.get(),

                'radio_select_user_response': self.select_user_response.get(),
                'check_mandatory_questions': self.var_mandatory_questions.get(),
                'check_use_previous_solution' : self.var_use_previous_solution.get(),
                'check_show_test_cancel': self.var_show_test_cancel.get(),
                'radio_select_not_answered_questions': self.select_not_answered_questions.get(),

                'check_show_question_list_process_status': self.var_show_question_list_process_status.get(),
                'check_question_mark': self.var_question_mark.get(),
                'check_overview_answers': self.var_overview_answers.get(),
                'check_show_end_comment': self.var_show_end_comment.get(),
                'entry_end_comment': self.concluding_remarks_infobox.get("1.0", 'end-1c'),
                'check_forwarding': self.var_forwarding.get(),
                'check_notification': self.var_notification.get()


            }
        )
        conn.commit()
        conn.close()
        print("GOT VALUES")

    def profile_load_settings(self):
        print("LOAD")

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("SELECT * FROM my_profiles_table WHERE oid =" + self.load_settings_entry.get())



        profile_records = c.fetchall()
        # Loop thru Results
        for profile_record in profile_records:
            self.profile_name_entry.get()
        #   profil_name_entry -> profile_record[0]
            self.description_infobox.delete('1.0', END)
            self.description_infobox.insert('1.0', profile_record[1])
            self.select_question.set(profile_record[2])
            self.select_anonym.set(profile_record[3])
            self.var_online.set(profile_record[4])
            self.var_time_limited.set(profile_record[5])
            self.var_introduction.set(profile_record[6])
            self.introduction_infobox.delete('1.0', END)
            self.introduction_infobox.insert('1.0', profile_record[7])
            self.var_test_prop.set(profile_record[8])

            self.test_start_year_entry.delete(0, END)
            self.test_start_year_entry.insert(0, profile_record[9])
            self.test_start_month_entry.delete(0, END)
            self.test_start_month_entry.insert(0, profile_record[10])
            self.test_start_day_entry.delete(0, END)
            self.test_start_day_entry.insert(0, profile_record[11])
            self.test_start_hour_entry.delete(0, END)
            self.test_start_hour_entry.insert(0, profile_record[12])
            self.test_start_minute_entry.delete(0, END)
            self.test_start_minute_entry.insert(0, profile_record[13])

            self.test_end_year_entry.delete(0, END)
            self.test_end_year_entry.insert(0, profile_record[14])
            self.test_end_month_entry.delete(0, END)
            self.test_end_month_entry.insert(0, profile_record[15])
            self.test_end_day_entry.delete(0, END)
            self.test_end_day_entry.insert(0, profile_record[16])
            self.test_end_hour_entry.delete(0, END)
            self.test_end_hour_entry.insert(0, profile_record[17])
            self.test_end_minute_entry.delete(0, END)
            self.test_end_minute_entry.insert(0, profile_record[18])

            self.test_password_entry.delete(0, END)
            self.test_password_entry.insert(0, profile_record[19])
            self.var_specific_users.set(profile_record[20])
            self.limit_users_max_amount_entry.delete(0, END)
            self.limit_users_max_amount_entry.insert(0, profile_record[21])
            self.inactivity_time_for_users_entry.delete(0, END)
            self.inactivity_time_for_users_entry.insert(0, profile_record[22])
            self.limit_test_runs_entry.delete(0, END)
            self.limit_test_runs_entry.insert(0, profile_record[23])

            self.limit_time_betw_test_runs_month_entry.delete(0, END)
            self.limit_time_betw_test_runs_month_entry.insert(0, profile_record[24])
            self.limit_time_betw_test_runs_day_entry.delete(0, END)
            self.limit_time_betw_test_runs_day_entry.insert(0, profile_record[25])
            self.limit_time_betw_test_runs_hour_entry.delete(0, END)
            self.limit_time_betw_test_runs_hour_entry.insert(0, profile_record[26])
            self.limit_time_betw_test_runs_minute_entry.delete(0, END)
            self.limit_time_betw_test_runs_minute_entry.insert(0, profile_record[27])

            self.var_processing_time.set(profile_record[28])
            self.limit_processing_time_minutes_entry.delete(0, END)
            self.limit_processing_time_minutes_entry.insert(0, profile_record[29])
            self.var_processing_time_reset.set(profile_record[30])

            self.var_examview.set(profile_record[31])
            self.var_examview_test_title.set(profile_record[32])
            self.var_examview_user_name.set(profile_record[33])
            self.var_show_ilias_nr.set(profile_record[34])
            self.select_show_question_title.set(profile_record[35])
            self.var_autosave.set(profile_record[36])
            self.check_autosave_interval_entry.delete(0, END)
            self.check_autosave_interval_entry.insert(0, profile_record[37])
            self.var_mix_questions.set(profile_record[38])
            self.var_show_solution_notes.set(profile_record[39])
            self.var_direct_response.set(profile_record[40])
            self.select_user_response.set(profile_record[41])
            self.var_mandatory_questions.set(profile_record[42])
            self.var_use_previous_solution.set(profile_record[43])
            self.var_show_test_cancel.set(profile_record[44])
            self.select_not_answered_questions.set(profile_record[45])
            self.var_show_question_list_process_status.set(profile_record[46])
            self.var_question_mark.set(profile_record[47])
            self.var_overview_answers.set(profile_record[48])
            self.var_show_end_comment.set(profile_record[49])
            self.concluding_remarks_infobox.delete('1.0', END)
            self.concluding_remarks_infobox.insert('1.0', profile_record[50])
            self.var_forwarding.set(profile_record[51])
            self.var_notification.set(profile_record[52])

        conn.commit()
        conn.close()

    def profile_delete(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()

        c.execute("DELETE from my_profiles_table WHERE oid= " + self.profile_oid_entry.get())

        #self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()

    def profile_delete_last(self):

        conn = sqlite3.connect('test_settings_profiles_db.db')
        c = conn.cursor()
        self.profile_oid_entry.insert(0, self.profile_records_len)
        c.execute("DELETE from my_profiles_table WHERE oid= " + self.profile_oid_entry.get())
        print("LAST DB ENTRY DELETED")
        #self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()



    # For create test settings -->  Toplevel must be opened (Test-Settings Window)
    def create_settings(self):
        try:
            #profile_name --> profile_record[0]_
            self.description = self.description_infobox.get('1.0', 'end-1c')
            self.question_type = self.select_question.get()
            self.anonym = self.select_anonym.get()
            self.online = self.var_online.get()
            self.time_limited = self.var_time_limited.get()
            self.introduction_check = self.var_introduction.get()
            self.introduction_text = self.introduction_infobox.get('1.0', 'end-1c')
            self.test_prop = self.var_test_prop.get()

            self.test_start_year = self.test_start_year_entry.get()
            self.test_start_month=  self.test_start_month_entry.get()
            self.test_start_day=  self.test_start_day_entry.get()
            self.test_start_hour=  self.test_start_hour_entry.get()
            self.test_start_minute=  self.test_start_minute_entry.get()

            self.test_end_year = self.test_end_year_entry.get()
            self.test_end_month= self.test_end_month_entry.get()
            self.test_end_day= self.test_end_day_entry.get()
            self.test_end_hour= self.test_end_hour_entry.get()
            self.test_end_minute= self.test_end_minute_entry.get()

            self.test_password = self.test_password_entry.get()
            self.specific_users = self.var_specific_users.get()
            self.limit_users_max = self.limit_users_max_amount_entry.get()
            self.inactivity_time_for_users = self.inactivity_time_for_users_entry.get()
            self.limit_test_runs = self.limit_test_runs_entry.get()

            self.limit_time_betw_test_runs_month = self.limit_time_betw_test_runs_month_entry.get()
            self.limit_time_betw_test_runs_day = self.limit_time_betw_test_runs_day_entry.get()
            self.limit_time_betw_test_runs_hour = self.limit_time_betw_test_runs_hour_entry.get()
            self.limit_time_betw_test_runs_minute = self.limit_time_betw_test_runs_minute_entry.get()

            self.processing_time = self.var_processing_time.get()
            self.limit_processing_time_minutes = self.limit_processing_time_minutes_entry.get()
            self.check_processing_time_reset = self.var_processing_time_reset.get()

            self.examview = self.var_examview.get()
            self.examview_test_title = self.var_examview_test_title.get()
            self.examview_user_name = self.var_examview_user_name.get()
            self.show_ilias_nr = self.var_show_ilias_nr.get()
            self.show_question_title = self.select_show_question_title.get()
            self.autosave = self.var_autosave.get()
            self.autosave_interval = self.check_autosave_interval_entry.get()

            self.mix_questions = self.var_mix_questions.get()
            self.show_solution_notes = self.var_show_solution_notes.get()
            self.direct_response = self.var_direct_response.get()
            self.user_response = self.select_user_response.get()
            self.mandatory_questions = self.var_mandatory_questions.get()
            self.use_previous_solution = self.var_use_previous_solution.get()
            self.show_test_cancel = self.var_show_test_cancel.get()
            self.not_answered_questions = self.select_not_answered_questions.get()
            self.show_question_list_process_status = self.var_show_question_list_process_status.get()
            self.question_mark = self.var_question_mark.get()
            self.overview_answers = self.var_overview_answers.get()
            self.show_end_comment = self.var_show_end_comment.get()
            self.concluding_remarks = self.concluding_remarks_infobox.get("1.0", 'end-1c')
            self.forwarding = self.var_forwarding.get()
            self.notification = self.var_notification.get()


            self.mytree = ET.parse(self.qti_file_path_write)
            self.myroot = self.mytree.getroot()

            # hours_from_minutes = str(datetime.timedelta(minutes=int(self.limit_processing_time_minutes)))
            self.duration_time = int(self.limit_processing_time_minutes)
            self.duration_time_hours = self.duration_time // 60
            self.duration_time_minutes = self.duration_time % 60


            # Format of duration: P0Y0M0DT1H30M0S
            self.duration = "P0Y0M0DT" + str(self.duration_time_hours) + "H" + str(self.duration_time_minutes) + "M0S"


            for qticomment in self.myroot.iter('qticomment'):
                qticomment.text = self.description
                break


            for duration in self.myroot.iter('duration'):
                duration.text = self.duration
                break

            questestinterop = ET.Element('questestinterop')
            assessment = ET.SubElement(questestinterop, 'assessment')
            qticomment = ET.SubElement(assessment, 'qticomment')
            qticomment.text = self.description

            for qtimetadatafield in self.myroot.iter('qtimetadatafield'):

                if qtimetadatafield.find('fieldlabel').text == "anonymity":
                    qtimetadatafield.find('fieldentry').text = self.anonym
                    if self.anonym == "":
                        qtimetadatafield.find('fieldentry').text = "0"
                        print("NO ENTRY IN <ANONYM>")


                if qtimetadatafield.find('fieldlabel').text == "question_set_type":
                    if self.question_type == 0:
                        qtimetadatafield.find('fieldentry').text = "FIXED_QUEST_SET"
                        #print("WRITE FIXED-Question")

                    elif self.question_type == 1:
                        qtimetadatafield.find('fieldentry').text = "RANDOM_QUEST_SET"
                        #print("WRITE RANDOM-Question")

                    elif self.question_type == 2:
                        qtimetadatafield.find('fieldentry').text = "DYNAMIC_QUEST_SET"
                        #print("WRITE DYNAMIC-Question")
                    else:
                        qtimetadatafield.find('fieldentry').text = "FIXED_QUEST_SET"
                        print("NO ENTRY IN <QUESTION_TYPE> ")

                #if qtimetadatafield.find('fieldlabel').text == "author":
                    #qtimetadatafield.find('fieldentry').text = str(Formelfrage.autor_entry.get())

                if qtimetadatafield.find('fieldlabel').text == "reset_processing_time":
                    qtimetadatafield.find('fieldentry').text = str(self.check_processing_time_reset)
                    if self.check_processing_time_reset == "":
                        qtimetadatafield.find('fieldentry').text = "0"
                        print("NO ENTRY IN <RESET PROCESSING TIME>")

                if qtimetadatafield.find('fieldlabel').text == "password":
                    qtimetadatafield.find('fieldentry').text = str(self.test_password)


                if qtimetadatafield.find('fieldlabel').text == "allowedUsers":
                    qtimetadatafield.find('fieldentry').text = str(self.limit_users_max)

                if qtimetadatafield.find('fieldlabel').text == "allowedUsersTimeGap":
                    qtimetadatafield.find('fieldentry').text = str(self.inactivity_time_for_users)

                if qtimetadatafield.find('fieldlabel').text == "nr_of_tries":
                    qtimetadatafield.find('fieldentry').text = str(self.limit_test_runs)

                if qtimetadatafield.find('fieldlabel').text == "pass_waiting":
                   qtimetadatafield.find('fieldentry').text = str(self.limit_time_betw_test_runs_month) + ":0" + str(self.limit_time_betw_test_runs_day) + ":" + str(self.limit_time_betw_test_runs_hour) + ":" + str(self.limit_time_betw_test_runs_minute) + ":00"
                   if self.limit_time_betw_test_runs_month == "MM":
                        qtimetadatafield.find('fieldentry').text = "00:000:00:00:00"
                        print(" >WARNING< NO limit_time_betw_test_runs SET.. --> set limit_time to \"00:000:00:00:00\" ")


                #Prüfungsansicht: Alle drei haken (Titel+Ansicht): "7" / Zwei Haken (Titel) = "3" / Zwei Haken (Name) = "5" / Ein Haken = "1" / "0" -> deaktiviert
                if qtimetadatafield.find('fieldlabel').text == "kiosk":
                    if self.examview == 0:
                        qtimetadatafield.find('fieldentry').text = "0"
                    elif self.examview == 1:
                        qtimetadatafield.find('fieldentry').text = "1"
                    elif self.examview == 1 and self.examview_test_title == 1:
                        qtimetadatafield.find('fieldentry').text = "3"
                    elif self.examview == 1 and self.examview_user_name == 1:
                        qtimetadatafield.find('fieldentry').text = "5"
                    elif self.examview == 1 and self.examview_user_name == 1 and self.examview_test_title == 1:
                        qtimetadatafield.find('fieldentry').text = "7"




                #if qtimetadatafield.find('fieldlabel').text == "use_previous_answers":
                    #qtimetadatafield.find('fieldentry').text = "0"

                #if qtimetadatafield.find('fieldlabel').text == "title_output":
                    #qtimetadatafield.find('fieldentry').text = "0"

                #if qtimetadatafield.find('fieldlabel').text == "examid_in_test_pass":
                    #qtimetadatafield.find('fieldentry').text = "0"

               #if qtimetadatafield.find('fieldlabel').text == "show_summary":
                    #qtimetadatafield.find('fieldentry').text = "0"

                if qtimetadatafield.find('fieldlabel').text == "show_cancel":
                    qtimetadatafield.find('fieldentry').text = str(self.show_test_cancel)

                #if qtimetadatafield.find('fieldlabel').text == "show_marker":
                    #qtimetadatafield.find('fieldentry').text = "99"

                #if qtimetadatafield.find('fieldlabel').text == "fixed_participants":
                   #qtimetadatafield.find('fieldentry').text = "99"

              #  if qtimetadatafield.find('fieldlabel').text == "showinfo":
                    #qtimetadatafield.find('fieldentry').text = "99"

                if qtimetadatafield.find('fieldlabel').text == "shuffle_questions":
                    qtimetadatafield.find('fieldentry').text = str(self.mix_questions)

                if qtimetadatafield.find('fieldlabel').text == "processing_time":

                    #self.minutes = self.limit_processing_time_minutes
                    hours_from_minutes = str(datetime.timedelta(minutes=int(self.limit_processing_time_minutes)))
                    print("len_min_to_hours: " + str(hours_from_minutes))

                    qtimetadatafield.find('fieldentry').text = "0" + hours_from_minutes

                if qtimetadatafield.find('fieldlabel').text == "enable_examview":
                    qtimetadatafield.find('fieldentry').text = str(self.examview)

                #if qtimetadatafield.find('fieldlabel').text == "show_examview_pdf":
                    #qtimetadatafield.find('fieldentry').text = "99"

                if qtimetadatafield.find('fieldlabel').text == "starting_time":
                    qtimetadatafield.find('fieldentry').text = "P" + str(self.test_start_year) + "Y" + str(self.test_start_month) + "M" +  str(self.test_start_day) + "DT" + str(self.test_start_hour) + "H" + str(self.test_start_minute) + "M" + "0S"
                    if self.test_start_year == "YYYY":
                        qtimetadatafield.find('fieldentry').text = "P2020Y1M1DT00H0M0S"
                        print(" >WARNING< NO STARTING TIME SET.. --> set START to \"P2020Y1M1DT00H0M0S\"")


                if qtimetadatafield.find('fieldlabel').text == "ending_time":
                    qtimetadatafield.find('fieldentry').text = "P" + str(self.test_end_year) + "Y" + str(self.test_end_month) + "M" +  str(self.test_end_day) + "DT" + str(self.test_end_hour) + "H" + str(self.test_end_minute) + "M" + "0S"
                    if self.test_end_year == "YYYY":
                        qtimetadatafield.find('fieldentry').text = "P2020Y12M30DT00H0M0S"
                        print(" >WARNING< NO ENDING TIME SET.. --> set END to \"P2020Y12M30DT00H0M0S\"")


                if qtimetadatafield.find('fieldlabel').text == "autosave":
                    qtimetadatafield.find('fieldentry').text = str(self.autosave)

                if qtimetadatafield.find('fieldlabel').text == "autosave_ival":
                    qtimetadatafield.find('fieldentry').text = str(self.autosave_interval)

                #if qtimetadatafield.find('fieldlabel').text == "offer_question_hints":
                    #qtimetadatafield.find('fieldentry').text = "99"

                #if qtimetadatafield.find('fieldlabel').text == "obligations_enabled":
                    #qtimetadatafield.find('fieldentry').text = "99"

                if qtimetadatafield.find('fieldlabel').text == "enable_processing_time":
                    qtimetadatafield.find('fieldentry').text = str(self.processing_time)

                #if qtimetadatafield.find('fieldlabel').text == "mark_step_0":
                    #qtimetadatafield.find('fieldentry').text = "99"

                #if qtimetadatafield.find('fieldlabel').text == "mark_step_1":
                    #qtimetadatafield.find('fieldentry').text = "99"

                #tree = ET.ElementTree(questestinterop)
                #tree.write("WORKED_neuerAnfang.xml")

            print("Write Test_Settings to File")
            self.mytree.write(self.qti_file_path_write)
            print("Create Test WITH Test_settings")
        except:
            e = sys.exc_info()[0]
            print('\033[91m' + "Error: %s" % e + '\033[0m')
            print('\033[91m' +"To use Test-Settings properly, the \"Test_settings\"-window must be opened when create the question"+ '\033[0m')


# print("--------------------3-----------------------------")


app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()
#def save_settings_to_database():









def trash_class():
    """
   """
def trash():
    """   
        class updateFormelFrage(Formelfrage):
    def __init__(self):
        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()
        records = c.fetchall()
        self.record_id = self.create_formelfrage_entry.get()

       ##### FILL ENTRY FIELDS TO EDIT

        # Loop thru Results
        for record in records:
            #formula_entry_editor.insert(0, record[0])

            self.formula_title_entry = str(record[0])
            self.formula_description_entry = str(record[1])
            self.formula_question_entry = str(record[2])



            self.var1_min_entry = str(record[4])
            self.var1_max_entry = str(record[5])
            self.var1_prec_entry = str(record[6])
            self.var1_divby_entry = str(record[7])

            self.var2_min_entry = str(record[8])
            self.var2_max_entry = str(record[9])
            self.var2_prec_entry = str(record[10])
            self.var2_divby_entry = str(record[11])

            self.var3_min_entry = str(record[12])
            self.var3_max_entry = str(record[13])
            self.var3_prec_entry = str(record[14])
            self.var3_divby_entry = str(record[15])

            self.var4_min_entry = str(record[16])
            self.var4_max_entry = str(record[17])
            self.var4_prec_entry = str(record[18])
            self.var4_divby_entry = str(record[19])

            self.var5_min_entry = str(record[20])
            self.var5_max_entry = str(record[21])
            self.var5_prec_entry = str(record[22])
            self.var5_divby_entry = str(record[23])

            self.var6_min_entry = str(record[24])
            self.var6_max_entry = str(record[25])
            self.var6_prec_entry = str(record[26])
            self.var6_divby_entry = str(record[27])

            self.var7_min_entry = str(record[28])
            self.var7_max_entry = str(record[29])
            self.var7_prec_entry = str(record[30])
            self.var7_divby_entry = str(record[31])

            self.res1_min_entry = str(record[32])
            self.res1_max_entry = str(record[33])
            self.res1_prec_entry = str(record[34])
            self.res1_tol_entry = str(record[35])
            self.res1_points_entry = str(record[36])
            self.res1_formula_entry = str(record[3])

            self.res2_min_entry = str(record[37])
            self.res2_max_entry = str(record[38])
            self.res2_prec_entry = str(record[39])
            self.res2_tol_entry = str(record[40])
            self.res2_points_entry = str(record[41])
            self.res2_formula_entry = str(record[49])

            self.res3_min_entry = str(record[42])
            self.res3_max_entry = str(record[43])
            self.res3_prec_entry = str(record[44])
            self.res3_tol_entry = str(record[45])
            self.res3_points_entry = str(record[46])
            self.res3_formula_entry = str(record[50])

            #self.img_name_entry = str(record[47])
            #self.img_data_entry = str(record[48])
            #self.test_time_entry = str(record[51])
            #self.oid_entry = str(record[52])


       #### UPDATE DATABASE ENTRY
        c.execute(""""""UPDATE my_table SET
                
                formula_title = :formula_title
                formula_description_title = :formula_description_title
                formula_description = :formula_description
                
                res1_formula = :res1_formula
                var1_min = :var1_min,
                var1_max = :var1_max,
                var1_prec = :var1_prec,
                var1_divby = :var1_divby,

                var2_min = :var2_min,
                var2_max = :var2_max,
                var2_prec = :var2_prec,
                var2_divby = :var2_divby,

                var3_min = :var3_min,
                var3_max = :var3_max,
                var3_prec = :var3_prec,
                var3_divby = :var3_divby,
                
                var4_min = :var4_min,
                var4_max = :var4_max,
                var4_prec = :var4_prec,
                var4_divby = :var4_divby,
                
                var5_min = :var5_min,
                var5_max = :var5_max,
                var5_prec = :var5_prec,
                var5_divby = :var5_divby,
                
                var6_min = :var6_min,
                var6_max = :var6_max,
                var6_prec = :var6_prec,
                var6_divby = :var6_divby,
                
                var7_min = :var7_min,
                var7_max = :var7_max,
                var7_prec = :var7_prec,
                var7_divby = :var7_divby,


                res1_min = :res1_min,
                res1_max = :res1_max,
                res1_prec = :res1_prec,
                res1_tol = :res1_tol,
                res1_points = :res1_points
                
                
                res2_min = :res2_min,
                res2_max = :res2_max,
                res2_prec = :res2_prec,
                res2_tol = :res2_tol,
                res2_points = :res2_points
                res3_formula = :res2_formula   
                
                res3_min = :res3_min,
                res3_max = :res3_max,
                res3_prec = :res3_prec,
                res3_tol = :res3_tol,
                res3_points = :res3_points
                res3_formula = :res3_formula
                
                WHERE oid = :oid"""""",
                  {'formula': self.res1_formula_entry.get(),
                   'var1_min': self.var1_min_entry.get(),
                   'var1_max': self.var1_max_entry.get(),
                   'var1_prec': self.var1_prec_entry.get(),
                   'var1_divby': self.var1_divby_entry.get(),

                   'var2_min': self.var2_min_entry.get(),
                   'var2_max': self.var2_max_entry.get(),
                   'var2_prec': self.var2_prec_entry.get(),
                   'var2_divby': self.var2_divby_entry.get(),

                   'var3_min': self.var3_min_entry.get(),
                   'var3_max': self.var3_max_entry.get(),
                   'var3_prec': self.var3_prec_entry.get(),
                   'var3_divby': self.var3_divby_entry.get(),

                   'var4_min': self.var4_min_entry.get(),
                   'var4_max': self.var4_max_entry.get(),
                   'var4_prec': self.var4_prec_entry.get(),
                   'var4_divby': self.var4_divby_entry.get(),

                   'var5_min': self.var5_min_entry.get(),
                   'var5_max': self.var5_max_entry.get(),
                   'var5_prec': self.var5_prec_entry.get(),
                   'var5_divby': self.var5_divby_entry.get(),

                   'var6_min': self.var6_min_entry.get(),
                   'var6_max': self.var6_max_entry.get(),
                   'var6_prec': self.var6_prec_entry.get(),
                   'var6_divby': self.var6_divby_entry.get(),

                   'var7_min': self.var7_min_entry.get(),
                   'var7_max': self.var7_max_entry.get(),
                   'var7_prec': self.var7_prec_entry.get(),
                   'var7_divby': self.var7_divby_entry.get(),

                   'res1_min': self.res1_min_entry.get(),
                   'res1_max': self.res1_max_entry.get(),
                   'res1_prec': self.res1_prec_entry.get(),
                   'res1_tol': self.res1_tol_entry.get(),
                   'res1_points': self.res1_points_entry.get(),

                   'res2_min': self.res2_min_entry.get(),
                   'res2_max': self.res2_max_entry.get(),
                   'res2_prec': self.res2_prec_entry.get(),
                   'res2_tol': self.res2_tol_entry.get(),
                   'res2_points': self.res2_points_entry.get(),

                   'res3_min': self.res3_min_entry.get(),
                   'res3_max': self.res3_max_entry.get(),
                   'res3_prec': self.res3_prec_entry.get(),
                   'res3_tol': self.res3_tol_entry.get(),
                   'res3_points': self.res3_points_entry.get(),

                   'oid': self.record_id
                   })
     
        
     
    

        def expand_db(self):

        #self.expand_db_window = Tk()
        #self.expand_db_window.geometry('300x500')

        self.test_window = Tk()

        # Create a ScrolledFrame widget
        self.sf = ScrolledFrame(self.test_window, width=800, height=300)
        self.sf.grid()

        # Bind the arrow keys and scroll wheel
        self.sf.bind_arrow_keys(app)
        self.sf.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.inner_frame = self.sf.display_widget(Frame)


        # CREATE FULL-LISTBOX LABELS IN NEW WINDOW
        self.title_listbox_label = Label(self.inner_frame, text="Title", width=15)
        # self.title_listbox_label.grid(row=25, column=1, sticky=W, pady=(20, 0))


        self.description_listbox_label = Label(self.inner_frame, text="Description", width=15)
        self.description_listbox_label.grid(row=25, column=2, sticky=W)

        self.formula_listbox_label = Label(self.inner_frame, text="Formula", width=15)
        self.formula_listbox_label.grid(row=25, column=3, sticky=W)

        self.var1_min_listbox_label = Label(self.inner_frame, text="var1\nmin")
        self.var1_min_listbox_label.grid(row=25, column=4, sticky=W)
        self.var1_max_listbox_label = Label(self.inner_frame, text="var1\nmax")
        self.var1_max_listbox_label.grid(row=25, column=5, sticky=W)
        self.var1_prec_listbox_label = Label(self.inner_frame, text="var1\nprec")
        self.var1_prec_listbox_label.grid(row=25, column=6, sticky=W)
        self.var1_divby_listbox_label = Label(self.inner_frame, text="var1\ndivby")
        self.var1_divby_listbox_label.grid(row=25, column=7, sticky=W)

        self.var2_min_listbox_label = Label(self.inner_frame, text="var2\nmin")
        self.var2_min_listbox_label.grid(row=25, column=8, sticky=W)
        self.var2_max_listbox_label = Label(self.inner_frame, text="var2\nmax")
        self.var2_max_listbox_label.grid(row=25, column=9, sticky=W)
        self.var2_prec_listbox_label = Label(self.inner_frame, text="var2\nprec")
        self.var2_prec_listbox_label.grid(row=25, column=10, sticky=W)
        self.var2_divby_listbox_label = Label(self.inner_frame, text="var2\ndivby")
        self.var2_divby_listbox_label.grid(row=25, column=11, sticky=W)

        self.var3_min_listbox_label = Label(self.inner_frame, text="var3\nmin")
        self.var3_min_listbox_label.grid(row=25, column=12, sticky=W)
        self.var3_max_listbox_label = Label(self.inner_frame, text="var3\nmax")
        self.var3_max_listbox_label.grid(row=25, column=13, sticky=W)
        self.var3_prec_listbox_label = Label(self.inner_frame, text="var3\nprec")
        self.var3_prec_listbox_label.grid(row=25, column=14, sticky=W)
        self.var3_divby_listbox_label = Label(self.inner_frame, text="var3\ntol")
        self.var3_divby_listbox_label.grid(row=25, column=15, sticky=W)

        self.var4_min_listbox_label = Label(self.inner_frame, text="var4\nmin")
        self.var4_min_listbox_label.grid(row=25, column=16, sticky=W)
        self.var4_max_listbox_label = Label(self.inner_frame, text="var4\nmax")
        self.var4_max_listbox_label.grid(row=25, column=17, sticky=W)
        self.var4_prec_listbox_label = Label(self.inner_frame, text="var4\nprec")
        self.var4_prec_listbox_label.grid(row=25, column=18, sticky=W)
        self.var4_divby_listbox_label = Label(self.inner_frame, text="var4\ntol")
        self.var4_divby_listbox_label.grid(row=25, column=19, sticky=W)

        self.var5_min_listbox_label = Label(self.inner_frame, text="var5\nmin")
        self.var5_min_listbox_label.grid(row=25, column=20, sticky=W)
        self.var5_max_listbox_label = Label(self.inner_frame, text="var5\nmax")
        self.var5_max_listbox_label.grid(row=25, column=21, sticky=W)
        self.var5_prec_listbox_label = Label(self.inner_frame, text="var5\nprec")
        self.var5_prec_listbox_label.grid(row=25, column=22, sticky=W)
        self.var5_divby_listbox_label = Label(self.inner_frame, text="var5\ntol")
        self.var5_divby_listbox_label.grid(row=25, column=23, sticky=W)

        self.var6_min_listbox_label = Label(self.inner_frame, text="var6\nmin")
        self.var6_min_listbox_label.grid(row=25, column=24, sticky=W)
        self.var6_max_listbox_label = Label(self.inner_frame, text="var6\nmax")
        self.var6_max_listbox_label.grid(row=25, column=25, sticky=W)
        self.var6_prec_listbox_label = Label(self.inner_frame, text="var6\nprec")
        self.var6_prec_listbox_label.grid(row=25, column=26, sticky=W)
        self.var6_divby_listbox_label = Label(self.inner_frame, text="var6\ntol")
        self.var6_divby_listbox_label.grid(row=25, column=27, sticky=W)

        self.var7_min_listbox_label = Label(self.inner_frame, text="var7\nmin")
        self.var7_min_listbox_label.grid(row=25, column=28, sticky=W)
        self.var7_max_listbox_label = Label(self.inner_frame, text="var7\nmax")
        self.var7_max_listbox_label.grid(row=25, column=29, sticky=W)
        self.var7_prec_listbox_label = Label(self.inner_frame, text="var7\nprec")
        self.var7_prec_listbox_label.grid(row=25, column=30, sticky=W)
        self.var7_divby_listbox_label = Label(self.inner_frame, text="var7\ntol")
        self.var7_divby_listbox_label.grid(row=25, column=31, sticky=W)

        self.res1_min_listbox_label = Label(self.inner_frame, text="res1\nmin")
        self.res1_min_listbox_label.grid(row=25, column=32, sticky=W)
        self.res1_max_listbox_label = Label(self.inner_frame, text="res1\nmax")
        self.res1_max_listbox_label.grid(row=25, column=33, sticky=W)
        self.res1_prec_listbox_label = Label(self.inner_frame, text="res1\nprec")
        self.res1_prec_listbox_label.grid(row=25, column=34, sticky=W)
        self.res1_tol_listbox_label = Label(self.inner_frame, text="res1\ntol")
        self.res1_tol_listbox_label.grid(row=25, column=35, sticky=W)
        self.res1_points_listbox_label = Label(self.inner_frame, text="res1\npts")
        self.res1_points_listbox_label.grid(row=25, column=36, sticky=W)

        self.res2_min_listbox_label = Label(self.inner_frame, text="res2\nmin")
        self.res2_min_listbox_label.grid(row=25, column=37, sticky=W)
        self.res2_max_listbox_label = Label(self.inner_frame, text="res2\nmax")
        self.res2_max_listbox_label.grid(row=25, column=38, sticky=W)
        self.res2_prec_listbox_label = Label(self.inner_frame, text="res2\nprec")
        self.res2_prec_listbox_label.grid(row=25, column=39, sticky=W)
        self.res2_tol_listbox_label = Label(self.inner_frame, text="res2\ntol")
        self.res2_tol_listbox_label.grid(row=25, column=40, sticky=W)
        self.res2_points_listbox_label = Label(self.inner_frame, text="res2\npts")
        self.res2_points_listbox_label.grid(row=25, column=41, sticky=W)

        self.res3_min_listbox_label = Label(self.inner_frame, text="res3\nmin")
        self.res3_min_listbox_label.grid(row=25, column=42, sticky=W)
        self.res3_max_listbox_label = Label(self.inner_frame, text="res3\nmax")
        self.res3_max_listbox_label.grid(row=25, column=43, sticky=W)
        self.res3_prec_listbox_label = Label(self.inner_frame, text="res3\nprec")
        self.res3_prec_listbox_label.grid(row=25, column=44, sticky=W)
        self.res3_tol_listbox_label = Label(self.inner_frame, text="res3\ntol")
        self.res3_tol_listbox_label.grid(row=25, column=45, sticky=W)
        self.res3_points_listbox_label = Label(self.inner_frame, text="res3\npts")
        self.res3_points_listbox_label.grid(row=25, column=46, sticky=W)

        self.img_name_listbox_label = Label(self.inner_frame, text=" img\n name")
        self.img_name_listbox_label.grid(row=25, column=47, sticky=W)

        self.img_data_label = Label(self.inner_frame, text=" img\n data")
        self.img_data_label.grid(row=25, column=48, sticky=W)

        self.oid_listbox_label = Label(self.inner_frame, text=" oid")
        self.oid_listbox_label.grid(row=25, column=49, sticky=W)

        # CREATE FULL-LISTBOX ENTRYS IN NEW WINDOW

        self.my_listbox_title = Listbox(self.inner_frame, width=15)
        self.my_listbox_title.grid(row=30, column=1, sticky=W, pady=20)
        self.my_listbox_description = Listbox(self.inner_frame, width=15)
        self.my_listbox_description.grid(row=30, column=2, sticky=W)
        self.my_listbox_formula = Listbox(self.inner_frame, width=15)
        self.my_listbox_formula.grid(row=30, column=3, sticky=W)

        self.my_listbox_var1_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_min.grid(row=30, column=4, sticky=W)
        self.my_listbox_var1_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_max.grid(row=30, column=5, sticky=W)
        self.my_listbox_var1_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_prec.grid(row=30, column=6, sticky=W)
        self.my_listbox_var1_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var1_divby.grid(row=30, column=7, sticky=W)

        self.my_listbox_var2_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_min.grid(row=30, column=8, sticky=W)
        self.my_listbox_var2_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_max.grid(row=30, column=9, sticky=W)
        self.my_listbox_var2_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_prec.grid(row=30, column=10, sticky=W)
        self.my_listbox_var2_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var2_divby.grid(row=30, column=11, sticky=W)

        self.my_listbox_var3_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_min.grid(row=30, column=12, sticky=W)
        self.my_listbox_var3_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_max.grid(row=30, column=13, sticky=W)
        self.my_listbox_var3_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_prec.grid(row=30, column=14, sticky=W)
        self.my_listbox_var3_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var3_divby.grid(row=30, column=15, sticky=W)

        self.my_listbox_var4_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_min.grid(row=30, column=16, sticky=W)
        self.my_listbox_var4_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_max.grid(row=30, column=17, sticky=W)
        self.my_listbox_var4_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_prec.grid(row=30, column=18, sticky=W)
        self.my_listbox_var4_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var4_divby.grid(row=30, column=19, sticky=W)

        self.my_listbox_var5_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_min.grid(row=30, column=20, sticky=W)
        self.my_listbox_var5_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_max.grid(row=30, column=21, sticky=W)
        self.my_listbox_var5_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_prec.grid(row=30, column=22, sticky=W)
        self.my_listbox_var5_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var5_divby.grid(row=30, column=23, sticky=W)

        self.my_listbox_var6_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_min.grid(row=30, column=24, sticky=W)
        self.my_listbox_var6_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_max.grid(row=30, column=25, sticky=W)
        self.my_listbox_var6_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_prec.grid(row=30, column=26, sticky=W)
        self.my_listbox_var6_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var6_divby.grid(row=30, column=27, sticky=W)

        self.my_listbox_var7_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_min.grid(row=30, column=28, sticky=W)
        self.my_listbox_var7_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_max.grid(row=30, column=29, sticky=W)
        self.my_listbox_var7_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_prec.grid(row=30, column=30, sticky=W)
        self.my_listbox_var7_divby = Listbox(self.inner_frame, width=5)
        self.my_listbox_var7_divby.grid(row=30, column=31, sticky=W)

        self.my_listbox_res1_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_min.grid(row=30, column=32, sticky=W)
        self.my_listbox_res1_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_max.grid(row=30, column=33, sticky=W)
        self.my_listbox_res1_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_prec.grid(row=30, column=34, sticky=W)
        self.my_listbox_res1_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_tol.grid(row=30, column=35, sticky=W)
        self.my_listbox_res1_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res1_points.grid(row=30, column=36, sticky=W)

        self.my_listbox_res2_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_min.grid(row=30, column=37, sticky=W)
        self.my_listbox_res2_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_max.grid(row=30, column=38, sticky=W)
        self.my_listbox_res2_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_prec.grid(row=30, column=39, sticky=W)
        self.my_listbox_res2_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_tol.grid(row=30, column=40, sticky=W)
        self.my_listbox_res2_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res2_points.grid(row=30, column=41, sticky=W)

        self.my_listbox_res3_min = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_min.grid(row=30, column=42, sticky=W)
        self.my_listbox_res3_max = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_max.grid(row=30, column=43, sticky=W)
        self.my_listbox_res3_prec = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_prec.grid(row=30, column=44, sticky=W)
        self.my_listbox_res3_tol = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_tol.grid(row=30, column=45, sticky=W)
        self.my_listbox_res3_points = Listbox(self.inner_frame, width=5)
        self.my_listbox_res3_points.grid(row=30, column=46, sticky=W)

        self.my_listbox_img_name = Listbox(self.inner_frame, width=5)
        self.my_listbox_img_name.grid(row=30, column=47, sticky=W)

        self.my_listbox_img_data = Listbox(self.inner_frame, width=5)
        self.my_listbox_img_data.grid(row=30, column=48, sticky=W)

        self.my_listbox_oid = Listbox(self.inner_frame, width=5)
        self.my_listbox_oid.grid(row=30, column=49, sticky=W)




        conn = sqlite3.connect('ilias_questions_db.db')
        c = conn.cursor()

        c.execute("SELECT *, oid FROM my_table")
        records = c.fetchall()

        # Clear List Boxes
        self.my_listbox_formula.delete(0, END)
        self.my_listbox_var1_min.delete(0, END)
        self.my_listbox_var1_max.delete(0, END)
        self.my_listbox_var1_prec.delete(0, END)
        self.my_listbox_var1_divby.delete(0, END)
        self.my_listbox_var2_min.delete(0, END)
        self.my_listbox_var2_max.delete(0, END)
        self.my_listbox_var2_prec.delete(0, END)
        self.my_listbox_var2_divby.delete(0, END)
        self.my_listbox_var3_min.delete(0, END)
        self.my_listbox_var3_max.delete(0, END)
        self.my_listbox_var3_prec.delete(0, END)
        self.my_listbox_var3_divby.delete(0, END)
        self.my_listbox_res1_min.delete(0, END)
        self.my_listbox_res1_max.delete(0, END)
        self.my_listbox_res1_prec.delete(0, END)
        self.my_listbox_res1_tol.delete(0, END)
        self.my_listbox_res1_points.delete(0, END)
        self.my_listbox_oid.delete(0, END)

        # Loop thru Results
        for record in records:
            self.my_listbox_formula.insert(END, record[0])
            self.my_listbox_var1_min.insert(END, record[1])
            self.my_listbox_var1_max.insert(END, record[2])
            self.my_listbox_var1_prec.insert(END, record[3])
            self.my_listbox_var1_divby.insert(END, record[4])
            self.my_listbox_var2_min.insert(END, record[5])
            self.my_listbox_var2_max.insert(END, record[6])
            self.my_listbox_var2_prec.insert(END, record[7])
            self.my_listbox_var2_divby.insert(END, record[8])
            self.my_listbox_var3_min.insert(END, record[9])
            self.my_listbox_var3_max.insert(END, record[10])
            self.my_listbox_var3_prec.insert(END, record[11])
            self.my_listbox_var3_divby.insert(END, record[12])
            self.my_listbox_res1_min.insert(END, record[13])
            self.my_listbox_res1_max.insert(END, record[14])
            self.my_listbox_res1_prec.insert(END, record[15])
            self.my_listbox_res1_tol.insert(END, record[16])
            self.my_listbox_res1_points.insert(END, record[17])
            self.my_listbox_oid.insert(END, record[18])

            print(record)
        conn.commit()
        conn.close()





    """
