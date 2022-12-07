from year2022.day2022 import Day2022


class File:
    def __init__(self, parent: 'File', name: str, is_dir: bool = True, size = None):
        self.parent = parent
        self.name = name
        self.is_dir = is_dir
        self.children = []
        self._size = size

    def has_child(self, name: str) -> bool:
        return any(f.name == name for f in self.children)

    def get_child(self, name: str) -> 'File':
        return [f for f in self.children if f.name == name][0]

    def size(self) -> int:
        if self._size is None:
            return sum(f.size() for f in self.children)
        return self._size


class Day(Day2022):
    @property
    def num(self) -> int:
        return 7

    def create_file(self):
        lines = self.get_data()
        root_file = File(None, '/')
        current_file = root_file
        for line in lines:
            if line[0] == '$':
                cmd = line[2:]
                if cmd[:2] == 'cd':
                    target = cmd[3:]
                    if target == '..':
                        current_file = current_file.parent
                    elif current_file.has_child(target):
                        current_file = current_file.get_child(target)
                    else:
                        current_file.children.append(File(current_file, target))
                        current_file = current_file.children[-1]
                else:
                    assert cmd[:2] == 'ls'
            else:
                if line[:3] == 'dir':
                    current_file.children.append(File(current_file, line[4:]))
                else:
                    sizestr, name = tuple(line.split(' '))
                    size = int(sizestr)
                    current_file.children.append(File(current_file, name, False, size))
        return root_file

    def _puzzle1(self, file: File):
        if not file.is_dir:
            return 0
        size = file.size()
        children = sum(self._puzzle1(c) for c in file.children)
        if size <= 100000:
            return size + children
        return children

    def puzzle1(self):
        print(self._puzzle1(self.create_file()))

    def _puzzle2(self, file: File, target_size: int) -> File:
        if not file.is_dir:
            return None
        files = [self._puzzle2(c, target_size) for c in file.children]
        files = [f for f in files if f is not None]
        if file.size() >= target_size:
            files.append(file)
        # print(f'{file.name}: {[f.name for f in files]}')
        try:
            return min(files, key=lambda f: f.size())
        except:
            return None

    def puzzle2(self):
        root = self.create_file()
        print(self._puzzle2(root, -40000000 + root.size()).size())
