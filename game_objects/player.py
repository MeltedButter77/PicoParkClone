import pygame as pg
import os

from game_objects import block


class Player(pg.sprite.Sprite):
    def __init__(self, game, position, size, controls, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.game = game

        # Set Variables
        self.gravity = pg.Vector2(0, 600)  # x gravity, still buggy. -y should work
        self.move_speed = 300
        self.controls = tuple(controls)  # (w,a,s,d)

        # Changing Variables
        self.pos = pg.Vector2(position)
        self.vel = pg.Vector2(0, 0)

        self.carrying = []
        self.grounded = False

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.image.load(f"../assets/players/player.png")
        self.image = pg.transform.scale(self.image_original, size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update(self, event=None):
        if event:
            if event.key == self.controls[0]:
                if self.grounded:
                    self.vel.y = -self.move_speed
        else:
            dt = self.game.dt
            keys = self.game.keys_pressed

            if keys[self.controls[1]]:
                self.vel.x = -self.move_speed
            elif keys[self.controls[3]]:
                self.vel.x = self.move_speed
            else:
                self.vel.x = 0

            # Apply Gravity
            self.vel += self.gravity * dt

            # Apply velocity accounting for dt
            self.pos += self.vel * dt

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
        if self.gravity.y > 0:
            collide_indices = self.rect.inflate(0, 1).collidelistall(collision_rects)
        elif self.gravity.y < 0:
            collide_indices = self.rect.inflate(0, 1).move(0, -1).collidelistall(collision_rects)
        if self.gravity.x > 0:
            collide_indices = self.rect.inflate(1, 0).collidelistall(collision_rects)
        elif self.gravity.x < 0:
            collide_indices = self.rect.inflate(1, 0).move(-1, 0).collidelistall(collision_rects)

        if self.gravity.length() == 0:
            collide_indices = self.rect.inflate(2, 2).move(-1, -1).collidelistall(collision_rects)

        # Filter collide_rects to include only the rectangles that actually collide
        collided_rects = [collision_rects[i] for i in collide_indices]

        if collided_rects:
            self.grounded = True
        else:
            self.grounded = False

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
                self.rect.bottom = collided_obj.rect.top
                self.vel.y = min(self.vel.y, 0)

            # top side collision
            if (self.rect.top < collided_obj.rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_obj.rect.left and self.rect.left < collided_obj.rect.right):
                self.rect.top = collided_obj.rect.bottom
                self.vel.y = max(self.vel.y, 0)

            # right side collision
            if (self.rect.right > collided_obj.rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push("right")

                self.rect.right = collided_obj.rect.left
                self.vel.x = min(self.vel.x, 0)

            # left side collision
            if (self.rect.left < collided_obj.rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_obj.rect.top and self.rect.top < collided_obj.rect.bottom):

                if isinstance(collided_obj, block.PushBlock):
                    collided_obj.push("left")

                self.rect.left = collided_obj.rect.right
                self.vel.x = max(self.vel.x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)
