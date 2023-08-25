import pygame
from core_functions import *
from pygame.locals import *

import random

random_number = random.randint(1, 9)
number_text = None
number_rect = None

boxh = 20
boxw = 20

k2intro = pygame.mixer.Sound(f"assets/Narrator/k2/k2intro.wav")
k2output = pygame.mixer.Sound(f"assets/Narrator/k2/k2output.wav")

# Initialize pygame
pygame.init()

print("Loading section k-2...")


def pre_render_boxes(initial_count=10):
    global boxes_drawn, robot_position
    
    k2intro.play()
    
    initial_x_position = 100  
    vertical_offset = 20
    
    boxes_drawn = 0
    box_group.empty()
    
    for count in range(initial_count):
        current_x_position = initial_x_position + (boxes_drawn * (10 + 10))
        
        for i in range(boxes_drawn + 1):  
            robot.state = "runRight"

            base_height = (SCREEN_HEIGHT - 160) - top_floor_tiles.get_height()
            new_box_y = base_height - (i + 1) * (10 + SPACING) + vertical_offset

            target_position = [current_x_position, new_box_y]

            for new_position in move_robot_to(target_position, 40):
                robot.rect.x, robot.rect.y = new_position
                draw_output_screen()
                #k2output.play()
                all_sprites.update()
                all_sprites.draw(screen)

                pygame.display.flip()
                pygame.time.wait(10)

            new_box = Box(current_x_position, new_box_y + ROBOT_HEIGHT - vertical_offset,10,10)
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

    title = large_font.render("Pick a number a number K (1-9)", True, WHITE)
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
    Screen where user inputs a number between 1-9.
    """
    global current_number, robot_position, number_text, number_rect
    pre_render_boxes(10)
    typing = True
    number_str = ""

    robot.state = "idle"
    robot_position[0] = 200
    robot_position[1] = 528
    invalid = False
    
    while typing:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == KEYDOWN:
                if event.unicode.isdigit() and len(number_str) < 1:  # ensure max 1 digit
                    number_str += event.unicode
                elif event.key == K_BACKSPACE:
                    number_str = number_str[:-1]
                elif event.key == K_RETURN:
                    current_number = int(number_str)
                    if current_number >= 1 and current_number <= 9:
                        typing = False
                        invalid = False
                        k2output.play()
                    else:
                        print("Invalid input. Please try again.")
                        invalid = True
                        
        input_box = draw_input_screen()  # Draws the input screen and captures the input box
        
        
        all_sprites.update()
        all_sprites.draw(screen)

        if invalid == True:
            invalid_text = "Invalid input (1-9)"
            invalid_text = medium_font.render(invalid_text, True, BLACK)
            invalid_rect = invalid_text.get_rect(center=(SCREEN_WIDTH // 2, 700))  # Place it at the bottom of the screen
            screen.blit(invalid_text, invalid_rect)

        # Then render it using Pygame's font rendering
        number_text = medium_font.render(number_str, True, BLACK)
        number_rect = number_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + 25))  # Place it at the bottom of the screen
        screen.blit(number_text, number_rect)

        pygame.display.flip()
        clock.tick(60)

    k2_output_screen()


def k2_output_screen():
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

    # Variable to keep track of the current number of boxes to draw
    current_stack_count = 1

    if current_number >=5:
        boxw = 5
        boxh = 5
    else:
        boxw = 10
        boxh = 10

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

        current_x_position = initial_x_position + (boxes_drawn * (boxw + 10))

        for i in range(current_stack_count):  
            robot.state = "runRight"

            base_height = (SCREEN_HEIGHT - 160) - top_floor_tiles.get_height()
            new_box_y = base_height - (i + 1) * (boxh + SPACING) + vertical_offset

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
            
            new_box = Box(current_x_position, new_box_y + ROBOT_HEIGHT - vertical_offset, boxw, boxh)
            box_group.add(new_box)

        boxes_drawn += 1

        # Increment the current_stack_count by the current_number
        current_stack_count += current_number  
        
        if boxes_drawn >= 10:  # Limit the number of stacks to 10
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


