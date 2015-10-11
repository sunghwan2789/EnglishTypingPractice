from tkinter import *

"""
@file Typing.py
@brief
"""
class Typing(Frame):

    def __init__(self, master=None, **kw):
        super().__init__(master, kw)
        self.initializeWidget()

    def initializeWidget(self):
        self.txt = Label(self)
        self.txt['justify'] = LEFT
        self.txt['text'] = '_'
        self.txt.pack(side=LEFT)

        self.pack(fill=BOTH, expand=TRUE)

        self.bind('<KeyPress>', self.keyDown)
        self.focus_set()

    """
    @brief 키 다운 처리
    @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    """
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            if e.keysym_num <= 0x7F and ch != '\0': self.txt['text'] = self.txt['text'][:-1] + ch + '_'
            elif e.keysym == 'BackSpace': self.txt['text'] = self.txt['text'][:-2] + '_'
            elif e.keysym == 'Return': self.txt['text'] = self.txt['text'][:-1] + '\n' + '_'
        except ValueError:
            pass
