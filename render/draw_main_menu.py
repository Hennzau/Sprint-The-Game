# Imports

import pygame

from level.obstacle import colors
from render.box import draw_covered_box, draw_text_box, draw_empty_box

from sound import sound_button, sound_game_launched


def draw_main_menu(surface, menu, game):
    """
    the draw_main_menu function draw the main menu of the game on the given surface
    It also manages actions on the game

    Parameters:
    surface (Surface): the surface on which you want to draw the end menu,
    menu (MainMenu): the MainMenu object you want to draw
    game (Game): the Game object
    """

    # Draw the main menu interface and manage the different buttons
    width, height = surface.width, surface.height
    button_width, button_height = 131, 30

    # Draw the background
    surface.py_surface.fill(colors["darkerblue"])
    backgroud = pygame.image.load('assets/images/Sprint_Background.png')
    surface.py_surface.blit(backgroud, (0, 0))

    # Initialise the different fonts used
    font = pygame.font.Font("assets/fonts/BulletTrace7-rppO.ttf", 60)
    font_levels = pygame.font.Font("assets/fonts/BulletTrace7-rppO.ttf", 30)
    font_switch = pygame.font.SysFont("arial", 30)

    # Show the title inside a box 

    title = font.render('SPRINT THE GAME', True, colors["ivory"])
    start_button = font.render(
        'Select Level to Start', True, colors["ivory"])

    x_title_extended = width / 2 - start_button.get_width() / 2
    y_title_extended = height / 2 - title.get_height() / 2 - 200
    title_extended_width = start_button.get_width()
    title_extended_height = title.get_height() + start_button.get_height() + 25

    draw_text_box(surface.py_surface, x_title_extended, y_title_extended, title_extended_width, title_extended_height)
    surface.py_surface.blit(title, (width / 2 - title.get_width() / 2,
                                    height / 2 - title.get_height() / 2 - 200))

    surface.py_surface.blit(start_button, (width / 2 - start_button.get_width() /
                                           2, height / 2 + start_button.get_height() / 2 - 175))

    # Draw buttons to switch row of levels
    


    increase_button = font_switch.render(">", True, colors["ivory"])
    decrease_button = font_switch.render("<", True, colors["ivory"])
    x1 =  width /2 - decrease_button.get_width() - 2 * decrease_button.get_width()
    x2 =  width /2 - increase_button.get_width() + 3 * increase_button.get_width()
    y = (height + 544)/2 - increase_button.get_height()/2 + 50

    draw_empty_box(surface.py_surface,x1 - 20, y - 20, decrease_button.get_width() + 40, decrease_button.get_height() + 40)
    surface.py_surface.blit(decrease_button, (x1,y))
    draw_empty_box(surface.py_surface, x2 - 20, y - 20, increase_button.get_width() + 40, increase_button.get_height() + 40)
    surface.py_surface.blit(increase_button, (x2,y))

    if pygame.Rect(x1 - 20, y - 20, decrease_button.get_width() + 40, decrease_button.get_height() + 40).collidepoint(pygame.mouse.get_pos()):
        draw_covered_box(surface.py_surface, x1 - 20, y - 20, decrease_button.get_width() + 40, decrease_button.get_height() + 40)
        surface.py_surface.blit(decrease_button, (x1,y))
        sound = False
        if pygame.mouse.get_pressed()[0] and not menu.button1_pressed:
            menu.decrease_cursor(game)
            menu.button1_pressed = True
    else:
        menu.button1_pressed = False

    if pygame.Rect(x2 - 20, y - 20, increase_button.get_width() + 40, increase_button.get_height() + 40).collidepoint(pygame.mouse.get_pos()):
        draw_covered_box(surface.py_surface, x2 - 20, y - 20, increase_button.get_width() + 40, increase_button.get_height() + 40)
        surface.py_surface.blit(increase_button, (x2,y))
        sound = False
        if pygame.mouse.get_pressed()[0] and not menu.button2_pressed :
            menu.increase_cursor(game)
            menu.button2_pressed = True
    else:
        menu.button2_pressed = False
          
    # Draw the levels button, up to 5 per line and 2 lines

    m = len(game.levels) // 10

    if menu.level_cursor < m:
        n = 10
        p = 5
    else:
        n = len(game.levels[menu.level_cursor * 10:])
        if n % 2 == 1:
            p = int(n / 2) + 1
        else:
            p = int(n / 2)

    sound = True  # Check if we have to play the sound when we're over a button

    # Draw the first line

    for i in range(p):
        level = f"Level " + str(i + 1 + menu.level_cursor * 10)
        levels_button = font_levels.render(level, True, colors["ivory"])
        k = width / 2 - 131 / 2 + (- p + 2 * i) * 131 + 131

        draw_empty_box(surface.py_surface, k - 26, height / 2 - (levels_button.get_height() / 2 - 100) - 26,
                       button_width + 52, button_height + 52)
        surface.py_surface.blit(levels_button, (k, height / 2 - (levels_button.get_height() / 2 - 100)))
        # We check if the mouse is over the button

        if pygame.Rect(k - 26, height / 2 - (levels_button.get_height() / 2 - 100) - 26, button_width + 52,
                       button_height + 52).collidepoint(pygame.mouse.get_pos()):

            draw_covered_box(surface.py_surface, k - 26, height / 2 - (levels_button.get_height() / 2 - 100) - 26,
                             button_width + 52, button_height + 52)
            surface.py_surface.blit(levels_button, (k, height / 2 - (levels_button.get_height() / 2 - 100)))

            sound = False

            # We check is the button is pressed and switch to the according game.stage 

            if pygame.mouse.get_pressed()[0]:
                menu.level_selected = i + menu.level_cursor * 10
                menu.start_game = True
                menu.launch_game(game)
                sound_game_launched()

    # We draw the second line the exact same way

    if (n - p) > 0:
        for i in range(n - p):
            level = f"Level " + str(i + p + 1 + menu.level_cursor * 10)
            levels_button = font_levels.render(level, True, colors["ivory"])
            k = width / 2 - 131 / 2 + (-(n - p) + 2 * i) * 131 + 131
            draw_empty_box(surface.py_surface, k - 26, height / 2 - (levels_button.get_height() / 2 - 225) - 26,
                           button_width + 52, button_height + 52)
            surface.py_surface.blit(levels_button, (k, height / 2 - (levels_button.get_height()) / 2 + 225))
            if pygame.Rect(k - 26, height / 2 - (levels_button.get_height() / 2 - 225) - 26, button_width + 52,
                           button_height + 52).collidepoint(pygame.mouse.get_pos()):
                draw_covered_box(surface.py_surface, k - 26, height / 2 - (levels_button.get_height() / 2 - 225) - 26,
                                 button_width + 52, button_height + 52)

                surface.py_surface.blit(levels_button, (k, height / 2 - (levels_button.get_height() / 2 - 225)))

                sound = False

                if pygame.mouse.get_pressed()[0]:
                    menu.level_selected = i + p + menu.level_cursor * 10
                    menu.start_game = True
                    menu.launch_game(game)
                    sound_game_launched()

    # We now draw the "Level Editor" button, the same way the other button were.

    level_editor = font_levels.render("Level Editor", True, colors["ivory"])

    x_lvled, y_lvled = (25, height / 2 - level_editor.get_height() / 2 + 320)

    draw_empty_box(surface.py_surface, x_lvled - 21, y_lvled - 21, level_editor.get_width() + 42,
                   level_editor.get_height() + 42)
    surface.py_surface.blit(level_editor, (x_lvled, y_lvled))

    if pygame.Rect(x_lvled - 21, y_lvled - 21, level_editor.get_width() + 42,
                   level_editor.get_height() + 42).collidepoint(pygame.mouse.get_pos()):
        draw_covered_box(surface.py_surface, x_lvled - 21, y_lvled - 21, level_editor.get_width() + 42,
                         level_editor.get_height() + 42)
        surface.py_surface.blit(level_editor, (x_lvled, y_lvled))

        if pygame.mouse.get_pressed()[0]:
            game.stage = "Level Editor"
            sound_game_launched()

        sound = False

    # We now check if the mouse was over one of the button and if it just entered the button to play the sound

    if not game.sound and not sound:
        game.sound = True
        sound_button()

    # We put back the value "False" if the mouse wasn't in any button

    if sound:
        game.sound = False
