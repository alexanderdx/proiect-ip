# pip install vlc pafy youtube-search-python

import time, vlc, pafy
from youtubesearchpython import VideosSearch
 

vlc_instance = vlc.Instance ()
player       = vlc_instance.media_player_new()

def play_video (url, new_player = True):
    best  = pafy.new(url).getbest()
    media = vlc_instance.media_new(best.url)
     
    player.set_media(media)
    player.play()


def youtube_search (query):
    videosSearch = VideosSearch(query, limit = 1)

    return videosSearch.result()['result'][0]['link']


def main ():
    while True:
        print ('Search: ', end = '')
        query = input ()
        play_video (youtube_search (query), new_player = True if player.is_playing else False)


if __name__ == '__main__':
    main ()
