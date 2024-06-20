import pygame as py
import menu


class App():
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((1280, 720), py.SCALED | py.RESIZABLE)
        self.screen_default_res = (1280, 720)
        self.screen_ratio = self.screen_default_res[0] / self.screen_default_res[1]
        self.clock = py.time.Clock()
        self.fps = 60

        self.active_game = None
        self.selected_mode = menu.Menu(self, menu="main_menu").run()

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()

            while True:
                match self.selected_mode:
                    case "play":
                        pass
                    case "resume":
                        pass
                    case "quit":
                        py.quit()
                        quit()

                    # if the button does not return an action case
                    # send button's id to the menu selector
                    case _:
                        self.selected_mode = menu.Menu(self, menu=self.selected_mode).run()

                        # Handle invalid menu case
                        if self.selected_mode is None:
                            self.selected_mode = menu.Menu(self, menu="main_menu").run()


app = App()
app.run()
