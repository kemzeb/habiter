'''
'   math.py
'
'   Provides stat and other mathematical
'   functions for habiter to work with
'
'''

## NOTE: the math will need to be approved and documented, but for
# now squaring away implementations is priority

## ALSO NOTE: All the functions below are implementation details,
#  so as of right now there exists little to no type checking

import math
import sys


def neumaier_sum(summ, val):
    raise NotImplementedError


def avg_percent_delta(avg1:float, avg2:float, time=1):
    ''' Computes the average percent change
        for some function of time, expressed
        as a percentage (though it returns a
        float value)
        So,
            avg2 - avg1      1
            -----------  *  ---- * 100
                avg1        time

        represents the computation found below

        If it inputs a '-': represents % decrease
        If it inputs a '+': represents % increase
    Parameters
        avg1:   the old average
        avg2:   the new average
        time:   an int value for a function of
                time (by default is one for 'one
                day')
    '''
    try:
        return (((avg2 - avg1) / avg1) * (1 / time)) * 100
    except ZeroDivisionError:
        print("[Error: Division by zero.]")
        sys.exit(1)


def avg(summation, nTrials:int):
    try:
        return summation / nTrials
    except ZeroDivisionError:
        print("[Error: Division by zero.]")
        sys.exit(1)


# Unused function, needs to be tested
def running_avg(avg, newVal, nTrials):
    old_avg = avg * (nTrials-1)
    return old_avg + ( (newVal - old_avg) / nTrials )


def poisson_prob(lmda, x:int):
    ''' Computes the probability for a discrete random
        variable using the Poisson probability
    Parameters
        lmda:   the lambda parameter
        x:      a discete event that is observed (i.e. for occurrence(s))
    '''
    return (math.e) ** (-lmda) * ( (lmda**x) / math.factorial(x) )


if __name__ == "__main__":
    #print(avg(summation=5, nTrials=2))
    print(avg_percent_delta(4,8))
