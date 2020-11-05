

from tkinter import *                  # Stellt die Funktionen für z.B. Labels & Entrys zur Verfügung
from tkinter import ttk                # Stellt die Funktionen der Comboboxen (Auswahlboxen) zur Verfügung
from tkinter import filedialog
import base64
import pathlib
import sqlite3





class SingleChoice:
    def __init__(self, singlechoice_tab):
        self.singlechoice_tab = singlechoice_tab

        ###### FRAMES

        self.sc_frame = LabelFrame(self.singlechoice_tab, text="Single Choice", padx=5, pady=5)
        self.sc_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)

        self.sc_frame_question_attributes = LabelFrame(self.singlechoice_tab, text="Fragen Attribute", padx=5, pady=5)
        self.sc_frame_question_attributes.grid(row=9, column=0, padx=170, pady=10, sticky="NW")

        self.sc_frame_question_description_functions = LabelFrame(self.singlechoice_tab, text="Fragentext Funktionen", padx=5, pady=5)
        self.sc_frame_question_description_functions.grid(row=9, column=0, padx=10, pady=10, sticky="NW")

        self.sc_frame_database = LabelFrame(self.singlechoice_tab, text="SingleChoice-Datenbank", padx=5, pady=5)
        self.sc_frame_database.grid(row=10, column=0, padx=10, pady=10, sticky=NW)
        ###################### -------- LABELS / ENTRYS / BUTTONS for "Single Choice" - FRAME ------- ############################
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
        # expr = r'$$  {\text{Zu berechnen ist:  }}\  sin(x^2)\ {\text{Textblock 2}}\ {formel2} $$'
        # preview(expr, viewer='file', filename='output.png')

        # file_image = ImageTk.PhotoImage(Image.open('output.png'))
        # file_image_label = Label(self.sc_frame, image=file_image)
        # file_image_label.image = file_image

        # def latex_preview():
        #    file_image_label.grid(row=20, column=1, pady=20)

        # self.myLatex_btn = Button(self.sc_frame, text="show LaTeX Preview", command=latex_preview)
        # self.myLatex_btn.grid(row=4, column=1, sticky=E)

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
        self.sc_check_mix_questions = Checkbutton(self.sc_frame, text="", variable=self.sc_var_mix_questions,
                                                  onvalue="1", offvalue="0")
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

        # ------------------------------- VARIABLES - TEXT & ENTRY --------------------------------------------
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


        self.sc_var1_points_entry = Entry(self.sc_frame, textvariable=self.sc_var1_points_text, width=8)
        self.sc_var2_points_entry = Entry(self.sc_frame, textvariable=self.sc_var2_points_text, width=8)
        self.sc_var3_points_entry = Entry(self.sc_frame, textvariable=self.sc_var3_points_text, width=8)
        self.sc_var4_points_entry = Entry(self.sc_frame, textvariable=self.sc_var4_points_text, width=8)
        self.sc_var5_points_entry = Entry(self.sc_frame, textvariable=self.sc_var5_points_text, width=8)
        self.sc_var6_points_entry = Entry(self.sc_frame, textvariable=self.sc_var6_points_text, width=8)
        self.sc_var7_points_entry = Entry(self.sc_frame, textvariable=self.sc_var7_points_text, width=8)

        # ------------------------------- VARIABLES BUTTONS - SELECT IMAGE --------------------------------------------
        self.sc_var1_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var1_img_label_entry, self.sc_var1_img_data))
        self.sc_var2_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var2_img_label_entry, self.sc_var2_img_data))
        self.sc_var3_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var3_img_label_entry, self.sc_var3_img_data))
        self.sc_var4_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var4_img_label_entry, self.sc_var4_img_data))
        self.sc_var5_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var5_img_label_entry, self.sc_var5_img_data))
        self.sc_var6_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var6_img_label_entry, self.sc_var6_img_data))
        self.sc_var7_select_img_btn = Button(self.sc_frame, text="Datei wählen", command=lambda: SingleChoice.sc_open_image(self, self.sc_var7_img_label_entry, self.sc_var7_img_data))

        self.sc_database_submit_singlechoice_btn = Button(self.sc_frame_database, text="Speichern unter neuer ID", command=lambda: SingleChoice.sc_submit(self))
        self.sc_database_submit_singlechoice_btn.grid(row=2, column=0, sticky=W, pady=5)

        # ------------------------------- VARIABLES  - TEXT & ENTRY --------------------------------------------

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
        self.sc_var1_points_entry.grid(row=10, column=2, sticky=W, padx=20)
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
            self.sc_var7_points_entry.grid(row=16, column=2, sticky=W, padx=20)
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

        ###################### -------- LABELS / ENTRYS / BUTTONS for "Fragen Attribute" - FRAME ------- ############################
        self.sc_question_difficulty_label = Label(self.sc_frame_question_attributes, text="Schwierigkeitsgrad der Frage")
        self.sc_question_difficulty_label.grid(row=0, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_difficulty_entry = Entry(self.sc_frame_question_attributes, width=10)
        self.sc_question_difficulty_entry.grid(row=0, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_category_label = Label(self.sc_frame_question_attributes, text="Fragenkategorie")
        self.sc_question_category_label.grid(row=1, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_category_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_category_entry.grid(row=1, column=1, pady=5, padx=5, sticky=W)

        self.sc_question_type_label = Label(self.sc_frame_question_attributes, text="Fragen-Typ")
        self.sc_question_type_label.grid(row=2, column=0, pady=5, padx=5, sticky=W)

        self.sc_question_type_entry = Entry(self.sc_frame_question_attributes, width=15)
        self.sc_question_type_entry.grid(row=2, column=1, pady=5, padx=5, sticky=W)
        self.sc_question_type_entry.insert(0, "Singlechoice")

        """
        ###################### -------- LABELS / ENTRYS / BUTTONS for "Fragentext Funktionen" - FRAME ------- ############################
        self.sc_add_latex_term_btn = Button( self.sc_frame_question_description_functions, text="Text \"Latex\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_latex(self))
        self.sc_add_latex_term_btn.grid(row=1, column=0, padx=10, sticky="W")

        self.sc_set_text_sub_btn = Button( self.sc_frame_question_description_functions, text="Text \"Tiefgestellt\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_sub(self))
        self.sc_set_text_sub_btn .grid(row=2, column=0, padx=10, pady=(10, 0), sticky="W")

        self.sc_set_text_sup_btn = Button( self.sc_frame_question_description_functions, text="Text \"Hochgestellt\"", command=lambda: Ilias_Test_Generator.Formelfrage.text_sup(self))
        self.sc_set_text_sup_btn.grid(row=3, column=0, padx=10, sticky="W")

        self.sc_set_text_italic_btn = Button( self.sc_frame_question_description_functions, text="Text \"Kursiv\"",command=lambda: Ilias_Test_Generator.Formelfrage.text_italic(self))
        self.sc_set_text_italic_btn.grid(row=4, column=0, padx=10, sticky="W")
        """

        ######  VARIABLES
        self.sc_var1_img_data_encoded64_string = ""
        self.sc_var2_img_data_encoded64_string = ""
        self.sc_var3_img_data_encoded64_string = ""
        self.sc_var4_img_data_encoded64_string = ""
        self.sc_var5_img_data_encoded64_string = ""
        self.sc_var6_img_data_encoded64_string = ""
        self.sc_var7_img_data_encoded64_string = ""






    def sc_open_image(self, var_img_label_entry, var_img_data_encoded64_string):


        ### Dateipfad auswählen

        self.sc_picture_name = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")
        #self.sc_picture_name = filename
        self.sc_sorted_picture_name = self.sc_picture_name
        self.sc_last_char_index = self.sc_sorted_picture_name.rfind("/")
        self.sc_foo = ([pos for pos, char in enumerate(self.sc_sorted_picture_name) if char == '/'])
        self.sc_foo_len = len(self.sc_foo)
        self.sc_picture_name_new = self.sc_sorted_picture_name[self.sc_foo[self.sc_foo_len - 1] + 1:-4]  # letzten char des bildnamens ist das dateiformat: Testbild.jpg
        self.sc_image_format_new = self.sc_picture_name[-4:]

        ### Bild-Namen entsprechendes Eingabefeld übertragen
        var_img_label_entry.insert(0, str(self.sc_picture_name_new) + str(self.sc_image_format_new))

        ### Bild-Daten in base64 speichern. Die XML Datei enthält die Bilder der Antworten in base64 encoded
        # "encoded64_string_raw enthält die Daten als String in der Form b'String'
        # Um die Daten in der richtigen Form zu erhalten (nur den String ohne b''), wird die Funktion .decode('utf-8') verwendet
        # Dieser String kann in der .xml Datei verwendet werden um im Ilias ein Bild zu erzeugen
        with open(self.sc_picture_name, "rb") as image_file:
            encoded64_string_raw = base64.b64encode(image_file.read())
            encoded64_string = encoded64_string_raw.decode('utf-8')
            var_img_data_encoded64_string = encoded64_string

        print(self.sc_picture_name)

    def sc_save_id_to_db(self):
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()

        # format of duration P0Y0M0DT0H30M0S
        self.sc_test_time = "P0Y0M0DT" + self.sc_proc_hours_box.get() + "H" + self.sc_proc_minutes_box.get() + "M" + self.sc_proc_seconds_box.get() + "S"

        # Insert into Table
        c.execute(
            "INSERT INTO my_table VALUES ("
            ":question_difficulty, :question_category, :question_type, "
            ":question_title, :question_description_title, :question_description_main, "
            ":response_1_text, :response_1_pts, :response_1_img_label, :response_1_img_string_base64_encoded,"
            ":response_2_text, :response_2_pts, :response_2_img_label, :response_2_img_string_base64_encoded,"
            ":response_3_text, :response_3_pts, :response_3_img_label, :response_3_img_string_base64_encoded,"
            ":response_4_text, :response_4_pts, :response_4_img_label, :response_4_img_string_base64_encoded,"
            ":response_5_text, :response_5_pts, :response_5_img_label, :response_5_img_string_base64_encoded,"
            ":response_6_text, :response_6_pts, :response_6_img_label, :response_6_img_string_base64_encoded,"
            ":response_7_text, :response_7_pts, :response_7_img_label, :response_7_img_string_base64_encoded,"
            ":response_8_text, :response_8_pts, :response_8_img_label, :response_8_img_string_base64_encoded,"
            ":response_9_text, :response_9_pts, :response_9_img_label, :response_9_img_string_base64_encoded,"
            ":response_10_text, :response_10_pts, :response_10_img_label, :response_10_img_string_base64_encoded,"
            ":description_img_name, :description_img_data, :test_time, :var_number, :res_number, :question_pool_tag)",
            {
                'question_difficulty': self.sc_question_difficulty_entry.get(),
                'question_category': self.sc_question_category_entry.get(),
                'question_type': self.sc_question_type_entry.get(),

                'question_title': self.sc_question_title_entry.get(),
                'question_description_title': self.sc_question_description_entry.get(),

                # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first character).
                # END is an imported constant which is set to the string "end". The END part means to read until the end of the text box is reached.
                # The only issue with this is that it actually adds a newline to our input. "
                # "So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while -2c would mean delete two characters, and so on."
                'question_description_main': self.sc_infobox.get("1.0", 'end-1c'),

                # Antwort-Text  in Datenbank-Fach: var_name
                'response_1_text': self.sc_var1_answer_text.get(),
                'response_1_pts': self.sc_var1_points_text.get(),
                'response_1_img_label': self.sc_var1_img_label_text.get(),
                'response_1_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_2_text': self.sc_var1_answer_text.get(),
                'response_2_pts': self.sc_var1_points_text.get(),
                'response_2_img_label': self.sc_var1_img_label_text.get(),
                'response_2_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_3_text': self.sc_var1_answer_text.get(),
                'response_3_pts': self.sc_var1_points_text.get(),
                'response_3_img_label': self.sc_var1_img_label_text.get(),
                'response_3_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_4_text': self.sc_var1_answer_text.get(),
                'response_4_pts': self.sc_var1_points_text.get(),
                'response_4_img_label': self.sc_var1_img_label_text.get(),
                'response_4_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_5_text': self.sc_var1_answer_text.get(),
                'response_5_pts': self.sc_var1_points_text.get(),
                'response_5_img_label': self.sc_var1_img_label_text.get(),
                'response_5_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_6_text': self.sc_var1_answer_text.get(),
                'response_6_pts': self.sc_var1_points_text.get(),
                'response_6_img_label': self.sc_var1_img_label_text.get(),
                'response_6_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_7_text': self.sc_var1_answer_text.get(),
                'response_7_pts': self.sc_var1_points_text.get(),
                'response_7_img_label': self.sc_var1_img_label_text.get(),
                'response_7_img_string_base64_encoded':  self.sc_var1_img_data_encoded64_string,

                'response_8_text': " ",
                'response_8_pts': " ",
                'response_8_img_label': " ",
                'response_8_img_string_base64_encoded': " ",

                'response_9_text': " ",
                'response_9_pts': " ",
                'response_9_img_label': " ",
                'response_9_img_string_base64_encoded': " ",

                'response_10_text': " ",
                'response_10_pts': " ",
                'response_10_img_label': " ",
                'response_10_img_string_base64_encoded': " ",

                'description_img_name': "",
                'description_img_data': "",

                'test_time': self.sc_test_time,

                'var_number': "",
                'res_number': "",
                'question_pool_tag': ""

            }
        )
        conn.commit()
        conn.close()

        print("Neuer Eintrag in die SingleChoice-Datenbank!")

    def sc_load_id_from_db(self):
        conn = sqlite3.connect('ilias_singlechoice_db.db')
        c = conn.cursor()
        record_id = self.load_box.get()
        c.execute("SELECT * FROM my_table WHERE oid =" + record_id)
        records = c.fetchall()

        self.sc_question_difficulty_entry.delete(0, END)
        self.sc_question_category_entry.delete(0, END)
        self.sc_question_type_entry.delete(0, END)

        self.sc_question_title_entry.delete(0, END)
        self.sc_question_description_entry.delete(0, END)
        self.sc_formula_question_entry.delete('1.0', 'end-1c')

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
    def sc_delete_id_from_db(self):
    def sc_edit_id(self):

