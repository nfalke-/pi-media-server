from omxplayer.player import OMXPlayer
from pathlib import Path


class Player(object):
    def __init__(self, media_dir):
        self.media_dir = media_dir

    def play(self, filename):
        if self.player:
            self.player.quit()
            self.player = None
        video_path = Path(self.media_dir + filename)
        self.player = OMXPlayer(video_path)

    def quit(self):
        self.player.quit()
        self.player = None

    def pause(self):
        self.player.pause()

    def seek(self, val):
        self.player.set_position(val)

    @property
    def status(self):
        return {
            'time': self.player.position()
        }
