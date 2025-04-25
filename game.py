import pygame
from settings import *
import sys
from map import Map
from player import Player
from object_renderer import ObjectRenderer
from object_handler import ObjectHandler
from weapon import Weapon
from sound import Sound


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.window = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.assign_game_entities()

    def assign_game_entities(self):
        self.map = Map(self)
        self.object_renderer = ObjectRenderer(self)
        self.player = Player(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)

    def update(self):
        self.player.update()
        self.object_handler.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{self.clock.get_fps():.1f}")

    def check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    quit()
                case pygame.MOUSEBUTTONDOWN:
                    self.weapon.fire(event)
                case default:
                    pass
                    
        
            

    def draw(self):
        # self.window.fill("black")
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
