import itertools
import re
from collections import deque

from year2024.day2024 import Day2024


class Day(Day2024):
    @property
    def num(self) -> int:
        return 24

    def get_data(self, example=False):
        lines = super().get_raw_data(example)
        start_str, connection_str = lines.split('\n\n')
        initial = {}
        for line in start_str.splitlines():
            match = re.match(r'([xy]\d\d): ([01])', line)
            initial[match.group(1)] = match.group(2) == '1'
        connections = {}
        edges = {}
        for line in connection_str.splitlines():
            match = re.match(r'([a-z\d]{3}) (AND|OR|XOR) ([a-z\d]{3}) -> ([a-z\d]{3})', line)
            key = tuple(sorted([match.group(1), match.group(3)]))
            if key not in connections:
                connections[key] = []
            connections[key].append((match.group(2), match.group(4)))
            if match.group(1) not in edges:
                edges[match.group(1)] = set()
            if match.group(3) not in edges:
                edges[match.group(3)] = set()
            if match.group(4) not in edges:
                edges[match.group(4)] = set()
            edges[match.group(1)].add(match.group(3))
            edges[match.group(3)].add(match.group(1))
        return initial, connections, edges

    def puzzle1(self):
        values, connections, edges = self.get_data()
        queue = deque([neighbor for start, neighbors in edges.items() for neighbor in neighbors if start in values])
        while len(queue) > 0:
            node = queue.popleft()
            for connection in edges[node]:
                if node in values and connection in values:
                    key = tuple(sorted([node, connection]))
                    test_out = connections[key][0][1]
                    if test_out not in values:
                        for gate, out in connections[key]:
                            if gate == 'AND':
                                values[out] = values[node] and values[connection]
                            elif gate == 'OR':
                                values[out] = values[node] or values[connection]
                            elif gate == 'XOR':
                                values[out] = values[node] ^ values[connection]
                            else:
                                assert False
                            queue.extend(edges[out])

        ans_str = ''
        for idx in itertools.count():
            node = 'z' + ('0' if idx < 10 else '') + str(idx)
            if node not in edges:
                break
            ans_str = ('1' if values[node] else '0') + ans_str
        print(int(ans_str, 2))

    def puzzle2(self):
        values, connections, edges = self.get_data()
        mids = []
        and_ins = []
        carries = []
        and_carries = [None]
        try:
            for idx in range(45):
                idx_str = ('0' if idx < 10 else '') + str(idx)
                key = (f'x{idx_str}', f'y{idx_str}')
                assert key in connections, f'{key} not in connections'
                for gate, out in connections[key]:
                    if gate == 'AND':
                        assert out[0] != 'z', f'{key} (AND) is outputting to {out}'
                        and_ins.append(out)
                    elif gate == 'XOR':
                        assert idx == 0 or out[0] != 'z', f'{key} (XOR) is outputting to {out}'
                        mids.append(out)
                    else:
                        assert False, f'{key} has {gate} gate, outputting to {out}'
            assert mids[0] == 'z00'

            carries.append(and_ins[0])
            for idx in range(1, 46):
                key = tuple(sorted([mids[idx], carries[idx - 1]]))
                assert key in connections, f'{key} (mid {mids[idx]} and carry {carries[idx - 1]}) not in connections'
                assert len(connections[key]) == 2, f'{key} (mid {mids[idx]} and carry {carries[idx - 1]}) has wrong number of gates'
                for gate, out in connections[key]:
                    if gate == 'AND':
                        and_carries.append(out)
                    elif gate == 'XOR':
                        target_out = 'z' + ('0' if idx < 10 else '') + str(idx)
                        assert out == target_out, f'{key} (mid {mids[idx]} and carry {carries[idx - 1]}) outputs to {out} instead of {target_out}'
                    else:
                        assert False, f'{key} (mid {mids[idx]} and carry {carries[idx - 1]}) has a {gate} gate outputting to {out}'

                key = tuple(sorted([and_ins[idx], and_carries[idx]]))
                assert key in connections, f'{key} (and_in {and_ins[idx]} and_carry {and_carries[idx - 1]}) not in connections'
                assert len(connections[key]) == 1, f'{key} (and_in {and_ins[idx]} and_carry {and_carries[idx - 1]}) has multiple outputs'
                assert connections[key][0][0] == 'OR', f'{key} (and_in {and_ins[idx]} and_carry {and_carries[idx - 1]}) is not an AND gate'
                carries.append(connections[key][0][1])
        except AssertionError as err:
            print(f'mids:        {mids}')
            print(f'and_ins:     {and_ins}')
            print(f'and_carries:  {and_carries}')
            print(f'carries:     {carries}')
            # Will halt whenever something is wrong, give you some info, then you go manually fix it
            raise err
        nodes = ['jst', 'z05', 'dnt', 'z15', 'mcm', 'gdf', 'gwc', 'z30']
        print(','.join(sorted(nodes)))


def one_line():
    pass
