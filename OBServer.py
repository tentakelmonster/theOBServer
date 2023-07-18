"""
    OBServer

    A small GUI tool to update a bunch of text files for an OBS overlay.

    Created 2023/03/14 by Max
"""

import tkinter as tk
import os
import sys
import json
from tkinter.messagebox import askyesno
import random
try:
    from pynput import keyboard
    print('Using global keybinds')
    GLOBAL_KEY_BINDS = True
except ModuleNotFoundError as e:
    print('Using regular keybinds')
    GLOBAL_KEY_BINDS = False

path2pathJson = r'paths.json'   # use this if the json is in the same folder as the script. Use actual path otherwise.

class obServer(tk.Frame):
    def __init__(self, master, *listener):
        """ This runs the main functions of the GUI. """
        tk.Frame.__init__(self, master)
        self.pack(expand=True)
        self.paths = self.readFilePaths()
        self.build()
        self.resetLife()
        self.mainFrame.focus_set()
        self.readInitStates()
        self.colA = ["Full English", "Oops! All", "Five Color", "Big", "Steamy", "Delverless", "Boomer", "Zoomer", "Pauper", 
                "Saucy", "The Legendary", "Topdeck", "Dead Guy", "Ye ol'", "Questionable", "3-0 6-0", "0-2 drop", "The Real Slim", 
                "Million Dollar", "Invoke", "Chef Anthony's", "Phyrexian", "Regular", "Junk", "Bad", "Strong", "Cube", "Uber",
                "Synergistic", "Tiny", "Eldrazi", "Turbo", "Squandered", "Irregular", "Bun Magic", "Babies First", "This Player's",
                "WUBRG", "Gavin Verhey's", "Soul", "Death and", "Hardened", "Bathtub"]
        self.colB = ["Breakfast", "Aggrocontrol", "Tempo", "Tribal", "Baneslayers", "Mulldrifters", "Deck", "Problems", "Tron", 
                "Ham Sandwich", "Bears", "Money Pile", "Baby!", "Sagas", "Triomes", "Zoo", "Looters", "Sushi", "Gods", 
                "Moms", "Noodle", "Junk", "Big Boys", "Mustache", "Tools", "Synergy", "Saprolings", "Squirrels", "Netdeck",
                "Superfriends", "Superenemies", "Stax", "Storm", "Robots", "Cascade", "Bogles", "Devotion", "Madness", "Cannons"]

    def build(self):
        """ Here the GUI is built. """
        # init
        self.player1 = tk.StringVar()
        self.player2 = tk.StringVar()
        self.deck1 = tk.StringVar()
        self.deck2 = tk.StringVar()
        self.lifeP1 = tk.StringVar()
        self.lifeP1.trace('w', self._updateLifeTotals)
        self.lifeP2 = tk.StringVar()
        self.lifeP2.trace('w', self._updateLifeTotals)
        self.producer = tk.StringVar()
        rowCount = 0
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=rowCount, column=0, rowspan=10, columnspan=6, padx=5, pady=5, sticky=tk.N + tk.W)
        # ------ Name Row ------
        tk.Label(self.mainFrame, text="Name1:").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        self.nameEntry1 = tk.Entry(self.mainFrame, textvariable=self.player1)
        self.nameEntry1.grid(row=rowCount, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W) 
        tk.Label(self.mainFrame, text="Name2:").grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.W)
        self.nameEntry2 = tk.Entry(self.mainFrame, textvariable=self.player2)
        self.nameEntry2.grid(row=rowCount, column=4, padx=5, pady=5, columnspan=2, sticky=tk.W)
        # ------ Deck Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text="Deck1:").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        self.deckEntry1 = tk.Entry(self.mainFrame, textvariable=self.deck1)
        self.deckEntry1.grid(row=rowCount, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W)
        tk.Label(self.mainFrame, text="Deck2:").grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.W)
        self.deckEntry2 = tk.Entry(self.mainFrame, textvariable=self.deck2)
        self.deckEntry2.grid(row=rowCount, column=4, padx=5, pady=5, columnspan=2, sticky=tk.W)
        # ------ Producer and Buttons Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text='Producer:').grid(row=rowCount, column=0, sticky=tk.W)
        self.producerEntry = tk.Entry(self.mainFrame, textvariable=self.producer)
        self.producerEntry.grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.setBtn = tk.Button(self.mainFrame, text='   Set   ', command=self._setNames)
        self.setBtn.grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.W)
        # ------ Life Total Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text='Life Totals:').grid(row=rowCount, column=0, sticky=tk.W)
        self.lifeTotalEntryOne = tk.Entry(self.mainFrame, textvariable=self.lifeP1).grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.lifeTotalEntryTwo = tk.Entry(self.mainFrame, textvariable=self.lifeP2).grid(row=rowCount, column=3, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.resetLifeBtn = tk.Button(self.mainFrame, text='Reset', command=self._resetLifeBtn)
        self.resetLifeBtn.grid(row=rowCount, column=5, padx=5, pady=5, sticky=tk.W)
        # ------ Increment Decrement Row ------
        rowCount += 1
        self.incBtn1 = tk.Button(self.mainFrame, text='  -  ', command=self._decrementLeft)
        self.incBtn1.grid(row=rowCount, column=1, rowspan=2, padx=5, pady=5, sticky=tk.W)
        self.incBtn2 = tk.Button(self.mainFrame, text='  -  ', command=self._decrementRight)
        self.incBtn2.grid(row=rowCount, column=3, rowspan=2, padx=5, pady=5, sticky=tk.W)
        self.decBtn1 = tk.Button(self.mainFrame, text='  +  ', command=self._incrementLeft)
        self.decBtn1.grid(row=rowCount, column=2, rowspan=2, padx=5, pady=5, sticky=tk.W)
        self.decBtn2 = tk.Button(self.mainFrame, text='  +  ', command=self._incrementRight)
        self.decBtn2.grid(row=rowCount, column=4, rowspan=2, padx=5, pady=5, sticky=tk.W)
        # ------ Keybind Explanation Row ------
        rowCount += 2
        tk.Label(self.mainFrame, text='Hotkeys:').grid(row=rowCount, column=0, sticky=tk.W)
        tk.Label(self.mainFrame, text=' d ').grid(row=rowCount, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.mainFrame, text=' f ').grid(row=rowCount, column=2, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.mainFrame, text=' j ').grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.mainFrame, text=' k ').grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.W)
        # ------ Reset and Quit Row ------
        rowCount += 1
        self.generateNamesBtn = tk.Button(self.mainFrame, text='   Generate Deck Names   ', command=self._generateDeckNames)
        self.generateNamesBtn.grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.W)
        self.resetBtn = tk.Button(self.mainFrame, text=' Reset All', command=self._resetAll)
        self.resetBtn.grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.W)
        self.quitBtn = tk.Button(self.mainFrame, text=' Exit ', command=self._quit)
        self.quitBtn.grid(row=rowCount, column=5, padx=5, pady=5, sticky=tk.W)
        # set key binds
        if not GLOBAL_KEY_BINDS:
            self.mainFrame.bind('d', lambda event: self._decrementLeft())
            self.mainFrame.bind('f', lambda event: self._incrementLeft())
            self.mainFrame.bind('j', lambda event: self._decrementRight())
            self.mainFrame.bind('k', lambda event: self._incrementRight())
        self.nameEntry1.bind('<Return>', lambda event: self._writeSingeFile('player1', self.player1.get()))
        self.nameEntry2.bind('<Return>', lambda event: self._writeSingeFile('player2', self.player2.get()))
        self.deckEntry1.bind('<Return>', lambda event: self._writeSingeFile('deck1', self.deck1.get()))
        self.deckEntry2.bind('<Return>', lambda event: self._writeSingeFile('deck2', self.deck2.get()))
        self.producerEntry.bind('<Return>', lambda event: self._writeSingeFile('producer', self.producer.get()))
        self.mainFrame.bind("<Button-1>", self.callback)


    def readFilePaths(self):
        """
        Reads the provided json file.
        returns: dict
        """
        with open(path2pathJson, 'r') as jsonFile:
            paths = json.load(jsonFile)
        return paths

    def _writeSingeFile(self, field, value):
        """ writes the value of a field to the respective file """
        with open(self.paths[field], 'w') as f:
            f.write(value)

    def _setNames(self):
        """ Writes the five name related files """
        with open(self.paths['player1'], 'w') as f:
            f.write(self.player1.get())
        with open(self.paths['player2'], 'w') as f:
            f.write(self.player2.get())
        with open(self.paths['deck1'], 'w') as f:
            f.write(self.deck1.get())
        with open(self.paths['deck2'], 'w') as f:
            f.write(self.deck2.get())
        with open(self.paths['producer'], 'w') as f:
            f.write(self.producer.get())

    def _updateLifeTotals(self, *args):
        """ Writes the two life total related files """
        with open(self.paths['lifeP1'], 'w') as f:
            f.write(self.lifeP1.get())
        with open(self.paths['lifeP2'], 'w') as f:
            f.write(self.lifeP2.get())

    def _incrementLeft(self):
        newLife = int(self.lifeP1.get()) + 1
        self.lifeP1.set(str(newLife))
        self._updateLifeTotals()

    def _incrementRight(self):
        newLife = int(self.lifeP2.get()) + 1
        self.lifeP2.set(str(newLife))
        self._updateLifeTotals()

    def _decrementLeft(self):
        newLife = int(self.lifeP1.get()) - 1
        self.lifeP1.set(str(newLife))
        self._updateLifeTotals()

    def _decrementRight(self):
        newLife = int(self.lifeP2.get()) - 1
        self.lifeP2.set(str(newLife))
        self._updateLifeTotals()

    def resetLife(self):
        self.lifeP1.set('20')
        self.lifeP2.set('20')
        self._updateLifeTotals()

    def _generateDeckNames(self):
        a1, a2 = random.sample(self.colA, 2)
        b1, b2 = random.sample(self.colB, 2)
        self.deck1.set(a1 + ' ' + b1)
        self.deck2.set(a2 + ' ' + b2)

    def _resetLifeBtn(self):
        if askyesno('Reset Life Totals?', 'Do you really want to reset life totals?'):
            self.resetLife()

    def _resetAll(self):
        if askyesno('Reset All Entries?', 'Do you really want to reset everything?'):
            self.player1.set('')
            self.player2.set('')
            self.deck1.set('')
            self.deck2.set('')
            self.producer.set('')
            self._setNames()
            self.resetLife()

    def _quit(self):
        self.master.quit()

    def callback(self, event):
        """ Brings back the focus to the frame on button click """
        self.mainFrame.focus_set()

    def readInitStates(self):
        with open(self.paths['player1'], 'r') as f:
            data = f.readline().strip()
            self.player1.set(data)
        with open(self.paths['player2'], 'r') as f:
            data = f.readline().strip()
            self.player2.set(data)
        with open(self.paths['deck1'], 'r') as f:
            data = f.readline().strip()
            self.deck1.set(data)
        with open(self.paths['deck2'], 'r') as f:
            data = f.readline().strip()
            self.deck2.set(data)
        with open(self.paths['producer'], 'r') as f:
            data = f.readline().strip()
            self.producer.set(data)


if __name__ == '__main__':
    if GLOBAL_KEY_BINDS:
        root  = tk.Tk()
        root.title('The OBServer')
        observerApp = obServer(root)
        listener = keyboard.GlobalHotKeys({
            'd': observerApp._decrementLeft,
            'f': observerApp._incrementLeft,
            'j': observerApp._decrementRight,
            'k': observerApp._incrementRight}) 
        listener.start()
        root.mainloop()
        listener.stop()
        listener.join()
    else:
        root  = tk.Tk()
        root.title('The OBServer')
        observerApp = obServer(root)
        root.mainloop()
