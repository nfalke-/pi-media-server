from subprocess import Popen
import requests


class Player(object):
    def __init__(self, port, password, media_dir):
        self.proc = None
        self.port = port
        self.base = 'http://localhost:'+self.port
        self.path = '/requests/status.json'

        self.media_dir = media_dir
        self.password = password
        self.auth = ('', password)
        return

    def play(self, filename):
        command = []
        command += [
            'vlc', '-f',
            self.media_dir + filename
        ]
        command += [
            '-I', 'http',
            '--http-password', self.password,
            '--http-port', self.port,
        ]
        self.proc = Popen(command)

    def quit(self):
        self.proc.kill()
        self.proc = None

    def pause(self):
        args = {
            'command': 'pl_pause'
        }
        requests.get(
            self.base+self.path,
            params=args,
            auth=self.auth
        )

    def seek(self, val):
        args = {
            'command': 'seek',
            'val': val
        }
        requests.get(
            self.base+self.path,
            params=args,
            auth=self.auth
        )

    @property
    def status(self):
        return requests.get(
            self.base+self.path,
            auth=self.auth
        ).json()
