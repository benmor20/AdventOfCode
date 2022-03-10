import itertools
from typing import *
from year2019.day2019 import Day2019
from year2019.intcode import Intcode


class Amplifier(Intcode):
    def __init__(self, code: List[int], phase: int):
        self.phase = phase
        super().__init__(code, [phase])

    def output_signal(self, input_signal, first_run=True):
        inputs = [input_signal, self.phase] if first_run else [input_signal]
        return self.run_until_output(first_run, inputs)


def run_feedback_amps(amps):
    signal = 0
    signals = []
    first_run = True
    while signal is not None:
        for amp in amps:
            signal = amp.output_signal(signal, first_run)
        signals.append(signal)
        first_run = False
    signals.pop()
    assert max(signals) == signals[-1]
    return max(signals)


class Day(Day2019):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example: Union[bool, int] = False):
        lines = super().get_data(example)
        data = [int(i) for i in lines[0].split(',')]
        return data

    def puzzles(self):
        code = self.get_data()
        # signals = {}
        # for phases in itertools.permutations(range(5)):
        #     amps = [Amplifier(code, p) for p in phases]
        #     signal = 0
        #     for i, amp in enumerate(amps):
        #         signal = amp.output_signal(signal)
        #     signals[phases] = signal
        # max_signal = max(signals.values())
        # print(f'Max signal is {max_signal}')

        feedback_signals = {}
        for phases in itertools.permutations(range(5, 10)):
            amps = [Amplifier(code, p) for p in phases]
            feedback_signals[phases] = run_feedback_amps(amps)
        print(f'Max feedback signal is {max(feedback_signals.values())}')
