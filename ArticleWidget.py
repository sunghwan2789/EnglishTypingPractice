from tkinter import *
from Article import *

## Article의 기본 정보를 담은 Widget
class ArticleWidget(Frame, Article):

    ## 생성자
    def __init__(self, master=None, article=None, **kw):
        Frame.__init__(self, master, kw)
        article = article if article != None else Article()
        Article.__init__(self, article.url, article.title, article.words)

    def pack(self):
        self.lblTitle = Label(self)
        self.lblTitle['text'] = self.title
        self.lblTitle['anchor'] = W
        self.lblTitle.grid(row=0, column=0, sticky=W)

        self.lblWords = Label(self)
        self.lblWords['text'] = self.words
        self.lblWords['fg'] = 'gray'
        self.lblWords.grid(row=0, column=1)

        self.grid_columnconfigure(0, weight=1)
        super().pack(fill=X, expand=TRUE)
