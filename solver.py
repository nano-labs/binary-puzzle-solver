import itertools
import sys
from time import sleep
from terminaltables import AsciiTable, SingleTable

_ = None

RED = "\033[91m"
GREEN = "\033[92m"
GRAY = "\033[90m"
RESET = "\033[0m"


class Bit:

    def __init__(self, value, row, column, initial=False):
        self.value = value
        self.row = row
        self.column = column
        self.initial = initial

    @classmethod
    def inital_map(cls, binary):
        new_binary = []
        for i, r in enumerate(binary):
            row = []
            for j, c in enumerate(r):
                row.append(cls(value=c, row=i, column=j, initial=True))
            new_binary.append(row)
        return new_binary

    def __str__(self):
        if self.value is None:
            return " "
        return (
            f"{GRAY}{self.value}{RESET}"
            if self.initial
            else f"{GREEN}{self.value}{RESET}"
        )

    def __repr__(self):
        return str(self)


class BinarySolver:

    def __init__(self, binary):
        self.binary = Bit.inital_map(binary)
        self._printed = False

    @property
    def rows(self):
        return self.binary

    @property
    def columns(self):
        cols = []
        for i in range(12):
            col = []
            for row in self.binary:
                col.append(row[i])
            cols.append(col)
        return cols

    def update_bit(self, bit, value):
        self.binary[bit.row][bit.column] = Bit(
            value=value, row=bit.row, column=bit.column, initial=False
        )
        self.print(0.1)

    def refresh_bit(self, bit):
        return self.binary[bit.row][bit.column]

    def check_doubles(self, bit):
        if not bit.value is None:
            return False

        # check up
        if bit.row >= 2:
            if [
                self.binary[bit.row - 1][bit.column].value,
                self.binary[bit.row - 2][bit.column].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True
            if [
                self.binary[bit.row - 1][bit.column].value,
                self.binary[bit.row - 2][bit.column].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True

        # check down
        if bit.row < 10:
            if [
                self.binary[bit.row + 1][bit.column].value,
                self.binary[bit.row + 2][bit.column].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True
            if [
                self.binary[bit.row + 1][bit.column].value,
                self.binary[bit.row + 2][bit.column].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True

        # check left
        if bit.column >= 2:
            if [
                self.binary[bit.row][bit.column - 1].value,
                self.binary[bit.row][bit.column - 2].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True
            if [
                self.binary[bit.row][bit.column - 1].value,
                self.binary[bit.row][bit.column - 2].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True

        # check right
        if bit.column < 10:
            if [
                self.binary[bit.row][bit.column + 1].value,
                self.binary[bit.row][bit.column + 2].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True
            if [
                self.binary[bit.row][bit.column + 1].value,
                self.binary[bit.row][bit.column + 2].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True

        return False

    def check_neighbour(self, bit):
        if not bit.value is None:
            return False

        # check horizontally
        if bit.column >= 1 and bit.column < 11:
            if [
                self.binary[bit.row][bit.column - 1].value,
                self.binary[bit.row][bit.column + 1].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True
            if [
                self.binary[bit.row][bit.column - 1].value,
                self.binary[bit.row][bit.column + 1].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True

        # check vertically
        if bit.row >= 1 and bit.row < 11:
            if [
                self.binary[bit.row - 1][bit.column].value,
                self.binary[bit.row + 1][bit.column].value,
            ] == [1, 1]:
                self.update_bit(bit, 0)
                return True
            if [
                self.binary[bit.row - 1][bit.column].value,
                self.binary[bit.row + 1][bit.column].value,
            ] == [0, 0]:
                self.update_bit(bit, 1)
                return True

        return False

    def check_sequence(self, sequence):

        def is_valid(guess, sequence):
            to_test = []
            for i in sequence:
                if i.value is None:
                    to_test.append(Bit(value=guess.pop(0), row=i.row, column=i.column))
                else:
                    to_test.append(i)

            for i in range(2, 12):
                if list([b.value for b in to_test[i - 3 : i]]) in [
                    [1, 1, 1],
                    [0, 0, 0],
                ]:
                    return None
            return to_test

        changed = False
        sequence = list([self.refresh_bit(bit) for bit in sequence])
        zeros = len([i for i in sequence if i.value == 0])
        ones = len([i for i in sequence if i.value == 1])

        items = ([0] * (6 - zeros)) + ([1] * (6 - ones))

        unique_permutations = sorted(set(itertools.permutations(items)))

        valids = []
        for guess in unique_permutations:
            valid = is_valid(list(guess), sequence)
            if valid:
                valids.append(valid)

        uniques = [
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
        ]
        for p in valids:
            for i in range(12):
                uniques[i].add(p[i].value)

        for i, item in enumerate(uniques):
            if (
                len(list([x for x in item if not x is None])) == 1
                and sequence[i].value is None
            ):
                self.update_bit(sequence[i], item.pop())
                # breakpoint()
                changed = True
        return changed

    def solve_simple(self):
        changed = False
        keep_checking = True
        while keep_checking is True:
            keep_checking = False
            for row in self.rows:
                for bit in row:
                    if self.check_doubles(bit):
                        changed = True
                        keep_checking = True
                    elif self.check_neighbour(bit):
                        changed = True
                        keep_checking = True
        return changed

    def solve_sequences(self):
        changed = False
        for row in self.rows:
            if self.check_sequence(row):
                changed = True
                self.solve_simple()
        for column in self.columns:
            if self.check_sequence(column):
                changed = True
                self.solve_simple()

        return changed

    def solve(self):
        self.solve_simple()

        changed = True
        while changed is True:
            changed = self.solve_sequences()

    def print(self, delay=0.0):
        if self._printed:
            sys.stdout.write("\033[25A\033[J")
            sys.stdout.flush()
        self._printed = True
        print(self)
        if delay:
            sleep(delay)

    def check(self, delay=0.0):
        if delay:
            sleep(delay)
        data = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "Zeros", "Ones"],
        ]
        for row in self.rows:
            zeros = len([r for r in row if r.value == 0])
            zeros = f"{RED}{zeros}{RESET}" if not zeros == 6 else f"{GREEN}{zeros}{RESET}"
            ones = len([r for r in row if r.value == 0])
            ones = f"{RED}{ones}{RESET}" if not ones == 6 else f"{GREEN}{ones}{RESET}"
            data.append(row[:] + [zeros, ones])

        zs = []
        os = []
        for column in self.columns:
            zeros = len([r for r in row if r.value == 0])
            zeros = f"{RED}{zeros}{RESET}" if not zeros == 6 else f"{GREEN}{zeros}{RESET}"
            zs.append(zeros)
            ones = len([r for r in row if r.value == 0])
            ones = f"{RED}{ones}{RESET}" if not ones == 6 else f"{GREEN}{ones}{RESET}"
            os.append(ones)

        data.append(zs[:] + ["Zeros"])
        data.append(os[:] + ["Ones"])

        table = SingleTable(data)
        table.inner_heading_row_border = False
        table.inner_row_border = True

        if self._printed:
            sys.stdout.write("\033[31A\033[J")
            sys.stdout.flush()
        self._printed = True

        print(table.table)

    def __str__(self):
        table = SingleTable(self.binary)
        table.inner_row_border = True
        return table.table


binary = [
    [_, _, _, _, 1, _, 1, 1, _, 0, _, _],  # 1
    [_, _, _, 0, _, 0, _, _, 0, _, _, _],  # 2
    [0, _, _, _, _, _, _, _, _, _, _, 0],  # 3
    [_, _, 1, _, _, 0, _, _, _, _, _, 0],  # 4
    [_, _, _, _, 1, _, _, _, _, _, 1, _],  # 5
    [_, _, 1, _, 1, _, _, _, _, 0, _, _],  # 6
    [0, _, _, _, _, _, _, _, _, _, _, _],  # 7
    [_, _, _, 1, 1, _, _, _, _, _, 0, _],  # 8
    [0, _, 0, _, _, 1, _, _, 1, _, 0, 0],  # 9
    [_, 1, _, _, _, 1, _, _, _, _, _, 0],  # 10
    [_, _, _, _, 0, _, _, _, 1, 1, _, _],  # 11
    [1, _, _, 0, 0, _, _, _, _, _, _, 1],  # 12
]

s = BinarySolver(binary)
s.solve()
# s.check()
