from typing import *


class Operation:
    def __init__(self, opcode: int, nargs: int, perform: Callable[[List[int], List[int]], Tuple[bool, List[int]]]):
        self.opcode = opcode
        self.nargs = nargs
        self._perform = perform

    def __call__(self, *args, **kwargs):
        return self._perform(*args)


class CombineOperation(Operation):
    def __init__(self, opcode: int, combine: Callable[[int, ...], int], nargs: int = 3):
        def perform(intcode: List[int], args: List[int]) -> Tuple[bool, List[int]]:
            inputs = [intcode[i] for i in args[:-1]]
            intcode[args[-1]] = combine(*inputs)
            return False, intcode
        super().__init__(opcode, nargs, perform)


OPERATIONS = {
                1: CombineOperation(1, lambda a, b: a + b),
                2: CombineOperation(2, lambda a, b: a * b),
                99: Operation(99, 0, lambda ic, args: (True, ic)),
            }


class Intcode:
    def __init__(self, intcode, **kwargs):
        self.intcode = intcode.copy()
        self.pointer = 0
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
        opcode = self.intcode[self.pointer]
        operation = OPERATIONS[opcode]
        self.pointer += 1
        args = self.intcode[self.pointer:self.pointer+operation.nargs]
        end, self.intcode = operation(self.intcode, args)
        self.pointer += operation.nargs
        return end

    def run(self) -> List[int]:
        while not self.step():
            pass
        return self.intcode
