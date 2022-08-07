
import random
import json
import time
from utils import Display, Responses
display = Display()
responses = Responses()

class Mathmatrix:
    def __init__(self):
        self.highscore = 0

    def start(self, name):
        self.user_name = name
        
        self.matrix = self.gen_table(12, [])
        self.pick_items(matrix)
        self.hide_items(matrix)
        self.introtext = f"Hi {self.user_name}. This is a maths games designed to improve times tables recognition and speed. It consists of a standard 12x12 timestables matrix, with some numbers hidden. To play the game, you must enter the hidden numbers as quickly as possible. Note: there is no order in which to enter your numbers"

        display.top()
        display.one_line("Maths Matrix Game")
        display.divider()
        display.split_text(self.introtext)
        if responses.input_continue(): return

        self.game_running = True
        start_time = time.time()

        while self.game_running:
            self.display_table(matrix) # Output function
            self.get_guess() # Input and processing function
            self.check_win() # Processing function

        end_time = time.time()
        time_elapsed = round((end_time - start_time), 2)

        if time_elapsed < self.highscore or self.highscore == 0: 
            self.highscore = time_elapsed

        
        with open('./userdata.json', 'r+') as f:
            data = json.load(f)
            # Looks through every list item in the file to find the user
            # Once found, compares the user's highscore, and updates it if necessary
            for i in data:
                print(i)
                if i["user_name"] == self.user_name:
                    print("user found")
                    if "mathsmatrix_highscore" in i:
                        if i["mathsmatrix_highscore"] < self.highscore: i["mathsmatrix_highscore"] = self.highscore
                        else: self.highscore = i["mathsmatrix_highscore"]
                    else: i["mathsmatrix_highscore"] = self.highscore
            # Goes to the top of the file, writes the updated data to the file, and deletes anything left at the bottom.
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            # Looks through every list item in the file to find the highest score out of all users.
            bestscore_score = 0
            for i in data:
                if "mathsmatrix_highscore" in i: 
                    print(i["mathsmatrix_highscore"])
                    if i["mathsmatrix_highscore"] > bestscore_score or bestscore_score == 0: 
                        bestscore_player = i["user_name"]
                        bestscore_score = i["mathsmatrix_highscore"]

        # Feedback with scores
        display.top()
        display.one_line(f"You completed the game in {time_elapsed} seconds")
        display.one_line(f"Your Best time: {self.highscore}")
        display.one_line(f"Local Best time: {bestscore_score} ({bestscore_player})")
        responses.input_continue()

        responses.ask_to_play_again(self.start, self.user_name)

    def gen_table(self, num, matrix):
        for i in range(num+1):
            matrix.append([])
            for j in range(num+1):
                # Normally these would all result in 0. Replaces it with numbers 1-12 to be column/row headings
                if i == 0: multiplierx = 1
                else: multiplierx = i
                if j == 0: multipliery = 1
                # Else do the normal multiplication
                else: multipliery = j
                matrix[i].append(multiplierx*multipliery)
        # sets first element (top left corner) to be 'x'
        matrix[0][0] = 'x'
        return matrix

    def pick_items(self, table):
        self.hidden_items = []
        items = 0
        # Chooses 5 numbers (items) to hide
        while items <= 5:
            # Picks a random row, and then an item in that row
            row = random.choice(table)
            item = random.choice(row)
            # Passes if the item has already been chosen
            if item in self.hidden_items:
                pass
            else:
                # Adds the item to the list
                self.hidden_items.append(item)
                items += 1

    def hide_items(self, table):
        global matrix
        length = len(table[0])
        for i in self.hidden_items:
            for r in range(length):
                for c in range(length):
                    if r == 0 or c == 0: pass
                    elif table[r][c] == i: table[r][c] = '?'
        matrix = table

    def display_table(self, table):
        global matrix
        table = matrix
        length = len(table[0])
        display.top()
        print(f"║{'Enter the numbers hidden under the question marks'.center(display.width)}║")
        display.divider()
        for row in table:
            firstcolumn = True
            if row == table[0]: 
                pass
            elif row == table[1]:
                print("\n║" + ("═══╬" + "═══╩" * (length-2) + "════").center(display.width) + "║")
            else: 
                print("\n║" + ("═══╣" + "───┼" * (length-2) + "────").center(display.width) + "║")
            for i in row[:-1]:
                if i == row[0] and firstcolumn == True: 
                    print("║" + ' ' * ((display.width-51)//2) + str(i).center(3) + '║', end='')
                    firstcolumn = False
                elif row == table[0]:
                    print(str(i).center(3) + '║', end='')
                
                else: print(str(i).center(3) + '│', end='')
            print(str(row[-1]).center(3), end=' ' * ((display.width-51)//2) + "║")
        print()
        display.bottom()

    def get_guess(self):
        global matrix
        print()
        guess = responses.get_int()
        if responses.check_for_quit(guess): return
        if int(guess) in self.hidden_items:
            display.top()
            display.one_line("Correct!")
            display.bottom()
            self.hidden_items.remove(int(guess))
            print(self.hidden_items)
            original_matrix = self.gen_table(12, [])
            self.hide_items(original_matrix)
        

    def check_win(self):
        if self.hidden_items == []:
            self.game_running = False   
        else: 
            return


            