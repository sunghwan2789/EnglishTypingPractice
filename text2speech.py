import urllib.parse
import urllib.request
import threading
import winsound

## Text를 Speech하는 클래스
# @see http://text2speech.us
# @see https://docs.python.org/3/library/winsound.html
class TTS:

    ## 생성자
    # @param repeat Speech 반복 여부를 설정합니다.
    def __init__(self, repeat=False):
        self.flags = winsound.SND_FILENAME | winsound.SND_ASYNC
        if repeat:
            self.flags |= winsound.SND_LOOP
        # initialize session in tts.us
        urllib.request.urlopen('http://text2speech.us')

    def play(self, text):
        TTS.stop()
        thread = threading.Thread(target=TTS.run, args=[ text, self.flags ])
        thread.start()

    ## Thread 동작
    #
    # tts.us에서 speech 파일을 내려받고 재생한다.
    @staticmethod
    def run(text, flags):
        url = 'http://text2speech.us/wavfile.php?t=%s&lf=en&gender=female' % urllib.parse.quote(text)
        (sndpath, _) = urllib.request.urlretrieve(url)
        winsound.PlaySound(sndpath, flags)

    @staticmethod
    def stop():
        winsound.PlaySound(None, winsound.SND_ASYNC)
