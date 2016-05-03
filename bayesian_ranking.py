'''
    Implements two approaches to compute bayesian score

    1. computes the lower bound of a credible interval of a normal
    https://docs.google.com/document/d/1eR2VGxGKEId2A0l2p6GBJujgnpelLm3Cf-fCpvwBNIo/edit

    2. computes the bayesian weighted average for items with mimimum number of
    votes
    https://docs.google.com/document/d/16lfMQFwggaf9jYf9YIP3cbfrW_PFNE1_Ay86A8H4STA/edit
'''
from __future__ import division
import math
import pandas

K = 5
sk = [1,2,3,4,5]
z = 1.65

def lower_bound_normal_credible_interval(nk):

    N = sum(nk)
    terma = 0
    termb = 0
    wavg = 0

    for k in range(K):
        avg = (nk[k]+1)/(N+K)
        terma = terma + sk[k]*avg
        wavg = wavg + sk[k]**2*avg

    termb = math.sqrt((wavg-terma**2)/(N+K+1))
    return terma - z*termb


def read_idea_ratings_data(file):
    data = pandas.read_csv(file, header=None)
    return data.values.tolist()


totalratings = 0
totalstars = 0
for a in read_idea_ratings_data("idea_ratings.csv"):
    totalratings = totalratings + sum(a)
    for k in range(K):
        totalstars = totalstars + sk[k]*a[k]
C = totalstars/totalratings

def bayesian_weighted_average(nk):
    '''
        S = N*R + m*C / N+m
        N = number of ratings of an idea
        R = average ratings on an idea
        C = average ratings on all ideas
    '''
    m = 10
    N = sum(nk)
    R = 0
    for k in range(K):
        R = R + sk[k]*nk[k]
    R = R/N
    return (N*R + m*C)/(N+m)

def print_separate_lines(alist):
    for a in alist:
        print a
    print "\n"

scores = map(
    lower_bound_normal_credible_interval,
    read_idea_ratings_data("sample.csv")
    )
print_separate_lines(scores)

wavgs = map(
    bayesian_weighted_average,
    read_idea_ratings_data("sample.csv")
    )
print_separate_lines(wavgs)
