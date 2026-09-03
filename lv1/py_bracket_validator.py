def bracket_validator(s: str) -> bool:
    pairs = {
        '}': '{',
        ']': '[',
        ')': '('
    }
    pile = []
    opened = set(pairs.values())
    closed = set(pairs.keys())

    for i in s:
        if i in opened:
            pile.append(i)

        elif i in closed:
            if not pile or pile.pop() != pairs[i]:
                return False
    return len(pile) == 0


if __name__ == "__main__":
    print(bracket_validator("(Hello)"))
