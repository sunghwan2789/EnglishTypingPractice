from practice import Practice, DisplayMode
from text2speech import TTS

class Practice4(Practice):

    displayMode = DisplayMode.hidden
    ## TTS
    # @var TTS
    reader = None

    def __init__(self, master=None, article=None, **kw):
        self.reader = TTS(True)
        super().__init__(master, article, **kw)

    def onLoad(self):
        super().onLoad()
        self.reader.play(self.article.texts[self.line])

    def onClosing(self):
        self.reader.stop()
        super().onClosing()
