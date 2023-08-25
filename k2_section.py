import pygame
from core_functions import *
from pygame.locals import *

import random

random_number = random.randint(1, 9)
number_text = None
number_rect = None

# Initialize pygame
pygame.init()

print("Loading section k-2...")

def pre_render_boxes(initial_count=10):
    global boxes_drawn, robot_position
    
    initial_x_position = 100  
    vertical_offset = 20
    
    boxes_drawn = 0
    box_group.empty()
    
    for count in range(initial_count):
        current_x_position = initial_x_position + (boxes_drawn * (BOX_WIDTH + 10))
        
        for i in range(boxes_drawn + 1):  
            robot.state = "runRight"

            base_height = (SCREEN_HEIGHT - 160) - top_floor_tiles.get_height()
            new_box_y = base_height - (i + 1) * (BOX_HEIGHT + SPACING) + vertical_offset

            target_position = [current_x_position, new_box_y]

            for new_position in move_robot_to(target_position, 40):
                robot.rect.x, robot.rect.y = new_position
                draw_output_screen()

                all_sprites.update()
                all_sprites.draw(screen)

                pygame.display.flip()
                pygame.time.wait(10)

            new_box = Box(current_x_position, new_box_y + ROBOT_HEIGHT - vertical_offset)
            box_group.add(new_box)

            # Play the sound when a box is placed
            #place_sound.play()
        
        boxes_drawn += 1



def draw_input_screen():
    """
    Draw the background and input box on the screen.

    Returns:
        pygame.Rect: The rectangle object representing the input box.
    """
    draw_background()

    title = large_font.render("Pick a number a number K (1-100)", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))  # Adjust the '100' to move vertically
    

    screen.blit(title, title_rect)

    # Note: This is a simplistic input box, which will only display a prompt.
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, 250, 140, 50)
    pygame.draw.rect(screen, WHITE, input_box)

    return input_box  # Return the input box rect for interaction purposes

def draw_output_screen():
    """
    Draw the background, sprites, and boxes on the screen.
    """

    draw_background()

    # Draw all sprites
    all_sprites.draw(screen)
    box_group.draw(screen)



def k2_input_screen():
    """
    Screen where user inputs a number between 1-100.
    """
    global current_number, robot_position, number_text, number_rect
    pre_render_boxes(2)
    typing = True
    number_str = ""

    robot.state = "idle"
    robot_position[0] = 200
    robot_position[1] = 528
  
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

        all_sprites.update()
        all_sprites.draw(screen)

        
        # Then render it using Pygame's font rendering
        number_text = medium_font.render(number_str, True, BLACK)
        number_rect = number_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + 25))  # Place it at the bottom of the screen
        screen.blit(number_text, number_rect)

        pygame.display.flip()
        clock.tick(60)

    k2_output_screen()


def k2_output_screen():
    """
    Screen where robot moves and boxes are drawn based on the user input number.
    """

    global boxes_drawn, robot_position, number_rect, number_text

    

    button_width, button_height = 150, 40
    button_x = SCREEN_WIDTH - button_width - 10
    button_y = 10
    return_button = pygame.Rect(button_x, button_y, button_width, button_height)

    boxes_drawn = 0  # Resetting box count
    box_group.empty()  # Emptying any existing boxes

    # Initial horizontal starting position for the robot
    initial_x_position = 100  

    vertical_offset = 20

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

        # Horizontal position for the new stack
        current_x_position = initial_x_position + (boxes_drawn * (BOX_WIDTH + 10))

        for i in range(boxes_drawn + 1):  # +1 because we want at least one box in each stack
            robot.state = "runRight"

            base_height = (SCREEN_HEIGHT - 160) - top_floor_tiles.get_height()
            new_box_y = base_height - (i + 1) * (BOX_HEIGHT + SPACING) + vertical_offset

            target_position = [current_x_position, new_box_y]

            for new_position in move_robot_to(target_position, 100):
                robot.rect.x, robot.rect.y = new_position
                draw_output_screen()

                all_sprites.update()
                all_sprites.draw(screen)

                pygame.draw.rect(screen, GRAY, return_button)
                button_text = medium_font.render("Return to Menu", True, BLACK)
                button_text_rect = button_text.get_rect(center=return_button.center)
                screen.blit(button_text, button_text_rect)

                pygame.display.flip()
                pygame.time.wait(10)

            new_box = Box(current_x_position, new_box_y + ROBOT_HEIGHT - vertical_offset)
            box_group.add(new_box)


            # Play the sound when a box is placed
            #place_sound.play()

        boxes_drawn += 1
        if boxes_drawn >= current_number:
            running = False

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


