import pygame as py


class Wall(py.sprite.Sprite):
    def __init__(self, game, position, size, *groups: py.sprite.Group):
        super().__init__(*groups)

        self.game = game
        self.pos = py.Vector2(position)
        self.size = py.Vector2(size)

        self.image_original = py.Surface(self.size)
        self.image = py.transform.scale(self.image_original, self.size)
        self.image.fill((0, 0, 255))

        self.rect = py.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def draw(self, screen, camera):
        location = [self.rect[i] - camera[i] for i in range(2)]
        screen.blit(self.image, location)
