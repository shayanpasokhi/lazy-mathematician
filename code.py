import math, re

variables = {}
functions = ['add', 'sub', 'mul', 'div', 'pow', 'gcd', 'log']

assignmentSign = ':='
assignmentSignPattern = '\:\='
variablePattern = '[a-zA-z\_]+'
numberPattern = '\d+(\.\d+)?'
simpleAssignmentPattern = variablePattern + assignmentSignPattern + '.+'
simpleFunctionPattern = '.+\(.+\,.+\)'
notNumberPattern = '(\d*(\.{2,}|\D+\.\D+|[^\.^\d])\d*|^\.|\.&|\.+.*\.+)'

def absolutePattern(pattern):
    return '^' + pattern + '$'

def calculator(functionName, argument1, argument2):
    if functionName == 'add':
        return argument1 + argument2
    elif functionName == 'sub':
        return argument1 - argument2
    elif functionName == 'mul':
        return argument1 * argument2
    elif functionName == 'div':
        return argument1 / argument2
    elif functionName == 'pow':
        return math.pow(argument1, argument2)
    elif functionName == 'gcd':
        return math.gcd(int(argument1), int(argument2))
    elif functionName == 'log':
        return math.log(argument1, argument2)

while True:
    try:
        line = input().replace(' ', '')
        
        if line != 'end':
            if re.search(absolutePattern(simpleAssignmentPattern), line):
                leftStatement, rightStatement = line.split(assignmentSign)

                if re.search(absolutePattern(simpleFunctionPattern), rightStatement):
                    functionName, tmp = rightStatement.split('(')
                    argument1, tmp = tmp.split(',')
                    argument2 = tmp.split(')')[0]

                    if functionName in functions:
                        if re.search(absolutePattern(variablePattern), argument1):
                            if argument1 not in variables:
                                raise Exception('variable error')
                            else:
                                argument1 = variables[argument1]
                        elif re.search(notNumberPattern, argument1):
                            raise Exception(argument1 + ' is not a number')

                        if re.search(absolutePattern(variablePattern), argument2):
                            if argument2 not in variables:
                                raise Exception('variable error')
                            else:
                                argument2 = variables[argument2]
                        elif re.search(notNumberPattern, argument2):
                            raise Exception(argument2 + ' is not a number')
                        
                        variables[leftStatement] = calculator(functionName, float(argument1), float(argument2))
                    else:
                        raise Exception('function not found')
                elif re.search(absolutePattern(variablePattern), rightStatement):
                    if rightStatement in variables:
                        variables[leftStatement] = variables[rightStatement]
                    else:
                        raise Exception('variable error')
                elif re.search(absolutePattern(numberPattern), rightStatement):
                    variables[leftStatement] = float(rightStatement)
                elif re.search(notNumberPattern, rightStatement):
                    raise Exception(rightStatement + ' is not a number')
            elif re.search(absolutePattern(variablePattern), line):
                if line in variables:
                    print('{:.3f}'.format(variables[line]))
                else:
                    raise Exception('variable not found')
        else:
            break
    except Exception as e:
        print(e)
