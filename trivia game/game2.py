import json
import random
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.scores = 0

    def add_points(self):
        self.scores += 1

class Game:
    def __init__(self, questions_file):
        with open("questions.json", "r") as file:
            data = json.load(file)
            self.easy_questions = data["easy_questions"]
            self.medium_questions = data["medium_questions"]
            self.hard_questions = data["hard_questions"]

        self.players = []
        self.current_player_index = 0
        self.level_questions = []

    def add_player(self, name):
        self.players.append(Player(name))

    def choose_level(self):
        print("Level 1 is the easy questions")
        print("Level 2 is the medium questions")
        print("Level 3 is the hard questions")
        while True:
            try:
                choose_level = int(input("Enter the level you want to play: "))
                if choose_level == 1:
                    self.level_questions = self.easy_questions
                elif choose_level == 2:
                    self.level_questions = self.medium_questions
                elif choose_level == 3:
                    self.level_questions = self.hard_questions
                else:
                    raise ValueError
                break
            except ValueError:
                print("Please enter an appropriate number (1, 2, or 3)")

    def ask_question(self, question):
        print(question["question"])
        for index, answer in enumerate(question["answers"]):
            print(f"{index + 1}. {answer}")
        return question["correct_answer"]

    def play_game(self):
        for _ in range(len(self.level_questions)):
            current_player = self.players[self.current_player_index]
            random_index = random.randint(0, len(self.level_questions) - 1)
            question = self.level_questions.pop(random_index)
            correct_answer = self.ask_question(question)
            while True:
                try:
                    choice = int(input("Enter your answer (1-4): "))
                    if 1 <= choice <= 4:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter a number between 1 and 4")
            
            chosen_answer = question["answers"][choice - 1]
            if correct_answer == chosen_answer:
                current_player.add_points()
            else:
                print(f"The turn has progressed to player number {self.current_player_index + 2}")
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_winner(self):
        winner = max(self.players, key=lambda player: player.scores)
        print(f"The winner is {winner.name} with a score of {winner.scores}")

def main():
    parser = argparse.ArgumentParser(description="Quiz Game")
    parser.add_argument("questions_file", help="Path to the JSON file with questions")
    parser.add_argument("num_players", type=int, help="Number of players")
    args = parser.parse_args()

    game = Game(args.questions_file)
    
    for i in range(args.num_players):
        name = input(f"Please enter the name of player {i + 1}: ")
        game.add_player(name)

    game.choose_level()
    game.play_game()
    game.get_winner()

if __name__ == "__main__":
    main()
