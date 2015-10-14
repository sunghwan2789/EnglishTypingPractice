import tkinter.messagebox as MessageBox
import urllib.request
import patch_urllib_request
import urllib.parse
import html
import re

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
    ## 기사 본문
    # @see load()
    # @var list<string>
    texts = list

    ## 생성자
    def __init__(self, url=None, title=None, words=None):
        self.url = url
        self.title = title
        self.words = words
        self.texts = []

    ## url에서 기사 본문을 긁어 온다.
    def load(self, cnt=0):
        if len(self.texts) > 0:
            return
        # 기사 본문 내려받기
        url = 'http://mobile' + self.url[10:-4] + 'amp.html'
        response = urllib.request.urlopen(url)
        content = response.read().decode('UTF-8')
        # 문단 추출
        startIdx = 0
        paraRe = re.compile(r'body-text\'>(.*?)</p', re.S)
        while 1:
            match = paraRe.search(content, startIdx)
            if match == None:
                break
            # HTML 태그 제거
            raw = re.sub(r'<(?P<tag>[A-Za-z]).*?>(.*?)</(?P=tag).*?>', r'\2', match.group(1), flags=re.S).strip()
            # quote 치환
            raw = re.sub(r'[“”]|‘‘|’’', '"', raw)
            raw = re.sub(r'[‘’]', "'", raw)
            raw = html.unescape(raw)
            self.texts.append(raw)
            # 다음 문단 검색
            startIdx = match.end() + 1
