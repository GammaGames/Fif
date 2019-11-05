# Fif
*/fīf/*

Welcome to the repo for Fif! Fif is a stack based programming language that uses line lengths to perform operations, allowing two programs that read completely differently to act the exact same.

While Fif is based on stacks, you can swap the stack type between FiFo and FiLo. You also have multiple stacks to work with, with the power to move values between.

#### FiF currently supports only a subset of planned features

## Commands:

### I/O (helpers to read lines)
- [x] Length 1: print character - printed using `ord(pop())`
- [x] Length 2: print number
- [ ] Length 3: read character (chr)
- [ ] Length 4: read line as number
- [ ] Length 5: read line as string
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
- [ ] Length 20: pop
- [ ] Length 21: change to container 1
- [ ] Length 22: change to container 2
- [ ] Length 22: change to stack
- [ ] Length 23: change to queue
- [ ] Length 24: copy from primary to secondary
- [ ] Length 25: move from primary to secondary

Inspired by the great project [Enjamb](https://github.com/TartanLlama/enjamb)
