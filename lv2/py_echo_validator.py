def echo_validator(text: str) -> bool:
    pile = "".join(i for i in text.lower() if i.isalpha())
    return pile == pile[::-1]


if __name__ == "__main__":
    print(echo_validator("Hello"))
    print(echo_validator("Ka       548138 &      ya    k  "))
