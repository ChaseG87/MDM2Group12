import pandas as pd

'''
Object based lambda calculus evaluator that can evaluate normal form
or inner application first depending on sorting method in lambda simplify.
'''

## Sets the default filename for the input
filename = 'hello.txt'


class Function:
    def __init__(self, lst):
        """Seperates the parts of the equation """
         ## Gets the index of the .
        period_idx = lst.index('.')

        ## Uses the index of the . to seperate the remaining sections.
        self.vars = lst[1:period_idx]
        self.body = lst[period_idx+1:]
        self.lst = lst

        def __call__(self):
        """ Runs a Diagnostics - Useful for Displaying. """

        print("\n\n","String:", self.lst)
        print("Body:", self.body)
        print("Vars:", self.vars, "\n\n")
        
    def update(self):
        """ Regularly updates the list with the vars and body to make sure they are consistent. """
        
        if len(self.vars) > 0:
            self.lst = ['/'] + self.vars + ['.'] + self.body
        else:
            self.lst = self.body



    def beta_reduce(self, inputs):
        '''
        Beta reduces the function to create a simpler module. Necessary for the inputs.
        
        Input Parameters:
        inputs - List of inputs to beta reduce by. Note that A.beta_reduce(B) means #######################
        '''


        def alpha_reduction(input, vars):
           '''
            Changes input into form that doesnt conflict with body. Necessary for beta reduction.

            Input Parameters:
            input - The input sentence being searched for substitution.
            vars - The variables already present in the sentence. 

            Output:
            input - The alpha substituted sentence.
            '''


            def find_replacement(input, vars):
                """Finds a replacement variable. Used for alpha reduction."""
                options = 'abcdefghijklmnopqrstuvwxyz'
                for option in options:
                    if option not in input and option not in vars:
                        return option
                    
            ## Searches through all characters in input and locates non-special characters
            for char in input:
                if char in ['/', '.', '(', ')']:
                    continue

                ## If the character is in variables, find a replacement.
                elif char in vars:
                    replacement = find_replacement(input, vars)

                    # Updates variable with replacement for each instance
                    for _ in range(input.count(char)):
                        rep_idx = input.index(char)
                        input = input[:rep_idx] + [replacement] + input[rep_idx+1:] 
                        
            return input
            
         ## Creates a seperate variable for the variable list, locates the inside and flattens the body. (RHS of . in lambda expression)
        var_list = self.vars
        ins = [function_flattener(input) for input in inputs]
        self.body = function_flattener(self.body)

        ## Iterates through the variables and flattened indexes and alpha reduces them.
        for idx in range(min(len(var_list), len(ins))):
            var = var_list[idx]
            innie = ins[idx]
            self.vars = self.vars[1:]
            innie = alpha_reduction(innie, var_list)

        ## Substitutes the inside of the equations back into the bodies ##############################
            for _ in range(self.body.count(var)):
                insert_idx = self.body.index(var)
                self.body = self.body[0:insert_idx] + innie + self.body[insert_idx+1:]

        ## Updates the self.lst
        self.update()

def pull_txt():
    ''' Pulls text from predetermined file '''
    df = pd.read_csv(filename, sep=" ", header=None)
    sentence = df[0][0] 
    return sentence


def check_parenthesis(sentence):
    ''' Checks if parenthetic grammar is correct '''
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')
    

def string_to_list(string):
    ''' Turns a string lambda expression to a list '''
    result = [i for i in string]
    return result


def list_to_string(lst):
    ''' Turns list lambda expression to a string '''
    string = ''
    for i in lst:
            string += str(i)
    return string


def function_reduce(lst):
    ''' 
    Turns innermost function into Function class then nests all to functional form

    Input parameters:
    lst - The input function to analyse.

    Output:
    lst (for arguments without /) - The original list, unchanged
    updated (for arguments with /) - The innermost function within the original list.
    '''

    ## Collects the index of the lambdas.
    lambda_idx = [i for i in range(len(lst)) if lst[i] == '/']

    ## While there are more than one lambda left in the expression
    while lst.count('/'):
        ## Isolates the first lambda
        lamb = lambda_idx[0]
        lambda_idx.pop(0)

        ## Sets default values, with parenthesis count = 0
        paren_count = 0
        idx = lamb+1
        no_inner = True

        ## Parenthesis depth calculation.
        ## Detects the balance of ( to ), and inners using /. If more ) than (, it breaks the loop.
        while paren_count >= 0 and idx < len(lst):
            if lst[idx] == '/':
                no_inner = False
            if lst[idx] == ')':
                paren_count -= 1
            if lst[idx] == '(':
                paren_count += 1
            idx += 1

        ## Creates a new list and reduces it. Only if count of "(" < count of ")"
        if no_inner and paren_count < 0:
            new_list = lst[0:lamb] + [Function(lst[lamb:idx-1])] + lst[idx-1:]
            updated = function_reduce(new_list)
            return updated

       ## Creates a new list and reduces it. Only if count of "(" >= count of ")"
        elif no_inner and paren_count >= 0:
            new_list = lst[0:lamb] + [Function(lst[lamb:idx])] + lst[idx:]
            updated = function_reduce(new_list)
            return updated
            
    return lst


def single_chop(lst):
    '''
    Performs a single chop of parentheses with a list input using a stack.

    Input Parameters:
    lst - The list input being analysed.

    Output:
    stack - The chopped stack.
    '''

    ## Inputs the current stack and sets a default value for depth
    stack = []
    current = []
    depth = 0

    ## Creates the depth for the various list.
    ## Iterates through each item in the list; if it reaches a '(' then depth increases by 1.
    for i in lst:
        if i == '(':
            depth += 1

            ## Appends to current if it has a bracket depth of only 1
            if depth == 1:
                current = []
                current.append(i)
            else:
                current.append(i)

        ## Reduces depth by 1 if encounters ')'.
        elif i == ')':
            depth -= 1

            ## Appends to current if it has a bracket depth of 0.
            if depth == 0:
                current.append(i)
                stack.append(current)
            else:
                current.append(i)

        ## Appends i to a list if its a character thats not a bracket; stack if depth = 0, current if depth is not 0.        
        else:
            if depth == 0:
                stack.append(i)
            else:
                current.append(i)
    return stack

#####################################################COMPLETE THIS
def remove_double_parenthesis(lst):
    '''
    Removes double parentheses in a lambda calculus expression given a list form.
    
    Input Parameters:
    lst - The list of characters in the lambda calculus expression ##############################
    '''
    
    ## Setting default values for the depth and index
    depth = 0
    idx = 0
    active_search, search_depth = False, depth
    while idx < len(lst):

        # Stops search if outside of scope
        if depth == 0: 
            active_search = False
            
        if lst[idx] == '(':
            depth += 1

            #Turns on search for same depth double parentheses
            if lst[idx-1] == '(':
                active_search, search_depth = True, depth
                start_idx = idx-1

        ## Removes double parenthesis if detects an increase in the depth by 2 (double brackets), performs the function recursively
        if lst[idx] == ')':
            depth -= 1
            
            if lst[idx-1] == ')' and active_search and search_depth == depth + 2:
                lst = lst[0:start_idx] + lst[start_idx+1:idx] + lst[idx+1:]
                return remove_double_parenthesis(lst)
        idx += 1

    ## Returns the reduced outcome
    return lst


def function_flattener(lst):
    '''Recursive flattener of lists and function objects'''
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


def lambda_simplify(lst, body=False):  
    lst = preprocess_church(lst)
    chopped = single_chop(lst) #breaks into largest reducible functions
    chopped = [function_reduce(j) if isinstance(j, list) else j for j in chopped]
    for i in range(len(chopped)): #does all possible beta reduction operations
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
        #takes away outermost parentheses if redundant
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

    
def find_next_action(lst, step):
    '''
    Takes an input of a lambda calculus sentence in list mode, finds all options for the next reduction,
    then picks 
    '''
    lst = preprocess_church(lst) #normaizes form of lambda expressions
    options = []
    lambda_idx = [i for i in range(len(lst)) if lst[i] == '/']
    if not lambda_idx:
        return lst
    if (lambda_idx[0] == 0 or lambda_idx[0] == 1) and lst != lambda_simplify(lst):
        options.append([lambda_simplify(lst), depth_test(lst, lambda_idx[0]), lambda_idx[0]])
    for lamb in lambda_idx: #goes through lambdas and checks if beta reduction is possible then adds that possibility
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
    if options and step%100 > 2: #sorts possibilites bredth first
        options_sorted = sorted(options, key=lambda x:  x[1] -x[2]*0.001)
        return options_sorted[-1][0]
    elif options and step%100 <= 2: #sort possible updates  depth first
        options_sorted = sorted(options, key=lambda x: -x[1])
        return options_sorted[-1][0]
    else:
        return remove_double_parenthesis(lst)


def full_lambda_evaluator(string, give_steps=False):
    '''
    Inputs a string of lambda calculus with '/' as lambda.
    Returns a string reduced but equivalent to the input.
    '''
    n = 1
    loop_checker = [[]] # keeps track of updates to look for repetitions
    current = string_to_list(string)
    if give_steps: 
        print('Initial:', string) # print initial value if in give_steps mode
    new = find_next_action(current, step=n)
    loop_checker.append(new)
    if give_steps:
        print('Step 1:', list_to_string(new)) # gives each step of the evaluator if in give_steps mode
    n = 2
    while current != new: # while loop makes sure there are no more next steps from 'find_next_action'
        current = new
        new = find_next_action(current, step=n)
        loop_checker.append(new)
        if loop_checker[-1] == loop_checker[-3]: # checks if function will 1st form loop
            print('Sentence loops!')
            if give_steps:
                print('Reduced Form:', list_to_string(loop_checker[-1]))
            return list_to_string(loop_checker[-1])
        if give_steps:
            print(f'Step {n}:', list_to_string(new))
        n += 1
        if n >= 1000: # stops process after 1000 steps to stop 'sneaky' loops
            print('Max recursion depth reached')
            break
    if give_steps: # returns final result if in give_steps mode
                print('Reduced Form:', list_to_string(remove_double_parenthesis(current)))
    return list_to_string(remove_double_parenthesis(current))


def main():
    '''
    Runs the main process of lambda_reader2.py. Evaluates text in hello.txt
    using full_lambda_evaluator in give_steps mode.
    '''
    text = pull_txt()
    return full_lambda_evaluator(text, give_steps=True)
    


if __name__ == "__main__":
    main() 


def fileread(input, filename = 'definitions.csv', display = False):
    df = pd.read_csv(filename, header = None, names = ['Symbol', 'Expression'])

    if display:
        print(symbol)
    

    symbol = df['Symbol']
    expression = df['Expression']

    while True:
        present = False
        for character in input:
            for idx, val in enumerate(symbol):
                if val == character:
                    input = input.replace(character, "("+str(expression[idx])+")")
                    present = True

            if display:
                print("Character:",character)
                print("Input:",input)
                print("Present:", present)

        if present == False:
            return input


def compare_two_cases(sentence1, sentence2, display = False):
    sentence1 = full_lambda_evaluator(fileread(sentence1))
    sentence2 = full_lambda_evaluator(fileread(sentence2))

    print("Sentence1:", sentence1)
    print("Sentence2:", sentence2)
    for idx, char in enumerate(sentence1):

        if sentence2[idx] == char:
            continue
        else:
            sentence2 = sentence2.replace(sentence2[idx], char)

            if display:
                print("Char", char)

    if sentence1 == sentence2:
        return True
    
    else:
        return False
        

def test_case(filename = 'TestCases.csv', display = False, specific_case = None):
    df = pd.read_csv(filename, header = None, names = ['Question', 'Answer'])
    print(df)
    question = df['Question']
    answer = df['Answer']

    if display:
        print("Question:", question)
        print("Answer:", answer)
    
    if specific_case == None:
        for idx, val in enumerate(question):
            test = compare_two_cases(val, answer[idx])
            
            if test:
                print("Test " + str(idx) + ":", "SUCCESS")

            else:
                print("Test " + str(idx) + ":", "FAIL")

    else:
        test = compare_two_cases(question[specific_case], answer[specific_case])                  
        if test:
            print("Test " + str(specific_case) + ":", "SUCCESS")

        else:
            print("Test " + str(specific_case) + ":", "FAIL")

def replace_with_shorthand(input, filename = 'Definitions.csv'):
    df = pd.read_csv(filename, header = None, names = ['Symbol', 'Expression'])  
    expression = df['Expression']

    while True:
        prior_version = input
        temporary_version = input

        for idx, char in enumerate(temporary_version):
            if char == "(":
                left_bracket_index = idx
                print("Left Bracket Index:", left_bracket_index)

        for idx, char in enumerate(reversed(temporary_version)):
            if char == ")":
                right_bracket_index = idx
                print("Right Bracket Index:", right_bracket_index)
        
        try:
            temporary_version = temporary_version[:left_bracket_index] + temporary_version[(left_bracket_index + 1):right_bracket_index] + temporary_version[(right_bracket_index + 1):]
            selected_area = input[(left_bracket_index + 1) : right_bracket_index]

        except UnboundLocalError:
            selected_area = input

        for val in expression:
            if compare_two_cases(selected_area, val) == True:
                input = input.replace(selected_area, val)

        later_version = input

        if prior_version == later_version:
            return input


########################################################


# string_to_evaluate = fileread('/x.xFT')
# print(string_to_evaluate)
# print(type(string_to_evaluate))
# full_lambda_evaluator(string_to_evaluate, give_steps = True)

# test_case()
# test_case(specific_case = 13)

