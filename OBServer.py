"""
    OBServer

    A small GUI tool to update a bunch of text files for an OBS overlay.

    Created 2023/03/14 by Max
"""

import tkinter as tk
import os
import sys
import json

path2pathJson = r'paths.json'   # use this if the json is in the same folder as the script. Use actual path otherwise.

class obServer(tk.Frame):
    def __init__(self, master):
        """
        This runs the main functions of the GUI.
        """
        tk.Frame.__init__(self, master)
        self.pack(expand=True)
        self.paths = self.readFilePaths()
        self._build()
        self._reset()

    def _build(self):
        """
        Here the GUI is built.
        """
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
        tk.Label(self.mainFrame, text="Name1:").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.E)
        self.nameEntry1 = tk.Entry(self.mainFrame, textvariable=self.player1).grid(row=rowCount, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W)
        tk.Label(self.mainFrame, text="Name2:").grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.E)
        self.nameEntry2 = tk.Entry(self.mainFrame, textvariable=self.player2).grid(row=rowCount, column=4, padx=5, pady=5, columnspan=2, sticky=tk.W)
        # ------ Deck Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text="Deck1:").grid(row=rowCount, column=0, padx=5, pady=5, sticky=tk.E)
        self.deckEntry1 = tk.Entry(self.mainFrame, textvariable=self.deck1).grid(row=rowCount, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W)
        tk.Label(self.mainFrame, text="Deck2:").grid(row=rowCount, column=3, padx=5, pady=5, sticky=tk.E)
        self.deckEntry2 = tk.Entry(self.mainFrame, textvariable=self.deck2).grid(row=rowCount, column=4, padx=5, pady=5, columnspan=2, sticky=tk.W)
        # ------ Producer and Set Button Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text='Producer:').grid(row=rowCount, column=0, sticky=tk.E)
        self.producerEntry = tk.Entry(self.mainFrame, textvariable=self.producer).grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.setBtn = tk.Button(self.mainFrame, text='   Set   ', command=self._setNames)
        self.setBtn.grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.E)
        # ------ Life Total Row ------
        rowCount += 1
        tk.Label(self.mainFrame, text='Life Totals:').grid(row=rowCount, column=0, sticky=tk.E)
        self.lifeTotalEntryOne = tk.Entry(self.mainFrame, textvariable=self.lifeP1).grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.lifeTotalEntryTwo = tk.Entry(self.mainFrame, textvariable=self.lifeP2).grid(row=rowCount, column=3, columnspan=2, padx=5, pady=5, sticky=tk.W)
        # ------ Increment Decrement Row ------
        rowCount += 1
        self.incBtn1 = tk.Button(self.mainFrame, text='  -  ', command=self._decrementLeft)
        self.incBtn1.grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.incBtn2 = tk.Button(self.mainFrame, text='  -  ', command=self._decrementRight)
        self.incBtn2.grid(row=rowCount, column=3, columnspan=2, padx=5, pady=5, sticky=tk.W)
        self.decBtn1 = tk.Button(self.mainFrame, text='  +  ', command=self._incrementLeft)
        self.decBtn1.grid(row=rowCount, column=1, columnspan=2, padx=5, pady=5, sticky=tk.E)
        self.decBtn2 = tk.Button(self.mainFrame, text='  +  ', command=self._incrementRight)
        self.decBtn2.grid(row=rowCount, column=3, columnspan=2, padx=5, pady=5, sticky=tk.E)
        # ------ Producer and Misc Row ------
        rowCount += 2
        self.resetBtn = tk.Button(self.mainFrame, text=' Reset ', command=self._reset)
        self.resetBtn.grid(row=rowCount, column=4, padx=5, pady=5, sticky=tk.E)
        self.quitBtn = tk.Button(self.mainFrame, text=' Exit ', command=self._quit)
        self.quitBtn.grid(row=rowCount, column=5, padx=5, pady=5, sticky=tk.E)

    def readFilePaths(self):
        """
        Reads the provided json file.
        returns: dict
        """
        with open(path2pathJson, 'r') as jsonFile:
            paths = json.load(jsonFile)
        return paths

    def _setNames(self):
        """
        Writes the five name related files
        """
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
        """
        Writes the two life total related files
        """
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

    def _reset(self):
        self.player1.set('')
        self.player2.set('')
        self.deck1.set('')
        self.deck2.set('')
        self.lifeP1.set('20')
        self.lifeP2.set('20')
        self.producer.set('')
        self._setNames()
        self._updateLifeTotals()

    def _quit(self):
        self.master.quit()

if __name__ == '__main__':
    root  = tk.Tk()
    root.title('The OBServer')
    observerApp = obServer(root)
    root.mainloop()
