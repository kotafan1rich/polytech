import customtkinter as ctk
import json as js
import threading as th
import time
from ai.api import api
from sys import exit

slang = js.load(open("translate.json", "r", encoding="utf-8"))


def GetDefinition(input, model):
    return api(input, model)


class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("750x500")
        self.window.title("Slang Translator")

        self.processed = ctk.IntVar(value=0)

        self.ConfigureGrid()
        self.CreateUI()
        self.GridUI()

        self.window.bind("<Return>", self.enterPressed)
        self.window.mainloop()
        exit()

    def ConfigureGrid(self):
        self.window.columnconfigure(index=0, weight=1, uniform="a")
        self.window.columnconfigure(index=1, weight=2, uniform="a")
        self.window.columnconfigure(index=2, weight=2, uniform="a")
        self.window.columnconfigure(index=3, weight=1, uniform="a")

        self.window.rowconfigure(index=0, weight=2, uniform="a")
        self.window.rowconfigure(index=1, weight=1, uniform="a")
        self.window.rowconfigure(index=2, weight=1, uniform="a")
        self.window.rowconfigure(index=3, weight=1, uniform="a")
        self.window.rowconfigure(index=4, weight=3, uniform="a")
        self.window.rowconfigure(index=5, weight=1, uniform="a")
        self.window.rowconfigure(index=6, weight=1, uniform="a")

    def CreateUI(self):
        self.name = ctk.CTkLabel(
            master=self.window, text="Переводчик Слэнга", font=("Arial", 40)
        )
        self.inputField = ctk.CTkEntry(
            master=self.window, font=("Arial", 40), corner_radius=20
        )
        self.output = ctk.CTkLabel(master=self.window, text="", font=("Arial", 20))
        self.output = ctk.CTkLabel(master=self.window, text="", font=("Arial", 20))
        self.confButton = ctk.CTkButton(
            master=self.window,
            text="ПЕРЕВЕСТИ",
            command=self.Click,
            fg_color="#000000",
            corner_radius=20,
            font=("Arial", 25),
            hover_color="#AAAAAA",
        )
        self.modelOption = ctk.CTkOptionMenu(master=self.window, values=["Z", "O", "ZHATCBT"])
        self.optionName = ctk.CTkLabel(master=self.window, text="Доступные модели: ", font=("Arial", 20))
        self.radioText = ctk.CTkRadioButton(master=self.window, variable=self.processed, value=0, text="Слово")
        self.radioSentence = ctk.CTkRadioButton(master=self.window, variable=self.processed, value=1, text="Предложение")
        self.vScroll = ctk.CTkScrollbar(master=self.window, orientation="vertical")

    def GridUI(self):
        self.name.grid(row=0, column=1, sticky="nsew", columnspan=2)
        self.inputField.grid(row=1, column=1, sticky="nsew", columnspan=2)
        self.optionName.grid(row=2, column=1, sticky="nsew")
        self.modelOption.grid(row=2, column=2, sticky="we")
        self.radioText.grid(row=3, column=1, sticky="nsew")
        self.radioSentence.grid(row=3, column=2, sticky="nsew")
        self.output.grid(row=4, column=1, sticky="nsew", columnspan=2)
        self.confButton.grid(row=5, column=1, sticky="nsew", columnspan=2)

    def Click(self):
        t = th.Thread(target=self.Processing)
        t.daemon = True
        t.start()
    
    def LoadingStatus(self):
        self.isLoading = True
        self.output.configure(font=("Arial", 40))
        while self.isLoading:
            self.output.configure(text="Загрузка.")
            time.sleep(0.5)
            if not self.isLoading:
                break
            self.output.configure(text="Загрузка..")
            time.sleep(0.5)
            if not self.isLoading:
                break
            self.output.configure(text="Загрузка...")
            time.sleep(0.5)

    def Processing(self):
        value = self.inputField.get().lower().strip()
        if value == "":
            return 0
        p = th.Thread(target=self.LoadingStatus)
        p.daemon = True
        p.start()
        self.output.configure(text="")
        if self.processed == 0:
            if value not in slang.keys():
                out = GetDefinition(value, self.modelOption.get())
            else:
                out = slang[value]
            if len(out) <= 22:
                self.output.configure(font=("Arial", 40))
            elif len(out) <= 29:
                self.output.configure(font=("Arial", 30))
            else:
                self.output.configure(font=("Arial", 20))
            self.isLoading = False
            self.output.configure(text=out.capitalize()[:45])
        else:
            ...

    def enterPressed(self, event):
        self.Click()


app = App()
