import pygame as pg
import os


class Player(pg.sprite.Sprite):
    def __init__(self, game, position, size, controls, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.game = game

        # Set Variables
        self.gravity = pg.Vector2(0, 10) # x gravity, still buggy. -y should work
        self.move_speed = 300
        self.controls = tuple(controls)  # (w,a,s,d)

        # Changing Variables
        self.pos = pg.Vector2(position)
        self.size = pg.Vector2(size)
        self.vel = pg.Vector2(0, 0)

        self.carrying = []
        self.grounded = False

        # Image & Rect
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.image_original = pg.image.load(f"../assets/players/player.png")
        self.image = pg.transform.scale(self.image_original, self.size)
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
            self.vel += self.gravity

            # Apply velocity accounting for dt
            self.pos += self.vel * dt

            # EXPLANATION about order of operations -- update rect before collision.
            # This allows for the use of the rect in collision calculations
            # If rect was not updated, when updating pos after moving rect (by setting pos to rect.topleft) pos gets rounded.
            # This would cause off-by-1 errors which look jittery as the collision would not be detected and after being moved by gravity
            # it would round to colliding rather than colliding and being moved back.
            self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

            # Will change velocity depending on collisions
            self.collision_check()
            # Calculate after collrecting position
            self.calc_grounded()

    def calc_grounded(self):
        # Get rectangles for walls and players directly into a list
        collision_rects = [wall.rect for wall in self.game.walls]
        collision_rects.extend(player.rect for player in self.game.players if player != self)

        # Identify all rectangles that collide with self.rect which is one bigger in the vertical direction
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
            print("Grounded")
        else:
            self.grounded = False
            print("NOT Grounded")


    def collision_check(self):
        # Get rectangles for walls and players directly into a list
        collision_rects = [wall.rect for wall in self.game.walls]
        collision_rects.extend(player.rect for player in self.game.players) #if player != self) # BUG for some reason, removing self causes jittering

        # Identify all rectangles that collide with self.rect
        collide_indices = self.rect.collidelistall(collision_rects)

        # Filter collide_rects to include only the rectangles that actually collide
        collided_rects = [collision_rects[i] for i in collide_indices]

        for collided_rect in collided_rects:
            # if rect.bottom is lower than wall top and old_rect.bottom is higher than rect top
            if (self.rect.bottom > collided_rect.top >= self.old_rect.bottom and
                    self.rect.right > collided_rect.left and self.rect.left < collided_rect.right):
                self.rect.bottom = collided_rect.top
                self.vel.y = min(self.vel.y, 0)

            # if rect.top is higher than wall bottom and old_rect.top is lower than rect bottom
            if (self.rect.top < collided_rect.bottom <= self.old_rect.top and
                    self.rect.right > collided_rect.left and self.rect.left < collided_rect.right):
                self.rect.top = collided_rect.bottom
                self.vel.y = max(self.vel.y, 0)

            if (self.rect.right > collided_rect.left >= self.old_rect.right and
                    self.rect.bottom > collided_rect.top and self.rect.top < collided_rect.bottom):
                self.rect.right = collided_rect.left
                self.vel.x = min(self.vel.x, 0)

            if (self.rect.left < collided_rect.right <= self.old_rect.left and
                    self.rect.bottom > collided_rect.top and self.rect.top < collided_rect.bottom):
                self.rect.left = collided_rect.right
                self.vel.x = max(self.vel.x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = pg.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()

    def draw(self, screen, camera):
        location = [self.rect[i] - camera[i] for i in range(2)]
        screen.blit(self.image, location)
