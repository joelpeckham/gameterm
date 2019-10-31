import sys
import tb as traceback
import javascript
from browser import document as doc
from browser import window, alert, console

# The Credits, Copyright, and License information have been temporarily
# removed to make this file more readible. In the mean time this information
# can be found at https://brython.info/tests/console.py.
_credits = """Credits"""
_copyright = """Copyright Notice"""
_license = """License Notice"""

clog = javascript.this().console.log
jterm = javascript.this().term
getTermLine = javascript.this().getTermLine
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
    global OUT_BUFFER
    writeTerm(OUT_BUFFER)
    OUT_BUFFER = ''

def writeTerm(text):
    #clog(f"Printing `{text}`")
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
    jterm._core.buffer.y = javascript.this().getLastTermLineNum()
    jterm._core.buffer.x = len(getTermLine()) #move cursor to end


def get_col(area):
    return jterm._core.buffer.x

def pressedTab(event):
    event.preventDefault()
    writeTerm("    ")

def pressedEnter(event):
    global _status
    src = CODE_ELT.value
    if _status == "main":
        currentLine = getTermLine().rstrip()[4:]
    elif _status == "3string":
        currentLine = getTermLine().rstrip()[4:]
        currentLine = currentLine.replace('\n... ', '\n')
    else:
        currentLine = getTermLine().rstrip()[4:]
    #clog(f"Current line: '{currentLine}'")
    if _status == 'main' and not currentLine.strip():
        writeTerm('\n>>> ')
        event.preventDefault()
        return
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
            writeTerm('>>> ')
            _status = "main"
        except IndentationError:
            writeTerm('... ')
            _status = "block"
        except SyntaxError as msg:
            if str(msg) == 'invalid syntax : triple string end not found' or \
                str(msg).startswith('Unbalanced bracket'):
                writeTerm('... ')
                _status = "3string"
            elif str(msg) == 'eval() argument must be an expression':
                try:
                    exec(currentLine, editor_ns)
                except:
                    print_tb()
                flush()
                writeTerm('>>> ')
                _status = "main"
            elif str(msg) == 'decorator expects function':
                writeTerm('... ')
                _status = "block"
            else:
                syntax_error(msg.args)
                writeTerm('>>> ')
                _status = "main"
        except:
            # the full traceback includes the call to eval(); to
            # remove it, it is stored in a buffer and the 2nd and 3rd
            # lines are removed
            print_tb()
            writeTerm('>>> ')
            _status = "main"
    elif currentLine == "":  # end of block

        #This is really bad. Needs to be fixed to avoid constructing entire history of terminal every time.
        src = '\n'.join([jterm.buffer.getLine(line).translateToString(True).rstrip() for line in range(0,javascript.this().getLastTermLineNum())])
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
        writeTerm('>>> ')
    else:
        writeTerm('... ')
    cursorToEnd()
    event.preventDefault()

def pressedArrowLeft(event):
    currentLine = jterm.buffer.getLine(jterm.buffer.cursorY)
    lineText = currentLine.translateToString(True).rstrip()
    if (lineText[:4] != '>>> ' and lineText[:4] != '... ') or jterm._core.buffer.x > 4:
        if jterm._core.buffer.x == 0 and currentLine.isWrapped == True:
            clog(jterm._core.buffer.x,jterm._core.buffer.y)
            jterm._core.buffer.y -= 1 if jterm._core.buffer.y >= 1 else 0
            jterm._core.buffer.x = len(jterm.buffer.getLine(jterm._core.buffer.y).translateToString())
            jterm.write("[C")
        else:
            clog('write left arrow')
            jterm.write("[D")

def pressedArrowRight(event):
    currentLine = jterm.buffer.getLine(jterm.buffer.cursorY).translateToString(True).rstrip()
    if jterm._core.buffer.x <= len(currentLine) - 1:
        jterm.write("[C")

def pressedArrowUp(event):
    pass
    # currentLine = getTermLine()
    # global current
    # if current > 0:
    #     pos = CODE_ELT.selectionStart
    #     col = get_col(CODE_ELT)
    #     # remove current line
    #     CODE_ELT.value = CODE_ELT.value[:pos - col + 4]
    #     current -= 1
    #     CODE_ELT.value += history[current]
    #     prompt = currentLine[:4]
    #     jterm.write("\x1b[2K\r" + prompt + history[current])
    #     event.preventDefault()

def pressedArrowDown(event):
    pass
    # currentLine = getTermLine()
    # global current
    # if current < len(history) - 1:
    #     pos = CODE_ELT.selectionStart
    #     col = get_col(CODE_ELT)
    #     # remove current line
    #     CODE_ELT.value = CODE_ELT.value[:pos - col + 4]
    #     current += 1
    #     CODE_ELT.value += history[current]
    #     prompt = currentLine[:4]
    #     jterm.write("\x1b[2K\r" + prompt + history[current])
    # elif current == len(history) - 1:
    #     pos = CODE_ELT.selectionStart
    #     col = get_col(CODE_ELT)
    #     CODE_ELT.value = CODE_ELT.value[:pos - col + 4]
    #     prompt = currentLine[:4]
    #     jterm.write("\x1b[2K\r" + prompt)
    # event.preventDefault()

def pressedBackspace(event):
    currentLine = getTermLine()
    src = CODE_ELT.value
    lstart = src.rfind('\n')
    if (lstart == -1 and len(src) < 5) or (len(src) - lstart < 6):
        event.preventDefault()
        event.stopPropagation()

    if (currentLine[:4] == '>>> ' or currentLine[:4] == '... ') \
    and jterm._core.buffer.x > 4:
        jterm.write('\b \b')
        CODE_ELT.value = CODE_ELT.value[:-1]

def pressedCtrlKeyC(event):
    javascript.this().location.reload()

def termKeyDown(event):
    # clog("Pressed Key: " + event.key)
    if "pressed" + event.code in globals():
        globals()["pressed" + event.code](event)
    elif event.ctrlKey:
        if "pressedCtrl" + event.code in globals():
            globals()["pressedCtrl" + event.code](event)
    elif chr(event.keyCode).isprintable():
        event.preventDefault()
        CODE_ELT.value += event.key
        writeTerm(event.key)

doc["keyTrigger"].bind('keypress', termKeyDown)
CODE_ELT.value = ">>> "
cursorToEnd()
writeTerm(">>> ")
