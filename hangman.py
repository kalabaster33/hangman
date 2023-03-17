# Create a hangman game...

import csv
import random
import os
import time
import sys
import tty
import termios

def main():
    player_name = start_screen()

    while True:
        csv_file = select_dif()
        os.system('cls' if os.name == 'nt' else 'clear')
        # pick a category
        list_of_categories = list_category(csv_file)
        print("Please select your category")
#--------------------------------------------------------------------------------------------------#
        for i in range(len(list_of_categories)):
            print(f"{i+1}. {list_of_categories[i]}")
        print("0. Go Back")
        print("H. Show TOP 10 best players")
#--------------------------------------------------------------------------------------------------#
        # pick categories to play and get back list of words
        cat_number = input("Enter a valid choice: ")
        if cat_number == "0":
            continue
        elif cat_number.lower() == "h":
            show_highscores()
            continue

        else:
            list_of_words, header = pick_category(cat_number, list_of_categories, csv_file)
            print(header)
#--------------------------------------------------------------------------------------------------#
        # return a score after function play_round
        # I input the list_of_words to get a random one from it to be played, and header to be written
        # - on the screen (reminder of which category is played)
        score = play_round(list_of_words, header)

        scoreboard = retrieve_scores()
        print(scoreboard)
        highscores = input_highscore(scoreboard, player_name, score)
        write_highscores(highscores)
        print(f"Your score was: {score}")

#--------------------------------------------------------------------------------------------------#
def start_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    greeting_msg = "\nGreetings traveler. Say your name and play\n"
    print(greeting_msg)
    player_name = input("\nEnter name: ")
    print(f"\n             Hello   {player_name}.")
    time.sleep(2)
    return player_name

#--------------------------------------------------------------------------------------------------#
#function for selecting difficulty
# 1 and 2, 1 being easy, 2 being hard.

def select_dif():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n       Please select difficulty level")

    while True:
        selection = input("\n-- 1 -- for EASY           -- 2 -- for HARD\n              -->     ")
        isvalid = [1, 2, 456]
        try:
            if int(selection) not in isvalid:
                raise ValueError
            if selection.isalpha():
                raise ValueError
            if int(selection) == 1:
                return "easy.csv"

            if int(selection) == 2:
                return "hard.csv"

            if int(selection) == 456:
                return "small.csv"

        except ValueError:
            continue
#--------------------------------------------------------------------------------------------------#
# define a list of categories, that is read from the easy.csv or hard.csv file,
# the list of categories can be dynamically updated acroding to the .csv file entries
def list_category(csv_file):
    with open(csv_file, "r") as file:
        data = list(csv.reader(file, delimiter=","))
        return data[0]
#--------------------------------------------------------------------------------------------------#

# show categories
def category(subject, csv_file):
    # the agrument should be compared to a csv file, with header of subjects, and rows of words.
    # open the csv file, and append the words from the selected subject to the list
    category = []
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row[subject]
            category.append(word)
        # return a list of words???
        return category, subject
#--------------------------------------------------------------------------------------------------#
# pick a category
def pick_category(cat_number, list_of_categories, csv_file):
    while True:
        try:
       #     cat_number = input("Enter your choice: ")
            if int(cat_number) in range(1, len(list_of_categories)+1):
                # get the list of words for the selected category
                return category(list_of_categories[int(cat_number)-1], csv_file)
            if cat_number.isalpha() == True:
                raise ValueError
            if int(cat_number) not in range(1, len(list_of_categories)+1):
                raise ValueError


        except ValueError:
            continue


#--------------------------------------------------------------------------------------------------#
# the game algoritm
def word_guess(word, header):
    # define counter (lives)
    lives = 6
    game_word = []
    for i in range(len(word)):
        game_word.append("_ ")

    used_letters = []

    while lives > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(header.upper())
        print("Guess the word: " + "".join(game_word))
        print(f"Lives: {lives}")
        letter = input("Letter: ")
        if len(letter) > 1:
            print("Please enter only one character")
            anykey_screen()
            continue
        if letter.isalpha() == False:
            print("Please enter an aplhabetical character")
            anykey_screen()
            continue
        # check if letter is already used, i.e is it in the used_letters[]?
        if letter in used_letters:
            print(f"You have already used this letter: -- {letter.upper()} --")
            anykey_screen()
            continue
        if letter not in word:
            # append letter to used_letters[], to be able to check if it is used
            letter = letter.lower()
            used_letters.append(letter)

            lives -= 1
            result = "".join(game_word)
            continue

        if letter in word:
            # append letter to used_letters[], to be able to check if it is used
            letter = letter.lower()
            used_letters.append(letter)
            # get the index of the letter in word[]
            indexes = [index for index, item in enumerate(word) if item == letter]

            for i in range(len(indexes)):
                game_word[indexes[i]] = word[indexes[i]]
                result = "".join(game_word)


            if word == "".join(game_word):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"You guessed the word -- {word.upper()} -- Good Job ")
                return 1

        if lives == 0:
            return 0
#--------------------------------------------------------------------------------------------------#
#play a round
# this function will return the highscore of the player after playing for maximum of len(list_of_words) number of times
# i randomly generate a number, which will correspond with an index from list_of_words[]
# after playing the word, I remove it from the list, so it doesn't repeat when playing
# the next round, random will generate a number from 1 to len(list_of_words) - 1, repeating untill i == 0
def play_round(list_of_words, header):
    highscore = 0
    i = len(list_of_words)
    while i > 0:
        index = random.randint(0, i-1)
        word = list_of_words[index].lower().strip().replace(" ", "")
        print(word)
        if word_guess(word, header) == 1:
            highscore += 1
            list_of_words.pop(index)
            i -= 1
            print(f"Great job, you are a waliking library. Your highscore is {highscore}")
            prompt = input("Do you want to try again?  yes/no  ").lower()
            valid_input = ["y", "yes", "n", "no"]

            if prompt not in valid_input:
                while True:
                    try:
                        prompt = input("Please select valid input:  yes/no   ").lower()
                        if prompt not in valid_input:
                            raise ValueError
                    except ValueError:
                        continue

                    break

            if prompt == "y" or prompt == "yes":
                continue
            elif prompt == "n" or prompt == "no":
                os.system('cls' if os.name == 'nt' else 'clear')
                return highscore

        else:
            print(f"You failed to guess the word:  {word.upper()}")
            print(f"\n  Too bad. Try again or change a category\n")
            anykey_screen()
            os.system('cls' if os.name == 'nt' else 'clear')
            return highscore

    print("You guessed all the words from the category. Pick new.")
    time.sleep(3)
    return highscore
#--------------------------------------------------------------------------------------------------#
# this function opens the file score.csv that has all previous games played and appends them to
# an empty list which will be used in the next function, to append a new score to.
def retrieve_scores():
    scoreboard = []
    with open("score.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            score = row["score"]
            scoreboard.append({"name":name, "score":score})

    return scoreboard


#--------------------------------------------------------------------------------------------------#
# this function should append the new player and his score to the populated scoreboard
# and return the scoreboard
def input_highscore(scoreboard, name, score):

    scoreboard.append({"name":name, "score":score})
    return scoreboard

#--------------------------------------------------------------------------------------------------#
#this function rewrites the score.csv file with the new entries
def write_highscores(highscores):
    fieldnames = ["name", "score"]
    with open("score.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in highscores:
            writer.writerow(row)

#--------------------------------------------------------------------------------------------------#
# this function should show highscores
# highscores should be shown sorted by key: score in descending order
def show_highscores():
    os.system('cls' if os.name == 'nt' else 'clear')
    highscores = []
    with open("score.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            highscores.append({"name": row["name"], "score": row["score"]})

        for player in sorted(highscores, key=lambda player: int(player['score']), reverse=True)[:10]:
            print(f"-- {player['name']} has a score of: {player['score']}")

    anykey_screen()
#--------------------------------------------------------------------------------------------------#
# ----- this sets terminal to await for any key stroke to continue with code-----------------------#
def anykey_screen():
        # set terminal into raw mode
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)

    print("Press any key to continue...")
    sys.stdin.read(1) # wait for any key to be pressed

    # restore terminal settings
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    return
#--------------------------------------------------------------------------------------------------#



if __name__ == "__main__":
    main()