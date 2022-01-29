# pip install vlc pafy youtube-search-python

import time, vlc, pafy
from youtubesearchpython import VideosSearch
 

class media_player:
    def __init__ (self):
        self.vlc_instance = vlc.Instance ()
        self.player       = self.vlc_instance.media_player_new ()
        self.volume       = 100


    def set_media (self, source, is_youtube = True):
        if is_youtube:
            best  = pafy.new (source).getbest ()
            media = self.vlc_instance.media_new (best.url)
            
            self.player.set_media(media)
            self.player.play()


    def search (self, query):
        videosSearch = VideosSearch (query, limit = 1)

        return videosSearch.result()['result'][0]['link']

    
    def pause (self):
        self.player.pause ()

    
    def play (self):
        self.player.play ()

    def volume_up (self):
        self.volume += 10
        self.player.audio_set_volume (self.volume)

    def volume_down (self):
        self.volume -= 10
        self.player.audio_set_volume (self.volume)

    def volume_absolute (self, volume):
        self.player.audio_set_volume (volume)

    def mute (self):
        self.player.audio_set_volume (0)

    def unmute (self):
        self.player.audio_set_volume (self.volume)



if __name__ == '__main__':
    mp = media_player ()
    
    while True:
        print ('Search: ', end = '')
        query = input ()

        if query == "play":
            mp.play ()
        elif query == "pause":
            mp.pause ()
        elif query == "vup":
            mp.volume_up ()
        elif query == "vdown":
            mp.volume_down ()
        elif query == "mute":
            mp.mute ()
        elif query == "unmute":
            mp.unmute ()
        else:
            mp.set_media (mp.search (query))
