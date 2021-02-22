import math
import numpy as np
import matplotlib.pyplot as plt


class Zeigerdiagramme:
    def __init__(self, diagramm_typ, spannungsdiagramm_check, impedanz_diagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz):


        self.diagramm_typ = diagramm_typ
        self.spannungsdiagramm_check = spannungsdiagramm_check
        self.impedanz_diagramm_check = impedanz_diagramm_check

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


        self.zeiger_linien_dicke = 4
        self.zeiger_kopf_dicke = 0.7
        self.zeiger_kopf_laenge = 0.9

        #####
        self.spannung_ges = 5+5j
        self.widerstand = 5
        self.induktivitaet = 1e-3
        self.kapazitaet = 10e-6
        self.frequenz = 1000


        Zeigerdiagramme.zeigerdiagramm_erstellen(self)


    def serienschaltung_R_L(self, impedanz_diagramm_check, widerstand, induktivitaet, frequenz):
        self.widerstand = widerstand
        self.induktivitaet = induktivitaet


        if impedanz_diagramm_check == '1':

            # Zeiger: Impedanzen
            self.impedanz_X_L = 1j * 2 * math.pi * frequenz * induktivitaet
            self.impedanz_Zges = self.widerstand + self.impedanz_X_L
            phase_impedanz_Zges = np.angle(self.impedanz_Zges, deg=True)


    def serienschaltung_R_C(self, widerstand, kapazitaet, frequenz, spannung, fig):
        self.spannung_rc_Uges = spannung
        self.impedanz_rc_R = widerstand


        self.impedanz_rc_R = 500
        kapazitaet = 100e-6
        frequenz = 1000
        self.spannung_rc_Uges = 10

        self.zeigerdiagramm_typ_titel = "Serienschaltung RC - Spannungen"

        self.impedanz_rc_X_C = -1j / (2 * math.pi * frequenz * kapazitaet)
        self.impedanz_rc_Zges = self.impedanz_rc_R + self.impedanz_rc_X_C

        self.strom_rc_Iges = self.spannung_rc_Uges / (self.impedanz_rc_Zges)

        self.spannung_rc_U_R = self.strom_rc_Iges * self.impedanz_rc_R
        self.spannung_rc_U_C = self.strom_rc_Iges * self.impedanz_rc_X_C

        #phase_impedanz_Zges = np.angle(self.impedanz_Zges, deg=True)

        fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
        plt.arrow(0,     0,      self.spannung_rc_Uges.real, self.spannung_rc_Uges.imag,     length_includes_head=True,  color ='black', label ='Uges', alpha=0.7)
        plt.arrow(0,     0,      self.spannung_rc_U_R.real, self.spannung_rc_U_R.imag,        length_includes_head=True, color ='blue',  label ='U_R', alpha=0.7)
        plt.arrow(0,     0,      self.spannung_rc_U_C.real, self.spannung_rc_U_C.imag,         length_includes_head=True,  color ='green', label ='U_C', alpha=0.7)
        plt.arrow(0,     0,      self.strom_rc_Iges.real, self.strom_rc_Iges.imag,         length_includes_head=True,  color ='red', label ='Iges', alpha=0.7)



    def serienschaltung_R_L_C(self, impedanz_diagramm_check, spannungsdiagramm_check, spannung_ges, widerstand, induktivitaet, kapazitaet, frequenz, fig):
        
        
        self.spannung_rlc_Uges =spannung_ges
        self.widerstand = float(widerstand)
        self.induktivitaet = float(induktivitaet)
        self.kapazitaet = float(kapazitaet)
        self.frequenz = float(frequenz)

        print(self.widerstand)
        print(self.induktivitaet)
        print(self.kapazitaet)
        print(self.frequenz)

        #self.widerstand = 5
        #self.induktivitaet = 1e-3
        #self.kapazitaet = 1e-6
        #self.frequenz = 1000

        self.impedanz_R = self.widerstand
        self.impedanz_X_L = 1j * 2 * math.pi * self.frequenz * self.induktivitaet
        self.impedanz_X_C = -1j / (2 * math.pi * self.frequenz * self.kapazitaet)
        self.impedanz_Zges = self.widerstand + self.impedanz_X_L + self.impedanz_X_C

        print(impedanz_diagramm_check, widerstand, induktivitaet, kapazitaet, frequenz)

        if impedanz_diagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Impedanzen"
            # Zeiger: Impedanzen


            phase_impedanz_Zges = np.angle(self.impedanz_Zges, deg=True)

            print(self.impedanz_Zges, self.impedanz_X_L, self.impedanz_X_C)

            return self.impedanz_Zges,self.impedanz_R, self.impedanz_X_L, self.impedanz_X_C, self.zeigerdiagramm_typ_titel
        
        if spannungsdiagramm_check == 1:
            self.zeigerdiagramm_typ_titel = "Serienschaltung RLC - Spannungen"
            # Zeiger: Spannungen


            self.strom_rlc_Iges = self.spannung_rlc_Uges / self.impedanz_Zges

            self.spannung_rlc_U_R = self.strom_rlc_Iges * self.widerstand
            phase_Iges = np.angle(self.strom_rlc_Iges, deg=True)
            self.spannung_rlc_U_L = self.strom_rlc_Iges * self.impedanz_X_L
            self.spannung_rlc_U_C = self.strom_rlc_Iges * self.impedanz_X_C

            print("RLC SPANNUNGEN")
            print(abs(self.spannung_rlc_U_R), abs(self.spannung_rlc_U_L), abs(self.spannung_rlc_U_C), abs(self.strom_rlc_Iges))
            print("phase: ", phase_Iges )
            print("##############")

            fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
            plt.arrow(0,   0,    self.spannung_rlc_U_R.real, self.spannung_rlc_U_R.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color ='black', label ='U_R', alpha=0.7)
            plt.arrow(0,   0,    self.spannung_rlc_U_L.real, self.spannung_rlc_U_L.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True, color ='blue',  label ='U_L', alpha=0.7)
            plt.arrow(0,   0,    self.spannung_rlc_U_C.real, self.spannung_rlc_U_C.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color ='green', label ='U_C', alpha=0.7)
            plt.arrow(0,   0,    self.strom_rlc_Iges.real, self.strom_rlc_Iges.imag,   linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color ='red',   label ='Iges', alpha=0.7)


            #return self.spannung_rlc_Uges, self.spannung_rlc_R, self.spannung_rlc_L, self.spannung_rlc_C, self.zeigerdiagramm_typ_titel

    def zeigerdiagramm_erstellen(self):

        #skalierungx = math.fabs(12)
        #skalierungy = math.fabs(12)

        # if Wirkleistung < 0:
        #     winkel_wirk = 180
        #     textx = - skalierungx * 0.08
        # else:
        #     winkel_wirk = 0
        #     textx = skalierungx * 0.08
        # if Blindleistung < 0:
        #     winkel_blind = 270
        #     texty = - skalierungx * 0.023
        # else:
        #     winkel_blind = 90
        #     texty = skalierungx * 0.023

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




        if self.diagramm_typ.lower() == "serienschaltung: rc":
            if self.spannungsdiagramm_check == 1:
                Zeigerdiagramme.serienschaltung_R_C(self, self.widerstand, self.kapazitaet, self.frequenz, self.spannung_ges, fig)



        if self.diagramm_typ.lower() == "serienschaltung: rlc":
            
            if self.impedanz_diagramm_check == 1:
                self.impedanz_Zges, self.impedanz_R, self.impedanz_X_L, self.impedanz_X_C, self.zeigerdiagramm_typ_titel = Zeigerdiagramme.serienschaltung_R_L_C(self, self.impedanz_diagramm_check, self.spannungsdiagramm_check, self.spannung_ges, self.widerstand, self.induktivitaet, self.kapazitaet, self.frequenz, fig)




                fig.suptitle(self.zeigerdiagramm_typ_titel, fontsize=16)
                plt.arrow(0,                        0,                                                  self.impedanz_Zges.real, self.impedanz_Zges.imag, linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color ='black', label ='Z')
                plt.arrow(0,                        0,                                                  self.impedanz_X_L.real, self.impedanz_X_L.imag,   linewidth=self.zeiger_linien_dicke,     length_includes_head=True, color ='blue',  label ='X_L')
                plt.arrow(self.impedanz_R.real,     (self.impedanz_R.imag+self.impedanz_X_L.imag),      self.impedanz_X_C.real, self.impedanz_X_C.imag,   linewidth=self.zeiger_linien_dicke,      length_includes_head=True,  color ='green', label ='X_C')
                plt.arrow(self.impedanz_X_L.real,   self.impedanz_X_L.imag,    self.impedanz_R,        0,                                                  linewidth=self.zeiger_linien_dicke,    length_includes_head=True,  color ='red',   label ='R')

            if self.spannungsdiagramm_check == 1:
                Zeigerdiagramme.serienschaltung_R_L_C(self, self.impedanz_diagramm_check, self.spannungsdiagramm_check, self.spannung_ges, self.widerstand, self.induktivitaet, self.kapazitaet, self.frequenz, fig)


        plt.legend(fontsize=8)

        fig.tight_layout()

        plt.show()

