import pytest

from computer import Context, Processor, States, run_code, run_with_io, run_with_just_io


def test_context_load_dump():
  ctx = Context()
  ctx.load('1,9,10,3,2,3,11,0,99,30,40,50')
  assert ctx.code == [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
  assert ctx.dump() == '1,9,10,3,2,3,11,0,99,30,40,50'


def test_opcode_parse():
  assert Processor.parse_opcode(2) == (2, [0, 0, 0])
  assert Processor.parse_opcode(102) == (2, [1, 0, 0])
  assert Processor.parse_opcode(1002) == (2, [0, 1, 0])
  assert Processor.parse_opcode(10002) == (2, [0, 0, 1])


def test_op_lookup():
  assert Processor.resolve_op(1) == (Processor.OP_1, 3)
  assert Processor.resolve_op(2) == (Processor.OP_2, 3)
  assert Processor.resolve_op(99) == (Processor.OP_99, 0)


def test_day2():
  assert run_code('1,9,10,3,2,3,11,0,99,30,40,50') == '3500,9,10,70,2,3,11,0,99,30,40,50'
  assert run_code('1,0,0,0,99') == '2,0,0,0,99'
  assert run_code('2,3,0,3,99') == '2,3,0,6,99'
  assert run_code('2,4,4,5,99,0') == '2,4,4,5,99,9801'
  assert run_code('1,1,1,4,99,5,6,0,99') == '30,1,1,4,2,5,6,0,99'


def test_day5():
  # Immediate mode
  assert run_code('1101,100,-1,4,0') == '1101,100,-1,4,99'
  assert run_code('1002,4,3,4,33') == '1002,4,3,4,99'
  # Input / Output
  assert run_with_io('3,3,1101,0,10,0,99', 20) == ('30,3,1101,20,10,0,99', ())
  assert run_with_io('104,77,99') == ('104,77,99', (77,))


def test_day5_part2():
  # Test equal param mode
  assert run_with_io('3,9,8,9,10,9,4,9,99,-1,8', 8) == ('3,9,8,9,10,9,4,9,99,1,8', (1,))
  assert run_with_io('3,9,8,9,10,9,4,9,99,-1,8', 9) == ('3,9,8,9,10,9,4,9,99,0,8', (0,))
  # Test less than param mode
  assert run_with_io('3,9,7,9,10,9,4,9,99,-1,8', 7) == ('3,9,7,9,10,9,4,9,99,1,8', (1,))
  assert run_with_io('3,9,7,9,10,9,4,9,99,-1,8', 8) == ('3,9,7,9,10,9,4,9,99,0,8', (0,))
  # Test equal immediate mode
  assert run_with_io('3,3,1108,-1,8,3,4,3,99', 8) == ('3,3,1108,1,8,3,4,3,99', (1,))
  assert run_with_io('3,3,1108,-1,8,3,4,3,99', 7) == ('3,3,1108,0,8,3,4,3,99', (0,))
  # Test less than immediate mode
  assert run_with_io('3,3,1107,-1,8,3,4,3,99', 7) == ('3,3,1107,1,8,3,4,3,99', (1,))
  assert run_with_io('3,3,1107,-1,8,3,4,3,99', 8) == ('3,3,1107,0,8,3,4,3,99', (0,))
  # Test jumps with param mode
  jump_test = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
  assert run_with_just_io(jump_test, 0) == (0,)
  assert run_with_just_io(jump_test, 1) == (1,)
  assert run_with_just_io(jump_test, -1) == (1,)
  # Test jumps with immediate mode.
  jump_test = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
  assert run_with_just_io(jump_test, 0) == (0,)
  assert run_with_just_io(jump_test, 1) == (1,)
  assert run_with_just_io(jump_test, -1) == (1,)
  # Bigger test
  big_test = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,' \
      '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,' \
      '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
  assert run_with_just_io(big_test, 7) == (999,)
  assert run_with_just_io(big_test, 8) == (1000,)
  assert run_with_just_io(big_test, 9) == (1001,)
