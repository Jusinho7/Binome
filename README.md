*This project has been created as part of the 42 curriculum by srasolov.*

---

# ft_printf

## Description

`ft_printf` is a partial re-implementation of the standard C `printf` function.
The goal of this project is to understand how variadic functions work in C, and to practice parsing a format string to produce formatted output — without relying on any standard output functions other than `write`.

The function mimics the behavior of `printf` for a defined set of conversion specifiers, and returns the total number of characters written, just like the original.

---

## Instructions

### Compilation

To build the library:

```bash
make
```

This produces `libftprintf.a`.

To compile your project with it:

```bash
cc -Wall -Wextra -Werror main.c libftprintf.a -o my_program
```

### Usage

Include the header in your source file:

```c
#include "ft_printf.h"
```

Then call `ft_printf` just like the standard `printf`:

```c
ft_printf("Hello, %s! You are %d years old.\n", "srasolov", 21);
ft_printf("Pointer: %p | Hex: %x\n", (void *)ptr, 255);
ft_printf("Percent sign: %%\n");
```

---

## Supported Conversions

| Specifier | Description                              |
|-----------|------------------------------------------|
| `%c`      | Single character                         |
| `%s`      | String                                   |
| `%p`      | Pointer address (hexadecimal)            |
| `%d`      | Decimal integer                          |
| `%i`      | Integer (base 10)                        |
| `%u`      | Unsigned decimal integer                 |
| `%x`      | Hexadecimal integer (lowercase)          |
| `%X`      | Hexadecimal integer (uppercase)          |
| `%%`      | Literal percent sign                     |

 Flags (`-`, `0`, `.`, `*`, `#`, `+`, space) are not supported in this version.

---

## Resources

- Linux man page — printf(3)
- cppreference — printf : https://en.cppreference.com/w/c/io/fprintf
- cppreference — va_list / stdarg.h : https://en.cppreference.com/w/c/variadic.html
- codequoi — file : https://www.codequoi.com/manipuler-un-fichier-a-laide-de-son-descripteur-en-c

---

## Algorithm

`ft_printf` works in two steps.

**1. Parsing the format string — `ft_printf`**

The function iterates over the format string character by character. When it encounters a `%` followed by another character, it moves to the next character and passes it to `set_format` for dispatch. Otherwise, it prints the character as-is using `ft_putchar`. A running `count` accumulates the number of characters written and is returned at the end.

**2. Dispatching the specifier — `set_format`**

`set_format` receives the character immediately after `%` and a `va_list` to retrieve the corresponding argument. It maps each specifier to a dedicated output function:

| Specifier | Function called | Notes |
|-----------|----------------|-------|
| `%c` | `ft_putchar` | Argument cast to `int` (C variadic promotion) |
| `%s` | `ft_putstr` | | 
| `%p` | `ft_putptr` | Receives a `void *` |
| `%d`, `%i` | `ft_putnbr` | Signed integer |
| `%u` | `ft_putunsigned` | Unsigned integer |
| `%x` | `ft_puthex` | Lowercase base 16 charset passed as argument |
| `%X` | `ft_puthex` | Uppercase base 16 charset passed as argument |
| `%%` | `write` | Directly writes a literal `%` |

If the character after `%` does not match any specifier, `set_format` returns `0` and nothing is printed.

---

### AI Usage

AI (Claude) was used during this project for the following purposes:

- **Debugging & error correction** — understanding compiler errors (e.g., implicit function declarations, type mismatches) and identifying the root cause of unexpected behavior.

- **Concept comprehension** — clarifying how variadic functions work (`va_list`, `va_start`, `va_arg`, `va_end`), and understanding the relationship between format string parsing and output formatting.

---

No AI was used to generate the actual implementation of the project.
