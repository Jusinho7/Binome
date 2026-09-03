def inter(s1: str, s2: str) -> str:
    pile = ""
    for i in s1:
        if i in s2 and i not in pile:
            pile += i
    return pile


if __name__ == "__main__":
    print(inter("hello", "world"))
    print(inter("banana", "band"))
    print(inter("abcabc", "bc"))
    print(inter("abc", "xyz"))
    print(inter("", "abc"))