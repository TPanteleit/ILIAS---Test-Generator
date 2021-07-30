"""
********************************************
test_generator_modul_zeigerdiagramme.py
@digitalfellowship - Stand 07/2021
Autor: Tobias Panteleit
********************************************

Dieses Modul dient der Erstellung von Zeigerdiagrammen für Serienschaltungen
Die Funktionen hierfür sind noch stark begrenzt und geben eine Idee wie Zeigerdiagramme auf der
GUI angegeben werden könnten. Ein sinnvoller Einsatz ist im jetzigen Zustand nicht möglich.
Die definierten Schaltungen sind noch intern mit festen Werten belegt!
"""

import math
import numpy as np
import matplotlib.pyplot as plt


class Zeigerdiagramme:
    def __init__(self, diagramm_typ, spannung_strom_diagramm_check, impedanz_diagramm_check, admittanz_diagramm_check, leistungsdiagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz):


        self.diagramm_typ = diagramm_typ
        self.spannungsdiagramm_check = spannung_strom_diagramm_check
        self.impedanz_diagramm_check = impedanz_diagramm_check
        self.admittanz_diagramm_check = admittanz_diagramm_check
        self.leistungsdiagramm_check = leistungsdiagramm_check

        self.spannung_ges = spannung_ges
        self.widerstand = widerstand
        self.induktivitaet = induktivitaet
        self.kapazitaet = kapazitaet
        self.frequenz = frequenz

        # ---------
        # Eigenschaften des Plots

        self.fenster_groesse_x = 4
        self.fenster_groesse_y = 4

        self.achse_x_name_groesse = 10
        self.achse_y_name_groeese = 10

        self.achsen_beschriftung_groesse = 10


        self.zeiger_linien_dicke = 3
        self.zeiger_kopf_dicke = 0.7
        self.zeiger_kopf_laenge = 0.9

        #####
        self.spannung_ges = 5
        self.widerstand = 5
        self.induktivitaet = 1e-3
        self.kapazitaet = 10e-6
        self.frequenz = 1000


        # Farbenpalette für matplotlib
        # https://matplotlib.org/2.0.2/examples/color/named_colors.html

        # Behindertengerechte Farbpalette
        # dunkelblau, blau, hellblau
        # dunkelgrau, grau, hellgrau
        # schwarz, orange, braun, hellrot

        self.arrow_1_color = 'darkgrey'
        self.arrow_2_color = 'brown'
        self.arrow_3_color = 'orange'
        self.arrow_4_color = 'royalblue'


        #self.arrow_2_color = 'royalblue'
        #self.arrow_3_color = 'deepskyblue'
        #self.arrow_4_color = 'dimgray'
        self.arrow_5_color = 'tan'
        self.arrow_6_color = 'lightgrey'
        self.arrow_7_color = 'black'
        self.arrow_8_color = 'orange'
        self.arrow_9_color = 'brown'
        self.arrow_10_color = 'coral'

        Zeigerdiagramme.zeigerdiagramm_erstellen(self)


    def serienschaltung_R_L(self, spannung_strom_diagramm_check, impedanz_diagramm_check, admittanz_diagramm_check, leistungsdiagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz, fig):

        self.widerstand = widerstand
        self.induktivitaet = induktivitaet

        self.spannung_rl_Uges = spannung_ges
        self.impedanz_rl_R = widerstand
        self.impedanz_rl_R = 50

        self.induktivitaet = 1*10e-3
        self.frequenz = 50
        self.spannung_rl_Uges = 10



        self.impedanz_rl_X_L = 1j * 2 * math.pi * self.frequenz * self.induktivitaet
        self.impedanz_rl_X_L = 1j*70


        self.impedanz_rl_Zges = self.impedanz_rl_R + self.impedanz_rl_X_L

        self.strom_rl_Iges = self.spannung_rl_Uges / (self.impedanz_rl_Zges)

        self.spannung_rl_U_R = self.strom_rl_Iges * self.impedanz_rl_R
        self.spannung_rl_U_L = self.strom_rl_Iges * self.impedanz_rl_X_L




        if spannung_strom_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RL - Spannungen/Strom"

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,     0,      self.spannung_rl_Uges.real, self.spannung_rl_Uges.imag,     length_includes_head=True,  color = self.arrow_1_color, label ='Uges',)
            plt.arrow(0,     0,      self.spannung_rl_U_R.real, self.spannung_rl_U_R.imag,        length_includes_head=True, color = self.arrow_2_color,  label ='U_R', alpha=0.7)
            plt.arrow(0,     0,      self.spannung_rl_U_L.real, self.spannung_rl_U_L.imag,       length_includes_head=True,  color = self.arrow_3_color, label ='U_L', alpha=0.7)
            plt.arrow(0,     0,      self.strom_rl_Iges.real, self.strom_rl_Iges.imag,         length_includes_head=True,    color = self.arrow_4_color, label ='Iges', alpha=0.7)

        if impedanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RL - Impedanzen"

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.impedanz_rl_Zges.real, self.impedanz_rl_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Z', alpha=0.7)
            plt.arrow(0,                        0,                                                  self.impedanz_rl_R.real,    self.impedanz_rl_R.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='R', alpha=0.7)
            plt.arrow(self.impedanz_rl_R.real,     self.impedanz_rl_R.imag,                       self.impedanz_rl_X_L.real,  self.impedanz_rl_X_L.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='X_L', alpha=0.7)



        if admittanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RL - Admittanzen"
            self.admittanz_rl_R = np.reciprocal(self.impedanz_rl_R)
            self.admittanz_rl_X_L = np.reciprocal(self.impedanz_rl_X_L)

            self.admittanz_rl_Zges = self.admittanz_rl_R + self.admittanz_rl_X_L


            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.admittanz_rl_Zges.real, self.admittanz_rl_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Y')
            plt.arrow(0,                        0,                                                  self.admittanz_rl_R.real, self.admittanz_rl_R.imag,        linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='G')
            plt.arrow(self.admittanz_rl_R.real,     self.admittanz_rl_R.imag,                       self.admittanz_rl_X_L.real, self.admittanz_rl_X_L.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Y_L')


        if leistungsdiagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RL - Leistungen"
            self.rl_scheinleistung = self.spannung_rl_Uges * self.strom_rl_Iges
            self.rl_wirkleistung = self.rl_scheinleistung.real
            self.rl_blindleistung = self.rl_scheinleistung.imag*1j

            print(self.rl_scheinleistung)
            print(self.rl_wirkleistung)
            print(self.rl_blindleistung)

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                      self.rl_scheinleistung.real, self.rl_scheinleistung.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='S')
            plt.arrow(0,                        0,                                                      self.rl_wirkleistung.real,   self.rl_wirkleistung.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='P')
            plt.arrow(self.rl_wirkleistung.real,   self.rl_wirkleistung.imag,                           self.rl_blindleistung.real,  self.rl_blindleistung.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Q')



    def serienschaltung_R_C(self, spannung_strom_diagramm_check, impedanz_diagramm_check, admittanz_diagramm_check, leistungsdiagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz, fig):

        self.widerstand = widerstand


        self.spannung_rc_Uges = spannung_ges
        self.impedanz_rc_R = widerstand
        self.impedanz_rc_R = 12000

        self.rc_kapazitaet = 200e-9
        self.rc_frequenz = (1000/(2*math.pi))
        self.spannung_rc_Uges = 33.8

        self.impedanz_rc_X_C = -1j / (2 * math.pi * self.rc_frequenz * self.rc_kapazitaet)

        self.impedanz_rc_Zges = self.impedanz_rc_R + self.impedanz_rc_X_C

        self.strom_rc_Iges = self.spannung_rc_Uges / (self.impedanz_rc_Zges)

        self.spannung_rc_U_R = self.strom_rc_Iges * self.impedanz_rc_R
        self.spannung_rc_U_C = self.strom_rc_Iges * self.impedanz_rc_X_C


        print("X_C ", self.impedanz_rc_X_C)
        print("Iges ", self.strom_rc_Iges)
        print("U_R ", self.spannung_rc_U_R)
        print("U_C ", self.spannung_rc_U_C)


        if spannung_strom_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RC - Spannungen/Strom"

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,     0,      self.spannung_rc_Uges.real, self.spannung_rc_Uges.imag,     length_includes_head=True,  color = self.arrow_1_color, label ='Uges',)
            plt.arrow(0,     0,      self.spannung_rc_U_R.real, self.spannung_rc_U_R.imag,        length_includes_head=True, color = self.arrow_2_color,  label ='U_R', alpha=0.7)
            plt.arrow(0,     0,      self.spannung_rc_U_C.real, self.spannung_rc_U_C.imag,       length_includes_head=True,  color = self.arrow_3_color, label ='U_C', alpha=0.7)
            plt.arrow(0,     0,      self.strom_rc_Iges.real, self.strom_rc_Iges.imag,         length_includes_head=True,    color = self.arrow_4_color, label ='Iges', alpha=0.7)

        if impedanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RC - Impedanzen"

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.impedanz_rc_Zges.real, self.impedanz_rc_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Z', alpha=0.7)
            plt.arrow(0,                        0,                                                  self.impedanz_rc_R.real,    self.impedanz_rc_R.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='R', alpha=0.7)
            plt.arrow(self.impedanz_rc_R.real,     self.impedanz_rc_R.imag,                       self.impedanz_rc_X_C.real,  self.impedanz_rc_X_C.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='X_C', alpha=0.7)



        if admittanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RC - Admittanzen"
            self.admittanz_rc_R = np.reciprocal(self.impedanz_rc_R)
            self.admittanz_rc_X_C = np.reciprocal(self.impedanz_rc_X_C)

            self.admittanz_rc_Zges = self.admittanz_rc_R + self.admittanz_rc_X_C


            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.admittanz_rc_Zges.real, self.admittanz_rc_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Y')
            plt.arrow(0,                        0,                                                  self.admittanz_rc_R.real, self.admittanz_rc_R.imag,        linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='G')
            plt.arrow(self.admittanz_rc_R.real,     self.admittanz_rc_R.imag,                       self.admittanz_rc_X_C.real, self.admittanz_rc_X_C.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Y_C')


        if leistungsdiagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RC - Leistungen"
            self.rc_scheinleistung = self.spannung_rc_Uges * self.strom_rc_Iges
            self.rc_wirkleistung = self.rc_scheinleistung.real
            self.rc_blindleistung = self.rc_scheinleistung.imag*1j

            print(self.rc_scheinleistung)
            print(self.rc_wirkleistung)
            print(self.rc_blindleistung)

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                      self.rc_scheinleistung.real, self.rc_scheinleistung.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='S')
            plt.arrow(0,                        0,                                                      self.rc_wirkleistung.real,   self.rc_wirkleistung.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='P')
            plt.arrow(self.rc_wirkleistung.real,   self.rc_wirkleistung.imag,                           self.rc_blindleistung.real,  self.rc_blindleistung.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Q')



    def serienschaltung_R_L_C(self, spannung_strom_diagramm_check, impedanz_diagramm_check, admittanz_diagramm_check, leistungsdiagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz, fig):
        
        

        self.widerstand = float(widerstand)
        self.induktivitaet = float(induktivitaet)
        self.kapazitaet = float(kapazitaet)
        self.frequenz = float(frequenz)

        self.impedanz_R = self.widerstand
        self.impedanz_X_L = 1j * 2 * math.pi * self.frequenz * self.induktivitaet
        self.impedanz_X_C = -1j / (2 * math.pi * self.frequenz * self.kapazitaet)
        self.impedanz_Zges = self.widerstand + self.impedanz_X_L + self.impedanz_X_C

        self.spannung_rlc_Uges = spannung_ges
        self.strom_rlc_Iges = self.spannung_rlc_Uges / self.impedanz_Zges


        print(self.widerstand)
        print(self.induktivitaet)
        print(self.kapazitaet)
        print(self.frequenz)

        #self.widerstand = 5
        #self.induktivitaet = 1e-3
        #self.kapazitaet = 1e-6
        #self.frequenz = 1000



        print(impedanz_diagramm_check, widerstand, induktivitaet, kapazitaet, frequenz)


        if spannung_strom_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Spannungen"





            self.spannung_rlc_U_R = self.strom_rlc_Iges * self.widerstand
            phase_Iges = np.angle(self.strom_rlc_Iges, deg=True)
            self.spannung_rlc_U_L = self.strom_rlc_Iges * self.impedanz_X_L
            self.spannung_rlc_U_C = self.strom_rlc_Iges * self.impedanz_X_C

            print("RLC SPANNUNGEN")
            print(abs(self.spannung_rlc_U_R), abs(self.spannung_rlc_U_L), abs(self.spannung_rlc_U_C), abs(self.strom_rlc_Iges))
            print("phase: ", phase_Iges )
            print("##############")

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,   0,    self.spannung_rlc_U_R.real, self.spannung_rlc_U_R.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color = self.arrow_1_color, label ='U_R', alpha=0.7)
            plt.arrow(0,   0,    self.spannung_rlc_U_L.real, self.spannung_rlc_U_L.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True, color =self.arrow_2_color,  label ='U_L', alpha=0.7)
            plt.arrow(0,   0,    self.spannung_rlc_U_C.real, self.spannung_rlc_U_C.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color =self.arrow_3_color, label ='U_C', alpha=0.7)
            plt.arrow(0,   0,    self.strom_rlc_Iges.real, self.strom_rlc_Iges.imag,        linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color =self.arrow_4_color,   label ='Iges', alpha=0.7)
            plt.arrow(0,   0,    self.spannung_rlc_Uges.real, self.spannung_rlc_Uges.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color =self.arrow_5_color,   label ='Uges', alpha=0.7)


            #return self.spannung_rlc_Uges, self.spannung_rlc_R, self.spannung_rlc_L, self.spannung_rlc_C, self.zeigerdiagramm_typ_titel

        if impedanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Impedanzen"
            # Zeiger: Impedanzen

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.impedanz_Zges.real, self.impedanz_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Z')
            plt.arrow(0,                        0,                                                  self.impedanz_X_L.real, self.impedanz_X_L.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='X_L')
            plt.arrow(self.impedanz_R.real,     (self.impedanz_R.imag+self.impedanz_X_L.imag),      self.impedanz_X_C.real, self.impedanz_X_C.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='X_C')
            plt.arrow(self.impedanz_X_L.real,   self.impedanz_X_L.imag,    self.impedanz_R,        0,                                                  linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color=self.arrow_4_color,   label ='R')

            phase_impedanz_Zges = np.angle(self.impedanz_Zges, deg=True)
        
        if admittanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Admittanzen"
            self.admittanz_R = np.reciprocal(self.impedanz_R)
            self.admittanz_X_L = np.reciprocal(self.impedanz_X_L)
            self.admittanz_X_C = np.reciprocal(self.impedanz_X_C)
            self.admittanz_Zges = self.admittanz_R + self.admittanz_X_L + self.admittanz_X_C


            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.admittanz_Zges.real, self.admittanz_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='Y')
            plt.arrow(0,                        0,                                                  self.admittanz_X_L.real, self.admittanz_X_L.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='Y_L')
            plt.arrow(self.admittanz_R.real,     (self.admittanz_R.imag+self.admittanz_X_L.imag),      self.admittanz_X_C.real, self.admittanz_X_C.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Y_C')
            plt.arrow(self.admittanz_X_L.real,   self.admittanz_X_L.imag,    self.admittanz_R,        0,                                                  linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color=self.arrow_4_color,   label ='G')

        if leistungsdiagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Leistungen"
            self.scheinleistung = self.spannung_rlc_Uges * self.strom_rlc_Iges
            self.wirkleistung = self.scheinleistung.real
            self.blindleistung = self.scheinleistung.imag*1j

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,                        0,                                                  self.scheinleistung.real, self.scheinleistung.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,     color=self.arrow_1_color, label ='S')
            plt.arrow(0,                        0,                                                  self.wirkleistung.real, self.wirkleistung.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True,    color=self.arrow_2_color,  label ='P')
            plt.arrow(self.wirkleistung.real,   self.wirkleistung.imag,                             self.blindleistung.real,  self.blindleistung.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color=self.arrow_3_color, label ='Q')


    def zeigerdiagramm_erstellen(self):

        # Fenstergröße
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(self.fenster_groesse_x, self.fenster_groesse_y))

        # Move left y-axis and bottim x-axis to centre, passing through (0,0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Show ticks in the left and lower axes only
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')



        ax.set_xlabel('Re', fontsize=self.achse_x_name_groesse, fontweight='bold', loc='right')
        ax.set_ylabel('Im', fontsize=self.achse_y_name_groeese, fontweight='bold', loc='top', rotation=0)


        #ax.xaxis.set_label_coords(1.1)
        #ax.yaxis.set_label_coords(0, 1.05)
        # ax.set_ylim(-skalierung,skalierung)
        # ax.set_xlim(-skalierung,skalierung)

        # ax.set_aspect(1)
        ax.minorticks_on()

        ax.grid(True, which='both', lw=0.25)
        #ax.grid(color='b')
        plt.tick_params(
            axis='both',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=True,  # ticks along the bottom edge are off
            top=True,  # ticks along the top edge are off
            # labelbottom=False,
            # labeltop=False,
            # labelleft=False,
            # labelright=False)
            labelsize= self.achsen_beschriftung_groesse)

        if self.diagramm_typ.lower() == "serienschaltung: rl":
            Zeigerdiagramme.serienschaltung_R_L(self, self.spannungsdiagramm_check, self.impedanz_diagramm_check, self.admittanz_diagramm_check, self.leistungsdiagramm_check,  self.spannung_ges, self.widerstand, self.induktivitaet, self.kapazitaet, self.frequenz, fig)


        if self.diagramm_typ.lower() == "serienschaltung: rc":
            Zeigerdiagramme.serienschaltung_R_C(self, self.spannungsdiagramm_check, self.impedanz_diagramm_check, self.admittanz_diagramm_check, self.leistungsdiagramm_check,  self.spannung_ges, self.widerstand, self.induktivitaet, self.kapazitaet, self.frequenz, fig)


        if self.diagramm_typ.lower() == "serienschaltung: rlc":
            Zeigerdiagramme.serienschaltung_R_L_C(self, self.spannungsdiagramm_check, self.impedanz_diagramm_check, self.admittanz_diagramm_check, self.leistungsdiagramm_check,  self.spannung_ges, self.widerstand, self.induktivitaet, self.kapazitaet, self.frequenz, fig)


        plt.legend(fontsize=8)

        fig.tight_layout()

        plt.show()

