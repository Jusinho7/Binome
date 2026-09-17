def string_sculptor(text: str) -> str:
    res = ""
    n = 0

    for char in text:
        if char == " ":
            n = 0
            res += char
        elif char.isalpha():
            res += char.lower() if n % 2 == 0 else char.upper()
            n += 1
        else:
            res += char

    return res


if __name__ == "__main__":
    print(string_sculptor("hello"))
    print(string_sculptor("Hello World"))
