import pygame
from core_functions import *
from pygame.locals import *

questions = [
    {"question": "At what x are 2x and x^2 the same?", "answer": "2"},
    {"question": "What x value > 0 is 2^x and x^2 the same?", "answer": "2"},
    # More questions here
]


current_question = 0
correct = "None"

from math import pow 

intro35 = pygame.mixer.Sound(f"assets/Narrator/35/35intro.wav")

print("Loading section 3-5...")

def Three5_input_screen():
    intro35.play()
    global current_number, function_selected, correct, current_question, drawn_boxes_positions
    current_question = 0
    correct = "None"
    


    """
    Input screen for 3-5 grade level. Users choose between three functions (2x, x^2, or 2^x)
    and then input a number between 1 and 100.
    """

    typing = False
    number_str = ""

    x_pos = 100

    draw_function_curve_and_boxes("2x", BROWN,x_pos, 64)
    draw_function_curve_and_boxes("x2", BROWN,x_pos+150, 25)
    draw_function_curve_and_boxes("2^x", BROWN,x_pos+300, 13)
            

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if not typing:  # Start typing only if a function has been selected
                    typing = True
                if typing:
                    if event.unicode.isdigit() and len(number_str) < 4:
                        number_str += event.unicode
                    elif event.key == K_BACKSPACE:
                        number_str = number_str[:-1]
                    if event.key == K_RETURN and number_str:  # Ensure there is some number entered
                        current_number = int(number_str.strip())
                        if current_number > 100 or current_number < 1:
                            correct = "Invalid number entered"
                        elif questions[current_question]["answer"] == str(current_number):
                                correct = "Correct"+ str(current_question)
                                #Three5_output_screen()  # This will transition to the output screen
                                #return current_number  # Return the selected function and number
                        elif questions[current_question]["answer"]!= str(current_number):
                            correct = "Incorrect"
            if correct == "Finished":
                return
        
            
        #Three5_output_screen()  # This will transition to the output screen
            # Return the selected function and number

        draw_background()

        title = large_font.render(questions[current_question]["question"], True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        # Draw buttons with active selection highlighted
        #pygame.draw.rect(screen, WHITE if function_selected != '2x' else GRAY, btn_2x)
        #pygame.draw.rect(screen, WHITE if function_selected != 'x2' else GRAY, btn_x2)
        #pygame.draw.rect(screen, WHITE if function_selected != '2^x' else GRAY, btn_2powerx)

        # Put function text on the buttons
        #fx_text = medium_font.render('2x', True, BLACK)
        #screen.blit(fx_text, (btn_2x.x + 30, btn_2x.y + 10))

        #fx2_text = medium_font.render('x^2', True, BLACK)
        #screen.blit(fx2_text, (btn_x2.x + 30, btn_x2.y + 10))

        #f2powerx_text = medium_font.render('2^x', True, BLACK)
        #screen.blit(f2powerx_text, (btn_2powerx.x + 10, btn_2powerx.y + 10))

        # If a function is selected, show the input box for number
          
        number_box = pygame.Rect(SCREEN_WIDTH // 2 - 70, 320, 140, 50)
        pygame.draw.rect(screen, WHITE, number_box)
        

        number_text = medium_font.render(number_str, True, BLACK)
        number_rect = number_text.get_rect(center=number_box.center)
        screen.blit(number_text, number_rect)

        condition_correct = correct[:-1]

        if correct == "Correct0":
            message_text = small_font.render("Correct! The anwser is 2!", True, BLACK)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 650))
            screen.blit(message_text, message_rect)

            graph = FunctionGraph(screen, x_range=(-2, 3), y_range=(-4, 4), line_width=2, offset_x=50, offset_y=500, graph_width=200, graph_height=100)
            #graph.draw_background((200, 200, 200))  # Light gray background
            graph.draw_ticks(tick_length=5)

            graph.plot_function(f_twotimesx)
            graph.plot_function(f_xtothetwo, color=RED)
        elif correct == "Correct1":
            message_text = small_font.render("Correct! The anwser is 2 as well!", True, BLACK)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 650))
            screen.blit(message_text, message_rect)

            graph = FunctionGraph(screen, x_range=(-2, 3), y_range=(-4, 4), line_width=2, offset_x=50, offset_y=500, graph_width=200, graph_height=100)
            #graph.draw_background((200, 200, 200))  # Light gray background
            graph.draw_ticks(tick_length=5)

            graph.plot_function(f_twotothex)
            graph.plot_function(f_xtothetwo, color=RED)
            
            

        elif correct == "Incorrect":
            message_text = medium_font.render("Incorrect!", True, BLACK)
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 650))
            screen.blit(message_text, message_rect)
        
        
        if questions[current_question]["question"] == questions[len(questions)-1]["question"] and correct == "Correct"+str(current_question):
            btn_next = pygame.Rect(SCREEN_WIDTH // 2 , 250, 370, 40)
            fx_text = medium_font.render('Finished! Return to Main Menu', True, BLACK)
            pygame.draw.rect(screen, GRAY, btn_next)
            screen.blit(fx_text, (btn_next.x + 30, btn_next.y + 10))
            if event.type == MOUSEBUTTONDOWN:
                if btn_next.collidepoint(event.pos):
                    correct = "Finished"
                    drawn_boxes_positions.clear()
                    robot_position = [100,525]
        elif len(questions) > current_question + 1 and condition_correct == "Correct":
            btn_next = pygame.Rect(SCREEN_WIDTH // 2 , 250, 200, 40)
            fx_text = medium_font.render('Next Question', True, BLACK)
            pygame.draw.rect(screen, GRAY, btn_next)
            screen.blit(fx_text, (btn_next.x + 30, btn_next.y + 10))
            if event.type == MOUSEBUTTONDOWN:
                if btn_next.collidepoint(event.pos):
                    current_question +=1
                    correct = "None"
                    current_number = ""



        pygame.display.flip()
        clock.tick(60)

def f_twotimesx(x):
    return 2 * x
def f_xtothetwo(x):
    return x**2
def f_twotothex(x):
    return 2**x

#def Three5_output_screen():
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
    

    # Display the surface
    pygame.display.flip()

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

class FunctionGraph:
    def __init__(self, surface, x_range=(-10, 10), y_range=(-10, 10), line_width=1, offset_x=0, offset_y=0, graph_width=None, graph_height=None):
        self.surface = surface
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.line_width = line_width
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.graph_width = graph_width if graph_width else surface.get_width()
        self.graph_height = graph_height if graph_height else surface.get_height()
        # Initialize zero labeled flag
        self.zero_labeled = False

        # Colors
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)

    def translate_point(self, x, y):
        # Translate and scale the x and y coordinates
        screen_x = int((x - self.x_min) / (self.x_max - self.x_min) * self.graph_width) + self.offset_x
        screen_y = int((self.y_max - y) / (self.y_max - self.y_min) * self.graph_height) + self.offset_y

        return screen_x, screen_y
    
    def draw_background(self, color):
        pygame.draw.rect(self.surface, color, (self.offset_x, self.offset_y, self.graph_width, self.graph_height))

    def draw_ticks(self, tick_interval=1, tick_length=10, label_interval=2):
        font = pygame.font.Font(None, 24)  # Use a default font, size 24

        # Reset zero labeled flag
        self.zero_labeled = False

        for x in range(self.x_min, self.x_max + 1, tick_interval):
            screen_x, screen_y = self.translate_point(x, 0)
            pygame.draw.line(self.surface, self.BLACK, (screen_x, screen_y - tick_length//2), (screen_x, screen_y + tick_length//2))
            
            if x == 0 and not self.zero_labeled:
                text = font.render(str(x), True, self.BLACK)
                self.surface.blit(text, (screen_x - text.get_width() // 2, screen_y + tick_length // 2))
                self.zero_labeled = True
            elif x % label_interval == 0 and x != 0:
                text = font.render(str(x), True, self.BLACK)
                self.surface.blit(text, (screen_x - text.get_width() // 2, screen_y + tick_length // 2))

        for y in range(self.y_min, self.y_max + 1, tick_interval):
            screen_x, screen_y = self.translate_point(0, y)
            pygame.draw.line(self.surface, self.BLACK, (screen_x - tick_length//2, screen_y), (screen_x + tick_length//2, screen_y))

            if y == 0 and not self.zero_labeled:
                text = font.render(str(y), True, self.BLACK)
                self.surface.blit(text, (screen_x + tick_length // 2, screen_y - text.get_height() // 2))
                self.zero_labeled = True
            elif y % label_interval == 0 and y != 0:
                text = font.render(str(y), True, self.BLACK)
                self.surface.blit(text, (screen_x + tick_length // 2, screen_y - text.get_height() // 2))



    def plot_function(self, func, color=None):
        if color is None:
            color = self.BLUE

        last_point = None
        for pixel_x in range(self.offset_x, self.offset_x + self.graph_width):
            x = self.x_min + (self.x_max - self.x_min) * ((pixel_x - self.offset_x) / self.graph_width)
            try:
                y = func(x)
            except:
                continue

            point = self.translate_point(x, y)

            if last_point is not None:
                pygame.draw.line(self.surface, color, last_point, point, self.line_width)

            last_point = point


