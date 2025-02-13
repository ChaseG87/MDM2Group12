import pandas as pd
import numpy as np

#lambda = \\
df = pd.read_csv("hello.txt", sep=" ", header=None)
#print(df[0][0])
sentence = df[0][0]



def check_parenthesis(sentence):
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')


def paren_index(sentence):
    master = []
    opens = []
    closeds = []
    for i in range(len(sentence)):
        char = sentence[i]
        if char == '(':
            master.append(i)
            opens.append(i)
        if char == ')':
            master.append(i)
            closeds.append(i)
    return master, opens, closeds


def depth_calc(master, opens, closeds):
    depths = [0]
    for idx in master:
        if idx in opens:
            depth +=1
        if idx in closeds:
            depth -= 1
        depths.append(depth)
    return depths


def chop(sentence):
    check_parenthesis(sentence)
    master, opens, closeds = paren_index(sentence)
    chopped = []
    chopped.append([sentence[0:master[0]]])
    for i in range(len(master)-1):
        chopped.append([sentence[master[i]+1:master[i+1]]])
    chopped.append([sentence[master[-1]+1:]])
    chopped = [i for i in chopped if i != ['']]
    depth_list = depth_calc(master, opens, closeds)
    return chopped

#want [['/x.x'], ['/x.xy'], [['/xy.xx', 'x.x']]]
print(chop(sentence))
       

def preprocess(sentence):
    for i in range(len(sentence)):
        char = sentence[i]
        if char == '/' or char == 'λ':
            if sentence[i+2] != '.':
                pass


class Function:
    def __init__(self, string):
        period_idx = string.index('.')
        self.vars = string[1:period_idx]
        self.body = string[period_idx+1:]
        self.string = string
    def printit(self):
        print(self.string)
    def beta_reduce(self, *inputs):
        var_list = [self.vars[i] for i in range(len(self.vars))]
        ins = [input[i].string() if input[i].type() == Function else input[i] for i in inputs]


        
    