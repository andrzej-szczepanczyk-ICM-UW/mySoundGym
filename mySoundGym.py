import customtkinter
import librosa
import soundfile
import numpy as np

import tkinter
import tkinter.messagebox
import customtkinter

import pydub

import librosa
import librosa.display
from playsound import playsound

from math import log10

import random

MODES = {
    "LEFT": "filtr dolno-przepustowy [Hz]",
    "RIGHT": "filtr górno-przepustowy [Hz]",
    "FREQ": "Wzmocnienie częstotliwości [Hz]",
    "AMPLI":  "wzmocnienie dźwięku [dB]"
}

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def myNorm(x):
    return np.exp(-x*x)


def raw2dB(rawval):
    dB = 8*rawVal-4
    return dB


def raw2Hz(rawval):
    logHz = 4*rawval+1
    Hz = 10**logHz
    return Hz




class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("my own implementation of SoundGym")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ variables ============
        self.targetRawValue = random.random()
        self.guessedRawValue = 0.5
        self.numExercise = 0
        self.MAXNUMEXERCISES = 5

        # ============ create 3 frames ============

        # configure grid layout (1x2)
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_upper = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_upper.grid(row=0, column=0, columnspan=2, sticky="nswe")

        self.frame_down = customtkinter.CTkFrame(master=self)
        self.frame_down.grid(row=1, column=0, sticky="nswe", padx=5, pady=5)
        self.frame_down_right = customtkinter.CTkFrame(master=self)
        self.frame_down_right.grid(row=1, column=1, sticky="nswe", padx=5, pady=5)

        # ============ frame_upper ============

        # configure grid layout (1x11)
        self.frame_upper.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_upper.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_upper.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_upper.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
        self.frame_upper.grid_rowconfigure(15, minsize=10)  # empty row with minsize as spacing

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_upper,  width=120,
                                                    values=[MODES["FREQ"]])
        self.combobox_1.grid(row=0, column=0, columnspan=3, pady=10, padx=20, sticky="we")

        # ============ frame_down ============

        self.botton_originalSound = customtkinter.CTkButton(master=self.frame_down,
                                                text="Oryginał",
                                                command=self.originalSound_event)
        self.botton_originalSound.grid(row=1, column=0, pady=10, padx=20)


        self.botton_modifiedSound = customtkinter.CTkButton(master=self.frame_down,
                                                text="Przerobione",
                                                command=self.modifiedSound_event)
        self.botton_modifiedSound.grid(row=1, column=1, pady=10, padx=20)


        self.slider_1 = customtkinter.CTkSlider(master=self.frame_down,
                                                from_=0,
                                                to=1,
                                                number_of_steps=50,
                                                command=self.sliderEvent)
        self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")


        self.label1 = customtkinter.CTkLabel(master=self.frame_down)
        self.label1.configure(text=raw2Hz(0.5))
        #self.label1.place(relx=0.5, rely=0.5)
        self.label1.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        self.botton_confirm = customtkinter.CTkButton(master=self.frame_down,
                                                text="Zaakceptuj",
                                                command=self.confirm_event)
        self.botton_confirm.grid(row=6, column=0, columnspan=2, pady=10, padx=20)

        # ============ frame_down_right ============
        self.cells = [ [0]*3 for i in range(self.MAXNUMEXERCISES+1)]
        self.cells[0][0] = tkinter.Label(self.frame_down_right, text="zgadłeś [Hz]", bg="white", width=10, padx=5, pady=1) 
        self.cells[0][0].grid(row=0, column=0, padx=1, pady=10)
        self.cells[0][1] = tkinter.Label(self.frame_down_right, text="było [Hz]", bg="white", width=10, padx=5, pady=1) 
        self.cells[0][1].grid(row=0, column=1, padx=1, pady=10)
        self.cells[0][2] = tkinter.Label(self.frame_down_right, text="wsp. różnicy", bg="white", width=10, padx=5, pady=1) 
        self.cells[0][2].grid(row=0, column=2, padx=1, pady=10)
        for i in range(1, self.MAXNUMEXERCISES+1):
            for j in range(3):
                #self.table = tkinter.Entry(self.frame_down_right, width=12, fg='blue')#,font=('Arial',14))
                self.cells[i][j] = tkinter.Label(self.frame_down_right, text="---", bg="white", width=10, padx=5, pady=1)
                self.cells[i][j].grid(row=i, column=j, padx=1, pady=10)
                #self.table.insert(tkinter.END, 0)




    def sliderEvent(self, e):
        rawval = self.slider_1.get()
        Hz = raw2Hz(rawval)
        val = round(Hz, int(-log10(Hz))+2)
        self.label1.configure(text=val)
        self.guessedRawValue = rawval

        

    def originalSound_event(self, event=0):
        print("originalSound button pressed in {} mode".format(self.combobox_1.textvariable))
        rawl, sr = librosa.load("music-set/1.mp3", offset=7, duration=6)
        soundfile.write("music-set/TMP.wav", rawl, sr)
        playsound("music-set/TMP.wav", block=False)

    def modifiedSound_event(self, event=0):
        print("modifiedSound button pressed in {} mode".format(self.combobox_1.textvariable))
        rawl, sr = librosa.load("music-set/1.mp3", offset=7, duration=6)
        l = librosa.stft(rawl)
        midFreqIndex = raw2Hz(self.targetRawValue)
        varFreqIndex = 10
        ampliFactor= 10
        amplifier = np.zeros_like(l)
        for i in range(len(amplifier)):
            amplifier[i] = 1+(ampliFactor-1)*myNorm((i-midFreqIndex)/varFreqIndex)
        transformedl = librosa.istft(l*amplifier)
        soundfile.write("music-set/TMPtransformed.wav", transformedl, sr)
        playsound("music-set/TMPtransformed.wav", block=False)

    def confirm_event(self, event=0):
        print("confirm button pressed")
        if self.numExercise >= self.MAXNUMEXERCISES:
            self.numExercise = 0
            for i in range(1, self.MAXNUMEXERCISES+1):
                for j in range(3):
                    self.cells[i][j].configure(text="---")
        i=self.numExercise

        guessedHz = raw2Hz(self.guessedRawValue)
        targetHz = raw2Hz(self.targetRawValue)
        self.cells[i+1][0].configure(text=round(guessedHz, int(-log10(guessedHz))+2))
        self.cells[i+1][1].configure(text=round(targetHz, int(-log10(targetHz))+2))
        self.cells[i+1][2].configure(text=round(self.targetRawValue-self.guessedRawValue, 2))

        self.targetRawValue = random.random()
        self.guessedRawValue = 0.5
        self.numExercise += 1
        
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
