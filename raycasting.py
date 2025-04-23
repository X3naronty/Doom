import math
from settings import *
import pygame


class Raycasting:
    def __init__(self, player):
        self.player = player
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.player.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for index, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(
                    wall_column, (SCALE, proj_height))
                wall_pos = (index * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),
                    TEXTURE_HALF_SIZE - texture_height // 2,
                    SCALE,
                    texture_height
                )
                wall_column = pygame.transform.scale(
                    wall_column, (SCALE, HEIGHT)
                )
                wall_pos = (index * SCALE, 0)
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.player.pos
        x_map, y_map = self.player.map_pos

        ray_angle = self.player.angle - HALF_FOV + 0.001
        texture_vert, texture_hor = 1, 1
        for ray in range(NUM_RAYS):
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
                if tile_vert in self.player.game.map.objects:
                    texture_vert = self.player.game.map.objects[tile_vert]
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
                if tile_hor in self.player.game.map.objects:
                    texture_hor = self.player.game.map.objects[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # depth, texture_offset
            if depth_hor < depth_vert:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            else:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)

            # revome fishball effect
            depth *= math.cos(self.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            self.ray_casting_result.append(
                (depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
