from tkinter import *
import tkinter.messagebox as MessageBox
from WFrame import *

class Practice1(WFrame):

    ##
    # @var Article
    article = None

    row = int
    ROWS_PER_PAGE = 6

    def __init__(self, master=None, article=None, **kw):
        self.article = article
        self.row = 0
        super().__init__(master, **kw)

    def initializeWidget(self):
        self.labels = []
        self.texts = []
        for i in range(self.ROWS_PER_PAGE):
            label = Label(self, justify=LEFT, font='Consolas', padx=0, pady=0)
            label.place(x=40, y=20 + i * 60)
            self.labels.append(label)

            text = Label(self, justify=LEFT, font='Consolas', padx=0, pady=0)
            text.place(x=40, y=40 + i * 60)
            self.texts.append(text)

        self.text = '영어 타자 연습 모드1'
        self.width = 640
        self.height = 480
        self.startPosition = StartPosition.centerParent
        self.bind('<KeyPress>', self.keyDown)

    def onLoad(self):
        if self.row >= len(self.article.texts):
            MessageBox.showerror(self.text, '타자 끝')
            self.close()
            return
        row = self.row % self.ROWS_PER_PAGE
        if row == 0:
            texts = self.article.texts[self.row:][:self.ROWS_PER_PAGE]
            for i in range(self.ROWS_PER_PAGE):
                self.labels[i]['text'] = texts[i] if i < len(texts) else ''
                self.texts[i]['text'] = ''
        self.texts[row]['text'] = '_'

    ## 키 입력 처리
    # @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            context = self.article.texts[self.row]
            row = self.texts[self.row % self.ROWS_PER_PAGE]
            text = row['text'][:-1]
            # default behavior
            if e.keysym_num <= 0x7F and ch != '\0':
                if len(text) < len(context):
                    row['text'] = text + ch + '_'
                # row completed
                else:
                    self.endRow()
            # erase
            elif e.keysym == 'BackSpace' and len(text):
                row['text'] = text[:-1] + '_'
            # increase row
            elif e.keysym == 'Return':
                self.endRow()
        except ValueError:
            pass

    def endRow(self):
        row = self.texts[self.row % self.ROWS_PER_PAGE]
        text = row['text'][:-1]
        row['text'] = text

        self.row += 1
        self.onLoad()

