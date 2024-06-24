import pygame as pg
import pygame.mouse
import utils
import player
import json
import wall
import menu


class LevelEditor:
    def __init__(self, app):
        self.app = app

        self.camera = pg.Vector2(0, 0)

        self.dt = 1
        self.keys_pressed = None

        self.input_box = menu.InputBox(10, 10, 140, 32)

        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()

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
                            self.export()
                        if event.key == pg.K_l and self.input_box.text:
                            self.load()

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
            for wall_obj in self.walls:
                wall_obj.draw(self.app.screen, self.camera)
            for player_obj in self.players:
                player_obj.draw(self.app.screen, self.camera)
            if display_rect:
                pygame.draw.rect(self.app.screen, (255, 255, 255), display_rect)

            self.input_box.draw(self.app.screen)

            pg.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

    def export(self):
        info_dict = {
            "players": [],
            "walls": []
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

        path = f"data/levels/level_{self.input_box.text}.json"
        # Write to json
        with open(path, "w") as write:
            json.dump(info_dict, write, indent=2)

    def load(self):
        # Clear current sprites
        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        path = f"data/levels/level_{self.input_box.text}.json"
        level_info = utils.json_load(path)

        if not level_info:
            print("failed to load level")
            return

        if level_info["players"]:
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
                    player.Player(self, (info["x"], info["y"]), (info["width"], info["height"]), controls, self.players)
                else:
                    print("not enough controls defined for player", i + 1)
        else:
            print("no players in level")

        if level_info["walls"]:
            for wall_info in level_info["walls"]:
                wall.Wall(self, (wall_info["x"], wall_info["y"]), (wall_info["width"], wall_info["height"]), self.walls)
        else:
            print("no walls in level")

    def move_camera(self, keys_pressed):
        if keys_pressed[pg.K_LEFT]:
            self.camera.x -= 10
        if keys_pressed[pg.K_RIGHT]:
            self.camera.x += 10
        if keys_pressed[pg.K_UP]:
            self.camera.y -= 10
        if keys_pressed[pg.K_DOWN]:
            self.camera.y += 10

