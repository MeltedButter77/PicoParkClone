import pygame as pg


class Wall(pg.sprite.Sprite):
    def __init__(self, game, position, size, *groups: pg.sprite.Group):
        super().__init__(*groups)
        self.game = game

        self.pos = pg.Vector2(position)
        self.size = pg.Vector2(size)

        self.image_original = pg.Surface(self.size)
        self.image = pg.transform.scale(self.image_original, self.size)
        self.image.fill("dark green")

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def draw(self, screen):
        location = [self.rect[i] - self.game.camera[i] for i in range(2)]
        screen.blit(self.image, location)
