#############################################################################################################
#                                                                                                           #
#    Ilias Test - Generator_without_GUI                                                                     #
#    Version: 1.7.3                                                                                         #
#    Author:  Tobias Panteleit                                                                              #
#                                                                                                           #
#    Das Tool dient zur Erstellung von Fragen für die Ilias-Plattform.                                      #
#    In der derzeitigen Version (v1.7.3) wird sich auf die Erstellung von Formelfragen beschränkt           #
#                                                                                                           #
#    Neuerungen:                                                                                            #
#    - Unterstützung von Taxonomie Einträgen und nachträgliche Ergänzung von Taxonomien                     #                                          
#    - Bild-Dateien können nun aus Excel importiert und aus der Datenbank exportiert werden.                #
#    - $V und $R werden in der Fragenbeschreibung und in der Formel entsprechend in $v und $r konvertiert   #
#    - Bei der Erstellung von Fragenpools werden neue Ordner mit aufsteigender Nummerierung                 #                                          
#                                                                                                           #
#                                                                                                           #
# -------------------------------------------------------------------------------------------------         #
#    Behandlung der Excel-Inhalte:                                                                          #
#    Unter der Kategorie "Fragen-Typ" MUSS "Formelfrage" oder "Multiple Choice" eingetragen werden, da      #
#    ansonsten die Frage vom Programm nicht verwertbar ist                                                  #
#                                                                                                           #
#    Wird ein "Result" (1..10) ausgefüllt MUSS auch die entsprechende Spalte für "Result-pts" ein Wert      #
#    enthalten, ansonsten schlägt der Import nach ILIAS fehl.                                               #
#                                                                                                           #
#    Die Ordner zum zippen und importieren nach ILIAS befinden sich in                                      #
#        ILIAS-Fragenpool_zum_Import                                                                        #
#                                                                                                           #
#    Jeweils der Ordner mit der höchsten Nummer am Ende. Bei Programmstart darf sich in diesen              #
#    Ordnern keine *.zip o.ä. befinden!                                                                     #
#                                                                                                           #
#############################################################################################################



from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3  # verwendet für mySQL Datenbank
import xml.etree.ElementTree as ET
from sympy import *
import os
import pandas as pd  # used for import excel (xlsx) to mySQL_DB
import pathlib
import xlsxwriter
import shutil  # zum kopieren und zippen von Dateien
import openpyxl  # zum excel import von Bildern



class GuiMainWindow:

    def __init__(self, master):
        self.master = master
        master.title('ilias - Test-Generator_without_GUI v1.7.3')

        # --------------------------    Set PATH for Project

        self.project_root_path = pathlib.Path().absolute()
        self.img_file_path_create_folder = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
        self.img_file_path = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463', 'objects'))
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

        self.tst_file_path_write = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463','1590475954__0__tst_1944463.xml'))
        self.qti_file_path_write = os.path.normpath(os.path.join(self.project_root_path, 'ILIAS-Fragentest_tst_Daten', '1590475954__0__tst_1944463','1590475954__0__qti_1944463.xml'))

        # Question Pool - Files

        self.ilias_id_pool_qpl = "1596569820__0__qpl_" + str(max(self.filename_id) + 1)
        self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + str(max(self.filename_id) + 1) + ".xml"
        self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + str(max(self.filename_id) + 1) + ".xml"

        self.img_file_path_create_folder_pool = os.path.normpath(
            os.path.join(self.project_root_path, 'ILIAS-Fragenpool_qpl_Daten', self.ilias_id_pool_qpl, 'objects'))

        self.qpl_file_pool_path_read = os.path.normpath(os.path.join(self.project_root_path, 'orig_qpl_qti_files', 'orig_1594724569__0__qpl_1950628.xml'))
        self.qti_file_pool_path_read = os.path.normpath( os.path.join(self.project_root_path, 'orig_qpl_qti_files', 'orig_1594724569__0__qti_1950628.xml'))

        self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl,self.ilias_id_pool_qpl_xml))
        self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl,self.ilias_id_pool_qti_xml))

        # Taxonomy - Files
        self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services','Taxonomy', 'set_1', 'export.xml'))
        self.taxonomy_file_writes = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl, 'Services','Taxonomy', 'set_1', 'export.xml'))

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

        print("\n")


        # Read XML File


        self.picture_name = "EMPTY"



        # ---Init Variable Matrix
        Formelfrage.__init__(self)




    # create table / Database
    def create_database(self):
        # Create a database or connect to one
        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')

        # Create cursor
        c = conn.cursor()

        # Delete existing entries
        c.execute("DROP TABLE IF EXISTS my_table")

        # Create table
        c.execute("""CREATE TABLE IF NOT EXISTS my_table (
                question_difficulty text,
                question_category text,
                question_type text,
                question_title text,
                question_description_title text,
                question_description_main text,
                res1_formula text,
                res2_formula text,
                res3_formula text,
                res4_formula text,
                res5_formula text,
                res6_formula text,
                res7_formula text,
                res8_formula text,
                res9_formula text,
                res10_formula text,
                var1_name text,
                var1_min int,
                var1_max int,
                var1_prec int,
                var1_divby int,
                var1_unit text,
                var2_name text,
                var2_min int,
                var2_max int,
                var2_prec int,
                var2_divby int,
                var2_unit text,
                var3_name text,
                var3_min int,
                var3_max int,
                var3_prec int,
                var3_divby int,
                var3_unit text,
                var4_name text,
                var4_min int,
                var4_max int,
                var4_prec int,
                var4_divby int,
                var4_unit text,
                var5_name text,
                var5_min int,
                var5_max int,
                var5_prec int,
                var5_divby int,
                var5_unit text,
                var6_name text,
                var6_min int,
                var6_max int,
                var6_prec int,
                var6_divby int,
                var6_unit text,
                var7_name text,
                var7_min int,
                var7_max int,
                var7_prec int,
                var7_divby int,
                var7_unit text,
                var8_name text,
                var8_min int,
                var8_max int,
                var8_prec int,
                var8_divby int,
                var8_unit text,
                var9_name text,
                var9_min int,
                var9_max int,
                var9_prec int,
                var9_divby int,
                var9_unit text,
                var10_name text,
                var10_min int,
                var10_max int,
                var10_prec int,
                var10_divby int,
                var10_unit text,
                res1_name text,
                res1_min int,
                res1_max int,
                res1_prec int,
                res1_tol int,
                res1_points int,
                res1_unit text,
                res2_name text,
                res2_min int,
                res2_max int,
                res2_prec int,
                res2_tol int,
                res2_points int,
                res2_unit text,
                res3_name text,
                res3_min int,
                res3_max int,
                res3_prec int,
                res3_tol int,
                res3_points int,
                res3_unit text,
                res4_name text,
                res4_min int,
                res4_max int,
                res4_prec int,
                res4_tol int,
                res4_points int,
                res4_unit text,
                res5_name text,
                res5_min int,
                res5_max int,
                res5_prec int,
                res5_tol int,
                res5_points int,
                res5_unit text,
                res6_name text,
                res6_min int,
                res6_max int,
                res6_prec int,
                res6_tol int,
                res6_points int,
                res6_unit text,
                res7_name text,
                res7_min int,
                res7_max int,
                res7_prec int,
                res7_tol int,
                res7_points int,
                res7_unit text,
                res8_name text,
                res8_min int,
                res8_max int,
                res8_prec int,
                res8_tol int,
                res8_points int,
                res8_unit text,
                res9_name text,
                res9_min int,
                res9_max int,
                res9_prec int,
                res9_tol int,
                res9_points int,
                res9_unit text,
                res10_name text,
                res10_min int,
                res10_max int,
                res10_prec int,
                res10_tol int,
                res10_points int,
                res10_unit text,
                img_name text,
                img_data blop,
                test_time text,
                var_number int,
                res_number int,
                question_pool_tag text
                )""")

        # Commit Changes
        conn.commit()

        # Close Connection
        conn.close()




class Formelfrage(GuiMainWindow):

    def __init__(self):
        print("Excel-Datei zur Erstellung eines ILIAS-Fragenpools wählen:")

        GuiMainWindow.create_database(self)
        Database.excel_xlsx_import(self)
        Create_formelfrage_pool.__init__(self)





    def replace_symbols_in_formula(self):
        print("----------------------")
        print("Übernehme Formel aus Eingabefeld")

        self.formula1 = self.res1_formula_entry.get()
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


        return self.formula1

    def unit_table(self, selected_unit):
        self.unit_to_ilias_code = {"H": "125", "mH": "126", "µH": "127", "nH": "128", "kH": "129", "pH": "130",
                                   "F": "131", "mF": "132", "µF": "133", "nF": "134", "kF": "135",
                                   "W": "136", "kW": "137", "MW": "138", "mW": "149",
                                   "V": "139", "kV": "140", "mV": "141", "µV": "142", "MV": "143",
                                   "A": "144", "mA": "145", "µA": "146", "kA": "147",
                                   "Ohm": "148", "kOhm": "150", "mOhm": "151"}

        self.varTEST = selected_unit
        # print(self.varTEST)
        self.selected_unit = self.unit_to_ilias_code[self.varTEST]
        return self.selected_unit

    def read_XML(self):

        app.filename = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.select_taxonomy_file = app.filename

        self.folder_name = self.select_taxonomy_file.rsplit('/', 1)[-1]
        self.folder_name_split1 = self.folder_name[:15]
        self.folder_name_split2 = self.folder_name.rsplit('_', 1)[-1]


        self.taxonomy_exportXML_file = os.path.normpath(
            os.path.join(self.select_taxonomy_file, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.taxonomy_file_write = self.taxonomy_exportXML_file

        self.taxonomy_qtiXML_file = os.path.normpath(os.path.join(self.select_taxonomy_file,
                                                                  self.folder_name_split1 + "qti_" + self.folder_name_split2 + ".xml"))
        self.taxonomy_file_read = os.path.normpath(
            os.path.join(self.select_taxonomy_file, 'Services', 'Taxonomy', 'set_1', 'export.xml'))

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
        # self.sf_taxonomy.bind_arrow_keys(app)
        # self.sf_taxonomy.bind_scroll_wheel(app)

        # Create a frame within the ScrolledFrame
        self.taxonomy = self.sf_taxonomy.display_widget(Frame)

        self.taxonomy_frame_labels_scroll = LabelFrame(self.taxonomy, text="Fragen ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        # self.taxonomy_frame_labels2.bind_arrow_keys(app)
        # self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)

        # self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        # self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        self.taxonomy_frame_boxes = LabelFrame(self.taxonomy, text="Fragen ID's", padx=5, pady=5)
        self.taxonomy_frame_boxes.grid(row=0, column=1, padx=20, pady=10, sticky=NW)

        self.taxonomy_frame_tree = LabelFrame(self.taxonomy, text="Taxonomie Baum", padx=5, pady=5)
        self.taxonomy_frame_tree.grid(row=0, column=1, padx=20, pady=200, sticky=NW)

        # self.taxonomy_frame_tree_picture = LabelFrame(self.taxonomy, text="Taxonomie Bild", padx=5, pady=5)
        # self.taxonomy_frame_tree_picture.grid(row=2, column=1, padx=20, pady=10, sticky=NW)

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
        self.assign_to_node_btn = Button(self.taxonomy_frame_boxes, text="Fragen dem Knoten\nhinzufügen",
                                         command=lambda: Formelfrage.assign_questions_to_node(self))
        self.assign_to_node_btn.grid(row=4, column=0, sticky=W, pady=(20, 0))

        self.remove_from_node_btn = Button(self.taxonomy_frame_boxes, text="Fragen von Knoten\nentfernen",
                                           command=lambda: Formelfrage.remove_question_from_node(self))
        self.remove_from_node_btn.grid(row=4, column=1, sticky=W, padx=5, pady=(20, 0))

        self.tax_add_node_btn = Button(self.taxonomy_frame_tree, text="Neuen Knoten hinzufügen",
                                       command=lambda: Formelfrage.add_node_to_tax(self))
        self.tax_add_node_btn.grid(row=6, column=0, sticky=W, padx=5, pady=(20, 0))

        self.scan_tax_tree_btn = Button(self.taxonomy_frame_tree, text="scan_tax_tree",
                                        command=lambda: Formelfrage.scan_tax_tree(self))
        self.scan_tax_tree_btn.grid(row=6, column=1, sticky=W, padx=5, pady=(20, 0))

        self.update_taxonomy_name_btn = Button(self.taxonomy_frame_tree, text="Taxonomie-Namen\naktualisieren",
                                               command=lambda: Formelfrage.update_taxonomy_name(self))
        self.update_taxonomy_name_btn.grid(row=0, column=2, sticky=E, padx=5, pady=(5, 0))

        self.tax_remove_node_btn = Button(self.taxonomy_frame_tree, text="Knoten entfernen",
                                          command=lambda: Formelfrage.remove_node_from_tax(self))
        self.tax_remove_node_btn.grid(row=6, column=2, sticky=W, padx=5, pady=(20, 0))

        self.tax_reallocate_btn = Button(self.taxonomy_frame_tree, text="Taxonomie-Datei\nneu anordnen",
                                         command=lambda: Formelfrage.tax_reallocate(self))
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

        # print(len(self.ident))

        for id_text in self.item_id_list:
            label_id = Label(self.taxonomy_frame_labels, text=id_text)
            label_id.grid(sticky=W, pady=5, row=self.item_id_var, column=0)
            self.item_labels_list.append(str(label_id.cget("text")))
            # print("Label ID: " + str(label_id.cget("text")))

            label_placeholder = Label(self.taxonomy_frame_labels, text=" ---- ")
            label_placeholder.grid(sticky=W, pady=5, row=self.item_id_var, column=1)

            self.item_id_var = self.item_id_var + 1

        for title_text in self.item_title_list:
            label_title = Label(self.taxonomy_frame_labels, text=title_text)
            label_title.grid(sticky=W, pady=5, row=self.item_title_var, column=2)
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

        # print("Nodes found: " + str(self.node_tag))
        # print("with Child ID: " + str(self.child_tag))

        # convert list "child tag" and list "node_tag" to dictionary
        self.id_to_node_dict = dict(zip(self.child_tag, self.node_tag))
        self.node_to_id_dict = dict(zip(self.node_tag, self.child_tag))
        # print(self.id_to_node_dict)
        print("------------------------------------------------")

        print("\n")
        # print("------- Show Question assignments -------")
        for i in range(len(self.child_tag)):
            for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
                if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text == str(
                        self.child_tag[i]):  # Bsp. für Ebene 1 ID
                    self.item_in_node.append(str(self.child_tag[i]))
                    self.item_tag.append(tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text)
                    self.item_nr_list.append(self.item_labels_list.index(
                        tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text))

        for i in range(len(self.item_nr_list)):
            label_taxnode = Label(self.taxonomy_frame_labels,
                                  text=" --- " + str(self.id_to_node_dict.get(self.item_in_node[i])))
            label_taxnode.grid(sticky=W, pady=5, row=self.item_labels_list.index(self.item_tag[i]), column=4)

        # PRüfen ob die Fragen im Fragenpool konsistent sind (fortlaufende ID's
        self.check_question_id_start = str(self.item_labels_list[0])
        self.check_question_id_end = str(self.item_labels_list[len(self.item_labels_list) - 1])
        self.check_question_id_counter = int(self.check_question_id_start)

        # for i in range(len(self.item_labels_list)):
        #    if int(self.item_labels_list[i]) != int(self.check_question_id_counter):
        #        print("Error in Labels list", self.item_labels_list[i], self.check_question_id_counter)

        #    self.check_question_id_counter = self.check_question_id_counter + 1
        # print("Label-check DONE")

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
        # print("refresh_file_location: " + str(self.file_location))
        with open(self.file_location, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('ns0:', 'exp:')
        xml_str = xml_str.replace('ns2:', 'ds:')
        xml_str = xml_str.replace('ns3:', '')  # replace "x" with "new value for x"
        xml_str = xml_str.replace(
            '<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
            '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')
        xml_str = xml_str.replace(
            '<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Entity="tax" InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd">',
            '<exp:Export InstallationId="0" InstallationUrl="https://ilias.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://ilias.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://ilias.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://ilias.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')

        # print(self.var_use_question_pool_for_eAss_ilias)
        # Anpassung Taxonomie Datei (export.xml) für das Prüfungsilias
        # if self.var_use_question_pool_for_eAss_ilias == 1:
        #    xml_str = xml_str.replace('<exp:Export xmlns:ns0="http://www.ilias.de/Services/Export/exp/4_1" xmlns:ns2="http://www.ilias.de/Services/DataSet/ds/4_3" xmlns:ns3="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" InstallationId="0" InstallationUrl="https://f07.eassessment.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://f07.eassessment.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_ds_4_3.xsd">',
        #                              '<exp:Export InstallationId="0" InstallationUrl="https://f07.eassessment.th-koeln.de" Entity="tax" SchemaVersion="4.3.0" TargetRelease="5.4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:exp="http://www.ilias.de/Services/Export/exp/4_1" xsi:schemaLocation="http://www.ilias.de/Services/Export/exp/4_1 https://f07.eassessment.th-koeln.de/xml/ilias_export_4_1.xsd http://www.ilias.de/Services/Taxonomy/tax/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_tax_4_3.xsd http://www.ilias.de/Services/DataSet/ds/4_3 https://f07.eassessment.th-koeln.de/xml/ilias_ds_4_3.xsd" xmlns="http://www.ilias.de/Services/Taxonomy/tax/4_3" xmlns:ds="http://www.ilias.de/Services/DataSet/ds/4_3">')

        with open(self.file_location, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

            # print(self.file_location)
        # print("Taxonomie Datei editiert")

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
        Child.text = str(int(max(self.collect_childs)) + 1)

        if self.tax_node_parent_entry.get() == "":
            Parent.text = str(min(self.collect_childs))
            Depth.text = str(int(min(self.collect_depth)) + 1)
            if Depth.text == "1":
                Type.text = ""
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)  # Änderung min() auf max()
            else:
                Type.text = "taxn"  # fix
                Title.text = str(self.tax_node_name_entry.get())
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)


        else:
            Parent.text = str(self.title_to_id_dict.get(self.tax_node_parent_entry.get()))
            Depth.text = str(int(self.title_to_depth_dict.get(self.tax_node_parent_entry.get())) + 1)
            Type.text = "taxn"  # fix
            Title.text = str(self.tax_node_name_entry.get())
            OrderNr.text = str(int(max(self.collect_order_nr)) + 1)

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

        # print(self.collect_order_nr)

        # Taxonomie Datei nach Hauptebene (ID und Name) suchen
        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Tax'):
            if TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text == "1970392":
                self.tax_root_id = TaxId.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Id').text

        # print(self.collect_childs)
        # print(self.collect_title)
        # print(self.collect_depth)
        # print(self.collect_parent)
        # print(self.collect_order_nr)

        self.collect_title.pop(0)
        self.title_to_id_dict = {}
        self.title_to_id_dict = dict(zip(self.collect_title, self.collect_childs))

        self.title_to_depth_dict = {}
        self.title_to_depth_dict = dict(zip(self.collect_title, self.collect_depth))

        # for i in range(len(self.collect_title)):
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
        Child.text = str(int(max(self.collect_childs)) + 1)

        # Wenn kein "Parent"-Node existiert
        if parent_node_name == "EMPTY":
            Parent.text = str(min(self.collect_childs))
            Depth.text = str(int(min(self.collect_depth)) + 1)
            if Depth.text == "1":
                Type.text = ""
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)  # Änderung min() auf max()
                # print("ORderNr: " + OrderNr.text)
            else:
                Type.text = "taxn"  # fix
                Title.text = str(new_node_name)
                OrderNr.text = str(int(max(self.collect_order_nr)) + 1)
                # print("ORderNr: " + OrderNr.text)

        else:
            Parent.text = str(self.title_to_id_dict.get(parent_node_name))
            Depth.text = str(int(self.title_to_depth_dict.get(parent_node_name)) + 1)
            Type.text = "taxn"  # fix
            Title.text = str(new_node_name)
            OrderNr.text = str(int(max(self.collect_order_nr)) + 1)

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

            # if self.root_node != "000000":
            #    print("Root Node found: " + str(self.root_node))
            # else:
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

        # print("Nodes found: " + str(self.node_tag))
        # print("with Child ID: " + str(self.child_tag))

        # convert list "child tag" and list "node_tag" to dictionary
        self.node_to_id_dict = dict(zip(self.node_tag_assign, self.child_tag_assign))
        # print("------------------------------------------------")

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

        # Rec = ET.SubElement(DataSet, 'ds:Rec')
        Rec.set('Entity', "tax_node_assignment")
        # ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

        NodeId.text = self.node_to_id_dict.get(item_pool)

        Component.text = "qpl"  # fix
        ItemType.text = "quest"  # fix
        ItemId.text = item_id  # Fragen ID üblicherweise > 100000, wenn Fragen ID z.B. 000001 dann ist der itemValue "nur" 1 und es fehlen nullen
        self.myroot[0][len(self.myroot[0]) - 1].append(Rec)

        # print("NodeId: " + NodeId.text)
        # print("ItemId: " + ItemId.text)

        self.mytree.write(file_location)

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, file_location)

    ##########################################################################

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

        self.reallocate_item_list = list(zip(self.reallocate_item_id, self.reallocate_node_id))

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
        print("Fragen in Nodes werden aktualisiert...")

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

        self.reallocate_item_list = list(zip(self.reallocate_item_id, self.reallocate_node_id))

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

    def tax_combobox_refresh(self):

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

        self.taxonomy_frame_tree_picture2 = ScrolledFrame(self.taxonomy_frame_tree_picture_scroll, height=250,
                                                          width=200)
        self.taxonomy_frame_tree_picture2.pack(expand=1, fill="both")

        ### Bind the arrow keys and scroll wheel
        ### Funktion hat keine auswirkungen, erzeugt jedoch (vernachlässigbare) Fehler
        # self.taxonomy_frame_tree_picture2.bind_arrow_keys(app)
        # self.taxonomy_frame_tree_picture2.bind_scroll_wheel(app)
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

            # print(self.parentId_to_title_dict)

        for child in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Child'):
            self.collect_childs.append(child.text)

        for parent in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Parent'):
            self.collect_parent.append(parent.text)

        for depth in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Depth'):
            self.collect_depth.append(depth.text)

        for title in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}Title'):
            self.collect_title.append(title.text)
            # print(title.text)
        for order_nr in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}OrderNr'):
            self.collect_order_nr.append(order_nr.text)

        self.tax_data = list(zip(self.collect_childs, self.collect_parent, self.collect_depth, self.collect_title,
                                 self.collect_order_nr))

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
            # print(self.collect_parent[i], self.collect_childs[i],self.id_to_depth_dict.get(self.collect_childs[i]), self.collect_title[i], self.collect_order_nr[i])

            if self.id_to_depth_dict.get(self.collect_childs[i]) == "2":
                self.tax_depth_1_label = Label(self.taxonomy_frame_tree_picture,
                                               text="     " + str(self.collect_title[i]))
                # self.tax_depth_1_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_1_label.cget("text"))

            if self.id_to_depth_dict.get(self.collect_childs[i]) == "3":
                self.tax_depth_2_label = Label(self.taxonomy_frame_tree_picture, text="         " + str(
                    self.id_to_title_dict.get(self.collect_parent[i])) + "   ===>   " + str(self.collect_title[i]))
                # self.tax_depth_2_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_2_label.cget("text"))

            if self.id_to_depth_dict.get(self.collect_childs[i]) == "4":
                self.tax_depth_3_label = Label(self.taxonomy_frame_tree_picture, text="            " + str(
                    self.id_to_title_dict.get(
                        self.parentId_from_id_dict.get(self.collect_parent[i]))) + "  ===>    " + str(
                    self.id_to_title_dict.get(self.collect_parent[i])) + "   ===>   " + str(self.collect_title[i]))
                # self.tax_depth_3_label.grid(sticky=W)
                self.collect_labels_sorted.append(self.tax_depth_3_label.cget("text"))

        for i in range(len(self.collect_labels_sorted)):
            self.collect_labels_sorted[i] = self.collect_labels_sorted[i].strip()

        self.collect_labels_sorted.sort()

        for i in range(len(self.collect_labels_sorted)):

            self.depth_count = "0"
            self.depth_count = self.collect_labels_sorted[i].count("==>")

            if self.depth_count == 0:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture,
                                           text="     " + self.collect_labels_sorted[i])
                self.sorted_labels.grid(sticky=W)

            if self.depth_count == 1:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture,
                                           text="         " + self.collect_labels_sorted[i])
                self.sorted_labels.grid(sticky=W)

            if self.depth_count == 2:
                self.sorted_labels = Label(self.taxonomy_frame_tree_picture,
                                           text="            " + self.collect_labels_sorted[i])
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

            for i in range(self.starting_id, self.ending_id + 1):
                for tax_node in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}TaxNodeAssignment'):
                    if tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId').text == str(i):
                        print("ID found: " + str(i))

        if self.node_to_id_dict.get(self.tax_nodes_myCombo.get()) != self.child_tag[0]:
            if self.entry_starting_id.get() != "" and self.entry_ending_id.get() != "":

                for i in range(self.starting_id, self.ending_id + 1):
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

                    # Rec = ET.SubElement(DataSet, 'ds:Rec')
                    Rec.set('Entity', "tax_node_assignment")
                    # ItemId = ET.SubElement(TaxNodeAssignment, 'ItemId')

                    NodeId.text = self.node_to_id_dict.get(self.tax_nodes_myCombo.get())

                    Component.text = "qpl"  # fix
                    ItemType.text = "quest"  # fix
                    ItemId.text = str(
                        i)  # Fragen ID üblicherweise > 100000, wenn Fragen ID z.B. 000001 dann ist der itemValue "nur" 1 und es fehlen nullen
                    self.myroot[0][len(self.myroot[0]) - 1].append(Rec)

                    # print("NodeId: " + NodeId.text)
                    # print("ItemId: " + ItemId.text)

                    self.mytree.write(self.taxonomy_file_write)

            else:
                print("Need starting/ending ID")
        else:
            print("Node for Questions not selected")

        # Taxonomie-datei "refreshen"
        Formelfrage.tax_file_refresh(self, self.taxonomy_exportXML_file)

        # Taxonomie Fesnter wird "refreshed" um Text der Labels zu aktualisieren
        self.taxonomy_frame_labels.destroy()

        self.taxonomy_frame_labels_scroll = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        # self.taxonomy_frame_labels2.bind_arrow_keys(app)
        # self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)

        # self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        # self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

        Formelfrage.read_taxonomy_file(self)

    def test(self):
        self.taxonomy_qtiXML_file = os.path.normpath(
            os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten", self.ilias_id_pool_qpl,
                         self.ilias_id_pool_qti_xml))

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
                        print("removed from Node: " + str(
                            tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text))
                        tax_node.find('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId').text = "00000"
                        self.mytree.write(self.taxonomy_file_write)
                        # print("Code auf 00000")

        for node_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}NodeId'):
            self.node_id.append(node_id.text)

        for item_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ItemId'):
            self.item_id.append(item_id.text)

        self.item_list = list(zip(self.item_id, self.node_id))

        # Alle TaxNodeAssignments löschen
        for rec in self.myroot.iter('{http://www.ilias.de/Services/DataSet/ds/4_3}DataSet'):
            for child in list(rec):
                # print(child)
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

        self.taxonomy_frame_labels_scroll = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        self.taxonomy_frame_labels_scroll.grid(row=0, column=0, padx=20, pady=10, sticky=NW)
        self.taxonomy_frame_labels2 = ScrolledFrame(self.taxonomy_frame_labels_scroll, height=700, width=500)
        self.taxonomy_frame_labels2.pack(expand=1, fill="both")
        # self.taxonomy_frame_labels2.bind_arrow_keys(app)
        # self.taxonomy_frame_labels2.bind_scroll_wheel(app)
        self.taxonomy_frame_labels = self.taxonomy_frame_labels2.display_widget(Frame)

        # self.taxonomy_frame_labels = LabelFrame(self.taxonomy, text="Question ID's", padx=5, pady=5)
        # self.taxonomy_frame_labels.grid(row=0, column=0, padx=20, pady=10, sticky=NW)

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
            self.search_p1_begin = self.formula_question_entry.search('^', self.search_index_start, stopindex="end")
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
            self.search_b1_begin = self.formula_question_entry.search('_', self.search_index_start, stopindex="end")
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
                self.search_italic1_begin = self.formula_question_entry.search('//', self.search_index_start,
                                                                               stopindex="end")
                self.search_italic1_end = self.formula_question_entry.search('///', self.search_italic1_begin,
                                                                             stopindex="end")
                self.formula_question_entry.tag_add('ITALIC', self.search_italic1_begin,
                                                    self.search_italic1_end + '+3c')
                self.formula_question_entry.tag_config('ITALIC', foreground='brown')
                self.formula_question_entry.tag_config('ITALIC', font=('Times New Roman', 9, 'italic'))
                self.search_index_start = self.search_italic1_end + '+3c'
                self.search_index_end = self.search_italic1_begin

            except:
                print("Index error in italic-function -> can be ignored ")

        print("Question entry text... re-allocated!")
        # -----------------------Place Label & Entry-Boxes for Variable  on GUI



class Database(Formelfrage):

    def excel_xlsx_import(self):

        self.xlsx_path = filedialog.askopenfilename(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.xlsx_data = pd.read_excel(self.xlsx_path)

        self.last_char_index = self.xlsx_path.rfind("/")
        self.foo2 = ([pos for pos, char in enumerate(self.xlsx_path) if char == '/'])
        self.foo2_len = len(self.foo2)
        self.xlsx_name = self.xlsx_path[self.foo2[self.foo2_len - 1] + 1:]

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

        # df = pd.read_excel(self.file_name, sheet_name=self.sheet_name, dtype=object)

        for img in self.worksheet._images:
            img.ref.seek(0)
            self.df.iat[img.anchor.to.row - 1, img.anchor.to.col] = img.ref.read()

        ################## Bilder auslesen

        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
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

        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
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

                self.check_if_string_data = isinstance(column_data, str)
                self.check_if_integer_data = isinstance(column_data, int)
                self.check_if_float_data = isinstance(column_data, float)


                if self.check_if_string_data == false and self.check_if_integer_data == false and self.check_if_float_data == false:

                    with open('export_img' + str(row_index) + '.png', 'wb') as image_file:
                        image_file.write(column_data)
                        excel_sheet.insert_image('ER' + str(row_index + 1),
                                                 str(self.project_root_path) + '/export_img' + str(row_index) + '.png',
                                                 {'object_position': 2, 'x_scale': x_scale, 'y_scale': y_scale})




                else:

                    excel_sheet.write(row_index, column_index, column_data, body_cell_format)
                column_index += 1
            row_index += 1

        print(str(row_index) + ' rows written successfully to ' + excel.filename)

        # Closing workbook
        excel.close()

        # query = ("SELECT question_difficulty, question_category, question_type, question_title, question_description_title,question_description_main")

    def ilias_test_to_sql_import(self):
        app.filename = filedialog.askdirectory(initialdir=pathlib.Path().absolute(), title="Select a File")
        self.select_test_import_file = app.filename
        print(self.select_test_import_file)

        self.ilias_folder_name = self.select_test_import_file.rsplit('/', 1)[-1]
        self.ilias_folder_name_split1 = self.ilias_folder_name[:15]
        self.ilias_folder_name_split2 = self.ilias_folder_name.rsplit('_', 1)[-1]
        self.ilias_test_qti_file = os.path.normpath(os.path.join(self.select_test_import_file,
                                                                 self.ilias_folder_name_split1 + "qti_" + self.ilias_folder_name_split2 + ".xml"))

        self.ilias_test_title = []
        self.ilias_test_question_description_title = []
        self.ilias_test_question_description = []

        self.ilias_test_question_description_image_name = []
        self.ilias_test_question_description_image_uri = []

        self.ilias_test_duration = []
        self.ilias_test_question_points = []

        self.ilias_test_variable1_prec = []
        self.ilias_test_variable1_divby = []
        self.ilias_test_variable1_min = []
        self.ilias_test_variable1_max = []

        self.ilias_test_variable2_prec = []
        self.ilias_test_variable2_divby = []
        self.ilias_test_variable2_min = []
        self.ilias_test_variable2_max = []

        self.ilias_test_variable3_prec = []
        self.ilias_test_variable3_divby = []
        self.ilias_test_variable3_min = []
        self.ilias_test_variable3_max = []

        self.ilias_test_variable4_prec = []
        self.ilias_test_variable4_divby = []
        self.ilias_test_variable4_min = []
        self.ilias_test_variable4_max = []

        self.ilias_test_variable5_prec = []
        self.ilias_test_variable5_divby = []
        self.ilias_test_variable5_min = []
        self.ilias_test_variable5_max = []

        self.ilias_test_variable6_prec = []
        self.ilias_test_variable6_divby = []
        self.ilias_test_variable6_min = []
        self.ilias_test_variable6_max = []

        self.ilias_test_variable7_prec = []
        self.ilias_test_variable7_divby = []
        self.ilias_test_variable7_min = []
        self.ilias_test_variable7_max = []

        self.ilias_test_variable8_prec = []
        self.ilias_test_variable8_divby = []
        self.ilias_test_variable8_min = []
        self.ilias_test_variable8_max = []

        self.ilias_test_variable9_prec = []
        self.ilias_test_variable9_divby = []
        self.ilias_test_variable9_min = []
        self.ilias_test_variable9_max = []

        self.ilias_test_variable10_prec = []
        self.ilias_test_variable10_divby = []
        self.ilias_test_variable10_min = []
        self.ilias_test_variable10_max = []

        # Werte für die Variable 1 in der Reihenfolge: "Präzision", "divby", "range_min", "range_max",
        self.ilias_test_variable1 = []
        self.ilias_test_variable2 = []
        self.ilias_test_variable3 = []
        self.ilias_test_variable4 = []
        self.ilias_test_variable5 = []
        self.ilias_test_variable6 = []
        self.ilias_test_variable7 = []
        self.ilias_test_variable8 = []
        self.ilias_test_variable9 = []
        self.ilias_test_variable10 = []

        self.ilias_test_result1 = []
        self.ilias_test_result1_prec = []
        self.ilias_test_result1_tol = []
        self.ilias_test_result1_min = []
        self.ilias_test_result1_max = []
        self.ilias_test_result1_pts = []
        self.ilias_test_result1_formula = []

        self.ilias_test_result2 = []
        self.ilias_test_result2_prec = []
        self.ilias_test_result2_tol = []
        self.ilias_test_result2_min = []
        self.ilias_test_result2_max = []
        self.ilias_test_result2_pts = []
        self.ilias_test_result2_formula = []

        self.ilias_test_result3 = []
        self.ilias_test_result3_prec = []
        self.ilias_test_result3_tol = []
        self.ilias_test_result3_min = []
        self.ilias_test_result3_max = []
        self.ilias_test_result3_pts = []
        self.ilias_test_result3_formula = []

        self.ilias_test_result4 = []
        self.ilias_test_result4_prec = []
        self.ilias_test_result4_tol = []
        self.ilias_test_result4_min = []
        self.ilias_test_result4_max = []
        self.ilias_test_result4_pts = []
        self.ilias_test_result4_formula = []

        self.ilias_test_result5 = []
        self.ilias_test_result5_prec = []
        self.ilias_test_result5_tol = []
        self.ilias_test_result5_min = []
        self.ilias_test_result5_max = []
        self.ilias_test_result5_pts = []
        self.ilias_test_result5_formula = []

        self.ilias_test_result6 = []
        self.ilias_test_result6_prec = []
        self.ilias_test_result6_tol = []
        self.ilias_test_result6_min = []
        self.ilias_test_result6_max = []
        self.ilias_test_result6_pts = []
        self.ilias_test_result6_formula = []

        self.ilias_test_result7 = []
        self.ilias_test_result7_prec = []
        self.ilias_test_result7_tol = []
        self.ilias_test_result7_min = []
        self.ilias_test_result7_max = []
        self.ilias_test_result7_pts = []
        self.ilias_test_result7_formula = []

        self.ilias_test_result8 = []
        self.ilias_test_result8_prec = []
        self.ilias_test_result8_tol = []
        self.ilias_test_result8_min = []
        self.ilias_test_result8_max = []
        self.ilias_test_result8_pts = []
        self.ilias_test_result8_formula = []

        self.ilias_test_result9 = []
        self.ilias_test_result9_prec = []
        self.ilias_test_result9_tol = []
        self.ilias_test_result9_min = []
        self.ilias_test_result9_max = []
        self.ilias_test_result9_pts = []
        self.ilias_test_result9_formula = []

        self.ilias_test_result10 = []
        self.ilias_test_result10_prec = []
        self.ilias_test_result10_tol = []
        self.ilias_test_result10_min = []
        self.ilias_test_result10_max = []
        self.ilias_test_result10_pts = []
        self.ilias_test_result10_formula = []

        # XML Datei "qti" einlesen
        self.mytree = ET.parse(self.ilias_test_qti_file)
        self.myroot = self.mytree.getroot()

        for item in self.myroot.iter('item'):
            # print(item.get('title'))
            self.ilias_test_title.append(item.get('title'))

        for comment in self.myroot.iter('qticomment'):
            if comment.text == None:
                comment.text = ""

        for item in self.myroot.iter('item'):
            if "" in item.find('qticomment').text:
                self.ilias_test_question_description_title.append(item.find('qticomment').text)

        for item in self.myroot.iter('item'):
            if "" in item.find('duration').text:
                self.ilias_test_duration.append(item.find('duration').text)

        for qtimetadatafield in self.myroot.iter('qtimetadatafield'):

            if qtimetadatafield.find('fieldlabel').text == "QUESTIONTYPE":
                self.ilias_question_type = qtimetadatafield.find('fieldentry').text

            if qtimetadatafield.find('fieldlabel').text == "points":
                self.ilias_test_question_points.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v1":
                self.ilias_test_variable1.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v2":
                self.ilias_test_variable2.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v3":
                self.ilias_test_variable3.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v4":
                self.ilias_test_variable4.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v5":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v6":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v7":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v8":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v9":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$v10":
                self.ilias_test_variable5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r1":
                self.ilias_test_result1.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r2":
                self.ilias_test_result2.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r3":
                self.ilias_test_result3.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r4":
                self.ilias_test_result4.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r5":
                self.ilias_test_result5.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r6":
                self.ilias_test_result6.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r7":
                self.ilias_test_result7.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r8":
                self.ilias_test_result8.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r9":
                self.ilias_test_result9.append(qtimetadatafield.find('fieldentry').text)

            if qtimetadatafield.find('fieldlabel').text == "$r10":
                self.ilias_test_result10.append(qtimetadatafield.find('fieldentry').text)

        # for mattext in self.myroot.iter('mattext'):
        #    self.ilias_test_question_description.append(mattext.text)

        for flow in self.myroot.iter('flow'):
            for material in flow.iter('material'):
                if "" in material.find('mattext').text:

                    # Wenn in dem Fragentext "img" enthalten ist, gibt es immer auch ein Bild zu der Frage
                    if "il_0_mob_" in material.find('mattext').text:
                        self.ilias_test_question_description.append(material.find('mattext').text)

                        # Bildname hinzufügen
                        if material.find('matimage').attrib.get('label'):
                            self.ilias_test_question_description_image_name.append(
                                material.find('matimage').attrib.get('label'))
                        # Bild Pfad hinzufügen
                        if material.find('matimage').attrib.get('uri'):
                            self.ilias_test_question_description_image_uri.append(
                                material.find('matimage').attrib.get('uri'))
                    else:
                        self.ilias_test_question_description.append(material.find('mattext').text)
                        self.ilias_test_question_description_image_name.append("EMPTY")
                        self.ilias_test_question_description_image_uri.append("EMPTY")

        # for flow in self.myroot.iter('flow'):
        #     for material in flow.iter('material'):
        #         if material.find('matimage').attrib.get('label'):
        #                 self.ilias_test_question_description_image_name.append(material.find('matimage').attrib.get('label'))

        # for flow in self.myroot.iter('flow'):
        #    for material in flow.iter('material'):
        #        if "" in material.find('matimage').attrib.get('uri'):
        #                self.ilias_test_question_description_image_uri.append(material.find('matimage').attrib.get('uri'))

        print("LABEL - NAMES")
        print(self.ilias_test_question_description_image_name)
        print(self.ilias_test_question_description_image_uri)
        # print("LÄNGE DER BESHREIBUNG: ")
        # print("länge von iter: " + str(len(self.test_iter)))
        # print(self.test_iter)

        # for i in range(len(self.ilias_test_question_description)):
        #    print(self.ilias_test_question_description[i])

        # Liste mit Fragenbeschreibungen enthalten in
        # Fach 1: "Willkommen zur Probe-Klausurl.."
        # Fach 2: "Hiermit versichere ich an Eides statt.."
        # Nach .pop(0) wird das Feld gelöscht und die List-Plätze nach vorne geschoben.
        # Um Feld 0 und 1 zu löschen muss daher zweimal der Befehl pop(0) ausgeführt werden
        # self.ilias_test_question_description.pop(0)
        # self.ilias_test_question_description.pop(0)
        # print("LÄNGE DER BESHREIBUNG 2: " + str(len(self.ilias_test_question_description)))

        # print()
        # print("+++++++++++++++++++++++++++++++++++++++")
        """
        self.string_split = []
        self.index_with_img = []


        print()
        print("+++++++++++++++++++++++")
        print(self.ilias_test_question_description[0])
        print("-----------------------")

        # String nach /p aufsplitten um an den Bild-String zu kommen
        self.string_split = self.ilias_test_question_description[0].split('</p>')
        print("LÄNGE SPLIT: " + str(len(self.string_split)))

        for i in range(len(self.string_split)):
            if "img" in self.string_split[i]:
                self.string_with_img = self.string_split[i]
                print("Wert i: " + str(i))
                self.index_with_img.append(i)

        print(self.index_with_img)

        for i in range(len(self.index_with_img)):
            self.string_split.pop(self.index_with_img[i])

        print("original")
        print(self.string_split)
        print("=======================")
        print("JOINED")
        print('</p>'.join(self.string_split))
        print("++++++++++++++++++++++")
        print("Just IMAGE")
        #print(self.string_with_img)
        print()
        """

        print()
        print("äääääääääääääääääääääääääääääääääää")
        print(self.ilias_test_question_description)

        self.test_list1 = []
        self.test_list1_l_join = []

        for i in range(len(self.ilias_test_question_description)):

            # Text aus Fach übernehmen
            self.test_neu1 = self.ilias_test_question_description[i]

            # Text auftrennen nach Beschreibung und IMG
            self.test_list1 = self.test_neu1.split('</p>')

            # IMG teil löschen
            for i in range(len(self.test_list1)):
                if "img" in self.test_list1[i]:
                    self.test_list1.pop(i)
                    break

            self.test_list1_l_join.append('</p>'.join(self.test_list1))

        for i in range(len(self.test_list1_l_join)):
            self.test_list1_l_join[i] = self.test_list1_l_join[i].replace('<p>', "")
            self.test_list1_l_join[i] = self.test_list1_l_join[i].replace('</p>', "")

        print("Anzahl der Fragen: " + str(len(self.ilias_test_title)))
        # print("Anzahl der Beschreibungen: " + str(len(self.ilias_test_question_description_title)))
        # print("Anzahl der Zeiten " + str(len(self.ilias_test_duration)))
        # print("Anzahl der Punkte " + str(len(self.ilias_test_question_points)))
        # print("Anzahl der Variablen1 " + str(len(self.ilias_test_variable1)))
        # print(self.ilias_test_variable1)

        self.ilias_test_variable1_settings = []
        self.ilias_test_variable1_settings_2nd = []
        self.ilias_test_variable2_settings = []
        self.ilias_test_variable2_settings_2nd = []
        self.ilias_test_variable3_settings = []
        self.ilias_test_variable3_settings_2nd = []
        self.ilias_test_variable4_settings = []
        self.ilias_test_variable4_settings_2nd = []
        self.ilias_test_variable5_settings = []
        self.ilias_test_variable5_settings_2nd = []
        self.ilias_test_variable6_settings = []
        self.ilias_test_variable6_settings_2nd = []
        self.ilias_test_variable7_settings = []
        self.ilias_test_variable7_settings_2nd = []
        self.ilias_test_variable8_settings = []
        self.ilias_test_variable8_settings_2nd = []
        self.ilias_test_variable9_settings = []
        self.ilias_test_variable9_settings_2nd = []
        self.ilias_test_variable10_settings = []
        self.ilias_test_variable10_settings_2nd = []

        self.ilias_test_result1_settings = []
        self.ilias_test_result1_settings_2nd = []
        self.ilias_test_result2_settings = []
        self.ilias_test_result2_settings_2nd = []
        self.ilias_test_result3_settings = []
        self.ilias_test_result3_settings_2nd = []
        self.ilias_test_result4_settings = []
        self.ilias_test_result4_settings_2nd = []
        self.ilias_test_result5_settings = []
        self.ilias_test_result5_settings_2nd = []
        self.ilias_test_result6_settings = []
        self.ilias_test_result6_settings_2nd = []
        self.ilias_test_result7_settings = []
        self.ilias_test_result7_settings_2nd = []
        self.ilias_test_result8_settings = []
        self.ilias_test_result8_settings_2nd = []
        self.ilias_test_result9_settings = []
        self.ilias_test_result9_settings_2nd = []
        self.ilias_test_result10_settings = []
        self.ilias_test_result10_settings_2nd = []

        # Liste Variable 1 - Werte auftrennen nach ";"
        for i in range(len(self.ilias_test_variable1)):
            self.ilias_test_variable1_settings += self.ilias_test_variable1[i].split(";")

        for i in range(len(self.ilias_test_variable2)):
            self.ilias_test_variable2_settings += self.ilias_test_variable2[i].split(";")

        for i in range(len(self.ilias_test_variable3)):
            self.ilias_test_variable3_settings += self.ilias_test_variable3[i].split(";")

        for i in range(len(self.ilias_test_variable4)):
            self.ilias_test_variable4_settings += self.ilias_test_variable4[i].split(";")

        for i in range(len(self.ilias_test_variable5)):
            self.ilias_test_variable5_settings += self.ilias_test_variable5[i].split(";")

        for i in range(len(self.ilias_test_variable6)):
            self.ilias_test_variable6_settings += self.ilias_test_variable6[i].split(";")

        for i in range(len(self.ilias_test_variable7)):
            self.ilias_test_variable7_settings += self.ilias_test_variable7[i].split(";")

        for i in range(len(self.ilias_test_variable8)):
            self.ilias_test_variable8_settings += self.ilias_test_variable8[i].split(";")

        for i in range(len(self.ilias_test_variable9)):
            self.ilias_test_variable9_settings += self.ilias_test_variable9[i].split(";")

        for i in range(len(self.ilias_test_variable10)):
            self.ilias_test_variable10_settings += self.ilias_test_variable10[i].split(";")

        for i in range(len(self.ilias_test_result1)):
            self.ilias_test_result1_settings += self.ilias_test_result1[i].split(";")

        for i in range(len(self.ilias_test_result2)):
            self.ilias_test_result2_settings += self.ilias_test_result2[i].split(";")

        for i in range(len(self.ilias_test_result3)):
            self.ilias_test_result3_settings += self.ilias_test_result3[i].split(";")

        for i in range(len(self.ilias_test_result4)):
            self.ilias_test_result4_settings += self.ilias_test_result4[i].split(";")

        for i in range(len(self.ilias_test_result5)):
            self.ilias_test_result5_settings += self.ilias_test_result5[i].split(";")

        for i in range(len(self.ilias_test_result6)):
            self.ilias_test_result6_settings += self.ilias_test_result6[i].split(";")

        for i in range(len(self.ilias_test_result7)):
            self.ilias_test_result7_settings += self.ilias_test_result7[i].split(";")

        for i in range(len(self.ilias_test_result8)):
            self.ilias_test_result8_settings += self.ilias_test_result8[i].split(";")

        for i in range(len(self.ilias_test_result9)):
            self.ilias_test_result9_settings += self.ilias_test_result9[i].split(";")

        for i in range(len(self.ilias_test_result10)):
            self.ilias_test_result10_settings += self.ilias_test_result10[i].split(";")

        # Lösche Fach 12 und danach jedes 13te Feld
        # Diese Felder enthalten keine Informationen. Der String schließt mit "unitvalue";s:0:"";} ab und die gelöschten Felder
        # enthalten den "Wert zwischen ; und } und sind unbrauchbar.
        del self.ilias_test_variable1_settings[12::13]
        del self.ilias_test_variable2_settings[12::13]
        del self.ilias_test_variable3_settings[12::13]
        del self.ilias_test_variable4_settings[12::13]
        del self.ilias_test_variable5_settings[12::13]
        del self.ilias_test_variable6_settings[12::13]
        del self.ilias_test_variable7_settings[12::13]
        del self.ilias_test_variable8_settings[12::13]
        del self.ilias_test_variable9_settings[12::13]
        del self.ilias_test_variable10_settings[12::13]

        # Erstes Feld löschen, dann enthält jedes 2. Fach der eigentliche Wert für die jeweilige Einstellung z.B. Präzision
        if len(self.ilias_test_variable1_settings) > 0:
            self.ilias_test_variable1_settings.pop(0)

        if len(self.ilias_test_variable2_settings) > 0:
            self.ilias_test_variable2_settings.pop(0)

        if len(self.ilias_test_variable3_settings) > 0:
            self.ilias_test_variable3_settings.pop(0)

        if len(self.ilias_test_variable4_settings) > 0:
            self.ilias_test_variable4_settings.pop(0)

        if len(self.ilias_test_variable5_settings) > 0:
            self.ilias_test_variable5_settings.pop(0)

        if len(self.ilias_test_variable6_settings) > 0:
            self.ilias_test_variable6_settings.pop(0)

        if len(self.ilias_test_variable7_settings) > 0:
            self.ilias_test_variable7_settings.pop(0)

        if len(self.ilias_test_variable8_settings) > 0:
            self.ilias_test_variable8_settings.pop(0)

        if len(self.ilias_test_variable9_settings) > 0:
            self.ilias_test_variable9_settings.pop(0)

        if len(self.ilias_test_variable10_settings) > 0:
            self.ilias_test_variable10_settings.pop(0)

        self.ilias_test_variable1_settings_2nd = self.ilias_test_variable1_settings[::2]
        self.ilias_test_variable2_settings_2nd = self.ilias_test_variable2_settings[::2]
        self.ilias_test_variable3_settings_2nd = self.ilias_test_variable3_settings[::2]
        self.ilias_test_variable4_settings_2nd = self.ilias_test_variable4_settings[::2]
        self.ilias_test_variable5_settings_2nd = self.ilias_test_variable5_settings[::2]
        self.ilias_test_variable6_settings_2nd = self.ilias_test_variable6_settings[::2]
        self.ilias_test_variable7_settings_2nd = self.ilias_test_variable7_settings[::2]
        self.ilias_test_variable8_settings_2nd = self.ilias_test_variable8_settings[::2]
        self.ilias_test_variable9_settings_2nd = self.ilias_test_variable9_settings[::2]
        self.ilias_test_variable10_settings_2nd = self.ilias_test_variable10_settings[::2]

        # for i in range(len(self.ilias_test_variable1_settings_2nd)):
        #   print("Fach " + str(i) + ": " + str(self.ilias_test_variable1_settings_2nd[i]))

        for i in range(0, len(self.ilias_test_variable1_settings_2nd), 6):
            self.ilias_test_variable1_prec.append(self.ilias_test_variable1_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable1_divby.append(self.ilias_test_variable1_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable1_min.append(self.ilias_test_variable1_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable1_max.append(self.ilias_test_variable1_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable2_settings_2nd), 6):
            self.ilias_test_variable2_prec.append(self.ilias_test_variable2_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable2_divby.append(self.ilias_test_variable2_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable2_min.append(self.ilias_test_variable2_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable2_max.append(self.ilias_test_variable2_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable3_settings_2nd), 6):
            self.ilias_test_variable3_prec.append(self.ilias_test_variable3_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable3_divby.append(self.ilias_test_variable3_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable3_min.append(self.ilias_test_variable3_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable3_max.append(self.ilias_test_variable3_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable4_settings_2nd), 6):
            self.ilias_test_variable4_prec.append(self.ilias_test_variable4_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable4_divby.append(self.ilias_test_variable4_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable4_min.append(self.ilias_test_variable4_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable4_max.append(self.ilias_test_variable4_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable5_settings_2nd), 6):
            self.ilias_test_variable5_prec.append(self.ilias_test_variable5_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable5_divby.append(self.ilias_test_variable5_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable5_min.append(self.ilias_test_variable5_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable5_max.append(self.ilias_test_variable5_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable5_settings_2nd), 6):
            self.ilias_test_variable5_prec.append(self.ilias_test_variable5_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable5_divby.append(self.ilias_test_variable5_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable5_min.append(self.ilias_test_variable5_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable5_max.append(self.ilias_test_variable5_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable6_settings_2nd), 6):
            self.ilias_test_variable6_prec.append(self.ilias_test_variable6_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable6_divby.append(self.ilias_test_variable6_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable6_min.append(self.ilias_test_variable6_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable6_max.append(self.ilias_test_variable6_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable7_settings_2nd), 6):
            self.ilias_test_variable7_prec.append(self.ilias_test_variable7_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable7_divby.append(self.ilias_test_variable7_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable7_min.append(self.ilias_test_variable7_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable7_max.append(self.ilias_test_variable7_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable8_settings_2nd), 6):
            self.ilias_test_variable8_prec.append(self.ilias_test_variable8_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable8_divby.append(self.ilias_test_variable8_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable8_min.append(self.ilias_test_variable8_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable8_max.append(self.ilias_test_variable8_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable9_settings_2nd), 6):
            self.ilias_test_variable9_prec.append(self.ilias_test_variable9_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable9_divby.append(self.ilias_test_variable9_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable9_min.append(self.ilias_test_variable9_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable9_max.append(self.ilias_test_variable9_settings_2nd[i + 3].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_variable10_settings_2nd), 6):
            self.ilias_test_variable10_prec.append(self.ilias_test_variable10_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_variable10_divby.append(self.ilias_test_variable10_settings_2nd[i + 1][5:][:-1])
            self.ilias_test_variable10_min.append(self.ilias_test_variable10_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_variable10_max.append(self.ilias_test_variable10_settings_2nd[i + 3].rsplit(':', 1)[-1])

        # print(len(self.ilias_test_variable1_prec), self.ilias_test_variable1_prec)
        # print(len(self.ilias_test_variable1_divby), self.ilias_test_variable1_divby)
        # print(len(self.ilias_test_variable1_min), self.ilias_test_variable1_min)
        # print(len(self.ilias_test_variable1_max), self.ilias_test_variable1_max)

        # print(len(self.ilias_test_variable2_prec), self.ilias_test_variable2_prec)
        # print(len(self.ilias_test_variable2_divby), self.ilias_test_variable2_divby)
        # print(len(self.ilias_test_variable2_min), self.ilias_test_variable2_min)
        # print(len(self.ilias_test_variable2_max), self.ilias_test_variable2_max)

        # Listen auffüllen. Liste "Fragentitel" enthält die max. Anzahl an Fragen

        for i in range(len(self.ilias_test_variable2_min), len(self.ilias_test_title)):
            self.ilias_test_variable2_prec.append(" ")
            self.ilias_test_variable2_divby.append(" ")
            self.ilias_test_variable2_min.append(" ")
            self.ilias_test_variable2_max.append(" ")

        for i in range(len(self.ilias_test_variable3_min), len(self.ilias_test_title)):
            self.ilias_test_variable3_prec.append(" ")
            self.ilias_test_variable3_divby.append(" ")
            self.ilias_test_variable3_min.append(" ")
            self.ilias_test_variable3_max.append(" ")

        for i in range(len(self.ilias_test_variable4_min), len(self.ilias_test_title)):
            self.ilias_test_variable4_prec.append(" ")
            self.ilias_test_variable4_divby.append(" ")
            self.ilias_test_variable4_min.append(" ")
            self.ilias_test_variable4_max.append(" ")

        for i in range(len(self.ilias_test_variable5_min), len(self.ilias_test_title)):
            self.ilias_test_variable5_prec.append(" ")
            self.ilias_test_variable5_divby.append(" ")
            self.ilias_test_variable5_min.append(" ")
            self.ilias_test_variable5_max.append(" ")

        for i in range(len(self.ilias_test_variable6_min), len(self.ilias_test_title)):
            self.ilias_test_variable6_prec.append(" ")
            self.ilias_test_variable6_divby.append(" ")
            self.ilias_test_variable6_min.append(" ")
            self.ilias_test_variable6_max.append(" ")

        for i in range(len(self.ilias_test_variable7_min), len(self.ilias_test_title)):
            self.ilias_test_variable7_prec.append(" ")
            self.ilias_test_variable7_divby.append(" ")
            self.ilias_test_variable7_min.append(" ")
            self.ilias_test_variable7_max.append(" ")

        for i in range(len(self.ilias_test_variable8_min), len(self.ilias_test_title)):
            self.ilias_test_variable8_prec.append(" ")
            self.ilias_test_variable8_divby.append(" ")
            self.ilias_test_variable8_min.append(" ")
            self.ilias_test_variable8_max.append(" ")

        for i in range(len(self.ilias_test_variable9_min), len(self.ilias_test_title)):
            self.ilias_test_variable9_prec.append(" ")
            self.ilias_test_variable9_divby.append(" ")
            self.ilias_test_variable9_min.append(" ")
            self.ilias_test_variable9_max.append(" ")

        for i in range(len(self.ilias_test_variable10_min), len(self.ilias_test_title)):
            self.ilias_test_variable10_prec.append(" ")
            self.ilias_test_variable10_divby.append(" ")
            self.ilias_test_variable10_min.append(" ")
            self.ilias_test_variable10_max.append(" ")

        # print(len(self.ilias_test_variable3_prec), self.ilias_test_variable3_prec)
        # print(len(self.ilias_test_variable3_divby), self.ilias_test_variable3_divby)
        # print(len(self.ilias_test_variable3_min), self.ilias_test_variable3_min)
        # print(len(self.ilias_test_variable3_max), self.ilias_test_variable3_max)

        # print(len(self.ilias_test_variable4_prec), self.ilias_test_variable4_prec)
        # print(len(self.ilias_test_variable4_divby), self.ilias_test_variable4_divby)
        # print(len(self.ilias_test_variable4_min), self.ilias_test_variable4_min)
        # print(len(self.ilias_test_variable4_max), self.ilias_test_variable4_max)

        # print(len(self.ilias_test_variable5_prec), self.ilias_test_variable5_prec)
        # print(len(self.ilias_test_variable5_divby), self.ilias_test_variable5_divby)
        # print(len(self.ilias_test_variable5_min), self.ilias_test_variable5_min)
        # print(len(self.ilias_test_variable5_max), self.ilias_test_variable5_max)

        # print("######################")
        # print(self.ilias_test_variable1[0])
        # print("LÄNGE: " + str(len(self.ilias_test_variable1)))
        # print(self.ilias_test_variable1_settings[0])
        # print("LÄNGE: " +str(len(self.ilias_test_variable1_settings)))
        # print(self.ilias_test_variable1_settings_2nd[0])
        # print("LÄNGE: " + str(len(self.ilias_test_variable1_settings_2nd)))
        # print("#######################")

        # Ergebnis String auslesen

        print("Länge der Settings")
        print(self.ilias_test_result1_settings)
        print(self.ilias_test_result2_settings)
        print(self.ilias_test_result3_settings)
        print(self.ilias_test_result4_settings)
        print(self.ilias_test_result5_settings)
        print(self.ilias_test_result6_settings)
        print(self.ilias_test_result7_settings)
        print(self.ilias_test_result8_settings)
        print(self.ilias_test_result9_settings)
        print(self.ilias_test_result10_settings)

        if len(self.ilias_test_result1_settings) > 0:
            self.ilias_test_result1_settings.pop(0)

        if len(self.ilias_test_result2_settings) > 0:
            self.ilias_test_result2_settings.pop(0)

        if len(self.ilias_test_result3_settings) > 0:
            self.ilias_test_result3_settings.pop(0)

        if len(self.ilias_test_result4_settings) > 0:
            self.ilias_test_result4_settings.pop(0)

        if len(self.ilias_test_result5_settings) > 0:
            self.ilias_test_result5_settings.pop(0)

        if len(self.ilias_test_result6_settings) > 0:
            self.ilias_test_result6_settings.pop(0)

        if len(self.ilias_test_result7_settings) > 0:
            self.ilias_test_result7_settings.pop(0)

        if len(self.ilias_test_result8_settings) > 0:
            self.ilias_test_result8_settings.pop(0)

        if len(self.ilias_test_result9_settings) > 0:
            self.ilias_test_result9_settings.pop(0)

        if len(self.ilias_test_result10_settings) > 0:
            self.ilias_test_result10_settings.pop(0)

        self.ilias_test_result1_settings_2nd = self.ilias_test_result1_settings[::2]
        self.ilias_test_result2_settings_2nd = self.ilias_test_result2_settings[::2]
        self.ilias_test_result3_settings_2nd = self.ilias_test_result3_settings[::2]
        self.ilias_test_result4_settings_2nd = self.ilias_test_result4_settings[::2]
        self.ilias_test_result5_settings_2nd = self.ilias_test_result5_settings[::2]
        self.ilias_test_result6_settings_2nd = self.ilias_test_result6_settings[::2]
        self.ilias_test_result7_settings_2nd = self.ilias_test_result7_settings[::2]
        self.ilias_test_result8_settings_2nd = self.ilias_test_result8_settings[::2]
        self.ilias_test_result9_settings_2nd = self.ilias_test_result9_settings[::2]

        for i in range(len(self.ilias_test_result1_settings_2nd)):
            self.ilias_test_result1_settings_2nd[i] = self.ilias_test_result1_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result2_settings_2nd)):
            self.ilias_test_result2_settings_2nd[i] = self.ilias_test_result2_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result3_settings_2nd)):
            self.ilias_test_result3_settings_2nd[i] = self.ilias_test_result3_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result4_settings_2nd)):
            self.ilias_test_result4_settings_2nd[i] = self.ilias_test_result4_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result5_settings_2nd)):
            self.ilias_test_result5_settings_2nd[i] = self.ilias_test_result5_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result6_settings_2nd)):
            self.ilias_test_result6_settings_2nd[i] = self.ilias_test_result6_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result7_settings_2nd)):
            self.ilias_test_result7_settings_2nd[i] = self.ilias_test_result7_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result8_settings_2nd)):
            self.ilias_test_result8_settings_2nd[i] = self.ilias_test_result8_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result9_settings_2nd)):
            self.ilias_test_result9_settings_2nd[i] = self.ilias_test_result9_settings_2nd[i].replace('"', '')

        for i in range(len(self.ilias_test_result10_settings_2nd)):
            self.ilias_test_result10_settings_2nd[i] = self.ilias_test_result10_settings_2nd[i].replace('"', '')

        for i in range(0, len(self.ilias_test_result1_settings_2nd), 10):
            self.ilias_test_result1_prec.append(self.ilias_test_result1_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result1_tol.append(self.ilias_test_result1_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result1_min.append(self.ilias_test_result1_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result1_max.append(self.ilias_test_result1_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result1_pts.append(self.ilias_test_result1_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result1_formula.append(self.ilias_test_result1_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result2_settings_2nd), 10):
            self.ilias_test_result2_prec.append(self.ilias_test_result2_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result2_tol.append(self.ilias_test_result2_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result2_min.append(self.ilias_test_result2_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result2_max.append(self.ilias_test_result2_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result2_pts.append(self.ilias_test_result2_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result2_formula.append(self.ilias_test_result2_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result3_settings_2nd), 10):
            self.ilias_test_result3_prec.append(self.ilias_test_result3_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result3_tol.append(self.ilias_test_result3_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result3_min.append(self.ilias_test_result3_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result3_max.append(self.ilias_test_result3_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result3_pts.append(self.ilias_test_result3_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result3_formula.append(self.ilias_test_result3_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result4_settings_2nd), 10):
            self.ilias_test_result4_prec.append(self.ilias_test_result4_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result4_tol.append(self.ilias_test_result4_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result4_min.append(self.ilias_test_result4_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result4_max.append(self.ilias_test_result4_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result4_pts.append(self.ilias_test_result4_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result4_formula.append(self.ilias_test_result4_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result5_settings_2nd), 10):
            self.ilias_test_result5_prec.append(self.ilias_test_result5_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result5_tol.append(self.ilias_test_result5_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result5_min.append(self.ilias_test_result5_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result5_max.append(self.ilias_test_result5_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result5_pts.append(self.ilias_test_result5_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result5_formula.append(self.ilias_test_result5_settings_2nd[i + 5].rsplit(':', 1)[-1])

        print("####### 5er #############")
        print(self.ilias_test_result5_formula)
        print("#####################")

        for i in range(0, len(self.ilias_test_result6_settings_2nd), 10):
            self.ilias_test_result6_prec.append(self.ilias_test_result6_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result6_tol.append(self.ilias_test_result6_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result6_min.append(self.ilias_test_result6_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result6_max.append(self.ilias_test_result6_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result6_pts.append(self.ilias_test_result6_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result6_formula.append(self.ilias_test_result6_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result7_settings_2nd), 10):
            self.ilias_test_result7_prec.append(self.ilias_test_result7_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result7_tol.append(self.ilias_test_result7_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result7_min.append(self.ilias_test_result7_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result7_max.append(self.ilias_test_result7_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result7_pts.append(self.ilias_test_result7_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result7_formula.append(self.ilias_test_result7_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result8_settings_2nd), 10):
            self.ilias_test_result8_prec.append(self.ilias_test_result8_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result8_tol.append(self.ilias_test_result8_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result8_min.append(self.ilias_test_result8_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result8_max.append(self.ilias_test_result8_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result8_pts.append(self.ilias_test_result8_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result8_formula.append(self.ilias_test_result8_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result9_settings_2nd), 10):
            self.ilias_test_result9_prec.append(self.ilias_test_result9_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result9_tol.append(self.ilias_test_result9_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result9_min.append(self.ilias_test_result9_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result9_max.append(self.ilias_test_result9_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result9_pts.append(self.ilias_test_result9_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result9_formula.append(self.ilias_test_result9_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(0, len(self.ilias_test_result10_settings_2nd), 10):
            self.ilias_test_result10_prec.append(self.ilias_test_result10_settings_2nd[i].rsplit(':', 1)[-1])
            self.ilias_test_result10_tol.append(self.ilias_test_result10_settings_2nd[i + 1].rsplit(':', 1)[-1])
            self.ilias_test_result10_min.append(self.ilias_test_result10_settings_2nd[i + 2].rsplit(':', 1)[-1])
            self.ilias_test_result10_max.append(self.ilias_test_result10_settings_2nd[i + 3].rsplit(':', 1)[-1])
            self.ilias_test_result10_pts.append(self.ilias_test_result10_settings_2nd[i + 4].rsplit(':', 1)[-1])
            self.ilias_test_result10_formula.append(self.ilias_test_result10_settings_2nd[i + 5].rsplit(':', 1)[-1])

        for i in range(len(self.ilias_test_result2_min), len(self.ilias_test_title)):
            self.ilias_test_result2_min.append(" ")
            self.ilias_test_result2_max.append(" ")
            self.ilias_test_result2_prec.append(" ")
            self.ilias_test_result2_tol.append(" ")
            self.ilias_test_result2_pts.append(" ")
            self.ilias_test_result2_formula.append(" ")

        for i in range(len(self.ilias_test_result3_min), len(self.ilias_test_title)):
            self.ilias_test_result3_min.append(" ")
            self.ilias_test_result3_max.append(" ")
            self.ilias_test_result3_prec.append(" ")
            self.ilias_test_result3_tol.append(" ")
            self.ilias_test_result3_pts.append(" ")
            self.ilias_test_result3_formula.append(" ")

        for i in range(len(self.ilias_test_result4_min), len(self.ilias_test_title)):
            self.ilias_test_result4_min.append(" ")
            self.ilias_test_result4_max.append(" ")
            self.ilias_test_result4_prec.append(" ")
            self.ilias_test_result4_tol.append(" ")
            self.ilias_test_result4_pts.append(" ")
            self.ilias_test_result4_formula.append(" ")

        for i in range(len(self.ilias_test_result5_min), len(self.ilias_test_title)):
            self.ilias_test_result5_min.append(" ")
            self.ilias_test_result5_max.append(" ")
            self.ilias_test_result5_prec.append(" ")
            self.ilias_test_result5_tol.append(" ")
            self.ilias_test_result5_pts.append(" ")
            self.ilias_test_result5_formula.append(" ")

        for i in range(len(self.ilias_test_result6_min), len(self.ilias_test_title)):
            self.ilias_test_result6_min.append(" ")
            self.ilias_test_result6_max.append(" ")
            self.ilias_test_result6_prec.append(" ")
            self.ilias_test_result6_tol.append(" ")
            self.ilias_test_result6_pts.append(" ")
            self.ilias_test_result6_formula.append(" ")

        for i in range(len(self.ilias_test_result7_min), len(self.ilias_test_title)):
            self.ilias_test_result7_min.append(" ")
            self.ilias_test_result7_max.append(" ")
            self.ilias_test_result7_prec.append(" ")
            self.ilias_test_result7_tol.append(" ")
            self.ilias_test_result7_pts.append(" ")
            self.ilias_test_result7_formula.append(" ")

        for i in range(len(self.ilias_test_result8_min), len(self.ilias_test_title)):
            self.ilias_test_result8_min.append(" ")
            self.ilias_test_result8_max.append(" ")
            self.ilias_test_result8_prec.append(" ")
            self.ilias_test_result8_tol.append(" ")
            self.ilias_test_result8_pts.append(" ")
            self.ilias_test_result8_formula.append(" ")

        for i in range(len(self.ilias_test_result9_min), len(self.ilias_test_title)):
            self.ilias_test_result9_min.append(" ")
            self.ilias_test_result9_max.append(" ")
            self.ilias_test_result9_prec.append(" ")
            self.ilias_test_result9_tol.append(" ")
            self.ilias_test_result9_pts.append(" ")
            self.ilias_test_result9_formula.append(" ")

        for i in range(len(self.ilias_test_result10_min), len(self.ilias_test_title)):
            self.ilias_test_result10_min.append(" ")
            self.ilias_test_result10_max.append(" ")
            self.ilias_test_result10_prec.append(" ")
            self.ilias_test_result10_tol.append(" ")
            self.ilias_test_result10_pts.append(" ")
            self.ilias_test_result10_formula.append(" ")

        print(len(self.ilias_test_result1_formula), len(self.ilias_test_result2_formula),
              len(self.ilias_test_result3_formula), len(self.ilias_test_result4_formula),
              len(self.ilias_test_result5_formula), len(self.ilias_test_result6_formula),
              len(self.ilias_test_result7_formula), len(self.ilias_test_result8_formula),
              len(self.ilias_test_result9_formula), len(self.ilias_test_result10_formula))
        print(self.ilias_test_result1_formula)
        print(self.ilias_test_result2_formula)
        print(self.ilias_test_result3_formula)
        print(self.ilias_test_result4_formula)
        print(self.ilias_test_result5_formula)
        print(self.ilias_test_result6_formula)
        print(self.ilias_test_result7_formula)
        print(self.ilias_test_result8_formula)
        print(self.ilias_test_result9_formula)
        print(self.ilias_test_result10_formula)

        print()

        for i in range(len(self.ilias_test_question_description_image_uri)):
            if self.ilias_test_question_description_image_uri[i] != "EMPTY":
                self.ilias_test_question_description_image_uri[i] = os.path.normpath(
                    os.path.join(self.select_test_import_file, self.ilias_test_question_description_image_uri[i]))

        # Daten in die SQL-Datenbank einfügen
        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
        c = conn.cursor()
        conn.commit()

        for i in range(len(self.ilias_test_title)):

            # if self.ilias_test_question_description_image_name[i] == "":
            #    self.ilias_test_question_description_image_name[i] = "EMTPY"

            if self.ilias_test_question_description_image_uri[i] != "EMPTY":
                with open(self.ilias_test_question_description_image_uri[i], 'rb') as image_file:
                    self.image_data = image_file.read()
            else:
                self.image_data = "EMPTY"

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
                    'question_difficulty': "",
                    'question_category': "",
                    'question_type': "Formelfrage",
                    'question_title': self.ilias_test_title[i],
                    'question_description_title': self.ilias_test_question_description_title[i],
                    'question_description_main': self.test_list1_l_join[i],

                    'res1_formula': self.ilias_test_result1_formula[i],
                    'res2_formula': self.ilias_test_result2_formula[i],
                    'res3_formula': self.ilias_test_result3_formula[i],
                    'res4_formula': self.ilias_test_result4_formula[i],
                    'res5_formula': self.ilias_test_result5_formula[i],
                    'res6_formula': self.ilias_test_result6_formula[i],
                    'res7_formula': self.ilias_test_result7_formula[i],
                    'res8_formula': self.ilias_test_result8_formula[i],
                    'res9_formula': self.ilias_test_result9_formula[i],
                    'res10_formula': self.ilias_test_result10_formula[i],

                    'var1_name': "",
                    'var1_min': self.ilias_test_variable1_min[i],
                    'var1_max': self.ilias_test_variable1_max[i],
                    'var1_prec': self.ilias_test_variable1_prec[i],
                    'var1_divby': self.ilias_test_variable1_divby[i],
                    'var1_unit': "",

                    'var2_name': "",
                    'var2_min': self.ilias_test_variable2_min[i],
                    'var2_max': self.ilias_test_variable2_max[i],
                    'var2_prec': self.ilias_test_variable2_prec[i],
                    'var2_divby': self.ilias_test_variable2_divby[i],
                    'var2_unit': "",

                    'var3_name': "",
                    'var3_min': self.ilias_test_variable3_min[i],
                    'var3_max': self.ilias_test_variable3_max[i],
                    'var3_prec': self.ilias_test_variable3_prec[i],
                    'var3_divby': self.ilias_test_variable3_divby[i],
                    'var3_unit': "",

                    'var4_name': "",
                    'var4_min': self.ilias_test_variable4_min[i],
                    'var4_max': self.ilias_test_variable4_max[i],
                    'var4_prec': self.ilias_test_variable4_prec[i],
                    'var4_divby': self.ilias_test_variable4_divby[i],
                    'var4_unit': "",

                    'var5_name': "",
                    'var5_min': self.ilias_test_variable5_min[i],
                    'var5_max': self.ilias_test_variable5_max[i],
                    'var5_prec': self.ilias_test_variable5_prec[i],
                    'var5_divby': self.ilias_test_variable5_divby[i],
                    'var5_unit': "",

                    'var6_name': "",
                    'var6_min': self.ilias_test_variable6_min[i],
                    'var6_max': self.ilias_test_variable6_max[i],
                    'var6_prec': self.ilias_test_variable6_prec[i],
                    'var6_divby': self.ilias_test_variable6_divby[i],
                    'var6_unit': "",

                    'var7_name': "",
                    'var7_min': self.ilias_test_variable7_min[i],
                    'var7_max': self.ilias_test_variable7_max[i],
                    'var7_prec': self.ilias_test_variable7_prec[i],
                    'var7_divby': self.ilias_test_variable7_divby[i],
                    'var7_unit': "",

                    'var8_name': "",
                    'var8_min': self.ilias_test_variable8_min[i],
                    'var8_max': self.ilias_test_variable8_max[i],
                    'var8_prec': self.ilias_test_variable8_prec[i],
                    'var8_divby': self.ilias_test_variable8_divby[i],
                    'var8_unit': "",

                    'var9_name': "",
                    'var9_min': self.ilias_test_variable9_min[i],
                    'var9_max': self.ilias_test_variable9_max[i],
                    'var9_prec': self.ilias_test_variable9_prec[i],
                    'var9_divby': self.ilias_test_variable9_divby[i],
                    'var9_unit': "",

                    'var10_name': "",
                    'var10_min': self.ilias_test_variable10_min[i],
                    'var10_max': self.ilias_test_variable10_max[i],
                    'var10_prec': self.ilias_test_variable10_prec[i],
                    'var10_divby': self.ilias_test_variable10_divby[i],
                    'var10_unit': "",

                    'res1_name': "",
                    'res1_min': self.ilias_test_result1_min[i],
                    'res1_max': self.ilias_test_result1_max[i],
                    'res1_prec': self.ilias_test_result1_prec[i],
                    'res1_tol': self.ilias_test_result1_tol[i],
                    'res1_points': self.ilias_test_result1_pts[i],
                    'res1_unit': "",

                    'res2_name': "",
                    'res2_min': self.ilias_test_result2_min[i],
                    'res2_max': self.ilias_test_result2_max[i],
                    'res2_prec': self.ilias_test_result2_prec[i],
                    'res2_tol': self.ilias_test_result2_tol[i],
                    'res2_points': self.ilias_test_result2_pts[i],
                    'res2_unit': "",

                    'res3_name': "",
                    'res3_min': self.ilias_test_result3_min[i],
                    'res3_max': self.ilias_test_result3_max[i],
                    'res3_prec': self.ilias_test_result3_prec[i],
                    'res3_tol': self.ilias_test_result3_tol[i],
                    'res3_points': self.ilias_test_result3_pts[i],
                    'res3_unit': "",

                    'res4_name': "",
                    'res4_min': self.ilias_test_result4_min[i],
                    'res4_max': self.ilias_test_result4_max[i],
                    'res4_prec': self.ilias_test_result4_prec[i],
                    'res4_tol': self.ilias_test_result4_tol[i],
                    'res4_points': self.ilias_test_result4_pts[i],
                    'res4_unit': "",

                    'res5_name': "",
                    'res5_min': self.ilias_test_result5_min[i],
                    'res5_max': self.ilias_test_result5_max[i],
                    'res5_prec': self.ilias_test_result5_prec[i],
                    'res5_tol': self.ilias_test_result5_tol[i],
                    'res5_points': self.ilias_test_result5_pts[i],
                    'res5_unit': "",

                    'res6_name': "",
                    'res6_min': self.ilias_test_result6_min[i],
                    'res6_max': self.ilias_test_result6_max[i],
                    'res6_prec': self.ilias_test_result6_prec[i],
                    'res6_tol': self.ilias_test_result6_tol[i],
                    'res6_points': self.ilias_test_result6_pts[i],
                    'res6_unit': "",

                    'res7_name': "",
                    'res7_min': self.ilias_test_result7_min[i],
                    'res7_max': self.ilias_test_result7_max[i],
                    'res7_prec': self.ilias_test_result7_prec[i],
                    'res7_tol': self.ilias_test_result7_tol[i],
                    'res7_points': self.ilias_test_result7_pts[i],
                    'res7_unit': "",

                    'res8_name': "",
                    'res8_min': self.ilias_test_result8_min[i],
                    'res8_max': self.ilias_test_result8_max[i],
                    'res8_prec': self.ilias_test_result8_prec[i],
                    'res8_tol': self.ilias_test_result8_tol[i],
                    'res8_points': self.ilias_test_result8_pts[i],
                    'res8_unit': "",

                    'res9_name': "",
                    'res9_min': self.ilias_test_result9_min[i],
                    'res9_max': self.ilias_test_result9_max[i],
                    'res9_prec': self.ilias_test_result9_prec[i],
                    'res9_tol': self.ilias_test_result9_tol[i],
                    'res9_points': self.ilias_test_result9_pts[i],
                    'res9_unit': "",

                    'res10_name': "",
                    'res10_min': self.ilias_test_result10_min[i],
                    'res10_max': self.ilias_test_result10_max[i],
                    'res10_prec': self.ilias_test_result10_prec[i],
                    'res10_tol': self.ilias_test_result10_tol[i],
                    'res10_points': self.ilias_test_result10_pts[i],
                    'res10_unit': "",

                    'img_name': self.ilias_test_question_description_image_name[i],
                    'img_data': self.image_data,

                    'test_time': self.ilias_test_duration[i],
                    'var_number': "",
                    'res_number': "",
                    'question_pool_tag': ""
                }
            )
        conn.commit()
        conn.close()

        print("Test importiert!")






class Create_formelfrage_pool(Formelfrage):

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


        #Pfad anpassungen - Die ID muss um +1 erhöht werden, wenn "Fragenpool erstellen" betätigt wird
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

        # Alle Fragen aus der DB in Pool-XML schreiben

        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()

        for record in records:
            self.my_list.append(int(record[len(record) - 1]))

        self.my_string = ','.join(map(str, self.my_list))
        self.entry_split = self.my_string.split(",")


        # Einzelne Fragen aus der DB in Pool-XML schreiben
        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
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

                        Create_formelfrage_pool.create_question_pool(self, x)  #

                        print("Formelfrage generated with Title --> \"" + self.question_title + "\"" + " mit pool tag: " + str(record[151]))   #Question_pool_tag

                        self.question_title_list.append(self.question_title)
                        self.question_pool_id_list.append(str(record[151]))


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


        self.question_title_to_item_id_dict = dict(zip(self.item_title_list, self.item_id_list))

        for i in range(len(self.item_title_list)):
            self.item_pool_no_dublicates.append(self.question_title_to_pool_id_dict.get(self.item_title_list[i]))


        self.item_pool_no_dublicates = list(dict.fromkeys(self.item_pool_no_dublicates))


        # Knoten schreiben
        for i in range(len(self.item_pool_no_dublicates)):

            ### Taxonomie Datei schreiben: self, Pfad zur Datei, new_node_id, parent_node_id    parent_node auf "EMTPY" gesetzt, da nur 1 Ebene in der Taxonomie exisitieren soll
            Formelfrage.add_node_to_tax_from_excel(self, self.taxonomy_file_question_pool, self.item_pool_no_dublicates[i], "EMPTY")

        # Fragen zu Knoten hinzufügen
        for i in range(len(self.item_title_list)):
            # FUnktion starten mit: self, Pfad zur Datei, Item_ID, Item_Pool
            Formelfrage.assign_questions_to_node_from_excel(self, self.taxonomy_file_question_pool, self.question_title_to_item_id_dict.get(self.item_title_list[i]), self.question_title_to_pool_id_dict.get(self.item_title_list[i])  )



        # Taxonomie-Datei neu sortieren
        Formelfrage.tax_reallocate_from_excel(self, self.taxonomy_file_question_pool)



        for i in range(len(self.entry_split)):
            Create_formelfrage_pool.create_question_pool_qpl(self, i)


        ######  Anpassung der Datei "qpl". Akualisierung des Dateinamens
        self.qpl_file = os.path.normpath(os.path.join(self.project_root_path, "ILIAS-Fragenpool_qpl_Daten",  self.ilias_id_pool_qpl, self.ilias_id_pool_qpl_xml))

        self.mytree = ET.parse(self.qpl_file)
        self.myroot = self.mytree.getroot()

        for ident_id in self.myroot.iter('Identifier'):
            ident_id.set('Entry', "il_0_qpl_" + str(max(self.filename_id)+1))
        self.mytree.write(self.qpl_file)

        print("Erstelle Ordner mit ID: 1596569820__0__qpl_" + str(max(self.filename_id) + 1) + "...")
        print("ID Anpassung interner Dateien.. DONE")


        self.filename_id.append(int(max(self.filename_id)+1))

        app.destroy()
        print("\n")
        print("Vorgang abgeschlossen")





    def create_question_pool(self, x):



        conn = sqlite3.connect('ILIAS-Fragen_temp_db.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM my_table")

        records = c.fetchall()



        def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Error: Creating directory. ' + directory)



        createFolder(self.img_file_path_create_folder_pool + '/' + 'il_0_mob_000000' + str(x) + '/')

        for record in records:

            #Ohne If Abfrage werden ALLE Fragen aus der Datenbank erstellt
            if str(record[len(record)-1]) == self.entry_split[x]:


                if self.img_data_raw != "EMPTY":
                    #img wird immer als PNG Datei abgelegt.

                    with open(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png", 'wb') as image_file:
                        image_file.write(self.img_data_raw)

                    self.image = Image.open(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")
                    self.image.save(self.img_file_path_create_folder_pool + "\\il_0_mob_000000" + str(x) + "\\" + self.img_name + ".png")







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
                self.autor_replaced = str(" ")
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
        Create_formelfrage_pool.replace_characters_pool(self)


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


app = Tk()
GUI = GuiMainWindow(app)
app.mainloop()


