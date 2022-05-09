from typing import *
from enum import Enum


class ParameterMode(Enum):
    POSITION = 0, True
    IMMEDIATE = 1, False
    RELATIVE = 2, True

    def __init__(self, code, is_addr):
        self.code = code
        self.is_addr = is_addr


class Argument:
    def __init__(self, arg: int, mode: ParameterMode):
        self.arg = arg
        self.mode = mode

    def __repr__(self):
        return f'{self.arg} ({self.mode.name})'


class Operation:
    def __init__(self, opcode: int, nargs: int, func: Callable[['Intcode', List[Argument]], None]):
        self.opcode = opcode
        self.nargs = nargs
        self._func = func

    def __call__(self, intcode: 'Intcode', args: List[Argument]):
        assert len(args) == self.nargs
        start_pointer = intcode.pointer
        self._func(intcode, args)
        if start_pointer == intcode.pointer:
            intcode.pointer += self.nargs + 1


class CombineOperation(Operation):
    def __init__(self, opcode: int, inputs: int, combine: Callable[[int, ...], int]):
        def perform(intcode: 'Intcode', args: List[Argument]):
            assert args[-1].mode.is_addr
            vals = [intcode.arg_value(a) for a in args[:-1]]
            intcode[args[-1]] = combine(*vals)
        super().__init__(opcode, inputs + 1, perform)


def perform_input_operation(intcode: 'Intcode', args: List[Argument]):
    intcode[args[0]] = intcode.inputs.pop()


def perform_output_operation(intcode: 'Intcode', args: List[Argument]):
    intcode.outputs.append(intcode[args[0]])


def get_perform_jump(jump_if_true: bool):
    def perform_jump(intcode: 'Intcode', args: List[Argument]):
        if (intcode[args[0]] != 0) == jump_if_true:
            intcode.pointer = intcode.arg_value(args[1])
    return perform_jump


def perform_base_adjust(intcode: 'Intcode', args: List[Argument]):
    intcode.relative_base += intcode.arg_value(args[0])


OPERATIONS = {
    1: CombineOperation(1, 2, lambda a, b: a + b),
    2: CombineOperation(2, 2, lambda a, b: a * b),
    3: Operation(3, 1, perform_input_operation),
    4: Operation(4, 1, perform_output_operation),
    5: Operation(5, 2, get_perform_jump(True)),
    6: Operation(6, 2, get_perform_jump(False)),
    7: CombineOperation(7, 2, lambda a, b: int(a < b)),
    8: CombineOperation(8, 2, lambda a, b: int(a == b)),
    9: Operation(9, 1, perform_base_adjust),
}


class Intcode:
    def __init__(self, code: List[int], inputs: Optional[List[int]] = None):
        self.code = code
        self.pointer = 0
        self.relative_base = 0
        self.inputs = [] if inputs is None else inputs
        self.outputs = []

    def address(self, arg: Argument) -> int:
        assert arg.mode.is_addr
        if arg.mode == ParameterMode.POSITION:
            return arg.arg
        return self.relative_base + arg.arg

    def arg_value(self, arg: Argument) -> int:
        if arg.mode.is_addr:
            return self[self.address(arg)]
        return arg.arg

    def step(self, verbose: bool = False) -> bool:
        intmodes, opcode = divmod(self[self.pointer], 100)
        if opcode == 99:
            if verbose:
                print('Reached Opcode 99')
            return True
        op = OPERATIONS[opcode]
        args = []
        for i in range(op.nargs):
            arg = self[self.pointer + i + 1]
            intmode = divmod(intmodes, 10 ** i)[0] % 10
            mode = list(ParameterMode)[intmode]
            args.append(Argument(arg, mode))
        if verbose:
            vals = [self.arg_value(a) for a in args]
            print(f'Running opcode {opcode} with inputs {args} and values {vals}...')
        op(self, args)
        if verbose:
            print('Done.')
            print(f'Pointer: {self.pointer}. Rel base: {self.relative_base}. Inputs: {self.inputs}. Outputs: {self.outputs}. Code: {self.code}')
        return False

    def run(self, inputs: Optional[List[int]] = None, verbose: bool = False) -> List[int]:
        if inputs is not None:
            self.inputs = inputs
        while not self.step(verbose=verbose):
            pass
        return self.outputs

    def run_until_output(self, inputs: Optional[List[int]] = None, verbose: bool = False) -> Optional[int]:
        if inputs is not None:
            self.inputs = inputs
        start_len = len(self.outputs)
        while len(self.outputs) == start_len:
            done = self.step(verbose=verbose)
            if done:
                return None
        return self.outputs.pop()

    def run_until_io(self, verbose: bool = False):
        try:
            out = self.run_until_output(verbose=verbose)
            if out is None:
                return None
            self.outputs.append(out)
            return True
        except IndexError:
            return False

    def __len__(self):
        return len(self.code)

    def __getitem__(self, item: Union[Argument, int]):
        if isinstance(item, Argument):
            return self.arg_value(item)
        return self.code[item] if item < len(self.code) else 0

    def __setitem__(self, key: Union[Argument, int], value: int):
        addr = self.address(key) if isinstance(key, Argument) else key
        if addr >= len(self):
            self.code = self.code + [0] * (addr - len(self) + 1)
        self.code[addr] = value
