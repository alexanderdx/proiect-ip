import time, vlc, pafy
from youtubesearchpython import VideosSearch
 

class media_player:
    def __init__ (self, title = None):

        options = ' '
        if title is not None:
            # title   = title.replace (' ', '_')
            options = f'--video-title {title}'

        self.vlc_instance = vlc.Instance (options)
        self.player       = self.vlc_instance.media_player_new ()
        self.volume       = 100


    def set_media (self, source, is_youtube = True):
        if is_youtube:
            best  = pafy.new (source).getbest ()
            media = self.vlc_instance.media_new (best.url)
            
            self.player.set_media (media)
            self.player.play ()
        else:
            media = self.vlc_instance.media_new (source)
            self.player.set_media (media)
            self.player.play ()


    def search (self, query):
        videosSearch = VideosSearch (query, limit = 1)

        return videosSearch.result ()['result'][0]['link']

    
    def pause (self):
        if self.player.is_playing():
            self.player.pause ()

    
    def play (self):
        if not self.player.is_playing():
            self.player.play ()

    def stop(self):
        self.player.stop ()

    def volume_up (self):
        if self.volume + 10 <= 100:
            self.volume += 10
            self.player.audio_set_volume (self.volume)

    def volume_down (self):
        if self.volume - 10 >= 0:
            self.volume -= 10
            self.player.audio_set_volume (self.volume)

    def volume_absolute (self, volume):
        self.player.audio_set_volume (volume)

    def mute (self):
        self.player.audio_set_volume (0)

    def unmute (self):
        self.player.audio_set_volume (self.volume)

    def close (self):
        self.player.stop ()

    def get_time (self):
        return self.player.get_time ()

    def set_time (self, time):
        self.player.set_time (time) 

    def get_volume (self):
        return self.player.audio_get_volume ()
