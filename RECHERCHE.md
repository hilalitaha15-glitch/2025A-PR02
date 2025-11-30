Pour intégrer les portails dans mon jeu Pacman, j’ai commencé par créer une fonction qui récupère toutes les cases libres du labyrinthe afin de déterminer où les portails peuvent apparaître. 
Ensuite, j’ai développé une fonction qui choisit aléatoirement deux positions parmi ces cases pour placer les portails.
Au début, j’ai rencontré plusieurs erreurs : la fonction ne retournait rien (ce qui donnait une erreur “NoneType”), et l’initialisation des portails était faite avant la création du layout, ce qui provoquait un “AttributeError”. 
J’ai corrigé ces problèmes en ajoutant un return et en réorganisant l’ordre des initialisations.

Une fois les portails placés, j’ai ajouté la téléportation de Pacman et des fantômes.
J’ai ensuite corrigé un bug où Pacman se téléportait en boucle en ajoutant un système de cooldown de 0,3 seconde.
