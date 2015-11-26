from tkinter import *
from wframe import WFrame, StartPosition
from article import Article
from articlewidget import ArticleWidget
from search import Search
from view import View
from practice1 import Practice1
from practice2 import Practice2
from practice3 import Practice3
from fixer import Fixer
import pickle

## 영어 타자 연습의 대문
#
# 타자 연습에 사용할 텍스트를 고른 후
# <b>연습 모드를 선택하여</b> 타자 연습을 시작하거나
# 오타 알리미를 열거나
# 텍스트 전문을 볼 수 있습니다.
class Main(WFrame):

    ## 연습 중인 기사
    # @var Article
    article = None

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

        self.btnTypePractice = Button(self)
        self.btnTypePractice['text'] = '기본 타자 연습'
        self.btnTypePractice['command'] = self.startPractice
        self.btnTypePractice.place(x=100, y=100)

        self.btnTypePractice = Button(self)
        self.btnTypePractice['text'] = '겹쳐 보기 연습'
        self.btnTypePractice['command'] = self.startPractice2
        self.btnTypePractice.place(x=300, y=100)

        self.btnTypePractice = Button(self)
        self.btnTypePractice['text'] = '받아쓰기 연습'
        self.btnTypePractice['command'] = self.startPractice3
        self.btnTypePractice.place(x=100, y=200)

        self.btnTypePractice = Button(self)
        self.btnTypePractice['text'] = '오타 알리미'
        self.btnTypePractice['command'] = self.startFixer
        self.btnTypePractice.place(x=300, y=200)

        self.text = '영어 타자 연습'
        self.width = 600
        self.height = 400
        self.startPosition = StartPosition.centerScreen
        self.master.resizable(FALSE, FALSE)
        self.columnconfigure(1, weight=1)
        self.pack(padx=40, pady=20)

    def onLoad(self):
        # 글 불러오기
        try:
            with open('data/article.pkl', 'rb') as article:
                self.article = pickle.load(article)
                ArticleWidget(self.frmArticle, self.article).pack()
        except:
            pass

    def onClosing(self):
        # 글 저장하기
        try:
            with open('data/article.pkl', 'wb') as article:
                pickle.dump(self.article, article)
        except:
            pass

    ## 기사 전문 보기
    def showArticle(self):
        if self.article:
            self.openDialog(View, article=self.article)

    ## Search로 NYTimes를 검색하고 연습에 쓸 기사를 선택합니다.
    def searchNYTimes(self):
        article = self.openDialog(Search).result
        if article == None:
            return
        # 옛 기사 삭제
        for widget in self.frmArticle.winfo_children():
            widget.destroy()
        # 새 기사 등록
        self.article = article
        ArticleWidget(self.frmArticle, self.article).pack()

    ## 타자 연습을 시작합니다.
    def startPractice(self):
        if self.article:
            self.openDialog(Practice1, article=self.article)

    ## 타자 연습2을 시작합니다.
    def startPractice2(self):
        if self.article:
            self.openDialog(Practice2, article=self.article)

    ## 타자 연습3을 시작합니다.
    def startPractice3(self):
        if self.article:
            self.openDialog(Practice3, article=self.article)

    ## 오타 알리미를 시작합니다.
    def startFixer(self):
        self.openDialog(Fixer)

if __name__ == '__main__':
    Main(Tk()).mainloop()
