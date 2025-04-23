import pygame
from settings import *
import sys
from map import Map
from player import Player
from object_renderer import ObjectRenderer


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.window = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.player = Player(self)
        self.delta_time = 1

    def update(self):
        self.player.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")

    def check_events(sef):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw(self):
        # self.window.fill("black")
        self.object_renderer.draw()
        # self.map.draw()
        # self.player.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
