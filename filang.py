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

import sys

# pop() -> stack
# pop(0) -> queue

primary = {
    "type": "stack",
    "contents": []
}
secondary = {
    "type": "queue",
    "contents": []
}


def add_to_container():
    pass


def remove_from_container():
    pass


def swap_to_one():
    pass


def swap_to_two():
    pass


stack = []


debug = not set(sys.argv).isdisjoint(["-d", "--debug"])


with open("tests/1.md") as f:
    command = None
    for line in f:
        stack_changing = False
        if debug:
            debug_string = "#"
        length = len(line.rstrip("\n"))
        if command is None:
            if length == 1:
                stack_changing = True
                debug_string = "putc"
                print(ord(stack.pop()))
            elif length == 2:
                stack_changing = True
                debug_string = "putn"
                print(stack.pop())
            elif length == 11:
                stack_changing = True
                debug_string = "add"
                stack.append(stack.pop() + stack.pop())
            elif length == 12:
                stack_changing = True
                debug_string = "sub"
                stack.append(stack.pop() - stack.pop())
            elif length == 16:
                debug_string = "push"
                command = "push"
            elif length == 17:
                stack_changing = True
                debug_string = "dup"
                stack.append(stack[-1])
            elif length == 20:
                stack_changing = True
                debug_string = "pop"
                stack.pop()
        else:
            if command == "push":
                stack_changing = True
                if debug:
                    debug_string = str(length)
                stack.append(length)
            command = None

        if debug:
            if stack_changing:
                print(f"{debug_string.ljust(6)} - {', '.join(str(x) for x in stack)}")
            else:
                print(debug_string)
