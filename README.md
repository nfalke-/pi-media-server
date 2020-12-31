# pi-media-server

plays media files using omxplayer, runs a simple flask app as a remote

# setup

pretty sure all you need is omxplayer and the stuff in requirements.txt

I start it up like so:

    . ~/venv/bin/activate
    cd pi-media-server
    sudo xinit &
    export FLASK_APP=main.py
    export DISPLAY=:0
    flask run --host=0.0.0.0 &
