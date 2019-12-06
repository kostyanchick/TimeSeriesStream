import numpy as np


def gen_normal_dist_number(mu=0, sigma=1):
    idx = 0
    while True:
        number = round(np.random.normal(mu, sigma), 4)
        yield (idx, number)
        idx += 1
