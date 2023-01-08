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
        for i in range(2):
            for j in range(3):
                self.e = tkinter.Entry(self.frame_down_right, width=12, fg='blue')#,font=('Arial',14))
                self.e.grid(row=i, column=j)
                self.e.insert(tkinter.END, 0)

        # ============ variables ============
        self.targetRawValue = random.random()
        self.guessedRawValue = 0.5

    def sliderEvent(self, e):
        #print(dir(self.label1))
        rawval = self.slider_1.get()
        val = round(raw2Hz(rawval), 1)
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
        pass
        
    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

