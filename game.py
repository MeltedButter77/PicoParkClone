import pygame as py
import utils
import player


class Game():
    def __init__(self, app):
        self.app = app
        self.level = utils.json_load("data/levels/level_" + app.selected_mode.split("_")[2] + ".json")

        self.dt = 1

        self.players = py.sprite.Group()
        self.objects = py.sprite.Group()

        for info in self.level["players"]:
            player_obj = player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), ["colour"], self.players)
        # for wall_info in self.level["walls"]:
        #     wall =

    def run(self):
        if not self.level:
            return "menu_main"

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        return "menu_main"

            ### LOGIC ###
            keys_pressed = py.key.get_pressed()
            self.players.update(keys_pressed)

            ### RENDER ###
            self.players.draw(self.app.screen)

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

