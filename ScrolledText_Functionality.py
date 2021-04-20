
from tkinter import *


class Textformatierung:
    def __init__(self):
        self.listeners = []
        print("init textformatierung")

    def subscribe(self, listener):
        self.listeners.append(listener)

    def text_latex(self, description_main_entry):
        self.description_main_entry = description_main_entry

        self.description_main_entry.insert(SEL_FIRST, '\\(', 'RED')
        self.description_main_entry.insert(SEL_LAST, '\\)', 'RED')
        self.description_main_entry.tag_config('RED', foreground='red')

    def text_sub(self, description_main_entry):
        self.description_main_entry = description_main_entry

        self.description_main_entry.insert(SEL_FIRST, '_', 'SUB')
        self.description_main_entry.insert(SEL_LAST, ' ', 'SUB')
        self.description_main_entry.tag_add('SUB', SEL_FIRST, SEL_LAST)
        self.description_main_entry.tag_config('SUB', offset=-4)
        self.description_main_entry.tag_config('SUB', foreground='blue')

    def text_sup(self, description_main_entry):
        self.description_main_entry = description_main_entry

        self.description_main_entry.insert(SEL_FIRST, '^', 'SUP')
        self.description_main_entry.insert(SEL_LAST, ' ', 'SUP')
        self.description_main_entry.tag_add('SUP', SEL_FIRST, SEL_LAST)
        self.description_main_entry.tag_config('SUP', offset=4)
        self.description_main_entry.tag_config('SUP', foreground='green')

    def text_italic(self, description_main_entry):
        self.description_main_entry = description_main_entry

        self.description_main_entry.insert(SEL_FIRST, '//', 'ITALIC')
        self.description_main_entry.insert(SEL_LAST, '///', 'ITALIC')
        self.description_main_entry.tag_add('ITALIC', SEL_FIRST, SEL_LAST)
        self.description_main_entry.tag_config('ITALIC', font=('Helvetica', 9, 'italic'))
        #self.formula_question_entry.tag_config('ITALIC', foreground='green')
