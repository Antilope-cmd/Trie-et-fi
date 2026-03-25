# 1- Présentation globale du projet:
Lors de l'arrivée du chapitre de NSI sur les algorithmes de tri, beacoups de nos camarades se sont trouvés perplexes quand à leur fonctionnement. Nous nous sommes alors dit s'il il existait des sites webs ou des logiciels **réellements** (et non juste des animations) que nous pouvions utiliser pour rendre ses algorithmes plus intuitifs à tous.

# 2- Organisation du travail
Nous avons étés quatres garçons à travailler sur ce projet: Assad Norat, Bachir Diallo, Vidal Corentin et Jean Brochard. Chacun avait un role particulier. Assad et Corentin on travailler sur l'affichage des histogrammes (ce qui a demandé beacoupo de maths) pour l'utilisateur, tandis que Bachir et Corentin se sont concentré sur l'algorithmie derrière le projet:

- rôle de chacun :
Assad : chef de projet, attribution des tâches
Bachir : Dévvellopeur algorithmique principal
Corentin : Dévellopeur GUI principal
Jean : Documentaliste, bug finder/fixer principal

- répartition : 
Assad : merge sort + reverse list + Dessiner son graphe
management des équipes + repo + GUI
Bachir : quicksort + bogo sort + globals et animations
Jean : selection sort + check list + insertion sort
Corentin : shaker sort + bubble sort + Affichage du canvas + GUI

Nous avons passé un peu près 2 mois sur ce projet.

# 3- Présentation des étapes du projet
Voici, dans un ordre relativement correct, les étapes que nous avons suivi dans la création du projet:
design de l'interface et du projet sur papier
création du repo
création du canva
mise en place des histogrammes
mécanique de mélange de listes
première mécanique d'échange
mise en place du premier tri
amélioration de l'interface
Mise en place des algorithmes récursifs
Mise en place des controles utilisateurs.
devellopement des algorithmes et optimisations...

# 4- Validation de l'opérationnalité du projet:
Lors de la mise en dépôt du projet, le programme était terminé. Pour éviter et vérifier l'abscence de bugs, nous avons préféré garder le code simple et lisible (en majorité) pour faciliter la relecture de notre code. De plus, nous avons gardé notre code de manière segmentée et conteneurisée pour isoler le plus possible les bugs.

Nous avions néanmoins rencontré plusieurs problèmes lors de la mise en place de nos idées:
1. Problème de performances
Le plus gros problème de ce projet était la perte de performence due au fait que le programme trie et affiche en même temps les solutions de tri. C'est alors qu'en abordant le chapitre sur le "multithreading" en python, nous avons pu séparer ces tâches sur deux thread différents.
2. Mise en place de la durée des couleurs
Il a fallu une mesure de temps a utiliser pour savoir quand une couleure doit disparaitre (sinon elle est supprimée instantanément). Nous avons opter pour la création d'une classe "Colorstamp" qui nous a permi de vérifier la "date d'expiration" d'une couleure rattavhée à un histogramme.
3. Représentation sur le canvas
Au tout début du projet, il a fallu que nous nous décidions sur la manière de représenter un triage fait par ordinateur. La solutions d'un graphique à histogramme est venue assez naturellement et a pu être implémentée grâce à une classe personnalisée.
4. Aucune libraire
Nous nous sommes mis au défis de n'utiliser aucune librairie (externe à python) dans ce projet. De cette manière l'installation et le lancement du code devient immédiatement plus facile pour n'importe qui (pas de commande pip dans le terminal). De plus, cette contrainte nous a forcée à redoubler d'ingénieurie lors de difficultées rencontrées.

# 5- ouverture
1. idées d'amélioration:
Pour améliorer ce logiciel, il serait possible d'ajouter plus d'algorithmes de tri (chose très facile à faire grace à la structure de fichier que nous avons mis en place), rendre l'interface plus esthétique, d'optimiser le prgogramme pour trier des graphes encore plus grands ou encore d'utiliser PyQt6 plutôt que tkinhter pour cette application (ce qui la rendrait plus performante).

Nous sommes très satisfaits du travail que nous avons pu fournir, mais le code reste néanmoins assez mal écrit en certains endroits.

Parmis les compétences que ce projet nous a permis de développer, il y a:
-> La maitrise des algorithmes de tri (évidemment)
-> La récursion en informatique
-> La création de Classes.
-> La mise en place d'une interface graphique utilisateur.
-> Une compréhension légèrement plus poussée de l'interpréteur python.

Pour inclure le plus de monde possible et rendre ce logiciel plus accessible, nous avons décider de le mettre en anglais.