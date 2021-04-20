from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
#import tkFileDialog
from tkinter.scrolledtext import ScrolledText
from Time_input_UI import Test_Time_UI

from PIL import Image, ImageTk

class Pictures():
    def __init__(self, Var, VarDict, Frame, Number, bg_color, label_color, button_color, fg_color, Label_Font, Entry_Font):
        self.Label_Font = Label_Font
        self.Entry_Font = Entry_Font
        self.bg_color = bg_color
        self.button_color = button_color
        self.label_color = label_color
        self.fg_color = fg_color
        self.frame = Frame
        self.Var = Var
        self.VarDict =VarDict
        self.Number = Number
        self.image = None


        self.ImageIndex = self.VarDict["description_img_data_{}".format(Number)]
        self.NameIndex = self.VarDict["description_img_name_{}".format(Number)]
        self.path = self.Var[self.ImageIndex][0].get()
        print("das ist der pfad", self.path)


        #self.image = self.Var[self.ImageIndex][0].get()
        self.Name = self.Var[self.NameIndex][0].get()

        self.Interaction_btn = Button(Frame, bg=self.button_color, fg=self.fg_color)
        self.Interaction_btn['font'] = self.Entry_Font
        self.Interaction_btn.place(relx=0, rely=0, relwidth=.3, relheight=1)

        self.name_lbl = Label(Frame, bg=self.label_color, fg=self.fg_color)
        self.name_lbl['font'] = self.Label_Font
        self.name_lbl.place(relx=.3, rely=0, relwidth=.7, relheight=1)

        self.name_lbl.configure(text=self.Var[self.ImageIndex][0].get())
        self.update_btn()

        self.name_lbl.bind('<Double-Button-1>', self.show_picture)

        if len(self.path) >= 1:
            print("test test", self.Var[self.ImageIndex][0].get())
            self.add_picture()
            # self.image = Image.open(self.Var[self.ImageIndex][0].get()) #öffnet original bild
            # self.image0 = ImageTk.PhotoImage(self.image)

    def delete_picture(self):
        self.path = ""
        self.Var[self.ImageIndex][0].set("")
        self.update_btn()

    def update_btn(self):
        if len(self.path) < 1:
            self.Interaction_btn.configure(text="Hinzufügen", command=self.choose_picture)
            self.name_lbl.configure(text=self.Var[self.ImageIndex][0].get())
            print("kein Bild vorhanden")
        else:
            self.Interaction_btn.configure(text="Löschen", command=self.delete_picture)
            self.name_lbl.configure(text=self.give_name(self.Var[self.ImageIndex][0].get()))
            print("Bild vorhanden")

    def give_name(self, path):

        print("path vorher", path)
        while path.find('/'):
            tobereplaced = path[0:path.find('/')]
            path = path.replace(tobereplaced, '1')
            print("path nachher", path)

        return path

    def add_picture(self):
        self.path = self.Var[self.ImageIndex][0].get()
        print(self.path)
        if len(self.path) > 1:
            # open image
            self.original = Image.open(self.path)
            self.name_lbl.configure(text=self.path)

            # get image size
            width, height = self.original.size
            # resize image
            scaling_factor = 200 / height
            new_height = int(scaling_factor * height)
            new_widht = int(scaling_factor * width)

            self.resized = self.original.resize((new_widht, new_height), Image.ANTIALIAS)
            self.image0 = ImageTk.PhotoImage(self.resized)
            #self.Var[self.NameIndex][0].set(self.image0)


            #self.Var[self.ImageIndex][0].set(ImageTk.PhotoImage(self.resized))

        self.update_btn()
    def choose_picture(self):
        self.file = filedialog.askopenfile(parent=self.frame, mode='rb', title='Choose a file')
        if self.file != None:
            self.Var[self.ImageIndex][0].set(self.file.name)  # Pfad wird in DB zwischenspeicher gelegt
            self.path = self.file.name
            print(self.file.name)
            data = self.file.read()
            self.file.close()
            print("I got %d bytes from this file." % len(data))
        self.add_picture()

    def chose_picture_from_explorer(self):
        self.file = filedialog.askopenfile(parent=self.frame, mode='rb', title='Choose a file')
        if self.file != None:
            data = self.file.read()
            self.file.close()
            print("I got %d bytes from this file." % len(data))
        self.add_picture()

    def show_picture(self, e):
        work_window = Toplevel()

        self.Image_Label = Label(work_window, image=self.image0)
        self.Image_Label.place(relwidth=1, relheight=1, relx=0, rely=0)

class picture_choice():
    def __init__(self, Var,  Frame, bg_color="#4cc9f0", label_color='#3a0ca3', button_color='#3f37c9', fg_color="#4cc9f0"):
        self.Label_Font = font.Font(family='Verdana', size=10, weight='bold')
        self.Entry_Font = font.Font(family='Verdana', size=10, weight='normal')
        self.bg_color = bg_color
        self.button_color = button_color
        self.label_color = label_color
        self.fg_color = fg_color
        self.frame = Frame
        self.Var = Var


        self.image = None


        #self.ImageIndex = self.VarDict["description_img_data_{}".format(Number)]
        #self.NameIndex = self.VarDict["description_img_name_{}".format(Number)]
        self.path = self.Var.get()
        print("das ist der pfad", self.path)


        #self.image = self.Var[self.ImageIndex][0].get()
        #self.Name = self.Var[0].get()

        self.Interaction_btn = Button(Frame, bg=self.button_color, fg=self.fg_color)
        self.Interaction_btn['font'] = self.Entry_Font
        self.Interaction_btn.place(relx=0, rely=0, relwidth=.3, relheight=1)

        self.name_lbl = Label(Frame, bg=self.label_color, fg=self.fg_color)
        self.name_lbl['font'] = self.Label_Font
        self.name_lbl.place(relx=.3, rely=0, relwidth=.7, relheight=1)

        self.name_lbl.configure(text=self.Var.get())
        self.update_btn()

        self.name_lbl.bind('<Double-Button-1>', self.show_picture)

        if len(self.path) >= 1:
            print("test test", self.Var.get())
            self.add_picture()
            # self.image = Image.open(self.Var[self.ImageIndex][0].get()) #öffnet original bild
            # self.image0 = ImageTk.PhotoImage(self.image)

    def delete_picture(self):
        print("Pfad {} wird gelöscht".format(self.Var.get()))
        self.Var.set("")
        self.path = self.Var.get()
        print(" 2 Pfad {} wird gelöscht".format(self.Var.get()))
        self.update_btn()

    def update_btn(self):


        if len(self.path) < 1:
            self.Interaction_btn.configure(text="Add Picture", command=self.choose_picture)
            self.name_lbl.configure(text=self.Var.get())
            print("kein Bild vorhanden")
        else:
            self.Interaction_btn.configure(text="delete picture", command=self.delete_picture)
            self.name_lbl.configure(text=self.Var.get())
            print("ein Bild vorhanden")

    def add_picture(self):
        self.path = self.Var.get()
        print(self.path)
        if len(self.path) > 1:
            # open image
            self.original = Image.open(self.path)
            self.name_lbl.configure(text=self.path)

            # get image size
            width, height = self.original.size
            # resize image
            scaling_factor = 200 / height
            new_height = int(scaling_factor * height)
            new_widht = int(scaling_factor * width)

            self.resized = self.original.resize((new_widht, new_height), Image.ANTIALIAS)
            self.image0 = ImageTk.PhotoImage(self.resized)
            #self.Var[self.NameIndex][0].set(self.image0)


            #self.Var[self.ImageIndex][0].set(ImageTk.PhotoImage(self.resized))

        self.update_btn()

    def choose_picture(self):
        self.file = filedialog.askopenfile(parent=self.frame, mode='rb', title='Choose a file')
        if self.file != None:
            self.Var.set(self.file.name)  # Pfad wird in DB zwischenspeicher gelegt
            self.path = self.file.name
            print(self.file.name)
            data = self.file.read()
            self.file.close()
            print("I got %d bytes from this file." % len(data))
        self.add_picture()

    def chose_picture_from_explorer(self):
        self.file = filedialog.askopenfile(parent=self.frame, mode='rb', title='Choose a file')
        if self.file != None:
            data = self.file.read()
            self.file.close()
            print("I got %d bytes from this file." % len(data))
        self.add_picture()

    def show_picture(self, e):
        work_window = Toplevel()

        self.Image_Label = Label(work_window, image=self.image0)
        self.Image_Label.place(relwidth=1, relheight=1, relx=0, rely=0)

    def configure(self, state):
        state = state