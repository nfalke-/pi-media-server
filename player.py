from subprocess import Popen
import requests


class Player(object):
    def __init__(self, port, password, media_dir):
        self.proc = None
        self.port = port
        self.base = 'http://localhost:'+self.port
        self.media_dir = media_dir
        self.password = password
        self.auth = ('', password)
        return

    def play(self, filename, subtitle_file):
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
        if subtitle_file:
            command += [
                '--sub-file', self.media_dir+subtitle_file,
            ]
        self.proc = Popen(command)

    def quit(self):
        self.proc.kill()
        self.proc = None

    def pause(self):
        path = '/requests/status.json'
        args = {
            'command': 'pl_pause'
        }
        requests.get(
            self.base+path,
            params=args,
            auth=self.auth
        )

    def seek(self):
        pass
