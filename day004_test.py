from day004 import check_number, skip_numbers, part2_check_number


def test_check_number():
  assert check_number(122345) is True
  assert check_number(111123) is True
  assert check_number(111111) is True
  assert check_number(135679) is False
  assert check_number(223450) is False
  assert check_number(123789) is False


def test_skip_numbers():
  assert skip_numbers(122345) == 122345
  assert skip_numbers(100000) == 111111
  assert skip_numbers(100900) == 111111
  assert skip_numbers(223450) == 223455


def test_part2_check_number():
  assert part2_check_number(122345) is True
  assert part2_check_number(111123) is False
  assert part2_check_number(111111) is False
  assert part2_check_number(135679) is False
  assert part2_check_number(223450) is False
  assert part2_check_number(123789) is False
  assert part2_check_number(112233) is True
  assert part2_check_number(111122) is True
  assert part2_check_number(123444) is False
