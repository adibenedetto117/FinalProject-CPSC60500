# This file will be the main program with the menu and everything.

import pygame
from pygame.locals import *
from core_functions import *
from k2_section import *
from three5_section import *
#from six8_section import *
from main_menu import *


def main():
    global in_main_menu
    run = True
    in_main_menu = True

    while run:


        if in_main_menu:
            k2_btn, Three5_btn, Six8_btn = draw_main_menu(in_main_menu)

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

            if event.type == MOUSEBUTTONDOWN and in_main_menu:
                if k2_btn.collidepoint(pygame.mouse.get_pos()):
                    in_main_menu = False
                    
                    k2_input_screen()
                    
                    in_main_menu = True  # Reset after returning from k2_input_screen()

                if Three5_btn.collidepoint(pygame.mouse.get_pos()):
                    in_main_menu = False
                    Three5_input_screen()
                    in_main_menu = True

                if Six8_btn.collidepoint(pygame.mouse.get_pos()):
                    in_main_menu = False
                    Six8_input_screen()
                    in_main_menu = True

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


