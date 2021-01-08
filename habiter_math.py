'''
'	habiter_math.py
'
'	Provides stat and other mathematical
'	functions for Habiter to work with
'
'''

# NOTE: that math will need to be approved and documented, but for
# now squaring away implementations is priority

# Needed math implementations
	# Possion Distro
	# Average Percentage Change

import math


def neumaier_sum(summ, val):
	raise NotImplementedError


def avg_delta_percent(avg1, avg2):
	raise NotImplementedError


def avg(summation, nTrials):
	return summation / nTrials


def running_avg(avg, newVal, nTrials):
	old_avg = avg * (nTrials-1)
	return old_avg + ( (newVal - old_avg) / nTrials )


def possion_prob(lmda, x):
	return (math.e) ** (-lmda) * ( (lmda**x) / math.factorial(x) )


if __name__ == "__main__":
	print( (1 - possion_prob(4, 0) - possion_prob(4, 1) ) * 100, "%" )
	print(running_avg(0, 4, 1))
