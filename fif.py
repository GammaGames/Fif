import inspect
import math
import grapheme
import click

# pop() -> stack
# pop(0) -> queue

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


class Fif():
    def __init__(self, debug=False):
        self.debug = debug
        self.program = None
        self.stack = []
        self.labels = {}
        self.parse = {
            6: self._p_lbl,
            "p_lbl": self.__p_lbl
        }
        self.commands = {
            1: self._putc,
            2: self._putn,
            4: self._getn,
            5: self._gets,
            6: self._lbl,
            "lbl": self.__lbl,
            7: self._jmp,
            "jmp": self.__jmp,
            11: self._add,
            12: self._sub,
            13: self._mul,
            14: self._div,
            15: self._mod,
            16: self._psh,
            "psh": self.__psh,
            17: self._dup,
            18: self._swp,
            19: self._pop
        }

    def _print_debug(self, length, message=None, include_stack=False):
        if self.debug:
            if message is None:
                caller = inspect.stack()[1].function
                if caller.startswith("_"):
                    message = caller[1:]

            if include_stack:
                print(f"{str(length).ljust(3)}{str(message).ljust(6)} - [{', '.join(str(x) for x in stack)}]")
            else:
                print(f"{str(length).ljust(3)}{str(message)}")

    def _putc(self, line, length, index):
        print(chr(stack.pop()), end="")
        self._print_debug(length, include_stack=True)

    def _putn(self, line, length, index):
        print(stack.pop(), end="")
        self._print_debug(length, include_stack=True)

    def _getn(self, line, length, index):
        stack.append(int(input()))
        self._print_debug(length, include_stack=True)

    def _gets(self, line, length, index):
        for ch in input():
            stack.append(ord(ch))
        self._print_debug(length, include_stack=True)

    def _lbl(self, line, length, index):
        self._print_debug(length)
        return "lbl"

    def __lbl(self, line, length, index):
        self._print_debug(length)

    def _jmp(self, line, length, index):
        self._print_debug(length)
        return "jmp"

    def __jmp(self, line, length, index):
        pass
        # TODO figure out best way to return new index values
        # return labels[line]

    # jump if zero
    # jump if neg

    def _exit(self, line, length, index):
        self._print_debug(length)
        quit()

    def _add(self, line, length, index):
        stack.append(stack.pop() + stack.pop())
        self._print_debug(length, include_stack=True)

    def _sub(self, line, length, index):
        right = stack.pop()
        stack.append(stack.pop() - right)
        self._print_debug(length, include_stack=True)

    def _mul(self, line, length, index):
        stack.append(stack.pop() * stack.pop())
        self._print_debug(length, include_stack=True)

    def _div(self, line, length, index):
        right = stack.pop()
        stack.append(math.floor(stack.pop() / right))
        self._print_debug(length, include_stack=True)

    def _mod(self, line, length, index):
        right = stack.pop()
        stack.append(math.floor(stack.pop() % right))
        self._print_debug(length, include_stack=True)

    def _psh(self, line, length, index):
        self._print_debug(length)
        return "psh"

    def __psh(self, line, length, index):
        stack.append(length)
        self._print_debug(length, "", True)

    def _dup(self, line, length, index):
        stack.append(stack[-1])
        self._print_debug(length, include_stack=True)

    def _swp(self, line, length, index):
        first = stack.pop()
        second = stack.pop()
        stack.append(first)
        stack.append(second)
        self._print_debug(length, include_stack=True)

    def _pop(self, line, length, index):
        stack.pop()
        self._print_debug(length, include_stack=True)

    def _p_lbl(self, line, length, index):
        return "p_lbl"

    def __p_lbl(self, line, length, index):
        labels[line] = index

    def preprocess(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index]
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in self.parse and command is None:
                command = self.parse[command_length](line, length, index)
            elif command in self.parse:
                command = self.parse[command](line, length, index)

    def process(self):
        command = None
        for index in range(len(self.program)):
            line = self.program[index]
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
@click.option("--debug", "-d", is_flag=True)
@click.argument('filename', type=click.File("r"))
def main(debug, filename):
    fif = Fif(debug)
    fif.execute(filename.readlines())


if __name__ == "__main__":
    main()
