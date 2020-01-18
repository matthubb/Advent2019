#!/usr/bin/env python
from __future__ import print_function


def check_number(number):
  """
  >>> check_
  """
  if not 111111 <= number <= 999999:
    return False
  prev = 0
  double = False
  for digit in (int(x) for x in str(number)):
    if digit < prev:
      return False
    elif digit == prev:
      double = True
    prev = digit
  return double


def skip_numbers(number):
  prev = 0
  replace = None
  result = []
  for digit in (int(x) for x in str(number)):
    if replace is not None:
      result.append(replace)
    elif digit < prev:
      replace = str(prev)
      result.append(replace)
    else:
      prev = digit
      result.append(str(digit))
  return int("".join(result))


def part1_count_possibles(start, stop, check_number=check_number):
  possibles = 0
  value = start
  while value <= stop:
    if check_number(value):
      possibles += 1
      value += 1
    else:
      value = max(value + 1, skip_numbers(value))
  return possibles


def part2_check_number(number):
  """
  >>> check_
  """
  if not 111111 <= number <= 999999:
    return False
  prev = 0
  repeats = {}
  for digit in (int(x) for x in str(number)):
    if digit < prev:
      return False
    elif digit == prev:
      if digit in repeats:
        repeats[digit] += 1
      else:
        repeats[digit] = 2
    prev = digit
  return 2 in repeats.values()


def part1_main(arg='307237-769058'):
  lhs, _, rhs = arg.partition('-')
  answer = part1_count_possibles(int(lhs), int(rhs))
  print("Day004, Part 1 answer = {0}".format(answer))


def part2_main(arg='307237-769058'):
  lhs, _, rhs = arg.partition('-')
  answer = part1_count_possibles(int(lhs), int(rhs), check_number=part2_check_number)
  print("Day004, Part 2 answer = {0}".format(answer))


if __name__ == '__main__':
  part1_main()
  part2_main()
