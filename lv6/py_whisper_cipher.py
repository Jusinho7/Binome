def whisper_cipher(text: str, shift: int) -> str:
    res = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                char  = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                char  = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
        res += char
    return res


if __name__ == "__main__":
    print(whisper_cipher("hello", 3))
