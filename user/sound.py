import pygame
import time
class player:
    def __init__(self):
        pygame.init()
        self.sound = {'auto':'sound/pop.wav','point':'sound/zoop.wav'}
    def play(self,sound):
        pygame.mixer.music.load(self.sound[sound])
        pygame.mixer.music.play()
        time.sleep(0.2)