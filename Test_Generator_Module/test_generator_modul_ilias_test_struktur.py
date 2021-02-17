import xml.etree.ElementTree as ET
import os
import shutil
from PIL import Image
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image          # Zur Preview von ausgewählten Bildern
import pathlib

# Eigene Module
from Test_Generator_Module import test_generator_modul_formelfrage
from Test_Generator_Module import test_generator_modul_singlechoice
from Test_Generator_Module import test_generator_modul_multiplechoice
from Test_Generator_Module import test_generator_modul_zuordnungsfrage
from Test_Generator_Module import test_generator_modul_formelfrage_permutation
from Test_Generator_Module import test_generator_modul_taxonomie_und_textformatierung


class Create_ILIAS_Test:
    def __init__(self,
                 entry_to_index_dict,
                 test_tst_file_path_template,
                 test_tst_file_path_output,
                 test_qti_file_path_template,
                 test_qti_file_path_output,
                 ilias_test_title_entry,
                 create_test_entry_ids,
                 question_type):

        # VARIABLEN UND PFADE FÜR ILIAS_TEST
        self.test_tst_file_path_template = test_tst_file_path_template
        self.test_tst_file_path_output = test_tst_file_path_output
        self.test_qti_file_path_template = test_qti_file_path_template
        self.test_qti_file_path_output = test_qti_file_path_output

        self.ilias_test_title_entry = ilias_test_title_entry
        self.create_test_entry_ids = create_test_entry_ids
        self.question_type = question_type


        self.db_entry_to_index_dict = entry_to_index_dict


        # Einlesen der "Formelfrage" _tst_.xml zum ändern des Test-Titel
        self.mytree = ET.parse(self.test_tst_file_path_template)
        self.myroot = self.mytree.getroot()

        # Aufruf -> Pool erstellen
        Create_ILIAS_Test.test_structure(self)

    def test_structure(self):

        # Titel-Eintrag ändern (Voreinstellung in der Vorlage: Titel = ff_test_vorlage)
        for ContentObject in self.myroot.iter('ContentObject'):
            for MetaData in ContentObject.iter('MetaData'):
                for General in MetaData.iter('General'):
                    for Title in General.iter('Title'):
                        Title.text = self.ilias_test_title_entry
                        # .XML Datei kann keine "&" verarbeiten.
                        # "&" muss gegen "&amp" ausgetauscht werden sonst kann Ilias die Datei hinterher nicht verwerten.
                        Title.text = Title.text.replace('&', "&amp;")





            # Sollte kein Namen vergeben werden, wird der Test-Titel auf "DEFAULT" gesetzt
            if Title.text == "ff_test_vorlage" or Title.text == "":
                Title.text = "DEFAULT"

            # Änderungen der .XML in eine neue Datei schreiben
            # Die Datei wird nach dem ILIAS-Import "Standard" benannt "1604407426__0__tst_2040314.xml"
            # Die Ziffernfolge der 10 Ziffern am Anfang sowie der 7 Ziffern zum Schluss können nach belieben variiert werden.
            self.mytree.write(self.test_tst_file_path_output)


            print("TST FILE aktualisiert!")
            print(self.test_tst_file_path_output)

        # Aufruf: Modul -> Formelfrage -> Test
        if self.question_type.lower() == "formelfrage" or self.question_type.lower() == "formel frage":
            test_generator_modul_formelfrage.Create_Formelfrage_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_test_entry_ids,
                                                                                   "question_test",
                                                                                   "ilias_id_pool_img_dir_not_used_for_ilias_test",
                                                                                   "ilias_id_pool_qpl_dir_not_used_for_ilias_test",
                                                                                   self.test_qti_file_path_template,
                                                                                   self.test_qti_file_path_output,
                                                                                   "ilias_pool_qpl_file_path_output_not_used_for_ilias_test",
                                                                                   "ilias_pool_qti_not_used_for_ilias_test",
                                                                                   "file_max_id_not_used_for_ilias_test",
                                                                                   "taxonomy_not_used_for_ilias_test"
                                                                                   )


        # Aufruf: Modul -> SingleChoice -> Test
        elif self.question_type.lower() == "singlechoice" or self.question_type.lower() == "single choice":
            test_generator_modul_singlechoice.Create_SingleChoice_Questions.__init__(self,
                                                                                     self.db_entry_to_index_dict,
                                                                                     self.create_test_entry_ids,
                                                                                     "question_test",
                                                                                     "ilias_id_pool_img_dir_not_used_for_ilias_test",
                                                                                     "ilias_id_pool_qpl_dir_not_used_for_ilias_test",
                                                                                     self.test_qti_file_path_template,
                                                                                     self.test_qti_file_path_output,
                                                                                     "ilias_pool_qpl_file_path_output_not_used_for_ilias_test",
                                                                                     "ilias_pool_qti_not_used_for_ilias_test",
                                                                                     "file_max_id_not_used_for_ilias_test",
                                                                                     "taxonomy_not_used_for_ilias_test"
                                                                                     )

        # Aufruf: Modul -> MultipleChoice -> Test
        elif self.question_type.lower() == "multiplechoice" or self.question_type.lower() == "multiple choice":
            test_generator_modul_multiplechoice.Create_MultipleChoice_Questions.__init__(self,
                                                                                         self.db_entry_to_index_dict,
                                                                                         self.create_test_entry_ids,
                                                                                         "question_test",
                                                                                         "ilias_id_pool_img_dir_not_used_for_ilias_test",
                                                                                         "ilias_id_pool_qpl_dir_not_used_for_ilias_test",
                                                                                         self.test_qti_file_path_template,
                                                                                         self.test_qti_file_path_output,
                                                                                         "ilias_pool_qpl_file_path_output_not_used_for_ilias_test",
                                                                                         "ilias_pool_qti_not_used_for_ilias_test",
                                                                                         "file_max_id_not_used_for_ilias_test",
                                                                                         "taxonomy_not_used_for_ilias_test"
                                                                                         )

        # Aufruf: Modul -> Zuordnungsfrage -> Test
        elif self.question_type.lower() == "zuordnungsfrage" or self.question_type.lower() == "zuordnungs frage":
            test_generator_modul_zuordnungsfrage.Create_Zuordnungsfrage_Questions.__init__(self,
                                                                                         self.db_entry_to_index_dict,
                                                                                         self.create_test_entry_ids,
                                                                                         "question_test",
                                                                                         "ilias_id_pool_img_dir_not_used_for_ilias_test",
                                                                                         "ilias_id_pool_qpl_dir_not_used_for_ilias_test",
                                                                                         self.test_qti_file_path_template,
                                                                                         self.test_qti_file_path_output,
                                                                                         "ilias_pool_qpl_file_path_output_not_used_for_ilias_test",
                                                                                         "ilias_pool_qti_not_used_for_ilias_test",
                                                                                         "file_max_id_not_used_for_ilias_test",
                                                                                         "taxonomy_not_used_for_ilias_test"
                                                                                         )

        # Fragentyp wird nicht unterstützt
        else:
            print("Fragen-Typ ist NICHT \"formelfrage\", \"singlechoice\", \"multiplechoice\" oder \"zuordnungsfrage\"")


        # Anschließend werden die "&amp;" in der XML wieder gegen "&" getauscht
        Additional_Funtions.replace_character_in_xml_file(self, self.test_qti_file_path_output)





class Create_ILIAS_Pool:
    def __init__(self,
                 project_root_path,
                 pool_directory_output,
                 question_type_files_path_pool_output,
                 pool_qti_file_path_template,
                 ilias_test_title_entry,
                 create_pool_entry_ids,
                 question_type,
                 database_db_name,
                 database_table_name,
                 entry_to_index_dict,
                 var_create_all_questions):

        # VARIABLEN UND PFADE FÜR ILIAS_TEST

        # Projekt-Pfad
        self.project_root_path = project_root_path

        # Datei-Ausgabe Pfad für Fragen_Typ spezifische Dateien, z.B: (self.project_root_path, "Formelfrage", "ff_ilias_pool_abgabe"))
        self.question_type_files_path_pool_output = question_type_files_path_pool_output

        # Ordner-Pfad für die Dateien (Fragen-Typ spezifisch), z.B.: "self.formelfrage_files_path, "ff_ilias_pool_abgabe""
        self.pool_directory_output = pool_directory_output

        # Vorlagen Pfade
        self.pool_qti_file_path_template = pool_qti_file_path_template

        # Wert aus Eingabefeldern nehmen: "Test-Titel", "IDs", "Fragen-Typ"
        self.ilias_test_title_entry = ilias_test_title_entry
        self.create_pool_entry_ids = create_pool_entry_ids
        self.question_type = question_type.lower()

        # Falls sich keine *.zip Ordner in der "ilias_pool_abgabe" befinden, wird die ID über eine Vorlage (fest hinterlegt) bestimmt.
        # Die Zahl muss 7-stellig sein!
        self.pool_id_file_zip_template = ""

        if self.question_type == "formelfrage" or self.question_type == "formel frage":
            self.pool_id_file_zip_template = "1115532"
        if self.question_type == "singlechoice" or self.question_type == "single choice":
            self.pool_id_file_zip_template = "2225532"
        if self.question_type == "multiplechoice" or self.question_type == "multiple choice":
            self.pool_id_file_zip_template = "3335532"
        if self.question_type == "zuordnungsfrage" or self.question_type == "zordnungs frage":
            self.pool_id_file_zip_template = "4445532"
        if self.question_type == "formelfrage_perm" or self.question_type == "formelfrage_permutation":
            self.pool_id_file_zip_template = "9995532"



        # Dictionary
        self.db_entry_to_index_dict = entry_to_index_dict

        # Namen der Datenbank und Table_Name
        self.database_db_name = database_db_name
        self.database_table_name = database_table_name

        # Checkbox - Alle Fragen erstellen?
        self.var_create_question_pool_all = var_create_all_questions

        ######################## Alle Dateien im Ordner Pool-output auslesen und neuen Ordner erstellen, mit aufsteigender ID ################
        self.question_title_list = []
        self.question_pool_id_list = []
        self.all_entries_from_db_list = []


        self.names = []
        self.filename_id = []


        self.list_of_directories = []
        self.list_of_file_IDs = []
        self.filename_with_zip_index = []

        self.question_title_list = []
        self.question_pool_id_list = []
        self.question_title_to_pool_id_dict = {}
        self.question_title_to_item_id_dict = {}



        # Auflistung der Ordner im Ordner-Pfad: pool_directory_output
        self.list_of_directories = os.listdir(self.pool_directory_output)

        # Wird in der Liste eine Datei mit der Endung "*.zip" gefunden, dann Index speichern
        for i in range(len(self.list_of_directories)):
            if ".zip" in self.list_of_directories[i]:
                self.filename_with_zip_index.append(i)

            #else:
             #   self.list_of_file_IDs.append(self.pool_id_file_zip_template)

        # Aus der Datei-Liste alle Einträge aus der *.zip Liste entfernen
        # Dadurch enthält die Datei-Liste keine Namen mehr mit ".zip" Endung
        # .pop entfernt einen Eintrag aus der Liste und schiebt die restlichen Einträge wieder zusammen
        # Werden mehrere Einträge entfernt, ändert sich auch immer der Index der verbleibenden Einträge
        # z.B: Liste mit 5 Einträgen: Liste[0,1,2,3,4] -> Liste.pop(0) -> Liste[1,2,3,4]
        # Sollen mehrerer Einträge entfernt werden, veschiebt sich der Index um die Anzahl der bereits gelöschten Einträge
        # Daher ist hier auch ein .pop(x)-j ("j" für Schleifendurchlauf), da sich der Index bei jeden ".pop()" und 1 verschiebt

        for j in range(len(self.filename_with_zip_index)):
            self.list_of_directories.pop(self.filename_with_zip_index[j]-j)


        # Die letzten sieben (7) Zeichen des Orndernamen in eine Liste packen. Die letzten 7 Zeichen geben die ID des Fragenpools an
        # Die Ordnernamen für ILIAS sind immer in dem Format: z.B.: 1604407426__0__tst_2040314
        # Die ID wird im nachhinein um "1" inkrementiert
        for k in range(len(self.list_of_directories)):

            self.list_of_file_IDs.append(self.list_of_directories[k][-7:])


        if len(self.list_of_directories) == 0:
            self.list_of_file_IDs.append(self.pool_id_file_zip_template)

        # Alle String Einträge nach "INT" konvertieren um mit der max() funktion die höchste ID herauszufiltern
        self.list_of_file_IDs = list(map(int, self.list_of_file_IDs))
        self.file_max_id = str(max(self.list_of_file_IDs)+1)


        #Pfad anpassungen - Die ID muss um +1 erhöht werden, wenn "Fragenpool erstellen" betätigt wird
        self.ilias_id_pool_qpl_dir = "1596569820__0__qpl_" + self.file_max_id
        self.ilias_id_pool_qpl_xml = "1596569820__0__qpl_" + self.file_max_id + ".xml"
        self.ilias_id_pool_qti_xml = "1596569820__0__qti_" + self.file_max_id + ".xml"
        self.ilias_id_pool_img_dir = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, "objects"))

        self.qpl_file_pool_path_write = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))
        self.qti_file_pool_path_write = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))


        # Pfad für ILIAS-Taxonomie Dateien --> "export.xml"
        self.modules_export_file = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, 'Modules', 'TestQuestionPool', 'set_1', 'export.xml'))
        self.taxonomy_file_question_pool = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))




        # Neuen Ordner erstellen
        Additional_Funtions.createFolder(self, os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir)))


        # Hier wird das Verzeichnis kopiert, um die Struktur vom Fragenpool-Ordner zu erhalten
        # Die Struktur stammt aus einem Vorlage-Ordner. Die notwendigen XML Dateien werden im Anschluss ersetzt bzw. mit Werten aktualisiert
        Additional_Funtions.copytree(self, os.path.normpath(os.path.join(self.project_root_path, "Vorlage_für_Fragenpool", 'Vorlage_1596569820__0__qpl_2074808')),
                 os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir)))

        # Da durch "copytree" alle Daten kopiert werden, werden hier die qpl.xml und die qti.xml auf die aktuelle Nummer umbenannt und später dadurch überschrieben
        # Anpassung ID für "qti".xml
        os.rename(os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qti_2074808.xml")),
                  os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml)))

        # Anpassung ID für "qpl".xml
        os.rename(os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, "1596569820__0__qpl_2074808.xml")),
                  os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml)))


        # Aufruf -> Pool erstellen
        Create_ILIAS_Pool.pool_structure(self)

    def pool_structure(self):


        ###### Anpassung der Datei "Modul -> export". Akualisierung des Dateinamens
        self.mytree = ET.parse(self.modules_export_file)
        self.myroot = self.mytree.getroot()

        for TaxId in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
            TaxId.set('Id', self.file_max_id)

        self.mytree.write(self.modules_export_file)

        with open(self.modules_export_file, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('ns0:', 'exp:')
        with open(self.modules_export_file, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)



        ######  Anpassung der Datei "Modules -> //... //  -> export.xml". Akualisierung des Dateinamens
        self.taxonomy_export_file = os.path.normpath(os.path.join(self.pool_directory_output, self.ilias_id_pool_qpl_dir, 'Services', 'Taxonomy', 'set_1', 'export.xml'))
        self.mytree = ET.parse(self.taxonomy_export_file)
        self.myroot = self.mytree.getroot()

        for ExportItem in self.myroot.iter('{http://www.ilias.de/Services/Export/exp/4_1}ExportItem'):
            if ExportItem.attrib.get('Id') != "":
                ExportItem.set('Id', self.file_max_id)
                break



        for object_id in self.myroot.iter('{http://www.ilias.de/Services/Taxonomy/tax/4_3}ObjId'):
            object_id.text = self.file_max_id
            break

        self.mytree.write(self.taxonomy_export_file)

        # Taxonomie-datei "refreshen"
        Additional_Funtions.taxonomy_file_refresh(self, self.taxonomy_export_file)
        ###############################################################################

        # Pfad für ILIAS-Pool Dateien (zum hochladen in ILIAS)
        # ilias_id_pool_
        self.pool_qti_file_path_output = os.path.normpath(os.path.join(self.question_type_files_path_pool_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qti_xml))
        self.pool_qpl_file_path_output = os.path.normpath(os.path.join(self.question_type_files_path_pool_output, self.ilias_id_pool_qpl_dir, self.ilias_id_pool_qpl_xml))



######## Hier wird der Fragen_Pool erstellt

        # Aufruf: Modul -> Formelfrage -> Pool
        if self.question_type.lower() == "formelfrage" or self.question_type.lower() == "formel frage":
            test_generator_modul_formelfrage.Create_Formelfrage_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_pool_entry_ids,
                                                                                   "question_pool",
                                                                                   self.ilias_id_pool_img_dir,
                                                                                   self.ilias_id_pool_qpl_dir,
                                                                                   self.pool_qti_file_path_template,
                                                                                   self.pool_qti_file_path_output,
                                                                                   self.pool_qpl_file_path_output,
                                                                                   self.ilias_id_pool_qti_xml,
                                                                                   self.file_max_id,
                                                                                   self.taxonomy_file_question_pool
                                                                                   )

        # Aufruf: Modul -> SingleChoice -> Pool
        if self.question_type.lower() == "singlechoice" or self.question_type.lower() == "single choice":
            test_generator_modul_singlechoice.Create_SingleChoice_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_pool_entry_ids,
                                                                                   "question_pool",
                                                                                   self.ilias_id_pool_img_dir,
                                                                                   self.ilias_id_pool_qpl_dir,
                                                                                   self.pool_qti_file_path_template,
                                                                                   self.pool_qti_file_path_output,
                                                                                   self.pool_qpl_file_path_output,
                                                                                   self.ilias_id_pool_qti_xml,
                                                                                   self.file_max_id,
                                                                                   self.taxonomy_file_question_pool
                                                                                   )

        # Aufruf: Modul -> MultipleChoice -> Pool
        if self.question_type.lower() == "multiplechoice" or self.question_type.lower() == "multiple choice":
            test_generator_modul_multiplechoice.Create_MultipleChoice_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_pool_entry_ids,
                                                                                   "question_pool",
                                                                                   self.ilias_id_pool_img_dir,
                                                                                   self.ilias_id_pool_qpl_dir,
                                                                                   self.pool_qti_file_path_template,
                                                                                   self.pool_qti_file_path_output,
                                                                                   self.pool_qpl_file_path_output,
                                                                                   self.ilias_id_pool_qti_xml,
                                                                                   self.file_max_id,
                                                                                   self.taxonomy_file_question_pool
                                                                                   )

        # Aufruf: Modul -> Zuordnungsfrage -> Pool
        if self.question_type.lower() == "zuordnungsfrage" or self.question_type.lower() == "zuordnungs frage":
            test_generator_modul_zuordnungsfrage.Create_Zuordnungsfrage_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_pool_entry_ids,
                                                                                   "question_pool",
                                                                                   self.ilias_id_pool_img_dir,
                                                                                   self.ilias_id_pool_qpl_dir,
                                                                                   self.pool_qti_file_path_template,
                                                                                   self.pool_qti_file_path_output,
                                                                                   self.pool_qpl_file_path_output,
                                                                                   self.ilias_id_pool_qti_xml,
                                                                                   self.file_max_id,
                                                                                   self.taxonomy_file_question_pool
                                                                                   )

        # Aufruf: Modul -> Formelfrage_Permutation -> Pool
        if self.question_type.lower() == "formelfrage_perm" or self.question_type.lower() == "formel frage_perm":
            print("STRUKTUR FORMELFRAGE_PERMUTATION")
            test_generator_modul_formelfrage_permutation.Create_formelfrage_permutation_Questions.__init__(self,
                                                                                   self.db_entry_to_index_dict,
                                                                                   self.create_pool_entry_ids,
                                                                                   "question_pool",
                                                                                   self.ilias_id_pool_img_dir,
                                                                                   self.ilias_id_pool_qpl_dir,
                                                                                   self.pool_qti_file_path_template,
                                                                                   self.pool_qti_file_path_output,
                                                                                   self.pool_qpl_file_path_output,
                                                                                   self.ilias_id_pool_qti_xml,
                                                                                   self.file_max_id,
                                                                                   self.taxonomy_file_question_pool
                                                                                   )

        # Anschließend werden die "&amp;" in der XML wieder gegen "&" getauscht
        Additional_Funtions.replace_character_in_xml_file(self, self.pool_qti_file_path_output)


        # Hier wird die Taxonomie des Fragenpools bearbeitet / konfiguriert
        #
        # self.create_pool_entry.get(),              -- Nimmt die eingetragenen IDs aus der Eingabebox für Fragenpool
        # self.var_create_question_pool_all.get(),   --  Check-Box, "Alle Fragen erstellen?"
        # database_db_name,                          -- Datenbank-Name
        # database_table,                            -- Datenbank-Table-Name
        # self.ff_entry_to_index_dict,               -- Dictionionary
        # self.taxonomy_file_question_pool,          -- Taxonomie-Datei Ordner Pfad
        # self.pool_qti_file_path_output             -- QTI-Datei - Pfad

        test_generator_modul_taxonomie_und_textformatierung.Taxonomie.create_taxonomy_for_pool(self,
                                                                                    self.create_pool_entry_ids,
                                                                                    self.var_create_question_pool_all,
                                                                                    self.database_db_name,
                                                                                    self.database_table_name,
                                                                                    self.db_entry_to_index_dict,
                                                                                    self.taxonomy_file_question_pool,
                                                                                    self.pool_qti_file_path_output)


class Additional_Funtions:

    def add_picture_to_description_main(self, description_img_name_1, description_img_data_1, description_img_name_2,
                                              description_img_data_2, description_img_name_3, description_img_data_3,
                                              question_description_main, question_description_mattext,
                                              question_description_material, id_nr):

        self.description_img_name_1 = description_img_name_1
        self.description_img_data_1 = description_img_data_1
        self.description_img_name_2 = description_img_name_2
        self.description_img_data_2 = description_img_data_2
        self.description_img_name_3 = description_img_name_3
        self.description_img_data_3 = description_img_data_3

        self.picture_string_name_replace_1 = "%Bild1%"
        self.picture_string_name_replace_2 = "%Bild2%"
        self.picture_string_name_replace_3 = "%Bild3%"

        self.check_img_1_exists = False
        self.check_img_2_exists = False
        self.check_img_3_exists = False

        self.question_description_main = question_description_main
        self.question_description_mattext = question_description_mattext


        if self.description_img_data_1 != "EMPTY":
            self.question_description_mattext = Additional_Funtions.set_picture_in_main(self, self.description_img_name_1, self.description_img_data_1, "%Bild1%", self.question_description_main, question_description_material, id_nr, "0")

        if self.description_img_data_2 != "EMPTY":
            self.question_description_mattext = Additional_Funtions.set_picture_in_main(self, self.description_img_name_2, self.description_img_data_2, "%Bild2%", self.question_description_mattext, question_description_material, id_nr, "1")


        if self.description_img_data_3 != "EMPTY":
            self.question_description_mattext = Additional_Funtions.set_picture_in_main(self, self.description_img_name_3, self.description_img_data_3, "%Bild3%", self.question_description_mattext, question_description_material, id_nr, "2")


        if self.description_img_data_1 == "EMPTY" and self.description_img_data_2 == "EMPTY" and self.description_img_data_3 == "EMPTY":
            self.question_description_mattext = "<p>" + self.question_description_main + "</p>"





        return self.question_description_mattext


    def set_picture_in_main(self, description_img_name_var, description_img_data_var, picture_string_name_replace_var, question_description_mattext, question_description_material, id_nr, img_id_nr):

        # img_id: ist nnotwendig weil die Fragen eigene ID bekommen

        self.description_img_name_var = description_img_name_var
        self.description_img_data_var = description_img_data_var
        self.picture_string_name_replace_var = picture_string_name_replace_var





        if self.description_img_data_var != "EMPTY":

            with open('il_0_mob_TEST.png', 'wb') as image_file:
                image_file.write(self.description_img_data_var)

            self.file_image_raw = Image.open('il_0_mob_TEST.png')
            self.file_image_size_width, self.file_image_size_height = self.file_image_raw.size

            self.picture_in_main = "<p><img height=\"" + str(self.file_image_size_height) + "\" src=\"il_0_mob_000000" + str(img_id_nr) + "\" width=\"" + str(self.file_image_size_width) + "\" /></p>"

            # Wird eine Bild Position im Fragen Text eingetragen, wird es hier durch das eigentliche Bild ersetzt
            if self.picture_string_name_replace_var in question_description_mattext.split():


                question_description_mattext = question_description_mattext.replace(self.picture_string_name_replace_var, self.picture_in_main)

            else:
                # Wird keine Bild position gewählt, dann wird das Bild am Ende des Textes angehangen
                question_description_mattext = "<p>" + question_description_mattext + "</p>" + self.picture_in_main

            matimage = ET.SubElement(question_description_material, 'matimage')
            matimage.set('label', "il_0_mob_000000" + str(img_id_nr))  # Object -> Filename
            matimage.set('uri', "objects/il_0_mob_000000" + str(id_nr) + "/" + str(self.description_img_name_var) + ".png")

        # Frage enthält kein Bild
        else:
            question_description_mattext = "<p>" + question_description_mattext + "</p>"


        return question_description_mattext


    def add_dir_for_images(self, description_img_name_var, description_img_data_var, id_nr, test_or_pool, question_test_img_path, question_pool_img_path):

        self.description_img_name_var = description_img_name_var
        self.description_img_data_var = description_img_data_var

        self.question_test_img_path = question_test_img_path
        self.question_pool_img_path = question_pool_img_path

        if question_pool_img_path != "ilias_id_pool_img_dir_not_used_for_ilias_test":
            if test_or_pool == "question_test":

                if self.description_img_name_var != "EMPTY":
                    Additional_Funtions.createFolder(self, self.question_test_img_path + '/' + 'il_0_mob_000000' + str(id_nr) + '/')

                    #img wird immer als PNG Datei abgelegt.
                    with open(self.question_test_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png", 'wb') as image_file:
                        image_file.write(self.description_img_data_var)

                    self.image = Image.open(self.question_test_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png")
                    self.image.save(self.question_test_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png")

            else:  # image pool
                if self.description_img_name_var != "EMPTY":
                    Additional_Funtions.createFolder(self, self.question_pool_img_path + '/' + 'il_0_mob_000000' + str(id_nr) + '/')

                    #img wird immer als PNG Datei abgelegt.
                    with open(self.question_pool_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png", 'wb') as image_file:
                        image_file.write(self.description_img_data_var)

                    self.image = Image.open(self.question_pool_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png")
                    self.image.save(self.question_pool_img_path + "\\il_0_mob_000000" + str(id_nr) + "\\" + self.description_img_name_var + ".png")


    def replace_character_in_xml_file(self, file_path_qti_xml):
        print("______________________________________________________________________")
        print("Überarbeite xml_datei_qti --  \"&amp;\"-Zeichen...          ", end="", flush=True)
        # Im Nachgang werden alle "&amp;" wieder gegen "&" getauscht
        # "&" Zeichen kann XML nicht verarbeiten, daher wurde beim schreiben der Texte in die XML "&" gegen "&amp;" getauscht

        # XML Datei zum lesen öffnen 'r' -> "read"
        with open(file_path_qti_xml, 'r') as xml_file:
            xml_str = xml_file.read()
        xml_str = xml_str.replace('&amp;', '&')  # replace 'x' with 'new_x'

        # In XML Datei schreiben 'w" -> "write"
        with open(file_path_qti_xml, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

        print("abgeschlossen!")

    def copytree(self, src, dst, symlinks=False, ignore=None):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

    def set_taxonomy_for_question(self, id_nr, number_of_entrys, item, question_type_pool_qpl_file_path_template, question_type_pool_qpl_file_path_output):
        # Zusatz für Taxonomie-Einstellungen
        self.number_of_entrys = number_of_entrys
        self.question_type_pool_qpl_file_path_template = question_type_pool_qpl_file_path_template
        self.question_type_pool_qpl_file_path_output = question_type_pool_qpl_file_path_output

        self.id_int_numbers = 400000 + id_nr

        self.number_of_entrys.append(format(self.id_int_numbers, '06d')) #Zahlenfolge muss 6-stellig sein.

        item.set('ident', "il_0_qst_" + self.number_of_entrys[id_nr])


        # Hier wird die QPL bearbeitet - Taxonomie
        self.mytree = ET.parse(self.question_type_pool_qpl_file_path_template)
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

            self.mytree.write(self.question_type_pool_qpl_file_path_output)


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
            self.mytree.write(self.question_type_pool_qpl_file_path_output)

    def taxonomy_file_refresh(self, file_location):
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

        with open(self.file_location, 'w') as replaced_xml_file:
            replaced_xml_file.write(xml_str)

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)

    def add_image_to_description(self, check_use_img_1, check_use_img_2, check_use_img_3, frame_name,
                                 picture_name_img_1, picture_name_img_2, picture_name_img_3, picture_path_img_1,
                                 picture_path_img_2, picture_path_img_3):

        self.question_description_img_1_filename_label = None
        self.question_description_img_2_filename_label = None
        self.question_description_img_3_filename_label = None

        #self.question_description_img_1_filename_label = question_description_img_1_filename_label
        #self.question_description_img_2_filename_label = question_description_img_2_filename_label
        #self.question_description_img_3_filename_label = question_description_img_3_filename_label



        self.frame_name = frame_name
        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        self.picture_name_img_1 = picture_name_img_1
        self.picture_name_img_2 = picture_name_img_2
        self.picture_name_img_3 = picture_name_img_3
        self.picture_path_img_1 = picture_path_img_1
        self.picture_path_img_2 = picture_path_img_2
        self.picture_path_img_3 = picture_path_img_3

        self.check_use_img_1_temp = 0




        # Bild 1 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_1 == 1:
            self.picture_path_img_1 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_1 = self.picture_path_img_1.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.picture_name_img_1 = self.picture_path_img_1[int(self.last_char_index_img_1) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_1 = self.picture_path_img_1[-4:]

            self.question_description_img_1_filename_label = Label(self.frame_name, text=self.picture_name_img_1)
            self.question_description_img_1_filename_label.grid(row=0, column=1, sticky=W)

            self.file_image_1 = ImageTk.PhotoImage(Image.open(self.picture_path_img_1).resize((100, 100)))
            self.file_image_1_raw = Image.open(self.picture_path_img_1)
            self.file_image_1_width, self.file_image_1_height = self.file_image_1_raw.size
            self.file_image_1_label = Label(self.frame_name, image=self.file_image_1)
            self.file_image_1_label.image = self.file_image_1
            self.file_image_1_label.grid(row=0, column=2)


        # Bild 2 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_2 == 1:
            self.picture_path_img_2 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_2 = self.picture_path_img_2.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.picture_name_img_2 = self.picture_path_img_2[int(self.last_char_index_img_2) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_2 = self.picture_path_img_2[-4:]

            self.question_description_img_2_filename_label = Label(self.frame_name, text=self.picture_name_img_2)
            self.question_description_img_2_filename_label.grid(row=1, column=1, sticky=W)


            self.file_image_2 = ImageTk.PhotoImage(Image.open(self.picture_path_img_2).resize((100, 100)))
            self.file_image_2_raw = Image.open(self.picture_path_img_2)
            self.file_image_2_width, self.file_image_2_height = self.file_image_2_raw.size
            self.file_image_2_label = Label(self.frame_name, image=self.file_image_2)
            self.file_image_2_label.image = self.file_image_2
            self.file_image_2_label.grid(row=1, column=2)


        # Bild 3 auswählen und von Datei-Pfad den Bild-Namen extrahieren
        if self.check_use_img_3 == 1:

            self.picture_path_img_3 = filedialog.askopenfilename(initialdir= pathlib.Path().absolute(), title="Select a File")
            self.last_char_index_img_3 = self.picture_path_img_3.rfind("/")                                 # Suche Index in dem das letzte "/" auftaucht

            self.picture_name_img_3 = self.picture_path_img_3[int(self.last_char_index_img_3) + 1:-4]   #letzten char des bildnamens ist das dateiformat: Testbild.jpg
            self.image_format_new_img_3 = self.picture_path_img_3[-4:]
            self.question_description_img_3_filename_label = Label(self.frame_name, text=self.picture_name_img_3)
            self.question_description_img_3_filename_label.grid(row=2, column=1, sticky=W)

            self.file_image_3 = ImageTk.PhotoImage(Image.open(self.picture_path_img_3).resize((100, 100)))
            self.file_image_3_raw = Image.open(self.picture_path_img_3)
            self.file_image_3_width, self.file_image_3_height = self.file_image_3_raw.size
            self.file_image_3_label = Label(self.frame_name, image=self.file_image_3)
            self.file_image_3_label.image = self.file_image_3
            self.file_image_3_label.grid(row=2, column=2)



        return self.picture_name_img_1, self.picture_name_img_2, self.picture_name_img_3, self.picture_path_img_1, self.picture_path_img_2, self.picture_path_img_3, self.question_description_img_1_filename_label, self.question_description_img_2_filename_label, self.question_description_img_3_filename_label

    def delete_image_from_description(self, check_use_img_1, check_use_img_2, check_use_img_3, question_description_img_1_filename_label, question_description_img_2_filename_label, question_description_img_3_filename_label, picture_name_img_1, picture_name_img_2, picture_name_img_3 ):
        self.check_use_img_1 = check_use_img_1
        self.check_use_img_2 = check_use_img_2
        self.check_use_img_3 = check_use_img_3

        self.question_description_img_1_filename_label = question_description_img_1_filename_label
        self.question_description_img_2_filename_label = question_description_img_2_filename_label
        self.question_description_img_3_filename_label = question_description_img_3_filename_label

        self.picture_name_img_1 = picture_name_img_1
        self.picture_name_img_2 = picture_name_img_2
        self.picture_name_img_3 = picture_name_img_3




        if self.check_use_img_1 == 0 and question_description_img_1_filename_label != None:

            self.question_description_img_1_filename_label.grid_remove()
            self.file_image_1_label.destroy()
            self.picture_name_img_1 ="EMPTY"
            question_description_img_1_filename_label = None

        if self.check_use_img_2 == 0 and question_description_img_2_filename_label != None :
            self.question_description_img_2_filename_label.grid_remove()
            self.file_image_2_label.destroy()
            self.picture_name_img_2 ="EMPTY"

        if self.check_use_img_3 == 0 and question_description_img_3_filename_label != None:
            self.question_description_img_3_filename_label.grid_remove()
            self.file_image_3_label.destroy()
            self.picture_name_img_3 ="EMPTY"


        return self.picture_name_img_1, self.picture_name_img_2, self.picture_name_img_3



