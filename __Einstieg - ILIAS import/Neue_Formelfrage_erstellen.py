import xml.etree.ElementTree as ET


# ------- XML DATEI EINLESEN
mytree = ET.parse('1587633204__0__qti_1944435.xml')
myroot = mytree.getroot()



# ------- FRAGEN-TITEL ÄNDERN
# Die Struktur der XML ist in einem ILIAS-Test leicht anders als in einem ILIAS-Pool
# Ein Test beinhaltet zum einen die Auflistung von Test-Einstellungen ("assessmentcontrol")
# In einem Fragen-Pool werden lediglich die einzelnen Fragen ('items') aufgelistet

# Hier wird der Titel des Fragen-Tests geändert
# Es muss kein neuer Eintrag mit ET.Subelement() erzeugt werden, da ein "assessment" Eintrag schon
# in der eingelesenen XML vorhanden ist. Es wird nur nach dem Eintrag "assessment" gesucht.
for assessment in myroot.iter('assessment'):
    assessment.set('title', "Fragen-Test 2")



# ------- STANDARD ID EINTRAGEN
# Für jede Frage ist eine eigene ID notwendig. Wird eine ID für "item" eingetragen, wird diese bei einem import
# in das ILIAS System automatisch angepasst. Das Format MUSS "il_0_qst_" + 6-stellige Nr sein!
for item in myroot.iter('item'):
    item.set('ident', "il_0_qst_000000")




# ------- NEUE FRAGE ZU BESTEHENDER DATEI HINZUFÜGEN
# Fragen sind immer vom Typ "item". Das bedeutet das jede Frage mit dem XML-Zweig "item" startet
# (Bsp.: <item ident="il_0_qst_497937" title="Runden">

# Wird eine XML Datei eingelesen und man schaut sich die Hauptzweige an, ergibt sich folgendes Bild:
#  myroot[0][0] -> qticomment
#  myroot[0][1] -> qtimetadata
#  myroot[0][2] -> objectives
#  myroot[0][3] -> assessmentcontrol
#  myroot[0][4] -> section

# Soll eine neue Frage angehangen werden, muss diese Frage in der Sektion "myroot[0][4] eingetragen werden
"""
XML-Datei (Zweige eingeklappt) 

<questestinterop>
	<assessment ident="il_0_tst_9634" title="Test-Titel">
		<qticomment>
		<qtimetadata>
		<objectives>
		<assessmentcontrol>
		<section>
		    <item>
	    </section>
	</assessment>
</questestinterop>		
"""




# -------XML BAUM-STRUKTUR ANLEGEN UND NEUE FRAGE (ITEM) HINZUFÜGEN
#
# Haupt-Element - "questestinterop"
# Sub-Element - "assessment"
# Sub-Element - "section"
# Sub-Element - "item"
#
# <questestinterop>
# 	<assessment>
#       <section>
# 			<item>

questestinterop = ET.Element('questestinterop')
assessment = ET.SubElement(questestinterop, 'assessment')
section = ET.SubElement(assessment, 'section')
item = ET.SubElement(section, 'item')
item.set('ident', "il_0_qst_000000")
item.set('title', "Frage 1")


formel = 'sqrt($v1 + $v2)'

qticomment = ET.SubElement(item, 'qticomment')

# Bearbeitungsdauer der Frage
duration = ET.SubElement(item, 'duration')
duration.text = "P0Y0M0DT1H0M0S"

# Subelemente von "item"
# "presentation" muss den gleichen Titel tragen, wie unter item -> title
itemmetadata = ET.SubElement(item, 'itemmetadata')
presentation = ET.SubElement(item, 'presentation')
presentation.set('label', "Frage 1")
flow = ET.SubElement(presentation, 'flow')
material = ET.SubElement(flow, 'material')
mattext = ET.SubElement(material, 'mattext')
mattext.set('texttype', "text/html")
mattext.text = "<p>" + formel + "= $r1</p>"


qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')


# ------- Formelfrage - spezifische Einträge hinzufügen
#
# Der Fragen-"Kopf" beinhaltet Informationen zur ILIAS-Version, Fragentyp, Autor etc.
# Diese sind von Fragentyp zu Fragentyp unterschiedlich
#
# Für jeden Eintrag müssen neue Sublemente "qtimetadatafield", "fieldlabel, "fieldentry" angelegt werden.

# -----------------------------------------------------------------------ILIAS VERSION
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = "ILIAS_VERSION"
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = "5.4.10 2020-03-04"

# -----------------------------------------------------------------------QUESTION_TYPE
# Eine Formelfrage wird in ILIAS durch den Eintrag "assFormulaQuestion" als Formelfrage bestimmt
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
fieldentry.text = "Tobias Panteleit"

# -----------------------------------------------------------------------POINTS
# Gibt die Punkte für das richtige Ergebnis der Formelfrage an
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = "points"
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = "1"

# -----------------------------------------------------------------------Variable 1
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = "$v1"
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = "a:6:{s:9:\"precision\";i:0;s:12:\"intprecision\";s:1:\"1\";s:8:\"rangemin\";d:0;s:8:\"rangemax\";d:10;s:4:\"unit\";s:0:\"\";s:9:\"unitvalue\";s:0:\"\";}"

# -----------------------------------------------------------------------Variable 2
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = "$v2"
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = "a:6:{s:9:\"precision\";i:0;s:12:\"intprecision\";s:1:\"1\";s:8:\"rangemin\";d:0;s:8:\"rangemax\";d:10;s:4:\"unit\";s:0:\"\";s:9:\"unitvalue\";s:0:\"\";}"

# -----------------------------------------------------------------------Solution 1
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = "$r1"
fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
fieldentry.text = "a:10:{s:9:\"precision\";i:1;s:9:\"tolerance\";s:1:\"0\";s:8:\"rangemin\";s:1:\"0\";s:8:\"rangemax\";s:1:\"5\";s:6:\"points\";s:1:\"1\";s:7:\"formula\";s:15:\"" + formel + "\";s:6:\"rating\";s:0:\"\";s:4:\"unit\";s:0:\"\";s:9:\"unitvalue\";s:0:\"\";s:11:\"resultunits\";a:0:{}}"

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
fieldentry.text = "5ea15b58e99d01.20189367"     # -------This number is some default number. It changes when imported/exported from ilias



# ------- NEUE FRAGE (ITEM) IN ENTSPRECHENDER SEKTION EINFÜGEN
# Soll eine neue Frage angehangen werden, muss diese Frage in der Sektion "myroot[0][4] eingetragen werden
myroot[0][4].append(item)


# -------Write to *.xml file
mytree.write('newV_ID_1587633204__0__qti_1944435.xml')



"""
Schema der XML Datei - ILIAS Testdatei

<questestinterop>
	<assessment ident="il_0_tst_9634" title="Test-Titel">
		<qticomment/>
		<qtimetadata>
			<qtimetadatafield>
			    <fieldlabel>ILIAS_VERSION</fieldlabel>
                <fieldentry>5.4.18 2020-10-23</fieldentry>
            </qtimetadatafield>
            
            <qtimetadatafield>
                <fieldlabel>QUESTIONTYPE</fieldlabel>
                <fieldentry>assFormulaQuestion</fieldentry>
            </qtimetadatafield>
            
            <qtimetadatafield>
                <fieldlabel>AUTHOR</fieldlabel>
                <fieldentry>Tobias Panteleit</fieldentry>
            </qtimetadatafield>
            
            <qtimetadatafield>
                <fieldlabel>points</fieldlabel>
                <fieldentry>1</fieldentry>
			</qtimetadatafield>
			
			[...]
			
		</qtimetadata>
		<objectives>
			<material>
				<mattext texttype="text/plain"/>
			</material>
		</objectives>
		<assessmentcontrol/>
		<section ident="1">
			<item ident="il_0_qst_601915" title="Frage 1">
                <qticomment/>
                <duration>P0Y0M0DT23H0M0S</duration>
                <itemmetadata>
                    <qtimetadata>
                        <qtimetadatafield>
                            <fieldlabel>ILIAS_VERSION</fieldlabel>
                            <fieldentry>5.4.18 2020-10-23</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>QUESTIONTYPE</fieldlabel>
                            <fieldentry>assFormulaQuestion</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>AUTHOR</fieldlabel>
                            <fieldentry>Tobias Panteleit</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>points</fieldlabel>
                            <fieldentry>1</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>$v1</fieldlabel>
                            <fieldentry>a:6:{s:9:"precision";i:1;s:12:"intprecision";s:1:"1";s:8:"rangemin";d:0;s:8:"rangemax";d:10;s:4:"unit";s:0:"";s:9:"unitvalue";s:0:"";}</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>$v2</fieldlabel>
                            <fieldentry>a:6:{s:9:"precision";i:1;s:12:"intprecision";s:1:"1";s:8:"rangemin";d:0;s:8:"rangemax";d:10;s:4:"unit";s:0:"";s:9:"unitvalue";s:0:"";}</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>$r1</fieldlabel>
                            <fieldentry>a:10:{s:9:"precision";i:1;s:9:"tolerance";s:1:"1";s:8:"rangemin";s:1:"0";s:8:"rangemax";s:3:"200";s:6:"points";s:1:"1";s:7:"formula";s:37:"$v4 * $v1 * 10^-6 + 0 * $v3 + 0 * $v2";s:6:"rating";s:0:"";s:4:"unit";s:0:"";s:9:"unitvalue";s:0:"";s:11:"resultunits";a:0:{}}</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>additional_cont_edit_mode</fieldlabel>
                            <fieldentry>default</fieldentry>
                        </qtimetadatafield>
                        <qtimetadatafield>
                            <fieldlabel>externalId</fieldlabel>
                            <fieldentry>5ea15be69c1e96.43933468</fieldentry>
                        </qtimetadatafield>
                    </qtimetadata>
                </itemmetadata>
                <presentation label="Frage 1">
                    <flow>
                        <material>
                            <mattext texttype="text/xhtml">&lt;p&gt;R1 = $v1µ&lt;/p&gt;&#13;&#10;&lt;p&gt;R2 = $v2&lt;/p&gt;&#13;&#10;&lt;p&gt;R3 = $v3&lt;/p&gt;&#13;&#10;&lt;p&gt;I =$v4&lt;/p&gt;&#13;&#10;&lt;p&gt;&lt;/p&gt;&#13;&#10;&lt;p&gt;Spannung U1 = $r1&lt;/p&gt;</mattext>
                        </material>
                    </flow>
                </presentation>
            </item>


"""