from requests import get
from bs4 import BeautifulSoup
from pyrhyme import RhymeBrain
from random import randint, randrange

RHYMES = RhymeBrain()

def getLyrics(artist, title):
    pageurl = "https://makeitpersonal.co/l3yrics?artist=" + artist + "&title=" + title
    lyrics = get(pageurl).text.strip()
    if lyrics == "Sorry, We don't have lyrics for this song yet.":
        wiki_url = "https://lyrics.fandom.com/wiki/"
        title = title.replace(" ", "_")
        artist = artist.replace(" ", "_")
        url = wiki_url + f"{artist}:{title}"
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        lyric_box = str(soup.find("div", {"class": "lyricbox"}))
        lyrics = lyric_box.replace("<br/>", "\n")
        lyrics = lyrics.replace('<div class="lyricbox">', '')
        lyrics = lyrics.replace('<div class="lyricsbreak">', '')
        lyrics = lyrics.replace('</div>', '')
    return lyrics

<<<<<<< HEAD
def removeCertainWords(lyrics):
=======
def getRhymes(word):
    words = RHYMES.rhyming_list(word=word, maxResults=4)
    formatted_words = []
    for word in words:
        formatted_words.append(str(word['word']))
    return formatted_words

def processLine(line):
    if randint(0, 3) == 0:
        line = line.split(' ')
        if len(line) > 0:
            for _ in range(3):
                random_index = randrange(0, len(line))
                random_word = line[random_index]
                if len(random_word) > 4:
                    break
                else:
                    pass
            else:
                return { 'words' : line, 'guess' : False, 'guess_index' : None,'options' : None, 'correct' : None }
            return { 'words' : line, 'guess' : True, 'guess_index' : random_index,'options' : getRhymes(random_word), 'correct' : random_word }
    return { 'words' : line, 'guess' : False, 'guess_index' : None,'options' : None, 'correct' : None }

def removeCertainWords(lyrics):
    lyrics = lyrics.split('\n')
    data = []
    for line in lyrics:
        data.append(processLine(line))
    return data
>>>>>>> 8ecfe6324fc1c1f5202964c7fe8a58ad65fb0e49
