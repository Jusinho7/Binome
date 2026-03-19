*This project has been created as part of the 42 curriculum by srasolov.*

---

# get_next_line

## Description

Get Next Line is a project from the 42 school that involves implementing a function capable of reading a line from a file descriptor. Called several times in succession, this function allows a text file to be read line by line until the end.

- Returns the next line read from file descriptor `fd` (`\n` is included if present)
- Returns `NULL` on end of file or error
- Works with any value of `BUFFER_SIZE` defined at compilation

---

## Instructions

### Compilation
```bash
# Standard version
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c

# Bonus version (multiple file descriptors)
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line_bonus.c get_next_line_utils_bonus.c
```

You can change the value of `BUFFER_SIZE` to suit your needs.

### Usage
```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int     fd;
    char    *line;

    fd = open("file.txt", O_RDONLY);
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

#### Bonus — multiple file descriptors simultaneously
```c
#include "get_next_line_bonus.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int     fd1;
    int     fd2;
    char    *line;

    fd1 = open("file1.txt", O_RDONLY);
    fd2 = open("file2.txt", O_RDONLY);

    line = get_next_line_bonus(fd1); 
    printf("fd1: %s", line); 
    free(line);
    line = get_next_line_bonus(fd2); 
    printf("fd2: %s", line); 
    free(line);
    line = get_next_line_bonus(fd1); 
    printf("fd1: %s", line); 
    free(line);
    line = get_next_line_bonus(fd2); 
    printf("fd2: %s", line); 
    free(line);

    close(fd1);
    close(fd2);
    return (0);
}
```

---

## Algorithm

The implementation is based on **3 main functions** and a static variable `content` which stores the reading surplus between each call.
```
get_next_line(fd)
│
├── 1. Parameter validation (fd < 0, BUFFER_SIZE <= 0)
│
├── 2. red_line(fd, content)  ← fills the content
│   │
│   ├── Allocates a buffer of BUFFER_SIZE + 1
│   ├── Loops read() as long as:
│   │     - no '\n' found in content
│   │     - AND read() returns > 0 (not EOF)
│   ├── Concatenates each read to content (ft_strjoin)
│   └── Returns content (may contain multiple lines)
│
├── 3. set_line(content)  ← extracts the line to return
│   │
│   ├── Scans content until '\n' or '\0'
│   ├── Allocates and copies the line (including '\n')
│   └── Returns the line
│
└── 4. ft_new_line(content)  ← updates the static variable
    │
    ├── Moves past the '\n' in content
    ├── Copies the remainder into a new string
    ├── Frees the old content
    └── Returns the remainder (or NULL if nothing after '\n')
```

### Memory diagram
```
Call 1 :  content = NULL
          read() → "Hello\nWorld\n"
          content = "Hello\nWorld\n"
          set_line    → returns "Hello\n"
          ft_new_line → content = "World\n"

Call 2 :  content = "World\n"  (already in memory, no read())
          set_line    → returns "World\n"
          ft_new_line → content = NULL

Call 3 :  content = NULL → read() → read_size = 0 (EOF)
          → returns NULL
```

---

## Bonus

The bonus version supports **multiple file descriptors simultaneously** using a static array instead of a single static pointer:
```c
static char *content[1024];
```
`1024` represents the maximum number of files that can be open simultaneously on Linux. Since a file descriptor is always a number between `0` and `1023`, `content[fd]` is always a valid index. Each element of the array is a pointer to a string, not a fixed-size buffer.

Each file descriptor has its own independent buffer, so reading from `fd1` and `fd2` alternately does not corrupt either buffer.

### Bonus memory diagram
```
get_next_line_bonus(fd1) → reads from content[fd1]
get_next_line_bonus(fd2) → reads from content[fd2]  (independent)
get_next_line_bonus(fd1) → resumes from content[fd1] (position preserved)
```

---

## Key concepts

| Concept | Description |
|---|---|
| `read()` | Reads the file in chunks of `BUFFER_SIZE` |
| Static variable | Retains the buffer remainder between calls |
| Dynamic allocation | Memory management with `malloc` / `free` |
| File descriptor | Identifier for a file or data stream |
| Static array (bonus) | One buffer per fd, enabling multi-fd support |

---

## Resources

-  [YouTube – Get Next Line explained](https://youtube.com)
-  [42 Cursus Guide – GNL](https://42-cursus.gitbook.io/guide/1-rank-01/get_next_line)
-  [Medium – Simplify your file reading with GNL](https://medium.com/@simonzerisenay/simplify-your-file-reading-with-get-next-line-d3a157da6223)

---

## AI Usage

This project was completed with the assistance of **Claude (Anthropic)** for the following tasks:

- **Debugging & error correction** — Used Claude to help identify and fix issues in the logic of `red_line` and `ft_new_line`, particularly around edge cases (empty files, missing `\n` at EOF, memory leaks)

- **README** — Used Claude to structure, write, and translate this README, including the algorithm diagram and memory diagram

All core logic and implementation were written by the author. AI was used as a support tool, not to generate the project's source code.

---