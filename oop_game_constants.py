from dataclasses import dataclass

BASE_HP = 100
INITIAL_MONEY = 1_000


@dataclass
class Stars:
    REGULAR_CITIZEN = 1
    WANTED_LOW = 2
    WANTED_HARD = 3
