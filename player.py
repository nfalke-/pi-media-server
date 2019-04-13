from omxplayer.player import OMXPlayer
from pathlib import Path


class Player(object):
    def __init__(self, media_dir):
        self.media_dir = media_dir
        self.player = None

    def play(self, filename):
        if self.player:
            self.player.quit()
            self.player = None
        video_path = Path(self.media_dir + filename)
        self.player = OMXPlayer(video_path, args=['--no-osd'])

    def quit(self):
        self.player.quit()
        self.player = None

    def pause(self):
        self.player.play_pause()

    def seek(self, val):
        self.player.set_position(val)

    def set_volume(self, val):
        self.player.set_volume(val)

    @property
    def status(self):
        return {
            'time': int(self.player.position()),
            'length': int(self.player.duration()),
            'volume': int(self.player.volume())
        }
