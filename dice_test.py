import numpy as np
from matplotlib import pyplot as plt
import pytest

from dice import Die

def test_dice()->None:
    d6=Die(6)
    results=[]
    rolls=1000000
    for _n in range(rolls):
        results.append(d6.roll())
    results_unique=sorted(list(set(results)))
    assert results_unique == [1,2,3,4,5,6]
    counts=[]
    for number in range(1,7):
        counts.append(results.count(number))
    assert np.all(np.abs(np.array(counts)/rolls-1./6) < 1e-3)
