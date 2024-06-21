import pygame as py
import menu
import level


class App():
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((800, 800), py.SCALED)
        self.clock = py.time.Clock()
        self.fps = 60

        self.active_game = None
        self.selected_mode = menu.Menu(self, menu="menu_main").run()

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()

            while True:
                match self.selected_mode:
                    case "button_quit":
                        py.quit()
                        quit()

                    case str(x) if "play_level_" in x:
                        self.selected_mode = level.Level(self, self.selected_mode).run()

                    case "option_fullscreen":
                        self.screen = py.display.set_mode((800, 800), py.FULLSCREEN)

                    # if the button does not return an action case
                    # send button's id to the menu selector
                    case _:
                        self.selected_mode = menu.Menu(self, menu=self.selected_mode).run()

                        # Handle invalid menu case
                        if self.selected_mode is None:
                            self.selected_mode = menu.Menu(self, menu="main_menu").run()


app = App()
app.run()
