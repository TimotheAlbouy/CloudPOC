# Preuve de concept - Confidentialité des données sur le Cloud

Timothé ALBOUY & Youssef EL HOR
INFO2

Aujourd'hui, une part de plus en plus importante de nos données personnelles est stockée sur le cloud. Il est donc légitime de vouloir protéger ces données de personnes malveillantes qui auraient accès à ces serveurs et qui pourraient les lire sans restriction. On pourrait donc penser qu'il suffit de chiffrer ces données avec des clés qu'on garde secrètes avant de les envoyer sur les serveurs, mais cela enlèverait un autre gros avantage du cloud (à part sa capacité de stockage), qui est sa grande puissance de calcul. En effet, on ne pourrait plus effectuer d'opérations comme des additions ou des comparaisons sur des données chiffrées avec des algorithmes classiques comme Triple DES ou AES.

La solution à cette problématique est de se tourner vers des algorithmes cryptographiques qui préservent les propriétés mathématiques des nombres qu'ils chiffrent. Le chiffrement préservant/révélant l'ordre (order-preserving/revealing encryption, OPE/ORE) permet de garder la relation d'ordre sur les chiffrés, et le chiffrement homomorphe (homomorphic encryption, HE) permet d'effectuer des additions et/ou des multiplications sur les chiffrés. À défaut d'avoir un unique algorithme qui permette de tout faire à la fois, il est pour l'instant possible de stocker sur le serveur cloud deux versions différentes d'une donnée : une version chiffrée en OPE, et une autre en HE. Ainsi, quand le client souhaite comparer deux valeurs, le serveur compare les chiffrés en OPE, et quand le client souhaite additionner/multiplier deux valeurs, le serveur additionne/multiplie les deux chiffrés en HE.

Nous avons fait une preuve de concept de ce principe en Python. Pour faire de l'OPE, nous avons utilisé la librairie [pyope de tonyo](https://github.com/tonyo/pyope). Pour faire de l'HE, nous avons utilisé la librairie [phe de data61](https://github.com/data61/python-paillier). Pour se connecter à la base de données MySQL, nous avons utilisé la librairie [MySQL Connector](https://github.com/mysql/mysql-connector-python).
 
Le package `client` contient le fichier `middleware.py` qui contient la classe représentant l'intergiciel côté client, ainsi qu'un fichier `constants.py` qui contient les clés cryptographiques, et enfin le fichier `crypto.py` qui contient les fonctions de chiffrement et déchiffrement.

Le package `server` contient le fichier `middleware.py` qui contient la classe représentant l'intergiciel côté serveur, ainsi qu'un fichier `constants.py` qui contient les informations de connection à la base de données MySQL, et enfin le fichier `crypto.py` qui contient une fonction pour additionner des chiffrés en HE.

Le répertoire `db` contient le script de création de tables et celui de dump de la base de données. On peut y voir qu'on crée une table `encrypted_variable` qui contient une colonne `name` (le nom de la variable, qui est clé primaire), une colonne `ope_cipher` (qui est la valeur de la variable chiffrée en OPE) et une colonne `he_cipher` (qui est la valeur chiffrée en HE de la variable).

Le fichier `scenario.py` contient le code d'un scénario utilisateur qui se déroule comme suit :

- Tout d'abord on crée 3 variables (`salary_alice`, `salary_bob` et `salary_charlie`) initialisées à des valeurs différentes. L'intergiciel côté client chiffre les 3 valeurs en OPE et en HE, puis envoie les noms de variables ainsi que les valeurs chiffrées à l'intergiciel côté serveur qui représente le cloud. Toutes ces informations sont ensuite entrées dans la base de données dans la table `encrypted_variable`.

- On compare ensuite les valeurs des variables `salary_alice` et `salary_bob`. Cette comparaison est faite côté serveur, en comparant les valeurs `ope_cipher` des deux variables dans la table `encrypted_variable`. Normalement, les deux valeurs chiffrées doivent préserver la relation d'ordre, donc leur comparaison doit donner le même résultat que sur les valeurs déchiffrées.

- Après, on met à jour la variable `salary_bob`. Encore une fois, on chiffre la nouvelle valeur de la variable côté client à la fois en OPE et en HE et on envoie ces nouvelles valeurs au côté serveur qui les rentre en base de données.

- On effectue encore une fois la comparaison des deux mêmes variables pour voir si le résultat a changé.

- On additionne ensuite les variables `salary_alice` et `salary_bob` et on stocke le résultat dans la variable `salary_charlie`. L'addition se déroule comme suit : l'intergiciel côté client envoie la requête à l'intergiciel côté serveur d'additionner deux variables chiffrées et de renvoyer le résultat. Les propriétés mathématiques de l'HE garantissent que ce résultat déchiffré sera égal à l'addition des deux valeurs en clair. Une fois qu'on a déchiffré le résultat, on le chiffre en OPE. Après, on met à jour les valeurs en OPE et HE de la variable destination dans la base de données avec les résultats qu'on a obtenus.

- Enfin on supprime toutes les variables créées dans ce scénario. L'intergiciel côté client appelle juste une fonction de l'intergiciel côté serveur en passant en paramètre le nom de la variable à supprimer et celui-ci la supprime de la base de données.

## Notes pour l'utilisation

Pour lancer le scénario sur votre ordinateur, vous devez modifier les constantes de connexion à MySQL que sont l'hôte, le port et le nom de la base de données dans le fichier `server/constants.py`.
