def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if from_base < 2 or from_base > 36:
        return "ERROR"

    if to_base < 2 or to_base > 36:
        return "ERROR"

    number = number.upper()

    for char in number:
        if char not in digits[:from_base]:
            return "ERROR"

    decimal = 0

    for char in number:
        value = digits.index(char)
        decimal = decimal * from_base + value

    if decimal == 0:
        return "0"

    result = ""

    while decimal > 0:
        remainder = decimal % to_base
        result = digits[remainder] + result
        decimal //= to_base

    return result


if __name__ == "__main__":
    print(number_base_converter("1010", 2, 10))
    print(number_base_converter("10", 10, 2))   
    print(number_base_converter("FF", 16, 10)) 
    print(number_base_converter("255", 10, 16))
    print(number_base_converter("Z", 36, 10)) 
    print(number_base_converter("123", 2, 10))