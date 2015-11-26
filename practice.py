from tkinter import *
import tkinter.messagebox as MessageBox
from wframe import WFrame, StartPosition
from enum import IntEnum
from time import time

class DisplayMode(IntEnum):
    # 0b001
    default = 1
    # 0b010
    overlap = 2
    # 0b100
    hidden  = 4

class Practice(WFrame):

    article = None

    line = int
    LINES_PER_PAGE = 6

    typeStart = float
    typed = int

    displayMode = DisplayMode.default

    def __init__(self, master=None, article=None, **kw):
        self.article = article
        self.line = 0
        self.typeStart = time()
        self.typed = 0
        super().__init__(master, **kw)

    def initializeWidget(self):
        labelOffset = -10 if self.displayMode & DisplayMode.default else 0
        textOffset = 10 if self.displayMode & DisplayMode.default else 0

        self.labels = []
        self.texts = []
        for i in range(self.LINES_PER_PAGE):
            label = Label(self)
            label['justify'] = LEFT
            label['font'] = 'Consolas'
            label['padx'] = 0
            label['pady'] = 0
            if self.displayMode & DisplayMode.overlap:
                label['fg'] = 'gray'
            if self.displayMode & ~DisplayMode.hidden:
                label.place(x=40, y=30 + labelOffset + i * 60)
            self.labels.append(label)

            text = Label(self)
            text['justify'] = LEFT
            text['font'] = 'Consolas'
            text['padx'] = 0
            text['pady'] = 0
            text.place(x=40, y=30 + textOffset + i * 60)
            self.texts.append(text)

        self.indicator = '' if self.displayMode & DisplayMode.overlap else '_'

        self.meter = Label(self)
        self.meter['text'] = '현재 타속:'
        self.meter.pack(side=BOTTOM, fill=X, pady=(0, 40))

        self.text = '영어 타자 연습'
        self.width = 640
        self.height = 480
        self.StartPosition = StartPosition.centerParent
        self.bind('<KeyPress>', self.keyDown)

    def onLoad(self):
        if self.line >= len(self.article.texts):
            MessageBox.showerror(self.text, '타자 끝')
            self.close()
            return

        line = self.line % self.LINES_PER_PAGE
        # 페이지 넘기기
        if line == 0:
            texts = self.article.texts[self.line:][:self.LINES_PER_PAGE]
            for i in range(self.LINES_PER_PAGE):
                self.labels[i]['text'] = texts[i] if i < len(texts) else ''
                self.texts[i]['text'] = ''
        # 타자 위치 안내자
        self.texts[line]['text'] = self.indicator

    ## 키 입력 처리
    # @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            context = self.article.texts[self.line]
            line = self.texts[self.line % self.LINES_PER_PAGE]
            text = line['text']
            if len(self.indicator):
                text = text[:-len(self.indicator)]
            # default behavior
            if e.keysym_num <= 0x7F and ch != '\0':
                # line incompleted
                if len(text) < len(context):
                    line['text'] = text + ch + self.indicator
                    # 정타 처리
                    if ch == context[len(text):][0]:
                        self.typed += 1
                # line completed
                else:
                    self.endLine()
            # erase
            elif e.keysym == 'BackSpace' and len(text):
                line['text'] = text[:-1] + self.indicator
                # penalty
                # self.typed -= 3
            # change line
            elif e.keysym == 'Return':
                self.endLine()
        except ValueError:
            pass
        # speed = typed / duration * 60
        self.meter['text'] = '현재 타속: %d' % int(self.typed / (time() - self.typeStart) * 60)

    def endLine(self):
        line = self.texts[self.line % self.LINES_PER_PAGE]
        text = line['text']
        if len(self.indicator):
            text = text[:-len(self.indicator)]
        line['text'] = text
        self.typed += 1

        self.line += 1
        self.onLoad()
