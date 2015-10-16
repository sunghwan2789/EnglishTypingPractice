from tkinter import *
from WFrame import *
from VScrollWidget import *

## 기사 한눈에 보기
#
# 후에 같은 프레임에 미니 단어장 추가!
class View(WFrame):

    ## 조회할 기사
    # @var Article
    article = None

    ## 생성자
    def __init__(self, master=None, article=None, **kw):
        self.article = article
        super().__init__(master, **kw)

    def initializeWidget(self):
        self.scrollFrame = VScrollWidget(self)
        self.scrollFrame.pack(fill=BOTH, expand=TRUE)

        self.lblArticle = Label(self.scrollFrame.frame)
        self.lblArticle['justify'] = LEFT
        self.lblArticle['text'] = '\n'.join(self.article.texts)
        self.lblArticle['font'] = 'Consolas'
        self.lblArticle['padx'] = 0
        self.lblArticle['pady'] = 0
        self.lblArticle.pack(padx=(40, 0), pady=(20, 0), anchor=NW)

        self.text = '기사 보기'
        self.width = 640
        self.height = 480
        self.startPosition = StartPosition.centerParent
