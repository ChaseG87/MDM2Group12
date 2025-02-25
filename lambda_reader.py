import pandas as pd
import numpy as np


'''
1. Parse sentence into chopped form
2. identify functions and expressions as classes
3. evaluate application of innermost objects on each other
4. evaluation alpha conversion, then beta then neu reduction (maybe)
5. repeat 3 and 4 till cannot be done anymore
functions and subfunctions that go from string to object and back?

[/x.xx, [/xy.yx]]
recursive function application??
'''
filename = 'hello.txt'

def pull_txt():
    df = pd.read_csv(filename, sep=" ", header=None)
    sentence = df[0][0] 
    return sentence


def check_parenthesis(sentence):
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')


def parse_expression(sentence, index=0):
    '''Recursive parser'''
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


#print(chop(sentence))

def find_replacement(input, body):
    options = 'abcdefghijklmnopqrstuvwxyz'
    for option in options:
        if option not in input and option not in body:
            return option


def alpha_reduction(input, body):
    '''Changes input into form that doesnt conflict with body.'''
    for char in input:
        if char in '/.()':
            continue
        else:
            if char in body:
                replacement = find_replacement(input, body)
                for _ in range(input.count(char)):
                    rep_idx = input.index(char)
                    input = input[:rep_idx] + replacement + input[rep_idx+1:]
    return input


def preprocess1(sentence):
    '''takes in a function and puts it in correct form eg. /x./y.xy -> /x.(/y.xy)'''
    for idx in range(len(sentence)):
        char = sentence[idx]
        if char == '.':
            if sentence[idx+1] == '/':
                paren_count = 0
                pos = idx+1
                while paren_count >= 0 and pos <= len(sentence)-1:
                    if sentence[pos] == '(':
                        paren_count += 1
                    if sentence[pos] == ')':
                        paren_count -= 1
                    pos += 1
                sentence = sentence[0:idx+1] + '(' + sentence[idx+1:pos] + ')' + sentence[pos:]
    return sentence


class Function:
    def __init__(self, string):
        period_idx = string.index('.')
        self.vars = string[1:period_idx]
        self.body = string[period_idx+1:]
        self.string = string

    def __call__(self):
        """
        Runs a Diagnostics - Useful for Displaying.
        """
        print("String", self.string)
        print("Body", self.body)
        print("Vars", self.vars, "\n")
        
    def printit(self):
        print(self.string)
    def beta_reduce(self, inputs):
        '''inputs is a list of each individual input'''
        var_list = [self.vars[i] for i in range(len(self.vars))]
        ins = ['(' + input.string + ')' if type(input) == Function else input for input in inputs]
        for idx in range(len(ins)):
            var = var_list[idx]
            innie = ins[idx]
            self.vars = self.vars[1:]
            innie = alpha_reduction(innie, self.body)
            for _ in range(self.body.count(var)):
                insert_idx = self.body.index(var)
                self.body = self.body[0:insert_idx] + innie + self.body[insert_idx+1:]
            

class Var:
    def __init__(self, name):
        self.name = name
        

def main():
    sentence = pull_txt()
    sentence = preprocess1(sentence)
    #chopped = chop(sentence)
    print(sentence)

        
sent1 = Function('/xy.xxyy')
sent2 = 'yy'
sent3 = Function('/bc.c')

sent1.beta_reduce([sent3])
sent1()

sent1.beta_reduce([sent2])
sent1()

print(preprocess1('/x./y.xxyy'))
main()



        
    
