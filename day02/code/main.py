import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def from_letter(letter):
        if letter in ('A', 'X'):
            return Shape.ROCK

        elif letter in ('B', 'Y'):
            return Shape.PAPER

        elif letter in ('C', 'Z'):
            return Shape.SCISSORS

        else:
            return NotImplementedError


    @staticmethod
    def score_of(shape):
        return {
            Shape.ROCK: 1,
            Shape.PAPER: 2,
            Shape.SCISSORS: 3
        }[shape]


    @staticmethod
    def loses_against(shape):
        return {
            Shape.ROCK: Shape.PAPER,
            Shape.PAPER: Shape.SCISSORS,
            Shape.SCISSORS: Shape.ROCK
        }[shape]
    

    def wins_against(shape):
        return {
            Shape.ROCK: Shape.SCISSORS,
            Shape.PAPER: Shape.ROCK,
            Shape.SCISSORS: Shape.PAPER
        }[shape]


class Outcome():
    def __init__(self, left: Shape, right: Shape):
        self.left = left
        self.right = right
    
    def score(self):
        if Shape.wins_against(self.left) == self.right:
            return 0

        if Shape.loses_against(self.left) == self.right:
            return 6

        elif self.right == self.left:
            return 3


def part_one(inp):
    total_score = 0

    for play in inp.splitlines():
        left, right = (Shape.from_letter(x) for x in play.split(" "))
        
        total_score += Outcome(left, right).score()
        total_score += Shape.score_of(right)

    return total_score


def part_two(inp):
    total_score = 0

    for play in inp.splitlines():
        left, result = play.split(" ")
        left = Shape.from_letter(left)

        # Gotta lose
        if result == 'X': 
            right = Shape.wins_against(left)
        
        # Gotta tie
        elif result == 'Y': 
            right = left

        # Gotta win
        else: 
            right = Shape.loses_against(left)

        total_score += Outcome(left, right).score()
        total_score += Shape.score_of(right)

    return total_score