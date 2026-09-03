def hidenp(small: str, big: str) -> bool:
    j = 0
    for i in big:
        if j < len(small) and i == small[j]:
            j += 1

    return j == len(small)


if __name__ == "__main__":
    print(hidenp("abc", "a1b2c3"))
    print(hidenp("", "a1b2c3"))
    print(hidenp("ace", "abcde"))
    print(hidenp("aec", "abcde"))
    print(hidenp("abc", "ab"))
    print(hidenp("aaaa", "aaa"))
    print(hidenp("sing","subsequence testing"))
    print(hidenp("aaaa", "AAA"))
