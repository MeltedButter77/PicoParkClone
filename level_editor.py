import pygame as pg
import pygame.mouse
import utils
import player
import json
import wall


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.active_colour = "blue"
        self.inactive_colour = "dark blue"
        self.font = pg.font.Font(None, 32)

        self.rect = pg.Rect(x, y, w, h)
        self.color = self.inactive_colour
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_colour if self.active else self.inactive_colour
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class LevelEditor:
    def __init__(self, app):
        self.app = app
        self.path = "data/levels/level_editor_"
        self.level = utils.json_load(self.path + "load.json")

        self.camera = pg.Vector2(0, 0)

        # prevents any failed level load being erred below
        if not self.level:
            return

        self.dt = 1
        self.keys_pressed = None

        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        for i, info in enumerate(self.level["players"]):
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
        for wall_info in self.level["walls"]:
            wall.Wall(self, (wall_info["x"], wall_info["y"]), (wall_info["width"], wall_info["height"]), self.walls)

    def run(self):
        # If level is not loaded, return to menu
        if not self.level:
            return "menu_main"
        
        camera_mouse_down = None
        selected_wall = None
        mouse_down_pos = None
        display_rect = None

        input_box = None
        input_result = None

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if input_box:
                    input_result = input_box.handle_event(event)
                    if input_result:
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

                        path = "data/levels/level_" + input_result + ".json"
                        # Write to json
                        with open(path, "w") as write:
                            json.dump(info_dict, write, indent=2)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return "menu_main"
                    if event.key == pg.K_e:
                        input_box = InputBox(10, 10, 140, 32)

                # Camera movement
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
                    camera_mouse_down = event.pos
                if event.type == pg.MOUSEBUTTONUP and event.button == 2:
                    camera_mouse_down = None
                if event.type == pg.MOUSEMOTION and event.buttons[1]:
                    if camera_mouse_down:
                        self.camera.x -= event.rel[0]
                        self.camera.y -= event.rel[1]

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

            if input_box:
                input_box.update()
                input_box.draw(self.app.screen)

            pg.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

    def move_camera(self, keys_pressed):
        if keys_pressed[pg.K_LEFT]:
            self.camera.x -= 10
        if keys_pressed[pg.K_RIGHT]:
            self.camera.x += 10
        if keys_pressed[pg.K_UP]:
            self.camera.y -= 10
        if keys_pressed[pg.K_DOWN]:
            self.camera.y += 10

