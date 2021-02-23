# Erste Schritte im Umgang mit XML Dateien und Python mit dem Plugin Element Tree
# Lesen/Schreiben in XML Dateien sowie Suchen/Ersetzen von Einträgen in der Baumstruktur
# Zum Schluss befindet sich eine kleine Übersicht der XML Struktur im Kommentar



# Importieren der notwendigen ElementTree Bibliothek
import xml.etree.ElementTree as ET


# ------- *.XML DATEI AUSLESEN
# ET.parse("Pfad") liest eine XML Datei ein
# .getroot() übernimmt die Baumstruktur aus der Datei
mytree = ET.parse('1587456989__0__qti_1938477.xml')
myroot = mytree.getroot()


# ------- DATEI NACH EINTRAG DURCHSUCHEN UND ERSETZEN
# In der XML wird unterschieden zwischen Text-Einträgen und Attributen
# Steht in der XML ein (einfacher) Text z.B.: <fieldlabel>author</fieldlabel>
# dann kann dieser mit '.text = ""' geändert werden
#
# Wohingegen bei Einträgen der Form <item ident="il_0_qst_601915" title="XML-Test">
# handelt es sich um Attribute von "item". 'ident' und 'title' (auch zu erkennen an dem '=') sind Attribute.
# Um einen solchen Eintrag zu ändern muss folgendes geschrieben werden: item.set('ident', "il_0_qst_000000")
# ---> item.set( name_von_attribut, wert_von_attribut )


# for x in myroot.iter("Eintrag") --> Die XML wird von oben nach unten nach dem/den Eintrag/Einträgen durchsucht
#                                     Es werden ALLE Einträge gefunden die den Namen tragen (kein STOP nach dem ersten Treffer)
#
# Wird der Eintrag gefunden, dann wird in der darunter liegenden Ebene (fieldlabel) nach dem Text "password" gesucht
# Anschließend wird Text für "fieldentry" geändert
#

for qtimetadatafield in myroot.iter('qtimetadatafield'):
    if qtimetadatafield.find('fieldlabel').text == "password":
        qtimetadatafield.find('fieldentry').text = str('Sample')

    if qtimetadatafield.find('fieldlabel').text == "author":
        qtimetadatafield.find('fieldentry').text = str(' Tobias  --updated')


# ------- DATEI NACH EINTRAG DURCHSUCHEN UND NACH 1.TREFFER STOPPEN
#
# Die XML wird nach dem Eintrag "item" durchsucht und das Attribut wird geändert
# Mit "break" wird NUR das erste "item" bearbeitet (der 1. Treffer beim durchsuchen der XML)
for item in myroot.iter('item'):
    print(item.get('ident'))

    item.set('ident', "il_0_qst_000000")

    print(item.get('ident'))
    break

# ------- ÄNDERUNGEN IN NEUE XML SCHREIBEN
# .write(Pfad) schreibt die Daten in die neue Datei *.xml
mytree.write('newVersion_1587456989__0__qti_1938477.xml')


"""
Schematischer Aufbau der XML Datei. Jede ILIAS XML Datei hat diese Art Struktur beginnend mit "questestinterop"
Hier werden zur leichteren Übersicht lediglich ein paar Zeilen gezeigt. 

<questestinterop>
	<item ident="il_0_qst_601915" title="XML-Test">
		<qticomment/>
		<qtimetadata>
			<qtimetadatafield>
				<fieldlabel>ILIAS_VERSION</fieldlabel>
				<fieldentry>5.4.18 2020-10-23</fieldentry>
            </qtimetadatafield>
			<qtimetadatafield>
				<fieldlabel>author</fieldlabel>
				<fieldentry>Tobias Panteleit</fieldentry>
			</qtimetadatafield>
			<qtimetadatafield>
				<fieldlabel>password</fieldlabel>
				<fieldentry/>
			</qtimetadatafield>
			...
"""



