import sys
try:
    import pygame
except ImportError:
    print("Error")
    sys.exit()


pygame.init()

LARGEUR, HAUTEUR = 1920, 1080
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Visualisation du tri à bulles")
horloge = pygame.time.Clock()

pile = [15, 20, 36, 98, 15, 20, 10, 55, 70, 5]

def tri_bulles(pile):
    n = len(pile)
    for i in range(n):
        for j in range(n - 1 - i):
            if pile[j] > pile[j + 1]:
                pile[j], pile[j + 1] = pile[j + 1], pile[j]
            yield j, j + 1

generateur = tri_bulles(pile)

def dessiner_barres(surface, pile, indices_actifs=()):
    largeur_barre = LARGEUR // len(pile)
    max_valeur = max(pile)
    for idx, valeur in enumerate(pile):
        hauteur = int((valeur / max_valeur) * (HAUTEUR - 40))
        x = idx * largeur_barre
        y = HAUTEUR - hauteur
        couleur = (255, 80, 80) if idx in indices_actifs else (100, 200, 255)
        pygame.draw.rect(surface, couleur, (x, y, largeur_barre - 2, hauteur))

def run(loading = True, finish = False):
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loading = False

        indices_actifs = ()
        if not finish:
            try:
                indices_actifs = next(generateur)
            except StopIteration:
                finish = True

        ecran.fill((20, 20, 20))
        dessiner_barres(ecran, pile, indices_actifs)
        pygame.display.flip()

        horloge.tick(30) 

run()  
pygame.quit()