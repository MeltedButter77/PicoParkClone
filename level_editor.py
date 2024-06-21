import pygame as py
import pygame.mouse

import utils
import player
import json


class LevelEditor:
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
        self.display_rect = None
        self.selected_rect = None

        self.players = py.sprite.Group()
        self.walls = []

        for info in self.level["players"]:
            player_obj = player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), self.players)
        for wall_info in self.level["walls"]:
            self.walls.append(py.Rect(wall_info["x"], wall_info["y"], wall_info["width"], wall_info["height"]))

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
                        info_dict = {
                            "players": [],
                            "walls": []
                        }
                        for wall in self.walls:
                            info_dict["walls"].append({
                                "x": wall.x,
                                "y": wall.y,
                                "width": wall.width,
                                "height": wall.height,
                            })
                        for player_obj in self.players.sprites():
                            info_dict["players"].append({
                                "x": player_obj.rect.centerx,
                                "y": player_obj.rect.centery,
                                "width": player_obj.rect.width,
                                "height": player_obj.rect.height,
                            })

                        # Write to json
                        with open(self.path + "export.json", "w") as write:
                            json.dump(info_dict, write, indent=2)

                if event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                    for wall in self.walls:
                        if wall.collidepoint(event.pos):
                            self.walls.remove(wall)

                # Create new or select to move
                if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    for wall in self.walls:
                        if wall.collidepoint(event.pos):
                            self.selected_rect = wall

                    if not self.selected_rect:
                        self.mouse_down_pos = (round(event.pos[0], -1), round(event.pos[1], -1))
                        self.display_rect = pygame.Rect((round(self.mouse_down_pos[0], -1), round(self.mouse_down_pos[1], -1)), (event.pos[0] - self.mouse_down_pos[0], event.pos[1] - self.mouse_down_pos[1]))

                # Create New walls (complete & display)
                if event.type == py.MOUSEBUTTONUP and self.mouse_down_pos and event.button == 1:
                    wall = self.display_rect
                    self.walls.append(wall)
                    self.mouse_down_pos = None
                    self.display_rect = None
                if event.type == py.MOUSEMOTION and self.mouse_down_pos and event.buttons[0]:
                    # Determine the top-left and bottom-right points
                    top_left = (round(min(self.mouse_down_pos[0], event.pos[0]), -1), round(min(self.mouse_down_pos[1], event.pos[1]), -1))
                    bottom_right = (round(max(self.mouse_down_pos[0], event.pos[0]), -1), round(max(self.mouse_down_pos[1], event.pos[1]), -1))

                    # Calculate width and height
                    width = bottom_right[0] - top_left[0]
                    height = bottom_right[1] - top_left[1]

                    self.display_rect = pygame.Rect(top_left, (width, height))

                # Move walls (complete & move display)
                if event.type == py.MOUSEMOTION and self.selected_rect:
                    self.selected_rect.center = event.pos
                if event.type == py.MOUSEBUTTONUP and self.selected_rect:
                    self.selected_rect = None

            ### LOGIC ###

            # Round wall locations to nearest 10
            for wall in self.walls:
                wall.x = round(wall.x, -1)
                wall.y = round(wall.y, -1)


            ### RENDER ###
            self.players.draw(self.app.screen)
            for wall in self.walls:
                py.draw.rect(self.app.screen, (255, 255, 255), wall)

            if self.display_rect:
                py.draw.rect(self.app.screen, (255, 0, 0), self.display_rect)

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

