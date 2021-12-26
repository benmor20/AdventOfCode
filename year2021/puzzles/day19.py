from year2021.day2021 import Day2021
import numpy as np


def all_pairs(vals, vals2=None):
    for i, v1 in enumerate(vals):
        for j, v2 in enumerate(vals if vals2 is None else vals2):
            if vals2 is not None or i > j:
                yield v1, v2


def could_match(b11, b12, b21, b22):
    d1 = b11[:3] - b12[:3]
    d2 = b21[:3] - b22[:3]
    return sorted(abs(d1)) == sorted(abs(d2))


def get_overlap_from_basis(sensor1_beacons, sensor2_beacons, basisi, basisj):
    basis1, basis2 = sensor1_beacons[basisi], sensor2_beacons[basisj]
    s1overlap, s2overlap = basis1.copy().reshape(4, 1), basis2.copy().reshape(4, 1)
    for i, b1 in enumerate(sensor1_beacons):
        if i == basisi:
            continue
        for j, b2 in enumerate(sensor2_beacons):
            if j == basisj:
                continue
            if could_match(basis1, b1, basis2, b2):
                s1overlap = np.concatenate((s1overlap, b1.reshape(4, 1)), axis=1)
                s2overlap = np.concatenate((s2overlap, b2.reshape(4, 1)), axis=1)
    # print(s1overlap)
    return np.array(s1overlap), np.array(s2overlap)


def get_overlap(readings, i, j):
    sensor1_beacons = readings[i].T
    sensor2_beacons = readings[j].T
    overlap = {}
    for basisi, basisj in all_pairs(range(len(sensor1_beacons)), range(len(sensor2_beacons))):
        overlap[(basisi, basisj)] = get_overlap_from_basis(sensor1_beacons, sensor2_beacons, basisi, basisj)
    return overlap[max(overlap, key=lambda o: overlap[o][0].shape[1])]


def get_transform(readings, i, j):
    s1_beacons, s2_beacons = get_overlap(readings, i, j)
    if s1_beacons is None or s1_beacons.shape[1] < 4:
        return None
    A = s2_beacons[:, :4] @ np.linalg.inv(s1_beacons[:, :4])
    return np.linalg.inv(np.round(A))


def all_in(vals, lst):
    for val in vals:
        if val not in lst:
            return False
    return True


def calculate_poses(readings):
    sensor_poses = {0: np.eye(4)}  # use dict: won't necessarily go in order
    checked = set()
    all_sensors = set(range(len(readings)))
    prev = {0}
    while not all_in(range(len(readings)), sensor_poses):
        for index in all_sensors - set(sensor_poses):
            for basis_index in sensor_poses:
                if (basis_index, index) in checked:
                    continue
                pose = get_transform(readings, basis_index, index)
                checked.add((basis_index, index))
                if pose is not None:
                    print(f'Adding {index}')
                    sensor_poses[index] = sensor_poses[basis_index] @ pose
                    break
        if set(sensor_poses) == prev:
            for basis in sensor_poses:
                for index in all_sensors - set(sensor_poses):
                    assert (basis, index) in checked
            raise ValueError(f'Could not calculate poses for {all_sensors - set(sensor_poses)}')
        prev = set(sensor_poses)
    return [sensor_poses[i] for i in range(len(sensor_poses))]


def to_tuple_set(beacons):
    res = set()
    for i in range(beacons.shape[1]):
        res.add(tuple(beacons[:3, i]))
    return res


def get_beacons(readings):
    poses = calculate_poses(readings)
    beacons = set()
    for pose, rel_beacons in zip(poses, readings):
        beacons.update(to_tuple_set(pose @ rel_beacons))
    return beacons


class Day(Day2021):
    @property
    def num(self) -> int:
        return 19

    def get_data(self, example=False):
        lines = super().get_data(example)
        readings = []
        beacons = []
        for line in lines:
            if len(line) == 0:
                b_arr = np.array(beacons).T
                readings.append(np.concatenate((b_arr, np.ones((1, b_arr.shape[1])))))
                beacons = []
                continue
            elif line[0:3] == '---':
                continue
            beacons.append([int(i) for i in line.split(',')])
        b_arr = np.array(beacons).T
        readings.append(np.concatenate((b_arr, np.ones((1, b_arr.shape[1])))))
        return readings

    def puzzle1(self):
        return
        # print(len(get_beacons(self.get_data(True))))

    def puzzle2(self):
        poses = calculate_poses(self.get_data())
        highest = 0
        for p1, p2 in all_pairs(poses):
            highest = max(highest, np.sum(abs(p1[:3, 3] - p2[:3, 3])))
        print(highest)
