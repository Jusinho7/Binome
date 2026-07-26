_DIGIT_4 = (
    "10010",
    "10010",
    "10010",
    "11111",
    "00010",
    "00010",
    "00010",
)

_DIGIT_2 = (
    "11110",
    "00001",
    "00001",
    "01110",
    "10000",
    "10000",
    "11111",
)


def build_pattern(gap: int = 1) -> list[str]:
    rows: list[str] = []
    spacer = "0" * gap
    for row4, row2 in zip(_DIGIT_4, _DIGIT_2):
        rows.append(row4 + spacer + row2)
    return rows


PATTERN_42: list[str] = build_pattern()
PATTERN_HEIGHT: int = len(PATTERN_42)
PATTERN_WIDTH: int = len(PATTERN_42[0])
