from tkinter import *
import tkinter.messagebox as MessageBox
from wframe import WFrame, StartPosition
from enum import Enum
from time import time

## 줄의 보기 설정을 관리하는 열거형
class DisplayMode(Enum):
    ## 예문, 입력 모두 보기
    default = 0
    ## 예문, 입력 겹쳐 보기
    overlap = 1
    ## 입력만 보기
    hidden  = 2

## 타자 연습하는 WFrame
class Practice(WFrame):

    ## 타자 연습에 쓸 기사
    # @var Article
    article = None
    ## 현재 타자 중인 줄 색인
    # @var int
    line = int
    LINES_PER_PAGE = 6
    ## 첫 타자 시각
    #
    # 타자 수 계산에 활용
    # @see keyDown()
    # @var time
    typeStart = float
    ## 타자 수
    #
    # 타자 수 계산에 활용
    # @see keyDown()
    # @var int
    typed = int
    ## 줄의 보기 설정
    # @var DisplayMode
    displayMode = DisplayMode.default

    ## 생성자
    def __init__(self, master=None, article=None, **kw):
        self.article = article
        self.line = 0
        self.typeStart = time()
        self.typed = 0
        super().__init__(master, **kw)

    ## displayMode에 근거하여 indicator를 정한다.
    #
    # displayMode가 overlap일 때 '_', 그 외 ''
    def initializeWidget(self):
        labelOffset = -10 if self.displayMode == DisplayMode.default else 0
        textOffset = 10 if self.displayMode == DisplayMode.default else 0

        self.labels = []
        self.texts = []
        for i in range(self.LINES_PER_PAGE):
            label = Label(self)
            label['justify'] = LEFT
            label['font'] = 'Consolas'
            label['padx'] = 0
            label['pady'] = 0
            if self.displayMode == DisplayMode.overlap:
                label['fg'] = 'gray'
            if not self.displayMode == DisplayMode.hidden:
                label.place(x=40, y=30 + labelOffset + i * 60)
            self.labels.append(label)

            text = Label(self)
            text['justify'] = LEFT
            text['font'] = 'Consolas'
            text['padx'] = 0
            text['pady'] = 0
            text.place(x=40, y=30 + textOffset + i * 60)
            self.texts.append(text)

        self.indicator = '' if self.displayMode == DisplayMode.overlap else '_'

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
            contexts = self.article.texts[self.line:][:self.LINES_PER_PAGE]
            for i in range(self.LINES_PER_PAGE):
                self.labels[i]['text'] = contexts[i] if i < len(contexts) else ''
                self.texts[i]['text'] = ''
        # 타자 위치 안내자
        self.texts[line]['text'] = self.indicator

    ## 키 입력 처리
    # @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            context = self.article.texts[self.line]
            text = self.texts[self.line % self.LINES_PER_PAGE]
            line = text['text'][:len(text['text']) - len(self.indicator)]
            # default behavior
            if e.keysym_num <= 0x7F and ch != '\0':
                # line incompleted
                if len(line) < len(context):
                    text['text'] = line + ch + self.indicator
                    # 정타 처리
                    if ch == context[len(line)]:
                        self.typed += 1
                # line completed
                else:
                    self.endLine()
            # erase
            elif e.keysym == 'BackSpace' and len(line):
                text['text'] = line[:-1] + self.indicator
                # penalty
                # self.typed -= 3
            # change line
            elif e.keysym == 'Return':
                self.endLine()
        except ValueError:
            pass
        # speed = typed / duration * 60
        self.meter['text'] = '현재 타속: %d' % int(self.typed / (time() - self.typeStart) * 60)

    ## 줄 넘기기
    def endLine(self):
        text = self.texts[self.line % self.LINES_PER_PAGE]
        line = text['text'][:len(text['text']) - len(self.indicator)]
        text['text'] = line
        self.typed += 1

        self.line += 1
        self.onLoad()
