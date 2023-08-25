import pygame
from core_functions import *
from pygame.locals import *

print("Loading section 3-5...")

def Three5_input_screen():
    """
    Input screen for 3-5 grade level. Users choose between three functions (2x, x^2, or 2^x)
    and then input a number between 1 and 100.
    """
    global current_number, function_selected
    typing = False
    number_str = ""

    btn_2x = pygame.Rect(SCREEN_WIDTH // 3 - 45, 250, 90, 40)
    btn_x2 = pygame.Rect(SCREEN_WIDTH // 2 - 45, 250, 90, 40)
    btn_2powerx = pygame.Rect(2 * SCREEN_WIDTH // 3 - 45, 250, 90, 40)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == MOUSEBUTTONDOWN:
                # Check which function button is clicked
                if btn_2x.collidepoint(event.pos):
                    function_selected = '2x'
                elif btn_x2.collidepoint(event.pos):
                    function_selected = 'x2'
                elif btn_2powerx.collidepoint(event.pos):
                    function_selected = '2^x'
                else:
                    # If the user clicks outside any function, reset the selection
                    function_selected = None

            if event.type == KEYDOWN:
                if not typing and function_selected:  # Start typing only if a function has been selected
                    typing = True
                if typing:
                    if event.unicode.isdigit() and len(number_str) < 3:
                        number_str += event.unicode
                    elif event.key == K_BACKSPACE:
                        number_str = number_str[:-1]
                    elif event.key == K_RETURN and number_str:  # Ensure there is some number entered
                        current_number = int(number_str)
                        Three5_output_screen()  # This will transition to the output screen
                        return function_selected, current_number  # Return the selected function and number

        draw_background()

        title = large_font.render("Pick a function", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Draw buttons with active selection highlighted
        pygame.draw.rect(screen, WHITE if function_selected != '2x' else GRAY, btn_2x)
        pygame.draw.rect(screen, WHITE if function_selected != 'x2' else GRAY, btn_x2)
        pygame.draw.rect(screen, WHITE if function_selected != '2^x' else GRAY, btn_2powerx)

        # Put function text on the buttons
        fx_text = medium_font.render('2x', True, BLACK)
        screen.blit(fx_text, (btn_2x.x + 30, btn_2x.y + 10))

        fx2_text = medium_font.render('x^2', True, BLACK)
        screen.blit(fx2_text, (btn_x2.x + 30, btn_x2.y + 10))

        f2powerx_text = medium_font.render('2^x', True, BLACK)
        screen.blit(f2powerx_text, (btn_2powerx.x + 10, btn_2powerx.y + 10))

        # If a function is selected, show the input box for number
        if function_selected:
            title = large_font.render("Input a number for x", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title, title_rect)

            number_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, 320, 140, 50)
            pygame.draw.rect(screen, WHITE, number_box)

            number_text = medium_font.render(number_str, True, BLACK)
            number_rect = number_text.get_rect(center=number_box.center)
            screen.blit(number_text, number_rect)

        pygame.display.flip()
        clock.tick(60)

def Three5_output_screen():
    """
    Output screen for 3-5 grade level. Displays the graph created by the chosen function
    and number. A robot places boxes along the curve.
    """
    print("Entered Three5_output_screen function.")  # Debugging print statement

    # This implementation assumes you've already defined plotting mechanisms for these functions.
    # Place boxes based on function and input number
    draw_background()

    print("About to draw_function_curve_and_boxes.")  # Debugging print statement
    # Draw the function curve and boxes
    draw_function_curve_and_boxes(function_selected, current_number)
    print("Finished drawing_function_curve_and_boxes.")  # Debugging print statement

    #Button variables
    btn_margin = 10  # margin between buttons
    btn_height = 40  # height of the buttons

    # Draw a "Return to Main Menu" button
    btn_return = pygame.Rect(SCREEN_WIDTH - 210, SCREEN_HEIGHT - btn_margin - btn_height, 200, btn_height)

    while True:  # This keeps the output screen running until an event takes you out of it
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == MOUSEBUTTONDOWN:
                if btn_return.collidepoint(event.pos):  # if the return button was clicked
                    return  # exit the function and return to the main menu
                elif btn_clear.collidepoint(event.pos):
                    draw_background  # This clears the screen
                    drawn_boxes_positions.clear()  # This clears the boxes' positions
                    # Any other clearing functionality goes here (e.g. resetting lists, counters, etc.)
                if event.type == MOUSEBUTTONDOWN:
                    if btn_input.collidepoint(event.pos):
                        Three5_input_screen()
                        draw_background

        # Remaining code to draw the screen elements...
        # Draw a "Main Menu" button
        pygame.draw.rect(screen, WHITE, btn_return)
        return_text = medium_font.render("Return to Main Menu", True, BLACK)
        return_rect = return_text.get_rect(center=btn_return.center)
        screen.blit(return_text, return_rect)

        # Draw a "Clear Data" button below the return button
        btn_clear = pygame.Rect(SCREEN_WIDTH - 210, btn_return.top - btn_margin - btn_height, 200, btn_height)
        pygame.draw.rect(screen, WHITE, btn_clear)
        clear_text = medium_font.render("Clear Data", True, BLACK)
        clear_rect = clear_text.get_rect(center=btn_clear.center)
        screen.blit(clear_text, clear_rect)

        #Draw a "Return to Input" button below the clear button
        btn_input = pygame.Rect(SCREEN_WIDTH - 210, btn_clear.top - btn_margin - btn_height, 200, btn_height)
        pygame.draw.rect(screen, WHITE, btn_input)
        input_text = medium_font.render("Input More Data", True, BLACK)
        input_rect = input_text.get_rect(center=btn_input.center)
        screen.blit(input_text, input_rect)

        pygame.display.flip()
        clock.tick(60)
