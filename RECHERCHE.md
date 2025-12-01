Pour intégrer les portails dans mon jeu Pacman, j’ai commencé par créer une fonction qui récupère toutes les cases libres du labyrinthe afin de déterminer où les portails peuvent apparaître. 
Ensuite, j’ai développé une fonction qui choisit aléatoirement deux positions parmi ces cases pour placer les portails.
Au début, j’ai rencontré plusieurs erreurs : la fonction ne retournait rien (ce qui donnait une erreur “NoneType”), et l’initialisation des portails était faite avant la création du layout, ce qui provoquait un “AttributeError”. 
J’ai corrigé ces problèmes en ajoutant un return et en réorganisant l’ordre des initialisations.

Une fois les portails placés, j’ai ajouté la téléportation de Pacman et des fantômes.
J’ai ensuite corrigé un bug où Pacman se téléportait en boucle en ajoutant un système de cooldown de 0,3 seconde.

Dans game.py, j’ai ajouté l’appel à la téléportation dans la boucle d’update :

self.maze.handle_portal_teleport(self.pacman)
for ghost in self.ghosts:
    self.maze.handle_portal_teleport(ghost)

Ces lignes permettent à Pacman et aux fantômes d’être téléportés automatiquement lorsqu’ils touchent un portail.

Égalment l'ajout de self.last_teleport_time = 0 qui permet d'enregistrer le moment où l’objet a été téléporté pour la dernière fois, et elle permet au cooldown de fonctionner.
