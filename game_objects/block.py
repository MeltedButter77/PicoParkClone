import os

import pygame as pg


def sum_vector(vectors):
    sum_v = pg.Vector2(0, 0)
    for vector in vectors:
        sum_v += vector
    return sum_v


class PushBlock(pg.sprite.Sprite):
    def __init__(self, game, info, *groups):
        super().__init__(*groups)
        self.game = game

        # Perma variables
        self.push_speed_multiplier = 0.5

        # Gravity dependant perma variables
        gravity_direction = "down"
        gravity = 300

        # Changing Variables
        self.pos = pg.Vector2(info['x'], info['y'])
        size = (info['width'], info['height'])
        self.velocity = {
            "gravity": pg.Vector2(0, 0),
            "movement": pg.Vector2(0, 0),
            "standing_on": pg.Vector2(0, 0),
        }

        # Dictionary mapping gravity directions to (gravity_vec, move_vec, jump_vec)
        self.directions = {
            "right": (pg.Vector2(gravity, 0)),
            "left": (pg.Vector2(-gravity, 0)),
            "up": (pg.Vector2(0, -gravity)),
            "down": (pg.Vector2(0, gravity))
        }
        # Add attributes
        self.gravity_direction, self.gravity_vec = None, None

        # Apply the vectors based on the gravity direction
        self.update_gravity_vectors(gravity_direction)

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.surface.Surface(size)  # pg.image.load("../assets/players/player.png")
        self.image_original.fill("black")  # remove for an actual image
        self.image = pg.transform.scale(self.image_original, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update_gravity_vectors(self, gravity_direction):
        self.gravity_direction = gravity_direction
        self.gravity_vec = self.directions[gravity_direction]

    def update(self):
        # Apply Gravity
        self.velocity["gravity"] += self.gravity_vec

        # Apply velocity accounting for dt
        velocity = self.velocity["gravity"] + self.velocity["movement"]
        self.pos += velocity * self.game.dt
        self.velocity["movement"] *= 0

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
                self.velocity["gravity"].y = min(self.velocity["gravity"].y, 0)

            # if rect.top is higher than wall bottom and old_rect.top is lower than rect bottom
            if (self.rect.top < collided_obj.rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):
                self.rect.top = collided_obj.rect.bottom
                self.velocity["gravity"].y = max(self.velocity["gravity"].y, 0)

            if (self.rect.right > collided_obj.rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):
                self.rect.right = collided_obj.rect.left
                self.velocity["gravity"].x = min(self.velocity["gravity"].x, 0)

            if (self.rect.left < collided_obj.rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):
                self.rect.left = collided_obj.rect.right
                self.velocity["gravity"].x = max(self.velocity["gravity"].x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def push(self, pushing_object, direction):

        if direction == "right":
            self.velocity["movement"] = sum_vector(pushing_object.velocity.values()) * self.push_speed_multiplier
        elif direction == "left":
            self.velocity["movement"] = sum_vector(pushing_object.velocity.values()) * self.push_speed_multiplier
        if direction == "down":
            self.velocity["movement"] = sum_vector(pushing_object.velocity.values()) * self.push_speed_multiplier
        elif direction == "up":
            self.velocity["movement"] = sum_vector(pushing_object.velocity.values()) * self.push_speed_multiplier

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)

