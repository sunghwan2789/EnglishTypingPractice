from tkinter import *
from WFrame import *
from Article import *
from Search import *
from Typing import *

## 영어 타자 연습의 대문
#
# 타자 연습에 사용할 텍스트를 고른 후
# <b>연습 모드를 선택하여</b> 타자 연습을 시작하거나
# 오타 알리미를 열거나
# 텍스트 전문을 볼 수 있습니다.
class Main(WFrame):

    def initializeWidget(self):
        self.lblNYTimes = Label(self)
        self.lblNYTimes['text'] = '연습할 기사:'
        self.lblNYTimes.grid(row=0, column=0)

        self.frmArticle = Frame(self)
        self.frmArticle.grid(row=0, column=1, sticky=W)

        self.btnArticle = Button(self)
        self.btnArticle['text'] = '전문 보기'
        self.btnArticle['command'] = self.showArticle
        self.btnArticle.grid(row=0, column=2, padx=5)

        self.btnNYTimes = Button(self)
        self.btnNYTimes['text'] = '새 기사 고르기'
        self.btnNYTimes['command'] = self.searchNYTimes
        self.btnNYTimes.grid(row=0, column=3)

        self.text = '영어 타자 연습'
        self.width = 600
        self.height = 400
        self.startPosition = StartPosition.centerScreen
        self.master.resizable(FALSE, FALSE)
        self.columnconfigure(1, weight=1)
        self.pack(padx=40, pady=20)

    def onLoad(self):
        # 글 불러오기
        pass

    def showArticle(self):
        pass

    def searchNYTimes(self):
        article = self.openDialog(Search).result
        if article == None:
            return

        Article.practicing = article
        for widget in self.frmArticle.winfo_children():
            widget.destroy()
        widget = ArticleWidget(self.frmArticle, Article.practicing)
        widget.pack()

Main(Tk()).mainloop()
