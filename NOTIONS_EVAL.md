# Notions à maîtriser pour l'évaluation — A-Maze-ing

Ce document résume les notions clés vues pendant la construction du
projet, pas à pas. Objectif : pouvoir les réexpliquer à voix haute,
sans regarder le code, devant un évaluateur.

---

## 1. Manipulation de bits (format de sortie)

- Chaque cellule est encodée sur **4 bits** : `N=1, E=2, S=4, W=8`
  (bit à 1 = mur **fermé**, bit à 0 = mur **ouvert**).
- Pourquoi 4 bits plutôt que 4 booléens séparés : ça correspond
  directement au format hexadécimal attendu par le sujet, sans
  conversion supplémentaire.
- `&` (ET), `|` (OU), `~` (NON) — opérateurs bit à bit :
  - `x &= ~bit` → **efface** un bit précis (ouvre un mur), laisse
    les autres intacts.
  - `x |= bit` → **force** un bit à 1 (referme un mur), laisse les
    autres intacts.
  - `x & bit` → **teste** si un bit est présent (mur fermé ou non).
- Savoir décoder à la main une valeur comme `13` (`0b1101`) en
  "quels murs sont ouverts/fermés".

## 2. Représentation de la grille

- Convention : `self._walls[y][x]` — **ligne d'abord, colonne
  ensuite**. `(x, y)` sont des coordonnées, `self._walls[y][x]` est
  la valeur stockée à cet endroit (pas la même chose).
- Piège classique : `[[FULLY_CLOSED] * width] * height` crée des
  lignes **partagées** en mémoire (modifier une ligne modifie
  toutes les autres). Il faut une vraie compréhension de liste
  imbriquée : `[[v for _ in range(w)] for _ in range(h)]`.

## 3. Les deux algorithmes principaux

### Backtracker récursif (génération — `_carve_spanning_tree`)
- Structure : une **pile** (`list`, LIFO — dernier entré, premier
  sorti).
- Principe : avancer vers une voisine non visitée au hasard ; si
  aucune voisine libre, reculer (`pop`) — le "backtrack".
- Construit un **arbre couvrant** : jamais de cycle, donc :
  - un seul chemin entre deux cellules quelconques (labyrinthe
    parfait "gratuit"),
  - aucune zone 2×2 (ou plus) totalement ouverte possible.

### BFS (résolution — `shortest_path`)
- Structure : une **file** (`collections.deque`, FIFO — premier
  entré, premier sorti), via `popleft()`/`append()`.
- Principe : explore par vagues de distance croissante depuis le
  départ → garantit de trouver le chemin **le plus court**.
- Le dictionnaire `prev` retient, pour chaque cellule, d'où on
  vient et par quelle direction — permet de reconstruire le chemin
  en remontant de la sortie vers l'entrée (d'où `path.reverse()`
  à la fin).
- Pourquoi `deque` et pas `list` : `list.pop(0)` est lent (décale
  tous les éléments), `deque.popleft()` est rapide des deux côtés.

### Différence clé à savoir expliquer
| | structure | retire | usage |
|---|---|---|---|
| Backtracker | pile (`list`) | fin (`pop()`) | génération |
| BFS | file (`deque`) | début (`popleft()`) | plus court chemin |

## 4. Contrainte "pas de couloir plus large que 2 cellules"

- Un arbre couvrant (backtracker seul) respecte déjà cette règle
  automatiquement (pas de cycle = pas de zone pleinement ouverte).
- `_add_loops` (si `PERFECT=False`) casse la perfection en ouvrant
  des murs supplémentaires, avec le principe **essayer / vérifier
  / annuler** :
  1. `_open_wall(...)` — on ouvre le mur pour de vrai.
  2. `_creates_3x3_open_area(...)` — on vérifie si ça crée une zone
     3×3 totalement ouverte (test sur les 9 fenêtres 3×3 possibles
     autour du point touché).
  3. Si oui → `_close_wall(...)` pour annuler.
- `_window_fully_open(ox, oy)` teste **une seule fenêtre 3×3** : 12
  murs internes à vérifier (6 Est/Ouest + 6 Nord/Sud).

## 5. Le motif "42"

- Un bitmap texte (`"1"`/`"0"`, lignes de caractères) est converti
  en vraies coordonnées de grille via un décalage de centrage :
  `ox = (width - PATTERN_WIDTH) // 2` (idem pour `oy`).
- Chaque `"1"` du bitmap devient une coordonnée `(ox + col_idx,
  oy + row_idx)` ajoutée à `_pattern_cells`.
- Ces cellules sont **exclues du parcours** du backtracker (pas
  juste "dessinées" après coup) — elles restent donc entièrement
  fermées, formant des blocs pleins visuellement : c'est
  l'exception "cellules isolées" prévue par le sujet.

## 6. Mécanismes Python utilisés dans le projet

- **Tuples et indexation** : `t[0]`, `t[2]` — accès positionnel.
- **Dictionnaires imbriqués** : `DIRECTIONS[OPPOSITE[direction]][2]`
  se lit de l'intérieur vers l'extérieur.
- **`enumerate()`** : donne `(indice, valeur)` en parcourant une
  séquence, évite un compteur manuel.
- **`zip()`** : "agrafe" plusieurs séquences ensemble, élément par
  élément ; s'arrête à la plus courte des séquences.
- **`set()` et soustraction d'ensembles** : `a - b` = éléments de
  `a` absents de `b` (utilisé pour détecter des cellules non
  atteintes : `free_cells - visited`).
- **Expression conditionnelle** `A if cond else B` vs `if/else`
  explicite : la forme compacte peut empêcher `mypy --strict` de
  "rétrécir" un type (*type narrowing*), notamment avec des tests
  `in (None, "")` plutôt que `is None`.
- **`@dataclass`** : génère automatiquement `__init__`, `__repr__`,
  `__eq__` à partir de la liste des champs annotés.
- **Convention `_nom`** : underscore = "usage interne", une
  convention (pas une vraie restriction technique en Python).
- **Gestionnaires de contexte** (`with open(...) as handle:`) :
  garantissent la fermeture du fichier même en cas d'erreur.
- **Formatage** : `f"{cell:X}"` (hexadécimal majuscule),
  `f"{raw!r}"` (repr — utile dans les messages d'erreur pour voir
  les espaces ou caractères invisibles).

## 7. Gestion des erreurs

- Exigence du sujet : jamais de crash inattendu, toujours un
  message clair.
- Erreurs **ciblées** dans `main()` : `ConfigError`,
  `MazeGenerationError`, `OSError` — chacune gérée précisément.
- Erreur **large** (`except Exception`) seulement autour de
  l'affichage terminal, avec `# noqa: BLE001` documenté — choix
  assumé pour garantir "jamais de plantage", même si ce n'est pas
  la pratique générale recommandée.

## 8. Architecture générale du projet

- `mazegen/` est un module **indépendant** : il ne connaît ni le
  format de config, ni le format de fichier de sortie, ni
  l'affichage. Livré comme package pip installable séparément
  (`mazegen-*.whl`).
- Flux complet :
  ```
  config.txt → config.py (MazeConfig)
             → mazegen.MazeGenerator (génération + shortest_path)
             → output_writer.py (écrit le fichier)
             → display/ascii_display.py (affichage terminal)
  ```
- `shortest_path()` n'est calculé **qu'une fois** dans le
  générateur ; le fichier de sortie et l'affichage terminal
  consomment tous les deux ce même résultat, sans jamais le
  recalculer chacun de leur côté.

---

## Points à savoir réexpliquer sans regarder le code

1. Comment le backtracker garantit un seul chemin (lien avec
   "arbre couvrant" / absence de cycle).
2. Pourquoi BFS et pas backtracker pour trouver le plus court
   chemin.
3. Comment le motif "42" reste isolé du reste du labyrinthe.
4. La différence pile vs file, et pourquoi chaque algorithme
   utilise la structure qui lui correspond.
5. Le rôle du bit `&`/`|`/`~` dans l'ouverture/fermeture des murs.
