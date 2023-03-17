# HANGMAN Game

## Description

Hangman is a text-based game that challenges players to guess a word by suggesting letters within a certain number of guesses. This Python project was built as the final project for Harvard's CS50p - Introduction to programming with Python.

The goal of this project was to create a game that incorporates the skills and concepts learned throughout the course, including loops, functions, file input/output...

## How to play

1. Run the hangman.py file using Python 3 in the terminal.
2. Enter your name when prompted.
3. Choose your difficulty level.
4. Based on the difficulty selected, the game will choose .csv file with easy or hard words.
5. Select the category you want to play.
6. Once a category is selected, you will be given a word and 6 attempts to try and guess the word.
7. If you guess the word, 1 will be added to your score, if you don't guess the word, it is game over.

## Features

Randomly selected words from a list of over 100,000 words in easy.csv or hard.csv
Categories and words can be added dynamically by just updating the .csv files with a category and corresponding words.
User-friendly interface with clear instructions and error messages.
Score tracking to keep track of the user's wins and losses.
The game ends when the user has either won or lost.

## Requirements

Python 3.x

Modules used:

- csv
- random
- os
- time
- sys
- tty
- termios

## Installation
1. Clone the repository or download the ZIP file.
2. Extract the files to a directory of your choice.
3. Open a terminal in the directory containing the files.
4. Type python hangman.py and press enter.

## Contributions
This project was created as a final project for Harvard's CS50p course and is not currently accepting contributions. However, feel free to use the code for educational purposes or to suggest improvements.

## License
This project is under no licensing. Anyone can use the code as they like.