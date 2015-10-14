from tkinter import *
from WFrame import *

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
        self.txtArticle = Text(self)
        self.txtArticle.insert(INSERT, '\n'.join(self.article.texts))
        self.txtArticle.pack()

        self.text = '기사 보기'
        self.width = 400
        self.height = 300
        self.startPosition = StartPosition.centerParent
