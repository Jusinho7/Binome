*This project has been created as part of the 42 curriculum by srasolov.*

# Libft - Your very first own library

## Description
Libft is the first project in the 42 course. The goal is to recreate a set of functions from the standard C library (libc) as well as additional utility functions. This project provides an in-depth understanding of memory management, pointers, and the manipulation of basic data structures in C.

This library (`libft.a`) will be used as the technical foundation for the majority of future projects within the school.

## Summary
- [Partie 1 : Functions of the Libc](#part-1--functions-of-libc)
- [Partie 2 : Additional functions](#part-2--additional-functions)
- [Partie 3 : Linked lists ](#part-3--linked-lists)
- [Instructions](#instructions)
- [Resources & AI](#ressources--ai)

---

## Library Contents

### Partie 1 - Fonctions de la Libc
Réimplémentation des fonctions standards avec le préfixe `ft_` :
* **Gestion des caractères :** `isalpha`, `isdigit`, `isalnum`, `isascii`, `isprint`, `toupper`, `tolower`.
* **Gestion de la mémoire :** `memset`, `bzero`, `memcpy`, `memmove`, `memchr`, `memcmp`, `calloc`.
* **Gestion des chaînes :** `strlen`, `strlcpy`, `strlcat`, `strchr`, `strrchr`, `strncmp`, `strnstr`, `strdup`.
* **Conversion :** `atoi`.

### Partie 2 - Fonctions supplémentaires
Fonctions non présentes dans la libc standard ou implémentées différemment :
* `ft_substr` : Extrait une sous-chaîne.
* `ft_strjoin` : Concatène deux chaînes.
* `ft_strtrim` : Supprime des caractères spécifiques au début et à la fin d'une chaîne.
* `ft_split` : Découpe une chaîne en tableau de chaînes selon un délimiteur.
* `ft_itoa` : Convertit un entier en chaîne de caractères.
* `ft_strmapi` / `ft_striteri` : Applique une fonction sur chaque caractère d'une chaîne.
* `ft_putchar_fd` / `ft_putstr_fd` / `ft_putendl_fd` / `ft_putnbr_fd` : Sorties sur un descripteur de fichier.

### Partie 3 - Listes chaînées
Utilisation de la structure `t_list` pour manipuler des listes dynamiques :
* `ft_lstnew`, `ft_lstadd_front`, `ft_lstsize`, `ft_lstlast`, `ft_lstadd_back`, `ft_lstdelone`, `ft_lstclear`, `ft_lstiter`, `ft_lstmap`.


---

## Instructions

### Compilation
Le projet utilise un `Makefile` pour la compilation.

1.  **Compiler la bibliothèque :**
    ```bash
    make
    ```
    ```
2.  **Nettoyer les fichiers objets :**
    ```bash
    make clean
    ```
3.  **Nettoyer tout (objets + .a) :**
    ```bash
    make fclean
    ```

### Utilisation
Pour utiliser cette bibliothèque dans un autre projet, inclus le header et lie le fichier `.a` lors de la compilation :
```c
#include "libft.h"
