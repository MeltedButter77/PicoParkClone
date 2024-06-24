import pygame as pg
import utils


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.active_colour = "blue"
        self.inactive_colour = "dark blue"
        self.font = pg.font.Font(None, 32)

        self.rect = pg.Rect(x, y, w, h)
        self.color = self.inactive_colour
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_colour if self.active else self.inactive_colour
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
            self.color = self.active_colour if self.active else self.inactive_colour
            self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, screen, center_x, center_y, width, height, border, curve, buttonColour, textColour, hoverColour, id, text, font='freesansbold.ttf', font_size=80, text_offset=0):
        pg.init()
        pg.font.init()
        self.font_size = font_size
        self.font = pg.font.Font(font, font_size)
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
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.highlighted = False

    def update(self, event):
        if not hasattr(event, "pos"):
            return

        if self.rect.collidepoint(event.pos):
            self.highlighted = True
            if event.type == pg.MOUSEBUTTONDOWN:
                return True
        elif not self.rect.collidepoint(event.pos):
            self.highlighted = False

    def draw(self):
        if self.highlighted:
            pg.draw.rect(self.screen, self.hover_colour, self.rect, self.border, self.curve)
        else:
            pg.draw.rect(self.screen, self.buttonColour, self.rect, self.border, self.curve)

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
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()

                for button in self.buttons:
                    if button.update(event) and button.id:
                        return button.id

            for button in self.buttons:
                button.draw()

            pg.display.update()
            self.app.screen.fill((60, 60, 60))
            self.app.clock.tick(self.app.fps)
            pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
