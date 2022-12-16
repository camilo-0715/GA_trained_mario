__author__ = 'justinarmstrong'

import pygame as pg
from . import setup
from . import constants as c

class Sound(object):
    """Handles all sound for the game"""
    def __init__(self, overhead_info):
        """Initialize the class"""
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.game_info = overhead_info.game_info
        self.set_music_mixer()



    def set_music_mixer(self):
        """Sets music for level"""
        if self.overhead_info.state == c.LEVEL:
            pg.mixer.music.load(self.music_dict['main_theme'])
            #pg.mixer.music.play()
            self.state = c.NORMAL
        elif self.overhead_info.state == c.GAME_OVER:
            pg.mixer.music.load(self.music_dict['game_over'])
            #pg.mixer.music.play()
            self.state = c.GAME_OVER


    def update(self, game_info, mario):
        """Updates sound object with game info"""
        self.game_info = game_info
        self.mario = mario
        self.handle_state()

    def  handle_state(self):
        """Handles the state of the soundn object"""
        if self.state == c.NORMAL:
            pass
        elif self.state == c.WORLD_CLEAR:
            pass
        elif self.state == c.MARIO_DEAD:
            pass
        elif self.state == c.GAME_OVER:
            pass

    def play_music(self, key, state):
        """Plays new music"""
        pg.mixer.music.load(self.music_dict[key])
        #pg.mixer.music.play()
        self.state = state

    def stop_music(self):
        """Stops playback"""
        pg.mixer.music.stop()



