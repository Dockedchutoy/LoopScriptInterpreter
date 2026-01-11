"""
NOTES:
variables are expressed by integer
unknown characters are ignored (comments!)
.ls file extension

COMMAND LIST:
+n => add 1 to variable n
-n => remove 1 from variable n
%n => save input to variable n
$n => output variable n, depending on value
(commands)n => Loop commands while n is not 0
?n => save random integer from {1,2,...,n} to variable n
"""
from random import randint

# Objects for interpreter

class Token():
    def __init__(self, op: str, var: int):
        self.op = op
        self.var = var
    
    def __repr__(self):
        return f"Token[{self.op} >> {self.var}]"

class LoopToken():
    def __init__(self, op: str, part: int, var: int):
        self.op = op
        self.part = part  # part is the partner parenthesis index
        self.var = var
    
    def __repr__(self):
        return f"LoopToken[{self.op} >> {self.part} >> {self.var}]"
    
class LoopScriptError(RuntimeError):
    def __init__(self, problem, *args):
        self.problem = problem
        super().__init__(*args)

# Interpreter

class LoopScript():

    # Parser
    
    def parse(self, source: str):
        program = [] # The program executed
        parens = [] # For parenthesis
        char = 0
        variable = ""

        while char < len(source):
            match source[char]:
                case "+" | "-" | "%" | "$":
                    op = source[char]
                    # Find variable
                    char += 1
                    while char < len(source) and source[char].isdigit():
                        variable += source[char]
                        char += 1
                    if not variable:
                        raise LoopScriptError("Missing variable or invalid variable name")
                    
                    program.append(Token(op, int(variable)))
                
                case "(":
                    program.append(LoopToken("(", None, None))
                    parens.append(len(program) - 1) # Adds opener index
                    char += 1
                
                case ")":
                    op = source[char]
                    # Find variable
                    char += 1
                    while char < len(source) and source[char].isdigit():
                        variable += source[char]
                        char += 1
                    if not variable:
                        raise LoopScriptError("Missing variable or invalid variable name")
                    
                    partindex = parens.pop()
                    program.append(LoopToken(op, partindex, int(variable)))
                    program[partindex].part = len(program) - 1
                    program[partindex].var = int(variable)

        
            variable = ""
        
        if parens:
            raise LoopScriptError("Loop not properly enclosed")
        
        program.append(Token("EOF", -1))

        return program
    
    # Execution
    
    def execute(self, program: list):
        env = {} # All variables are stored here
        tkn = 0

        while tkn < len(program):
            cmd = program[tkn]

            if cmd.var not in env:  # Initialize variable
                env[cmd.var] = 0

            if cmd.op == "+": # Increment
                env[cmd.var] += 1
        
            elif cmd.op == "-": # Increment
                env[cmd.var] -= 1
            
            elif cmd.op == "$": # Output
                print(env[cmd.var])
            
            elif cmd.op == "%": # Input
                set = input()
                if not set.isnumeric():
                    set = ord(set[0])
                env[cmd.var] = int(set)
            
            elif cmd.op == "(": # Loop start
                if env[cmd.var] == 0:
                    tkn = cmd.part
            
            elif cmd.op == ")": # Loop end
                tkn = cmd.part
                continue
        
            tkn += 1

# Main

if __name__ == "__main__":
    running = True

    print("LoopScript Python Interpreter v1.0")
    while running:
        code = input(" >>")
        try:
            ls = LoopScript()
            tokens = ls.parse(code)
            ls.execute(tokens)
        except LoopScriptError as e:
            print(f"Error: {e.problem}")