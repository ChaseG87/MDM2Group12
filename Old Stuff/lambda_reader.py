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
filename = 'input.txt'


def pull_txt():
    '''
    Reads the text file and returns a list which has the contents of one line as an entry.
    '''
    line_list = []

    file = open(filename, "r")
    for line in file:
        line_list.append(line.strip())
    return line_list


def check_parenthesis(sentence):
    """ Checks the parentheses in a sentance to make sure that the amount of ( and ) are equal. """
    if sentence.count('(') != sentence.count(')'):
        raise ValueError('The sentence has incorrect parenthetic grammar.')


def parse_expression(sentence, index=0):
    '''
    Parses expressions recursively by --------- 
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
    ''' Chops sentance by passing parse_expression() '''
    check_parenthesis(sentence)
    parsed, x = parse_expression(sentence)
    return parsed

#print(chop(sentence))

def find_replacement(input, body):
    '''
    Used in alpha conversion.
    Finds a substitute variable for a sentance in the case that one is occupied.
    '''
    options = 'abcdefghijklmnopqrstuvwxyz'
    for option in options:
        if option not in input and option not in body:
            return option


def alpha_reduction(input, body):
    ''' Changes input into form that doesnt conflict with body. '''
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
    ''' Takes in a function and puts it in correct form eg. /x./y.xy -> /x.(/y.xy) '''
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
        self.alpha_input = None

    def __call__(self):
        """ Runs a Diagnostics - Useful for Displaying. """
        print("\n\n","String:", self.string)
        print("Body:", self.body)
        print("Alpha Input:", self.alpha_input)
        print("Vars:", self.vars, "\n\n")
        
    def beta_reduce(self, inputs):
        '''
        Beta reduces the display using inputs.
        Uses notation (class)(inputs).
        '''
        var_list = [self.vars[i] for i in range(len(self.vars))]
        ins = ['(' + input.string + ')' if type(input) == Function else input for input in inputs]
        for idx in range(len(ins)):
            var = var_list[idx]
            innie = ins[idx]
            self.vars = self.vars[1:]
            innie = alpha_reduction(innie, self.body)
            self.alpha_input = innie
            for _ in range(self.body.count(var)):
                insert_idx = self.body.index(var)
                self.body = self.body[0:insert_idx] + innie + self.body[insert_idx+1:]
                

def read_multiple_functions(first_index = 0, second_index = 1, data = pull_txt(), reduce = False, display = False):
    '''
    Checks multiple lines of the file and then reduces them.
    Arguments:
    reduce - Can choose to reduce the function if true - first reduces second.
    display - can display the diagnostics for the first variable if on.
    '''
    
    ## Creates a list for functions to be read from the file
    list_of_functions = []

    ## Reads from the file and ensures that only things that have lambda in them become functions.
    ## NEED TO DEAL WITH yy(/x.xy) as an input - this would break the code.
    for value in data:
        if '/' in value:
            list_of_functions.append(Function(value))
        else:
            list_of_functions.append(value)

    ## Gets the first and second value - ONLY works for 2 values on each other, but would recommend using recursion for more complicated algorithms.
    first = list_of_functions[first_index]

    if second_index != None:
        second = list_of_functions[second_index]
    
        ## Checks whether it is a function
        if reduce:
            if not(isinstance(first, str)) == True:
                first.beta_reduce([second])
    
        if display:
            ## Runs Diagnostics on First 
            first()
            
    return first


def two_function_test(function1, function2):
    '''
    Compares whether two functions are the same.
    Works for both functions and arguments.
    '''
    
    f1_is_function = (not(isinstance(function1, str)) == True)
    f2_is_function = (not(isinstance(function2, str)) == True)

    if f1_is_function and f2_is_function:
        if function1.vars == function2.vars:
            if function1.body == function2.body:
                return True
        else:
            return False
    
    elif f1_is_function and not(f2_is_function):
        if function1.body == function2:
            return True
        else:
            return False
    
    elif not(f1_is_function) and f2_is_function:
        if function1 == function2.body:
            return True
        else:
            return False

    else:
        if function1 == function2:
            return True
        else:
            return False 


def test_cases(no_of_cases, display = True):
    '''
    Applys the test cases and prints out whether it is successful.
    No_of_cases = No of cases to be applyed starting at the first.
    display (optional) - chooses whether to display the outcomes of the tests. Default = True.
    '''
    
    if display:
        print("\n" + "TEST CASES")
        print("----------")
    
    for i in range(no_of_cases):
        test1 = read_multiple_functions(first_index = (3*i) + 0, second_index = (3*i) + 1, reduce = True, display = False)
        test2 = read_multiple_functions(first_index = (3*i) + 2, second_index = None, reduce = False, display = False)
        if two_function_test(test1, test2):
            print("Test", str(i+1)+":", "TEST SUCCESSFUL")
        else:
            print("Test", str(i+1)+":", "TEST FAILURE")


def main():
    '''
    Main function.
    Takes a sentence, preprocesses it and turns it into a list, where the lists represent brackets.
    '''
    sentence = pull_txt()
    sentence = preprocess1(sentence)
    #chopped = chop(sentence)
    print(sentence)
    
##################################################################

sent1 = Function('/xy.xxyy')
sent2 = 'yy'
sent3 = Function('/bc.c')

sent1.beta_reduce([sent3])
sent1()

sent1.beta_reduce([sent2])
sent1()

print(preprocess1('/x./y.xxyy'))
main()

test_cases(3)
