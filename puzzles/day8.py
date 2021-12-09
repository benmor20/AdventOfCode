from puzzles.daybase import DayBase


class Day(DayBase):
    @property
    def num(self) -> int:
        return 8

    def get_data(self, example=False):
        lines = super().get_data(example)
        data = []
        for line in lines:
            input, output = tuple(line.split(' | '))
            data.append((input.split(' '), output.split(' ')))
        return data

    def puzzle1(self):
        data = self.get_data()
        count = 0
        for i, (input, output) in enumerate(data):
            for seg in output:
                if len(seg) in (2, 3, 4, 7):
                    count += 1
                    # print(i, seg)
        print(count)

    def puzzle2(self):
        # Returns a list, where each element is a tuple containing 1. the segments for each digit (a list of the strings
        # to the left of the |) and 2. the segments for the number we want to find (a list of the strings to the right
        # of the |)
        data = self.get_data()

        # For single-value numbers - numbers we can identify by their length alone. Maps length to the number.
        len_key = {2: 1, 3: 7, 4: 4, 7: 8}
        total = 0
        for input, output in data:
            # Goal is to create a key that will map a (sorted) string of lit segments to the corresponding number.
            # We do not actually care about which segment is which, only which list of segments are which.
            key = {}
            single_val_sets = {}  # map of single value numbers (see len_key) to the set of segments it maps to
            for seg in input:
                seg_str = ''.join(sorted(seg))
                # Single value numbers are trivial - find them first, then can use them to find the rest
                if len(seg_str) in len_key:
                    key[seg_str] = len_key[len(seg_str)]
                    single_val_sets[len_key[len(seg_str)]] = set(seg)
            for seg in input:
                seg_str = ''.join(sorted(seg))
                seg_set = set(seg)
                if len(seg_str) not in len_key:  # skip over the single value numbers (already know them)
                    if len(seg_str) == 6:  # 0, 6, and 9
                        # Comparing sets means subsets - returns True iff all segments in the 1 are in the set of
                        # segments for this number. This rules out 6. Comparing to 4 rules out 0.
                        if single_val_sets[1] < seg_set:
                            key[seg_str] = 9 if single_val_sets[4] < seg_set else 0
                        else:
                            key[seg_str] = 6
                    else:  # length is 5 - 2, 3, and 5
                        # See above. Of 2, 3, and 5, 3 is the only one that contains all the segments lit in 1. Of 2 and
                        # 5, can't directly compare subsets as neither contains any single-value number in it, but can
                        # use subtraction (which returns a set containing all elements of the first without the elements
                        # of the second). 4 has 1 segment on that is not on in 5, but 2 segments on that are not on in
                        # 2. Therefore, the length of the set different between the segments for 4 and the segments for
                        # this number will distinguish between 5 and 2.
                        if single_val_sets[1] < seg_set:
                            key[seg_str] = 3
                        else:
                            key[seg_str] = 5 if len(single_val_sets[4] - seg_set) == 1 else 2
            num = 0
            for seg in output:  # Calculate number, then add it to the total
                seg_str = ''.join(sorted(seg))
                num *= 10
                num += key[seg_str]
            total += num
        print(total)
