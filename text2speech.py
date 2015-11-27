import urllib.parse
import urllib.request
import threading
import winsound

## Text를 Speech하는 클래스
# @see https://github.com/craic/bing_translate_text_to_speech
# @see https://docs.python.org/3/library/winsound.html
class TTS:

    ## 생성자
    # @param repeat Speech 반복 여부를 설정합니다.
    def __init__(self, repeat=False):
        self.flags = winsound.SND_FILENAME | winsound.SND_ASYNC
        if repeat:
            self.flags |= winsound.SND_LOOP

    def play(self, text):
        TTS.stop()
        thread = threading.Thread(target=TTS.run, args=[ text, self.flags ])
        thread.start()

    ## Thread 동작
    #
    # tts.us에서 speech 파일을 내려받고 재생한다.
    @staticmethod
    def run(text, flags):
        url = 'http://bing-translate-tts-demo.craic.com/text_to_speech_web_audio_api?query=%s&language=en' % urllib.parse.quote(text)
        (sndpath, _) = urllib.request.urlretrieve(url)
        winsound.PlaySound(sndpath, flags)

    @staticmethod
    def stop():
        winsound.PlaySound(None, winsound.SND_ASYNC)
