from core_functions import *
import copy


print("Loading section 6-8...")


#Set up the wrap_text function for all button text wrapping
def wrap_text(text, width):
   """Wraps the text to ensure it doesn't overflow from the screen."""
   font = pygame.font.Font(None, 14)
   words = text.split(' ')  # Changed self.text to text
   lines = []
   while words:
       line = ''
       while words and font.size(line + words[0])[0] <= width:  # Changed self.rect.width to width
           line += (words.pop(0) + ' ')
       lines.append(line)
   return lines

# Define button class for interaction
class Button:
   def __init__(self, x, y, width, height, color, text=''):
       self.rect = pygame.Rect(x, y, width, height)
       self.color = color
       self.text = text


   def wrap_text_method(self):
       return wrap_text(self.text, self.rect.width)


   def draw(self):
       pygame.draw.rect(screen, self.color, self.rect)
       if self.text != '':
           wrapped_text = self.wrap_text_method()  # Remove the 'self.text' argument here
           font = pygame.font.Font(None, 18)  # Reduced font size to 18
           for index, line in enumerate(wrapped_text):
               text_surface = font.render(line, True, WHITE)  # Text color set to white
               text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.y + 10 + index * 20))
               screen.blit(text_surface, text_rect)


   def is_over(self, pos):
       return self.rect.collidepoint(pos)


class Company:
   def __init__(self, name, behavior, stock_value=100):
       self.name = name
       self.behavior = behavior
       self.stock_value = stock_value
       self.history = [stock_value]  # Starts with the initial stock value


   def update_stock(self, event):
       """Updates the company's stock value based on an event."""
       # Use the calculate_stock_changes function to get the new stock value
       self.stock_value = calculate_stock_changes({'name': self.name, 'stock_value': self.stock_value}, event)


       # Append the updated value to the history
       self.history.append(self.stock_value)


   def __repr__(self):
       return f"<Company(name={self.name}, stock_value={self.stock_value:.2f})>"


class Graph:
   def __init__(self, x, y, width, height, data_sets=None):
       self.rect = pygame.Rect(x, y, width, height)
       if data_sets:
           self.max_points = max(2, max(len(data) for data in data_sets))
       else:
           self.max_points = 12


   def draw(self, data_sets, color=WHITE):
       if not data_sets or len(data_sets) == 0 or len(data_sets[0]) < 2:
           return

       max_value = max(max(data) for data in data_sets)
       min_value = min(min(data) for data in data_sets)
       range_value = max_value - min_value

       # If the values are the same, set range to the maximum value to avoid division by zero
       range_value = max_value if range_value == 0 else range_value

       print(f"Max points value: {self.max_points}")
       px_per_point_x = self.rect.width / (self.max_points - 1)
       px_per_point_y = self.rect.height / range_value

       for data_points, color in zip(data_sets, color):
           prev_x, prev_y = None, None
           for index, point in enumerate(data_points):
               current_x = self.rect.x + index * px_per_point_x
               # Reverse y since pygame's y increases downward
               current_y = self.rect.y + self.rect.height - (point - min_value) * px_per_point_y

               if prev_x is not None:
                   pygame.draw.line(screen, color, (prev_x, prev_y), (current_x, current_y), 6)

               prev_x, prev_y = current_x, current_y

class GameState:
   def __init__(self):
       self.month_index = 0
       self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
       self.player_credits = 1000
       self.companies = [
           Company(name='Megacorp', behavior='slow and steady'),
           Company(name='Farming Colony', behavior='steadier, but can be swingy with crops'),
           Company(name='Mining Company', behavior='less steady, swingy with large veins'),
           Company(name='Research Company', behavior='high risk, high reward')
       ]
       self.event_log = []
       self.stocks_owned = {company.name: 0 for company in self.companies}
       self.month_data = []
       self.year = 2552  # Initialize the year at 2552
       self.append_month_summary()


   @property
   def player_credits(self):
       return self._player_credits

   @property
   def current_month(self):
       return self.months[self.month_index]

   @player_credits.setter
   def player_credits(self, value):
       self._player_credits = round(value, 2)

   def get_company_stock(self, company_name):
       for company in self.companies:
           if company.name == company_name:
               return company.stock_value  # Assuming the Company object has a 'stock' attribute that represents the stock value
       return None

   def append_month_summary(self):
       month_summary = {
           "Month": self.current_month,
           "Year": self.year,
           "Player Balance": self.player_credits,
           "Megacorp Stock": self.get_company_stock('Megacorp'),
           "Farming Colony Stock": self.get_company_stock('Farming Colony'),
           "Mining Company Stock": self.get_company_stock('Mining Company'),
           "Research Company Stock": self.get_company_stock('Research Company'),
           "Events": self.event_log[-1] if self.event_log else None,
           "Net Income": self.player_credits - 1000
       }
       self.month_data.append(month_summary)

   def next_month(self):
       if self.month_index < len(self.months) - 1:
           event, warning = generate_monthly_event()
           self.append_month_summary()
           if warning:
               self.event_log.append(warning)
           if event:
               self.event_log.append(event)
           if len(self.event_log) > 3:
               self.event_log.pop(0)
           for company in self.companies:
               company.update_stock(event)
           self.month_index += 1
       else:
           # When we are at December, go to the summary screen
           self.display_summary()
           # Increment the year when December is done
           self.year += 1
           self.month_index = 0  # Reset the month to January
           # When we are at December, go to the summary screen
           self.display_summary()

   def display_summary(self):
       screen.fill(BLACK)

       # Get all companies' histories
       histories = [company.history for company in self.companies]
       colors = [company_colors[company.name] for company in self.companies]

       # Display line graphs for each company
       graph = Graph(10, 50, 640, 240, data_sets=histories)
       for company in self.companies:
           color = company_colors[company.name]  # Fetch the color for this company
           graph.draw([company.history], [color])  # Assuming that the draw function accepts a color tuple

        #  Display a simple legend for each company in the line graph
       font = pygame.font.Font(None, 18)
       for i, company in enumerate(self.companies):
           color = company_colors[company.name]  # Fetch the color for this company
           pygame.draw.line(screen, color, (10, 320 + i * 25), (40, 320 + i * 25), 3)  # Adding '3' for line thickness
           label = font.render(company.name, True, WHITE)
           screen.blit(label, (50, 315 + i * 25))

       # Display company stock details
       start_y = 650 - len(self.companies) * 25 - 25
       for i, company in enumerate(self.companies):
           color = GREEN if company.history[-1] - company.history[0] >= 0 else RED
           text_surface = font.render(
               f"{company.name}: Events={len(self.event_log)}, Change={company.history[-1] - company.history[0]:.2f} cR",
               True, color)
           screen.blit(text_surface, (10, start_y + i * 25))


       # Display player stats on the bottom left
       net_income = self.player_credits - 1000
       color = GREEN if net_income >= 0 else RED
       text_surface = font.render(f"Net Income: {net_income:.2f} cR", True, color)
       screen.blit(text_surface, (10, 650))


       # Buttons on the summary screen
       continue_button = Button(550, 500, 150, 40, (100, 100, 100), "Continue")
       new_game_button = Button(550, 550, 150, 40, (100, 100, 100), "New Game")
       main_menu_button = Button(550, 600, 150, 40, (100, 100, 100), "Main Menu")
       save_data_button = Button(550, 650, 150, 40, (100, 100, 100), "Save Data (.csv)")

       continue_button.draw()
       new_game_button.draw()
       main_menu_button.draw()
       save_data_button.draw()


       running = True
       while running:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False
                   pygame.quit()
               if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                   if continue_button.is_over(pygame.mouse.get_pos()):
                       self.month_index = 0 # Reset the month
                       running = False
                   elif new_game_button.is_over(pygame.mouse.get_pos()):
                       # Reset everything
                       self.__init__()
                       running = False
                   elif main_menu_button.is_over(pygame.mouse.get_pos()):
                       game_state.reset()
                       pygame.event.clear()
                       return "MAIN_MENU"
                   elif save_data_button.is_over(pygame.mouse.get_pos()):
                       save_data_to_csv(game_state)
                       print("Data saved to .csv in Downloads folder")

           pygame.display.flip()


   def reset(self):
       """Reset the game state to its initial state."""
       self.__init__()


game_state = GameState()
initial_game_state = copy.deepcopy(GameState())

class Ticker:
   def __init__(self, x, y, width, height):
       total_height = len(game_state.companies) * 20
       y = (screen.get_height() - total_height) // 2 - 50  # minus 50 moves the ticker up
       self.rect = pygame.Rect(x, y, width, height)


   def draw(self, companies, stocks_owned, stocks_quantity):
       font = pygame.font.Font(None, 28)
       for index, company in enumerate(companies):
           color = WHITE
           if len(company.history) >= 2:  # At least two data points to compare
               if company.history[-1] > company.history[-2]:
                   color = GREEN
               elif company.history[-1] < company.history[-2]:
                   color = RED


           text_surface = font.render(f"{company.name}: {company.stock_value:.2f} | Owned: {stocks_owned[company.name]} | Supply: {stocks_quantity[company.name]}", True, color)
           screen.blit(text_surface, (self.rect.x, self.rect.y + index * 20))


def game_loop():
   global game_state
   clock = pygame.time.Clock()
   running = True
   buttons = []


   # Define buy/sell buttons
   companies_names = [company.name for company in game_state.companies]
   button_width = 150
   gap = (720 - (len(companies_names) * button_width)) / (len(companies_names) + 1)


   for i, name in enumerate(companies_names):
       x_pos = int(gap + i * (button_width + gap))
       buttons.append(Button(x_pos, 450, button_width, 50, GREEN, f'Buy {name}'))
       buttons.append(Button(x_pos, 510, button_width, 50, RED, f'Sell {name}'))


   advance_button = Button(300, 600, 120, 70, (100, 100, 100), "Next Month")
   stock_ticker = Ticker(screen.get_width() * 0.25 - 110, screen.get_height() // 2 - 50, 220, 100)


   while running:
       screen.fill(BLACK)


       # Display static elements


       font = pygame.font.Font(None, 24)
       # Display player credits
       credits_text = font.render(f'Credits: {game_state.player_credits} cR', True, WHITE)


       screen.blit(credits_text, (10, 10))


       # Display stock ticker
       stock_ticker.draw(game_state.companies, game_state.stocks_owned, stocks_quantity)

       # Display current month and year in the top center
       font = pygame.font.Font(None, 32)
       month_and_year_text = f"{game_state.months[game_state.month_index]} {game_state.year}"
       month_text_surface = font.render(month_and_year_text, True, WHITE)
       screen.blit(month_text_surface, (screen.get_width() // 2 - month_text_surface.get_width() // 2, 10))

       # Display the events on the top right
       for i, log_event in enumerate(reversed(game_state.event_log)):
           font = pygame.font.Font(None, 18)
           wrapped_lines = wrap_text(str(log_event), 330)  # used 220 as an example width
           for j, line in enumerate(wrapped_lines):
               text_surface = font.render(line, True, WHITE)


               # Opacity changes based on the index 'i' of the event
               alpha = 255 - (i * 85)  # Decreasing alpha by 85 for each older event, this can be adjusted as needed
               text_surface.set_alpha(alpha)


               screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 20, 50 + (i * len(wrapped_lines) + j) * 20))


       # Draw buttons
       for button in buttons:
           button.draw()
       advance_button.draw()


       # Check for events
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False


           if event.type == pygame.MOUSEBUTTONDOWN:
               # Check if any button is clicked
               for button in buttons:
                   if button.is_over(pygame.mouse.get_pos()):
                       action, company_name = button.text.split(" ", 1)
                       # Inside the game_loop function, under pygame.MOUSEBUTTONDOWN
                       if action == "Buy":
                           company = next(c for c in game_state.companies if c.name == company_name)
                           if game_state.player_credits >= company.stock_value:
                               game_state.player_credits -= company.stock_value
                               game_state.stocks_owned[company_name] += 1
                               stocks_quantity[company_name] -= 1

                               # Update stocks_transaction_count for buying
                               stocks_transaction_count[company.name] += 1
                           else:
                               game_state.event_log.append("Insufficient funds.")
                               if len(game_state.event_log) > 3:
                                   game_state.event_log.pop(0)
                       elif action == "Sell":
                           company = next(c for c in game_state.companies if c.name == company_name)
                           if game_state.stocks_owned[company_name] > 0:
                               game_state.player_credits += company.stock_value
                               game_state.stocks_owned[company_name] -= 1
                               stocks_quantity[company_name] += 1

                               # Update stocks_transaction_count for selling
                               stocks_transaction_count[company.name] -= 1

               # Check for advancing to the next month
               if advance_button.is_over(pygame.mouse.get_pos()):
                   game_state.next_month()
                   if game_state.month_index == len(game_state.months):  # Check if current month is December
                       action = game_state.display_summary()
                       if action == "MAIN_MENU":
                           return "MAIN_MENU"  # This will break out of game_loop and go to main menu


       # Update the screen with everything drawn
       pygame.display.flip()


       clock.tick(60)


   pygame.quit()


if __name__ == '__main__':
    game_state = initial_game_state  # Set the current game state to the initial state
    action = game_loop()

    if action == "MAIN_MENU":
        # Here, call your main menu function
        main()  # Assuming you have a function called main_menu for the main menu screen



