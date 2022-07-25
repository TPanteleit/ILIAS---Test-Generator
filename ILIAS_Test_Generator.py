"""
********************************************
ILIAS_Test_Generator.py
@digitalfellowship - Stand 07/2022
Autor: Tobias Panteleit
********************************************

Dieses Modul ist die Hauptdatei zum Starten des Aufgabengenerators
Beim Start werden die Fragentyp-Module geladen und die GUI erstellt
"""



#############################################################################################################
#                                                                                                           #
#    Ilias Test - Generator                                                                                 #
#    Version: 2.6                                                                                           #
#    Author:  Tobias Panteleit                                                                              #
#                                                                                                           #
#    Dieses Tool dient der Erstellung und Verwaltung von Fragen für die ILIAS-Plattform.                    #
#    In der derzeitigen Version (v2.6) ist die Erstellung von folgenden Fragentypen möglich:                #
#        - Formelfrage                                                                                      #
#        - SingleChoice                                                                                     #
#        - MultipleChoice                                                                                   #
#        - Zuordnungsfragen                                                                                 #
#############################################################################################################
#                                                                                                           #
#    Neuerungen:                                                                                            #                                                 #
#     Neuer Button / neue Funktion unter "Formelfrage-Tab" --> ILIAS-Evaluator                              #
#     Über diese Funktion werden folgende Schritte ausgeführt:                                              #
#       - ILIAS Test zum importieren auswählen                                                              #
#       - Temp-DB wird erzeugt                                                                              #
#       - Daten werden in Temp-DB gespeichert                                                               #
#       - DB wird direkt exportiert, für alle Fragentypen (abgelegt unter dem ausgewählten Pfad)            #
#       - Temp-DB wird wieder gelöscht                                                                      #
#                                                                                                           #
#                                                                                                           #
#                                                                                                           #
#                                                                                                           #
#                                                                                                           #
#    - Bilder werden über einen relativen Pfad eingelesen/verwendet                                         #
#       Bisher war der exakte Pfad zum Bild notwendig (z.B. c:/user/bilder/test.png)                        #
#       Nun ist ein "Bilder"-Ordner im Projektverzeichnis vorhanden, indem die Bilder gespeichert werden.   #
#        Es können auch eigene Ordner in diesem Ordner erstellt werden                                      #
#        Der Pfad entspricht jetzt nur noch dem Pfad im "Bilder" Ordner. (z.B. Bilder/Panteleleit/test.png) #
#                                                                                                           #
#    - Datenbank Einträge löschen --> Alle Einträge löschen:                                                #
#       Erstellt KEIN Backup mehr. Es wird ein Abfrage Fenster geöffnet und beim bestätigen ausgeführt      #
#                                                                                                           #
#    - Datenbank Import:                                                                                    #
#       Beim Import von Fragen (mit dem exakt gleichen Titel) werden automatisch aktualisiert und nicht     #
#       in der Datenbank angehangen (als neue Frage)                                                        #
#                                                                                                           #
#   - Datenbank Export ---> Auswahl ob Export im XLSX oder ODS Format                                       #
#                                                                                                           #
#   - Tabellenkalkulationsdatei: Nicht mehr notwendig Bild-Einträge mit "EMPTY" zu versehen                 #
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
# -------------------------------------------------------------------------------------------------         #
#    Behandlung der Excel-Inhalte:                                                                          #
#    Unter der Kategorie "Fragen-Typ" MUSS z.B.: "Formelfrage" oder "Multiplechoice" eingetragen werden, da #
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
import pathlib

### Test-Generator Module
from Test_Generator_Module import test_generator_modul_datenbanken_erstellen
from Test_Generator_Module import test_generator_modul_formelfrage
from Test_Generator_Module import test_generator_modul_formelfrage_permutation
from Test_Generator_Module import test_generator_modul_singlechoice
from Test_Generator_Module import test_generator_modul_multiplechoice
from Test_Generator_Module import test_generator_modul_zuordnungsfrage



class GuiMainWindow:

    def __init__(self, master):
        self.master = master

        # Die größe der GUI wird durch die Einträge für self.window_width und self.window_height festgelegt
        master.geometry = '800x710'
        master.title('ilias - Test-Generator v2.6')

        # Wird verwendet um in der Konsole einen benutzerdefinierten Text mit * zu umranden
        def print_in_a_frame(*words):
            size = max(len(word) for word in words)
            print('*' * (size + 4))
            for word in words:
                print('* {:<{}} *'.format(word, size))
            print('*' * (size + 4))


        print("\n")
        print_in_a_frame("", "ILIAS - Test-Generator v2.6", "@digitalfellowship", "", )
        print("\n")

        # Fenstergröße für die Module setzen
        self.window_width = 1100
        self.window_height = 800

        # Projektpfad auslesen. Der Projektpfad ist der Ordner in dem das Programm ausgeführt wird.
        self.project_root_path = pathlib.Path().absolute()



        # <------------ ERSTELLEN VON TABS UND TAB_CONTROL ----------->
        # Durch tabControl können die einzelnen Tabs dargestellt und ausgewählt werden
        self.tabControl = ttk.Notebook(app)  # Create Tab Control


        # ---- Tab für Fragentyp: Formelfrage
        self.formelfrage_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formelfrage_tab_ttk, text='Formelfrage')  # Add the tab

        # ---- Tab für Fragentyp: Formelfrage_Permutation
        self.formelfrage_permutation_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.formelfrage_permutation_tab_ttk, text='Formelfrage Permutation')  # Add the tab

        # ---- Tab für Fragentyp: SingleChoice
        self.singlechoice_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.singlechoice_tab_ttk, text='Single Choice')  # Add the tab

        # ---- Tab für Fragentyp: MultipleChoice
        self.multiplechoice_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.multiplechoice_tab_ttk, text='Multiple Choice')  # Add the tab

        # ---- Tab für Fragentyp: Zuordnungsfrage (Matching Question)
        self.zuordnungsfrage_tab_ttk = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.zuordnungsfrage_tab_ttk, text='Zuordnungsfrage')  # Add the tab


        # <------------ CREATE SCROLLABLE FRAME ON TABS ----------->
        # Um in der GUI, Fenster mit Bildlaufleiste (Scroll-Balken) verwenden zu können, wird die Bibliothek "tkScrolledFrame" verwendet.
        # Es werden zusätzliche Rahmen erstellt, in welcher letztlich die Labels/Buttons und der Scroll-Balken platziert werden

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


        # Create a frame within the ScrolledFrame
        self.formelfrage_tab = self.scrolledframe_formelfrage.display_widget(Frame)
        self.formelfrage_permutation_tab = self.scrolledframe_formelfrage_permutation.display_widget(Frame)
        self.singlechoice_tab = self.scrolledframe_singlechoice.display_widget(Frame)
        self.multiplechoice_tab = self.scrolledframe_multiplechoice.display_widget(Frame)
        self.zuordnungsfrage_tab = self.scrolledframe_zuordnungsfrage.display_widget(Frame)


        # Tab-Control platzieren
        self.tabControl.pack(expand=1, fill="both")



        # <------------ ERSTELLEN VON DATENBANKEN ----------->
        # Bei Programmstart wird für jeden Fragen-Typ eine Datenbank erstellt, wenn keine vorhanden ist.
        test_generator_modul_datenbanken_erstellen.CreateDatabases.__init__(self, self.project_root_path)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_formelfrage(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_formelfrage_permutation(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_singlechoice(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_multiplechoice(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_zuordnungsfrage(self)
        test_generator_modul_datenbanken_erstellen.CreateDatabases.create_database_test_settings_profiles(self)


        # <------------ MODULE INITIALISIEREN ----------->
        # Durch den Aufruf wird das Modul aktiviert und kann in der GUI über den Reiter ausgewählt werden.
        test_generator_modul_formelfrage.Formelfrage.__init__(self, app, self.formelfrage_tab, self.project_root_path)
        test_generator_modul_singlechoice.SingleChoice.__init__(self, app, self.singlechoice_tab, self.project_root_path)
        test_generator_modul_multiplechoice.MultipleChoice.__init__(self, app, self.multiplechoice_tab, self.project_root_path)
        test_generator_modul_zuordnungsfrage.Zuordnungsfrage.__init__(self, app, self.zuordnungsfrage_tab, self.project_root_path)
        test_generator_modul_formelfrage_permutation.Formelfrage_Permutation.__init__(self, app, self.formelfrage_permutation_tab, self.project_root_path)





app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()







