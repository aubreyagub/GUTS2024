import numpy as np


def clamp(n, min=0, max=1):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


STINK_FACTOR_DISTRIBUTIONS = {
    # mean and std. dev
    "CS": (0.001, 0.0001),
    "History": (0.001, 0.0001)
}


def generate_stink_factor(course: str):
    stink_factor = np.random.normal(
        STINK_FACTOR_DISTRIBUTIONS[course][0], STINK_FACTOR_DISTRIBUTIONS[course][1])
    return clamp(stink_factor)


NATURAL_STINK_RATE_DISTRIBUTIONS = {
    # mean and std. dev
    "CS": (0.001, 0.0002),
    "History": (0.0003, 0.0001)
}


def generate_natural_stink_rate(course: str):
    natural_stink_rate = np.random.normal(
        NATURAL_STINK_RATE_DISTRIBUTIONS[course][0], NATURAL_STINK_RATE_DISTRIBUTIONS[course][1])
    return clamp(natural_stink_rate)


MAX_NATURAL_STINK_DISTRIBUTIONS = {
    # mean and std. dev
    "CS": (0.15, 0.05),
    "History": (0.05, 0.025)
}


def generate_max_natural_stink(course: str):
    max_natural_stink = np.random.normal(
        MAX_NATURAL_STINK_DISTRIBUTIONS[course][0], MAX_NATURAL_STINK_DISTRIBUTIONS[course][1])
    return clamp(max_natural_stink)


STINK_THRESHOLD_DISTRIBUTIONS = {
    # mean and std. dev
    "CS": (0.5, 0.2),
    "History": (0.3, 0.1)
}


def generate_stink_threshold(course: str):
    stink_threshold = np.random.normal(
        STINK_THRESHOLD_DISTRIBUTIONS[course][0], STINK_THRESHOLD_DISTRIBUTIONS[course][1])
    return clamp(stink_threshold)
