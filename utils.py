# Created by Malachi English DATE
# Contains various variables and functions that are used all across the project.

from dis import dis
import textwrap
import time

class Display:
    def __init__(self):
        # Runs when Display() is initialized.
        # Sets up variables once, at the start.
        self.width = 71
        self.halfwidth = int((self.width / 2) - 0.5)

    def adjust_width(self, new_width):
        self.width = new_width

        # Always makes width an odd number, which makes dividing it in half easier.
        if self.width % 2 == 0: self.width += 1

        # Clamps width between 31 and 201.
        if self.width < 31: self.width = 31
        if self.width > 201: self.width = 201

        self.halfwidth = int((self.width / 2) - 0.5)

    def split_text(self, text):
        words = text.split(' ')
        lines = []
        line = ''
        for i in range(len(words)):
            # checks if word will fit onto the line within the set width
            if len(line) + len(words[i]) < (self.width - 2):
                # Adds the word, plus a space.
                line = line + words[i] + ' '
            else:
                # Fills line with spaces so it is the exact correct length.
                line = line + ' ' * ((self.width - 1) - len(line))
                # Adds this line to the list of lines
                lines.append(line)
                # resets the line variable to nothing, adds the next word.
                line = ''
                line = line + words[i] + ' '
        line = line + ' ' * ((self.width - 1) - len(line))
        # If text has been centered, this makes sure an extra blank line isn't added.
        if line.strip() != '': lines.append(line)
        # Finally, print all the lines within the borders.
        for i in range(len(lines)):
            print("║ " + lines[i] + "║")
    
    def top(self):
        # Prints the top line of the border
        print(f"╔{'═' * self.width}╗")

    def bottom(self):
        # Prints the bottom line of the border
        print(f"╚{'═' * self.width}╝")
        
    def divider(self):
        # Prints a divider line for the border
        print(f"╠{'═' * self.width}╣")

    def one_line(self, text):
        # Prints text within a border on the left and right
        print(f"║{text.center(self.width)}║")

class Responses:
    def __init__(self):
        # Runs when Responses() is initialized.
        # Sets up variables once, at the start.
        self.quit_responses = ["q", "quit", "exit"]
        self.positive_responses = ["yes", "ye", "y", "yeah", "yea", "affirmative", "sure", "ok", "okay", "yep"]
        self.negative_responses = ["no", "n", "nah", "nup", "noo"]

    def input_continue(self):
        # Usage: if responses.input_continue(): return
        # Calling the function normally will not return to menu properly.
        display = Display()
        print(textwrap.dedent(f"""\
            ║{' ' * display.width}║
            ║{f"(Press enter to continue)".center(display.width)}║
            ╚{'═' * display.width}╝"""))
        # Any input except for any in 'quit_responses' will cause the program to continue.
        if self.check_for_quit(input()): 
            return True
        else: 
            return False

    def ask_to_play_again(self, start_function, name):
        display = Display()
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{'Would you like to play again?'.center(display.width)}║
            ╠{'═' * display.halfwidth}╦{'═' * display.halfwidth}╣
            ║{'[1] (Y)ES'.center(display.halfwidth)}║{'[2] (N)O'.center(display.halfwidth)}║
            ╚{'═' * display.halfwidth}╩{'═' * display.halfwidth}╝"""))
        while True:
            response = input('> ')
            if self.check_for_quit(response): return
            if response.lower() in self.positive_responses or response == '1':
                # Runs the function passed in to this function as a variable.
                # (Often the first function in the program, or the start program)
                start_function(name)
                break
            elif response.lower() in self.negative_responses or response == '2':
                # Goes back to main menu.
                break
            else:
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' Please Try Again '.center((display.width-2), '!')} ║
                    ╚{'═' * display.width}╝"""))
    
    def check_for_quit(self, input_value):
        # Usage: 
        # if responses.check_for_quit(input_value): return
        display = Display()
        if str(input_value).lower() in self.quit_responses:
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║ {' Quitting To Menu '.center((display.width-2), ' ')} ║
                ╚{'═' * display.width}╝"""))
            time.sleep(0.6)
            return True
        else:
            return False

    def get_int(self):
        display = Display()
        while True:
            num = input("> ")
            # removes whitespace from input and checks if it is a digit. 
            if num.strip().isdigit():
                return int(num.strip())     
            elif num.strip() in self.quit_responses:
                return num.strip()   
            else:
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' Invalid Input. Please try again. '.center((display.width-2), '!')} ║
                    ╚{'═' * display.width}╝"""))