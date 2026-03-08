# 📋 Push_swap — Plan d'implémentation

---

## 🗺️ Flux général

```
argc, argv
    │
    ▼
ft_atol(argv[i])        → convertir string en long
    │
    ├── overflow ?       → Error + exit
    │
    ▼
check_doublon(nums, i)  → vérifier les doublons
    │
    ├── doublon ?        → Error + exit
    │
    ▼
ft_new_node(value)      → créer un noeud
    │
    ▼
add_back(&stack_a, node) → ajouter dans la pile A
    │
    ▼
sort / affichage        → trier et afficher les moves
```

---

## ✅ Déjà implémenté

### 1. Lecture des arguments
```c
// argc = nombre d'arguments
// argv = tableau de strings
// argv[0] = "./push_swap"  → on skip
// argv[1..n] = les nombres → on traite
```

### 2. Conversion string → nombre (`ft_atol`)
```c
// argv[i] = "42"  (string)
//              ↓
// ft_atol  →  42  (long)
// Pourquoi long ? Pour détecter l'overflow avant de caster en int
```

### 3. Vérification des doublons (`check_doublon`)
```c
// argv = ["3", "1", "3"]
//                    ↑
//              doublon détecté → Error
//
// Attention : on convertit D'ABORD en int
// car "1" et "01" sont des doublons mais pas en string !
```

---

## 🔧 À faire

### 4. Création d'un noeud (`ft_new_node`)
```c
// Pour chaque nombre valide → créer un noeud
// node → [ 42 | NULL ]
```

### 5. Ajout dans la pile A (`add_back`)
```c
// Ajouter chaque noeud à la FIN de la pile A
// pour conserver l'ordre des arguments
//
// argv = [3, 1, 4, 2]
//              ↓
// A → [3] → [1] → [4] → [2] ✅
```

### 6. Tri (`sort`)
```c
// ≤ 3 éléments  → sort_small (cas hardcodés)
// ≤ 5 éléments  → sort_five  (pb pb → sort3 → pa pa)
// > 5 éléments  → sort_big   (algorithme de coût)
```

### 7. Affichage des moves
```c
// Chaque opération affiche son nom sur stdout
// ex: "pb\n", "ra\n", "sa\n"...
//
// $ ./push_swap 3 1 4 2
// pb
// ra
// pa
// sa
```

---

## 📊 Résumé

| Étape | Fonction | Status |
|-------|----------|--------|
| Lire les arguments | `argc, argv` | ✅ |
| Convertir en nombre | `ft_atol` | ✅ |
| Vérifier doublons | `check_doublon` | ✅ |
| Créer un noeud | `ft_new_node` | 🔧 À faire |
| Remplir la pile A | `add_back` | 🔧 À faire |
| Trier | `sort_small / sort_big` | 🔧 À faire |
| Afficher les moves | `write` dans chaque op | 🔧 À faire |
