import pygame as py


class Player(py.sprite.Sprite):
    def __init__(self, game, position, size, controls, *groups: py.sprite.Group):
        super().__init__(*groups)
        self.game = game

        # Set Variables
        self.gravity = 10
        self.move_speed = 300
        self.controls = tuple(controls)  # (w,a,s,d)

        # Changing Variables
        self.pos = py.Vector2(position)
        self.size = py.Vector2(size)
        self.vel = py.Vector2(0, 0)

        # Image & Rect
        self.image_original = py.image.load(f"assets/players/player.png")
        self.image = py.transform.scale(self.image_original, self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect

    def update(self, event=None):
        if event:
            if event.key == self.controls[0]:
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
            self.vel.y += self.gravity

            # Apply velocity accounting for dt
            self.pos += self.vel * dt

            # update rect before collision.
            # This allows for the use of the rect in collision calculations
            # If rect was not updated, rounding pos when updating pos after moving rect would cause off-by-1 errors which look jittery
            self.rect = py.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

            # Will change velocity depending on collisions
            self.collision_check()

    def collision_check(self):
        collide_list = self.rect.collidelistall(self.game.walls)

        collide_rects = []
        for i in collide_list:
            collide_rects.append(self.game.walls[i])

        player_rects = [player.rect for player in self.game.players]
        collide_rects.extend(player_rects)

        # If colliding with one rect
        for wall_rect in collide_rects:

            # if rect.bottom is lower than wall top and old_rect.bottom is higher than rect top
            if (self.rect.bottom > wall_rect.top >= self.old_rect.bottom and
                    self.rect.right > wall_rect.left and self.rect.left < wall_rect.right):
                self.rect.bottom = wall_rect.top
                self.vel.y = min(self.vel.y, 0)

            # if rect.top is higher than wall bottom and old_rect.top is lower than rect bottom
            if (self.rect.top < wall_rect.bottom <= self.old_rect.top and
                    self.rect.right > wall_rect.left and self.rect.left < wall_rect.right):
                self.rect.top = wall_rect.bottom
                self.vel.y = max(self.vel.y, 0)

            if (self.rect.right > wall_rect.left >= self.old_rect.right and
                    self.rect.bottom > wall_rect.top and self.rect.top < wall_rect.bottom):
                self.rect.right = wall_rect.left
                self.vel.x = min(self.vel.x, 0)

            if (self.rect.left < wall_rect.right <= self.old_rect.left and
                    self.rect.bottom > wall_rect.top and self.rect.top < wall_rect.bottom):
                self.rect.left = wall_rect.right
                self.vel.x = max(self.vel.x, 0)

            # Update pos attribute, as the rect was moved to the correct position
            self.pos = py.Vector2(self.rect.topleft)

        self.old_rect = self.rect.copy()
