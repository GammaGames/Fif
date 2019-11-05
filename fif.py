"""
### I/O (helpers to read lines)
1. Print character (ord)
2. Print number
3. Read character (chr)
4. Read line as number
5. Read line as string
### Flow (no call stack)
6. label
7. jump
8. jump if zero
9. jump if neg
10. exit
### Arithmetic (everything is int)
11. add
12. sub
13. mul
14. div
15. mod
### Container (Can have 2, Stack or Queue)
16. push
17. dup
18. swap top 2
20. pop
21. Change to container 1
22. Change to container 2
22. Change to stack
23. Change to queue
24. Copy from primary to secondary
25. Move from primary to secondary
"""

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


def _print_debug(length, message, include_stack=False):
    if include_stack:
        print(f"{str(length).ljust(3)}{str(message).ljust(6)} - [{', '.join(str(x) for x in stack)}]")
    else:
        print(f"{str(length).ljust(3)}{str(message)}")


def _putc(value):
    print(ord(stack.pop()))
    if debug:
        _print_debug(value, "putc", True)


def _putn(value):
    print(stack.pop())
    if debug:
        _print_debug(value, "putn", True)


# Read character (chr)
# Read line as number
# Read line as string
# label
# jump
# jump if zero
# jump if neg


def _exit(value):
    if debug:
        _print_debug(value, "exit")
    quit()


def _add(value):
    stack.append(stack.pop() + stack.pop())
    if debug:
        _print_debug(value, "add", True)


def _sub(value):
    right = stack.pop()
    stack.append(stack.pop() - right)
    if debug:
        _print_debug(value, "sub", True)


def _mul(value):
    stack.append(stack.pop() * stack.pop())
    if debug:
        _print_debug(value, "mul", True)


def _div(value):
    right = stack.pop()
    stack.append(math.floor(stack.pop() / right))
    if debug:
        _print_debug(value, "div", True)


def _mod(value):
    right = stack.pop()
    stack.append(math.floor(stack.pop() % right))
    if debug:
        _print_debug(value, "mod", True)


def _push(value):
    if debug:
        _print_debug(value, "push")
    return "push"


def __push(value):
    stack.append(value)
    if debug:
        _print_debug(value, "", True)


def _dup(value):
    stack.append(stack[-1])
    if debug:
        _print_debug(value, "dup", True)


def _swp(value):
    first = stack.pop()
    second = stack.pop()
    stack.append(first)
    stack.append(second)
    if debug:
        _print_debug(value, "swp", True)


# pop


commands = {
    1: _putc,
    2: _putn,
    11: _add,
    12: _sub,
    13: _mul,
    14: _div,
    15: _mod,
    16: _push,
    "push": __push,
    17: _dup,
    18: _swp
}


with open(args[-1], encoding="utf8") as f:
    command = None
    for line in f:
        length = grapheme.length(line.rstrip("\n"))
        if length in commands and command is None:
            command = commands[length](length)
        elif command in commands:
            command = commands[command](length)
