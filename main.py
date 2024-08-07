import pygame as pg
import menu
import game
import level_editor


class App:
    def __init__(self):
        pg.init()
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((1000, 600), pg.SCALED)
        self.clock = pg.time.Clock()
        self.fps = 60

        self.fullscreen = False

        self.active_game = None
        self.selected_mode = menu.Menu(self, menu="menu_main").run()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            while True:
                match self.selected_mode:
                    case "button_quit":
                        pg.quit()
                        quit()

                    case "level_editor":
                        self.active_game = level_editor.LevelEditor(self)
                        self.selected_mode = self.active_game.run()

                    case str(x) if "play_level_" in x:
                        self.active_game = game.Game(self)
                        self.selected_mode = self.active_game.run()

                    case "option_fullscreen":
                        if not self.fullscreen:
                            self.screen = pg.display.set_mode(self.screen.get_size(), pg.FULLSCREEN | pg.SCALED)
                            self.fullscreen = True
                        else:
                            self.screen = pg.display.set_mode(self.screen.get_size(), pg.SCALED)
                            self.fullscreen = False
                        self.selected_mode = "menu_options"

                    # if the button does not return an action case
                    # send button's id to the menu selector
                    case _:
                        # Handle invalid menu case
                        if self.selected_mode is None:
                            self.selected_mode = "menu_main"
                        self.selected_mode = menu.Menu(self, menu=self.selected_mode).run()


app = App()
app.run()
