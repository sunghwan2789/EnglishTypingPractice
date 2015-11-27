from tkinter import *
from wframe import WFrame, StartPosition
from vscrollwidget import VScrollWidget
import pickle

class Typo:
    context = None
    expected = -1
    ch = None

    def __init__(self, context, expected, ch):
        self.context = context
        self.expected = expected
        self.ch = ch

    def toString(self, suggest):
        return '\n'.join([
            self.context,
            ' ' * self.expected + '¯',
            '입력: %s; 개선 조언: %s' % (self.ch, suggest)
        ])

class TypoList(list):

    def append(self, context, expected, ch):
        super().append(Typo(context, expected, ch))

## 오타 알리미
class Fixer(WFrame):

    typos = None

    def __init__(self, master=None, **kw):
        self.typos = Fixer.load()
        super().__init__(master, **kw)

    def initializeWidget(self):
        self.scrollFrame = VScrollWidget(self)
        self.scrollFrame.pack(fill=BOTH, expand=TRUE)

        for typo in self.typos:
            label = Label(self.scrollFrame.frame)
            label['justify'] = LEFT
            label['font'] = 'Consolas'
            label['padx'] = 0
            label['pady'] = 0
            label['text'] = typo.toString(Fixer.suggest(typo))
            label.pack(padx=(40, 0), pady=(20, 0), anchor=NW)

        self.text = '오타 알리미'
        self.width = 640
        self.height = 480
        self.startPosition = StartPosition.centerParent

    ## 오타에 대한 조언을하는 메서드
    #
    # 매우 중요!
    # @return string
    @staticmethod
    def suggest(typo):
        if ' ' in typo.context[typo.expected - 2:][:4]:
            return '차분한 마음으로 타자해보세요.'
        elif typo.ch in typo.context[typo.expected - 2:][:4]:
            return '타속은 너무 신경쓰지 말고,\n연습하는 느낌으로 타자해보세요.'
        return '좀 더 연습하세요.'

    @staticmethod
    def load():
        try:
            with open('data/typos.pkl', 'rb') as data:
                typos = pickle.load(data)
        except:
            pass
        return TypoList() if typos == None else typos

    @staticmethod
    def save(typoList):
        typoBak = Fixer.load()
        with open('data/typos.pkl', 'wb') as typos:
            pickle.dump(typoBak + typoList, typos)
