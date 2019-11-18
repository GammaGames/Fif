# Fif
*/fīf/*

Fif is a stack based esoteric programming language that uses line lengths to perform operations, allowing two programs that read completely differently to execute the exact same process. The length of each line is modulo divided with 32, meaning a line of length 2 and 34 will produce the same output. Every value is stored as an integer, and characters are printed according to their unicode value.

While Fif is based on stacks, you can swap the stack type between FiFo and FiLo. You also have multiple stacks to work with, with the power to move values between.

#### FiF currently supports only a subset of planned features

## Commands:

### I/O (helpers to read lines)
- [x] Length 1: print character - printed using `ord(pop())`
- [x] Length 2: print integer
- [ ] Length 3: ?
- [x] Length 4: read line as integer
- [x] Length 5: read line as string
### Flow (no call stack)
- [ ] Length 6: label
- [ ] Length 7: jump
- [ ] Length 8: jump if zero
- [ ] Length 9: jump if neg
- [x] Length 10: exit
### Arithmetic (everything is int)
- [x] Length 11: add
- [x] Length 12: sub
- [x] Length 13: mul
- [x] Length 14: div
- [x] Length 15: mod
### Container (Can have 2, Stack or Queue)
- [x] Length 16: push
- [x] Length 17: dup
- [x] Length 18: swap top 2
- [x] Length 19: pop
- [ ] Length 20: change to stack
- [ ] Length 21: change to queue
- [ ] Length 22: change to container 1
- [ ] Length 23: change to container 2
- [ ] Length 24: copy from primary to secondary
- [ ] Length 25: move from primary to secondary

## Examples:

A simple program that adds two numbers from input and prints it could look like so:

```
read
read
add them up
output the numbers in text console
```

You can find more examples in the [tests](tests) folder.

Inspired by the great project [Enjamb](https://github.com/TartanLlama/enjamb)
