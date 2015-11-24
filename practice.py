from tkinter import *
import tkinter.mesagebox as MessageBox
from wframe import WFrame, StartPosition
from enum import Enum
from time import time

class PracticeMode(Enum):
    default = 0


class Practice(WFrame):

    article = None

    row = int
    ROWS_PER_PAGE = 6

    typeStart = float
    typed = int

    def __init__(self, master=None, article=None, **kw):
        self.article = article
        self.row = 0
        self.typeStart = time()
        self.typed = 0
        super().__init__(master, **kw)

    def initializeWidget(self):
        self.labels = []
        self.texts = []
        for i in range(self.ROWS_PER_PAGE):
            label = Label(self)
            label['justify'] = LEFT
            label['font'] = 'Consolas'
            label['padx'] = 0
            label['pady'] = 0
            label.place(x=40, y=20 + i * 60)

            text = Label(self)
            text['justify'] = LEFT
            text['font'] = 'Consolas'
            text['padx'] = 0
            text['pady'] = 0
            text.place(x=40, y=40 + i * 60)

        self.indicator = Label(self)
        self.indicator['text'] = '현재 타속:'
        self.indicator.pack(side=BOTTOM, fill=X, pady=(0, 40))

        self.text = '영어 타자 연습'
        self.width = 640
        self.height = 480
        self.StartPosition = StartPosition.centerParent
        self.bind('<KeyPress>', self.keyDown)


