import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
from helper_functions import ResultDict
import custom_irt as irt


class IliasDataPlotter:

    def __init__(self, filename, nr_questions=8):
        self.data = pd.read_excel(filename).dropna()
        self.nr_questions = nr_questions

    @property
    def questions(self):
        return self.data.iloc[:, -self.nr_questions:]

    def fix_question_length(self, question, maxlen=25):
        if len(question) > maxlen:
            return question[:(maxlen - 3)] + "..."
        else:
            return question

    def plot_used_time(self):
        minutes = [dp.minute + dp.second / 60 for dp in pd.to_datetime(self.data["Bearbeitungsdauer"])]
        sns.boxplot(pd.Series(minutes, name="Bearbeitungszeit in Minuten"), orient="v")

    def plot_result(self, min=0.0, max=10.0):
        results = self.data["Testergebnis in Punkten"]
        sns.distplot(results, kde=False)

    def plot_question_dists(self):
        question_df = self.questions
        fig, axes = plt.subplots(int(self.nr_questions/3) + 1, 3,
                                 figsize=(10, 10))
        plt.subplots_adjust(wspace=0.4, hspace=0.5)
        for i, question in enumerate(question_df):
            data = question_df[question]
            sns.distplot(data,
                         kde=False,
                         bins=np.arange(0, max(data)+2),
                         ax=axes[i % 3, int(i / 3)],
                         axlabel=False)
            axes[i % 3, int(i / 3)].set_title(self.fix_question_length(question))
        plt.show()


class ExamDataPlotter:

    def __init__(self, filename, max_points):
        cols = ["ZW 0", "ZW 1", "ZW 2", "", "P 0", "P 1", "P 2", "P 3"]
        self.data = pd.read_csv(filename, delimiter=";", skiprows=2, names=cols, header=0)
        self.max_points = max_points

    def boxplot(self, size=(12, 6), color=None):
        plt.figure(figsize=size)
        sns.boxplot(data=self.data, palette=color)
        plt.ylabel("Klausurpunkte")
        plt.xlabel("Anzahl absolvierter Zwischenleistungen")

    def violinplot(self, size=(12, 6), color=None):
        plt.figure(figsize=size)
        sns.violinplot(data=self.data, palette=color)
        plt.ylabel("Klausurpunkte")
        plt.xlabel("Anzahl absolvierter Zwischenleistungen")

        
class IliasParser:

    def __init__(self, filename):
        non_question_cols = 19  # Anzahl der Spalten in der Ausgabedatei ohne Fragen!
        self.df_dict = pd.read_excel(filename, sheet_name=None)
        self.nr_questions = len(self.df_dict["Testergebnisse"].keys()) - non_question_cols

    @property
    def test_results(self):
        # Im folgenden werde fehlende Werte ergänzt, dafür werden unterschiedliche Methoden je nach Spalte benötigt!
        df_full = self.df_dict["Testergebnisse"].fillna(value=0)
        df_statistics = self.df_dict["Testergebnisse"].loc[:, :"Durchlauf"].fillna(method="ffill")
        df_full.update(df_statistics, overwrite=True)
        return df_full.set_index("Name")

    def _get_correct_entry(self, df, name):
        # Kleine Hilfsfunktion da teilweise mehr als eine Zeile pro Person verarbeitet werden muss
        final_rating_row = df.loc[name]["Bewerteter Durchlauf"]
        if type(final_rating_row) is pd.Series:
            boolean_comprehension = df.loc[name]["Durchlauf"] == final_rating_row[0]
            return df.loc[name][boolean_comprehension].iloc[0]
        else:
            return df.loc[name]

    def _unique_test_results(self):
        # Die Funktion wählt die korrekte Spalte im Übersichtstabellenblatt aus.
        # ILIAS erzeugt Leerzeilen, wenn eine Person mehrere Testdurchläufe durchführt
        unique_df = {}
        df = self.test_results
        for name in df.index:
            if name in unique_df:
                continue
            unique_df[name] = self._get_correct_entry(df, name)
        return pd.DataFrame(unique_df).T

    def _answers_per_sheet(self):
        answer_sheets = list(self.df_dict.keys())[1:]
        for i, name in enumerate(answer_sheets):
            df = self.df_dict[name]
            df.columns = ["Question", "Answer"]
            df = df.set_index("Question")
            df.to_csv(f"./answer_sheets/{i}.csv")

    def _answers_single_sheet(self):
        df = self.df_dict["Auswertung für alle Benutzer"]
        df.columns = ["Question", "Answer"]
        user = {}
        j = 0
        for i, line in tqdm(df.iterrows()):
            user[i] = line
            if type(line["Question"]) is str:
                if "Ergebnisse von Testdurchlauf" in line["Question"]:
                    user = pd.DataFrame(user).T.iloc[:-1]
                    user.reset_index(drop=True, inplace=True)
                    user.to_csv(f"./answer_sheets/{j}.csv")
                    j += 1
                    user = {}

    def _create_answer_log(self):
        if not "answer_sheets" in os.listdir():
            os.makedirs("./answer_sheets/")
        if "Auswertung für alle Benutzer" in self.df_dict.keys():
            self._answers_single_sheet()
        else:
            self._answers_per_sheet()

    def _create_results_dict(self):
        dir = "./answer_sheets/"
        results = os.listdir(dir)
        result_dict = ResultDict()
        unique_id = 0
        for (student_id, file) in tqdm(enumerate(results)):
            table = pd.read_csv(dir + file, index_col=0)
            for row in table.iterrows():
                if row[1].Question is np.nan and row[1].Answer is np.nan:
                    # deletes empty rows from file and skips loop execution
                    continue
                if row[1].Question in ("Formelfrage", "Single Choice", "Multiple Choice"):
                    # identifies current question
                    current_question = row[1].Answer
                    unique_id = 0  # the unique id helps, if ilias is not returning any variables as question name
                    continue
                result_dict.append(current_question, row[1], unique_id, student_id)
                unique_id += 1
        result_dict.save()

    def export(self, name):
        df = self._unique_test_results()
        self._create_answer_log()
        df.to_csv(f"{name}.csv")
        print(f"Test results saved as {name}.csv!")

    def export_anon(self, name):
        df = self._unique_test_results()
        self._create_answer_log()
        df.reset_index(drop=True, inplace=True)
        df["Benutzername"] = range(len(df))
        df["Matrikelnummer"] = range(len(df))
        df.to_csv(f"{name}.csv")
        print(f"Anonymous test results saved as {name}.csv!")


class PaperDataPlotter:

    def __init__(self, filename):
        self.df_dict = pd.read_excel(filename, sheet_name=None)
        self.keys = list(self.df_dict.keys())
        self.max_points = [41, 43, 50, 40, 40, 40]
        self.font_size = 2
        self.color = "Blues"
        self.size = (24, 12)

        for key in self.df_dict:
            self.df_dict[key].drop(self.df_dict[key].index[0:3], inplace=True)
            self.df_dict[key].columns = self.df_dict[key].iloc[0]
            self.df_dict[key].drop(self.df_dict[key].index[0], inplace=True)

    def boxplot(self, key=0):
        sns.set(font_scale=self.font_size)
        plt.figure(figsize=self.size)
        data = self.df_dict[self.keys[key]] / self.max_points[key]
        data.columns = data.columns.fillna(value="")
        ax = sns.boxplot(data=data, palette=self.color)
        nobs = self.df_dict[self.keys[key]].count(axis=0)
        median = data.median(axis=0)
        pos = range(len(nobs))
        half = len(nobs)/2
        for tick, label in zip(pos, ax.get_xticklabels()):
            if tick > half:
                col = "w"
            else:
                col = "k"
            ax.text(pos[tick], median[tick] + 0.005, f"n={nobs[tick]}",
                    horizontalalignment='center', size='x-small', color=col, weight='semibold')
        ax.set(ylim=(0, 1))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
        ax.text(pos[0], 0.95, "Zwischentests",
                    horizontalalignment='left', size='large', color='k', weight='semibold')
        ax.text(pos[10], 0.95, "Praktika",
                    horizontalalignment='left', size='large', color='k', weight='semibold')
        plt.ylabel("Erreichte relative Klausurpunktzahl")
        plt.xlabel("Anzahl absolvierter Zwischenleistungen")

    def boxplot_p(self, key=4):
        sns.set(font_scale=self.font_size)
        plt.figure(figsize=self.size)
        data = self.df_dict[self.keys[key]]
        data.columns = data.columns.fillna(value="")
        ax = sns.boxplot(data=data, palette=self.color)
        nobs = self.df_dict[self.keys[key]].count(axis=0)
        median = data.median(axis=0)
        pos = range(len(nobs))
        half = len(nobs)/2
        for tick, label in zip(pos, ax.get_xticklabels()):
            if tick > half:
                col = "w"
            else:
                col = "k"
            ax.text(pos[tick], median[tick] + 0.005, f"n={nobs[tick]}",
                    horizontalalignment='center', size='x-small', color=col, weight='semibold')
        ax.set(ylim=(0, 1))
        ax.text(pos[0], 0.95, "Praktika",
                    horizontalalignment='left', size='large', color='k', weight='semibold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
        plt.ylabel("Erreichte relative Klausurpunktzahl")
        plt.xlabel("Anzahl absolvierter Praktika")

    def boxplot_bp(self, key=4):
        sns.set(font_scale=self.font_size)
        plt.figure(figsize=self.size)
        data = self.df_dict[self.keys[key]]
        data.columns = data.columns.fillna(value="")
        ax = sns.boxplot(data=data, palette=self.color)
        nobs = self.df_dict[self.keys[key]].count(axis=0)
        median = data.median(axis=0)
        pos = range(len(nobs))
        half = len(nobs)/2
        for tick, label in zip(pos, ax.get_xticklabels()):
            if tick > half:
                col = "w"
            else:
                col = "k"
            ax.text(pos[tick], median[tick] + 0.005, f"n={nobs[tick]}",
                    horizontalalignment='center', size='x-small', color=col, weight='semibold')
        ax.set(ylim=(0, 1))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
        ax.text(pos[0], 0.95, "Bonuspunkte",
                    horizontalalignment='left', size='large', color='k', weight='semibold')
        plt.ylabel("Erreichte relative Klausurpunktzahl")
        plt.xlabel("Anzahl erreichter Bonuspunkte")


class IRT_Plotter:

    def __init__(self, filename):
        self.data = pd.read_excel(filename)
        self._learn()

    def _learn(self):
        print("Berechnung der IRT-Variablen gestartet, dieser Prozess kann einige Minuten in Anspruch nehmen!")
        self.thetas, abcd = irt.estimate_thetas(self.data, verbose=True)
        self.abcd = pd.DataFrame(abcd)
        self.abcd.columns = ["a", "b", "c", "d"]
        self.abcd.index = self.data.columns
        print("Berechnung der IRT-Variablen abgeschlossen!")

    def _4pl_model(self, x, abcd):
        return abcd["c"]*((abcd["a"]-abcd["d"])/(self._complex((float(x - abcd["d"]) - 1) ** float(1/abcd["b"]))))
        #return abcd["d"] + (abcd["a"] - abcd["d"]) / (1 + self._complex(x / abcd["c"]))**abcd["b"]

    def _complex(self, c):
        dir = 1
        if c.real < 0:
            dir = -1
        return np.sqrt(c.real**2 + c.imag**2) * dir

    def show_thetas(self):
        sns.set(font_scale=1.5)
        plt.figure(figsize=(10, 5))
        plt.plot(np.sort(np.squeeze(self.thetas)))

    def show_a(self):
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        self.abcd["a"].plot.bar()

    def show_b(self):
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        self.abcd["b"].plot.bar()

    def show_c(self):
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        self.abcd["c"].plot.bar()

    def show_d(self):
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        self.abcd["d"].plot.bar()

    def show_model_curve(self, exercise):
        xs = np.arange(0, 1.1, 0.1)
        abcd = self.abcd.loc[exercise]
        y = []
        for x in xs:
            y.append(self._4pl_model(x, abcd))
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        pd.DataFrame(y, xs).plot()
        plt.show()

    def show_model_curve2(self, exercise):
        xs = np.arange(0, 1.1, 0.1)
        abcd = self.abcd.loc[exercise]
        y = []
        for x in xs:
            y.append(self._4pl_model(x, abcd))
        sns.set(font_scale=1.5)
        plt.figure(figsize=(14, 7))
        pd.DataFrame(y, xs).plot(xlim=(0, 1), ylim=(0, 1))
        plt.show()

    def show_all_models(self):
        exercises = list(self.data.columns)
        for e in exercises:
            self.show_model_curve2(e)



if __name__ == "__main__":
    #ilias = IliasParser("Zwischentest_3__Wasserkocher_results.xlsx")
    #df = ilias._unique_test_results()
    #ilias.export_anon("fn")
    #self = ilias  # für einfacheres debugging ^^'
    e = IRT_Plotter("Klausur.xlsx")
    #e.show_model_curve("1a")
    self=e
