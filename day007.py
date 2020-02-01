#!/usr/bin/env python
from __future__ import print_function
from computer import Context, Processor
from itertools import permutations


class AMP(object):
  def __init__(self, code, stages=5):
    self.code = code
    self.stages = stages

  def run(self, args, initial_value=0):
    if isinstance(args, basestring):
      args = Context.deserialise(args)
    assert len(args) == self.stages
    assert all(isinstance(x, int) for x in args)
    ctxs = {}
    for i in range(self.stages):
      ctxs[i] = Context(code=self.code, input=[args[i]])
    next_input = initial_value
    complete = False
    while not complete:
      for i in range(self.stages):
        ctx = ctxs[i]
        ctx.input.append(next_input)
        Processor.run(ctx)
        assert len(ctx.output) == 1
        next_input = ctx.output.pop(0)
        if ctx.complete:
          complete = True
    return next_input


def read_file(filename):
  with open(filename, 'r') as file:
    for line in file:
      line = line.rstrip()
      if not line or line[0] == '#':
        continue
      yield line


def part1_main(filename='day007_input.txt'):
  code = read_file(filename).next()
  amp = AMP(code)
  phase_settings = [0, 1, 2, 3, 4]
  results = {}
  for permutation in permutations(phase_settings):
    results[tuple(permutation)] = amp.run(permutation)
  highest = max(results.items(), key=lambda (k, v): v)
  print('Highest value {0} from {1!r}'.format(highest[1], highest[0]))
  print('Day7, Part1 answer: {}'.format(highest[1]))


def part2_main(filename='day007_input.txt'):
  code = read_file(filename).next()
  amp = AMP(code)
  phase_settings = [5, 6, 7, 8, 9]
  results = {}
  for permutation in permutations(phase_settings):
    results[tuple(permutation)] = amp.run(permutation)
  highest = max(results.items(), key=lambda (k, v): v)
  print('Highest value {0} from {1!r}'.format(highest[1], highest[0]))
  print('Day7, Part2 answer: {}'.format(highest[1]))


if __name__ == '__main__':
  part1_main()
  part2_main()
