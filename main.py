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
@app.route('/list_shows/<path:path>')
def list_shows(path=''):
    files = sorted([
        {
            'file': path + i,
            'is_dir': os.path.isdir(media_dir + path + i),
            'display_name': i.replace('_', ' ')
        }
        for i in os.listdir(media_dir + path)
        if not i.endswith('.srt')
    ], key=lambda x: x['display_name'])
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
        if args.get('seek', '').isdigit():
            player.seek(int(args.get('seek')))
        else:
            if args.get('seek')[0] == '+':
                player.seek(player.status + int(args.get('seek')[1:]))
            elif args.get('seek')[0] == '-':
                player.seek(player.status - int(args.get('seek')[1:]))

    if args.get('volume'):
        player.set_volume(int(args.get('volume')))

    if args.get('subtitle'):
        if args.get('subtitle', '').isdigit():
            player.set_subtitle_track(int(args.get('subtitle')))
        else:
            player.toggle_subtitles()

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
