from tkinter import *
from enum import Enum

## WFrame 창의 처음 위치를 나타내는 열거형
class StartPosition(Enum):
    default = 0
    centerScreen = 1
    centerParent = 2
    manual = 3

## Windows Forms를 토대로 작성한 Frame
#
# http://effbot.org/tkinterbook/
class WFrame(Frame):

    ## 제목 표시줄에 표시할 제목
    # @var string
    text = 'WFrame'
    ## WFrame 너비
    # @var int
    width = 300
    ## WFrame 높이
    # @var int
    height = 300
    ## 창 왼쪽 위치
    # @var int
    x = 0
    ## 창 위쪽 위치
    # @var int
    y = 0
    ## 창의 처음 위치
    # @var StartPosition
    startPosition = StartPosition.default
    ## 부모 WFrame
    # @see open()
    # @var WFrame
    parent = None

    ## 생성자
    def __init__(self, master=None, parent=None, **kw):
        super().__init__(master, kw)
        self.master.protocol('WM_DELETE_WINDOW', self._onClosing)
        self.parent = parent if parent != None else self
        self._initializeWidget()
        self.onLoad()

    ## 원시 Widget을 초기화한다.
    def _initializeWidget(self):
        self.initializeWidget()
        self.master.title(self.text)
        self.master.geometry('%dx%d' % (self.width, self.height))
        self.master.geometry('+%d+%d' % self._getPosition())
        self.pack(fill=BOTH, expand=TRUE)
        self.focus_set()

    # onClosing Handler
    def _onClosing(self):
        self.onClosing()
        self.master.destroy()

    ## startPosition에 근거한 위치를 계산한다.
    # @return tuple (x, y)
    def _getPosition(self):
        self.master.update_idletasks()
        (width, height) = self.getSize()
        (parentWidth, parentHeight) = self.parent.getSize()
        if self.startPosition == StartPosition.default:
            self.x = self.master.winfo_x()
            self.y = self.master.winfo_y()
        elif self.startPosition == StartPosition.centerScreen:
            self.x = self.master.winfo_screenwidth() / 2 - width / 2
            self.y = self.master.winfo_screenheight() / 2 - height / 2
        elif self.startPosition == StartPosition.centerParent:
            self.x = self.parent.master.winfo_x() + parentWidth / 2 - width / 2
            self.y = self.parent.master.winfo_y() + parentHeight / 2 - height / 2
        elif self.startPosition != StartPosition.manual:
            raise ValueError('%s is not a valid StartPosition' % str(self.startPosition))
        return (self.x, self.y)

    ## 창의 크기를 잰다.
    # @return tuple (width, height)
    def getSize(self):
        width = self.master.winfo_width() + (self.master.winfo_rootx() - self.master.winfo_x()) * 2
        height = self.master.winfo_height() + (self.master.winfo_rooty() - self.master.winfo_y()) * 2
        return (width, height)

    ## Widget을 추가한다.
    #
    # Windows Forms의 InitializeComponent처럼 작성한다.
    def initializeWidget(self):
        pass

    ## load 완료 후 작업
    def onLoad(self):
        pass

    ## 창을 닫는다.
    def close(self):
        self._onClosing()

    ## 창 끌 때 할 작업
    def onClosing(self):
        pass

    ## wFrame을 자식 창에 띄우고 wFrame을 반환한다.
    # @param wFrame 자식 창에 띄울 WFrame
    # @return WFrame
    def open(self, wFrame, **kw):
        return wFrame(Toplevel(self), parent=self, **kw)

    ## 자식 창을 닫을 때까지 부모 창을 숨긴다.
    # @see open()
    def openDialog(self, wFrame, **kw):
        self.master.withdraw()
        wframe = self.open(wFrame, **kw)
        wframe.wait_window()
        self.master.deiconify()
        return wframe
