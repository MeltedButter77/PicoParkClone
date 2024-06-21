import pygame as py
import utils


class Game():
    def __init__(self, app):
        self.app = app
        self.level = utils.json_load("data/levels/level_" + app.selected_mode.split("_")[2] + ".json")

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

            print("Running level")

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.app.clock.tick(self.app.fps)
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

