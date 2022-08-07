import random
import time
import json
import textwrap
from utils import Display, Responses
display = Display()
responses = Responses()


class Timestables:
    def __init__(self):
        self.highscore = 0

    def start(self, name):
        self.game_running = True
        self.user_name = name
        self.correct_answers = 0
        self.introtext = f"Hi {self.user_name}. This is a simple times tables test where you are asked times tables questions 10 at a time. You can select your difficulty, which corresponds to the highest number that may be used in a question."

        display.top()
        display.one_line("Times Tables Test")
        display.divider()
        display.split_text(self.introtext)
        display.bottom()

        self.choose_difficulty()
        self.start_time = time.time()
        questions = 10
        while self.game_running == True and questions > 0:
            questions -= 1
            self.ask_question()

        if self.game_running == True: self.end()

    def end(self):        
        end_time = time.time()
        time_elapsed = round((end_time - self.start_time), 2)

        score = round((self.correct_answers * (100/time_elapsed) * self.difficulty), 2)
        if score > self.highscore: 
            self.highscore = score
        with open('./userdata.json', 'r+') as f:
            data = json.load(f)
            for i in data:
                print(i)
                if i["user_name"] == self.user_name:
                    print("user found")
                    if "timestables_highscore" in i:
                        if i["timestables_highscore"] < self.highscore: i["timestables_highscore"] = self.highscore
                        else: self.highscore = i["timestables_highscore"]
                    else: i["timestables_highscore"] = self.highscore
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

            bestscore_score = 0
            for i in data:
                if "timestables_highscore" in i: 
                    print(i["timestables_highscore"])
                    if i["timestables_highscore"] < bestscore_score or bestscore_score == 0: 
                        bestscore_player = i["user_name"]
                        bestscore_score = i["timestables_highscore"]

        display.top()
        display.one_line("Score:")
        display.one_line(f"Correct Answers: {self.correct_answers}/10")
        display.one_line(f"Difficulty: {self.difficulty}")
        display.one_line(f"Time: {time_elapsed} seconds")
        display.one_line('')
        display.one_line(f"Score: {score}")
        display.one_line(f"Highscore: {self.highscore}")
        display.one_line(f"Local Best Highscore: {bestscore_score} ({bestscore_player})")
        if responses.input_continue(): return

        responses.ask_to_play_again(self.start, self.user_name)

    def choose_difficulty(self):
        while True:
            display.top()
            display.one_line("Please choose a difficulty between 5 and 25. Recommended: 12")
            display.bottom()
            self.difficulty = responses.get_int()
            if responses.check_for_quit(self.difficulty): 
                self.game_running = False
                return
            if 5 <= self.difficulty <= 25:
                display.top()
                display.one_line(f"You have chosen a difficulty of {self.difficulty}")
                if responses.input_continue(): return
                break
            else:
                print(textwrap.dedent(f"""
                    ╔{'═' * display.width}╗
                    ║ {' That number is too big or too small '.center((display.width-2), '!')} ║
                    ╚{'═' * display.width}╝"""))
        print(self.difficulty)

    def ask_question(self):
        num1 = random.randint(1, self.difficulty)
        num2 = random.randint(1, self.difficulty)
        display.top()
        display.one_line(f"What is {num1} x {num2}?")
        display.bottom()
        answer = responses.get_int()
        if responses.check_for_quit(answer): 
            self.game_running = False
            return
        if answer == num1 * num2:
            display.top()
            display.one_line("Correct!")
            display.bottom()
            self.correct_answers += 1 
        else: 
            display.top()
            display.one_line(f"The correct answer is {num1 * num2}.")
            if responses.input_continue(): return

