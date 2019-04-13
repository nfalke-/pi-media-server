from flask import Flask, request, render_template, url_for, redirect
from subprocess import Popen
import os
import requests
app = Flask(__name__)


print('test')
class Player(object):
    def __init__(self, port, password):
        self.proc = None
        self.port = port
        self.base = 'http://localhost:'+self.port
        self.password = password
        self.auth = ('', password)
        return

    def play(self, filename, subtitle_file):
        command = []
        command += [
            'vlc', '-f', 
            './media/' + filename
        ]
        command += [
            '-I', 'http',
            '--http-password', self.password,
            '--http-port', self.port,
        ]
        if subtitle_file:
            command += [
                '--sub-file', './media/'+subtitle_file,
            ]
        print(command)
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



player = Player(port='8080', password='temp')


@app.route('/')
def root():
    return redirect(url_for('list_shows'))
    return render_template('root.html')

@app.route('/list_shows')
def list_shows():
    files = [
        i for i in os.listdir('./media') if not i.endswith('srt')
    ]
    return render_template('list_shows.html', files=files)

@app.route('/list_subtitles')
def list_subtitles():
    args = request.args
    files = [
        i for i in os.listdir('./media') if i.endswith('srt')
    ]
    return render_template('list_subtitles.html', video=args.get('file'), files=files)

@app.route('/control')
def control():
    args = request.args

    if args.get('quit'):
        player.quit()
        return redirect(url_for('list_shows'))

    if args.get('pause'):
        player.pause()
    
    return render_template('control.html')

@app.route('/run')
def run():
    video = request.args.get('file')
    subtitle = request.args.get('subtitle')
    if not video:
        return "please supply a file"
    player.play(video, subtitle)
    return redirect(url_for('control'))

