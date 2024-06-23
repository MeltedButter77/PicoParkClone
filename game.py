import pygame as py
import utils
import player


class Game:
    def __init__(self, app):
        self.app = app
        self.level = utils.json_load("data/levels/level_" + app.selected_mode.split("_")[2] + ".json")

        self.camera = py.Vector2(0, 0)

        # prevents any failed level load being erred below
        if not self.level:
            return

        self.dt = 1
        self.keys_pressed = None

        self.players = py.sprite.Group()
        self.walls = []

        for i, info in enumerate(self.level["players"]):
            controls = None

            # Player controls should be imported from json, for now they are all stored here
            if i == 0:
                controls = [py.K_w, py.K_a, py.K_s, py.K_d]
            elif i == 1:
                controls = [py.K_UP, py.K_LEFT, py.K_DOWN, py.K_RIGHT]
            elif i == 2:
                controls = [py.K_i, py.K_j, py.K_k, py.K_l]

            if controls:
                player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), controls, self.players)
            else:
                print("not enough controls defined for player", i + 1)
        for wall_info in self.level["walls"]:
            wall = py.Rect(wall_info["x"], wall_info["y"], wall_info["width"], wall_info["height"])
            self.walls.append(wall)

    def run(self):
        # If level is not loaded, return to menu
        if not self.level:
            return "menu_main"
        mouse_down = None

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        return "menu_main"
                    self.players.update(event)

                if event.type == py.MOUSEBUTTONDOWN:
                    mouse_down = event.pos
                if event.type == py.MOUSEBUTTONUP:
                    mouse_down = None
                if event.type == py.MOUSEMOTION:
                    if mouse_down:
                        self.camera.x -= event.rel[0]
                        self.camera.y -= event.rel[1]

            ### LOGIC ###
            self.keys_pressed = py.key.get_pressed()

            self.players.update()

            ### RENDER ###
            for wall in self.walls:
                display_rect = wall.copy()
                display_rect.topleft = [wall[i] - self.camera[i] for i in range(2)]
                py.draw.rect(self.app.screen, (0, 0, 0), display_rect)
            for player_obj in self.players.sprites():
                player_obj.draw(self.app.screen, self.camera)

            # Update screen
            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
