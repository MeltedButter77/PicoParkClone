import pygame as py
import json


class Level:
    def __init__(self, app, level_id):
        py.init()
        self.app = app
        self.level = self.load(level_id)

    def load(self, level_id):
        path = "data/levels/level_" + level_id.split("_")[2] + ".json"
        level_info = json.load(open(path))
        print("Successfully loaded", level_id)
        return level_info

    def run(self):
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