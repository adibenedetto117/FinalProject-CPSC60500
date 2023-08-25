import pygame
from core_functions import *

print("Displaying main menu...")

def draw_main_menu(in_main_menu):

    draw_background(in_main_menu)

    title = large_font.render("Choose your grade level", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title, title_rect)

    btn_k2 = pygame.Rect(SCREEN_WIDTH // 2 - 70, 250, 140, 50)
    btn_35 = pygame.Rect(SCREEN_WIDTH // 2 - 70, 320, 140, 50)
    btn_68 = pygame.Rect(SCREEN_WIDTH // 2 - 70, 390, 140, 50)

    pygame.draw.rect(screen, WHITE, btn_k2)
    pygame.draw.rect(screen, WHITE, btn_35)
    pygame.draw.rect(screen, WHITE, btn_68)

#k-2 button
    k2_text = medium_font.render("K-2", True, BLACK)
    k2_text_rect = k2_text.get_rect(center=btn_k2.center)

    screen.blit(k2_text, k2_text_rect)

#3-5 button
    Three5_text = medium_font.render("3-5", True, BLACK)
    Three5_rect = k2_text.get_rect(center=btn_35.center)

    screen.blit(Three5_text, Three5_rect)

#6-8 button
    Six8_text = medium_font.render("6-8", True, BLACK)
    Six8_rect = k2_text.get_rect(center=btn_68.center)

    screen.blit(Six8_text, Six8_rect)

    return btn_k2, btn_35, btn_68