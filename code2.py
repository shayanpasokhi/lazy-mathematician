import sys
import math

ID, ASSIGN, NUMBER, END, LPAREN, COMMA, RPAREN, ADD, SUB, MUL, DIV, POW, GCD, LOG, EOF = 'ID', 'ASSIGN', 'NUMBER', 'END', 'LPAREN', 'COMMA', 'RPAREN', 'ADD', 'SUB', 'MUL', 'DIV', 'POW', 'GCD', 'LOG', 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORD = {
    ADD.lower(): Token(ADD, ADD.lower()),
    SUB.lower(): Token(SUB, SUB.lower()),
    MUL.lower(): Token(MUL, MUL.lower()),
    DIV.lower(): Token(DIV, DIV.lower()),
    POW.lower(): Token(POW, POW.lower()),
    GCD.lower(): Token(GCD, GCD.lower()),
    LOG.lower(): Token(LOG, LOG.lower()),
    END.lower(): Token(END, END.lower())
} 

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentChar = self.text[self.pos]

    def error(self, message='Invalid character'):
        print(message)
        sys.exit()

    def advance(self):
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.currentChar = None
        else:
            self.currentChar = self.text[self.pos]

    def peek(self):
        peekPos = self.pos + 1

        if peekPos > len(self.text) - 1:
            return None
        else:
            return self.text[peekPos]

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

    def _id(self):
        result = ''

        while self.currentChar is not None and (self.currentChar.isalpha() or self.currentChar == '_'):
            result += self.currentChar
            self.advance()
        
        return RESERVED_KEYWORD.get(result, Token(ID, result))

    def getNextToken(self):
        while self.currentChar is not None:
            if self.currentChar.isspace():
                self.skipWhitespace()

                continue

            if self.currentChar.isalpha() or self.currentChar == '_':
                return self._id()

            if self.currentChar.isdigit():
                return Token(NUMBER, self.number())

            if self.currentChar == ':' and self.peek() == '=':
                self.advance()
                self.advance()

                return Token(ASSIGN, ':=')

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

class AST:
    pass

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Function(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.arg = []

class End(AST):
    pass

class Error(AST):
    def __init__(self, message):
        self.message = message

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.getNextToken()

    def error(self, message='Invalid syntax'):
        print(message)
        sys.exit()

    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def forwardError(self, token):
        message = str(self.formatNumber(token.value)) + str(self.currentToken.value) + ' is not a number'

        while self.currentToken.type != EOF:
            self.currentToken = self.lexer.getNextToken()

        return message

    def formatNumber(self, number):
        if number % 1 == 0:
            return int(number)
        else:
            return number

    def program(self):
        if self.currentToken.type == END:
            self.eat(END)

            return End()
        else:
            node = self.variable()

            if self.currentToken.type == ASSIGN:
                token = self.currentToken
                self.eat(ASSIGN)

                return Assign(node, token, self.expr())
            elif self.currentToken.type != EOF:
                self.error()

            return node

    def variable(self):
        token = self.currentToken
        self.eat(ID)

        return Var(token)

    def expr(self):
        if self.currentToken.type == NUMBER:
            token = self.currentToken
            self.eat(NUMBER)

            if self.currentToken.type != EOF:
                return Error(self.forwardError(token))
            return Num(token)
        else:
            node = self.function()

            if self.currentToken.type == LPAREN:
                self.eat(LPAREN)
                root = Function(node)
                arg1 = self.arg()

                if self.currentToken.type != COMMA:
                    return Error(self.forwardError(arg1))
                root.arg.append(arg1)
                self.eat(COMMA)
                arg2 = self.arg()

                if self.currentToken.type != RPAREN:
                    return Error(self.forwardError(arg2))
                root.arg.append(arg2)
                self.eat(RPAREN)

                return root
            elif self.currentToken.type != EOF:
                self.error()

            return node

    def function(self):
        if self.currentToken.type == ADD:
            token = self.currentToken
            self.eat(ADD)
        elif self.currentToken.type == SUB:
            token = self.currentToken
            self.eat(SUB)
        elif self.currentToken.type == MUL:
            token = self.currentToken
            self.eat(MUL)
        elif self.currentToken.type == DIV:
            token = self.currentToken
            self.eat(DIV)
        elif self.currentToken.type == POW:
            token = self.currentToken
            self.eat(POW)
        elif self.currentToken.type == GCD:
            token = self.currentToken
            self.eat(GCD)
        elif self.currentToken.type == LOG:
            token = self.currentToken
            self.eat(LOG)
        else:
            return self.variable()

        return token

    def arg(self):
        if self.currentToken.type == NUMBER:
            token = self.currentToken
            self.eat(NUMBER)

            return Num(token)
        else:
            node = self.variable()

            return node

    def parse(self):
        node = self.program()

        if self.currentToken.type != EOF:
            self.error()

        return node

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
