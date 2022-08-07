# Created by Malachi English 15/8/22

# Connect four grid is 6x7

from utils import Display, Responses
display = Display()
responses = Responses()

class ConnectFour:

    def start(self, name):
        self.game_running = True
        self.name = name
        self.grid = []
        self.grid_w = 7
        self.grid_h = 6
        self.introtext = f"Hi {name}. This game is a digital, text-based recreation of 'connect four'. It is a two player game, where the aim is to get four in a row (horizontally, vertically or diagonally), by dropping tokens into any of the seven columns."

        self.tokens = {
            "Player One": "X",
            "Player Two": "O"
        }
        self.players = {
            self.tokens["Player One"]: "Player One",
            self.tokens["Player Two"]: "Player Two"
        }

        # Creates the 6x7 grid - every element is ' ' at this stage
        for i in range(self.grid_h):
            self.grid.append([])
            for j in range(self.grid_w):
                self.grid[i].append(' ')

        # Introduction
        display.top()
        display.split_text(self.introtext)
        if responses.input_continue(): return

        while self.game_running:
            self.display_grid() # Output function
            self.add_token(self.tokens["Player One"]) # Input and processing function
            self.check_win(self.tokens["Player One"]) # Processing function
            if self.game_running:
                self.display_grid()
                self.add_token(self.tokens["Player Two"])
                self.check_win(self.tokens["Player Two"])

    def display_grid(self):
        # Message above grid
        display.top()
        display.one_line('Enter the number corresponding with your selected column (1-7)')
        display.divider()

        # Prints the top line of the grid
        print('║' + ' ' * ((display.width-29)//2) + '┌───' + '┬───'*6 + '┐' + ' ' * ((display.width-29)//2) + '║')

        # Loops through each row in the grid
        # For each row, it prints:
        # The outside border (left)
        # The inside border of the grid
        # each element seperated by grid lines, then the outside border (right)
        # The dividing lines below
        for i in self.grid:
            print('║' + ' ' * ((display.width-29)//2), end='')
            print('│ ', end='')
            print(*i, sep=' │ ', end=(' │' + ' ' * ((display.width-29)//2) + '║\n'))
            print('║' + ' ' * ((display.width-29)//2) + '├───' + '┼───'*6 + '┤'+ ' ' * ((display.width-29)//2) + '║')

        # Prints the outside border (left)    
        print('║' + ' ' * ((display.width-29)//2) + '│', end='')

        # Prints the selection numbers (1-7) 
        for i in range(self.grid_w):
            print((' ' + str(i+1)), end=' │')
        print(' ' * ((display.width-29)//2) + '║')

        display.bottom()

    def add_token(self, token):
        while True:
            # Gets user input
            location = responses.get_int()
            if responses.check_for_quit(location): return

            # Ensures numbers are within the range of 1-7
            if 1 <= location <= 7: break
            else:
                display.top() 
                display.one_line("Please enter a number between 1 and 7")
                display.bottom()
            
        # Loops through the numbers 6-0 (decreasing)    
        for i in range(6, 0, -1):
            # The lowest row it finds an empty space, it places the token
            if self.grid[i-1][location-1] == ' ': 
                self.grid[i-1][location-1] = token
                break
            # Once the loop has reached 1, it means the column is full.
            if i == 1: 
                display.top()
                display.one_line("column full")
                display.bottom()
                self.add_token(token)

    def check_win(self, token):
        win_type = ''
        # Check for horizontal win |
        # For every tile except the last three columns, checks the three tiles to it's right
        for y in range(self.grid_h-3):
            for x in range(self.grid_w):
                if self.grid[y][x] == token and self.grid[y+1][x] == token and self.grid[y+2][x] == token and self.grid[y+3][x] == token: 
                    win_type = "vertically (|)"

        # Check for vertical win -
        # For every tile except the last 3 rows, checks the three tiles underneath it.
        for y in range(self.grid_h):
            for x in range(self.grid_w-3):
                if self.grid[y][x] == token and self.grid[y][x+1] == token and self.grid[y][x+2] == token and self.grid[y][x+3] == token: 
                    win_type = "horizontally (-)"

        # Check for diagonal win \
        # For every tile except the last three columns and row, checks diagonally downwards to it's right.
        for y in range(self.grid_h-3):
            for x in range(self.grid_w-3):
                if self.grid[y][x] == token and self.grid[y+1][x+1] == token and self.grid[y+2][x+2] == token and self.grid[y+3][x+3] == token: 
                    win_type = "diagonally downwards (\)"

        # Check for diagonal win /
        # For every tile except the first three columns and the last three rows, checks diagonally upwards to it's right
        for y in range(3, self.grid_h):
            for x in range(self.grid_w-3):
                if self.grid[y][x] == token and self.grid[y-1][x+1] == token and self.grid[y-2][x+2] == token and self.grid[y-3][x+3] == token: 
                    win_type = "diagonally upwards (/)"
        
        if win_type != '':
            self.game_running = False
            self.display_grid()
            display.top()
            print(f"║{(self.players[token] + ' (' + token + ') ' + 'got four in a row ' + win_type + ' and won!').center(display.width)}║")
            if responses.input_continue(): return
            responses.ask_to_play_again(self.start, self.name)


    def AI_turn(self):
        pass



