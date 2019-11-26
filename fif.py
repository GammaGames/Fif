import inspect
import math
import grapheme
import click

# pop() -> stack
# pop(0) -> queue


class Fif():
    def __init__(self, debug=False):
        self.debug = debug
        self.program = None
        self.index = 0
        self.stack = []
        self.labels = {}
        self.parse = {
            6: self._p_labl,
            "p_labl": self.__p_labl
        }
        self.commands = {
            1: self._putc,
            2: self._putn,
            4: self._getn,
            5: self._gets,
            6: self._labl,
            "labl": self.__labl,
            7: self._jump,
            "jump": self.__jump,
            11: self._add,
            12: self._sub,
            13: self._mul,
            14: self._div,
            15: self._mod,
            16: self._push,
            "push": self.__push,
            17: self._dup,
            18: self._swap,
            19: self._pop
        }

    def _print_debug(self, length, message=None, include_stack=False):
        if self.debug:
            if message is None:
                caller = inspect.stack()[1].function
                if caller.startswith("_"):
                    message = caller[1:]

            if include_stack:
                print(f"{str(length).ljust(3)}{str(message).ljust(6)} - [{', '.join(str(x) for x in self.stack)}]")
            else:
                print(f"{str(length).ljust(3)}{str(message)}")

    def _putc(self, line, length, index):
        popped = chr(self.stack.pop())
        if not self.debug:
            print(popped, end="")
        self._print_debug(length, message=f"putc {popped}", include_stack=True)

    def _putn(self, line, length, index):
        popped = self.stack.pop()
        if not self.debug:
            print(popped, end="")
        self._print_debug(length, message=f"putn {popped}", include_stack=True)

    def _getn(self, line, length, index):
        self.stack.append(int(input()))
        self._print_debug(length, include_stack=True)

    def _gets(self, line, length, index):
        for ch in input():
            self.stack.append(ord(ch))
        self._print_debug(length, include_stack=True)

    def _labl(self, line, length, index):
        self._print_debug(length)
        return "lbl"

    def __labl(self, line, length, index):
        self._print_debug(length)

    def _jump(self, line, length, index):
        self._print_debug(length)
        return "jump"

    def __jump(self, line, length, index):
        self.index = self.labels[line]
        self._print_debug(self.index, "jump")

    # jump if zero
    # jump if neg

    def _exit(self, line, length, index):
        self._print_debug(length, "exit")
        quit()

    def _add(self, line, length, index):
        self.stack.append(self.stack.pop() + self.stack.pop())
        self._print_debug(length, include_stack=True)

    def _sub(self, line, length, index):
        right = self.stack.pop()
        self.stack.append(self.stack.pop() - right)
        self._print_debug(length, include_stack=True)

    def _mul(self, line, length, index):
        self.stack.append(self.stack.pop() * self.stack.pop())
        self._print_debug(length, include_stack=True)

    def _div(self, line, length, index):
        right = self.stack.pop()
        self.stack.append(math.floor(self.stack.pop() / right))
        self._print_debug(length, include_stack=True)

    def _mod(self, line, length, index):
        right = self.stack.pop()
        self.stack.append(math.floor(self.stack.pop() % right))
        self._print_debug(length, include_stack=True)

    def _push(self, line, length, index):
        self._print_debug(length)
        return "push"

    def __push(self, line, length, index):
        self.stack.append(length)
        self._print_debug(length, "", True)

    def _dup(self, line, length, index):
        self.stack.append(self.stack[-1])
        self._print_debug(length, include_stack=True)

    def _swap(self, line, length, index):
        first = self.stack.pop()
        second = self.stack.pop()
        self.stack.append(first)
        self.stack.append(second)
        self._print_debug(length, include_stack=True)

    def _pop(self, line, length, index):
        self.stack.pop()
        self._print_debug(length, include_stack=True)

    def _p_labl(self, line, length, index):
        return "p_labl"

    def __p_labl(self, line, length, index):
        self.labels[line] = index

    def preprocess(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index].rstrip("\n")
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in self.parse and command is None:
                command = self.parse[command_length](line, length, index)
            elif command in self.parse:
                command = self.parse[command](line, length, index)

    def process(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index].rstrip("\n")
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in self.commands and command is None:
                command = self.commands[command_length](line, length, index)
            elif command in self.commands:
                command = self.commands[command](line, length, index)

    def execute(self, program):
        self.program = program
        self.preprocess()
        self.process()


@click.command()
@click.option("--debug", "-d", is_flag=True, help="Print debug information")
@click.argument('filename', type=click.File("r"))
def main(debug, filename):
    fif = Fif(debug)
    fif.execute(filename.readlines())


if __name__ == "__main__":
    main()
