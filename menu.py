import pygame as py
import utils


class Button:
    def __init__(self, screen, center_x, center_y, width, height, border, curve, buttonColour, textColour, hoverColour, id, text, font='freesansbold.ttf', font_size=80, text_offset=0):
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
        self.width = width
        self.height = height
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

        button_info = utils.json_load("data/buttons/buttons.json")[menu]
        self.buttons = []
        for button in button_info:
            self.buttons.append(
                Button(screen, button["x"], button["y"], button["width"], button["height"], button["border"], button["curve"], button["buttonColour"], button["textColour"], button["hoverColour"], button["id"], button["text"], button["font"], button["font_size"], button["text_offset"])
            )

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
