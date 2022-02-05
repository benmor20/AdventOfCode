import numpy as np


class D4Group:
    def __init__(self, rot90, flip_horz):
        self.rot90 = rot90
        self.flip_horz = flip_horz
        self.transforms = [self.rot0, self.rot90, self.rot180, self.rot270,
                           self.flip_horz, self.flip_vert, self.flip_diag, self.flip_diag2]

    def rot0(self, obj):
        return obj

    def rot180(self, obj):
        return self.rot90(self.rot90(obj))

    def rot270(self, obj):
        return self.rot90(self.rot180(obj))

    def flip_vert(self, obj):
        return self.rot180(self.flip_horz(obj))

    def flip_diag(self, obj):
        return self.flip_horz(self.rot90(obj))

    def flip_diag2(self, obj):
        return self.rot90(self.flip_horz(obj))


D4 = D4Group(np.rot90, lambda a: np.flip(a, 0))
