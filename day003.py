#!/usr/bin/env python
from __future__ import print_function
from math import sqrt


class Coord(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    if isinstance(other, Coord):
      return self.x == other.x and self.y == other.y
    return NotImplemented

  def __ne__(self, other):
    ret = self.__eq__(other)
    if ret is not NotImplemented:
      return not ret
    return ret

  def __repr__(self):
    return 'Coord({self.x},{self.y})'.format(self=self)

  def difference(self, other):
    x = max(self.x, other.x) - min(self.x, other.x)
    y = max(self.y, other.y) - min(self.y, other.y)
    return (x, y)

  def manhattan_distance(self, other):
    x, y = self.difference(other)
    return x + y

  def euclidian_distance(self, other):
    x, y = self.difference(other)
    return sqrt(x * x + y * y)

  def up(self, count=1):
    return Coord(self.x, self.y + count)

  def down(self, count=1):
    return Coord(self.x, self.y - count)

  def left(self, count=1):
    return Coord(self.x - count, self.y)

  def right(self, count=1):
    return Coord(self.x + count, self.y)

  def follow_vector(self, direction, count):
    assert direction in self.directions
    coord = self
    for i in range(count):
      coord = coord.directions[direction](coord)  # These dict values are the unbound methods, have to supply self=coord
      yield coord

  def __hash__(self):
    return hash((self.x, self.y))

  directions = dict(
      U=up,
      D=down,
      L=left,
      R=right,
  )


class Path(object):
  def __init__(self, instructions=None):
    self.start = Coord(0, 0)
    self.visited = set()
    self.path = [self.start]
    if instructions is not None:
      self.follow_instructions(instructions)

  def follow_instructions(self, instructions):
    for vector in instructions.strip().split(','):
      direction, distance = self.parse_vector(vector)
      current_position = self.path[-1]
      for coord in current_position.follow_vector(direction, distance):
        self.visited.add(coord)
        self.path.append(coord)

  def distance_to_point(self, point):
    if point not in self.visited:
      raise ValueError("This path doesn't visit {0!r}".format(point))
    else:
      return self.path.index(point)

  @staticmethod
  def parse_vector(vector):
    direction = vector[0]
    distance = int(vector[1:])
    return direction, distance

  def find_distance_of_nearest_common(self, other):
    common = self.visited & other.visited
    if self.start in common:
      common.remove(self.start)
    distances = []
    for intersection in common:
      distance = self.start.manhattan_distance(intersection)
      distances.append(distance)
    if distances:
      return min(distances)
    raise ValueError('Intersection not found')

  def find_length_of_shortest_common(self, other):
    common = self.visited & other.visited
    if self.start in common:
      common.remove(self.start)
    distances = []
    for intersection in common:
      distance = self.distance_to_point(intersection) + other.distance_to_point(intersection)
      distances.append(distance)
    if distances:
      return min(distances)
    raise ValueError('Intersection not found')


def part1_find_distance(path1_instructions, path2_instructions):
  path1 = Path(path1_instructions)
  path2 = Path(path2_instructions)
  return path1.find_distance_of_nearest_common(path2)


def part2_find_length(path1_instructions, path2_instructions):
  path1 = Path(path1_instructions)
  path2 = Path(path2_instructions)
  return path1.find_length_of_shortest_common(path2)


def part1_main(filename='day003_input.txt'):
  with open(filename, 'r') as file:
    data = file.readlines()
  assert len(data) == 2
  answer = part1_find_distance(*data)
  print("Day003, Part 1 answer = {0}".format(answer))


def part2_main(filename='day003_input.txt'):
  with open(filename, 'r') as file:
    data = file.readlines()
  assert len(data) == 2
  answer = part2_find_length(*data)
  print("Day003, Part 2 answer = {0}".format(answer))


if __name__ == '__main__':
  part1_main()
  part2_main()
