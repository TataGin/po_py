"""Contains functions to control for user inputs."""

import pathlib as pl
import sys
import re


def yes_no(question):
    """Check if user gave a valid answer to a yes/no question.

    Positional argments:
    :question str
    """
    # Add '?' if not done by user
    question = question.strip()
    if not question.endswith('?'):
        question += '?'

    answer = input(question + " (y/n): ").lower().strip()
    print('')
    while not(answer == "y" or answer == "yes" or
              answer == "n" or answer == "no"):
        print("Input yes or no please! \n")

        answer = input(question + "(y/n):").lower().strip()

    if answer[0] == "y":
        return True
    else:
        return False


def custom_question(question, answers):
    """Check if user gave a valid answer to the question.

    Positional arguments:
    :question str
    :answers dict
    """
    # Add '?' if not done by user
    question = question.strip()
    if not question.endswith('?'):
        question += '?'

    valid_long_answers = list(map(lambda x: x.strip().lower(),
                                  list(answers.keys())))
    valid_short_answers = list(map(lambda x: x.strip().lower(),
                                   list(answers.values())))
    str_valid_answers = ', '.join(map(str, valid_long_answers))

    answer = input(question + ' (' + str_valid_answers + '): ').strip().lower()
    print('')

    while not (answer in list(map(str.lower,
                                  valid_long_answers+valid_short_answers))):
        print('Answer not valid. Valid answers: '+str_valid_answers+'\n')
        answer = input(question + ' (' + str_valid_answers +
                       '): ').strip().lower()

    return answer


def if_none(x, y):
    """If x is None, return y.

    Positional arguments:
    : x any
    : y any
    """
    if x:
        return x
    else:
        return y
