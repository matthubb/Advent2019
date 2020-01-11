#!/usr/bin/env python

from enum import Enum

States = Enum('RUN', 'WAIT', 'HALT')


class Context(object):
  def __init__(self):
    self.instruction_pointer = 0
    self.relative_base = 0
    self.state = States.WAIT
    self.cycles = 0

  def load(self, program):
    # Receive a program into memory
    self.code = [int(x) for x in program.strip().split(',')]

  def dump(self):
    # Serialise
    code = ",".join(str(x) for x in self.code)
    return code

  def read_location(self, offset, mode):
    if mode == 0:  # Position Mode
      return self.code[offset]
    elif mode == 1:  # Immediate Mode
      return offset
    elif mode == 2:  # Relative Mode
      return self.code[self.relative_base + offset]
    else:
      raise ValueError('Unhandled read parameter mode {0}'.format(mode))

  def write_location(self, value, offset, mode):
    if mode == 0:  # Position Mode
      self.code[offset] = value
    elif mode == 2:  # Relative Mode
      self.code[self.relative_base + offset] = value
    else:
      raise ValueError('Unhandled write parameter mode {0}'.format(mode))


class Processor(object):
  @classmethod
  def run(cls, ctx, cycle_limit=1000):
    while True:
      if ctx.state == States.HALT:
        break
      elif ctx.cycles > cycle_limit:
        raise Exception("How big is this program? Exceeded cycle_limit, {0}".format(cycle_limit))
      # Run an operation
      cls.process_operation(ctx)

  @classmethod
  def process_operation(cls, ctx):
    code = ctx.code
    # Fetch opcode from code @ instruction pointer
    opcode = code[ctx.instruction_pointer]
    # Parse opcode for op and parameter modes
    op, modes = cls.parse_opcode(opcode)
    # Lookup function for op and number of parameters
    opfunc, param_count = cls.resolve_op(op)
    # Load parameters according to modes
    params = []
    for i in range(param_count):
      params.append(code[ctx.instruction_pointer + 1 + i])
    # FIXME - do this better.
    params_modes = zip(params, modes)
    opfunc(ctx, params_modes)
    # Ramp instruction pointer
    ctx.instruction_pointer += 1 + param_count
    # Keep track of how many operations have been processed
    ctx.cycles += 1

  @staticmethod
  def parse_opcode(opcode):
    opcode = "{0:05d}".format(opcode)
    assert len(opcode) == 5
    mode3, mode2, mode1, op = [int(x) for x in [opcode[0], opcode[1], opcode[2], opcode[3:]]]
    return op, [mode1, mode2, mode3]

  @classmethod
  def resolve_op(cls, op):
    methodname = 'OP_{1}'.format(op)
    if hasattr(cls, methodname):
      opfunc = getattr(cls, methodname)
      param_count = opfunc.__dict__.get('params', 3)
      assert 0 <= param_count <= 3, "Invalid number of parameters for code {0}: {1}".format(methodname, param_count)
      return opfunc, param_count
    else:
      raise NotImplementedError(methodname)

  @staticmethod
  def OP_1(ctx, params_modes):
    """ADD"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    result = param1 + param2
    ctx.write_location(result, *params_modes[2])
  OP_1.params = 3

  @staticmethod
  def OP_2(ctx, params_modes):
    """Multiply"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    result = param1 * param2
    ctx.write_location(result, *params_modes[2])
  OP_2.params = 3

  @staticmethod
  def OP_99(ctx, params_modes):
    """Halt"""
    ctx.state = States.Halt
  OP_99.params = 0
