import tkinter as tk
from threadManager import ThreadManager
from tkinter import filedialog
from math import ceil
from ExcelManager import ExcelManager

PRIMARY_COLOR = "#0D66B0"
SECONDARY_COLOR = "#e1e9f7"
LIGHT_BLUE = "#a6bcde"
SUN_YELLOW = "#E3A417"
IVORY = "#F9E499"
TEXT_MAIN_COLOR = "#ffffff"
FONT_TITLE = ("helvetica","26","bold")
FONT = ("helvetica","14")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master["bg"] = PRIMARY_COLOR
        self.master.bind("<Return>", self.process)
        self.pack(fill="both")
        self.create_header()
        self.create_survey()
        self.create_result_area()
        self.create_footer()

    def create_header(self):
        self.header = tk.Frame(self)
        self.header["bg"] = TEXT_MAIN_COLOR
        self.inc_name = tk.Label(self.header)
        self.inc_name["text"] = "INCORPORATION"
        self.inc_name["fg"] = PRIMARY_COLOR
        self.inc_name["bg"] = TEXT_MAIN_COLOR
        self.inc_name["font"] = FONT_TITLE
        self.inc_name["height"] = 2
        self.inc_name.pack(side="left",padx=15)
        self.menu = tk.Button(self.header)
        try:
            check_if_path_saved = open("preference.txt","r")
        except:
            check_if_path_saved = open("preference.txt","w+")
        path_saved = check_if_path_saved.read()
        check_if_path_saved.close()
        if path_saved:
            self.menu["text"] = "Changer de fichier excel"
            self.menu["bg"] = LIGHT_BLUE
            self.filename = path_saved
        else:
            self.menu["text"] = "Veuillez charger un fichier excel"
            self.menu["bg"] = SUN_YELLOW
        self.menu["font"] = FONT
        self.menu["fg"] = TEXT_MAIN_COLOR
        self.menu["command"] = self.browse_file
        self.menu.pack(side="right",padx=15)
        self.header.pack(fill="x",expand="yes",pady=(0,100))

    def create_survey(self):
        self.entries = []
        self.create_survey_module("Nombre de pièces par boite:")
        self.entries[0].insert(0,"500")
        self.create_survey_module("Numéro d'OF:")

        self.confirm_button = tk.Button(self)
        self.confirm_button["text"] = "Confirmer"
        self.confirm_button["command"] = self.process
        self.confirm_button.pack(pady=(25,0))

    def create_survey_module(self, textArg):
        self.text_part = tk.Label(self)
        self.text_part["text"] = textArg
        self.text_part["font"] = FONT
        self.text_part["bg"] = PRIMARY_COLOR
        self.text_part["fg"] = TEXT_MAIN_COLOR
        self.text_part["height"] = 3
        self.text_part.pack()

        self.field_part = tk.Entry(self)
        self.field_part["bg"] = SECONDARY_COLOR
        self.field_part["bd"] = 2
        self.field_part.pack()
        self.entries.append(self.field_part)

    def create_footer(self):
        self.footer = tk.Label(self)
        self.footer["text"] = "Temps d'exécution :"
        self.footer["fg"] = TEXT_MAIN_COLOR
        self.footer["bg"] = PRIMARY_COLOR
        self.footer["font"] = ("helvetica", 6)
        self.footer.pack(side="bottom",pady=(100,0))

    def process(self,event=0):
        self.part_per_box = int(self.entries[0].get())
        self.of = self.entries[1].get()
        try:
            self.thread1 = ThreadManager(self.filename, self.of)
            self.thread1.start()
            self.dynamic_text.configure(text = "Chargement ...",fg = IVORY)
            self.confirm_button.configure(state = "disabled")
            self.after(80,self.is_process_terminated)
        except:
            self.dynamic_text.configure(text = "Veuillez sélectionner un fichier excel", fg = SUN_YELLOW)

    def is_process_terminated(self):
        if(self.thread1.is_alive()):
            self.after(80, self.is_process_terminated)
        else:
            self.compteur = self.thread1.get_compteur()
            executionTime = self.thread1.get_execution_time()
            if self.part_per_box > 0:
                if self.compteur > self.part_per_box:
                    self.compteur = ceil(self.compteur / self.part_per_box)
                else:
                    self.compteur = 0
                self.dynamic_text.configure(text = self.compteur, fg = TEXT_MAIN_COLOR)
            else:
                self.dynamic_text.configure(text = "Nombre de pièces par boite incorrect", fg = SUN_YELLOW)
            self.footer.configure(text= "Temps d'exécution : %.3f s" % executionTime)
            self.confirm_button.configure(state = "active")



    def create_result_area(self):
        self.static_text = tk.Label(self)
        self.static_text["text"] = "Nombre de boites:"
        self.static_text["bg"] = PRIMARY_COLOR
        self.static_text["fg"] = TEXT_MAIN_COLOR
        self.static_text["font"] = FONT
        self.static_text["height"] = 3
        self.static_text.pack(pady=(75,0))

        self.dynamic_text = tk.Label(self)
        self.dynamic_text["text"] = "XXX"
        self.dynamic_text["bg"] = PRIMARY_COLOR
        self.dynamic_text["fg"] = TEXT_MAIN_COLOR
        self.dynamic_text["font"] = FONT
        self.dynamic_text.pack()
    
    def browse_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes = (("Xlsx files","*.xlsx*"),("all files","*.*")))
        savedFile = open("preference.txt","w")
        savedFile.write(self.filename)
        savedFile.close()
        self.menu.configure(text="Changer de fichier excel")
        self.menu.configure(bg = LIGHT_BLUE)

root = tk.Tk()
app = Application(master=root)
app.master.minsize(600,800)
app.master.title("Multitech: Tri")
app.master.iconbitmap("box-icone.ico")
app.configure(bg=PRIMARY_COLOR)
app.mainl