from os import system
from random import randint

# function that runs say command and takes in a string
def say(something):
    system('espeak "%s"' % something)

# largest number possible
max_num = 10
first_line = "Guess a number between 1 and %d" % max_num

print first_line
say(first_line)

number = randint(1, max_num)
not_solved = True

# keep looping until we guess correctly
while not_solved:
    answer = input("? ")
    you_said = "You typed %d" % answer
    say(you_said)

    if answer > number:
        say("The number you guessed is too big, try again!")
    elif answer < number:
        say("The number you guessed is too small, try again!")
    else:
        say("You got the number!")
        not_solved = False




