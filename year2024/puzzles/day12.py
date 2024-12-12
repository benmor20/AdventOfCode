from year2024.day2024 import Day2024
from collections import Counter


DIRECTIONS = {
    1: [-1j, 1j],
    -1: [-1j, 1j],
    1j: [1, -1],
    -1j: [1, -1]
}


def split_areas(og_data):
    new_data = {}
    num_fields = {}
    for pos, field in og_data.items():
        if pos in new_data:
            continue
        field_num = num_fields.get(field, 0)
        queue = [pos]
        while len(queue) > 0:
            curr = queue.pop()
            if curr in new_data:
                continue
            new_data[curr] = field + str(field_num)
            for drctn in DIRECTIONS:
                nxt = curr + drctn
                if nxt in og_data and og_data[nxt] == field and nxt not in new_data:
                    queue.append(nxt)
        num_fields[field] = field_num + 1
    return new_data


class Day(Day2024):
    @property
    def num(self) -> int:
        return 12

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = {}
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                data[i + j * 1j] = lines[i][j]
        return data

    def puzzle1(self):
        data = self.get_data()
        fields = split_areas(data)
        areas = {}
        perims = {}
        for pos, field in fields.items():
            areas[field] = areas.get(field, 0) + 1
            if field not in perims:
                perims[field] = 0
            for drctn in DIRECTIONS:
                adj = pos + drctn
                if adj not in fields or (adj in fields and fields[adj] != field):
                    perims[field] = perims[field] + 1
        # print(areas)
        # print(perims)
        price = 0
        for field in areas:
            price += areas[field] * perims[field]
        print(price)


    def puzzle2(self):
        data = self.get_data()
        fields = split_areas(data)
        areas = Counter(fields.values())
        checked = set()
        nedges = {}
        for pos, field in fields.items():
            if field not in nedges:
                nedges[field] = 0
            for drctn, perps in DIRECTIONS.items():
                nxt = pos + drctn
                if (pos, drctn) in checked or (nxt in fields and fields[nxt] == field):
                    continue
                checked.add((pos, drctn))
                # print(f'{pos} ({field}) with {drctn} not checked, adding edge')
                nedges[field] = nedges[field] + 1
                curr = pos
                for perp in perps:
                    curr = curr + perp
                    adj = curr + drctn
                    while curr in fields and fields[curr] == field and (adj not in fields or fields[adj] != field):
                        checked.add((curr, drctn))
                        curr += perp
                        adj += perp
        price = 0
        for field in areas:
            price += areas[field] * nedges[field]
            # print(f'{field}: {areas[field]} * {nedges[field]} = {areas[field] * nedges[field]}')
        print(price)



def one_line():
    pass
