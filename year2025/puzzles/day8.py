from collections import Counter

import networkx as nx
import numpy as np

from year2025.day2025 import Day2025


class Day(Day2025):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = np.array([[int(i) for i in line.split(",")] for line in lines])
        return data

    def puzzle1(self):
        example = False
        data = self.get_data(example)
        nconns = 10 if example else 1000
        dists = np.linalg.norm(data[np.newaxis, :, :] - data[:, np.newaxis, :], axis=-1)
        for i in range(data.shape[0]):
            for j in range(i + 1):
                dists[i, j] = np.inf
        print("Starting sort")
        flat_idxs = np.argsort(dists.flatten())
        print("Done")
        shortest_dists = np.array(np.unravel_index(flat_idxs, dists.shape)).T
        connections = [{i} for i in range(data.shape[0])]
        connection_locations = list(range(data.shape[0]))
        rem_connections = nconns
        for shortest_idxs in shortest_dists:
            assert shortest_idxs.shape == (2,), shortest_idxs
            i, j = shortest_idxs
            iloc = connection_locations[i]
            jloc = connection_locations[j]
            # if iloc == jloc:
            #     continue
            # print(f"Connecting {i} and {j} (located at {iloc} and {jloc})")

            connections[iloc].update(connections[jloc])
            for idx in connections[jloc]:
                connection_locations[idx] = iloc
            # print(f"Set size is now {len(connections[iloc])}")
            # print(f"There are {len(connections)} sets: {connections}")
            # print(f"{connection_locations=}")

            rem_connections -= 1
            if rem_connections == 0:
                break

        set_sizes = Counter(connection_locations)
        print(set_sizes)
        largest_idxs = set_sizes.most_common(3)
        print(largest_idxs)

        prod = 1
        for _, amt in largest_idxs:
            prod *= amt
        print(prod)

    def puzzle2(self):
        data = self.get_data()
        dists = np.linalg.norm(data[np.newaxis, :, :] - data[:, np.newaxis, :], axis=-1)
        for i in range(data.shape[0]):
            for j in range(i + 1):
                dists[i, j] = np.inf
        flat_idxs = np.argsort(dists.flatten())
        shortest_dists = np.array(np.unravel_index(flat_idxs, dists.shape)).T
        connections = [{i} for i in range(data.shape[0])]
        connection_locations = list(range(data.shape[0]))
        ncircuits = data.shape[0]
        for shortest_idxs in shortest_dists:
            i, j = shortest_idxs
            iloc = connection_locations[i]
            jloc = connection_locations[j]
            if iloc == jloc:
                continue
            connections[iloc].update(connections[jloc])
            for idx in connections[jloc]:
                connection_locations[idx] = iloc

            ncircuits -= 1
            if ncircuits == 1:
                print(data[i, 0] * data[j, 0])
                break


def one_line():
    pass
