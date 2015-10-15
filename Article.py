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
    ## 타자 연습에 사용하기 좋게 60자로 자른 기사 본문
    #
    # 60자로 자르면 Practice 창에 보기 좋게 나온다.
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
        paragraphs = []
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
            paragraphs.append(raw)
            # 다음 문단 검색
            startIdx = match.end() + 1
        # 문장 자르기
        for para in paragraphs:
            startIdx = 0
            while startIdx < len(para):
                part = para[startIdx:startIdx + 60]
                try:
                    # 문장이 덜 끝났다면 마지막 단어를 다음 문장으로 넘긴다.
                    if para[startIdx + 60] != ' ':
                        data = part.rsplit(' ', 1)
                        part = data[0]
                        # 문장에 단어가 하나밖에 없으면 자른다.
                        # 단어가 60자를 넘는 경우
                        if len(data) == 1:
                            part = part[:59] + '-'
                            startIdx -= 1
                except:
                    pass
                self.texts.append(part.strip())
                startIdx += len(part)
