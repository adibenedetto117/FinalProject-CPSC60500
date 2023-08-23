import pygame
from core_functions import *
from pygame.locals import *

# Initialize pygame
pygame.init()

print("Loading section k-2...")

def draw_input_screen():
    screen.fill(BLACK)

    title = large_font.render("Pick a number 1-100", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title, title_rect)

    # Note: This is a simplistic input box, which will only display a prompt.
    # In a full application, you'd likely want a more interactive text input box.
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, 250, 140, 50)
    pygame.draw.rect(screen, WHITE, input_box)

    return input_box  # Return the input box rect for interaction purposes

def draw_output_screen():
    screen.fill(BLACK)

    # Draw all sprites
    all_sprites.draw(screen)
    box_group.draw(screen)


def k2_input_screen():
    global current_number
    typing = True
    number_str = ""

    while typing:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.unicode.isdigit() and len(number_str) < 3:  # ensure max 3 digits
                    number_str += event.unicode
                elif event.key == K_BACKSPACE:
                    number_str = number_str[:-1]
                elif event.key == K_RETURN:
                    current_number = int(number_str)
                    typing = False

        input_box = draw_input_screen()  # Draws the input screen and captures the input box

        number_text = medium_font.render(number_str, True, BLACK)
        number_rect = number_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + 25))
        screen.blit(number_text, number_rect)

        pygame.display.flip()
        clock.tick(60)

    k2_output_screen()

def k2_output_screen():
    global boxes_drawn, robot_position

    button_width, button_height = 150, 40
    button_x = SCREEN_WIDTH - button_width - 10
    button_y = 10
    return_button = pygame.Rect(button_x, button_y, button_width, button_height)

    boxes_drawn = 0
    box_group.empty()
    robot.rect.x = SCREEN_WIDTH // 2 - ROBOT_WIDTH // 2 - BOX_WIDTH - 10
    robot.rect.y = SCREEN_HEIGHT - ROBOT_HEIGHT

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    running = False
                    pygame.event.clear(MOUSEBUTTONDOWN)

        if boxes_drawn < current_number:
            new_box = Box(SCREEN_WIDTH // 2 - BOX_WIDTH // 2,
                          SCREEN_HEIGHT - (boxes_drawn + 1) * (BOX_HEIGHT + SPACING) - ROBOT_HEIGHT)
            box_group.add(new_box)

            robot.rect.y -= (BOX_HEIGHT + SPACING)
            boxes_drawn += 1

        draw_output_screen()  # This replaces the older screen.fill(BLACK)

        pygame.draw.rect(screen, GRAY, return_button)
        button_text = medium_font.render("Return to Menu", True, BLACK)
        button_text_rect = button_text.get_rect(center=return_button.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()
        clock.tick(2)

    while True:
        draw_output_screen()

        pygame.draw.rect(screen, GRAY, return_button)
        button_text = medium_font.render("Return to Menu", True, BLACK)
        button_text_rect = button_text.get_rect(center=return_button.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    boxes_drawn = 0
                    return

        clock.tick(60)