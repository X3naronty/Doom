from sprite_object import SpriteObject, AnimatedSprite
from random import randint, random, choice
from os.path import join
from settings import *
import pygame


class NPC(AnimatedSprite):
    def __init__(
        self,
        game,
        path=join("resources", "sprites", "npc", "soldier", "idle"),
        pos=(4, 1.5),
        scale=0.6,
        shift=0.38,
        animation_time=180
    ):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.sprites = {}
        self.sprites["attack"] = self.get_images(join(path, "..", "attack"))
        self.sprites["death"] = self.get_images(join(path, "..", "death"))
        self.sprites["idle"] = self.get_images(join(path, "..", "idle"))
        self.sprites["pain"] = self.get_images(join(path, "..", "pain"))
        self.sprites["walk"] = self.get_images(join(path, "..", "walk"))

        self.attack_dist = 3
        self.speed = 0.03
        self.size = 10
        self.health = 20
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True

        self.images = self.sprites["idle"]

        self.animation_count = 0
        self.is_animating = False

        self.is_reachable = True
        self.is_observable = False
        
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.render_sprite()
        self.is_observable = self.player_npc_raycasting()
        self.run_logic()

        # self.draw_ray_cast()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def player_npc_raycasting(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ray_angle = self.theta
        cos_a = math.cos(ray_angle)
        sin_a = math.sin(ray_angle)

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.objects:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # horizontals

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.objects:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        self.dist = player_dist = max(player_dist_h, player_dist_v)
        wall_dist = max(wall_dist_h, wall_dist_v)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pygame.draw.circle(self.game.window, "red",
                           (100 * self.x, 100 * self.y), 15)
        if self.is_observable:
            pygame.draw.line(self.game.window, "orange", (100 * self.game.player.x,
                             100 * self.game.player.y), (100 * self.x, 100 * self.y), 2)

    def check_hit(self):
        return self.game.weapon.shot and HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width and self.is_observable

    def handle_hit(self):
        self.game.weapon.shot = False
        self.animation_count = 0
        self.is_animating = True
        self.images = self.sprites["pain"]
        self.game.sound.npc_pain.play()
        self.health -= self.game.weapon.damage
        if (self.health <= 0):
            self.handle_death()

    def handle_death(self):
        self.alive = False
        self.game.sound.npc_death.play()
        self.images = self.sprites["death"]
        self.animation_count = 0
        self.is_animating = True


    def move(self):
        player = self.game.player
        next_pos = next_x, next_y = self.game.bfs.get_next_step(self.map_pos, player.map_pos)
        # next_post = next_x, next_y = player.map_pos

        if next_pos not in self.game.object_handler.npc_positions:
            # print(self.game.object_handler.npc_positions)

            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)

            dx = self.speed * math.cos(angle)        
            dy = self.speed * math.sin(angle)

            if self.is_not_collided(int(self.x + dx * self.size), int(self.y)):
                self.x += dx
            if self.is_not_collided(int(self.x), int(self.y + dy * self.size)):
                self.y += dy

    def is_not_collided(self, x, y):
        return (x, y) not in self.game.map.objects and (x, y) != self.game.player.map_pos 

    def handle_attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            


    def run_logic(self):
        if self.alive:
            if self.check_hit():
                if self.health > 0:
                    self.handle_hit()
                else: self.handle_death()
            elif self.dist <= self.attack_dist and self.is_observable:
                if not self.is_animating: 
                    self.images = self.sprites["attack"]
                    self.is_animating = True 
                    self.animation_count = 0
                self.handle_attack()
            elif self.is_observable or self.is_reachable: 
                self.move()
                if not self.is_animating:
                    self.images = self.sprites["walk"]
            elif not self.is_animating:
                self.images = self.sprites["idle"]
            self.animate()
            if self.animation_trigger: self.animation_count += 1

        elif self.is_animating:
            if self.game.global_trigger:
                self.image = self.images[0]
                self.images.rotate(-1)
                self.animation_count += 1
        if self.animation_count == len(self.images): 
            self.animation_count = 0
            self.is_animating = False


        

