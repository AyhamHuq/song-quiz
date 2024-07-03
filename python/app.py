from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
load_dotenv()

@app.route('/token', methods=['GET'])
def get_token():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        return jsonify({'error': 'Missing Spotify Client ID or Secret'}), 400

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    token = auth_manager.get_access_token(as_dict=False)
    return jsonify({'access_token': token})

if __name__ == '__main__':
    app.run(debug=True)
