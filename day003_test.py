from day003 import Coord, Path, part1_find_distance, part2_find_length


def test_coord_directions():
  start = Coord(0, 0)
  assert start.up() == Coord(0, 1)
  assert start.down() == Coord(0, -1)
  assert start.left() == Coord(-1, 0)
  assert start.right() == Coord(1, 0)
  assert start.up(7) == Coord(0, 7)
  assert start.down(7) == Coord(0, -7)
  assert start.left(7) == Coord(-7, 0)
  assert start.right(7) == Coord(7, 0)


def test_parse_vector():
  assert Path.parse_vector('R90') == ('R', 90)
  assert Path.parse_vector('U2') == ('U', 2)
  assert Path.parse_vector('L100') == ('L', 100)


def test_path():
  assert Path('R3').path == [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]


def test_part1():
  assert part1_find_distance('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159
  assert part1_find_distance('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135


def test_part2():
  assert part2_find_length('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 610
  assert part2_find_length('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410
