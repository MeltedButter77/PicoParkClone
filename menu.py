import pygame as py


class Button:
    def __init__(self, screen, x, y, height, width, border, curve, buttonColour, textColour, hoverColour, id, text, font='freesansbold.ttf', font_size=80, font_offset=20):
        py.init()
        py.font.init()
        self.font_size = font_size
        self.font = py.font.Font(font, font_size)
        self.font_offset = font_offset

        self.screen = screen
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

    def update_size(self, app):
        multi_x = app.screen.get_width() / app.screen_default_res[0]
        multi_y = app.screen.get_height() / app.screen_default_res[0]

        self.rect = py.Rect(round(self.x * multi_x), round(self.y * multi_y), round(self.width * multi_x), round(self.height * multi_y))
        self.font.set_point_size(round(self.font_size * multi_x))

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
            text_rect = text_surf.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2 + self.font_offset))
            self.screen.blit(text_surf, text_rect)


class Menu:
    def __init__(self, app, menu="main_menu"):
        self.app = app
        screen = app.screen

        if menu == "main_menu":
            self.buttons = [
                Button(screen, 600, 250, 100, 200,  0, 7, "dark green", "white", "green", "level_select_menu", "Play"),
                Button(screen, 225, 400, 100, 350, 0, 7, "dark blue", "white", "blue", "options_menu", "Options"),
                Button(screen, 300, 550, 100, 200, 0, 7, "dark red", "white", "red", "quit", "Quit"),
            ]
            if self.app.active_game:
                self.buttons.append(Button(screen, 225, 100, 100, 350, 0, 7, "dark green", "white", "green", "resume", "Resume"))

        elif menu == "level_select_menu":
            self.buttons = [
                Button(screen, 50, 50, 150, 150, 0, 7, "dark green", "white", "green", "level_1", "1"),
                Button(screen, 250, 50, 150, 150, 0, 7, "dark green", "white", "green", "level_2", "2"),
                Button(screen, 450, 50, 150, 150, 0, 7, "dark green", "white", "green", "level_2", "2"),
            ]

        elif menu == "options_menu":
            self.buttons = [
                Button(screen, 75, 400, 100, 650, 0, 7, "dark blue", "white", "blue", "", "I do nothing lol"),
                Button(screen, 300, 550, 100, 200, 0, 7, "dark red", "white", "red", "main_menu", "Back"),
            ]

        else:
            self.buttons = []

        for button in self.buttons:
            button.update_size(self.app)

    def run(self):
        if not self.buttons:
            print("Invalid menu")
            return

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()

                if event.type == py.WINDOWRESIZED:
                    self.app.screen = py.display.set_mode((event.x, 1/self.app.screen_ratio * event.x), py.SCALED | py.RESIZABLE)
                    for button in self.buttons:
                        button.update_size(self.app)

                for button in self.buttons:
                    if button.update(event) and button.id:
                        return button.id

            for button in self.buttons:
                button.draw()

            py.display.update()
            self.app.screen.fill((60, 60, 60))
            self.app.clock.tick(self.app.fps)
            py.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
