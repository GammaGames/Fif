import inspect
import math
import sys
import grapheme

# pop() -> stack
# pop(0) -> queue

DEBUG_ARGS = ["-d", "--debug"]
debug = not set(sys.argv).isdisjoint(DEBUG_ARGS)
args = [arg for arg in sys.argv if arg not in DEBUG_ARGS][1:]
stack = []
labels = {}


primary = {
    "type": "stack",
    "contents": []
}
secondary = {
    "type": "queue",
    "contents": []
}


def _print_debug(length, message=None, include_stack=False):
    if debug:
        if message is None:
            caller = inspect.stack()[1].function
            if caller.startswith("_"):
                message = caller[1:]

        if include_stack:
            print(f"{str(length).ljust(3)}{str(message).ljust(6)} - [{', '.join(str(x) for x in stack)}]")
        else:
            print(f"{str(length).ljust(3)}{str(message)}")


def _putc(line, length, index):
    print(chr(stack.pop()), end="")
    _print_debug(length, include_stack=True)


def _putn(line, length, index):
    print(stack.pop(), end="")
    _print_debug(length, include_stack=True)


def _getn(line, length, index):
    stack.append(int(input()))
    _print_debug(length, include_stack=True)


def _gets(line, length, index):
    for ch in input():
        stack.append(ord(ch))
    _print_debug(length, include_stack=True)


def _lbl(line, length, index):
    _print_debug(length)
    return "lbl"


def __lbl(line, length, index):
    _print_debug(length)


def _jmp(line, length, index):
    _print_debug(length)
    return "jmp"


def __jmp(line, length, index):
    pass
    # TODO figure out best way to return new index values
    # return labels[line]


# jump if zero
# jump if neg


def _exit(line, length, index):
    _print_debug(length)
    quit()


def _add(line, length, index):
    stack.append(stack.pop() + stack.pop())
    _print_debug(length, include_stack=True)


def _sub(line, length, index):
    right = stack.pop()
    stack.append(stack.pop() - right)
    _print_debug(length, include_stack=True)


def _mul(line, length, index):
    stack.append(stack.pop() * stack.pop())
    _print_debug(length, include_stack=True)


def _div(line, length, index):
    right = stack.pop()
    stack.append(math.floor(stack.pop() / right))
    _print_debug(length, include_stack=True)


def _mod(line, length, index):
    right = stack.pop()
    stack.append(math.floor(stack.pop() % right))
    _print_debug(length, include_stack=True)


def _psh(line, length, index):
    _print_debug(length)
    return "psh"


def __psh(line, length, index):
    stack.append(length)
    _print_debug(length, "", True)


def _dup(line, length, index):
    stack.append(stack[-1])
    _print_debug(length, include_stack=True)


def _swp(line, length, index):
    first = stack.pop()
    second = stack.pop()
    stack.append(first)
    stack.append(second)
    _print_debug(length, include_stack=True)


def _pop(line, length, index):
    stack.pop()
    _print_debug(length, include_stack=True)


def _p_lbl(line, length, index):
    return "p_lbl"


def __p_lbl(line, length, index):
    labels[line] = index


commands = {
    1: _putc,
    2: _putn,
    4: _getn,
    5: _gets,
    6: _lbl,
    "lbl": __lbl,
    7: _jmp,
    "jmp": __jmp,
    11: _add,
    12: _sub,
    13: _mul,
    14: _div,
    15: _mod,
    16: _psh,
    "psh": __psh,
    17: _dup,
    18: _swp,
    19: _pop
}


parse = {
    6: _p_lbl,
    "p_lbl": __p_lbl
}


class Fif():
    def __init__(self, debug=False):
        self.debug = debug
        self.program = None
        self.stack = []
        self.labels = {}

    def preprocess(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index]
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in parse and command is None:
                command = parse[command_length](line, length, index)
            elif command in parse:
                command = parse[command](line, length, index)

    def process(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index]
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in commands and command is None:
                command = commands[command_length](line, length, index)
            elif command in commands:
                command = commands[command](line, length, index)

    def execute(self, program):
        self.program = program
        self.preprocess()
        self.process()


def main():
    fif = Fif(debug)
    program = []

    with open(args[-1], encoding="utf8") as f:
        program = f.readlines()

    fif.execute(program)


if __name__ == '__main__':
    main()
