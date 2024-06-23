import pygame as py
import utils
import player


class Game():
    def __init__(self, app):
        self.app = app
        self.level = utils.json_load("data/levels/level_" + app.selected_mode.split("_")[2] + ".json")

        # prevents any failed level load being erred below
        if not self.level:
            return

        self.dt = 1
        self.keys_pressed = None

        self.players = py.sprite.Group()
        self.walls = []

        for info in self.level["players"]:
            player_obj = player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), self.players)
        for wall_info in self.level["walls"]:
            wall = py.Rect(wall_info["x"], wall_info["y"], wall_info["width"], wall_info["height"])
            self.walls.append(wall)

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

                    if event.key == py.K_w:
                        self.players.update(event)

            ### LOGIC ###
            self.keys_pressed = py.key.get_pressed()

            self.players.update()

            ### RENDER ###
            for wall in self.walls:
                py.draw.rect(self.app.screen, (0, 0, 0), wall)
            self.players.draw(self.app.screen)

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

