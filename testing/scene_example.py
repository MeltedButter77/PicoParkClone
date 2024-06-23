import pygame
pygame.init()

def main():
    screen = pygame.display.set_mode((800, 400))
    scene = "scene_menu"
    while True:
        if scene == "scene_menu":
            scene = menu(screen)
        elif scene == "scene_game":
            scene = game(screen)
        elif scene == "scene_shop":
            scene = shop(screen)

def menu(screen):
    # Draw the game scene.
    txt_font = pygame.font.SysFont('timesnewroman', 40)
    menu_txt = txt_font.render("This is the menu", False, (0, 0, 0))
    menu_opt_a = txt_font.render("Press A to return to the game", False, (0, 0, 0))
    menu_opt_b = txt_font.render("Press B to return to the shop", False, (0, 0, 0))
    screen.fill((0, 255, 0))  # A green game.
    screen.blit(menu_txt, (200, 50))
    screen.blit(menu_opt_a, (100, 200))
    screen.blit(menu_opt_b, (100, 300))
    pygame.display.update()

    while True:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:    # Go to game if you press A.
                    scene = "scene_game"
                    return scene
                elif event.key == pygame.K_b:  # Go to shop if you press B.
                    scene = "scene_shop"
                    return scene

def game(screen):
    # Draw the game scene.
    txt_font = pygame.font.SysFont('timesnewroman', 40)
    game_txt = txt_font.render("This is the game", False, (0, 0, 0))
    game_opt_a = txt_font.render("Press A to return to the menu", False, (0, 0, 0))
    game_opt_b = txt_font.render("Press B to return to the shop", False, (0, 0, 0))
    screen.fill((0, 0, 255))  # A blue game.
    screen.blit(game_txt, (200, 50))
    screen.blit(game_opt_a, (100, 200))
    screen.blit(game_opt_b, (100, 300))
    pygame.display.update()

    while True:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:    # Go to menu if you press A.
                    scene = "scene_menu"
                    return scene
                elif event.key == pygame.K_b:  # Go to shop if you press B.
                    scene = "scene_shop"
                    return scene

def shop(screen):
    # Draw the shop.
    txt_font = pygame.font.SysFont('timesnewroman', 40)
    shop_txt = txt_font.render("This is the shop", False, (0, 0, 0))
    shop_opt_a = txt_font.render("Press A to return to the game", False, (0, 0, 0))
    shop_opt_b = txt_font.render("Press B to return to the game", False, (0, 0, 0))
    screen.fill((255, 0, 0))  # A red shop.
    screen.blit(shop_txt, (200, 50))
    screen.blit(shop_opt_a, (100, 200))
    screen.blit(shop_opt_b, (100, 300))
    pygame.display.update()

    while True:
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:    # Go to game if you press A.
                    scene = "scene_game"
                    return scene
                elif event.key == pygame.K_b:  # Go to shop if you press B.
                    scene = "scene_menu"
                    return scene


if __name__ == "__main__":
    main()
