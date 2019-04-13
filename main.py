from flask import Flask, request, render_template, url_for, redirect
from player import Player
import json
import os
app = Flask(__name__)
media_dir = '../media/'
player = Player(media_dir=media_dir)


@app.route('/')
def root():
    return redirect(url_for('list_shows'))
    return render_template('root.html')


@app.route('/list_shows')
def list_shows():
    files = [i for i in os.listdir(media_dir) if not i.endswith('srt')]
    return render_template('list_shows.html', files=files)


@app.route('/status')
def status():
    return json.dumps(player.status)


@app.route('/control')
def control():
    args = request.args

    if args.get('quit'):
        player.quit()
        return redirect(url_for('list_shows'))

    if args.get('pause'):
        player.pause()

    if args.get('seek'):
        player.seek(args.get('seek'))

    return render_template(
        'control.html',
        length=player.status['length']
    )


@app.route('/run')
def run():
    video = request.args.get('file')
    if not video:
        return "please supply a file"
    player.play(video)
    return redirect(url_for('control'))
