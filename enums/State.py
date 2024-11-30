from enum import Enum
class State(Enum):
    Susceptible = 0
    Exposed = 1
    Infected = 2
    Doubtful = 3
    Recovered = 4