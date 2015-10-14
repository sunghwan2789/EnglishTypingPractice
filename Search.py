from tkinter import *
from WFrame import *
from VScrollWidget import *
from Article import *
from ArticleWidget import *
import urllib.parse
import urllib.request
import json
import __config__

## NYTimes 기사 검색기
class Search(WFrame):

    ## 검색 결과 선택한 Article
    # @see select()
    # @var Article
    result = None

    def initializeWidget(self):
        self.txtKeyword = Entry(self)
        self.txtKeyword['width'] = 987654
        self.txtKeyword.grid(row=0, column=0)

        self.btnSearch = Button(self)
        self.btnSearch['text'] = '검색'
        self.btnSearch['command'] = self.search
        self.btnSearch.grid(row=0, column=1)

        self.frmArticleList = VScrollWidget(self)
        self.frmArticleList.grid(row=1, column=0, columnspan=2, sticky=N)
        self.frmArticleList.bind_all('<Button-1>', self.select)

        self.btnSearchNext = Button(self)
        self.btnSearchNext['text'] = '더 보기'
        self.btnSearchNext['command'] = self.searchNext
        self.btnSearchNext.grid(row=2, column=0, columnspan=2)

        self.text = 'NYTimes 기사 검색기'
        self.width = 400
        self.height = 300
        self.startPosition = StartPosition.centerParent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    ## 기사 검색에 필요한 초기화 작업을 한다.
    def search(self):
        for widget in self.frmArticleList.frame.winfo_children():
            widget.destroy()
        self.page = 0
        self.searchNext()

    ## txtKeyword의 값으로 기사를 검색하고 화면에 결과를 출력한다.
    def searchNext(self):
        self.page += 1
        for article in Search.getArticles(self.txtKeyword.get(), self.page):
            ArticleWidget(self.frmArticleList.frame, article).pack()

    ## 선택한 ArticleWidget으로 Article을 만든 후 result에 저장하고 창을 닫는다.
    def select(self, e):
        isArticleWidget = isinstance(e.widget, ArticleWidget)
        if isArticleWidget or isinstance(e.widget.master, ArticleWidget):
            aw = e.widget if isArticleWidget else e.widget.master
            self.result = aw.article
            self.master.destroy()

    ## NYTimes의 API를 이용해 keyword에 해당하는 기사의 목록을 10개 단위로 가져온다.
    #
    # http://developer.nytimes.com/docs/read/article_search_api_v2
    # @param keyword 검색할 키워드
    # @param page 페이지
    # @return list<Article>
    @staticmethod
    def getArticles(keyword, page=1):
        url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=%s&fl=%s&page=%d' % (
            urllib.parse.quote(__config__.APIKey),
            urllib.parse.quote('web_url,headline,word_count'),
            (page - 1) * 10)
        if len(keyword) > 0:
            url += '&q=%s' % urllib.parse.quote(keyword)
        response = urllib.request.urlopen(url)
        content = response.read().decode('UTF-8')

        jobject = json.loads(content, 'UTF-8')
        articles = []
        for i in jobject['response']['docs']:
            url = i['web_url']
            # i['headline']['main']은 KeyError가 발생할 수 있음
            title = i['headline'].get('main')
            words = i['word_count']
            articles.append(Article(url, title, words))
        return articles
