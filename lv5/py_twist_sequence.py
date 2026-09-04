def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return []

    k %= len(arr)
    return arr[-k:] + arr[:-k]


if __name__ == "__main__":
    print(twist_sequence([1, 2, 3, 4, 5], 1))
