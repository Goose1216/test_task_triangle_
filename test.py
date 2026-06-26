class Triangle:

    def __init__(self, symbols, positions):
        self.symbols = symbols
        self.positions = positions

    @classmethod
    def from_reordered(cls, reordered_text, positions):
        return cls(list(reordered_text), list(positions))

    def compress(self):
        while len(self.symbols) >= 4 and self._every_block_is_can_compress():
            self.symbols = [block[0] for block in self._blocks(self.symbols)]
            self.positions = [
                min(block) for block in self._blocks(self.positions)
            ]

    def _every_block_is_can_compress(self):
        return all(
            block == [block[0]] * 4 for block in self._blocks(self.symbols)
        )

    @staticmethod
    def _blocks(items):
        return [items[start:start + 4] for start in range(0, len(items), 4)]

    def __str__(self):
        # Символы расставляются обратно по их позициям во входной строке.
        ordered = sorted(zip(self.positions, self.symbols))
        return "".join(symbol for _, symbol in ordered)


class Reorder:

    def __init__(self, level):
        self.side = 2 ** level

    def positions_in_subtriangle_order(self):
        return self.collect_positions(self.all_cells_with_start_positions(), self.side)

    def all_cells_with_start_positions(self):
        cells = []
        position = 0
        for row in range(self.side):
            for column in range(2 * (self.side - 1 - row), -1, -1):
                cells.append((row, column, position))
                position += 1
        return cells

    def collect_positions(self, cells, side):
        # проход через треугольники в следующем порядке: нижний правый, перевернутый, нижний левый, верхний
        if len(cells) == 1:
            return [cells[0][2]]
        bottom_right, center, bottom_left, top = self.normalize_coordinate(cells, side)
        half = side // 2
        return (
            self.collect_positions(bottom_right, half)
            + self.collect_positions(center, half)
            + self.collect_positions(bottom_left, half)
            + self.collect_positions(top, half)
        )

    @classmethod
    def normalize_coordinate(cls, cells, side):
        half = side // 2
        bottom_right, center, bottom_left, top = [], [], [], []
        for row, column, position in cells:
            if row >= half:
                top.append((row - half, column, position))
                continue
            row_width = 2 * (side - 1 - row) + 1
            wing_width = 2 * (half - 1 - row) + 1
            if column < wing_width:
                bottom_left.append((row, column, position))
            elif column >= row_width - wing_width:
                bottom_right.append(
                    (row, column - (row_width - wing_width), position))
            else:
                # Перевёрнутый центральный треугольник отражается в обычный,
                # чтобы к нему рекурсивно применялось то же разбиение.
                flipped_row = half - 1 - row
                flipped_width = 2 * (half - 1 - flipped_row) + 1
                flipped_column = flipped_width - 1 - (column - wing_width)
                center.append((flipped_row, flipped_column, position))
        return bottom_right, center, bottom_left, top


def calc_level_recurs(length):
    level = 0
    while 4 ** level < length:
        level += 1
    return level


with open("input.txt", encoding="utf-8") as source:
    text = source.read().strip()

reorder = Reorder(calc_level_recurs(len(text)))
positions = reorder.positions_in_subtriangle_order()
reordered_text = "".join(text[position] for position in positions)

triangle = Triangle.from_reordered(reordered_text, positions)
triangle.compress()

with open("output.txt", "w", encoding="utf-8") as output:
    output.write(str(triangle))
