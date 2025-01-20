# projet-2


		Labyrinthe en ray casting 


Le but de ce projet était de créer un code se basant sur la théorie des graphes; Ce code a pour but de créer aléatoirement un labyrinthe puis d’y appliquer des méthodes de chemin minimaux pour y trouver la sortie. 

	Dans notre cas, nous avons décidé de créer un fichier où sont contenues les classes labyrinthe et graphes que nous avons créé grâce à la POO python. La classe graphe est une classe de graphe python concernant les graphes orienté pondéré , les fonctions s’y retrouvant y sont similaires à celles vu en classe. 
	Pour la classe labyrinthe, notre projet initial était de l’afficher dans le terminal et pour cela , on l'affiche à l’aide de la méthode représentation de cette classe , qui utilisait le graphe telle une matrice et indiquait les murs selon un dictionnaire. 
	Mais déjà pour avoir une matrice représentant le labyrinthe il nous fallait construire ce dernier. Pour cela Nous avons pris la liberté de partir sur l’aglorithme growing three explique sur ce blog : https://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm


Cet algorithme marche de la façon suivante , il prend une cellule , la cellule en haut à gauche dans notre cas , puis prend un de ses voisins de façon aléatoire créant un chemin entre les deux, fermant la porte aux autres voisins de la cellule initiale. Il fait cela récursivement jusqu'à obtenir une case sans voisins disponible dès lors il repart en arrière jusqu'à une cellule qui a une cellule voisine , pas dans le chemin , il détruit le mur initialement tracé et reprend l’algorithme a partir de cette cellule. L’algorithme s'arrête lorsqu’il aura parcouru chaque élément du graphe.
	

Puis nous avons décidé d'améliorer notre interface utilisateur avec une interface 3D grâce au ray casting. Le ray casting est une technique de rendu utilisée en informatique pour déterminer quelles parties d'une scène 3D sont visibles depuis une caméra. Elle consiste à lancer des rayons depuis la caméra et à calculer leurs intersections avec les objets de la scène pour simuler la perspective et la profondeur. 
	tous le code de cette partie est contenue dans le code de Main.

Afin de permettre de rendre le jeu le plus compréhensible on retrouve des constantes des jeux vidéo actuelles.: 
la mini-map du labyrinthe indiquant le chemin de dijkstra avec des point bleu se situe en haut à gauche 
Les commandes pour se déplacer sont z,q,s,d
On peut augmenter sa vitesse avec le shift droit et le diminuer avec shift gauche
On peut modifier la FOV avec les flèches directionnelles Haute et bas 
On peut modifier l’angle de la caméra avec les flèches directionnels droite et gauche.
Pour rendre plus simple l'expérience utilisateur , nous avons pris également le parti de colorer le sol en rouge lorsque le joueur parcourt le chemin de dijkstra. 



