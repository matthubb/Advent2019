#!/usr/bin/env python
from __future__ import print_function
from computer import run_with_just_io


def read_file(filename):
  with open(filename, 'r') as file:
    for line in file:
      line = line.rstrip()
      if not line or line[0] == '#':
        continue
      yield line


def part1_main(filename='day005_input.txt'):
  code = read_file(filename).next()
  outputs = run_with_just_io(code, 1)
  print('Result: {}'.format(','.join(str(x) for x in outputs)))
  print('Day5, Part1 answer: {:d}'.format(outputs[-1]))


def part2_main(filename='day005_input.txt'):
  code = read_file(filename).next()
  outputs = run_with_just_io(code, 5)
  print('Result: {}'.format(','.join(str(x) for x in outputs)))
  print('Day5, Part2 answer: {:d}'.format(outputs[-1]))


if __name__ == '__main__':
  part1_main()
  part2_main()
