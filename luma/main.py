from pypackage.functions import isnumber, reverse_list
from types import FunctionType
import copy
import re


###################################################
'''
TODO:
. add builtin classes

. lists (length)

. dictinaries
'''
class LumaInterpreter:
    def __init__(self):
        self.functions: dict[str, LumaInterpreter.LumaFunction] = {}
        def nativecode(pytext):
            return eval(pytext)
        self.functions['nativecode'] = self.LumaFunction('nativecode', ['pytext'], nativecode)
        self.classes: dict[str, LumaInterpreter.LumaClass] = {}
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
    

    def runsubprogram(self, subprogram: str, Object = None, returnto = None):
        if Object == None:
            Object = self
        if returnto == None:
            returnto = self
        linen = 1
        subprogram = subprogram.splitlines()
        for i in range(len(subprogram)):
            subprogram[i] = self.removetab(subprogram[i])
        subprogram = '\n'.join(subprogram)
        self.scopes.append(subprogram)
        for subline in subprogram.splitlines():
            self.process(subline, linen, Object, returnto)
            if subline.startswith('return'):
                break
            linen += 1
        self.scopes.pop()

    
    def process(self, line: str, linenum: int, Object = None, returnto = None):
        returnto: LumaInterpreter | LumaInterpreter.LumaClass
        if Object == None:
            vars = self.vars
            functions: dict[str, LumaInterpreter.LumaFunction] = self.functions
        else:
            Object: LumaInterpreter | LumaInterpreter.LumaClass
            vars = Object.vars
            functions: dict[str, LumaInterpreter.LumaFunction] = Object.functions
        program = self.scopes[-1]
        if line.startswith('function'):
            func_name = line[9:line.find(' (')]
            args = line[line.find(' (') + 2:line.find(')')].split(', ')
            if args == ['']:
                args = []
            a = program[program.find(f'{func_name} (') + len(func_name) + 2:]
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee != '':
                    if linee[0] == '}':
                        break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            functions[func_name] = self.LumaFunction(func_name, args, body)
        elif line.startswith('class'):
            class_name = line[6:line.find(' {')]
            a = program[program.find(f'class {class_name}' + ' {') + len(class_name) + 2:]
            stop = len(a[:a.find(' {') + 3])
            for linee in a[a.find(' {') + 3:].splitlines():
                if linee != '':
                    if linee[0] == '}':
                        break
                stop += len(linee) + 1
            body = a[a.find(' {') + 3:stop].strip()
            parent = None
            if '(' in class_name and ')' in class_name:
                parent = class_name[class_name.find('(') + 1:class_name.find(')')]
                class_name = class_name[:class_name.find('(') - 1]
                self.classes[class_name] = copy.deepcopy(self.classes[parent])
            else:
                self.classes[class_name] = self.LumaClass(class_name)
            self.runsubprogram(body, self.classes[class_name])
        elif line.startswith('constructor'):
            class_name = line[12:line.find(' (')]
            args = line[line.find(' (') + 2:line.find(')')].split(', ')
            if args == ['']:
                args = []
            a = program[program.find(f'{class_name} (') + len(class_name) + 2:]
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee != '':
                    if linee[0] == '}':
                        break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            functions['constructor'] = self.LumaFunction('constructor', args, body)
        elif line.startswith('set'):
            varname = line[4:line.find('to') - 1]
            value = self.evaluate(line[line.find('to') + 3:], True, varname)
            if varname.count('.') == 1:
                instancename = varname.split('.')[0]
                if instancename == 'this':
                    scopes: list[dict] = reverse_list(self.localparams)
                    for scope in scopes:
                        if 'this' in scope.keys():
                            scope['this'].vars[varname.split('.')[1]] = value
                elif varname.split('.')[0] in self.vars.keys():
                    vars[instancename].vars[varname.split('.')[1]] = value
            else:
                vars[varname] = value
        elif line.startswith('import'):
            module = line[7:]
            self.runimport(module)
        elif line.startswith('if'):
            condition = line[4:line.find('){')]
            a = "\n".join(program.splitlines()[linenum - 1:])
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee != '':
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
                stop = len(a[:a.find('){') + 3])
                for linee in a[a.find('){') + 3:].splitlines():
                    if linee != '':
                        if linee[0] == '}':
                            break
                    stop += len(linee) + 1
                bd = a[a.find('){') + 3:stop].strip()
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
                stop = len(a[:a.find('{') + 2])
                for linee in a[a.find('{') + 2:].splitlines():
                    if linee != '':
                        if linee[0] == '}':
                            break
                    stop += len(linee) + 1
                elsebody = a[a.find('{') + 2:stop].strip()
            if eval(condition):
                self.runsubprogram(body)
            else:
                foundelif = False
                for i in range(len(conditions)):
                    con = conditions[i]
                    bd: str = bodys[i]
                    if eval(con):
                        self.runsubprogram(bd)
                        foundelif = True
                        break
                if not foundelif:
                    self.runsubprogram(elsebody)
        elif line.startswith('while'):
            condition = line[7:line.find('){')]
            a = "\n".join(program.splitlines()[linenum - 1:])
            stop = len(a[:a.find('){') + 3])
            for linee in a[a.find('){') + 3:].splitlines():
                if linee != '':
                    if linee[0] == '}':
                        break
                stop += len(linee) + 1
            body = a[a.find('){') + 3:stop].strip()
            processedcondition = self.processcondition(condition)
            while eval(processedcondition):
                self.runsubprogram(body)
                processedcondition = self.processcondition(condition)
        elif line.startswith('return'):
            value = line[7:]
            vars[returnto].returnedvalue = self.evaluate(value.strip())
        elif line.startswith('#') or line == '' or line.startswith(' ') or line == '}' or line.startswith('elif') or line.startswith('else'):
            pass
        elif line.count('.') == 1 and self.getfirstword(line).split('.')[0] in self.vars.keys():
            dexpr = self.getfirstword(line)
            self.vars: dict[str, LumaInterpreter.LumaClass]
            instancename = dexpr.split('.')[0]
            propertyname = dexpr.split('.')[1]
            if propertyname in self.vars[instancename].functions.keys():
                args = self.extractargs(line.strip(), propertyname)
                if len(args) == len(self.vars[instancename].functions[propertyname].args):
                    self.vars[instancename].callmethod(propertyname, args, self, instancename)
        else:
            if self.getfirstword(line) in functions.keys():
                func_name = self.getfirstword(line)
                args = self.extractargs(line, func_name)
                if len(args) == len(functions[func_name].args):
                    functions[func_name].run(self, args)
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
        if rawargs == '':
            return []
        args = rawargs.split(', ')
        for i in range(len(args)):
            args[i] = self.evaluate(args[i])
        return args
    

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
        elif expr[0] == '&' and expr[1:] in self.vars.keys():
            return type(self.vars[expr[1:]]).__name__
        elif '.' in expr and expr.split('.')[0] in self.vars.keys():
            self.vars: dict[str, LumaInterpreter.LumaClass]
            instancename = expr.split('.')[0]
            propertyname = expr.split('.')[1]
            if propertyname in self.vars[instancename].vars.keys():
                return self.vars[instancename].vars[propertyname]
            elif propertyname in self.vars[instancename].functions.keys():
                args = self.extractargs(expr.strip(), propertyname)
                if len(args) == len(self.vars[instancename].functions[propertyname].args):
                    if type(self.vars[instancename].functions[propertyname].body) == str:
                        if 'return' in self.vars[instancename].functions[propertyname].body:
                            pass
                        else:
                            return None
                    self.vars[instancename].callmethod(propertyname, args, self, instancename)
                    return self.vars[instancename].returnedvalue
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
            return expr
        elif self.getfirstword(expr) in self.functions.keys():
            args = self.extractargs(expr.strip(), self.getfirstword(expr))
            if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                if type(self.functions[self.getfirstword(expr)].body) == str:
                    if 'return' in self.functions[self.getfirstword(expr)].body:
                        pass
                    else:
                        return None
                self.functions[self.getfirstword(expr.strip())].run(self, args)
                return self.returnedvalue
        else:
            raise LumaInterpreter.LumaNameError(f"undefined variable '{expr}'")


    def evaluate(self, expr: str, recursable: bool = True, evalforwhat = None):
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
                    if type(self.evaluate(terms[i])) == list:
                        res += str(self.evaluate(terms[i])) + ' + '
                    elif not isnumber(self.evaluate(terms[i])):
                        res += '"' + str(self.evaluate(terms[i])) + '" + '
                    else:
                        res += str(self.evaluate(terms[i])) + ' + '
                if type(self.evaluate(terms[i])) == list:
                        res += str(self.evaluate(terms[i]))
                elif not isnumber(self.evaluate(terms[-1])):
                    res += '"' + str(self.evaluate(terms[-1])) + '"'
                else:
                    res += str(self.evaluate(terms[-1]))
                return self.evaluate(res, False)
            else:
                for term in terms:
                    res += str(self.evaluate(term))
                return res
        elif expr[0] == '&' and expr[1:] in self.vars.keys():
            return type(self.vars[expr[1:]]).__name__
        elif self.getfirstword(expr) in self.classes.keys():
            args = self.extractargs(expr.strip(), self.getfirstword(expr))
            if len(args) == len(self.classes[self.getfirstword(expr.strip())].functions['constructor'].args):
                instance = self.classes[self.getfirstword(expr.strip())].instance(args, self, evalforwhat)
                return instance
        elif expr.count('.') == 1:
            dexpr = self.getfirstword(expr)
            self.vars: dict[str, LumaInterpreter.LumaClass]
            instancename = dexpr.split('.')[0]
            propertyname = dexpr.split('.')[1]
            scopes: list[dict] = reverse_list(self.localparams)
            for scope in scopes:
                if 'this' in scope.keys():
                    return scope['this'].vars[propertyname]
            if self.getfirstword(expr).split('.')[0] in self.vars.keys():
                if propertyname in self.vars[instancename].vars.keys():
                    return self.vars[instancename].vars[propertyname]
                elif propertyname in self.vars[instancename].functions.keys():
                    args = self.extractargs(expr.strip(), propertyname)
                    if len(args) == len(self.vars[instancename].functions[propertyname].args):
                        if type(self.vars[instancename].functions[propertyname].body) == str:
                            if 'return' in self.vars[instancename].functions[propertyname].body:
                                pass
                            else:
                                self.returnedvalue = None
                        self.vars[instancename].callmethod(propertyname, args, self, instancename)
                        return self.vars[instancename].returnedvalue
            else:
                raise LumaInterpreter.LumaNameError(f"undefined variable '{instancename}'")
        elif expr.startswith('"') and expr.endswith('"') and not '"' in expr[1:-1]:
            return expr[1:-1]
        elif self.getfirstword(expr) in self.functions.keys():
            args = self.extractargs(expr.strip(), self.getfirstword(expr))
            if len(args) == len(self.functions[self.getfirstword(expr.strip())].args):
                if type(self.functions[self.getfirstword(expr)].body) == str:
                    if 'return' in self.functions[self.getfirstword(expr)].body:
                        pass
                    else:
                        self.returnedvalue = None
                self.functions[self.getfirstword(expr.strip())].run(self, args)
                return self.returnedvalue
        else:
            raise LumaInterpreter.LumaNameError(f"undefined variable '{expr}'")

    class LumaFunction:
        def __init__(self, name: str, args: list[str], body: str | FunctionType):
            self.name = name
            self.args = args
            self.body = body


        def run(self, interpreter, args: list, Object = None):
            argdict = {}
            interpreter: LumaInterpreter
            Object: LumaInterpreter.LumaClass | None
            for i in range(len(args)):
                argdict[self.args[i]] = args[i]
            if Object:
                argdict['this'] = interpreter.vars[Object]
            interpreter.localparams.append(argdict)
            orig_func = set(interpreter.functions.keys())
            orig_vars = set(interpreter.vars.keys())
            if type(self.body) == str:
                interpreter.runsubprogram(self.body, None, Object)
            else:
                if Object:
                    Object.returnedvalue = self.body(*args)
                else:
                    interpreter.returnedvalue = self.body(*args)
            added_keys = set(interpreter.functions.keys()) - orig_func
            for key in added_keys:
                interpreter.functions.pop(key, None)
            added_keys = set(interpreter.vars.keys()) - orig_vars
            for key in added_keys:
                interpreter.vars.pop(key, None)
            interpreter.localparams.pop()

    
    class LumaClass:
        def __init__(self, name):
            self.name = name
            self.functions: dict[str, LumaInterpreter.LumaFunction] = {}
            self.vars: dict[str] = {}
            self.returnedvalue = None


        def instance(self, args: list, interpreter, name):
            interpreter: LumaInterpreter
            instance = copy.deepcopy(self)
            interpreter.vars[name] = instance
            instance.callmethod('constructor', args, interpreter, name)
            return instance


        def callmethod(self, method, args: list, interpreter, instancename):
            interpreter: LumaInterpreter
            method: LumaInterpreter.LumaFunction = self.functions[method]
            method.run(interpreter, args, instancename)
            

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
