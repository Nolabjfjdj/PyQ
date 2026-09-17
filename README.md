# PyQ

> **PyQ** est un langage de programmation indépendant, francophone et interprété, créé par **LaBanane415**.

PyQ est conçu comme un véritable langage de programmation avec sa propre syntaxe, son lexer, son parser, son AST et son interpréteur.

Python est utilisé uniquement pour développer l'interpréteur actuel de PyQ. Les programmes PyQ ne sont pas transformés en fichiers Python.

## ✨ Fonctionnalités

PyQ prend actuellement en charge :

- Variables
- Chaînes de caractères
- Nombres entiers
- Opérations mathématiques
- Priorité des opérations
- Parenthèses
- Booléens `vrai` et `faux`
- Comparaisons
- Opérateurs logiques `et`, `ou` et `non`
- Conditions `si`
- Conditions `sinon`
- Blocs avec indentation
- Boucles `tantque`
- Listes
- Listes imbriquées
- Accès aux éléments d'une liste
- Modification des éléments d'une liste
- Fonctions
- Paramètres de fonctions
- Valeurs de retour avec `retourner`
- Fonctions appelées dans des expressions

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
│   ├── tantque.pyq
│   ├── logique.pyq
│   ├── listes.pyq
│   ├── fonctions.pyq
│   └── stress_test.pyq
│
└── pyq/
    ├── __init__.py
    ├── lexer.py
    ├── parser.py
    ├── ast.py
    └── interpreter.py

## 🚀 Utilisation

PyQ fonctionne actuellement avec Python.

Pour exécuter un programme :

    python pyq.py exemples/bonjour.pyq

Exemple :

    afficher("Bonjour le monde !")

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

Les opérations respectent leur priorité :

    afficher(10 + 5 * 2)

Résultat :

    20

Les parenthèses peuvent également être utilisées :

    afficher((10 + 5) * 2)

Résultat :

    30

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

### Conditions

Une condition peut être écrite avec `si` :

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

### Boucles `tantque`

PyQ permet de répéter un bloc tant qu'une condition est vraie :

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

### Listes

PyQ permet de créer des listes :

    nombres = [10, 20, 30, 40]

    afficher(nombres[0])
    afficher(nombres[2])

Les éléments peuvent être modifiés :

    nombres[1] = 50

    afficher(nombres[1])

Les listes peuvent également être imbriquées :

    matrice = [[1, 2], [3, 4]]

    afficher(matrice[0][1])

### Fonctions

PyQ permet de créer des fonctions :

    fonction saluer(nom):
        afficher("Bonjour")
        afficher(nom)

    saluer("Nolan")

Les fonctions peuvent recevoir plusieurs paramètres :

    fonction additionner(a, b):
        retourner a + b

    resultat = additionner(10, 5)

    afficher(resultat)

Les fonctions peuvent retourner une valeur avec `retourner`.

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

- nombres
- chaînes
- identifiants
- opérateurs
- parenthèses
- crochets
- virgules
- deux-points
- nouvelles lignes
- indentation
- désindentation

### Parser

Le parser transforme les tokens en structure logique.

Il permet notamment de construire :

- affectations
- appels de fonctions
- opérations
- comparaisons
- opérations logiques
- listes
- accès aux listes
- conditions
- boucles
- fonctions
- valeurs de retour

### AST

L'AST représente la structure du programme sous forme d'objets.

### Interpréteur

L'interpréteur exécute directement l'AST de PyQ.

PyQ n'est donc pas un simple traducteur de syntaxe vers Python.

## 🎯 Objectif du projet

PyQ est actuellement en développement.

L'objectif est de construire progressivement un langage de programmation complet avec :

- une syntaxe cohérente
- un interpréteur indépendant
- plusieurs types de données
- davantage de structures de contrôle
- des fonctions
- des collections
- une gestion des erreurs
- des modules
- une bibliothèque standard
- et éventuellement son propre environnement d'exécution

## 📌 Version actuelle

**PyQ 0.9**

La version 0.9 ajoute notamment :

- Les fonctions
- Les paramètres
- Les valeurs de retour
- Les fonctions imbriquées dans les expressions
- Les portées locales des fonctions

Les versions précédentes ont notamment introduit :

- Les boucles `tantque`
- Les opérateurs logiques
- Les listes
- Les accès et modifications de listes

## 🚀 Prochaine étape

**PyQ 1.0** sera une étape majeure du développement du langage.

Cette version aura pour objectif de renforcer les fondations de PyQ et d'introduire progressivement de nouvelles fonctionnalités importantes.

## 👤 Auteur

**LaBanane415**

Développement :

**Nolabjfjdj**

## 📄 Licence

Voir le fichier `LICENSE` pour connaître les conditions d'utilisation, de modification et de distribution du projet.