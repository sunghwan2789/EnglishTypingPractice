from tkinter import *
from WFrame import *

class Practice1(WFrame):

    ##
    # @var Article
    article = None

    def __init__(self, master=None, article=None, **kw):
        self.article = article
        super().__init__(master, **kw)

    def initializeWidget(self):
        self.txtt = Label(self)
        self.txtt['justify'] = LEFT
        self.txtt['text'] = '\n'.join(self.article.texts)
        self.txtt['font'] = 'Consolas'
        self.txtt['padx'] = 0
        self.txtt['pady'] = 0
        self.txtt.place(x=40, y=20)

        self.txt = Label(self)
        self.txt['justify'] = LEFT
        #self.txt['text'] = '_'
        self.txt['font'] = 'Consolas'
        self.txt['padx'] = 0
        self.txt['pady'] = 0
        self.txt.place(x=40, y=20)

        self.text = '영어 타자 연습 모드1'
        self.width = 640
        self.height = 480
        self.startPosition = StartPosition.centerParent
        self.bind('<KeyPress>', self.keyDown)

    """
    @brief 키 다운 처리
    @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    """
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            if e.keysym_num <= 0x7F and ch != '\0': self.txt['text'] = self.txt['text'] + ch# + '_'
            elif e.keysym == 'BackSpace': self.txt['text'] = self.txt['text'][:-1]# + '_'
            elif e.keysym == 'Return': self.txt['text'] = self.txt['text'] + '\n'# + '_'
        except ValueError:
            pass
