def string_permutation_checker(s1: str, s2: str) -> bool:
    return sorted(s1.replace(" ", "")) == sorted(s2.replace(" ", ""))


if __name__ == "__main__":
    print(string_permutation_checker("abc", "bca"))
    print(string_permutation_checker("abc", "def"))
    print(string_permutation_checker("listen", "silent"))
