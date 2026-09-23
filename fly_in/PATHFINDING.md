# Pathfinding dans Fly-in

Ce document explique comment fonctionne le système de pathfinding du projet et pourquoi le solveur est conçu de cette manière.

## 1. Objectif

Le but n’est pas seulement de trouver un itinéraire du hub de départ au hub d’arrivée, mais aussi de le faire en respectant :

- les contraintes de capacité des zones
- les contraintes de capacité des connexions
- les coûts de retard des zones restreintes
- le mouvement simultané de plusieurs drones
- l’évitement des impasses et la gestion des goulots d’étranglement

En bref, le projet est un problème de routage temporel, plus qu’un simple problème de plus court chemin dans un graphe.

## 2. Modèle de carte

L’environnement est représenté comme un graphe :

- une `Zone` est un nœud contenant un nom, des coordonnées, un type et un nombre maximum de drones
- une `Connection` est une arête reliant deux zones
- un `DroneMap` stocke le graphe complet, la zone de départ, la zone d’arrivée et les métadonnées des drones

Chaque zone peut avoir un type différent :

- `normal` : coût de déplacement standard
- `restricted` : coût de déplacement plus lent (2 tours)
- `blocked` : impossible à traverser
- `priority` : peut être traité spécialement selon certaines stratégies

## 3. Pourquoi l’algorithme A* standard ne suffit pas

Un A* classique ne trouve qu’un chemin spatial le plus court.

Ce n’est pas suffisant pour Fly-in, car le problème est dynamique :

- un drone ne peut arriver dans une zone que si cette zone a encore de la capacité à ce moment-là
- une connexion ne peut être utilisée que si elle n’est pas saturée pendant la fenêtre de temps considérée
- une zone restreinte peut nécessiter plusieurs tours pour être traversée
- plusieurs drones se disputent les mêmes goulots d’étranglement

Le solveur doit donc raisonner en fonction du temps, et pas seulement de l’espace.

## 4. Espace d’états temporels

Le pathfinder utilise un état de la forme :

```python
(zone_name, turn)
```

Cela signifie que l’algorithme ne cherche plus seulement une zone, mais une position à un moment précis de la simulation.

C’est indispensable, car la même zone peut être valide au tour 5 mais pas au tour 6 si elle est pleine.

## 5. Système de réservation

Le solveur conserve deux structures de réservation :

- `zone_reservations` : nombre de drones déjà affectés à une zone à un tour donné
- `connection_reservations` : nombre de drones déjà affectés à une connexion à un tour donné

Ces réservations servent à éviter les collisions et les surcharges.

Lorsqu’un drone planifie un déplacement :

1. il vérifie si la zone de destination est toujours disponible au moment d’arrivée
2. il vérifie si la connexion utilisée est disponible à chaque étape du mouvement
3. il enregistre la réservation pour que les drones suivants évitent le même conflit

## 6. Heuristique utilisée

L’algorithme utilise une heuristique basée sur une estimation de distance inversée depuis la destination.

Cela donne une estimation du coût restant, ce qui permet au moteur de recherche de privilégier les chemins qui semblent prometteurs tout en tenant compte des contraintes.

L’heuristique est mise en cache pour éviter de recalculer les mêmes estimations de distance à répétition.

## 7. La boucle de recherche

Le pathfinder est implémenté avec une file de priorité (`heapq`).

Chaque état candidat contient :

- un coût total estimé
- le coût actuel du chemin
- le tour actuel
- l’état lui-même

À chaque itération :

1. on extrait l’état le plus prometteur
2. on ignore les entrées obsolètes
3. on teste l’option d’attente
4. on essaie toutes les connexions voisines
5. on valide les contraintes de temps, de capacité et d’occupation
6. on enregistre le meilleur coût connu pour le nouvel état
7. on réinjecte le nouvel état dans la frontière

C’est le schéma classique de l’A*, adapté à un graphe avec réservations.

## 8. Pourquoi l’attente est modélisée

L’attente est cruciale.

Un drone peut être contraint de retarder son déplacement parce que :

- la prochaine zone est pleine
- une zone restreinte n’est pas encore disponible
- une liaison est saturée à ce moment

L’algorithme inclut une transition d’attente dans le graphe des états. Cela lui permet de trouver des plans valides et globalement faisables, même quand un itinéraire direct est temporairement bloqué.

## 9. Zones restreintes et coût de mouvement

Les zones restreintes sont spéciales car elles coûtent deux tours au lieu d’un.

Cela signifie qu’un drone entrant dans une zone restreinte ne dépense pas seulement une unité de temps ; il réserve aussi la destination pour un tour d’arrivée plus tard et maintient le transit bloqué pendant la durée du mouvement.

C’est l’une des principales raisons pour lesquelles un simple algorithme de plus court chemin échoue sur les cartes plus difficiles.

## 10. Stratégie spécifique au challenger

La carte finale du projet, `01_the_impossible_dream.txt`, est volontairement conçue comme un test de stress. Le solveur générique fonctionne déjà, mais la carte défi peut créer de graves goulots d’étranglement.

Pour améliorer la performance sur cette carte, le projet introduit un biais spécifique au domaine dans le score de priorité :

- les routes passant par des couloirs très encombrés sont pénalisées
- des couloirs plus sûrs ou plus équilibrés sont privilégiés
- le solveur pousse les drones vers des branches moins saturées lorsque plusieurs routes valides existent

Cela ne remplace pas la logique centrale de réservation ; il améliore uniquement la sélection des routes lorsque de nombreuses solutions sont techniquement valides, mais qu’une partie d’entre elles est nettement meilleure que les autres.

## 11. Pourquoi le système est robuste

La logique de pathfinding est robuste parce qu’elle combine :

- la recherche dans un graphe
- la modélisation des états en fonction du temps
- le suivi des réservations
- la validation des capacités
- le guidage par l’heuristique
- un biais spécifique pour les scénarios difficiles

Cela le rend adapté à la fois aux cartes standards et aux cartes défi, tout en conservant la validité sous des contraintes de concurrence.

## 12. Résumé

Le pathfinding du projet n’est pas un simple solveur de plus court chemin. C’est un planificateur temporel contraint qui calcule des itinéraires sûrs en respectant l’occupation des zones et des goulots d’étranglement.

Les idées principales sont :

- modéliser le monde comme un graphe
- raisonner en états `(zone, tour)`
- réserver de la capacité sur les zones et les liens
- utiliser l’A* avec une heuristique temporelle
- gérer explicitement l’attente et les transports restreints
- ajouter un biais spécifique aux cartes les plus difficiles

C’est ce qui rend la simulation à la fois réaliste et capable de résoudre des cartes personnalisées difficiles.
