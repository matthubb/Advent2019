import pytest

from computer import Context, Processor, States, run_code, run_with_io


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
