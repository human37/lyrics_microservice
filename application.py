from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import parse_qs
from lyrics import getLyrics

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return 'Welcome to our lyrics microservice!'

@app.route('/lyrics', methods = ['POST'])
def lyrics_endpoint():
    data = parse_qs(request.get_data().decode('utf-8'))
    try:
        artist = data['artist'][0]
        if ' + ' in artist:
            artist = artist.split('+')[0]
        title = data['title'][0]
        lyrics = getLyrics(artist, title)
        return jsonify(lyrics)
    except:
        return 'Data was not formatted properly.'

if __name__ == '__main__':
    app.debug = True
    app.run()