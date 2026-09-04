def string_sculptor(text: str) -> str:
    res = ""

    for i, char in enumerate(text):
        if i % 2 == 0:
            res += char.lower()
        else:
            res += char.upper()

    return res


if __name__ == "__main__":
    print(string_sculptor("hello"))
    print(string_sculptor("Hello World"))
