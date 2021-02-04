#############################################################################################################
#                                                                                                           #
#    Ilias Test - Generator                                                                                 #
#    Version: 2.0                                                                                           #
#    Author:  Tobias Panteleit                                                                              #
#                                                                                                           #
#    Das Tool dient zur Erstellung von Fragen für die ILIAS-Plattform.                                      #
#    In der derzeitigen Version (v2.0) ist die Erstellung von folgenden Fragentypen möglich:                #
#        - Formelfrage                                                                                      #
#        - SingleChoice                                                                                     #
#        - MultipleChoice                                                                                   #
#        - Zuordnungsfragen                                                                                 #
#############################################################################################################
#                                                                                                           #
#                                                                                                           #
#    PERMUTATION ----- NOCH IN ENTWICKLUNG                                                                  #
#    Das Tool soll die Möglichkeit bieten, eine Vielzahl an Aufgaben zu erstellen. Dazu soll unter anderem  #
#    eine Art "Fragen-Permutation" dienen. Dabei wird ein Fragen-Text definiert und im Anschluss werden     #
#    die Ergebnisse und Variablen "durch rotiert" z.B.:                                                     #
#         "Gegeben ist eine Reihenschaltung aus drei Widerständen R1 = 100Ohm, R2 = 200Ohm R3=300Ohm.       #
#          Der Strom beträgt 5A, berechne die Spannung U$x1"                                                #
#                                                                                                           #
#    Die Variable $x1 wird im Tool definiert z.B.: $x1 = [1,3,2]. Dadurch werden bei der Erstellung der     #
#    Frage, drei Fragen erzeugt (..berechne Spannung U1, U3, U2). Hierbei werden auch die Formeln           #
#    angepasst.                                                                                             #
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
#    Unter der Kategorie "Fragen-Typ" MUSS z.B.: "Formelfrage" oder "MultipleChoice" eingetragen werden, da #
#    ansonsten die Frage vom Programm nicht verwertbar ist                                                  #
#                                                                                                           #
#    Wird ein "Result" (1..10) ausgefüllt MUSS auch die entsprechende Spalte für "Result-pts" ein Wert      #
#    enthalten, ansonsten schlägt der Import nach ILIAS fehl.                                               #
#                                                                                                           #
#    Die Ordner zum zippen und importieren nach ILIAS befinden sich unterteilt nach Fragentyp in z.B.:      #
#        ILIAS-Formelfrage\ff_ilias_pool_abgabe                                                             #
#        ILIAS-Formelfrage\ff_ilias_test_abgabe                                                             #
#    Jeweils der Ordner mit der höchsten Nummer am Ende.                                                    #
#                                                                                                           #
#    Bei der nachträglichen Ergänzung von Taxonomien MUSS ZWINGEND mit "Reallocate Text"                    #
#    die XML Datei neu sortiert werden. SONST ERKENNT ILIAS DIESEN NICHT!                                   #
#---------------------------------------------------------------------------------------------------------- #




from tkinter import *
from tkinter import ttk
from tkscrolledframe import ScrolledFrame  #Bewegbares Fesnter (Scrollbalken)
import os
import sys
import os.path
import pathlib


### Ilias-Tool Module

from Test_Generator_Module import test_generator_modul_datenbanken_erstellen  # Modul zum erstellen von notwendigen Datenbanken
from Test_Generator_Module import test_generator_modul_formelfrage
from Test_Generator_Module import test_generator_modul_formelfrage_permutation
from Test_Generator_Module import test_generator_modul_singlechoice
from Test_Generator_Module import test_generator_modul_multiplechoice
from Test_Generator_Module import test_generator_modul_zuordnungsfrage



class GuiMainWindow:


    def __init__(self, master):
        self.master = master
        master.geometry = '800x710'
        master.title('ilias - Test-Generator v2.0')


        # --------------------------    Set PATH for Project

        self.project_root_path = pathlib.Path().absolute()
        self.img_file_path_create_folder = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
        self.img_file_path = os.path.normpath(os.path.join(self.project_root_path,'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
        self.emtpy_xml_file_path_read = os.path.normpath(os.path.join(self.project_root_path, 'empty_xml_files', 'empty_xml.xml'))
        self.ilias_questionpool_for_import = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragenpool_zum_Import'))



        #
        # # --------------------------    Check if Files are in correct position
        # print("\n")
        # print("##    Project Files inside this Project Folder?")
        # print("##")
        # print("##    Testfragen -> orig_tst_file:                     " + str(os.path.exists(self.tst_file_path_read)))
        # print("##    Testfragen -> orig_qti_file:                     " + str(os.path.exists(self.qti_file_path_read)))
        # print("##    Testfragen -> 1590475954__0__tst_1944463.xml:    " + str(os.path.exists(self.tst_file_path_write)))
        # print("##    Testfragen -> 1590475954__0__qti_1944463.xml:    " + str(os.path.exists(self.qti_file_path_write)))
        # print("##    Poolfragen -> orig_qpl_file:                     " + str(os.path.exists(self.qpl_file_pool_path_read)))
        # print("##    Poolfragen -> orig_qti_file:                     " + str(os.path.exists(self.qti_file_pool_path_read)))
        # print("##    Poolfragen -> Vorlage_für_Fragenpool:            " + str(os.path.exists(os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'orig_1596569820__0__qpl_2074808')))))
        # print("-------------------------------------------------------")





        # --------------------------   Set size of windows
        # Main-window
        self.window_width = 800
        self.window_height = 800

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



        # <------------ CREATE TABS AND TABCONTROL ----------->

        self.tabControl = ttk.Notebook(app)  # Create Tab Control


        # ---- Tab for Formula - Questions
        self.formelfrage_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formelfrage_tab_ttk, text='Formelfrage')  # Add the tab

        # ---- Tab for Formula permutation - Questions
        self.formelfrage_permutation_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formelfrage_permutation_tab_ttk, text='Formelfrage Permutation')  # Add the tab

        # ---- Tab for Single Choice - Questions
        self.singlechoice_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.singlechoice_tab_ttk, text='Single Choice')  # Add the tab

        # ---- Tab for Multiple Choice - Questions
        self.multiplechoice_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.multiplechoice_tab_ttk, text='Multiple Choice')  # Add the tab

        # ---- Tab for MatchingQuestion - Questions
        self.zuordnungsfrage_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.zuordnungsfrage_tab_ttk, text='Zuordnungsfrage')  # Add the tab

        # ---- Tab for Lueckentext - Questions
        self.formelfrage_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.lueckentext_tab_ttk, text='Lueckentext')  # Add the tab

        ####### CREATE SCROLLABLE FRAME ON TABS
        # Create a ScrolledFrame widget
        self.scrolledframe_formelfrage = ScrolledFrame(self.formelfrage_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_formelfrage.pack(expand=1, fill="both")

        self.scrolledframe_formelfrage_permutation = ScrolledFrame(self.formelfrage_permutation_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_formelfrage_permutation.pack(expand=1, fill="both")

        self.scrolledframe_singlechoice = ScrolledFrame(self.singlechoice_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_singlechoice.pack(expand=1, fill="both")

        self.scrolledframe_multiplechoice = ScrolledFrame(self.multiplechoice_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_multiplechoice.pack(expand=1, fill="both")

        self.scrolledframe_zuordnungsfrage = ScrolledFrame(self.zuordnungsfrage_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_zuordnungsfrage.pack(expand=1, fill="both")

        self.scrolledframe_zuordnungsfrage = ScrolledFrame(self.lueckentext_tab_ttk, width=self.window_width, height=self.window_height)
        self.scrolledframe_zuordnungsfrage.pack(expand=1, fill="both")

        # Create a frame within the ScrolledFrame
        self.formelfrage_tab = self.scrolledframe_formelfrage.display_widget(Frame)
        self.formelfrage_permutation_tab = self.scrolledframe_formelfrage_permutation.display_widget(Frame)
        self.singlechoice_tab = self.scrolledframe_singlechoice.display_widget(Frame)
        self.multiplechoice_tab = self.scrolledframe_multiplechoice.display_widget(Frame)
        self.zuordnungsfrage_tab = self.scrolledframe_zuordnungsfrage.display_widget(Frame)

        self.tabControl.pack(expand=1, fill="both")




        # ---Init Variable Matrix


        ####    ----- Create Databases ---
        test_generator_modul_datenbanken_erstellen.CreateDatabases.__init__(self, self.project_root_path)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_formelfrage(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_formelfrage_permutation(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_singlechoice(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_multiplechoice(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_zuordnungsfrage(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_test_settings_profiles(self)


        #Formelfrage_GUI.__init__(self)
        test_generator_modul_formelfrage.Formelfrage.__init__(self, app, self.formelfrage_tab, self.project_root_path)
        test_generator_modul_singlechoice.SingleChoice.__init__(self, app, self.singlechoice_tab, self.project_root_path)
        test_generator_modul_multiplechoice.MultipleChoice.__init__(self, app, self.multiplechoice_tab, self.project_root_path)
        test_generator_modul_zuordnungsfrage.Zuordnungsfrage.__init__(self, app, self.zuordnungsfrage_tab, self.project_root_path)
        test_generator_modul_formelfrage_permutation.Formelfrage_Permutation.__init__(self, app, self.formelfrage_permutation_tab, self.project_root_path)





app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()







