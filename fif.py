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
        self.labels = {}
        self.stack_key = 0
        self.stacks = {
            self.stack_key: []
        }
        self.parse = {
            6: self._parse_labl,
            "set_labl": self._set_labl
        }
        self.commands = {
            1: self._putc,
            2: self._putn,
            4: self._getn,
            5: self._gets,
            6: self._labl,
            "labl": self.__labl,
            7: self._jump,
            8: self._jz,
            9: self._jn,
            10: self._exit,
            "do_jump": self._do_jump,
            11: self._add,
            12: self._sub,
            13: self._mul,
            14: self._div,
            15: self._mod,
            16: self._push,
            "push": self.__push,
            17: self._dup,
            18: self._swap,
            19: self._pop,
            "noop": self._noop
        }

    def _print_debug(self, length, message=None, include_stack=False):
        if self.debug:
            if message is None:
                caller = inspect.stack()[1].function
                if caller.startswith("_"):
                    message = caller[1:]

            line_number = f"line {str(self.index + 1).rjust(len(str(len(self.program))))}"
            text = f"{line_number}: {str(length).ljust(3)}{str(message).ljust(6)}"
            if include_stack:
                print(f"{text} - [{', '.join(str(x) for x in self.stacks[self.stack_key])}]")
            else:
                print(text)

    def _putc(self, line, length, index):
        popped = chr(self.stacks[self.stack_key].pop())
        if not self.debug:
            print(popped, end="")
        self._print_debug(length, message=f"putc {popped}", include_stack=True)

    def _putn(self, line, length, index):
        popped = self.stacks[self.stack_key].pop()
        if not self.debug:
            print(popped, end="")
        self._print_debug(length, message=f"putn {popped}", include_stack=True)

    def _getn(self, line, length, index):
        self.stacks[self.stack_key].append(int(input()))
        self._print_debug(length, include_stack=True)

    def _gets(self, line, length, index):
        for ch in input():
            self.stacks[self.stack_key].append(ord(ch))
        self._print_debug(length, include_stack=True)

    def _labl(self, line, length, index):
        self._print_debug(length)
        return "labl"

    def __labl(self, line, length, index):
        # Essentally a noop
        pass

    def _jump(self, line, length, index):
        self._print_debug(length)
        return "do_jump"

    def _jz(self, line, length, index):
        check = self.stacks[self.stack_key][-1] == 0
        self._print_debug(length, message=f"jz {'T' if check else 'F'}", include_stack=True)
        return "do_jump" if check else "noop"

    def _jn(self, line, length, index):
        check = self.stacks[self.stack_key][-1] < 0
        self._print_debug(length, message=f"jn {'T' if check else 'F'}", include_stack=True)
        return "do_jump" if check else "noop"

    def _do_jump(self, line, length, index):
        self.index = self.labels[line]
        self._print_debug(self.index, "jump")

    def _exit(self, line, length, index):
        self._print_debug(length, "exit")
        quit()

    def _add(self, line, length, index):
        self.stacks[self.stack_key].append(self.stacks[self.stack_key].pop() + self.stacks[self.stack_key].pop())
        self._print_debug(length, include_stack=True)

    def _sub(self, line, length, index):
        right = self.stacks[self.stack_key].pop()
        self.stacks[self.stack_key].append(self.stacks[self.stack_key].pop() - right)
        self._print_debug(length, include_stack=True)

    def _mul(self, line, length, index):
        self.stacks[self.stack_key].append(self.stacks[self.stack_key].pop() * self.stacks[self.stack_key].pop())
        self._print_debug(length, include_stack=True)

    def _div(self, line, length, index):
        right = self.stacks[self.stack_key].pop()
        self.stacks[self.stack_key].append(math.floor(self.stacks[self.stack_key].pop() / right))
        self._print_debug(length, include_stack=True)

    def _mod(self, line, length, index):
        right = self.stacks[self.stack_key].pop()
        self.stacks[self.stack_key].append(math.floor(self.stacks[self.stack_key].pop() % right))
        self._print_debug(length, include_stack=True)

    def _push(self, line, length, index):
        self._print_debug(length)
        return "push"

    def __push(self, line, length, index):
        self.stacks[self.stack_key].append(length)
        self._print_debug(length, "", True)

    def _dup(self, line, length, index):
        self.stacks[self.stack_key].append(self.stacks[self.stack_key][-1])
        self._print_debug(length, include_stack=True)

    def _swap(self, line, length, index):
        first = self.stacks[self.stack_key].pop()
        second = self.stacks[self.stack_key].pop()
        self.stacks[self.stack_key].append(first)
        self.stacks[self.stack_key].append(second)
        self._print_debug(length, include_stack=True)

    def _pop(self, line, length, index):
        self.stacks[self.stack_key].pop()
        self._print_debug(length, include_stack=True)

    def _noop(self, line, length, index):
        self._print_debug(length)

    def _parse_labl(self, line, length, index):
        return "set_labl"

    def _set_labl(self, line, length, index):
        self.labels[line] = index

    def preprocess(self):
        self.labels = {}
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
        self.index = 0
        self.stack_index = 0
        self.stacks = {
            self.stack_index: []
        }
        command = None

        while self.index < len(self.program):
            line = self.program[self.index].rstrip("\n")
            length = grapheme.length(line.rstrip("\n"))
            command_length = length % 32
            if command_length in self.commands and command is None:
                command = self.commands[command_length](line, length, self.index)
            elif command in self.commands:
                command = self.commands[command](line, length, self.index)
            self.index += 1

    def execute(self, program):
        self.program = program
        self.preprocess()
        self.process()


def execute(program, debug=False):
    fif = Fif(debug)
    fif.execute(program)


@click.command()
@click.option("--debug", "-d", is_flag=True, help="Print debug information")
@click.argument('filename', type=click.File("r"))
def main(debug, filename):
    execute(filename.readlines(), debug=debug)


if __name__ == "__main__":
    main()
