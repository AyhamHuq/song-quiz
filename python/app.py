import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/')
def hello():
    return "Song Quiz Game Backend"

@socketio.on('startGame')
def handle_start_game(data):
    playlist_id = data['playlistId']
    results = sp.playlist_tracks(playlist_id)
    tracks = [{'name': item['track']['name'], 'artists': [artist['name'] for artist in item['track']['artists']]} for item in results['items']]
    emit('gameData', tracks)

if __name__ == '__main__':
    socketio.run(app, debug=True)
