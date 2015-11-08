from tkinter import *
import tkinter.messagebox as MessageBox
from WFrame import *
from time import time
import urllib.parse
import urllib.request
import winsound
import threading

class Practice3(WFrame):

    ##
    # @var Article
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
            label = Label(self, justify=LEFT, font='Consolas', padx=0, pady=0, fg='gray')
            label.place(x=40, y=30 + i * 60)
            self.labels.append(label)

            text = Label(self, justify=LEFT, font='Consolas', padx=0, pady=0)
            text.place(x=40, y=30 + i * 60)
            self.texts.append(text)

        self.indicator = Label(self)
        self.indicator['text'] = '현재 타속:'
        self.indicator.pack(side=BOTTOM, fill=X, pady=(0, 40))

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

        t = threading.Thread(target=Practice3.speak, args=[ self.article.texts[self.row] ])
        t.start()

    ## tts
    def speak(text):
        # tts.us에서 세션을 검사한다...
        url = 'http://text2speech.us'
        urllib.request.urlopen(url)
        # tts 파일 다운로드
        url = 'http://text2speech.us/wavfile.php?t=%s&lf=en&gender=female' % urllib.parse.quote(text)
        (sndpath, _) = urllib.request.urlretrieve(url)
        winsound.PlaySound(sndpath, winsound.SND_FILENAME)


    ## 키 입력 처리
    # @see http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    def keyDown(self, e):
        try:
            ch = chr(e.keysym_num)
            context = self.article.texts[self.row]
            row = self.texts[self.row % self.ROWS_PER_PAGE]
            text = row['text']
            # default behavior
            if e.keysym_num <= 0x7F and ch != '\0':
                if len(text) < len(context):
                    row['text'] = text + ch
                    if ch == context[len(text):][0]:
                        self.typed += 1
                # row completed
                else:
                    self.endRow()
            # erase
            elif e.keysym == 'BackSpace' and len(text):
                row['text'] = text[:-1]
                # self.typed -= 3
            # increase row
            elif e.keysym == 'Return':
                self.endRow()
        except ValueError:
            pass
        self.indicator['text'] = '현재 타속: %d' % int(self.typed / (time() - self.typeStart) * 60)

    def endRow(self):
        row = self.texts[self.row % self.ROWS_PER_PAGE]
        text = row['text'][:-1]
        row['text'] = text
        self.typed += 1

        self.row += 1
        self.onLoad()
