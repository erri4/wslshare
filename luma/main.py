from functions import isnumber, reverse_list
from types import FunctionType
import re


###################################################
'''
TODO:
. (lists, length), type

. dictinaries


. classes # I don't think so
'''
class LumaInterpreter:
    def __init__(self):
        self.functions: dict[str] = {}
        def nativecode(pytext):
            return eval(pytext)
        self.functions['nativecode'] = self.LumaFunction('nativecode', ['pytext'], nativecode)
        self.vars: dict[str] = {'true': True, 'false': False}
        self.localparams: list[dict[str]] = []
        self.returnedvalue = None


    def run(self, program: str, filename: str):
        self.vars['__file__'] = filename
        self.scopes: list[str] = [program]
        self.runimport('builtins.lum')
        linenum = 1
        for line in program.splitlines():
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
    

    def removetab(self, line: str):
        return line.replace('    ', '', 1) if line.startswith('    ') else line
    

    def runimport(self, module):
        with open(module) as imported:
            linen = 1
            subprogram = imported.read()
            self.scopes.append(subprogram)
            for subline in subprogram.splitlines():
                self.process(subline, linen)
                linen += 1
            self.scopes.pop()
    

    def runsubprogram(self, subprogram: str):
        linen = 1
        subprogram = subprogram.splitlines()
        for i in range(len(subprogram)):
            subprogram[i] = self.removetab(subprogram[i])
        subprogram = '\n'.join(subprogram)
        self.scopes.append(subprogram)
        for subline in subprogram.splitlines():
            self.process(subline, linen)
            if subline.startswith('return'):
                break
            linen += 1
        self.scopes.pop()


    def process(self, line: str, linenum: int):
        program = self.scopes[-1]
        if line.startswith('function'):
            func_name = line[9:line.find(' (')]
            args = line[line.find(' (') + 2:line.find(')')].split(', ')
            if args == ['']:
                args = []
            a = program[program.find(f'{func_name} (') + len(func_name) + 2:]
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee[0] == '}':
                    break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            self.functions[func_name] = self.LumaFunction(func_name, args, body)
        elif line.startswith('set'):
            varname = line[4:line.find('to') - 1]
            value = self.evaluate(line[line.find('to') + 3:])
            self.vars[varname] = value
        elif line.startswith('import'):
            module = line[7:]
            self.runimport(module)
        elif line.startswith('if'):
            condition = line[4:line.find('){')]
            a = "\n".join(program.splitlines()[linenum - 1:])
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee[0] == '}':
                    break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            condition = self.processcondition(condition)
            conditions = []
            bodys = []
            linenu = int(linenum) + len(body.splitlines()) + 2
            subline = self.removetab(program.splitlines()[linenu - 1])
            while subline.startswith('elif'):
                cond = subline[6:subline.find(')')]
                a = "\n".join(program.splitlines()[linenu - 1:])
                bd = a[a.find('){') + 2:a.find('}')].strip()
                conditions.append(self.processcondition(cond))

                bodys.append(bd)
                linenu += len(bd.splitlines()) + 2

                try:
                    subline = self.removetab(program.splitlines()[linenu - 1])
                except IndexError:
                    break
            subline = self.removetab(program.splitlines()[linenu - 1])
            elsebody = ''
            if subline.startswith('else'):
                a = "\n".join(program.splitlines()[linenu - 1:])
                elsebody = a[a.find('{') + 1:a.find('}')].strip()
            if eval(condition):
                self.runsubprogram(body)
            else:
                stopped = False
                for i in range(len(conditions)):
                    con = conditions[i]
                    bd: str = bodys[i]
                    if eval(con):
                        self.runsubprogram(bd)
                        stopped = True
                        break
                if not stopped:
                    self.runsubprogram(elsebody)
        elif line.startswith('while'):
            condition = line[7:line.find('){')]
            a = "\n".join(program.splitlines()[linenum - 1:])
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee[0] == '}':
                    break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            processedcondition = self.processcondition(condition)
            while eval(processedcondition):
                self.runsubprogram(body)
                processedcondition = self.processcondition(condition)
        elif len(self.localparams) > 0 and line.startswith('return'):
            value = line[7:]
            self.returnedvalue = self.evaluate(value.strip())
        elif line.startswith('#') or line == '' or line.startswith(' ') or line == '}' or line.startswith('elif') or line.startswith('else'):
            pass
        else:
            if self.getfirstword(line) in self.functions.keys():
                func_name = self.getfirstword(line)
                args = self.extractargs(line, func_name)
                if len(args) == len(self.functions[func_name].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[func_name].args[i]] = args[i]
                    self.localparams.append(argdict)
                    if type(self.functions[func_name].body) == str:
                        self.runsubprogram(self.functions[func_name].body)
                    else:
                        self.functions[func_name].body(*args)
                    self.localparams.pop()
            else:
                raise self.LumaNameError(f"undefined function {self.getfirstword(line)}")
    

    def processcondition(self, condition: str):
        match = re.search(r' (==|<=|>=|>|<) ', condition)
        if not match:
            return self.evaluateeval(condition.strip())

        op = match.group(1)
        parts = condition.split(f' {op} ', 1)
        left = self.evaluateeval(parts[0].strip())
        right = self.evaluateeval(parts[1].strip())
        return f"{left} {op} {right}"


    def extractargs(self, line: str, funcname):
        rawargs = line[line.find(' (') + 2:-1]
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
    

    def alltermsclosed(self, exprs: list[str]):
        res = []
        for expr in exprs:
            stack = []
            inside_quotes = False

            pairs = {')': '(', ']': '[', '}': '{'}
            openers = set(pairs.values())

            i = 0
            while i < len(expr):
                char = expr[i]

                if char == '"':
                    inside_quotes = not inside_quotes
                elif not inside_quotes:
                    if char in openers:
                        stack.append(char)
                    elif char in pairs:
                        if not stack or stack[-1] != pairs[char]:
                            res.append(False)
                        else:
                            stack.pop()

                i += 1

            res.append(not inside_quotes and not stack)

        for protected in res:
            if protected == False:
                return False
        return True




    def evaluateeval(self, expr: str, recursable: bool = True):
        scopes: list[dict] = reverse_list(self.localparams)
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
            return f'"{self.vars[expr]}"'
        elif ' + ' in expr and self.alltermsclosed(expr.split(' + ')):
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
        elif expr.startswith('"') and expr.endswith('"') and not '"' in expr[1:-1]:
            return expr
        elif self.getfirstword(expr) in self.functions.keys():
            if type(self.functions[self.getfirstword(expr)].body) == str:
                if 'return' in self.functions[self.getfirstword(expr)].body:
                    args = self.extractargs(expr.strip(), self.getfirstword(expr))
                    if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                        argdict = {}
                        for i in range(len(args)):
                            argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                        self.localparams.append(argdict)
                        self.runsubprogram(self.functions[self.getfirstword(expr.strip())].body)
                        self.localparams.pop()
                        return self.returnedvalue
                else:
                    return None
            else:
                args = self.extractargs(expr.strip(), self.getfirstword(expr))
                if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                    self.localparams.append(argdict)
                    self.returnedvalue = self.functions[self.getfirstword(expr)].body(*args)
                    self.localparams.pop()
                    return self.returnedvalue
        else:
            raise LumaInterpreter.LumaNameError(f"undefined variable '{expr}'")


    def evaluate(self, expr: str, recursable: bool = True):
        scopes: list[dict] = reverse_list(self.localparams)
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
        elif ' + ' in expr and self.alltermsclosed(expr.split(' + ')):
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
        elif expr.startswith('"') and expr.endswith('"') and not '"' in expr[1:-1]:
            return expr[1:-1]
        elif self.getfirstword(expr) in self.functions.keys():
            if type(self.functions[self.getfirstword(expr)].body) == str:
                if 'return' in self.functions[self.getfirstword(expr)].body:
                    args = self.extractargs(expr.strip(), self.getfirstword(expr))
                    if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                        argdict = {}
                        for i in range(len(args)):
                            argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                        self.localparams.append(argdict)
                        self.runsubprogram(self.functions[self.getfirstword(expr.strip())].body)
                        self.localparams.pop()
                        return self.returnedvalue
                else:
                    return None
            else:
                args = self.extractargs(expr.strip(), self.getfirstword(expr))
                if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                    argdict = {}
                    for i in range(len(args)):
                        argdict[self.functions[self.getfirstword(expr.strip())].args[i]] = args[i]
                    self.localparams.append(argdict)
                    self.returnedvalue = self.functions[self.getfirstword(expr)].body(*args)
                    self.localparams.pop()
                    return self.returnedvalue
        else:
            raise LumaInterpreter.LumaNameError(f"undefined variable '{expr}'")

    class LumaFunction:
        def __init__(self, name: str, args: list[str], body: str | FunctionType):
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
