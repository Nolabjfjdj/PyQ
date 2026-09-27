# PyQ

> **PyQ** est un langage de programmation indépendant, francophone et interprété, créé par **LaBanane415**.

PyQ reprend de nombreux concepts de Python tout en proposant une syntaxe française.

L'objectif est simple :

> **Python, mais en français.**

Par exemple, en Python :

    print("Bonjour le monde !")

En PyQ :

    afficher("Bonjour le monde !")

PyQ possède sa propre syntaxe, son propre lexer, son propre parser, son propre AST et son propre interpréteur.

Python est actuellement utilisé uniquement pour développer l'interpréteur de PyQ. Les programmes PyQ ne sont pas transformés en fichiers Python.

## ✨ Fonctionnalités

PyQ prend actuellement en charge :

- Variables
- Chaînes de caractères
- Nombres entiers et décimaux
- Valeur `nul`
- Opérations mathématiques
- Priorité des opérations
- Parenthèses
- Modulo `%`
- Division entière `//`
- Puissance `**`
- Affectations composées `+=`, `-=`, `*=`, `/=`, `%=`, `//=`, `**=`
- Booléens `vrai` et `faux`
- Comparaisons `==`, `!=`, `>`, `<`, `>=`, `<=`
- Opérateurs logiques `et`, `ou` et `non`
- Opérateurs d'appartenance `dans` et `pas dans`
- Opérateurs d'identité `est` et `n'est pas`
- Conditions `si`
- Conditions `sinon`
- Conditions `sinon si`
- Blocs avec indentation
- Boucles `tantque`
- Boucles `pour`
- `interrompre`
- `continuer`
- Listes
- Listes imbriquées
- Dictionnaires
- Dictionnaires imbriqués
- Accès et modification des éléments de listes et dictionnaires
- Indexation des chaînes
- Découpage avec les tranches
- Méthodes de listes
- Méthodes de chaînes
- Fonctions
- Paramètres de fonctions
- Portées locales
- Valeurs de retour avec `retourner`
- Fonctions appelées dans des expressions
- Commentaires avec `#`
- Gestion des erreurs avec `essayer`, `sauf` et `enfin`
- Messages d'erreur d'exécution avec numéro de ligne

## 🚀 Installation

PyQ fonctionne actuellement avec **Python**.

### Windows

#### 1. Installer Python

Télécharge et installe Python depuis :

https://www.python.org/downloads/

Pendant l'installation, active l'option permettant d'ajouter Python au `PATH`.

#### 2. Vérifier Python

Ouvre **CMD** et exécute :

    python --version

Si une version de Python s'affiche, Python est correctement installé.

#### 3. Télécharger PyQ

Dans CMD :

    git clone https://github.com/Nolabjfjdj/PyQ.git

Puis entre dans le dossier :

    cd PyQ

#### 4. Exécuter PyQ

Lance un exemple :

    python pyq.py exemples/bonjour.pyq

Tu devrais obtenir :

    Bonjour le monde !

## ▶️ Exécuter un programme PyQ

Depuis le dossier de PyQ :

    python pyq.py chemin/vers/programme.pyq

Par exemple :

    python pyq.py exemples/bonjour.pyq

Tu peux également créer ton propre fichier `.pyq`.

Exemple :

    nom = "Monde"

    afficher("Bonjour " + nom + " !")

Puis l'exécuter :

    python pyq.py monprogramme.pyq

## 🐍 Python requis

Pour le moment, PyQ utilise Python comme environnement d'exécution de son interpréteur.

Python doit donc être installé pour exécuter PyQ.

À terme, PyQ pourra évoluer vers une installation et une utilisation plus indépendantes.

## 📝 Syntaxe

### Afficher du texte

    afficher("Bonjour le monde !")

### Variables

    nom = "Nolan"

    afficher(nom)

### Calculs

    a = 10
    b = 5

    afficher(a + b)
    afficher(a - b)
    afficher(a * b)
    afficher(a / b)

PyQ prend également en charge :

    afficher(10 % 3)
    afficher(10 // 3)
    afficher(2 ** 8)

Les opérations respectent leur priorité :

    afficher(10 + 5 * 2)

Résultat :

    20

Les parenthèses peuvent également être utilisées :

    afficher((10 + 5) * 2)

Résultat :

    30

### Affectations composées

    nombre = 10

    nombre += 5
    nombre *= 2
    nombre -= 4

    afficher(nombre)

Les opérateurs disponibles sont :

    +=
    -=
    *=
    /=
    %=
    //=
    **=

### Booléens

PyQ utilise :

    vrai
    faux

Exemple :

    afficher(vrai)
    afficher(faux)

Résultat :

    vrai
    faux

### Comparaisons

PyQ prend en charge :

    ==
    !=
    >
    <
    >=
    <=

Exemple :

    age = 14

    afficher(age == 14)
    afficher(age != 10)
    afficher(age > 10)
    afficher(age < 20)
    afficher(age >= 14)
    afficher(age <= 14)

### Opérateurs logiques

PyQ prend en charge :

    et
    ou
    non

Exemple :

    age = 14

    afficher(age >= 13 et age <= 18)
    afficher(age < 10 ou age == 14)

    connecte = faux

    afficher(non connecte)

### Appartenance

    nombres = [10, 20, 30]

    afficher(20 dans nombres)
    afficher(50 pas dans nombres)

### Identité

PyQ prend en charge :

    est
    n'est pas

Exemple :

    valeur = nul

    afficher(valeur est nul)
    afficher(valeur n'est pas nul)

### Conditions

    age = 14

    si age >= 13:
        afficher("Bienvenue")

Les blocs sont définis grâce à l'indentation.

### `sinon`

    age = 10

    si age >= 13:
        afficher("Bienvenue")
    sinon:
        afficher("Trop jeune")

### `sinon si`

    age = 14

    si age >= 18:
        afficher("Majeur")
    sinon si age >= 13:
        afficher("Adolescent")
    sinon:
        afficher("Enfant")

### Boucles `tantque`

    compteur = 1

    tantque compteur <= 5:
        afficher(compteur)
        compteur = compteur + 1

Résultat :

    1
    2
    3
    4
    5

### Boucles `pour`

    nombres = [10, 20, 30]

    pour nombre dans nombres:
        afficher(nombre)

### `interrompre` et `continuer`

    compteur = 0

    tantque compteur < 10:
        compteur += 1

        si compteur == 5:
            interrompre

        si compteur % 2 == 0:
            continuer

        afficher(compteur)

### Listes

    nombres = [10, 20, 30, 40]

    afficher(nombres[0])
    afficher(nombres[2])

Les éléments peuvent être modifiés :

    nombres[1] = 50

    afficher(nombres[1])

Les listes peuvent également être imbriquées :

    matrice = [[1, 2], [3, 4]]

    afficher(matrice[0][1])

### Dictionnaires

    utilisateur = {
        "nom": "Nolan",
        "age": 14
    }

    afficher(utilisateur["nom"])
    afficher(utilisateur["age"])

Les valeurs peuvent être modifiées :

    utilisateur["age"] = 15

    afficher(utilisateur["age"])

Les dictionnaires peuvent également être imbriqués.

### Méthodes de listes

    nombres = [10, 20, 30]

    afficher(nombres.taille())
    nombres.ajouter(40)
    nombres.retirer(20)

### Méthodes de chaînes

    texte = "Bonjour le monde"

    afficher(texte.taille())
    afficher(texte.majuscule())
    afficher(texte.minuscule())
    afficher(texte.titre())
    afficher(texte.inverser())

Les méthodes disponibles incluent notamment :

    taille()
    contient()
    commence_par()
    finit_par()
    majuscule()
    minuscule()
    titre()
    inverser()
    repetitions()
    remplacer()
    separer()
    joindre()

### Indexation et tranches

    nombres = [10, 20, 30, 40, 50]

    afficher(nombres[1:4])
    afficher(nombres[:3])
    afficher(nombres[2:])
    afficher(nombres[::-1])

Les indices négatifs sont également pris en charge.

### Fonctions

    fonction saluer(nom):
        afficher("Bonjour")
        afficher(nom)

    saluer("Nolan")

Les fonctions peuvent recevoir plusieurs paramètres :

    fonction additionner(a, b):
        retourner a + b

    resultat = additionner(10, 5)

    afficher(resultat)

Les fonctions peuvent retourner une valeur avec `retourner` et possèdent leur propre portée locale.

### `nul`

    valeur = nul

    afficher(valeur)
    afficher(valeur est nul)

### Commentaires

    # Ceci est un commentaire
    afficher("Bonjour")

### Gestion des erreurs

PyQ permet de gérer les erreurs d'exécution avec `essayer`, `sauf` et `enfin`.

    essayer:
        nombre = 10 / 0
        afficher(nombre)
    sauf:
        afficher("Une erreur est survenue")
    enfin:
        afficher("Fin du traitement")

Le bloc `sauf` est exécuté lorsqu'une erreur d'exécution survient dans le bloc `essayer`.

Le bloc `enfin` est exécuté à la fin du traitement, qu'une erreur ait eu lieu ou non.

## 🧠 Fonctionnement

PyQ suit une architecture de langage classique :

    Fichier .pyq
         ↓
       Lexer
         ↓
       Tokens
         ↓
       Parser
         ↓
        AST
         ↓
    Interpréteur PyQ
         ↓
       Résultat

### Lexer

Le lexer analyse le code source et le transforme en tokens.

Il gère notamment :

- nombres entiers et décimaux
- chaînes
- identifiants
- opérateurs
- parenthèses
- crochets
- accolades
- virgules
- points
- deux-points
- nouvelles lignes
- indentation
- désindentation
- commentaires

### Parser

Le parser transforme les tokens en structure logique.

Il permet notamment de construire :

- affectations
- affectations composées
- appels de fonctions
- opérations
- comparaisons
- opérations logiques
- opérateurs d'appartenance
- opérateurs d'identité
- listes
- dictionnaires
- accès et modifications par index
- tranches
- appels de méthodes
- conditions
- boucles
- fonctions
- valeurs de retour
- gestion des erreurs

### AST

L'AST représente la structure du programme sous forme d'objets.

Il contient notamment des nœuds pour les expressions, les affectations, les fonctions, les boucles, les conditions et la gestion des erreurs.

### Interpréteur

L'interpréteur exécute directement l'AST de PyQ.

PyQ n'est donc pas un simple traducteur de syntaxe vers Python.

Les erreurs d'exécution sont également converties en erreurs PyQ avec un message et, lorsque cela est possible, le numéro de ligne concerné.

## 📁 Structure du projet

    PyQ/
    ├── README.md
    ├── LICENSE
    ├── pyq.py
    │
    ├── exemples/
    │   ├── bonjour.pyq
    │   ├── nom.pyq
    │   ├── calcul.pyq
    │   ├── comparaisons.pyq
    │   ├── booleens.pyq
    │   ├── conditions.pyq
    │   ├── sinon.pyq
    │   ├── sinon_si.pyq
    │   ├── tantque.pyq
    │   ├── pour.pyq
    │   ├── interrompre_continuer.pyq
    │   ├── logique.pyq
    │   ├── listes.pyq
    │   ├── methodes_listes.pyq
    │   ├── dictionnaires.pyq
    │   ├── fonctions.pyq
    │   ├── commentaires.pyq
    │   ├── decimaux.pyq
    │   ├── nul.pyq
    │   ├── modulo.pyq
    │   ├── division_entiere.pyq
    │   ├── puissance.pyq
    │   ├── affectations.pyq
    │   ├── appartenance.pyq
    │   ├── identite.pyq
    │   ├── slicing.pyq
    │   ├── methodes_chaines.pyq
    │   ├── essayer_sauf_enfin.pyq
    │   └── stress_test.pyq
    │
    └── pyq/
        ├── __init__.py
        ├── lexer.py
        ├── parser.py
        ├── ast.py
        └── interpreter.py

## 🎯 Objectif du projet

PyQ est actuellement en développement.

L'objectif est de construire progressivement un langage de programmation complet avec :

- une syntaxe cohérente
- un interpréteur indépendant
- plusieurs types de données
- des structures de contrôle complètes
- des fonctions
- des collections
- une gestion des erreurs
- des modules
- une bibliothèque standard
- et éventuellement son propre environnement d'exécution

L'objectif à long terme est que PyQ puisse permettre de créer de véritables programmes et des projets importants, et pas uniquement de petits exemples.

## 📌 Version actuelle

**PyQ 0.9**

La version 0.9 continue de renforcer les fondations du langage avec notamment :

- Les nombres décimaux
- `nul`
- Les dictionnaires
- Les méthodes de listes
- Les méthodes de chaînes
- Les tranches
- Le modulo `%`
- La division entière `//`
- La puissance `**`
- Les affectations composées
- Les opérateurs d'appartenance
- Les opérateurs d'identité
- Une gestion plus complète des erreurs
- `essayer`, `sauf` et `enfin`

Les fonctionnalités précédentes comprennent notamment :

- Les variables
- Les opérations mathématiques
- Les booléens
- Les comparaisons
- Les opérateurs logiques
- Les conditions
- Les boucles `tantque`
- Les boucles `pour`
- `interrompre` et `continuer`
- Les listes
- Les fonctions
- Les paramètres
- Les valeurs de retour
- Les commentaires

## 🚀 Prochaine étape

**PyQ 1.0** sera une étape majeure du développement du langage.

Cette version aura pour objectif de continuer à renforcer les fondations de PyQ et d'introduire progressivement les fonctionnalités nécessaires à la création de programmes de plus en plus importants.

## 🤝 Contribution

Les suggestions, retours et contributions sont les bienvenus.

Si vous trouvez un bug, avez une idée de fonctionnalité ou souhaitez discuter de la conception du langage, vous pouvez ouvrir une issue sur GitHub.

## 👤 Auteur

**LaBanane415**

Développement :

**Nolabjfjdj**

## 📄 Licence

Voir le fichier `LICENSE` pour connaître les conditions d'utilisation, de modification et de distribution du projet.