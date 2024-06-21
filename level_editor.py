import pygame as py
import pygame.mouse

import utils
import player
import json


class LevelEditor():
    def __init__(self, app):
        self.app = app
        self.path = "data/levels/level_editor_"
        self.level = utils.json_load(self.path + "load.json")

        # prevents any failed level load being erred below
        if not self.level:
            return

        self.dt = 1
        self.keys_pressed = None

        self.mouse_down_pos = None

        self.players = py.sprite.Group()
        self.walls = []

        for info in self.level["players"]:
            player_obj = player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), ["colour"], self.players)
        # for wall_info in self.level["walls"]:
        #     wall =

    def run(self):
        # If level is not loaded, return to menu
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
                    if event.key == py.K_e:
                        walls_dict = {"walls": []}
                        for wall in self.walls:
                            walls_dict["walls"].append({
                                "x": wall.x,
                                "y": wall.y,
                                "width": wall.width,
                                "height": wall.height,
                            })

                        # Write to json
                        with open(self.path + "export.json", "w") as write:
                            json.dump(walls_dict, write, indent=2)

                if event.type == py.MOUSEBUTTONDOWN:
                    self.mouse_down_pos = event.pos
                if event.type == py.MOUSEBUTTONUP and self.mouse_down_pos:
                    size = (event.pos[0] - self.mouse_down_pos[0], event.pos[1] - self.mouse_down_pos[1])
                    wall = pygame.Rect(self.mouse_down_pos, size)
                    self.walls.append(wall)
                    self.mouse_down_pos = None

            ### LOGIC ###
            self.keys_pressed = py.key.get_pressed()

            self.players.update()

            ### RENDER ###
            self.players.draw(self.app.screen)
            for wall in self.walls:
                py.draw.rect(self.app.screen, (255, 255, 255), wall)

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

