import pygame as py


class Player(py.sprite.Sprite):
    def __init__(self, game, position, size, *groups: py.sprite.Group):
        super().__init__(*groups)
        self.game = game

        # Set Variables
        self.gravity = 10
        self.move_speed = 300

        # Changing Variables
        self.pos = py.Vector2(position)
        self.size = py.Vector2(size)
        self.vel = py.Vector2(0, 0)

        # Image & Rect
        self.image_original = py.image.load(f"assets/players/player.png")
        self.image = py.transform.scale(self.image_original, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.old_rect = self.rect

    def update(self, event=None):
        if event:
            if event.key == py.K_w:
                self.vel.y = -self.move_speed
        else:
            dt = self.game.dt
            keys = self.game.keys_pressed

            if keys[py.K_a]:
                self.vel.x = -self.move_speed
            elif keys[py.K_d]:
                self.vel.x = self.move_speed
            else:
                self.vel.x = 0

            # Apply Gravity
            self.vel.y += self.gravity

            # Will change velocity depending on collisions
            self.collision_check()

            # Apply velocity accounting for dt
            self.pos += self.vel * dt

            # update rect
            self.old_rect = self.rect.copy()
            self.rect = py.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def collision_check(self):
        collide_list = self.rect.collidelistall(self.game.walls)
        if collide_list:
            print(collide_list)
            self.vel.y = min(self.vel.y, 0)

