import pygame as py
import pygame.mouse
import utils
import player
import json
import wall


class LevelEditor:
    def __init__(self, app):
        self.app = app
        self.path = "data/levels/level_editor_"
        self.level = utils.json_load(self.path + "load.json")

        self.camera = py.Vector2(0, 0)

        # prevents any failed level load being erred below
        if not self.level:
            return

        self.dt = 1
        self.keys_pressed = None

        self.players = py.sprite.Group()
        self.walls = py.sprite.Group()

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
            wall.Wall(self, (wall_info["x"], wall_info["y"]), (wall_info["width"], wall_info["height"]), self.walls)

    def run(self):
        # If level is not loaded, return to menu
        if not self.level:
            return "menu_main"
        
        camera_mouse_down = None
        selected_wall = None
        mouse_down_pos = None
        display_rect = None

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

                        # Write to json
                        with open(self.path + "export.json", "w") as write:
                            json.dump(info_dict, write, indent=2)

                # Camera movement
                if event.type == py.MOUSEBUTTONDOWN and event.button == 2:
                    camera_mouse_down = event.pos
                if event.type == py.MOUSEBUTTONUP and event.button == 2:
                    camera_mouse_down = None
                if event.type == py.MOUSEMOTION and event.buttons[1]:
                    if camera_mouse_down:
                        self.camera.x -= event.rel[0]
                        self.camera.y -= event.rel[1]

                # Remove walls
                if event.type == py.MOUSEBUTTONDOWN and event.button == 3:
                    for wall_obj in self.walls:
                        if wall_obj.rect.move(self.camera * -1).collidepoint(event.pos):
                            self.walls.remove(wall_obj)

                # Create new (set mouse_down_pos) or select to move
                if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    for wall_obj in self.walls:
                        if wall_obj.rect.move(self.camera * -1).collidepoint(event.pos):
                            selected_wall = wall_obj
                    if not selected_wall:
                        mouse_down_pos = (round(event.pos[0], -1), round(event.pos[1], -1))
                        display_rect = pygame.Rect((round(mouse_down_pos[0], -1), round(mouse_down_pos[1], -1)), (event.pos[0] - mouse_down_pos[0], event.pos[1] - mouse_down_pos[1]))

                # Create New walls (complete & display)
                if event.type == py.MOUSEBUTTONUP and mouse_down_pos and event.button == 1:
                    wall.Wall(self, (display_rect.x + self.camera.x, display_rect.y + self.camera.y), (display_rect.width, display_rect.height), self.walls)
                    mouse_down_pos = None
                    display_rect = None
                if event.type == py.MOUSEMOTION and mouse_down_pos and event.buttons[0]:
                    # Determine the top-left and bottom-right points
                    top_left = (round(min(mouse_down_pos[0], event.pos[0]), -1), round(min(mouse_down_pos[1], event.pos[1]), -1))
                    bottom_right = (round(max(mouse_down_pos[0], event.pos[0]), -1), round(max(mouse_down_pos[1], event.pos[1]), -1))

                    # Calculate width and height
                    width = bottom_right[0] - top_left[0]
                    height = bottom_right[1] - top_left[1]

                    display_rect = pygame.Rect(top_left, (width, height))

                # Move walls (complete & move display)
                if event.type == py.MOUSEMOTION and selected_wall:
                    selected_wall.rect.center = event.pos + self.camera
                if event.type == py.MOUSEBUTTONUP and selected_wall:
                    selected_wall = None

            ### LOGIC ###
            self.keys_pressed = py.key.get_pressed()
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

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.dt = self.app.clock.tick(self.app.fps) / 1000
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))

    def move_camera(self, keys_pressed):
        if keys_pressed[py.K_LEFT]:
            self.camera.x -= 10
        if keys_pressed[py.K_RIGHT]:
            self.camera.x += 10
        if keys_pressed[py.K_UP]:
            self.camera.y -= 10
        if keys_pressed[py.K_DOWN]:
            self.camera.y += 10

