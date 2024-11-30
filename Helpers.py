import math
import random


def bernoulli_rvs(p):
    # Return a sample from a Bernoulli-distributed random source
    # We convert from a Uniform(0, 1)
    r = random.random()
    if r >= p:
        return 1
    return 0


def poisson_rvs(mu):
    p0 = math.exp(-mu)
    F = p0
    i = 0
    sample = random.random()
    while sample >= F:
        i += 1
        F += p0 * (mu ** i) / math.factorial(i)
    return i