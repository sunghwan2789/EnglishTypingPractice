## NYTimes 기사
class Article:

    ## 주소
    # @var string
    url = str
    ## 제목
    # @var string
    title = str
    ## 단어 수
    # @var int
    words = int

    ## 생성자
    def __init__(self, url=None, title=None, words=None):
        self.url = url
        self.title = title
        self.words = words

## 연습중인 기사
Article.practicing = None
