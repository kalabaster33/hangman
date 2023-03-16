# Create a hangman game...
# Subjects: major cities, states in the world.... I will complete this list later, let me get some functionality noow

import csv
import random
import os
import time

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    greeting_msg = "\nGreetings traveler. Say your name and play\n"
    print(greeting_msg)
    player_name = input("\nEnter name: ")
    print(f"\n             Hello   {player_name}.")
    time.sleep(3)

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
#--------------------------------------------------------------------------------------------------#
        # pick categories to play and get back list of words
        cat_number = input("Enter a valid choice: ")
        if cat_number == "0":
            continue
        else:
            list_of_words, header = pick_category(cat_number, list_of_categories, csv_file)
            print(header)
#--------------------------------------------------------------------------------------------------#
        # pick a word from the list for player at random
        score = play_round(list_of_words, header)
        scoreboard = retrieve_scores()
        print(scoreboard)
        highscores = input_highscore(scoreboard, player_name, score)
        write_highscores(highscores)
        print(f"Your score was: {score}")

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
            time.sleep(3)
            continue
        if letter.isalpha() == False:
            print("Please enter an aplhabetical character")
            time.sleep(3)
            continue
        # check if letter is already used, i.e is it in the used_letters[]?
        if letter in used_letters:
            print(f"You have already used this letter: -- {letter.upper()} --")
            time.sleep(3)
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
            print(f"\n  Too bad. Try again or change a category")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            return highscore

    print("You guessed all the words from the category. Pick new.")
    time.sleep(3)
    return highscore


def retrieve_scores():
    scoreboard = []
    with open("score.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            score = row["score"]
            scoreboard.append({"name":name, "score":score})

    return scoreboard



def input_highscore(scoreboard, name, score):

    scoreboard.append({"name":name, "score":score})
    return scoreboard


def write_highscores(highscores):
    fieldnames = ["name", "score"]
    with open("score.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in highscores:
            writer.writerow(row)











if __name__ == "__main__":
    main()