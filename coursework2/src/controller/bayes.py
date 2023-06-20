from dataclasses import dataclass
import math
from operator import mul
from functools import reduce


@dataclass
class Square:
    book_probability: float
    ame: str = "Hello"




grid_size = 16
book_count = 4


def bayes_probability(
        prior: float, 
        specificity: float,
        sensitivity: float = 1 # Percept always occurs for positives
) -> float:
    marginalised = (
        sensitivity * prior
        + ((1 - specificity) * (1 - prior))
    )
    return sensitivity * prior / marginalised


def square_probability(other_squares: list[Square], prior: float = None) -> float:
    default_prob = book_count / grid_size
    prior = default_prob if prior is None else prior # Allows for prior=0

    # Specificity equates to the cominbed likelihood of all other
    # adjacent squares being safe, so that a negative result
    # would be given (ie. no percept). 
    specificity = reduce(mul, [(1 - sq.book_probability) for sq in other_squares])
    return bayes_probability(prior, specificity)


# for i in [1, 2, 3, 4]:
#     probs = square_probability(i)
#     print(f"{i} -> {probs}")



# print(f"Compounded: {square_probability(3, prior=0.6)}")



squares = [Square(_) for _ in range(3)]
# new = square_probability(squares, prior=0.001)
# print(f"Squares: {new}")



a = sorted(squares, key=lambda x: x.book_probability)
print(f"a: {a}")