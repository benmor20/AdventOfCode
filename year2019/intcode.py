from typing import *
from enum import Enum
from utils import utils


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


def mode_from_id(mode_id):
    for mode in ParameterMode:
        if mode.value == mode_id:
            return mode
    return None


def arg_value(mode: ParameterMode, arg: int, intcode: Union[List[int], 'Intcode']) -> int:
    if mode == ParameterMode.POSITION:
        return intcode[arg]
    elif mode == ParameterMode.IMMEDIATE:
        return arg


class Operation:
    def __init__(self, opcode: int, nargs: int, perform: Callable[['Intcode', List[ParameterMode]], bool]):
        self.opcode = opcode
        self.nargs = nargs
        self._perform = perform

    def __call__(self, intcode: 'Intcode', modes: List[ParameterMode]) -> bool:
        start_pointer = intcode.pointer
        res = self._perform(intcode, modes)
        end_pointer = intcode.pointer
        if start_pointer == end_pointer:
            intcode.pointer += self.nargs
        return res


class CombineOperation(Operation):
    def __init__(self, opcode: int, combine: Callable[[int, ...], int], nargs: int = 3):
        def perform(intcode: 'Intcode', modes: List[ParameterMode]):
            assert modes[-1] == ParameterMode.POSITION
            args = intcode.intcode[intcode.pointer:intcode.pointer+nargs]
            inputs = [arg_value(m, a, intcode.intcode) for m, a in zip(modes[:-1], args[:-1])]
            intcode.intcode[args[-1]] = combine(*inputs)
            return False
        super().__init__(opcode, nargs, perform)


def perform_input_op(intcode: 'Intcode', modes: List[ParameterMode]) -> bool:
    assert len(modes) == 1
    mode = modes[0]
    arg = intcode[intcode.pointer]
    assert mode == ParameterMode.POSITION
    intcode[arg] = intcode.inputs.pop()
    return False


def perform_output_op(intcode: 'Intcode', modes: List[ParameterMode]) -> bool:
    assert len(modes) == 1
    mode = modes[0]
    arg = intcode[intcode.pointer]
    intcode.outputs.append(arg_value(mode, arg, intcode))
    return False


def perform_jump(jump_if: bool, intcode: 'Intcode', modes: List[ParameterMode]) -> bool:
    assert len(modes) == 2
    args = intcode[intcode.pointer:intcode.pointer+2]
    if (arg_value(modes[0], args[0], intcode) != 0) == jump_if:
        intcode.pointer = arg_value(modes[1], args[1], intcode)
    return False


OPERATIONS = {
                1: CombineOperation(1, lambda a, b: a + b),
                2: CombineOperation(2, lambda a, b: a * b),
                3: Operation(3, 1, perform_input_op),
                4: Operation(4, 1, perform_output_op),
                5: Operation(5, 2, lambda ic, m: perform_jump(True, ic, m)),
                6: Operation(6, 2, lambda ic, m: perform_jump(False, ic, m)),
                7: CombineOperation(7, lambda a, b: a < b),
                8: CombineOperation(8, lambda a, b: a == b),
                99: Operation(99, 0, lambda *_: True),
            }


class Intcode:
    def __init__(self, intcode, inputs=None, **kwargs):
        self.intcode = intcode.copy()
        self.pointer = 0
        if inputs:
            self.inputs = inputs
        else:
            self.inputs = []
        self.outputs = []
        self.set(kwargs)

    def set(self, values: Dict[Union[str, int], int]):
        for pos, value in values.items():
            if isinstance(pos, int):
                self.intcode[pos] = value
            elif pos == 'noun':
                self.intcode[1] = value
            elif pos == 'verb':
                self.intcode[2] = value
            else:
                raise ValueError(f'Unrecognized position: {pos}')

    def step(self) -> bool:
        modes_and_opcode = self.intcode[self.pointer]
        mode_num, opcode = divmod(modes_and_opcode, 100)
        operation = OPERATIONS[opcode]
        self.pointer += 1
        modes = list(map(mode_from_id, utils.to_digits(mode_num, operation.nargs)))[::-1]
        return operation(self, modes)

    def run(self) -> Tuple[List[int], List[int]]:
        while not self.step():
            pass
        return self.intcode, self.outputs

    def __getitem__(self, item):
        return self.intcode[item]

    def __setitem__(self, key, value):
        self.intcode[key] = value
