import pygame as pg
import utils
from game_objects import block, player, wall


def load_level(game, level_info):
    if not level_info:
        print("failed to load level")
        return

    if "players" in level_info.keys():
        for i, info in enumerate(level_info["players"]):
            controls = None

            # Player controls should be imported from json, for now they are all stored here
            if i == 0:
                controls = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
            elif i == 1:
                controls = [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]
            elif i == 2:
                controls = [pg.K_i, pg.K_j, pg.K_k, pg.K_l]

            if controls:
                gravity = "down"
                if i == 0:
                    gravity = "up"
                player.Player(game, (info["x"], info["y"]), (info["width"], info["height"]), gravity, controls, game.players)
            else:
                print("not enough controls defined for player", i + 1)

    if "walls" in level_info.keys():
        for wall_info in level_info["walls"]:
            wall.Wall(game, (wall_info["x"], wall_info["y"]), (wall_info["width"], wall_info["height"]), game.walls)

    if "blocks" in level_info.keys():
        for block_info in level_info["blocks"]:
            block.PushBlock(game, block_info, game.blocks)


class Game:
    def __init__(self, app):
        self.app = app
        level_info = utils.json_load("data/levels/level_" + app.selected_mode.split("_")[2] + ".json")

        self.camera = pg.Vector2(0, 0)

        self.dt = 0
        self.keys_pressed = None

        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.groups = [self.players, self.walls, self.blocks]

        load_level(self, level_info)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return "menu_main"
                    self.players.update(event)

            ### LOGIC ###
            self.keys_pressed = pg.key.get_pressed()

            self.move_camera()
            self.players.update()
            self.blocks.update()

            ### RENDER ###
            for group in self.groups:
                for obj in group:
                    obj.draw(self.app.screen)

            # Update screen
            pg.display.update()
            self.app.screen.fill("light blue")
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

    def move_camera(self):
        # Calculate average position of all players and set as camera origin
        total_players_pos = pg.Vector2(0, 0)
        for player_obj in self.players.sprites():
            total_players_pos += player_obj.pos

        try:
            average_pos = total_players_pos / len(self.players.sprites()) - pg.Vector2(self.app.screen.get_size()) / 2
        except ZeroDivisionError:
            average_pos = (0, 0)

        self.camera = pg.Vector2(average_pos)
