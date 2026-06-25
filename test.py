
class Triangle:

    def __init__(self, symbol=None, children=None):
        self.symbol = symbol
        self.children = children

    @classmethod
    def build(cls, segment):
        if segment == segment[0] * len(segment):
            return cls(symbol=segment[0])
        part = len(segment) // 4
        children = [
            cls.build(segment[start:start + part])
            for start in range(0, len(segment), part)
        ]
        head = children[0]
        if head.is_leaf and all(
            child.is_leaf and child.symbol == head.symbol
            for child in children
        ):
            return cls(symbol=head.symbol)
        return cls(children=children)

    @property
    def is_leaf(self):
        return self.children is None

    def __str__(self):
        if self.is_leaf:
            return self.symbol
        return "".join(str(child) for child in self.children)


class Reorder:

    def __init__(self, level):
        self.side = 2 ** level

    def reorder(self, text):
        source_positions = self.collect_possitions(self.all_cells_with_positions(),
                                          self.side)
        return "".join(text[position] for position in source_positions)

    def all_cells_with_positions(self):
        cells = []
        position = 0
        for row in range(self.side):
            for column in range(2 * (self.side - 1 - row), -1, -1): #self.side -1  тк отсчет с нуля
                cells.append((row, column, position))
                position += 1
        return cells

    def collect_possitions(self, cells, side):
        # проход через треугольники в следующем порядке: нижний правый, перевернутый, нижний левый, верхний
        if len(cells) == 1:
            return [cells[0][2]]
        bottom_right, center, bottom_left, top = self.normalize_coordinate(cells, side)
        half = side // 2
        return (
            self.collect_possitions(bottom_right, half)
            + self.collect_possitions(center, half)
            + self.collect_possitions(bottom_left, half)
            + self.collect_possitions(top, half)
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

level_recurs = calc_level_recurs(len(text))
reorder = Reorder(level_recurs)
reorder_text = reorder.reorder(text) # Для удобства взаимодействия с текстом, поменяем порядок символов на тот, с которым мы будем взаимодействовать напрямую
answer_text = Triangle.build(reorder_text)

with open("output.txt", "w", encoding="utf-8") as output:
    output.write(str(answer_text))


