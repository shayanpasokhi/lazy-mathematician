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

class NodeVisitor:
    def visit(self, node):
        methodName = 'visit' + type(node).__name__
        visitor = getattr(self, methodName, self.genericVisit)

        return visitor(node)

    def genericVisit(self, node):
        print('No visit{} method'.format(type(node).__name__))
        sys.exit()

class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def formatNumber(self, number):
        return '{:.3f}'.format(number)

    def visitAssign(self, node):
        varName = node.left.value
        right = self.visit(node.right)

        if right == 'variable not found' or right == 'variable error':
            return 'variable error'
        elif 'is not a number' in str(right):
            return right
        elif right == 'function not found':
            return right

        self.GLOBAL_SCOPE[varName] = self.visit(node.right)

    def visitVar(self, node):
        varName = node.value
        val = self.GLOBAL_SCOPE.get(varName)
        
        if val is None:
            return 'variable not found'
        else:
            return self.formatNumber(val)

    def visitNum(self, node):
        return node.value
    
    def visitFunction(self, node):
        if node.value == 'add':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return float(arg1) + float(arg2)
        elif node.value == 'sub':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return float(arg1) - float(arg2)
        elif node.value == 'mul':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return float(arg1) * float(arg2)
        elif node.value == 'div':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return float(arg1) / float(arg2)
        elif node.value == 'pow':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return math.pow(float(arg1), float(arg2))
        elif node.value == 'gcd':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return math.gcd(int(float(arg1)), int(float(arg2)))
        elif node.value == 'log':
            arg1 = self.visit(node.arg[0])
            arg2 = self.visit(node.arg[1])

            if arg1 == 'variable not found' or arg2 == 'variable not found':
                return 'variable error'

            if 'is not a number' in str(arg1):
                return arg1
            elif 'is not a number' in str(arg2):
                return arg2

            return math.log(float(arg1), float(arg2))
        else:
            return 'function not found'

    def visitEnd(self, node):
        sys.exit()

    def visitError(self, node):
        return node.message

    def interpret(self):
        tree = self.parser.parse()

        return self.visit(tree)

def main():
    while True:
        try:
            text = input('')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        
        if result is not None:
            print(result)

if __name__ == '__main__':
    main()
