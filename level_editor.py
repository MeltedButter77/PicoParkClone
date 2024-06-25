import os
import pygame as pg
import pygame.mouse
import game
import utils
import json
import menu
from game_objects import wall


class LevelEditor:
    def __init__(self, app):
        self.app = app

        self.camera = pg.Vector2(0, 0)

        self.dt = 1
        self.keys_pressed = None

        self.input_box = menu.InputBox(80, 25, 140, 32, "blue", "dark blue", "white", font_size=22)

        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.groups = [self.players, self.walls, self.blocks]

    def run(self):
        
        camera_mouse_down = None
        selected_wall = None
        mouse_down_pos = None
        display_rect = None

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                self.input_box.handle_event(event)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return "menu_main"
                    if not self.input_box.active:
                        if event.key == pg.K_s and self.input_box.text:
                            self.export_level_file()
                        if event.key == pg.K_l and self.input_box.text:
                            self.load_level_file()

                # Camera movement
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
                    camera_mouse_down = event.pos
                if event.type == pg.MOUSEBUTTONUP and event.button == 2:
                    camera_mouse_down = None
                if event.type == pg.MOUSEMOTION and event.buttons[1]:
                    if camera_mouse_down:
                        self.camera.x -= event.rel[0]
                        self.camera.y -= event.rel[1]

                # Creation and movement of rects can only happen when the button is not active
                if not self.input_box.active:
                    # Remove walls
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                        for wall_obj in self.walls:
                            if wall_obj.rect.move(self.camera * -1).collidepoint(event.pos):
                                self.walls.remove(wall_obj)

                    # Create new (set mouse_down_pos) or select to move
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        for wall_obj in self.walls:
                            if wall_obj.rect.move(self.camera * -1).collidepoint(event.pos):
                                selected_wall = wall_obj
                        if not selected_wall:
                            mouse_down_pos = (round(event.pos[0], -1), round(event.pos[1], -1))
                            display_rect = pygame.Rect((round(mouse_down_pos[0], -1), round(mouse_down_pos[1], -1)), (event.pos[0] - mouse_down_pos[0], event.pos[1] - mouse_down_pos[1]))

                    # Create New walls (complete & display)
                    if event.type == pg.MOUSEBUTTONUP and mouse_down_pos and event.button == 1:
                        if display_rect.width > 0 and display_rect.height > 0:
                            wall.Wall(self, (display_rect.x + self.camera.x, display_rect.y + self.camera.y), (display_rect.width, display_rect.height), self.walls)
                        mouse_down_pos = None
                        display_rect = None
                    if event.type == pg.MOUSEMOTION and mouse_down_pos and event.buttons[0]:
                        # Determine the top-left and bottom-right points
                        top_left = (round(min(mouse_down_pos[0], event.pos[0]), -1), round(min(mouse_down_pos[1], event.pos[1]), -1))
                        bottom_right = (round(max(mouse_down_pos[0], event.pos[0]), -1), round(max(mouse_down_pos[1], event.pos[1]), -1))

                        # Calculate width and height
                        width = bottom_right[0] - top_left[0]
                        height = bottom_right[1] - top_left[1]

                        display_rect = pygame.Rect(top_left, (width, height))

                    # Move walls (complete & move display)
                    if event.type == pg.MOUSEMOTION and selected_wall:
                        selected_wall.rect.center = event.pos + self.camera
                    if event.type == pg.MOUSEBUTTONUP and selected_wall:
                        selected_wall = None

            ### LOGIC ###
            self.keys_pressed = pg.key.get_pressed()
            self.move_camera(self.keys_pressed)

            # Round wall locations to nearest 10
            for wall_obj in self.walls:
                wall_obj.rect.x = round(wall_obj.rect.x, -1)
                wall_obj.rect.y = round(wall_obj.rect.y, -1)

            ### RENDER ###
            for group in self.groups:
                for obj in group:
                    obj.draw(self.app.screen)
            if display_rect:
                pygame.draw.rect(self.app.screen, (255, 255, 255), display_rect)

            self.input_box.draw(self.app.screen)

            pg.display.update()
            self.app.screen.fill("light blue")
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

    def export_level_file(self):
        info_dict = {
            "players": [],
            "walls": [],
            "blocks": [],
        }
        for wall_obj in self.walls.sprites():
            info_dict["walls"].append({
                "x": wall_obj.rect.x,
                "y": wall_obj.rect.y,
                "width": wall_obj.rect.width,
                "height": wall_obj.rect.height,
            })
        for player_obj in self.players.sprites():
            info_dict["players"].append({
                "x": player_obj.rect.centerx,
                "y": player_obj.rect.centery,
                "width": player_obj.rect.width,
                "height": player_obj.rect.height,
            })
        for block_obj in self.blocks.sprites():
            info_dict["blocks"].append({
                "x": block_obj.rect.centerx,
                "y": block_obj.rect.centery,
                "width": block_obj.rect.width,
                "height": block_obj.rect.height,
                "push_amount": block_obj.push_amount,
            })

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path = f"data/levels/level_{self.input_box.text}.json"
        # Write to json
        with open(path, "w") as write:
            json.dump(info_dict, write, indent=2)

    def load_level_file(self):
        # Clear current sprites
        for group in self.groups:
            group = pg.sprite.Group()

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        path = f"data/levels/level_{self.input_box.text}.json"
        level_info = utils.json_load(path)
        game.load_level(self, level_info)

    def move_camera(self, keys_pressed):
        if keys_pressed[pg.K_LEFT]:
            self.camera.x -= 10
        if keys_pressed[pg.K_RIGHT]:
            self.camera.x += 10
        if keys_pressed[pg.K_UP]:
            self.camera.y -= 10
        if keys_pressed[pg.K_DOWN]:
            self.camera.y += 10

