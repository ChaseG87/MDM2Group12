import pandas as pd

'''
Object based lambda calculus evaluator that can evaluate normal form
or inner application first depending on sorting method in lambda simplify.
'''

filename = 'hello.txt'


class Function:
    def __init__(self, lst):
        period_idx = lst.index('.')
        self.vars = lst[1:period_idx]
        self.body = lst[period_idx+1:]
        self.lst = lst

    def update(self):
        if len(self.vars) > 0:
            self.lst = ['/'] + self.vars + ['.'] + self.body
        else:
            self.lst = self.body



    def beta_reduce(self, inputs):
        '''inputs is a list of each individual input'''


        def alpha_reduction(input, vars):
            '''Changes input into form that doesnt conflict with body.'''


            def find_replacement(input, vars):
                options = 'abcdefghijklmnopqrstuvwxyz'
                for option in options:
                    if option not in input and option not in vars:
                        return option
                    

            for char in input:
                if char in ['/', '.', '(', ')']:
                    continue
                elif char in vars:
                    replacement = find_replacement(input, vars)
                    for _ in range(input.count(char)):
                        rep_idx = input.index(char)
                        input = input[:rep_idx] + [replacement] + input[rep_idx+1:]
            return input
            

        var_list = self.vars
        ins = [function_flattener(input) for input in inputs]
        self.body = function_flattener(self.body)
        for idx in range(min(len(var_list), len(ins))):
            var = var_list[idx]
            innie = ins[idx]
            self.vars = self.vars[1:]
            innie = alpha_reduction(innie, var_list)

            for _ in range(self.body.count(var)):
                insert_idx = self.body.index(var)
                self.body = self.body[0:insert_idx] + innie + self.body[insert_idx+1:]

        self.update()

def pull_txt():
    df = pd.read_csv(filename, sep=" ", header=None)
    sentence = df[0][0] 
    return sentence


def check_parenthesis(sentence):
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')
    

def string_to_list(string):
    result = [i for i in string]
    return result


def list_to_string(lst):
    string = ''
    for i in lst:
            string += str(i)
    return string


def function_reduce(lst):
    '''turns innermost function into Function class then nests all to functional form'''
    lambda_idx = [i for i in range(len(lst)) if lst[i] == '/']
    while lst.count('/'):
        lamb = lambda_idx[0]
        lambda_idx.pop(0)
        paren_count = 0
        idx = lamb+1
        no_inner = True
        while paren_count >= 0 and idx < len(lst):
            if lst[idx] == '/':
                no_inner = False
            if lst[idx] == ')':
                paren_count -= 1
            if lst[idx] == '(':
                paren_count += 1
            idx += 1
        if no_inner and paren_count < 0:
            new_list = lst[0:lamb] + [Function(lst[lamb:idx-1])] + lst[idx-1:]
            updated = function_reduce(new_list)
            return updated
        elif no_inner and paren_count >= 0:
            new_list = lst[0:lamb] + [Function(lst[lamb:idx])] + lst[idx:]
            updated = function_reduce(new_list)
            return updated
    return lst


def single_chop(lst):
    '''single chop of parentheses'''
    stack = []
    current = []
    depth = 0
    for i in lst:
        if i == '(':
            depth += 1
            if depth == 1:
                current = []
                current.append(i)
            else:
                current.append(i)
        elif i == ')':
            depth -= 1
            if depth == 0:
                current.append(i)
                stack.append(current)
            else:
                current.append(i)
        else:
            if depth == 0:
                stack.append(i)
            else:
                current.append(i)
    return stack


def remove_double_parenthesis(lst):
    depth = 0
    idx = 0
    active_search, search_depth = False, depth
    while idx < len(lst):
        if depth == 0:
            active_search = False
        if lst[idx] == '(':
            depth += 1
            if lst[idx-1] == '(':
                active_search, search_depth = True, depth
                start_idx = idx-1
        if lst[idx] == ')':
            depth -= 1
            if lst[idx-1] == ')' and active_search and search_depth == depth + 2:
                lst = lst[0:start_idx] + lst[start_idx+1:idx] + lst[idx+1:]
                return remove_double_parenthesis(lst)
        idx += 1
    return lst


def function_flattener(lst):
    master = []
    for l in lst:
        if isinstance(l, Function):
            master.extend(function_flattener(l.lst))
        elif isinstance(l, str):
            master.append(l)
        elif isinstance(l, list):
            master.extend(function_flattener(l))
    return master


def preprocess_church(sentence):
    ''' Takes in a function and puts it in correct form eg. /x./y.xy -> /x.(/y.xy) '''
    for idx in range(len(sentence)):
        char = sentence[idx]
        if char == '.':
            try:
                if sentence[idx+1] == '/':
                    paren_count = 0
                    pos = idx+1
                    while paren_count >= 0 and pos <= len(sentence)-1:
                        if sentence[pos] == '(':
                            paren_count += 1
                        if sentence[pos] == ')':
                            paren_count -= 1
                        pos += 1
                    sentence = sentence[0:idx+1] + ['('] + sentence[idx+1:pos] + [')'] + sentence[pos:]
            except:
                continue
    return sentence


def lambda_simplify(lst, nested=False, body=False):  
    lst = preprocess_church(lst)
    chopped = single_chop(lst)
    chopped = [function_reduce(j) if isinstance(j, list) else j for j in chopped]
    for i in range(len(chopped)):
        if i+1 < len(chopped):
            if isinstance(chopped[i][0], Function):
                if len(chopped[i][0].vars) and len(chopped) > i+1:
                    chopped[i][0].beta_reduce([chopped[i+1]])
                    chopped.pop(i+1)
                    break
            if len(chopped[i]) > 1:
                if isinstance(chopped[i][1], Function):
                    if len(chopped[i][1].vars) and len(chopped) > i+1:
                        chopped[i][1].beta_reduce([chopped[i+1]])
                        chopped.pop(i+1)
                        break
    lst = function_flattener(chopped)
    if len(chopped) == 1 and chopped[0][0] == '(' and chopped[0][-1] == ')' and not body:
        lst = lst[1:-1]
    return lst


def depth_test(lst, lamb):
    '''returns parenthetic depth of a given lambda index.'''
    idx = 0
    paren_depth = 0
    while idx != lamb:
        if lst[idx] == '(':
            paren_depth += 1
        if lst[idx] == ')':
            paren_depth -= 1
        idx += 1
    return paren_depth


def find_next_action(lst):
    lst = preprocess_church(lst)
    options = []
    lambda_idx = [i for i in range(len(lst)) if lst[i] == '/']
    if not lambda_idx:
        return lst
    if (lambda_idx[0] == 0 or lambda_idx[0] == 1) and lst != lambda_simplify(lst):
        options.append([lambda_simplify(lst), depth_test(lst, lambda_idx[0]), lambda_idx[0]])
    for lamb in lambda_idx:
        sidx = lamb+1
        paren_count = 0
        while sidx <= len(lst):
            if paren_count < -1:
                if lst[lamb-1:sidx-1] != lambda_simplify(lst[lamb-1:sidx-1], body=True):
                    options.append([lst[0:lamb-1] + lambda_simplify(lst[lamb-1:sidx-1], body=True) + lst[sidx-1:], depth_test(lst, lamb), lamb])
                    break
                else:
                    break
            try:
                if lst[sidx] =='(':
                    paren_count += 1
                if lst[sidx] == ')':
                    paren_count -= 1
            except:
                break
            sidx += 1
    if options:
        options_sorted = sorted(options, key=lambda x: - x[1] - x[2]*0.001)
        return options_sorted[-1][0]
    else:
        return remove_double_parenthesis(lst)


def full_lambda_evaluator(string, give_steps=False):
    loop_checker = [[]]
    current = string_to_list(string)
    if give_steps:
        print('Initial:', string)
    new = find_next_action(current)
    loop_checker.append(new)
    if give_steps:
        print('Step 1:', list_to_string(new))
    n = 2
    while current != new:
        current = new
        new = find_next_action(current)
        loop_checker.append(new)
        if loop_checker[-1] == loop_checker[-3]:
            print('Sentence loops!')
            if give_steps:
                print('Reduced Form:', list_to_string(loop_checker[-1]))
            return list_to_string(loop_checker[-1])
        if give_steps:
            print(f'Step {n}:', list_to_string(new))
        n += 1
        if n >= 100:
            print('Max recursion depth reached')
            break
    if give_steps:
                print('Reduced Form:', list_to_string(remove_double_parenthesis(current)))
    return list_to_string(remove_double_parenthesis(current))


def main():
    text = pull_txt()
    return full_lambda_evaluator(text, give_steps=True)
    


if __name__ == "__main__":
    main() 

########################################################

#(/nfx.f(nfx))(/fx.x)
#(/mnfx.m(mf(nfx)))(/fx.f(f(fx)))(/fx.f(f(f(fx))))

#full_lambda_evaluator('(/xy.xx)(/z.z)a', give_steps=True)



