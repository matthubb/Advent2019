from __future__ import print_function
from computer import Context, Processor
import doctest

day2_input = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,19,5,23,2,13,23,27,1,10,27,31,2,6,31,35,1,9,35,39,2,10,39,43,1,43,9,47,1,47,9,51,2,10,51,55,1,55,9,59,1,59,5,63,1,63,6,67,2,6,67,71,2,10,71,75,1,75,5,79,1,9,79,83,2,83,10,87,1,87,6,91,1,13,91,95,2,10,95,99,1,99,6,103,2,13,103,107,1,107,2,111,1,111,9,0,99,2,14,0,0'


def main(code=day2_input):
  ctx = Context()
  ctx.load(code)
  # Replace position 1 with 12
  ctx.write_location(12, 1, 0)
  # Replace position 2 with 2
  ctx.write_location(2, 2, 0)
  # Run
  Processor.run(ctx)
  print('Day2 part1 code completed in {ctx.cycles} cycles'.format(ctx=ctx))
  print('Day2 part1 answer: {0}'.format(ctx.read_location(0, 0)))


def part2_paramatized(noun=12, verb=2, code=day2_input):
  """
  >>> part2_paramatized(12, 2)
  2692315
  """
  ctx = Context()
  ctx.load(code)
  # Replace position 1 with noun
  ctx.write_location(noun, 1, 0)
  # Replace position 2 with verb
  ctx.write_location(verb, 2, 0)
  # Run
  Processor.run(ctx)
  return ctx.read_location(0, 0)


def part2_main(target=19690720):
  # Search
  for noun in range(100):
    for verb in range(100):
      answer = part2_paramatized(noun=noun, verb=verb)
      if answer == target:
        print("Target {t} achieved with noun={noun} and verb={verb}".format(
          t=target,
          noun=noun,
          verb=verb,
        ))
        print("100 * noun + verb == {0}".format(100 * noun + verb))
        break


if __name__ == '__main__':
  doctest.testmod()
  main()
  part2_main()
