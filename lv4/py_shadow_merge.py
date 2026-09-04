def shadow_merge(list1: list[int], list2: list[int]) -> list[int]:
    pile = []
    for i in list1:
        pile.append(i)
    for i in list2:
        pile.append(i)
    res = sorted(pile)
    return res


if __name__ == "__main__":
    print(shadow_merge([1, 3, 5], [2, 4, 6]))
    print(shadow_merge([1,2,3], [4,5,6]))
    print(shadow_merge([], [1,2,3]))
    print(shadow_merge([1,1,2], [1,3,3]))
