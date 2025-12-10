import itertools
from typing import Generator

import numpy as np
from matplotlib import pyplot as plt

from year2025.day2025 import Day2025


def along_line(start: complex, end: complex, yield_bounds: bool) -> Generator[complex, None, None]:
    if yield_bounds:
        yield start

    diff = end - start
    if diff.imag == 0:
        drctn = 1 if diff.real > 0 else -1
    elif diff.real == 0:
        drctn = 1j if diff.imag > 0 else -1j
    else:
        assert False

    to_yield = start + drctn
    while to_yield != end:
        yield to_yield
        to_yield += drctn

    if yield_bounds:
         yield end


def get_border_tiles(corner_tiles: list[complex]) -> set[complex]:
    tiles = set[complex]()
    for idx, tile in enumerate(corner_tiles):
        prev_tile = corner_tiles[idx - 1]
        for pt in along_line(prev_tile, tile, True):
            tiles.add(pt)
    return tiles


def get_edges(a: complex, b: complex) -> Generator[complex, None, None]:
    c = a.real + b.imag * 1j
    yield c
    d = b.real + a.imag * 1j
    yield d
    for p1, p2 in [(a, c), (c, b), (b, d), (d, a)]:
        yield from along_line(p1, p2, False)


def is_in_loop(point: complex, border_tiles: set[complex], min_bounds: complex, max_bounds: complex) -> bool:
    if point in border_tiles:
        return True

    dists = [point.real - min_bounds.real, point.imag - min_bounds.imag, max_bounds.real - point.real, max_bounds.imag - point.imag]
    min_dist = min(dists)
    if min_dist == dists[0]:
        drctn = -1
        target = min_bounds.real + point.imag * 1j
    elif min_dist == dists[1]:
        drctn = -1j
        target = point.real + min_bounds.imag * 1j
    elif min_dist == dists[2]:
        drctn = 1
        target = max_bounds.real + point.imag * 1j
    else:
        drctn = 1j
        target = point.real + max_bounds.imag * 1j

    count = 0
    for pt in along_line(point, target, True):
        if pt in border_tiles:
            count += 1
    return count % 2 == 1


# def compute_intersection(line1_start: complex, line1_end: complex, line2_start: complex, line2_end: complex) -> complex:
#     line1_det = determinant(line1_start.real, line1_start.imag, line1_end.real, line1_end.imag)
#     line2_det = determinant(line2_start.real, line2_start.imag, line2_end.real, line2_end.imag)
#     x_num = determinant(line1_det, line1_start.real - line1_end.real, line2_det, line2_start.real - line2_end.real)
#     y_num = determinant(line1_end.imag - line1_start.imag, line1_det, line2_end.imag - line2_start.imag, line2_det)
#     denom = determinant(line1_end.imag - line1_start.imag, line1_start.real - line1_end.real, line2_end.imag - line2_start.imag, line2_start.real - line2_end.real)
#     if denom == 0:
#         return None
#     return (x_num + y_num * 1j) / denom


def determinant(a, b, c, d):
    return a * d - b * c


def compute_intersection(p1: complex, p2: complex, p3: complex, p4: complex) -> complex | None:
    x1, y1 = p1.real, p1.imag
    x2, y2 = p2.real, p2.imag
    x3, y3 = p3.real, p3.imag
    x4, y4 = p4.real, p4.imag

    denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(denom) < 1e-9:
        return None

    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

    return px + py*1j


def point_in_edge(point: complex, edge_start: complex, edge_end: complex) -> bool:
    # assumes edge is ordered CCW
    edge_dir = edge_end - edge_start
    point_dir = point - edge_start
    return determinant(edge_dir.real, edge_dir.imag, point_dir.real, point_dir.imag) <= 0


def clip_polygon(subject_verts: list[complex], clip_verts: list[complex]):
    output_list = list(subject_verts)
    for clip_edge_idx, clip_edge_end in enumerate(clip_verts):
        clip_edge_start = clip_verts[clip_edge_idx - 1]
        input_list = list(output_list)
        output_list.clear()
        for idx, current_pt in enumerate(input_list):
            prev_pt = input_list[idx - 1]
            intersection_pt = compute_intersection(prev_pt, current_pt, clip_edge_start, clip_edge_end)
            if point_in_edge(current_pt, clip_edge_start, clip_edge_end):
                if not point_in_edge(prev_pt, clip_edge_start, clip_edge_end):
                    assert intersection_pt is not None
                    output_list.append(intersection_pt)
                output_list.append(current_pt)
            elif point_in_edge(prev_pt, clip_edge_start, clip_edge_end):
                assert intersection_pt is not None
                output_list.append(intersection_pt)
        # if not output_list:
        #     print(f"Polygon eliminated at clip edge {clip_edge_idx} ({clip_edge_start}, {clip_edge_end})")
        #     break
    return output_list


def plot_complex(pts: list[complex], style: str = None):
    np_data = np.array([[t.real, t.imag] for t in pts])
    plt.plot(np_data[:, 0], np_data[:, 1], style)


class Day(Day2025):
    @property
    def num(self) -> int:
        return 9

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = [int((splt := line.split(","))[0]) + int(splt[1]) * 1j for line in lines]
        return data

    def puzzle1(self):
        data = self.get_data()
        max_area = 0
        for a, b in itertools.combinations(data, r=2):
            width = abs(a.real - b.real) + 1
            height = abs(a.imag - b.imag) + 1
            area = width * height
            max_area = max(area, max_area)
        print(max_area)

    def puzzle2(self):
        corner_tiles_small = self.get_data()
        small_to_large_real = sorted(t.real for t in corner_tiles_small)
        small_to_large_imag = sorted(t.imag for t in corner_tiles_small)
        large_to_small_real = {t: idx for idx, t in enumerate(small_to_large_real)}
        large_to_small_imag = {t: idx for idx, t in enumerate(small_to_large_imag)}
        corner_tiles_small = [large_to_small_real[t.real] + large_to_small_imag[t.imag] * 1j for t in corner_tiles_small]
        tiles_small = set(corner_tiles_small)
        for idx, current in enumerate(corner_tiles_small):
            prev = corner_tiles_small[idx - 1]
            tiles_small.update(along_line(prev, current, False))
        for real in range(len(corner_tiles_small)):
            is_in_bounds = real in tiles_small
            for imag in range(len(corner_tiles_small)):
                pt = real + imag * 1j
                if pt in tiles_small and (pt + 1j) not in tiles_small:
                    is_in_bounds = not is_in_bounds
                if is_in_bounds:
                    tiles_small.add(pt)

        max_area = 0
        for a, b in itertools.combinations(corner_tiles_small, r=2):
            c = a.real + b.imag * 1j
            d = b.real + a.imag * 1j
            if c not in tiles_small or d not in tiles_small:
                continue
            if any(t not in tiles_small for t in along_line(a, c, False)):
                continue
            if any(t not in tiles_small for t in along_line(c, b, False)):
                continue
            if any(t not in tiles_small for t in along_line(b, d, False)):
                continue
            if any(t not in tiles_small for t in along_line(d, a, False)):
                continue

            width = abs(small_to_large_real[int(a.real)] - small_to_large_real[int(b.real)]) + 1
            height = abs(small_to_large_imag[int(a.imag)] - small_to_large_imag[int(b.imag)]) + 1
            area = width * height
            max_area = max(area, max_area)
        print(max_area)


    # def puzzle2(self):
    #     data = self.get_data()
    #     plot_complex(data, '-k')
    #
    #     border = get_border_tiles(data)
    #     min_bounds = min(t.real for t in data) + min(t.imag for t in data) * 1j - 1 - 1j
    #     max_bounds = max(t.real for t in data) + max(t.imag for t in data) * 1j + 1 + 1j
    #
    #     max_area = 0
    #     # print("Starting...")
    #     for a, b in itertools.combinations(data, r=2):
    #         if a.real == b.real or a.imag == b.imag:
    #             continue
    #         # c = a.real + b.imag * 1j
    #         # d = b.real + a.imag * 1j
    #         # rect = [a, c, b, d]
    #         # rect_set = set(rect)
    #         # clip = clip_polygon(rect, data)
    #         # print(f"{rect=}")
    #         # print(f"{clip=}")
    #         # plot_complex(rect, '-ob')
    #         # # plot_complex(clip, '-or')
    #         # break
    #         # if set(clip) != rect_set:
    #         #     continue
    #         out_of_loop = False
    #         for pt in get_edges(a, b):
    #             # print(f"{pt=}")
    #             in_loop = is_in_loop(pt, border, min_bounds, max_bounds)
    #             # print(f"{in_loop=}")
    #             if not in_loop:
    #                 out_of_loop = True
    #                 break
    #         if out_of_loop:
    #             # print("Continuing")
    #             continue
    #
    #         # print("Valid")
    #         width = abs(a.real - b.real) + 1
    #         height = abs(a.imag - b.imag) + 1
    #         area = width * height
    #         max_area = max(area, max_area)
    #
    #     # plt.axis("equal")
    #     # plt.show()
    #
    #     print(max_area)


def one_line():
    pass
