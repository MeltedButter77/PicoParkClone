import pygame as py
import pygame.draw


class Button:
    def __init__(self, screen, center_x, center_y, height, width, border, curve, buttonColour, textColour, hoverColour, id, text, font='freesansbold.ttf', font_size=80, text_offset=0):
        py.init()
        py.font.init()
        self.font_size = font_size
        self.font = py.font.Font(font, font_size)
        self.text_offset = text_offset

        self.screen = screen

        x = center_x - width / 2
        y = center_y - height / 2
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border = border
        self.curve = curve
        self.buttonColour = buttonColour
        self.textColour = textColour
        self.hover_colour = hoverColour
        self.id = id
        self.text = text
        self.rect = py.Rect(self.x, self.y, self.width, self.height)

        self.highlighted = False

    def update(self, event):
        if not hasattr(event, "pos"):
            return

        if self.rect.collidepoint(event.pos):
            self.highlighted = True
            if event.type == py.MOUSEBUTTONDOWN:
                return True
        elif not self.rect.collidepoint(event.pos):
            self.highlighted = False

    def draw(self):
        if self.highlighted:
            py.draw.rect(self.screen, self.hover_colour, self.rect, self.border, self.curve)
        else:
            py.draw.rect(self.screen, self.buttonColour, self.rect, self.border, self.curve)

        if self.text != "":
            text_surf = self.font.render(self.text, True, self.textColour)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + self.text_offset))
            self.screen.blit(text_surf, text_rect)


class Menu:
    def __init__(self, app, menu="menu_main"):
        self.app = app
        screen = app.screen

        buttons = {
            "menu_main": [
                Button(screen, 400, 200, 150, 350,  0, 35, "dark green", "white", "green", "menu_level_select", "Play", text_offset=5),
                Button(screen, 400, 400, 150, 350, 0, 35, "dark blue", "white", "blue", "menu_options", "Options", text_offset=5),
                Button(screen, 400, 600, 150, 350, 0, 35, "dark red", "white", "red", "button_quit", "Quit", text_offset=5),
            ],
            "menu_level_select": [
                Button(screen, 200, 200, 150, 150, 0, 35, "dark green", "white", "green", "play_level_1", "1", font_size=100, text_offset=8),
                Button(screen, 400, 200, 150, 150, 0, 35, "dark green", "white", "green", "play_level_2", "2", font_size=100, text_offset=8),
                Button(screen, 600, 200, 150, 150, 0, 35, "dark green", "white", "green", "play_level_2", "2", font_size=100, text_offset=8),
                Button(screen, 400, 600, 100, 200, 0, 35, "dark red", "white", "red", "menu_main", "Back", font_size=60, text_offset=4),
            ],
            "menu_options": [
                Button(screen, 400, 400, 150, 350, 0, 7, "dark blue", "white", "blue", "option_fullscreen", "Fullscreen", text_offset=5),
                Button(screen, 400, 600, 150, 350, 0, 7, "dark red", "white", "red", "menu_main", "Back", text_offset=5),
            ]
        }

        if menu in buttons.keys():
            self.buttons = buttons[menu]
        else:
            self.buttons = []

    def run(self):
        if not self.buttons:
            print("Invalid menu")
            return "menu_main"

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        quit()

                for button in self.buttons:
                    if button.update(event) and button.id:
                        return button.id

            for button in self.buttons:
                button.draw()

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.app.clock.tick(self.app.fps)
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
