import pandas as pd
import numpy as np

#lambda = \\
df = pd.read_csv("hello.txt", sep=" ", header=None)
#print(df[0][0])
sentence = df[0][0]



def check_parenthesis(sentence):
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')


def parse_expression(sentence, index=0):
    '''
    Recursive parser
    '''
    result = []
    current = ""

    while index < len(sentence):
        char = sentence[index]
        if char == '(':
            if current:
                result.append(current)
                current = ''
            nested, index = parse_expression(sentence, index + 1) #Recursive step
            result.append(nested)
        elif char == ')':
            if current:
                result.append(current)
            return result, index #stops sub operations
        else:
            current += char
        index += 1
    if current:
        result.append(current)
    return result, index

def chop(sentence):
    '''chops parentheses'''
    check_parenthesis(sentence)
    parsed, x = parse_expression(sentence)
    return parsed


print(chop(sentence))


def preprocess(sentence):
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


        
    