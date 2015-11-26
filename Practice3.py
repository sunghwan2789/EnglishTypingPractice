from practice import Practice, DisplayMode
import urllib.parse
import urllib.request
import winsound
import threading

class Practice3(Practice):

    displayMode = DisplayMode.overlap# | DisplayMode.hidden

    def onLoad(self):
        super().onLoad()
        t = threading.Thread(target=Practice3.speak, args=[ self.article.texts[self.line] ])
        t.start()

    @staticmethod
    def speak(text):
        # tts.us에서 세션을 검사한다...
        url = 'http://text2speech.us'
        urllib.request.urlopen(url)
        # tts 파일 다운로드
        url = 'http://text2speech.us/wavfile.php?t=%s&lf=en&gender=female' % urllib.parse.quote(text)
        (sndpath, _) = urllib.request.urlretrieve(url)
        winsound.PlaySound(sndpath, winsound.SND_FILENAME)
