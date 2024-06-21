import pygame as py


class Player(py.sprite.Sprite):
    def __init__(self, game, position, size, colour, *groups: py.sprite.Group):
        super().__init__(*groups)

        self.game = game
        self.pos = py.Vector2(position)
        self.size = py.Vector2(size)
        self.colour = colour

        self.image_original = py.image.load(f"assets/players/player.png")
        self.image = py.transform.scale(self.image_original, self.size)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, keys):
        dt = self.game.dt

        if keys[py.K_w]:
            self.pos.y -= 300 * dt
        if keys[py.K_s]:
            self.pos.y += 300 * dt
        if keys[py.K_a]:
            self.pos.x -= 300 * dt
        if keys[py.K_d]:
            self.pos.x += 300 * dt

        # update rect
        self.rect = py.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)