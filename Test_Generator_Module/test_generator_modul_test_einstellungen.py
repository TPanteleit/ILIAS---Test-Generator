from tkinter import *
from tkscrolledframe import ScrolledFrame  #Bewegbares Fesnter (Scrollbalken)
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
import datetime
import os




class Test_Einstellungen_GUI:

    def __init__(self, project_root_path, test_qti_file_path_output):

        # Projekt-Pfad
        self.project_root_path = project_root_path

        # Pfad für qti_(XML)-Datei für erstellten Test
        self.test_qti_file_path_output = test_qti_file_path_output


        # Name für Datenbank und Tabelle
        self.settings_database = "test_settings_profiles_db.db"
        self.settings_database_table = "my_profiles_table"

        # Pfad für die Datenbank
        self.settings_database_path = os.path.normpath(os.path.join(self.project_root_path, "Test_Generator_Datenbanken", self.settings_database))



        # New Window must be "Toplevel" not "Tk()" in order to get Radiobuttons to work properly
        self.test_settings_window = Toplevel()
        self.test_settings_window.title("Test Einstellungen verwalten")

        # Create a ScrolledFrame widget
        self.sf_test_settings = ScrolledFrame(self.test_settings_window, width=300,
                                              height=300)
        self.sf_test_settings.pack(expand=1, fill="both")

        # Bind the arrow keys and scroll wheel
        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        # self.sf_test_settings.bind_arrow_keys(app)
        # self.sf_test_settings.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.test_settings = self.sf_test_settings.display_widget(Frame)

        self.frame1 = LabelFrame(self.test_settings, text="Test Einstellungen", padx=5, pady=5)
        self.frame1.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.frame2 = LabelFrame(self.test_settings, text="Test Einstellungen", padx=5, pady=5)
        self.frame2.grid(row=0, column=1, padx=20, pady=10, sticky=NW)

        self.frame3 = LabelFrame(self.test_settings, text="Test Einstellungen", padx=5, pady=5)
        self.frame3.grid(row=0, column=2, padx=20, pady=10, sticky=NW)

        self.res12_min_listbox_label = Label(self.frame1, text="EINSTELLUNGEN DES TESTS",
                                             font=('Helvetica', 10, 'bold'))
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
        self.res13_points_listbox_label = Label(self.frame1,
                                                text="Zeitlich begrenzte Verfügbarkeit   ---   not working")
        self.res13_points_listbox_label.grid(row=11, column=0, sticky=W, padx=10)

        self.res22_tol_listbox_label = Label(self.frame1, text="INFORMATIONEN ZUM EINSTIEG",
                                             font=('Helvetica', 10, 'bold'))
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

        self.res41_tol_listbox_label = Label(self.frame1, text="DURCHFÜHRUNG: STEUERUNG TESTDURCHLAUF",
                                             font=('Helvetica', 10, 'bold'))
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

        self.res51_tol_listbox_label = Label(self.frame2, text="DURCHFÜHRUNG: VERHALTEN DER FRAGE",
                                             font=('Helvetica', 10, 'bold'))
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
        self.res66_points_listbox_label.grid(row=19, column=2, sticky=W, padx=10)

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

        # self.entry.grid(row=11, column=1, sticky=W, padx=20)
        self.check_time_limited = Checkbutton(self.frame1, text="", variable=self.var_time_limited, onvalue=1,
                                              offvalue=0,
                                              command=lambda
                                                  v=self.var_time_limited: Test_Einstellungen_GUI.show_entry_time_limited_start(
                                                  self, v))
        self.check_time_limited.deselect()
        self.check_time_limited.grid(row=11, column=1, sticky=W)

        self.var_introduction = IntVar()
        self.check_introduction = Checkbutton(self.frame1, text="", variable=self.var_introduction, onvalue=1,
                                              offvalue=0,
                                              command=lambda
                                                  v=self.var_introduction: Test_Einstellungen_GUI.show_introduction_textfield(
                                                  self, v))
        self.check_introduction.deselect()
        self.check_introduction.grid(row=15, column=1, sticky=W)

        self.var_test_prop = IntVar()
        self.check_test_prop = Checkbutton(self.frame1, text="", variable=self.var_test_prop, onvalue=1, offvalue=0)
        self.check_test_prop.deselect()
        self.check_test_prop.grid(row=16, column=1, sticky=W)

        # self.var_test_password = IntVar()
        # self.check_test_password = Checkbutton(self.frame1, text="", variable=self.var_test_password, onvalue=1, offvalue=0)
        # self.check_test_password.deselect()
        # self.check_test_password.grid(row=20, column=1, sticky=W)

        self.var_specific_users = IntVar()
        self.check_specific_users = Checkbutton(self.frame1, text="", variable=self.var_specific_users, onvalue=1,
                                                offvalue=0)
        self.check_specific_users.deselect()
        self.check_specific_users.grid(row=21, column=1, sticky=W)

        # self.var_fixed_users = IntVar()
        # self.check_fixed_users = Checkbutton(self.frame1, text="", variable=self.var_fixed_users, onvalue=1, offvalue=0)
        # self.check_fixed_users.deselect()
        # self.check_fixed_users.grid(row=22, column=1, sticky=W)

        # self.var_limit_test_runs = IntVar()
        # self.check_limit_test_runs = Checkbutton(self.frame1, text="", variable=self.var_limit_test_runs, onvalue=1, offvalue=0)
        # self.check_limit_test_runs.deselect()
        # self.check_limit_test_runs.grid(row=22, column=1, sticky=W)

        # self.var_time_betw_test_runs = IntVar()
        # self.check_time_betw_test_runs = Checkbutton(self.frame1, text="", variable=self.var_time_betw_test_runs, onvalue=1, offvalue=0)
        # self.check_time_betw_test_runs.deselect()
        # self.check_time_betw_test_runs.grid(row=25, column=1, sticky=W)

        self.var_processing_time = IntVar()
        self.check_processing_time = Checkbutton(self.frame1, text="", variable=self.var_processing_time, onvalue=1,
                                                 offvalue=0)
        self.check_processing_time.deselect()
        self.check_processing_time.grid(row=27, column=1, sticky=W)

        self.var_processing_time_reset = IntVar()
        self.check_processing_time_reset = Checkbutton(self.frame1, text="", variable=self.var_processing_time_reset,
                                                       onvalue=1, offvalue=0)
        self.check_processing_time_reset.deselect()
        self.check_processing_time_reset.grid(row=29, column=1, sticky=W)

        self.var_examview = IntVar()
        self.check_examview = Checkbutton(self.frame1, text="", variable=self.var_examview, onvalue=1, offvalue=0)
        self.check_examview.deselect()
        self.check_examview.grid(row=30, column=1, sticky=W)

        self.var_examview_test_title = IntVar()
        self.check_examview_test_title = Checkbutton(self.frame1, text="", variable=self.var_examview_test_title,
                                                     onvalue=1, offvalue=0)
        self.check_examview_test_title.deselect()
        self.check_examview_test_title.grid(row=31, column=1, sticky=W)

        self.var_examview_user_name = IntVar()
        self.check_examview_user_name = Checkbutton(self.frame1, text="", variable=self.var_examview_user_name,
                                                    onvalue=1, offvalue=0)
        self.check_examview_user_name.deselect()
        self.check_examview_user_name.grid(row=32, column=1, sticky=W)

        self.var_show_ilias_nr = IntVar()
        self.check_show_ilias_nr = Checkbutton(self.frame1, text="", variable=self.var_show_ilias_nr, onvalue=1,
                                               offvalue=0)
        self.check_show_ilias_nr.deselect()
        self.check_show_ilias_nr.grid(row=33, column=1, sticky=W)

        self.var_autosave = IntVar()
        self.check_autosave = Checkbutton(self.frame2, text="", variable=self.var_autosave, onvalue=1, offvalue=0,
                                          command=lambda v=self.var_autosave: Test_Einstellungen_GUI.enable_autosave(self,
                                                                                                                  v))

        self.check_autosave_interval_label = Label(self.frame2, text="Speicherintervall (in Sek.):")
        self.check_autosave_interval_entry = Entry(self.frame2, width=10)
        self.check_autosave.deselect()
        self.check_autosave.grid(row=4, column=3, sticky=W)

        self.var_mix_questions = IntVar()
        self.check_mix_questions = Checkbutton(self.frame2, text="", variable=self.var_mix_questions, onvalue=1,
                                               offvalue=0)
        self.check_mix_questions.deselect()
        self.check_mix_questions.grid(row=5, column=3, sticky=W)

        self.var_show_solution_notes = IntVar()
        self.check_show_solution_notes = Checkbutton(self.frame2, text="", variable=self.var_show_solution_notes,
                                                     onvalue=1, offvalue=0)
        self.check_show_solution_notes.deselect()
        self.check_show_solution_notes.grid(row=6, column=3, sticky=W)

        self.var_direct_response = IntVar()
        self.check_direct_response = Checkbutton(self.frame2, text="", variable=self.var_direct_response, onvalue=1,
                                                 offvalue=0)
        self.check_direct_response.deselect()
        self.check_direct_response.grid(row=7, column=3, sticky=W)

        self.var_mandatory_questions = IntVar()
        self.check_mandatory_questions = Checkbutton(self.frame2, text="", variable=self.var_mandatory_questions,
                                                     onvalue=1, offvalue=0)
        self.check_mandatory_questions.deselect()
        self.check_mandatory_questions.grid(row=12, column=3, sticky=W)

        self.var_use_previous_solution = IntVar()
        self.check_use_previous_solution = Checkbutton(self.frame2, text="", variable=self.var_use_previous_solution,
                                                       onvalue=1, offvalue=0)
        self.check_use_previous_solution.deselect()
        self.check_use_previous_solution.grid(row=14, column=3, sticky=W)

        self.var_show_test_cancel = IntVar()
        self.check_show_test_cancel = Checkbutton(self.frame2, text="", variable=self.var_show_test_cancel, onvalue=1,
                                                  offvalue=0)
        self.check_show_test_cancel.deselect()
        self.check_show_test_cancel.grid(row=15, column=3, sticky=W)

        self.var_show_question_list_process_status = IntVar()
        self.check_show_question_list_process_status = Checkbutton(self.frame2, text="",
                                                                   variable=self.var_show_question_list_process_status,
                                                                   onvalue=1, offvalue=0)
        self.check_show_question_list_process_status.deselect()
        self.check_show_question_list_process_status.grid(row=18, column=3, sticky=W)

        self.var_question_mark = IntVar()
        self.check_question_mark = Checkbutton(self.frame2, text="", variable=self.var_question_mark, onvalue=1,
                                               offvalue=0)
        self.check_question_mark.deselect()
        self.check_question_mark.grid(row=19, column=3, sticky=W)

        self.var_overview_answers = IntVar()
        self.check_overview_answers = Checkbutton(self.frame2, text="", variable=self.var_overview_answers, onvalue=1,
                                                  offvalue=0)
        self.check_overview_answers.grid(row=21, column=3, sticky=W)

        self.var_show_end_comment = IntVar()
        self.check_show_end_comment = Checkbutton(self.frame2, text="", variable=self.var_show_end_comment, onvalue=1,
                                                  offvalue=0,
                                                  command=lambda
                                                      v=self.var_show_end_comment: Test_Einstellungen_GUI.show_concluding_remarks(
                                                      self, v))
        self.check_show_end_comment.deselect()
        self.check_show_end_comment.grid(row=22, column=3, sticky=W)

        self.var_forwarding = IntVar()
        self.check_forwarding = Checkbutton(self.frame2, text="", variable=self.var_forwarding, onvalue=1, offvalue=0)
        self.check_forwarding.deselect()
        self.check_forwarding.grid(row=23, column=3, sticky=W)

        self.var_notification = IntVar()
        self.check_notification = Checkbutton(self.frame2, text="", variable=self.var_notification, onvalue=1,
                                              offvalue=0)
        self.check_notification.deselect()
        self.check_notification.grid(row=24, column=3, sticky=W)

        # --------------------------- RADIO BUTTONS ---------------------------------------

        self.select_question = IntVar()
        self.select_question.set(0)
        self.select_question_radiobtn1 = Radiobutton(self.frame1, text="Fest definierte Fragenauswahl",
                                                     variable=self.select_question, value=0)
        self.select_question_radiobtn1.grid(row=4, column=1, pady=0, sticky=W)  # FIXED_QUEST_SET
        self.select_question_radiobtn2 = Radiobutton(self.frame1, text="Zufällige Fragenauswahl",
                                                     variable=self.select_question, value=1)
        self.select_question_radiobtn2.grid(row=5, column=1, pady=0, sticky=W)  # RANDOM_QUEST_SET
        self.select_question_radiobtn3 = Radiobutton(self.frame1,
                                                     text="Wiedervorlagemodus - alle Fragen eines Fragenpools",
                                                     variable=self.select_question, value=2)
        self.select_question_radiobtn3.grid(row=6, column=1, pady=0, sticky=W)  # DYNAMIC_QUEST_SET

        self.select_anonym = IntVar()
        self.select_anonym.set(0)
        self.select_anonym_radiobtn1 = Radiobutton(self.frame1, text="Testergebnisse ohne Namen",
                                                   variable=self.select_anonym, value=0, borderwidth=0,
                                                   command=self.select_anonym.get())
        self.select_anonym_radiobtn1.grid(row=7, column=1, pady=0, sticky=W)
        self.select_anonym_radiobtn2 = Radiobutton(self.frame1, text="Testergebnisse mit Namen",
                                                   variable=self.select_anonym, value=1, borderwidth=0,
                                                   command=self.select_anonym.get())
        self.select_anonym_radiobtn2.grid(row=8, column=1, pady=0, sticky=W)

        self.select_show_question_title = IntVar()
        self.select_show_question_title.set(0)
        self.select_show_question_title_radiobtn1 = Radiobutton(self.frame2, text="Fragentitel und erreichbare Punkte",
                                                                variable=self.select_show_question_title, value=0,
                                                                borderwidth=0,
                                                                command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn1.grid(row=1, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn2 = Radiobutton(self.frame2, text="Nur Fragentitel",
                                                                variable=self.select_show_question_title, value=1,
                                                                borderwidth=0,
                                                                command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn2.grid(row=2, column=3, pady=0, sticky=W)
        self.select_show_question_title_radiobtn3 = Radiobutton(self.frame2,
                                                                text="Weder Fragentitel noch erreichbare Punkte",
                                                                variable=self.select_show_question_title, value=2,
                                                                borderwidth=0,
                                                                command=self.select_show_question_title.get())
        self.select_show_question_title_radiobtn3.grid(row=3, column=3, pady=0, sticky=W)

        self.select_user_response = IntVar()
        self.select_user_response.set(0)
        self.select_user_response_radiobtn1 = Radiobutton(self.frame2,
                                                          text="Antworten während des Testdurchlaufs nicht festschreiben",
                                                          variable=self.select_user_response, value=0, borderwidth=0,
                                                          command=self.select_user_response.get())
        self.select_user_response_radiobtn1.grid(row=8, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn2 = Radiobutton(self.frame2,
                                                          text="Antworten bei Anzeige der Rückmeldung festschreiben",
                                                          variable=self.select_user_response, value=1, borderwidth=0,
                                                          command=self.select_user_response.get())
        self.select_user_response_radiobtn2.grid(row=9, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn3 = Radiobutton(self.frame2,
                                                          text="Antworten bei Anzeige der Folgefrage festschreiben",
                                                          variable=self.select_user_response, value=2, borderwidth=0,
                                                          command=self.select_user_response.get())
        self.select_user_response_radiobtn3.grid(row=10, column=3, pady=0, sticky=W)
        self.select_user_response_radiobtn4 = Radiobutton(self.frame2,
                                                          text="Antworten mit der Anzeige von Rückmeldungen oder der Folgefrage festschreiben",
                                                          variable=self.select_user_response, value=3, borderwidth=0,
                                                          command=self.select_user_response.get())
        self.select_user_response_radiobtn4.grid(row=11, column=3, pady=0, sticky=W)

        self.select_not_answered_questions = IntVar()
        self.select_not_answered_questions.set(0)
        self.select_not_answered_questions_radiobtn1 = Radiobutton(self.frame2,
                                                                   text="Nicht beantwortete Fragen bleiben an ihrem Platz",
                                                                   variable=self.select_not_answered_questions, value=0,
                                                                   borderwidth=0,
                                                                   command=self.select_not_answered_questions.get())
        self.select_not_answered_questions_radiobtn1.grid(row=16, column=3, pady=0, sticky=W)
        self.select_not_answered_questions_radiobtn2 = Radiobutton(self.frame2,
                                                                   text="Nicht beantwortete Fragen werden ans Testende gesschoben",
                                                                   variable=self.select_not_answered_questions, value=1,
                                                                   borderwidth=0,
                                                                   command=self.select_not_answered_questions.get())
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

        self.profile_name_label = Label(self.frame3, text="Speichern unter...")
        self.profile_name_label.grid(row=0, column=0)

        self.profile_name_entry = Entry(self.frame3, width=15)
        self.profile_name_entry.grid(row=0, column=1)

        # self.profile_oid_label = Label(self.frame3, text="Choose oid to delete")
        # self.profile_oid_label.grid(row=4, column=0)

        self.profile_oid_entry = Entry(self.frame3, width=10)
        self.profile_oid_entry.grid(row=4, column=1)

        self.load_settings_entry = Entry(self.frame3, width=10)
        self.load_settings_entry.grid(row=3, column=1)

        # self.delete_settings_btn = Button(self.frame3, text="Delete Profile from ID", command=Test_Einstellungen_GUI.profile_save_settings(self))
        # self.delete_settings_btn.grid(row=4, column=0)

        self.profile_oid_listbox_label = Label(self.frame3, text=" DB\nID")
        self.profile_oid_listbox_label.grid(row=1, column=4, sticky=W)

        self.profile_name_listbox_label = Label(self.frame3, text="Name")
        self.profile_name_listbox_label.grid(row=1, column=5, sticky=W)

        self.my_listbox_profile_oid = Listbox(self.frame3, width=5)
        self.my_listbox_profile_oid.grid(row=2, column=4, sticky=W)

        self.my_listbox_profile_name = Listbox(self.frame3, width=15)
        self.my_listbox_profile_name.grid(row=2, column=5, sticky=W)


        self.save_settings_btn = Button(self.frame3, text="Speichern", command=lambda: Test_Einstellungen_GUI.profile_save_settings(self))
        self.save_settings_btn.grid(row=2, column=0)

        self.load_settings_btn = Button(self.frame3, text="Profil laden",  command=lambda: Test_Einstellungen_GUI.profile_load_settings(self))
        self.load_settings_btn.grid(row=3, column=0)

        self.delete_profile_btn = Button(self.frame3, text="Profil löschen", command=lambda: Test_Einstellungen_GUI.profile_delete(self))
        self.delete_profile_btn.grid(row=4, column=0)

        self.show_profiles_btn = Button(self.frame3, text="Alle gespeicherten Profile anzeigen", command=lambda: Test_Einstellungen_GUI.profile_show_db(self))
        self.show_profiles_btn.grid(row=5, column=0)

        #self.create_profile_btn = Button(self.frame3, text="Create Profile-Settings", command=lambda: Test_Einstellungen_GUI.create_settings(self))
        #self.create_profile_btn.grid(row=6, column=0)

        #Test_Einstellungen_GUI.create_settings(self, self.settings_database_path, self.settings_database_table, self.settings_db_profile_name)

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

        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()

        c.execute("SELECT *, oid FROM " + self.settings_database_table)
        profile_records = c.fetchall()

        # Clear List Boxes

        self.my_listbox_profile_name.delete(0, END)
        self.my_listbox_profile_oid.delete(0, END)

        # Loop thru Results
        for profile_record in profile_records:
            self.my_listbox_profile_name.insert(END, profile_record[0])
            self.my_listbox_profile_oid.insert(END, profile_record[len(profile_record) - 1])

        self.profile_records_len = len(profile_records)
        # print(profile_records[len(profile_records)-1])

        conn.commit()
        conn.close()
        print("LOOP THROUGH... SHOW PROFILES!")

    def profile_save_settings(self):

        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()

        # Insert into Table
        c.execute(
            "INSERT INTO " + self.settings_database_table + " VALUES ("
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
                'check_use_previous_solution': self.var_use_previous_solution.get(),
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

        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()

        c.execute("SELECT * FROM " + self.settings_database_table + " WHERE oid =" + self.load_settings_entry.get())

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

        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()

        c.execute("DELETE from " + self.settings_database_table + " WHERE oid= " + self.profile_oid_entry.get())

        # self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()

    def profile_delete_last(self):

        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()
        self.profile_oid_entry.insert(0, self.profile_records_len)
        c.execute("DELETE from " + self.settings_database_table + " WHERE oid= " + self.profile_oid_entry.get())
        print("LAST DB ENTRY DELETED")
        # self.profile_oid_entry(0, END)

        conn.commit()
        conn.close()

    # For create test settings -->  Toplevel must be opened (Test-Settings Window)
    def create_settings(self, settings_database_path, settings_database_table, selected_settings_db_profile_name):

        self.settings_database_path = settings_database_path
        self.settings_database_table = settings_database_table
        self.settings_db_profile_name = selected_settings_db_profile_name

        print("=======")

        print(self.settings_database_path)
        print(self.settings_database_table)
        print(self.settings_db_profile_name)
        print("=======")

        ###################### DATENBANK ENTRIES UND INDEX DICT ERSTELLEN  ###################

        # Dictionary aus zwei Listen erstellen
        self.settings_db_find_entries = []
        self.settings_db_find_indexes = []
        self.settings_db_column_names_list = []
        self.settings_collection_of_question_titles = []

        connect = sqlite3.connect(self.settings_database_path)
        cursor = connect.execute('select * from ' + self.settings_database_table)
        self.settings_db_column_names_list = list(map(lambda x: x[0], cursor.description))
        self.db_column_names_string = ', :'.join(self.settings_db_column_names_list)
        self.db_column_names_string = ":" + self.db_column_names_string

        for i in range(len(self.settings_db_column_names_list)):
            self.settings_db_find_indexes.append(i)

        """
        # Durch list(map(lambdax: x[0])) werden die Spaltennamen aus der DB ausgelesen
        cursor = conn.execute('select * from ' + self.ff_database_table)
        db_column_names_list = list(map(lambda x: x[0], cursor.description))
        db_column_names_string  = ', :'.join(db_column_names_list)
        db_column_names_string  = ":" + db_column_names_string
        """

        self.settings_db_entry_to_index_dict = dict(
            zip((self.settings_db_column_names_list), (self.settings_db_find_indexes)))

        connect.commit()
        connect.close()
        #####



        # mit Datenbank verbinden
        conn = sqlite3.connect(self.settings_database_path)
        c = conn.cursor()

        #c.execute("SELECT * FROM " + self.settings_database_table + " WHERE profile_name =" + self.settings_db_profile_name)
        c.execute("SELECT * FROM " + self.settings_database_table)
        profile_records = c.fetchall()


       # Loop through Results
        for profile_record in profile_records:
            if profile_record[self.settings_db_entry_to_index_dict["profile_name"]] == self.settings_db_profile_name:

                self.profile_name                             = profile_record[self.settings_db_entry_to_index_dict["profile_name"]]
                self.description                              = profile_record[self.settings_db_entry_to_index_dict["entry_description"]]
                self.question_type                            = profile_record[self.settings_db_entry_to_index_dict["radio_select_question"]]
                self.anonym                                   = profile_record[self.settings_db_entry_to_index_dict["radio_select_anonymous"]]
                self.online                                   = profile_record[self.settings_db_entry_to_index_dict["check_online"]]
                self.time_limited                             = profile_record[self.settings_db_entry_to_index_dict["check_time_limited"]]

                self.introduction                             = profile_record[self.settings_db_entry_to_index_dict["check_introduction"]]
                self.introduction_infobox                     = profile_record[self.settings_db_entry_to_index_dict["entry_introduction"]]
                self.test_prop                                = profile_record[self.settings_db_entry_to_index_dict["check_test_properties"]]

                self.test_start_year                          = profile_record[self.settings_db_entry_to_index_dict["entry_test_start_year"]]
                self.test_start_month                         = profile_record[self.settings_db_entry_to_index_dict["entry_test_start_month"]]
                self.test_start_day                           = profile_record[self.settings_db_entry_to_index_dict["entry_test_start_day"]]
                self.test_start_hour                          = profile_record[self.settings_db_entry_to_index_dict["entry_test_start_hour"]]
                self.test_start_minute                        = profile_record[self.settings_db_entry_to_index_dict["entry_test_start_minute"]]

                self.test_end_year                            = profile_record[self.settings_db_entry_to_index_dict["entry_test_end_year"]]
                self.test_end_month                           = profile_record[self.settings_db_entry_to_index_dict["entry_test_end_month"]]
                self.test_end_day                             = profile_record[self.settings_db_entry_to_index_dict["entry_test_end_day"]]
                self.test_end_hour                            = profile_record[self.settings_db_entry_to_index_dict["entry_test_end_hour"]]
                self.test_end_minute                          = profile_record[self.settings_db_entry_to_index_dict["entry_test_end_minute"]]

                self.test_password                            = profile_record[self.settings_db_entry_to_index_dict["entry_test_password"]]
                self.specific_users                           = profile_record[self.settings_db_entry_to_index_dict["check_specific_users"]]
                self.limit_users_max                          = profile_record[self.settings_db_entry_to_index_dict["entry_limit_users"]]
                self.inactivity_time_for_users                = profile_record[self.settings_db_entry_to_index_dict["entry_user_inactivity"]]
                self.limit_test_runs                          = profile_record[self.settings_db_entry_to_index_dict["entry_limit_test_runs"]]

                self.limit_time_betw_test_runs_month          = profile_record[self.settings_db_entry_to_index_dict["entry_limit_time_betw_test_run_month"]]
                self.limit_time_betw_test_runs_day            = profile_record[self.settings_db_entry_to_index_dict["entry_limit_time_betw_test_run_day"]]
                self.limit_time_betw_test_runs_hour           = profile_record[self.settings_db_entry_to_index_dict["entry_limit_time_betw_test_run_hour"]]
                self.limit_time_betw_test_runs_minute         = profile_record[self.settings_db_entry_to_index_dict["entry_limit_time_betw_test_run_minute"]]

                self.processing_time                          = profile_record[self.settings_db_entry_to_index_dict["check_processing_time"]]
                self.limit_processing_time_minutes            = profile_record[self.settings_db_entry_to_index_dict["entry_processing_time_in_minutes"]]
                self.processing_time_reset                    = profile_record[self.settings_db_entry_to_index_dict["check_processing_time_reset"]]

                self.examview                                 = profile_record[self.settings_db_entry_to_index_dict["check_examview"]]
                self.examview_test_title                      = profile_record[self.settings_db_entry_to_index_dict["check_examview_titel"]]
                self.examview_user_name                       = profile_record[self.settings_db_entry_to_index_dict["check_examview_username"]]
                self.show_ilias_nr                            = profile_record[self.settings_db_entry_to_index_dict["check_show_ilias_nr"]]

                self.select_show_question_title               = profile_record[self.settings_db_entry_to_index_dict["radio_select_show_question_title"]]
                self.autosave                                 = profile_record[self.settings_db_entry_to_index_dict["check_autosave"]]
                self.autosave_interval                        = profile_record[self.settings_db_entry_to_index_dict["entry_autosave_interval"]]
                self.mix_questions                            = profile_record[self.settings_db_entry_to_index_dict["check_mix_questions"]]
                self.show_solution_notes                      = profile_record[self.settings_db_entry_to_index_dict["check_show_solution_notes"]]
                self.direct_response                          = profile_record[self.settings_db_entry_to_index_dict["check_direct_response"]]

                self.select_user_response                     = profile_record[self.settings_db_entry_to_index_dict["radio_select_user_response"]]
                self.mandatory_questions                      = profile_record[self.settings_db_entry_to_index_dict["check_mandatory_questions"]]
                self.use_previous_solution                    = profile_record[self.settings_db_entry_to_index_dict["check_use_previous_solution"]]
                self.show_test_cancel                         = profile_record[self.settings_db_entry_to_index_dict["check_show_test_cancel"]]
                self.select_not_answered_questions            = profile_record[self.settings_db_entry_to_index_dict["radio_select_not_answered_questions"]]

                self.show_question_list_process_status        = profile_record[self.settings_db_entry_to_index_dict["check_show_question_list_process_status"]]
                self.question_mark                            = profile_record[self.settings_db_entry_to_index_dict["check_question_mark"]]
                self.overview_answers                         = profile_record[self.settings_db_entry_to_index_dict["check_overview_answers"]]
                self.show_end_comment                         = profile_record[self.settings_db_entry_to_index_dict["check_show_end_comment"]]
                self.concluding_remarks_infobox               = profile_record[self.settings_db_entry_to_index_dict["entry_end_comment"]]
                self.forwarding                               = profile_record[self.settings_db_entry_to_index_dict["check_forwarding"]]
                self.notification                             = profile_record[self.settings_db_entry_to_index_dict["check_notification"]]




                self.mytree = ET.parse(self.test_qti_file_path_output)
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
                            # print("WRITE FIXED-Question")

                        elif self.question_type == 1:
                            qtimetadatafield.find('fieldentry').text = "RANDOM_QUEST_SET"
                            # print("WRITE RANDOM-Question")

                        elif self.question_type == 2:
                            qtimetadatafield.find('fieldentry').text = "DYNAMIC_QUEST_SET"
                            # print("WRITE DYNAMIC-Question")
                        else:
                            qtimetadatafield.find('fieldentry').text = "FIXED_QUEST_SET"
                            print("NO ENTRY IN <QUESTION_TYPE> ")

                    # if qtimetadatafield.find('fieldlabel').text == "author":
                    # qtimetadatafield.find('fieldentry').text = str(Formelfrage.autor_entry.get())

                    if qtimetadatafield.find('fieldlabel').text == "reset_processing_time":
                        qtimetadatafield.find('fieldentry').text = str(self.processing_time_reset)
                        if self.processing_time_reset == "":
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
                        qtimetadatafield.find('fieldentry').text = str(self.limit_time_betw_test_runs_month) + ":0" + str(
                            self.limit_time_betw_test_runs_day) + ":" + str(
                            self.limit_time_betw_test_runs_hour) + ":" + str(self.limit_time_betw_test_runs_minute) + ":00"
                        if self.limit_time_betw_test_runs_month == "MM":
                            qtimetadatafield.find('fieldentry').text = "00:000:00:00:00"
                            print(
                                " >WARNING< NO limit_time_betw_test_runs SET.. --> set limit_time to \"00:000:00:00:00\" ")

                    # Prüfungsansicht: Alle drei haken (Titel+Ansicht): "7" / Zwei Haken (Titel) = "3" / Zwei Haken (Name) = "5" / Ein Haken = "1" / "0" -> deaktiviert
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

                    # if qtimetadatafield.find('fieldlabel').text == "use_previous_answers":
                    # qtimetadatafield.find('fieldentry').text = "0"

                    # if qtimetadatafield.find('fieldlabel').text == "title_output":
                    # qtimetadatafield.find('fieldentry').text = "0"

                    # if qtimetadatafield.find('fieldlabel').text == "examid_in_test_pass":
                    # qtimetadatafield.find('fieldentry').text = "0"

                    # if qtimetadatafield.find('fieldlabel').text == "show_summary":
                    # qtimetadatafield.find('fieldentry').text = "0"

                    if qtimetadatafield.find('fieldlabel').text == "show_cancel":
                        qtimetadatafield.find('fieldentry').text = str(self.show_test_cancel)

                    # if qtimetadatafield.find('fieldlabel').text == "show_marker":
                    # qtimetadatafield.find('fieldentry').text = "99"

                    # if qtimetadatafield.find('fieldlabel').text == "fixed_participants":
                    # qtimetadatafield.find('fieldentry').text = "99"

                    #  if qtimetadatafield.find('fieldlabel').text == "showinfo":
                    # qtimetadatafield.find('fieldentry').text = "99"

                    if qtimetadatafield.find('fieldlabel').text == "shuffle_questions":
                        qtimetadatafield.find('fieldentry').text = str(self.mix_questions)

                    if qtimetadatafield.find('fieldlabel').text == "processing_time":
                        # self.minutes = self.limit_processing_time_minutes
                        hours_from_minutes = str(datetime.timedelta(minutes=int(self.limit_processing_time_minutes)))
                        print("len_min_to_hours: " + str(hours_from_minutes))

                        qtimetadatafield.find('fieldentry').text = "0" + hours_from_minutes

                    if qtimetadatafield.find('fieldlabel').text == "enable_examview":
                        qtimetadatafield.find('fieldentry').text = str(self.examview)

                    # if qtimetadatafield.find('fieldlabel').text == "show_examview_pdf":
                    # qtimetadatafield.find('fieldentry').text = "99"

                    if qtimetadatafield.find('fieldlabel').text == "starting_time":
                        qtimetadatafield.find('fieldentry').text = "P" + str(self.test_start_year) + "Y" + str(
                            self.test_start_month) + "M" + str(self.test_start_day) + "DT" + str(
                            self.test_start_hour) + "H" + str(self.test_start_minute) + "M" + "0S"
                        if self.test_start_year == "YYYY":
                            qtimetadatafield.find('fieldentry').text = "P2020Y1M1DT00H0M0S"
                            print(" >WARNING< NO STARTING TIME SET.. --> set START to \"P2020Y1M1DT00H0M0S\"")

                    if qtimetadatafield.find('fieldlabel').text == "ending_time":
                        qtimetadatafield.find('fieldentry').text = "P" + str(self.test_end_year) + "Y" + str(self.test_end_month) + "M" + str(self.test_end_day) + "DT" + str(self.test_end_hour) + "H" + str(self.test_end_minute) + "M" + "0S"
                        if self.test_end_year == "YYYY":
                            qtimetadatafield.find('fieldentry').text = "P2020Y12M30DT00H0M0S"
                            print(" >WARNING< NO ENDING TIME SET.. --> set END to \"P2020Y12M30DT00H0M0S\"")

                        if qtimetadatafield.find('fieldlabel').text == "autosave":
                            qtimetadatafield.find('fieldentry').text = str(self.autosave)

                        if qtimetadatafield.find('fieldlabel').text == "autosave_ival":
                            qtimetadatafield.find('fieldentry').text = str(self.autosave_interval)

                        # if qtimetadatafield.find('fieldlabel').text == "offer_question_hints":
                        # qtimetadatafield.find('fieldentry').text = "99"

                        # if qtimetadatafield.find('fieldlabel').text == "obligations_enabled":
                        # qtimetadatafield.find('fieldentry').text = "99"

                        if qtimetadatafield.find('fieldlabel').text == "enable_processing_time":
                            qtimetadatafield.find('fieldentry').text = str(self.processing_time)

                        # if qtimetadatafield.find('fieldlabel').text == "mark_step_0":
                        # qtimetadatafield.find('fieldentry').text = "99"

                        # if qtimetadatafield.find('fieldlabel').text == "mark_step_1":
                        # qtimetadatafield.find('fieldentry').text = "99"

                        # tree = ET.ElementTree(questestinterop)
                        # tree.write("WORKED_neuerAnfang.xml")

        print("Write Test_Settings to File --- ",self.profile_name)
        self.mytree.write(self.test_qti_file_path_output)
        print("Create Test WITH Test_settings")
