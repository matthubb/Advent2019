#!/usr/bin/env python

from enum import Enum

States = Enum('RUN', 'WAIT', 'HALT')


class SignalInput(Exception):
  pass


class SignalHalt(Exception):
  pass


class Context(object):
  def __init__(self, code=None, input=None):
    self.instruction_pointer = 0
    self.relative_base = 0
    self.state = States.RUN
    self.cycles = 0
    self.input = [] if input is None else input
    self.output = []
    if code:
      self.load(code)
    else:
      self.code = []

  def load(self, program):
    # Receive a program into memory
    self.code = self.deserialise(program)

  @staticmethod
  def deserialise(program):
    return [int(x) for x in program.strip().split(',')]

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

  def read_input(self):
    if not self.input:
      raise SignalInput()
    return self.input.pop(0)

  def save_output(self, value):
    self.output.append(value)

  @property
  def complete(self):
    return self.state == States.HALT

  @property
  def waiting(self):
    return self.state == States.WAIT


class Processor(object):
  @classmethod
  def run(cls, ctx, cycle_limit=1000):
    if ctx.state == States.HALT:
      raise Exception("Context status == HALT")

    ctx.state = States.RUN
    while True:
      if ctx.cycles > cycle_limit:
        raise Exception("How big is this program? Exceeded cycle_limit, {0}".format(cycle_limit))
      # Run an operation
      try:
        cls.process_operation(ctx)
      except SignalInput:
        ctx.state = States.WAIT
      except SignalHalt:
        ctx.state = States.HALT
      #
      if ctx.state != States.RUN:
        break

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
    # Make a note of the instruction pointer
    track_ip = ctx.instruction_pointer
    # FIXME - do this better. Prepping parameters and modes for opfunc
    params_modes = zip(params, modes)
    # Run the opfunc with the context and parameters with their modes.
    opfunc(ctx, params_modes)
    # Ramp instruction pointer if unmodified by opfunc
    if ctx.instruction_pointer == track_ip:
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
    methodname = 'OP_{0}'.format(op)
    if hasattr(cls, methodname):
      opfunc = getattr(cls, methodname)
    else:
      raise NotImplementedError(methodname)

    params = 'OP_{0}_params'.format(op)
    # param_count = opfunc.__dict__.get('params', 3)
    param_count = getattr(cls, params, 3)
    assert 0 <= param_count <= 3, "Invalid number of parameters for code {0}: {1}".format(methodname, param_count)
    return opfunc, param_count

  @staticmethod
  def OP_1(ctx, params_modes):
    """ADD"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    result = param1 + param2
    ctx.write_location(result, *params_modes[2])
  OP_1_params = 3

  @staticmethod
  def OP_2(ctx, params_modes):
    """Multiply"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    result = param1 * param2
    ctx.write_location(result, *params_modes[2])
  OP_2_params = 3

  @staticmethod
  def OP_3(ctx, params_modes):
    """INPUT"""
    result = ctx.read_input()
    ctx.write_location(result, *params_modes[0])
  OP_3_params = 1

  @staticmethod
  def OP_4(ctx, params_modes):
    """OUTPUT"""
    param1 = ctx.read_location(*params_modes[0])
    ctx.save_output(param1)
  OP_4_params = 1

  @staticmethod
  def OP_5(ctx, params_modes):
    """JUMP IF TRUE"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    if param1 != 0:
      ctx.instruction_pointer = param2
  OP_5_params = 2

  @staticmethod
  def OP_6(ctx, params_modes):
    """JUMP IF FALSE"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    if param1 == 0:
      ctx.instruction_pointer = param2
  OP_6_params = 2

  @staticmethod
  def OP_7(ctx, params_modes):
    """LESS THAN"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    if param1 < param2:
      result = 1
    else:
      result = 0
    ctx.write_location(result, *params_modes[2])
  OP_7_params = 3

  @staticmethod
  def OP_8(ctx, params_modes):
    """LESS THAN"""
    param1 = ctx.read_location(*params_modes[0])
    param2 = ctx.read_location(*params_modes[1])
    if param1 == param2:
      result = 1
    else:
      result = 0
    ctx.write_location(result, *params_modes[2])
  OP_8_params = 3

  @staticmethod
  def OP_99(ctx, params_modes):
    """Halt"""
    # ctx.state = States.HALT
    raise SignalHalt()
  OP_99_params = 0


def run_code(code):
  ctx = Context()
  ctx.load(code)
  Processor.run(ctx)
  assert ctx.complete
  return ctx.dump()


def run_with_io(code, *input):
  ctx = Context()
  ctx.load(code)
  ctx.input.extend(input)
  Processor.run(ctx)
  assert ctx.complete
  return (ctx.dump(), tuple(ctx.output))


def run_with_just_io(code, *input):
  end_code, output = run_with_io(code, *input)
  return output
