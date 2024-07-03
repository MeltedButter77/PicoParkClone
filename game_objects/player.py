import pygame as pg
import os
from game_objects import block


class Player(pg.sprite.Sprite):
    def __init__(self, game, position, size, gravity_direction, controls, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.game = game

        # No non-gravity dependant perma variables

        # Gravity dependent perma variables
        gravity = 600
        move_speed = 300
        jump_amount = 300

        # Changing Variables
        self.pos = pg.Vector2(position)
        self.standing_on = []
        self.old_standing_offset = pg.Vector2(0, 0)
        self.velocity = {
            "movement": pg.Vector2(0, 0),
            "gravity": pg.Vector2(0, 0),
            "standing_on": pg.Vector2(0, 0),
        }

        # Controls and gravity setup
        self.controls_original = tuple(controls)
        # Dictionary mapping gravity directions to (gravity_vec, move_vec, jump_vec)
        self.directions = {
            "right": (pg.Vector2(gravity, 0), pg.Vector2(0, move_speed), pg.Vector2(-jump_amount, 0)),
            "left": (pg.Vector2(-gravity, 0), pg.Vector2(0, -move_speed), pg.Vector2(jump_amount, 0)),
            "up": (pg.Vector2(0, -gravity), pg.Vector2(-move_speed, 0), pg.Vector2(0, jump_amount)),
            "down": (pg.Vector2(0, gravity), pg.Vector2(-move_speed, 0), pg.Vector2(0, -jump_amount))
        }
        # Add attributes
        self.gravity_direction, self.controls, self.gravity_vec, self.move_vec, self.jump_vec = None, None, None, None, None

        # Update vectors based on gravity_direction
        self.update_gravity_vectors(gravity_direction)

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.image.load(f"../assets/players/player.png")
        self.image = pg.transform.scale(self.image_original, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update(self, event=None):
        if event:
            if event.key == self.controls[0]:
                if len(self.standing_on) > 0:
                    self.velocity["gravity"] = self.jump_vec.copy()

        else:
            dt = self.game.dt
            keys = self.game.keys_pressed

            if keys[self.controls[1]]:
                self.velocity["movement"] = self.move_vec
            elif keys[self.controls[3]]:
                self.velocity["movement"] = -self.move_vec
            else:
                self.velocity["movement"] = pg.Vector2(0, 0)

            # Update gravity velocity Gravity
            self.velocity["gravity"] += self.gravity_vec * dt

            if len(self.standing_on) > 0 and hasattr(self.standing_on[0], "velocity"):
                self.velocity["standing_on"] = self.standing_on[0].velocity["movement"]

            # Calc total velocity
            velocity = self.velocity["gravity"] + self.velocity["movement"]
            velocity += self.velocity["standing_on"]
            # Apply velocity accounting for dt
            self.pos += velocity * dt

            # update rect before collision.
            self.rect.topleft = self.pos
            # round pos to prevent floating point errors
            self.pos = pg.Vector2(self.rect.topleft)

            # Will change velocity depending on collisions
            self.collision_check()
            # Calculate after calculating position
            self.calc_grounded()

    def calc_grounded(self):
        # Get rectangles for walls and players directly into a list
        collision_objs = [obj for group in self.game.groups for obj in group if obj != self]  # Use this to include self - [obj.rect for group in self.game.groups for obj in group]

        collision_rects = [obj.rect for obj in collision_objs]  # Use this to include self - [obj.rect for group in self.game.groups for obj in group]

        # Identify all rectangles that collide with self.rect which is one bigger in the vertical direction
        collide_indices = []
        if self.gravity_direction == "down":
            collide_indices = self.rect.inflate(0, 1).collidelistall(collision_rects)
        elif self.gravity_direction == "up":
            collide_indices = self.rect.inflate(0, 1).move(0, -1).collidelistall(collision_rects)
        if self.gravity_direction == "right":
            collide_indices = self.rect.inflate(1, 0).collidelistall(collision_rects)
        elif self.gravity_direction == "left":
            collide_indices = self.rect.inflate(1, 0).move(-1, 0).collidelistall(collision_rects)

        # Filter collide_rects to include only the rectangles that actually collide
        self.standing_on = [collision_objs[i] for i in collide_indices]

    def collision_check(self):
        collision_objects = [obj for group in self.game.groups for obj in group if obj != self]

        # Get rectangles for walls and players directly into a list
        collision_rects = [obj.rect for obj in collision_objects]

        # Identify all rectangles that collide with self.rect
        collide_indices = self.rect.collidelistall(collision_rects)

        # Filter collide_rects to include only the rectangles that actually collide
        collided_objs = [collision_objects[i] for i in collide_indices]

        for collided_obj in collided_objs:
            # bottom side collision
            if (self.rect.bottom > collided_obj.rect.top >= self.old_rect.bottom and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push(self, "down")

                if self.gravity_direction in ["left", "right"]:
                    self.velocity["movement"].x *= 0
                if self.gravity_direction in ["up", "down"]:
                    self.velocity["gravity"].y = min(self.velocity["gravity"].y, 0)
                self.rect.bottom = collided_obj.rect.top

            # top side collision
            if (self.rect.top < collided_obj.rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push(self, "up")

                if self.gravity_direction in ["left", "right"]:
                    self.velocity["movement"].x *= 0
                if self.gravity_direction in ["up", "down"]:
                    self.velocity["gravity"].y = max(self.velocity["gravity"].y, 0)
                self.rect.top = collided_obj.rect.bottom

            # right side collision
            if (self.rect.right > collided_obj.rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push(self, "right")

                if self.gravity_direction in ["up", "down"]:
                    self.velocity["movement"].x *= 0
                if self.gravity_direction in ["left", "right"]:
                    self.velocity["gravity"].x = min(self.velocity["gravity"].x, 0)
                self.rect.right = collided_obj.rect.left

            # left side collision
            if (self.rect.left < collided_obj.rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push(self, "left")

                if self.gravity_direction in ["up", "down"]:
                    self.velocity["movement"].x *= 0
                if self.gravity_direction in ["left", "right"]:
                    self.velocity["gravity"].x = max(self.velocity["gravity"].x, 0)
                self.rect.left = collided_obj.rect.right

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def update_gravity_vectors(self, new_gravity_direction):
        # update direction attribute
        self.gravity_direction = new_gravity_direction
        # update vectors
        self.gravity_vec, self.move_vec, self.jump_vec = self.directions[new_gravity_direction]
        # update controls
        if new_gravity_direction == 'down':
            self.controls = self.controls_original
        elif new_gravity_direction == 'up':
            # Invert up and down
            self.controls = [self.controls_original[2], self.controls_original[1], self.controls_original[0], self.controls_original[3]]
        elif new_gravity_direction == 'left':
            # Rotate controls left
            self.controls = [self.controls_original[3], self.controls_original[0], self.controls_original[1], self.controls_original[2]]
        elif new_gravity_direction == 'right':
            # Rotate controls right
            self.controls = [self.controls_original[1], self.controls_original[2], self.controls_original[3], self.controls_original[0]]
        else:
            raise ValueError("Invalid gravity direction")

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)
