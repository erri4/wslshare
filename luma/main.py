from functions import isnumber
import re


###################################################
'''
get something's body return


function func (param){
    if (param == "string"){
        show (param)
    }
}

result:
if (param == "strincd show (param)
'''
###################################################
'''
TODO:
. elif/else
read all the elif's/else and then:
if condition: # handle if
    if body
else:
    stopped = false
    for con in conditions:
        if eval(con): # handle elif
            elif body
            stopped = true
            break
    if stopped: # handle else
        else body
. lists, length, type
. import

. dictinaries


. classes
'''
class LumaInterpreter:
    def __init__(self):
        self.functions: dict = {}
        self.vars: dict = {}
        self.localparams: list[dict[str]] = []
        self.returnedvalue = None


    def run(self, program: str, filename: str):
        self.scopes: list[str] = [program]
        linenum = 1
        for line in program.splitlines():
            #try:
            self.process(line, linenum - 1)
            linenum += 1
            '''except self.LumaNameError as e:
                print(f'File "{filename}", line {linenum}')
                print(f'    {line}')
                print(e)
                break'''
            '''except self.LumaSyntaxError as e:
                print(f'File "{filename}", line {linenum}')
                print(f'    {line}')
                print(e)
                break'''
            '''except self.LumaException as e:
                print(f'File "{filename}", line {linenum}')
                print(f'    {line}')
                print(e)
                break'''
            '''except Exception as e:
                print(f'File "{filename}", line {linenum}')
                print(f'    {line}')
                print(e)
                break'''
    

    def getfirstword(self, line: str):
        return line.split(' ')[0]


    def process(self, line: str, linenum: int):
        program = self.scopes[-1]
        if line.startswith('function'):
            print(program)
            func_name = line[9:line.find(' (')]
            args = line[line.find(' (') + 2:line.find(')')].split(', ')
            if args == ['']:
                args = []
            a = program[program.find(f'{func_name} (') + len(func_name) + 2:]
            stop = linenum
            for linee in a[a.find('){') + 2:].splitlines():
                if linee[0] == '}':
                    print(a[a.find('){') + 2:])
                    break
                stop += 1
            body = a[a.find('){') + 2:stop].strip()
            self.functions[func_name] = self.LumaFunction(func_name, args, body)
        elif line.startswith('show'):
            arg = self.evaluate(line[line.find('show (') + 6:len(line) - 1])
            print(arg)
        elif line.startswith('set'):
            varname = line[4:line.find('to') - 1]
            value = self.evaluate(line[line.find('to') + 3:])
            self.vars[varname] = value
        elif line.startswith('if'):
            print(program)
            condition = line[4:line.find(')')]
            a = "\n".join(program.splitlines()[linenum:])
            body = a[a.find('){') + 2:a.find('}')].strip()
            condition = self.processcondition(condition)
            conditions = []
            bodys = []
            while program.splitlines()[linenum].startswith('elif'):
                cond = line[6:line.find(')')]
                a = "\n".join(program.splitlines()[linen:])
                bd = a[a.find('){') + 2:a.find('}')].strip()
                conditions.append(self.processcondition(cond))
                bodys.append(bd)
                linenum += len(a[a.find('){') + 2:a.find('}')].strip().splitlines())
            if program.splitlines()[linenum].startswith('else'):
                pass
            if eval(condition):
                self.scopes.append(body)
                for subline in body.splitlines():
                    self.process(subline, 1)
                self.scopes.pop()
        elif line.startswith('while'):
            condition = line[7:line.find(')')]
            a = "\n".join(program.splitlines()[linenum:])
            body = a[a.find('){') + 2:a.find('}')].strip()
            processedcondition = self.processcondition(condition)
            self.scopes.append(body)
            while eval(processedcondition):
                linen = 1
                for subline in body.splitlines():
                    self.process(subline.replace('    ', '', 1), linen)
                processedcondition = self.processcondition(condition)
                linen += 1
            self.scopes.pop()
        elif len(self.localparams) > 0 and line.startswith('return'):
            value = line[7:]
            self.returnedvalue = self.evaluate(value.strip())
        elif line.startswith('#') or line == '' or line.startswith(' ') or line == '}':
            pass
        else:
            if self.getfirstword(line) in self.functions.keys():
                args = self.extractargs(line)
                if len(args) == len(self.functions[self.getfirstword(line)].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[self.getfirstword(line)].args[i]] = args[i]
                    self.localparams.append(argdict)
                    linen = 1
                    self.scopes.append(self.functions[self.getfirstword(line)].body)
                    for subline in self.functions[self.getfirstword(line)].body.splitlines():
                        self.process(subline.replace('    ', '', 1), linen)
                        if subline.startswith('return'):
                            break
                        linen += 1
                    self.scopes.pop()
                    self.localparams.pop()
            else:
                print(line)
                raise self.LumaNameError(f"undefined function {line}")
    

    def processcondition(self, condition: str):
        parts: list[str] = re.findall(r"(not|and|or|\S+\s*(?:==|!=|>=|<=|>|<)\s*\S+|\S+)", condition)
        result: list[str] = [part.strip() for part in parts if part.strip()]
        for i in range(len(result)):
            if result[i] != 'and' and result[i] != 'or' and result[i] != 'not':
                operator = ''
                for op in [' == ', ' > ', ' < ', ' => ', ' >= ', ' =< ', ' <= ']:
                    if len(result[i].split(op)) == 2:
                        operator = str(op)
                result[i] = operator.join([str(self.evaluateeval(result[i].split(operator)[0])), str(self.evaluateeval(result[i].split(operator)[1]))])
        return ' '.join(result)


    def extractargs(self, line: str):
        rawargs = line[line.find(' (') + 2:line.find(')')]
        args = rawargs.split(', ')
        res = []
        instring = False
        cuarg = ''
        if len(args) > 0 and args[0] != '':
            for i in range(len(args)):
                if not instring:
                    if args[i][0] == '"' and args[i][-1] != '"':
                        cuarg += args[i]
                        instring = True
                    else:
                        res.append(self.evaluate(args[i]))
                else:
                    if args[i].count('"') == 1:
                        cuarg += f', {args[i]}'
                        res.append(self.evaluate(cuarg))
                        cuarg = ''
                        instring = False
                    else:
                        cuarg += f', {args[i]}'
        return res


    def evaluateeval(self, expr: str, recursable: bool = True):
        scopes = list(reversed(self.localparams))
        if expr.startswith('input'):
            arg = self.evaluateeval(expr[expr.find('input (') + 7:len(expr) - 1])
            i = input(arg)
            if isnumber(i):
                return int(i)
            else:
                return f'"{str(i)}"'
        for scope in scopes:
            if expr in scope.keys():
                return f'"{scope[expr]}"'
        if isnumber(expr):
            return int(expr)
        elif not bool(re.search(r'[a-zA-Z]', expr)):
            try:
                result = eval(expr)
                return result
            except:
                raise self.LumaSyntaxError("invalid syntax")
        elif expr in self.vars.keys():
            return f'"{self.vars[expr]}"'
        elif ' + ' in expr:
            res = ''
            terms = expr.split(' + ')
            if recursable:
                for i in range(len(terms) - 1):
                    if not isnumber(self.evaluateeval(terms[i])):
                        res += '"' + self.evaluateeval(terms[i]) + '" + '
                    else:
                        res += str(self.evaluateeval(terms[i])) + ' + '
                if not isnumber(self.evaluateeval(terms[-1])):
                    res += '"' + self.evaluateeval(terms[-1]) + '"'
                else:
                    res += str(self.evaluateeval(terms[-1]))
                return self.evaluateeval(res, False)
            else:
                for term in terms:
                    res += str(self.evaluateeval(term))
                return res
        elif expr.startswith('"') and expr.endswith('"'):
            return expr
        elif self.getfirstword(expr) in self.functions.keys():
            if 'return' in self.functions[self.getfirstword(expr)].body:
                args = self.extractargs(expr.strip())
                if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                    self.localparams.append(argdict)
                    self.scopes.append(self.functions[self.getfirstword(expr.strip())].body)
                    linen = 1
                    for subline in self.functions[self.getfirstword(expr.strip())].body.splitlines():
                        self.process(subline.replace('    ', '', 1), linen)
                        if subline.startswith('return'):
                            break
                        linen += 1
                    self.scopes.pop()
                    self.localparams.pop()
                    return f'"{self.returnedvalue}"'
            else:
                return None
        else:
            print(expr)
            raise LumaInterpreter.LumaNameError(f"undefined variable {expr}")


    def evaluate(self, expr: str, recursable: bool = True):
        scopes = list(reversed(self.localparams))
        if expr.startswith('input'):
            arg = self.evaluate(expr[expr.find('input (') + 7:len(expr) - 1])
            i = input(arg)
            if isnumber(i):
                return int(i)
            else:
                return str(i)
        for scope in scopes:
            if expr in scope.keys():
                return scope[expr]
        if isnumber(expr):
            return int(expr)
        elif not bool(re.search(r'[a-zA-Z]', expr)):
            try:
                result = eval(expr)
                return result
            except:
                raise self.LumaSyntaxError("invalid syntax")
        elif expr in self.vars.keys():
            return self.vars[expr]
        elif ' + ' in expr:
            res = ''
            terms = expr.split(' + ')
            if recursable:
                for i in range(len(terms) - 1):
                    if not isnumber(self.evaluate(terms[i])):
                        res += '"' + self.evaluate(terms[i]) + '" + '
                    else:
                        res += str(self.evaluate(terms[i])) + ' + '
                if not isnumber(self.evaluate(terms[-1])):
                    res += '"' + self.evaluate(terms[-1]) + '"'
                else:
                    res += str(self.evaluate(terms[-1]))
                return self.evaluate(res, False)
            else:
                for term in terms:
                    res += str(self.evaluate(term))
                return res
        elif expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]
        elif self.getfirstword(expr) in self.functions.keys():
            if 'return' in self.functions[self.getfirstword(expr)].body:
                args = self.extractargs(expr.strip())
                if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                    self.localparams.append(argdict)
                    self.scopes.append(self.functions[self.getfirstword(expr.strip())].body)
                    linen = 1
                    for subline in self.functions[self.getfirstword(expr.strip())].body.splitlines():
                        self.process(subline.replace('    ', '', 1), linen)
                        if subline.startswith('return'):
                            break
                        linen += 1
                    self.scopes.pop()
                    self.localparams.pop()
                    return self.returnedvalue
            else:
                return None
        else:
            print(expr)
            raise LumaInterpreter.LumaNameError(f"undefined variable {expr}")

    class LumaFunction:
        def __init__(self, name: str, args: list[str], body: str):
            self.name = name
            self.args = args
            self.body = body


    class LumaNameError(NameError):
        def __init__(self, *args):
            super().__init__(*args)


    class LumaException(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    
    class LumaSyntaxError(SyntaxError):
        def __init__(self, *args):
            super().__init__(*args)


filename = input()
interpreter = LumaInterpreter()
if filename.endswith('.lum'):
    try:
        with open(f'{filename}') as file:
            program = file.read()
        interpreter.run(program, filename)
    except FileNotFoundError:
        print(f'The file {filename} does not exists.')
else:
    print(f'The file {filename} is not a luma program.')
