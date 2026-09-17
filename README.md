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
- Conditions `si`
- Conditions `sinon`
- Blocs avec indentation
- Boucles `tantque`
- Fonction `afficher()`

## 📁 Structure du projet

PyQ/
├── README.md
├── pyq.py
│
├── exemples/
│   ├── bonjour.pyq
│   ├── nom.pyq
│   ├── calcul.pyq
│   ├── comparaisons.pyq
│   ├── booleens.pyq
│   ├── conditions.pyq
│   └── tantque.pyq
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

PyQ permet également de répéter un bloc tant qu'une condition est vraie :

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
- conditions
- boucles

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
- davantage de types de données
- davantage de structures de contrôle
- des fonctions
- des collections
- une gestion des erreurs
- des modules
- une bibliothèque standard
- et éventuellement son propre environnement d'exécution

## 📌 Version actuelle

**PyQ 0.6**

Cette version ajoute notamment :

- les boucles `tantque`
- les modifications de variables
- l'exécution répétée de blocs

## 👤 Auteur

**LaBanane415**

Développement :

**Nolabjfjdj**

## 📄 Licence

Le projet est actuellement en développement.

Les conditions de distribution et la licence du projet pourront être définies ultérieurement.