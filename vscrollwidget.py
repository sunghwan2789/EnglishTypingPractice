from tkinter import *

## 종 스크롤 Widget
#
# 부모 Frame에 꽉차게 그린다.
# http://stackoverflow.com/a/16198198
class VScrollWidget(Frame):

    ## Widget을 추가할 때 쓸 Frame
    # @var Frame
    frame = None

    ## 생성자
    def __init__(self, master=None, **kw):
        super().__init__(master, kw)

        self.canvas = Canvas(self)
        self.canvas['highlightthickness'] = 0
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scrollbar = Scrollbar(self)
        self.scrollbar['orient'] = VERTICAL
        self.scrollbar['command'] = self.canvas.yview
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas['yscrollcommand'] = self.scrollbar.set

        self.frame = Frame(self)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        self.frame.bind('<Configure>', self._frameResized)

        self.bind('<Configure>', self._resized)

    ## frame에 위젯이 추가되거나 삭제되면 스크롤 영역을 조절한다.
    def _frameResized(self, e):
        self.canvas['scrollregion'] = '0 0 %d %d' % (e.width, e.height)

    ## 부모 Frame의 크기가 바뀌면 canvas의 크기를 조절한다.
    def _resized(self, e):
        self.canvas['width'] = self.master.winfo_width() - self.scrollbar.winfo_reqwidth()
        self.canvas['height'] = self.master.winfo_reqheight()
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_reqwidth())
