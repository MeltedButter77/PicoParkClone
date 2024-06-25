import pygame as pg
import os

from game_objects import block



class Player(pg.sprite.Sprite):
    def __init__(self, game, position, size, controls, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.game = game

        self.gravity_direction = "left"

        gravity = 600
        move_speed = 300
        jump_amount = 300

        self.controls_original = tuple(controls)
        # Dictionary mapping gravity directions to (gravity_vec, move_vec, jump_vec)
        self.directions = {
            "right": (pg.Vector2(gravity, 0), pg.Vector2(0, move_speed), pg.Vector2(-jump_amount, 0)),
            "left": (pg.Vector2(-gravity, 0), pg.Vector2(0, -move_speed), pg.Vector2(jump_amount, 0)),
            "up": (pg.Vector2(0, -gravity), pg.Vector2(-move_speed, 0), pg.Vector2(0, jump_amount)),
            "down": (pg.Vector2(0, gravity), pg.Vector2(-move_speed, 0), pg.Vector2(0, -jump_amount))
        }

        self.controls, self.gravity_vec, self.move_vec, self.jump_vec = None, None, None, None
        self.update_gravity_vectors("left")

        # Changing Variables
        self.pos = pg.Vector2(position)
        self.gravity_vel = pg.Vector2(0, 0)
        self.move_vel = pg.Vector2(0, 0)

        self.carrying = []
        self.grounded = False

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.image.load(f"../assets/players/player.png")
        self.image = pg.transform.scale(self.image_original, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update_gravity_vectors(self, gravity_direction):
        self.gravity_direction = gravity_direction
        self.gravity_vec, self.move_vec, self.jump_vec = self.directions[self.gravity_direction]
        if gravity_direction == 'down':
            self.controls = self.controls_original
        elif gravity_direction == 'up':
            # Invert up and down
            self.controls = [self.controls_original[2], self.controls_original[1], self.controls_original[0] .controls_original[3]]
        elif gravity_direction == 'left':
            # Rotate controls left
            self.controls = [self.controls_original[3], self.controls_original[0], self.controls_original[1], self.controls_original[2]]
        elif gravity_direction == 'right':
            # Rotate controls right
            self.controls = [self.controls_original[1], self.controls_original[2], self.controls_original[3], self.controls_original[0]]
        else:
            raise ValueError("Invalid gravity direction")

    def update(self, event=None):
        if event:
            if event.key == self.controls[0]:
                if self.grounded:
                    self.gravity_vel = self.jump_vec.copy()

        else:

            dt = self.game.dt
            keys = self.game.keys_pressed

            if keys[self.controls[1]]:
                self.move_vel = self.move_vec
            elif keys[self.controls[3]]:
                self.move_vel = -self.move_vec
            else:
                self.move_vel = pg.Vector2(0, 0)

            # Apply Gravity
            self.gravity_vel += self.gravity_vec * dt

            # Apply velocity accounting for dt
            self.pos += (self.gravity_vel + self.move_vel) * dt

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
        collision_rects = [obj.rect for group in self.game.groups for obj in group if obj != self]  # Use this to include self - [obj.rect for group in self.game.groups for obj in group]

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
        collided_rects = [collision_rects[i] for i in collide_indices]

        if collided_rects:
            self.grounded = True
        else:
            self.grounded = False
        print("grounded", self.grounded)

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
                    collided_obj.push("down")

                self.rect.bottom = collided_obj.rect.top
                self.gravity_vel.y = min(self.gravity_vel.y, 0)

            # top side collision
            if (self.rect.top < collided_obj.rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push("up")

                self.rect.top = collided_obj.rect.bottom
                self.gravity_vel.y = max(self.gravity_vel.y, 0)

            # right side collision
            if (self.rect.right > collided_obj.rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push("right")

                self.rect.right = collided_obj.rect.left
                self.gravity_vel.x = min(self.gravity_vel.x, 0)

            # left side collision
            if (self.rect.left < collided_obj.rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push("left")

                self.rect.left = collided_obj.rect.right
                self.gravity_vel.x = max(self.gravity_vel.x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)
