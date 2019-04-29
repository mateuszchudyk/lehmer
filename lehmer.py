#!/usr/bin/env python

"""Implementation of Lehmer Code.

Permutation - an array of integers. For the given interval, the array has to contains all numbers
for the interval and each of the number has to appear only once.

GitHub: https://github.com/mateuszchudyk/lehmer
"""

__author__ = "Mateusz Chudyk"
__license__ = "MIT"

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

@static_var("lut", [1])
def factorial(n):
    while n >= len(factorial.lut):
        factorial.lut.append(factorial.lut[-1] * len(factorial.lut))
    return factorial.lut[n]

def encode(permutation):
    """Return Lehmer Code of the given permutation.
    """
    def permutation_is_valid(permutation):
        if not permutation:
            return False

        minimum = min(permutation)
        maximum = max(permutation)

        used = [0] * (maximum - minimum + 1)
        for i in permutation:
            used[i - minimum] += 1

        if min(used) == 1 and max(used) == 1:
            return True
        else:
            return False

    def count_lesser(i, permutation):
        return sum(it < permutation[i] for it in permutation[i + 1:])
    
    def parial_result(i, permutation):
        return count_lesser(i, permutation) * factorial(len(permutation) - 1 - i)

    if not permutation_is_valid(permutation):
        return False
    
    return sum(parial_result(i, permutation) for i in range(0, len(permutation)))

def decode(length, lehmer):
    """Return permutation for the given Lehmer Code and permutation length. Result permutation contains
    number from 0 to length-1.
    """
    result = [(lehmer % factorial(length - i)) // factorial(length - 1 - i) for i in range(length)]
    used = [False] * length
    for i in range(length):
        counter = 0
        for j in range(length):
            if not used[j]:
                counter += 1
            if counter == result[i] + 1:
                result[i] = j
                used[j] = True
                break
    return result

def test():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    
    assert encode([]) == 0
    assert encode([0]) == 0
    assert encode([0, 1]) == 0
    assert encode([1, 0]) == 1
    assert encode([0, 1, 2, 3]) == 0
    assert encode([3, 1, 0, 2]) == 20
    assert encode([3, 2, 1, 0]) == 23

    assert decode(1, 0) == [0]
    assert decode(2, 1) == [1, 0]
    assert decode(3, 5) == [2, 1, 0]
    assert decode(4, 0) == [0, 1, 2, 3]
    assert decode(4, 20) == [3, 1, 0, 2]
    assert decode(4, 23) == [3, 2, 1, 0]
    assert decode(5, 119) == [4, 3, 2, 1, 0]
    assert decode(6, 719) == [5, 4, 3, 2, 1, 0]
    assert decode(7, 5039) == [6, 5, 4, 3, 2, 1, 0]
    assert decode(8, 40319) == [7, 6, 5, 4, 3, 2, 1, 0]
    assert decode(9, 362879) == [8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert decode(10, 3628799) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert decode(11, 39916799) == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert decode(12, 479001599) == [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

if __name__ == "__main__":
    test()
