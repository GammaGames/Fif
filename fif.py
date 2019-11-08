import inspect
import math
import sys
import grapheme

# pop() -> stack
# pop(0) -> queue

debug_args = ["-d", "--debug"]
debug = not set(sys.argv).isdisjoint(debug_args)
args = [arg for arg in sys.argv if arg not in debug_args][1:]
stack = []


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
                message = caller.lstrip("_")

        if include_stack:
            print(f"{str(length).ljust(3)}{str(message).ljust(6)} - [{', '.join(str(x) for x in stack)}]")
        else:
            print(f"{str(length).ljust(3)}{str(message)}")


def _putc(value):
    print(chr(stack.pop()), end="")
    _print_debug(value, include_stack=True)


def _putn(value):
    print(stack.pop(), end="")
    _print_debug(value, include_stack=True)


def _getn(value):
    stack.append(int(input()))
    _print_debug(value, include_stack=True)


def _gets(value):
    for ch in input():
        stack.append(ord(ch))
    _print_debug(value, include_stack=True)


# label
# jump
# jump if zero
# jump if neg


def _exit(value):
    _print_debug(value)
    quit()


def _add(value):
    stack.append(stack.pop() + stack.pop())
    _print_debug(value, include_stack=True)


def _sub(value):
    right = stack.pop()
    stack.append(stack.pop() - right)
    _print_debug(value, include_stack=True)


def _mul(value):
    stack.append(stack.pop() * stack.pop())
    _print_debug(value, include_stack=True)


def _div(value):
    right = stack.pop()
    stack.append(math.floor(stack.pop() / right))
    _print_debug(value, include_stack=True)


def _mod(value):
    right = stack.pop()
    stack.append(math.floor(stack.pop() % right))
    _print_debug(value, include_stack=True)


def _push(value):
    _print_debug(value)
    return "push"


def __push(value):
    stack.append(value)
    _print_debug(value, "", True)


def _dup(value):
    stack.append(stack[-1])
    _print_debug(value, include_stack=True)


def _swp(value):
    first = stack.pop()
    second = stack.pop()
    stack.append(first)
    stack.append(second)
    _print_debug(value, include_stack=True)


def _pop(value):
    stack.pop()
    _print_debug(value, include_stack=True)


commands = {
    1: _putc,
    2: _putn,
    4: _getn,
    5: _gets,
    11: _add,
    12: _sub,
    13: _mul,
    14: _div,
    15: _mod,
    16: _push,
    "push": __push,
    17: _dup,
    18: _swp,
    19: _pop
}


with open(args[-1], encoding="utf8") as f:
    command = None
    for line in f:
        length = grapheme.length(line.rstrip("\n"))
        if length in commands and command is None:
            command = commands[length](length)
        elif command in commands:
            command = commands[command](length)
