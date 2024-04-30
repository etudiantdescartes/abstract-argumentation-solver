# Solveur de système d'argumentation abstrait
L'objectif est de trouver diverses structures dans un système d'argumentation abstrait sous forme de graphe.

Le graphe est représenté par une matrice d’adjacence. Les arcs sont représentés par la valeur 1 dans la
matrice, le reste est à 0. Donc pour une matrice M, si M[i,j] = 1, le nœud i attaque le nœud j.

# Ensembles conflict-free
On cherche d’abord les ensembles sans conflit interne parmi toutes les combinaisons de nœuds. On
supprime donc toutes les combinaisons telles que :
- On a au moins une fois le cas : i et j appartiennent à cette combinaison et M[i][j] = 1

# Ensembles admissibles
On cherche ensuite tous les ensembles qui se défendent de leurs attaquants parmi les combinaisons
restantes. On vérifie donc pour chaque ensemble :
- Pour chaque nœud j de l’ensemble à vérifier, pour chaque nœud i du graphe, si i attaque j c’est-
à-dire M[i][j] = 1

  - On vérifie pour chaque nœud k de l’ensemble si M[k][i] = 1. Il suffit que i soit attaqué
  une seule fois par un élément de l’ensemble pour vérifier cette condition.

# Extensions complètes
- Une fonction vérifie si un nœud entré en paramètre est
défendu par un nœud d’un ensemble donné en paramètre, de la même manière que décrit
précédemment.
- Dans une seconde fonction, on appelle la première fonction pour chaque nœud du graphe : si le
nœud est défendu de tous ses attaquants par l’ensemble sans y appartenir, alors on rejette cet
ensemble.
- On peut ensuite appeler la seconde fonction pour chaque combinaison. Ce qui permet de savoir
si la combinaison de nœuds est une extension complète.

# Extensions stables
On définit une fonction permettant de vérifier si une liste passée en paramètre (extensions
complète) attaque tous les nœuds en dehors de cette liste :
- Pour chaque nœud du graphe, s’il n’est pas dans la liste, on vérifie s’il est attaqué par au moins
un nœud de la liste. Si c’est le cas la fonction renvoie True. Il suffit qu’il y ait un seul nœud qui ne
soit pas attaqué par l’ensemble pour sortir de la boucle et rejeter cet ensemble.

# DC-ST / DC-CO
Pour savoir si un argument est crédulement accepté :
- On parcourt la liste des combinaisons en appliquant les fonctions définies précédemment pour
savoir si un ensemble est admissible et une extension complète (dans le cas des extensions
stables, on appelle en plus la fonction associée).
- On regarde ensuite si l’argument est dans l’extension. Si c’est le cas on renvoie YES, sinon, on
continue à parcourir les ensembles.
# SE-ST
Pour trouver une extension stable, la fonction est similaire à celle décrite précédemment, sans la
vérification de la présence d’un argument dans l’extension.
# SE-CO
Pour l’option SE-CO on calcule l’extension grounded :
- On récupère d’abord la liste de tous les nœuds qui ne sont pas attaqués (donc tous les nœuds
dont la somme des éléments de la colonne correspondante dans la matrice est 0).
- On parcourt cette liste et on rejette tous les nœuds attaqués.
- On ajoute ensuite tous les nœuds qui ne sont pas attaqués (et non rejetés) dans la liste des
élément acceptés.
- On répète ces opérations jusqu’à ce que la longueur de la liste des éléments acceptés ne change
plus.
# DS-CO
On regarde d’abord si l’extension grounded est vide : si c’est le cas, on retourne ‘NO’. Sinon, comme
pour les algorithmes utilisés pour DC-ST et DC-CO, on récupère les extensions complètes parmi les
combinaisons de nœuds, si on trouve une extension complète dans laquelle l’argument ne se trouve
pas, on retourne ‘NO’. On retourne ‘YES’ à la fin de la fonction.
# DS-ST
Le principe est le même, en vérifiant si les extensions sont stables. De plus, si on ne trouve pas
d’extension stable, et que l’argument fait bien partie du graphe, on retourne ‘YES’.
