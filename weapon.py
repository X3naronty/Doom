from collections import deque
from sprite_object import AnimatedSprite
import pygame
from os.path import join
from settings import *


class Weapon(AnimatedSprite):
    def __init__(
        self,
        game,
        path=join("resources", "sprites", "weapon", "shotgun"),
        scale=0.4,
        animation_time=90
    ):
        super().__init__(
            game=game,
            path=path,
            scale=scale,
            animation_time=animation_time
        )
        self.images = deque(
            [pygame.transform.smoothscale(img, (
                self.image.get_width() * scale, self.image.get_height() * scale
            )) for img in self.images]
        )
        # print(self.pos)
        self.pos = (
            HALF_WIDTH - self.image.get_width() * scale // 2,
            HEIGHT - self.image.get_height() * scale
        )
        self.shot = False
        self.reload = False
        self.animation_count = 0
        self.animation_len = len(self.images)
        self.damage = 10

    def draw(self):
        self.game.window.blit(self.images[0], self.pos)

    def fire(self, event):
        if event.button == 1 and not self.shot and not self.reload:
            self.shot = True
            self.reload = True
            self.game.sound.gun_shot.play()

    def update(self):
        if self.reload:
            self.check_animation_time()
            if self.animation_trigger:
                self.shot = False
                self.images.rotate(-1)
                self.animation_count += 1
                if self.animation_count == self.animation_len:
                    self.reload = False
                    self.animation_count = 0
