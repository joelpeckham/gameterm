import sys
import tb as traceback
import javascript
from browser import document as doc
from browser import window, alert, console

_credits = """Credits"""
_copyright = """Copyright Notice"""
_license = """License Notice"""

jterm = javascript.this().term
CODE_ELT = doc['code']
OUT_BUFFER = ''

def credits():
    print(_credits)
credits.__repr__ = lambda:_credits

def copyright():
    print(_copyright)
copyright.__repr__ = lambda:_copyright

def license():
    print(_license)
license.__repr__ = lambda:_license

class Trace:

    def __init__(self):
        self.buf = ""

    def write(self, data):
        self.buf += str(data)

    def format(self):
        """Remove calls to function in this script from the traceback."""
        lines = self.buf.split("\n")
        stripped = [lines[0]]
        for i in range(1, len(lines), 2):
            if __file__ in lines[i]:
                continue
            stripped += lines[i: i+2]
        return "\n".join(stripped)

def print_tb():
    trace = Trace()
    traceback.print_exc(file=trace)
    formatted = trace.format()
    CODE_ELT.value += formatted
    writeTerm(formatted)

def syntax_error(args):
    info, filename, lineno, offset, line = args
    print(f"  File {filename}, line {lineno}")
    print("    " + line)
    print("    " + offset * " " + "^")
    print("SyntaxError:", info)
    flush()

def write(data):
    global OUT_BUFFER
    OUT_BUFFER += str(data)

def flush():
    global CODE_ELT, OUT_BUFFER
    CODE_ELT.value += OUT_BUFFER
    writeTerm(OUT_BUFFER)
    OUT_BUFFER = ''

def writeTerm(text):
    for char in text:
        if char == '\n' or char == '\r':
            jterm.writeln('')
        else:
            jterm.write(char)


sys.stdout.write = sys.stderr.write = write
sys.stdout.__len__ = sys.stderr.__len__ = lambda: len(OUT_BUFFER)

history = []
current = 0
_status = "main"  # or "block" if typing inside a block

# execution namespace
editor_ns = {'credits':credits,
    'copyright':copyright,
    'license':license,
    '__name__':'__main__'}

def cursorToEnd(*args):
    pos = len(CODE_ELT.value)
    jterm._core.buffer.x = len(javascript.this().getTermLine()) #move cursor to end
    CODE_ELT.setSelectionRange(pos, pos)
    CODE_ELT.scrollTop = CODE_ELT.scrollHeight


def get_col(area):
    # returns the column num of cursor
    sel = CODE_ELT.selectionStart
    lines = CODE_ELT.value.split('\n')
    for line in lines[:-1]:
        sel -= len(line) + 1
    return sel

def myKeyPress(event):
    #javascript.this().console.log("myKeyPress()", event, event.keyCode)
    global _status, current

    if event.keyCode == 9:  # tab key
        event.preventDefault()
        CODE_ELT.value += "    "
        writeTerm("    ")
    elif event.keyCode == 13:  # return
        src = CODE_ELT.value
        if _status == "main":
            currentLine = src[src.rfind('>>>') + 4:]
        elif _status == "3string":
            currentLine = src[src.rfind('>>>') + 4:]
            currentLine = currentLine.replace('\n... ', '\n')
        else:
            currentLine = src[src.rfind('...') + 4:]
        if _status == 'main' and not currentLine.strip():
            CODE_ELT.value += '\n>>> '
            writeTerm('\n>>> ')
            event.preventDefault()
            return
        CODE_ELT.value += '\n'
        writeTerm('\n')
        history.append(currentLine)
        current = len(history)
        if _status == "main" or _status == "3string":
            try:
                _ = editor_ns['_'] = eval(currentLine, editor_ns)
                flush()
                if _ is not None:
                    write(repr(_)+'\n')
                flush()
                CODE_ELT.value += '>>> '
                writeTerm('>>> ')
                _status = "main"
            except IndentationError:
                CODE_ELT.value += '... '
                writeTerm('... ')
                _status = "block"
            except SyntaxError as msg:
                if str(msg) == 'invalid syntax : triple string end not found' or \
                    str(msg).startswith('Unbalanced bracket'):
                    CODE_ELT.value += '... '
                    writeTerm('... ')
                    _status = "3string"
                elif str(msg) == 'eval() argument must be an expression':
                    try:
                        exec(currentLine, editor_ns)
                    except:
                        print_tb()
                    flush()
                    CODE_ELT.value += '>>> '
                    writeTerm('>>> ')
                    _status = "main"
                elif str(msg) == 'decorator expects function':
                    CODE_ELT.value += '... '
                    writeTerm('... ')
                    _status = "block"
                else:
                    syntax_error(msg.args)
                    CODE_ELT.value += '>>> '
                    writeTerm('>>> ')
                    _status = "main"
            except:
                # the full traceback includes the call to eval(); to
                # remove it, it is stored in a buffer and the 2nd and 3rd
                # lines are removed
                print_tb()
                CODE_ELT.value += '>>> '
                writeTerm('>>> ')
                _status = "main"
        elif currentLine == "":  # end of block
            block = src[src.rfind('>>>') + 4:].splitlines()
            block = [block[0]] + [b[4:] for b in block[1:]]
            block_src = '\n'.join(block)
            # status must be set before executing code in globals()
            _status = "main"
            try:
                _ = exec(block_src, editor_ns)
                if _ is not None:
                    print(repr(_))
            except:
                print_tb()
            flush()
            CODE_ELT.value += '>>> '
            writeTerm('>>> ')
        else:
            CODE_ELT.value += '... '
            writeTerm('... ')

        cursorToEnd()
        event.preventDefault()
    elif chr(event.keyCode).isprintable() and event.keyCode not in [37,38,39,40]:
        event.preventDefault()
        CODE_ELT.value += event.key
        writeTerm(event.key)

def myKeyDown(event):
    javascript.this().console.log("myKeyDown()", event)
    global _status, current
    if event.keyCode == 37:  # left arrow
        sel = get_col(CODE_ELT)
        if sel < 5:
            event.preventDefault()
            event.stopPropagation()
    elif event.keyCode == 36:  # line start
        pos = CODE_ELT.selectionStart
        col = get_col(CODE_ELT)
        CODE_ELT.setSelectionRange(pos - col + 4, pos - col + 4)
        event.preventDefault()
    elif event.keyCode == 38:  # up
        if current > 0:
            pos = CODE_ELT.selectionStart
            col = get_col(CODE_ELT)
            # remove current line
            CODE_ELT.value = CODE_ELT.value[:pos - col + 4]
            current -= 1
            CODE_ELT.value += history[current]
        event.preventDefault()
    elif event.keyCode == 40:  # down
        if current < len(history) - 1:
            pos = CODE_ELT.selectionStart
            col = get_col(CODE_ELT)
            # remove current line
            CODE_ELT.value = CODE_ELT.value[:pos - col + 4]
            current += 1
            CODE_ELT.value += history[current]
        event.preventDefault()
    elif event.keyCode == 8:  # backspace
        src = CODE_ELT.value
        lstart = src.rfind('\n')
        if (lstart == -1 and len(src) < 5) or (len(src) - lstart < 6):
            event.preventDefault()
            event.stopPropagation()

        currentLine = javascript.this().getTermLine()
        javascript.this().console.log(currentLine)
        if (currentLine[:4] == '>>> ' or currentLine[:4] == '... ') \
        and jterm._core.buffer.x > 4:
            jterm.write('\b \b')
            CODE_ELT.value = CODE_ELT.value[:-1]

    elif event.ctrlKey and event.keyCode == 65: # ctrl+a
        src = CODE_ELT.value
        pos = CODE_ELT.selectionStart
        col = get_col(CODE_ELT)
        CODE_ELT.setSelectionRange(pos - col + 4, len(src))
        event.preventDefault()
    elif event.keyCode in [33, 34]: # page up, page down
        event.preventDefault()

CODE_ELT.bind('keypress', myKeyPress)
CODE_ELT.bind('keydown', myKeyDown)
CODE_ELT.bind('click', cursorToEnd)
v = sys.implementation.version
CODE_ELT.value = ">>> "
cursorToEnd()
writeTerm(">>> ")
