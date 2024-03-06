import os
import time
import random
import webbrowser
import urllib
import signal
import threading
from flask import Flask, request

app = Flask(__name__)


def generate_state(seed=None):
    random.seed(seed)
    return round(random.random() * int('1' + ('0' * 16)))


def make_auth_url(url, data):
    return '?'.join([url, urllib.parse.urlencode(data)])


def shutdown_server():
    time.sleep(1)
    os.kill(os.getpid(), signal.SIGINT)


@app.route('/callback')
def callback():
    if request.args.get('state') == app.config['state']:
        app.config['code'] = request.args.get('code')

    threading.Thread(target=shutdown_server).start()
    return 'OK to close this tab'


def main():

    port = 8888
    client_id = '5a9c5f03e2104575ae720578579ff6f8'
    auth_url = 'https://accounts.spotify.com/authorize'
    redirect_uri = f'http://localhost:{port}/callback'

    state = generate_state(1919)

    scopes = ' '.join([
        'user-read-private',
        'user-read-email',
        'user-read-playback-state',
    ])

    data = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scopes,
        'redirect_uri': redirect_uri,
        'state': state,
    }

    app.config['state'] = state

    webbrowser.open_new_tab(make_auth_url(auth_url, data))

    app.run(debug=True, port=port, reload=False)


if __name__ == '__main__':
    main()
