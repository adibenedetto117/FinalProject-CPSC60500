import pygame
import random
from decimal import Decimal, ROUND_UP


print("Initializing core functionality...")

# This file has all the core logic and the controller for the program in it.

def linear_growth(initial_value, growth_rate, steps):
    """
    Calculate linear growth based on initial value, growth rate, and steps.

    :param initial_value: Starting value.
    :param growth_rate: Fixed amount to increase by each step.
    :param steps: Number of steps to calculate growth for.
    :return: List of values after each step.
    """
    values = [initial_value]
    for _ in range(steps):
        values.append(values[-1] + growth_rate)
    return values

# Growth of 1 starting from 0 for 10 steps
#print(linear_growth(0, 1, 10))

def exponential_growth(initial_value, growth_rate, steps):
    """
    Calculate exponential growth based on initial value, growth rate, and steps.

    :param initial_value: Starting value.
    :param growth_rate: Percentage rate to increase by each step (e.g., 0.05 for 5%).
    :param steps: Number of steps to calculate growth for.
    :return: List of values after each step.
    """
    values = [initial_value]
    for _ in range(steps):
        values.append(values[-1] * (1 + growth_rate))
    return values

# 5% growth starting from 1 for 10 steps
#print(exponential_growth(1, 0.05, 10))

def logistic_growth(initial_value, growth_rate, carrying_capacity, steps):
    """
    Calculate logistic growth based on initial value, growth rate, carrying capacity, and steps.

    :param initial_value: Starting value.
    :param growth_rate: Maximum rate of growth.
    :param carrying_capacity: Maximum sustainable population.
    :param steps: Number of steps to calculate growth for.
    :return: List of values after each step.
    """
    values = [initial_value]
    for _ in range(steps):
        delta = growth_rate * values[-1] * (1 - values[-1] / carrying_capacity)
        values.append(values[-1] + delta)
    return values

# Bacteria growth in a petri dish starting with 10 bacteria, growth rate of 0.2, carrying capacity of 1000, for 50 steps
#print(logistic_growth(10, 0.2, 1000, 50))

def get_grade_selection():
    """
    Captures user input for grade selection.
    :return: Grade as a string (K-2, 3-5, or 6-8).
    """
    while True:
        grade = input("Select the grade range (K-2, 3-5, or 6-8): ").strip().lower()
        if grade in ['k-2', '3-5', '6-8']:
            return grade
        else:
            print("Invalid grade range. Please enter a correct grade range.")

def get_growth_function_choice():
    """
    Captures user input for growth function choice.
    :return: Growth function choice as a string (linear, exponential, or logistic).
    """
    while True:
        choice = input("Choose a growth function (linear, exponential, logistic): ").strip().lower()
        if choice in ['linear', 'exponential', 'logistic']:
            return choice
        else:
            print("Invalid choice. Please choose a valid growth function.")

def execute_growth_function(choice):
    """
    Executes the growth function based on user choice and provides the results.
    :param choice: Growth function choice.
    :return: Growth values as a list.
    """
    if choice == 'linear':
        # These values can be further modified to be dynamic based on user input
        return linear_growth(0, 1, 10)
    elif choice == 'exponential':
        return exponential_growth(1, 0.05, 10)
    elif choice == 'logistic':
        return logistic_growth(10, 0.2, 1000, 50)

"""
def main():
    grade = get_grade_selection()
    choice = get_growth_function_choice()
    result = execute_growth_function(choice)
    print(f"Results for {choice} growth: \n", result)

# If this file is being run as the main program, the main function will execute
if __name__ == "__main__":
    main()
"""

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exponentials Final Project")
clock = pygame.time.Clock()

# Fonts
large_font = pygame.font.SysFont('Arial', 36, bold=True)
medium_font = pygame.font.SysFont('Arial', 24)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

#Other constants
MAX_BOXES = 1000
BOX_WIDTH = 10
BOX_HEIGHT = 10
ROBOT_WIDTH = 20
ROBOT_HEIGHT = 20
SPACING = 5  # space between boxes
robot_position = [SCREEN_WIDTH // 2 - BOX_WIDTH // 2, SCREEN_HEIGHT - BOX_HEIGHT * 2]
drawn_boxes_positions = []

all_sprites = pygame.sprite.Group()
box_group = pygame.sprite.Group()

#Global variable for current box count and selected number
boxes_drawn = 0
current_number = 0
function_selected = None

class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Create a simple robot rectangle for representation
        self.image = pygame.Surface([ROBOT_WIDTH, ROBOT_HEIGHT])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - ROBOT_WIDTH // 2 - BOX_WIDTH - 10  # 10 pixels offset from box
        self.rect.y = SCREEN_HEIGHT - ROBOT_HEIGHT

    def update(self):
        # For simplicity, if the robot's position updates, reflect it in its rect position
        self.rect.x = robot_position[0]
        self.rect.y = robot_position[1]


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Create a simple box rectangle
        self.image = pygame.Surface([BOX_WIDTH, BOX_HEIGHT])
        self.image.fill(BROWN)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

robot = Robot()
all_sprites.add(robot)

def move_robot_to(target_position, frames):
    """
    Yield positions for the robot to move it smoothly from its current position to the target.

    :param target_position: List of [x, y] coordinates for the target position.
    :param frames: Number of frames over which to complete the move.
    :yield: New [x, y] position for each frame.
    """
    global robot_position

    # Determine the movement needed in each frame
    dx = (target_position[0] - robot_position[0]) / frames
    dy = (target_position[1] - robot_position[1]) / frames

    for _ in range(frames):
        # Update robot's current position
        robot_position[0] += dx
        robot_position[1] += dy
        yield robot_position  # this allows the caller function to get the new position and update the display

    # Ensure the final position is exactly the target, to avoid any floating point inaccuracies.
    robot_position = target_position
    yield robot_position


def draw_function_curve_and_boxes(function_selected, current_number):
    # Define some constants for the graph, like space between points, size of boxes, etc.
    BOX_SIZE = 10
    SPACE_BETWEEN_POINTS = 1  # Adjust as per your graph size and screen width
    GRAPH_OFFSET_X = 30  # These offset the start of the graph so the boxes don't spawn on the edge of the window
    GRAPH_OFFSET_Y = -30

    # Calculate curve points and store in a list
    curve_points = []
    if function_selected == '2x':
        curve_points = [(i, 2 * i) for i in range(current_number + 1)]
    elif function_selected == 'x2':
        curve_points = [(i, i ** 2) for i in range(current_number + 1)]
    elif function_selected == '2^x':
        curve_points = [(i, 2 ** i) for i in range(current_number + 1)]

    for point in curve_points:
        x, y = point
        screen_x = GRAPH_OFFSET_X + x * SPACE_BETWEEN_POINTS  # Convert function input to screen x-coordinate
        screen_y = SCREEN_HEIGHT - y * SPACE_BETWEEN_POINTS + GRAPH_OFFSET_Y  # Convert function output to screen y-coordinate

        # Calculate target position for the robot
        target_x = screen_x - robot.rect.width
        target_y = screen_y

        # Move the robot smoothly to this position
        for robot_position in move_robot_to([target_x, target_y],
                                            30):  # 30 is an example for frames, adjust for desired speed
            # Clear the entire screen to remove the robot's previous position
            screen.fill(BLACK)

            # Redraw all the stationary elements (like the already placed boxes)
            for box_position in drawn_boxes_positions:
                pygame.draw.rect(screen, BROWN, box_position)

            # Update and redraw the robot in its new position
            robot.rect.x, robot.rect.y = robot_position
            all_sprites.update()
            all_sprites.draw(screen)

            pygame.display.flip()
            pygame.time.wait(10)  # you can adjust this wait time to make the robot move faster/slower

        # Now, draw the box only once after the robot has reached its position
        pygame.draw.rect(screen, BROWN, (screen_x, screen_y, BOX_SIZE, BOX_SIZE))
        drawn_boxes_positions.append((screen_x, screen_y, BOX_SIZE, BOX_SIZE))
        pygame.display.flip()  # Update the screen

def draw_output_screen():
    screen.fill(BLACK)

    # Draw all sprites
    all_sprites.draw(screen)
    box_group.draw(screen)

#6-8 Stuff below
# Event Definitions and probabilities
events = {
    'Solar Flares': {
        'affected': 'all',
        'effect': (-20, -10),  # max decrease, min decrease
        'probability': 1,
        'warning': "Increased solar activity detected. Possible solar flares incoming!"
    },
    'Alien Artifact Discovered': {
        'affected': ['Research Company', 'Megacorp'],
        'effect': (5, 20),  # min increase, max increase
        'probability': 3,
        'warning': "Unidentified object found in deep space."
    },
    'Meteoric Mineral Boom': {
            'affected': 'Mining Company',
            'effect': (10, 25),  # max decrease, min decrease
            'probability': 3,
            'warning': "Mining probes have been experiencing higher than normal readings."
    },
    'Intergalactic Pest Infestation': {
        'affected': ['Farming Colony'],
        'effect': (-20, -5),  # min increase, max increase
        'probability': 3,
        'warning': "Farmers are starting to complain more about pests."
    },
    'Cosmic Tech Fair': {
            'affected': ['Research Company', 'Megacorp'],
            'effect': (10, 20),  # max decrease, min decrease
            'probability': 4,
            'warning': "The Cosmic Tech Fair is next month!"
    },
    'Galactic Trade Embargo': {
        'affected': ['Farming Colony', 'Megacorp'],
        'effect': (-25, -3),  # min increase, max increase
        'probability': 3,
        'warning': "Political tensions between some planets are rising."
    },
    'Research Breakthrough': {
            'affected': 'Research Company',
            'effect': (50, 100),  # max decrease, min decrease
            'probability': 1,
            'warning': "Researchers say they may have discovered something big."
    },
    'Asteroid Collision Alert': {
        'affected': 'all',
        'effect': (-20, -5),  # min increase, max increase
        'probability': 2,
        'warning': "A large asteroid heading on a collision course with a major space station has been detected!"
    },
    'Discovery of New Livable Planet': {
            'affected': ['Farming Colony', 'Mining Company'],
            'effect': (50, 100),  # max decrease, min decrease
            'probability': 5,
            'warning': "Deep space explorers say they have found something big."
    },
    'Space Pirate Activity Increase': {
        'affected': 'all',
        'effect': (-20, -5),  # min increase, max increase
        'probability': 5,
        'warning': "Space Pirates have seem to be getting bolder."
    }
    # ... (Add other events similarly)
}

no_event_streak = 0 # Sets the variable to 0 so that events can become more likely the long there isn't one
current_month = 0
yearly_events = []

stocks_quantity = {
    'Megacorp': 500,
    'Farming Company': 500,
    'Mining Company': 500,
    'Research Company': 500
}


def generate_monthly_event():
    global current_month, yearly_events

    # if it's a new year or the game has just started
    if current_month == 0:
        yearly_events = pregenerate_events_for_year()

    event = yearly_events[current_month]
    current_month = (current_month + 1) % 12  # advance the month, reset to 0 if it's a new year

    # Return the event and its warning for the next month
    if current_month < 11:  # if it's not December
        next_event = yearly_events[current_month]
        if next_event:  # if there's an event next month
            warning = events[next_event]['warning']
            return event, warning
    return event, None



def pregenerate_events_for_year():
    events_for_year = []
    global no_event_streak

    for _ in range(12):  # For each month
        threshold = 10 + no_event_streak  # increasing probability of event

        rand_num = random.randint(1, 100)
        cumulative_prob = 0
        generated_event = None  # Default to no event
        for event, details in events.items():
            cumulative_prob += details['probability']
            if rand_num <= cumulative_prob:
                generated_event = event
                no_event_streak = 0  # reset streak
                break
        if not generated_event:
            no_event_streak += 5  # increase the streak multiplier

        events_for_year.append(generated_event)

    return events_for_year

def calculate_stock_changes(company, event_name):
    """
    Adjusts stock values based on the company and the event.
    """
    if not event_name:  # If there's no event, a normal fluctuation occurs
        change = random.uniform(-7, 7) / 100
        return company['stock_value'] * (1 + change)

    event = events.get(event_name, None)
    if not event:
        # If for some reason the event_name doesn't match any event in the dictionary
        raise ValueError(f"Unknown event: {event_name}")

    effect_range = event['effect']

    if event['affected'] == 'all' or company['name'] in event['affected']:
        change = random.uniform(effect_range[0], effect_range[1]) / 100
        return company['stock_value'] * (1 + change)

    # If the company is unaffected by the event, a normal fluctuation occurs
    change = random.uniform(-7, 7) / 100
    return company['stock_value'] * (1 + change)
