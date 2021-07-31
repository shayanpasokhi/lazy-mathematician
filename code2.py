import sys
import math

STRING, ASSIGNMENT, NUMBER, END, LPAREN, COMMA, RPAREN, EOF = 'STRING', 'ASSIGNMENT', 'NUMBER', 'END', 'LPAREN', 'COMMA', 'RPAREN', 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentChar = self.text[self.pos]

    def error(self):
        print('Invalid character')
        sys.exit()

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.currentChar = None
        else:
            self.currentChar = self.text[self.pos]

    def skipWhitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()

    def number(self):
        result = ''
        idDot = False

        while self.currentChar is not None and (self.currentChar.isdigit() or (self.currentChar == '.' and not idDot)):
            if self.currentChar == '.':
                isDot = True
            result += self.currentChar
            self.advance()

        if result[-1] == '.':
            self.error()
        
        return float(result)

    def string(self):
        result = ''

        while self.currentChar is not None and (self.currentChar.isalpha() or self.currentChar == '_'):
            result += self.currentChar
            self.advance()
        
        return result

    def getNextToken(self):
        while self.currentChar is not None:
            if self.currentChar.isspace():
                self.skipWhitespace()

                continue

            if self.currentChar.isalpha() or self.currentChar == '_':
                string = self.string()

                if string == 'end':
                    return Token(END, string)

                return Token(STRING, string)

            if self.currentChar.isdigit():
                return Token(NUMBER, self.number())

            if self.currentChar == ':':
                self.advance()

                if self.currentChar == '=':
                    self.advance()

                    return Token(ASSIGNMENT, ':=')
                else:
                    self.error()

            if self.currentChar == '(':
                self.advance()

                return Token(LPAREN, '(')

            if self.currentChar == ')':
                self.advance()

                return Token(RPAREN, ')')

            if self.currentChar == ',':
                self.advance()

                return Token(COMMA, ',')

            self.error()

        return Token(EOF, None)

class Interpreter:
    def __init__(self, lexer, variableDict):
        self.lexer = lexer
        self.currentToken = self.lexer.getNextToken()
        self.variableDict = variableDict

    def error(self):
        print('Invalid syntax')
        sys.exit()

    def getVariable(self, name):
        if name in self.variableDict:
            return self.variableDict[name]

        return None

    def calculator(self, name, arg1, arg2):
        if name == 'add':
            return arg1 + arg2
        elif name == 'sub':
            return arg1 - arg2
        elif name == 'mul':
            return arg1 * arg2
        elif name == 'div':
            return arg1 / arg2
        elif name == 'pow':
            return math.pow(arg1, arg2)
        elif name == 'gcd':
            return math.gcd(int(arg1), int(arg2))
        elif name == 'log':
            return math.log(arg1, arg2)
        else:
            return None

    def printNumber(self, number):
        return '{:.3f}'.format(number)

    def setVariable(self, name, value):
        self.variableDict[name] = value

        return self.variableDict

    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def variable(self):
        token = self.currentToken
        self.eat(STRING)

        return token.value

    def arg(self):
        if self.currentToken.type == NUMBER:
            token = self.currentToken
            self.eat(NUMBER)

            return token.value
        else:
            variable = self.variable()

            return variable

    def formatNumber(self, number):
        if number % 1 == 0:
            return int(number)
        else:
            return number

    def expr(self):
        if self.currentToken.type == END:
            self.eat(END)
            sys.exit()
        else:
            lVariable = self.variable()

            if self.currentToken.type != EOF:
                self.eat(ASSIGNMENT)

                if self.currentToken.type == NUMBER:
                    token = self.currentToken
                    self.eat(NUMBER)
                    
                    result = self.setVariable(lVariable, token.value)

                    if self.currentToken.type != EOF:
                        result = str(self.formatNumber(token.value)) + str(self.currentToken.value) + ' is not a number'

                        return result

                    self.eat(EOF)

                    return result
                else:
                    rVariable = self.variable()
                    
                    if self.currentToken.type == LPAREN:
                        self.eat(LPAREN)
                        arg1 = self.arg()

                        if isinstance(arg1, str):
                            arg1Value = self.getVariable(arg1)

                            if arg1Value is None:
                                result = 'variable error'

                                return result
                        else:
                            if self.currentToken.type != COMMA:
                                result = str(self.formatNumber(arg1)) + str(self.currentToken.value) + ' is not a number'

                                return result

                            arg1Value = arg1

                        self.eat(COMMA)
                        arg2 = self.arg()

                        if isinstance(arg2, str):
                            arg2Value = self.getVariable(arg2)

                            if arg2Value is None:
                                result = 'variable error'

                                return result
                        else:
                            if self.currentToken.type != RPAREN:
                                result = str(self.formatNumber(arg2)) + str(self.currentToken.value) + ' is not a number'

                                return result

                            arg2Value = arg2
                        
                        self.eat(RPAREN)
                        self.eat(EOF)

                        calc = self.calculator(rVariable, arg1Value, arg2Value)

                        if calc is None:
                            result = 'function not found'
                        else:
                            result = self.setVariable(lVariable, calc)

                        return result
                    else:
                        self.eat(EOF)
                        rVarValue = self.getVariable(rVariable)

                        if rVarValue is None:
                            result = 'variable error'
                        else:
                            result = self.setVariable(lVariable, rVarValue)

                        return result
            else:
                self.eat(EOF)
                lVarValue = self.getVariable(lVariable)

                if lVarValue is None:
                    result = 'variable not found'
                else:
                    result = self.printNumber(lVarValue)
                    
                return result

def main():
    variableDict = {}

    while True:
        try:
            text = input('')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        interpreter = Interpreter(lexer, variableDict)
        result = interpreter.expr()
        
        if isinstance(result, dict):
             variableDict = result
        else:
            print(result)

if __name__ == '__main__':
    main()