from requests import get
from bs4 import BeautifulSoup

def getLyrics(artist, title):
    pageurl = "https://makeitpersonal.co/lyrics?artist=" + artist + "&title=" + title
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
    # print(lyrics)
    return lyrics

def parseLyrics(lyrics):
    lines = lyrics.split('\n')
    words = []
    for line in lines:
        for word in line.split():
            words.append(word)
    parsed_data = []
    guessing = []
    i = j = l = 0
    while i < len(words):
        # Every 12 words
        if j > 12:
            # If it is a good word
            if len(words[i]) > 4 and words[i][0] != '(':
                w = words[i]
                # Find the whole line this word was in
                while l < len(lines):
                    if w in lines[l]:
                        words_arr = lines[l].split()
                        idx = words_arr.index(w)
                        # Check for trailing baddies
                        if w[-1] in ',!?':
                            char = w[-1]
                            w = w[0:-1]
                            words_arr[idx] = w[0:-1]
                            if len(words_arr) > idx:
                                words_arr.append(char)
                            else:
                                words_arr[idx + 1] = f"{char} {words_arr[idx + 1]}"
                        parsed_data.append({
                            'words' : words_arr, 'guessing' : True, 'guess_index' : idx, 'correct' : w
                        })
                        guessing.append(l)
                        l += 1
                        break
                    else:
                        parsed_data.append({
                            'words' : lines[l], 'guessing' : False, 'guess_index' : None, 'correct' : None
                        })
                    l += 1
                        
                j = 0
            else:
                j += 1
        else:
            j += 1
        i += 1

    return parsed_data
