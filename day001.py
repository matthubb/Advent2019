#!/usr/bin/env python


def fuel_calc(mass):
  """
  >>> fuel_calc(2)
  0
  >>> fuel_calc(12)
  2
  >>> fuel_calc(14)
  2
  >>> fuel_calc(1969)
  654
  >>> fuel_calc(100756)
  33583
  """
  return max((mass / 3) - 2, 0)


def fuel_cost(mass):
  """
  >>> fuel_cost(12)
  2
  >>> fuel_cost(14)
  2
  >>> fuel_cost(1969)
  966
  >>> fuel_cost(100756)
  50346
  """
  total_cost = 0
  mass_to_fund = mass
  while True:
    cost = max((mass_to_fund / 3) - 2, 0)
    if cost == 0:
      break
    total_cost += cost
    mass_to_fund = cost
  return total_cost


def process(filename='day001-input.txt'):
  masses = []
  with open(filename, 'r') as file:
    for line in file:
      line = line.strip()
      if not line or line[0] == '#':
        continue
      masses.append(int(line))
  return sum(fuel_cost(mass) for mass in masses)


if __name__ == '__main__':
  import doctest
  doctest.testmod()
  result = process()
  print result
