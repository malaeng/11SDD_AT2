# Created by Malachi English 15/8/22
# Game select and help function. This is the program that is run to access the other programs.

# NOTICE: keep in mind screen size when running the program. 
# A too small screen size could result in weird/messy output, due to the borders.

# Complete project can be found here: 
# If running yourself, ensure all .py and .json files are located in the same directory.

import textwrap
import json
# Imports all the classes from other files.
from connect4 import ConnectFour
from mathsmatrix import Mathmatrix
from timestables import Timestables
from utils import Display, Responses

connectfour = ConnectFour()
mathsmatrix = Mathmatrix()
timestables = Timestables()

display = Display()
responses = Responses()

class Main:
    
    def start(self):
        while True:
            print()
            print()
            print("This program uses borders")
            print("Having a small screen size could mess up the output.")
            print("Ensure the below arrow does not wrap around the screen:")
            print()
            print("<" + "-" * (display.width+1) + ">")
            print()
            print("Press Enter to continue...")
            input()
            # Asks for user's name and stores it in 'self.username'
            print(textwrap.dedent(f"""\
                ╔{'═' * display.width}╗
                ║{' Please Enter your name '.center((display.width))}║
                ╚{'═' * display.width}╝"""))
            self.user_name = input('> ').title()

            

            if self.user_name == '':
                # Ensures User does not press enter without entering a name.
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))

            else: break

        with open('./userdata.json', 'r+') as f:
            data = json.load(f)
            user_exists = False
            for i in data:
                if i["user_name"] == self.user_name: user_exists = True
            if user_exists == False: data.append({"user_name": self.user_name})
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        self.main()

    def main(self):
        # Says hello to user.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{(' Hello, ' + self.user_name).center((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Gives options to user.
        print(textwrap.dedent(f"""\
            ╔{'═' * display.width}╗
            ║{' Please select an option using the numbers provided '.center((display.width))}║
            ╠{'═' * display.width}╣
            ║{'   (1) Help '.ljust((display.width))}║
            ║{'   (2) Connect Four '.ljust((display.width))}║
            ║{'   (3) Maths Matrix Game '.ljust((display.width))}║
            ║{'   (4) Timestables Practice '.ljust((display.width))}║
            ║{'   (5) Quit '.ljust((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Runs program correlating with input number.
        while True:
            choice = input('> ')
            if choice == '1':
                self.help()
                break
            elif choice == '2':
                connectfour.start(self.user_name)
                break
            elif choice == '3':
                mathsmatrix.start(self.user_name)
                break
            elif choice == '4':
                timestables.start(self.user_name)
                break
            elif choice == '5' or choice in responses.quit_responses:
                quit()
            else:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))
        self.main()

    def help(self):
        file = open("./help.json")
        help_text = json.load(file)
        file.close()
        # Prints info on the program as a whole, then gives options for user to selectively learn about more in detail.
        display.top()
        display.split_text(help_text["help_blurb"])
        print(textwrap.dedent(f"""\
            ║{' ' * display.width}║
            ║{'   (1) Back to game select '.ljust((display.width))}║
            ║{'   (2) Connect Four '.ljust((display.width))}║
            ║{'   (3) Maths Matrix Game '.ljust((display.width))}║
            ║{'   (4) Times Tables Practice '.ljust((display.width))}║
            ╚{'═' * display.width}╝"""))

        # Gives information on the option the user selected.
        while True:
            choice = input('> ')
            if choice == '1':
                self.main()
                break
            elif choice == '2':
                display.top()
                display.split_text(help_text["connect_four"])
                if responses.input_continue(): return
                break
            elif choice == '3':
                display.top()
                display.split_text(help_text["maths_matrix"])
                if responses.input_continue(): return
                break
            elif choice == '4':
                display.top()
                display.split_text(help_text["timestables"])
                if responses.input_continue(): return
                break
            elif choice in responses.quit_responses:
                quit()
            else:
                print(textwrap.dedent(f"""\
                    ╔{'═' * display.width}╗
                    ║{' Invalid input '.center((display.width))}║
                    ╚{'═' * display.width}╝"""))
        self.help()


# Runs the program.
if __name__ == '__main__':
    main = Main()
    main.start()