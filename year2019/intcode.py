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
        self.original_code = self.intcode.copy()

    def reset(self, inputs: Optional[List[int]] = None):
        self.intcode = self.original_code.copy()
        self.outputs.clear()
        self.inputs = inputs if inputs is not None else []
        self.pointer = 0

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

    def step(self, verbose=False) -> bool:
        modes_and_opcode = self.intcode[self.pointer]
        mode_num, opcode = divmod(modes_and_opcode, 100)
        operation = OPERATIONS[opcode]
        self.pointer += 1
        modes = list(map(mode_from_id, utils.to_digits(mode_num, operation.nargs)))[::-1]
        if verbose:
            og_intcode = self.intcode.copy()
            og_pointer = self.pointer
        res = operation(self, modes)
        if verbose:
            print(f'Opcode was {opcode}. Inputs are now {self.inputs}, outputs are {self.outputs}. Arg vals were {[arg_value(m, a, og_intcode) for m, a in zip(modes, self.intcode[og_pointer:og_pointer+operation.nargs])]}. Pointer is now at {self.pointer} with intcode of {self.intcode}')
        return res

    def _run_setup(self, reset: bool = False, inputs: Optional[List[int]] = None, verbose=False):
        if reset:
            self.reset(inputs=inputs)
        elif inputs is not None:
            self.inputs = inputs
        if verbose:
            print(f'Inputs are {self.inputs}')

    def run(self, reset: bool = False, inputs: Optional[List[int]] = None, verbose: bool = False)\
            -> Tuple[List[int], List[int]]:
        self._run_setup(reset, inputs, verbose)
        while not self.step(verbose=verbose):
            pass
        return self.intcode, self.outputs

    def run_until_output(self, reset: bool = False, inputs: Optional[List[int]] = None, verbose: bool = False)\
            -> Optional[int]:
        self._run_setup(reset, inputs, verbose)
        while len(self.outputs) == 0 and not self.step(verbose=verbose):
            pass
        return self.outputs.pop() if len(self.outputs) > 0 else None

    def __getitem__(self, item):
        return self.intcode[item]

    def __setitem__(self, key, value):
        self.intcode[key] = value
