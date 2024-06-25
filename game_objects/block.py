import os

import pygame as pg


class PushBlock(pg.sprite.Sprite):
    def __init__(self, game, info, *groups):
        super().__init__(*groups)
        self.game = game

        self.pos = pg.Vector2(info['x'], info['y'])
        self.vel = pg.Vector2(0, 0)
        size = (info['width'], info['height'])
        self.push_amount = info['push_amount']

        self.gravity = pg.Vector2(0, 10)
        self.push_speed = 150

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.surface.Surface(size)  # pg.image.load("../assets/players/player.png")
        self.image_original.fill("black")  # remove for an actual image
        self.image = pg.transform.scale(self.image_original, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update(self):
        # Apply Gravity
        self.vel += self.gravity

        # Apply velocity accounting for dt
        self.pos += self.vel * self.game.dt

        # Update rect
        self.rect.topleft = self.pos

        # Check collision after rect update
        self.collision_check()

    def collision_check(self):
        collision_objects = [obj for group in self.game.groups for obj in group if obj != self]

        # Get rectangles for walls and players directly into a list
        collision_rects = [obj.rect for obj in collision_objects]

        # Identify all rectangles that collide with self.rect
        collide_indices = self.rect.collidelistall(collision_rects)

        # Filter collide_rects to include only the rectangles that actually collide
        collided_objs = [collision_objects[i] for i in collide_indices]

        for collided_obj in collided_objs:
            # if rect.bottom is lower than wall top and old_rect.bottom is higher than rect top
            if (self.rect.bottom > collided_obj.rect.top >= self.old_rect.bottom and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):
                self.rect.bottom = collided_obj.rect.top
                self.vel.y = min(self.vel.y, 0)

            # if rect.top is higher than wall bottom and old_rect.top is lower than rect bottom
            if (self.rect.top < collided_obj.rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):
                self.rect.top = collided_obj.rect.bottom
                self.vel.y = max(self.vel.y, 0)

            if (self.rect.right > collided_obj.rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):
                self.rect.right = collided_obj.rect.left
                self.vel.x = min(self.vel.x, 0)

            if (self.rect.left < collided_obj.rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):
                self.rect.left = collided_obj.rect.right
                self.vel.x = max(self.vel.x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def push(self, direction):
        if direction == "right":
            self.pos.x += self.push_speed * self.game.dt
        elif direction == "left":
            self.pos.x -= self.push_speed * self.game.dt

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)


def create_object(game, obj_info):
    if obj_info['type'] == 'push_block':
        PushBlock(game, obj_info, game.blocks)
