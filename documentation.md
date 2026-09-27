# Documentation PyQ

Bienvenue dans la documentation officielle de **PyQ**.

PyQ est un langage de programmation indépendant, francophone et interprété, créé par **LaBanane415**.

Son objectif est de proposer une syntaxe inspirée de Python, mais adaptée au français.

Cette documentation présente progressivement les bases du langage, ses principales fonctionnalités et sa syntaxe.

---

# Sommaire

1. [Qu'est-ce que PyQ ?](#quest-ce-que-pyq-)
2. [Installation](#installation)
3. [Premier programme](#premier-programme)
4. [Afficher du texte](#afficher-du-texte)
5. [Variables](#variables)
6. [Types de données](#types-de-données)
7. [Nombres et calculs](#nombres-et-calculs)
8. [Affectations composées](#affectations-composées)
9. [Booléens](#booléens)
10. [Comparaisons](#comparaisons)
11. [Opérateurs logiques](#opérateurs-logiques)
12. [Opérateurs d'appartenance](#opérateurs-dappartenance)
13. [Opérateurs d'identité](#opérateurs-didentité)
14. [Conditions](#conditions)
15. [Boucles `tantque`](#boucles-tantque)
16. [Boucles `pour`](#boucles-pour)
17. [`interrompre` et `continuer`](#interrompre-et-continuer)
18. [Listes](#listes)
19. [Dictionnaires](#dictionnaires)
20. [Indexation](#indexation)
21. [Tranches](#tranches)
22. [Méthodes de listes](#méthodes-de-listes)
23. [Chaînes de caractères](#chaînes-de-caractères)
24. [Méthodes de chaînes](#méthodes-de-chaînes)
25. [Fonctions](#fonctions)
26. [Paramètres](#paramètres)
27. [Portées locales](#portées-locales)
28. [`retourner`](#retourner)
29. [`nul`](#nul)
30. [Commentaires](#commentaires)
31. [Gestion des erreurs](#gestion-des-erreurs)
32. [Messages d'erreur](#messages-derreur)
33. [Combiner plusieurs fonctionnalités](#combiner-plusieurs-fonctionnalités)
34. [Architecture de PyQ](#architecture-de-pyq)
35. [Référence rapide](#référence-rapide)
36. [Version actuelle](#version-actuelle)

---

# Qu'est-ce que PyQ ?

PyQ est un langage de programmation indépendant écrit pour permettre de programmer avec une syntaxe francophone.

L'idée générale est simple :

**Python possède une syntaxe principalement en anglais. PyQ reprend plusieurs concepts familiers de la programmation de style Python, mais les exprime en français.**

Par exemple :

Python :

    if age >= 18:
        print("Majeur")

PyQ :

    si age >= 18:
        afficher("Majeur")

PyQ n'est pas un traducteur qui transforme automatiquement un programme Python en programme PyQ.

PyQ possède son propre lexer, son propre parser, sa propre représentation AST et son propre interpréteur.

Python sert actuellement à implémenter l'interpréteur de PyQ.

---

# Installation

## Windows

PyQ nécessite actuellement Python pour être exécuté.

### Installer Python

Télécharge Python depuis le site officiel :

https://www.python.org/downloads/

Pendant l'installation, active l'option permettant d'ajouter Python au PATH.

### Vérifier Python

Ouvre l'invite de commandes Windows et exécute :

    python --version

Une version de Python doit être affichée.

### Télécharger PyQ

Avec Git installé :

    git clone https://github.com/Nolabjfjdj/PyQ.git

Puis :

    cd PyQ

### Exécuter PyQ

Lance un exemple :

    python pyq.py exemples/bonjour.pyq

---

# Premier programme

Le programme PyQ le plus simple consiste à afficher du texte.

    afficher("Bonjour le monde !")

Enregistre ce programme dans un fichier portant l'extension `.pyq`.

Par exemple :

    bonjour.pyq

Puis exécute-le :

    python pyq.py bonjour.pyq

Le résultat sera :

    Bonjour le monde !

---

# Afficher du texte

PyQ utilise `afficher()` pour afficher une valeur.

    afficher("Bonjour")
    afficher("Bienvenue sur PyQ")

Une variable peut également être affichée :

    nom = "Nolan"
    afficher(nom)

Une expression peut également être utilisée :

    afficher(10 + 5)

Résultat :

    15

---

# Variables

Une variable permet de stocker une valeur.

    nom = "Nolan"
    age = 14

Une variable peut ensuite être utilisée :

    afficher(nom)
    afficher(age)

Une variable peut également être modifiée :

    age = 14
    age = 15

    afficher(age)

Résultat :

    15

Il n'est pas nécessaire d'écrire un mot-clé particulier pour créer une variable.

---

# Types de données

PyQ prend actuellement en charge plusieurs types de valeurs.

## Chaînes

Une chaîne contient du texte.

    nom = "Nolan"

## Entiers

Un entier est un nombre sans partie décimale.

    age = 14

## Nombres décimaux

PyQ prend également en charge les nombres décimaux.

    prix = 12.5

## Booléens

PyQ possède deux valeurs booléennes :

    vrai
    faux

## `nul`

`nul` représente une absence de valeur.

    valeur = nul

Les types et comportements disponibles peuvent évoluer avec le développement du langage.

---

# Nombres et calculs

PyQ permet d'effectuer des opérations mathématiques.

## Addition

    afficher(10 + 5)

Résultat :

    15

## Soustraction

    afficher(10 - 5)

Résultat :

    5

## Multiplication

    afficher(10 * 5)

Résultat :

    50

## Division

    afficher(10 / 5)

Résultat :

    2

## Modulo

Le modulo `%` permet d'obtenir le reste d'une division.

    afficher(10 % 3)

Résultat :

    1

## Division entière

L'opérateur `//` permet d'effectuer une division entière.

    afficher(10 // 3)

Résultat :

    3

## Puissance

L'opérateur `**` permet d'effectuer une puissance.

    afficher(2 ** 3)

Résultat :

    8

---

# Priorité des opérations

PyQ respecte la priorité des opérations.

    afficher(10 + 5 * 2)

Résultat :

    20

La multiplication est effectuée avant l'addition.

Les parenthèses permettent de modifier cette priorité :

    afficher((10 + 5) * 2)

Résultat :

    30

---

# Affectations composées

PyQ permet de modifier une variable avec des opérateurs composés.

    nombre = 10

    nombre += 5
    nombre -= 2
    nombre *= 3
    nombre /= 2
    nombre %= 4
    nombre //= 2
    nombre **= 2

Les opérateurs disponibles sont :

    +=
    -=
    *=
    /=
    %=
    //=
    **=

Par exemple :

    score = 10
    score += 5

    afficher(score)

Résultat :

    15

---

# Booléens

Les booléens représentent une valeur vraie ou fausse.

PyQ utilise :

    vrai
    faux

Exemple :

    connecte = vrai

    afficher(connecte)

Ou :

    connecte = faux

    afficher(connecte)

Les booléens sont particulièrement utiles avec les conditions.

---

# Comparaisons

Les comparaisons permettent de vérifier une relation entre deux valeurs.

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

Les résultats d'une comparaison sont des valeurs booléennes.

---

# Opérateurs logiques

PyQ utilise les opérateurs français :

    et
    ou
    non

## `et`

`et` permet de vérifier que plusieurs conditions sont vraies.

    age = 14

    afficher(age >= 13 et age <= 18)

## `ou`

`ou` permet d'accepter plusieurs possibilités.

    age = 14

    afficher(age < 10 ou age == 14)

## `non`

`non` inverse une valeur booléenne.

    connecte = faux

    afficher(non connecte)

---

# Opérateurs d'appartenance

PyQ possède les opérateurs :

    dans
    pas dans

Ils permettent de vérifier si une valeur est présente dans une collection ou une chaîne.

Exemple avec une liste :

    nombres = [10, 20, 30]

    afficher(20 dans nombres)
    afficher(50 pas dans nombres)

Exemple avec une chaîne :

    texte = "Bonjour"

    afficher("jour" dans texte)

---

# Opérateurs d'identité

PyQ possède les opérateurs :

    est
    n'est pas

Ils peuvent notamment être utilisés avec `nul`.

    valeur = nul

    afficher(valeur est nul)
    afficher(valeur n'est pas nul)

---

# Conditions

Les conditions permettent au programme de prendre des décisions.

PyQ utilise `si`.

Exemple :

    age = 18

    si age >= 18:
        afficher("Majeur")

Le bloc appartenant à la condition est défini grâce à l'indentation.

---

# `sinon`

`sinon` permet d'exécuter un autre bloc lorsque la condition précédente est fausse.

    age = 10

    si age >= 18:
        afficher("Majeur")
    sinon:
        afficher("Mineur")

---

# `sinon si`

Plusieurs conditions peuvent être enchaînées avec `sinon si`.

    age = 14

    si age >= 18:
        afficher("Majeur")
    sinon si age >= 13:
        afficher("Adolescent")
    sinon:
        afficher("Enfant")

PyQ teste les conditions dans l'ordre.

---

# Indentation

L'indentation est importante dans PyQ.

Elle permet de déterminer quelles instructions appartiennent à un bloc.

    age = 18

    si age >= 18:
        afficher("Majeur")

L'instruction `afficher()` appartient au bloc de la condition grâce à son indentation.

Cette organisation est utilisée pour les conditions, les boucles, les fonctions et les structures similaires.

---

# Boucles `tantque`

Une boucle `tantque` répète un bloc tant qu'une condition est vraie.

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

Il faut faire attention à ce que la condition puisse finalement devenir fausse.

---

# Boucles `pour`

Une boucle `pour` permet de parcourir les éléments d'une collection.

    nombres = [10, 20, 30]

    pour nombre dans nombres:
        afficher(nombre)

Résultat :

    10
    20
    30

---

# `interrompre` et `continuer`

## `interrompre`

`interrompre` permet de quitter immédiatement une boucle.

    compteur = 0

    tantque compteur < 10:
        compteur += 1

        si compteur == 5:
            interrompre

        afficher(compteur)

La boucle s'arrête lorsque `compteur` atteint 5.

## `continuer`

`continuer` permet de passer directement à l'itération suivante.

    compteur = 0

    tantque compteur < 5:
        compteur += 1

        si compteur == 3:
            continuer

        afficher(compteur)

---

# Listes

Une liste permet de stocker plusieurs valeurs.

    nombres = [10, 20, 30, 40]

On peut accéder à un élément avec son index.

    afficher(nombres[0])

Résultat :

    10

Les index commencent à zéro.

Ainsi :

    nombres[0]

correspond au premier élément.

    nombres[1]

correspond au deuxième élément.

---

# Modifier une liste

Les éléments d'une liste peuvent être modifiés.

    nombres = [10, 20, 30]

    nombres[1] = 50

    afficher(nombres[1])

Résultat :

    50

---

# Listes imbriquées

Une liste peut contenir d'autres listes.

    matrice = [[1, 2], [3, 4]]

On peut accéder à plusieurs niveaux :

    afficher(matrice[0][1])

Résultat :

    2

---

# Dictionnaires

Un dictionnaire permet d'associer des clés à des valeurs.

    utilisateur = {
        "nom": "Nolan",
        "age": 14
    }

On peut accéder à une valeur grâce à sa clé :

    afficher(utilisateur["nom"])
    afficher(utilisateur["age"])

---

# Modifier un dictionnaire

Une valeur peut être modifiée :

    utilisateur = {
        "nom": "Nolan",
        "age": 14
    }

    utilisateur["age"] = 15

    afficher(utilisateur["age"])

---

# Dictionnaires imbriqués

Les dictionnaires peuvent contenir d'autres dictionnaires.

    utilisateur = {
        "nom": "Nolan",
        "profil": {
            "niveau": 3
        }
    }

L'accès aux valeurs imbriquées peut être réalisé avec plusieurs indexations.

---

# Indexation

L'indexation permet d'accéder à un élément précis d'une liste ou d'une chaîne.

Avec une liste :

    nombres = [10, 20, 30]

    afficher(nombres[0])
    afficher(nombres[1])
    afficher(nombres[2])

Avec une chaîne :

    texte = "Bonjour"

    afficher(texte[0])

Les indices négatifs sont également pris en charge.

---

# Tranches

Les tranches permettent d'extraire une partie d'une liste ou d'une chaîne.

Exemple :

    nombres = [10, 20, 30, 40, 50]

    afficher(nombres[1:4])

Autres formes :

    afficher(nombres[:3])
    afficher(nombres[2:])
    afficher(nombres[::-1])

Les tranches permettent notamment de sélectionner une partie d'une collection ou de l'inverser.

---

# Méthodes de listes

PyQ fournit des méthodes permettant de manipuler les listes.

Exemple :

    nombres = [10, 20, 30]

    afficher(nombres.taille())

Pour ajouter une valeur :

    nombres.ajouter(40)

Pour retirer une valeur :

    nombres.retirer(20)

Ces méthodes permettent de modifier ou d'interroger les listes sans devoir gérer manuellement toutes les opérations.

---

# Chaînes de caractères

Les chaînes de caractères permettent de stocker du texte.

    message = "Bonjour le monde"

    afficher(message)

Une chaîne peut être utilisée dans une expression ou stockée dans une variable.

---

# Méthodes de chaînes

PyQ fournit plusieurs méthodes pour manipuler les chaînes.

Exemple :

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

Ces méthodes permettent d'effectuer différentes opérations sur du texte.

---

# Fonctions

Une fonction permet de regrouper des instructions afin de pouvoir les réutiliser.

PyQ utilise le mot-clé `fonction`.

    fonction saluer():
        afficher("Bonjour")

Une fonction peut ensuite être appelée :

    saluer()

---

# Paramètres

Une fonction peut recevoir des paramètres.

    fonction saluer(nom):
        afficher("Bonjour")
        afficher(nom)

Appel :

    saluer("Nolan")

Une fonction peut avoir plusieurs paramètres :

    fonction additionner(a, b):
        afficher(a + b)

    additionner(10, 5)

---

# Portées locales

Les fonctions possèdent leur propre portée locale.

Une variable créée à l'intérieur d'une fonction peut donc appartenir à cette fonction plutôt qu'au programme global.

Exemple :

    fonction test():
        message = "Bonjour"
        afficher(message)

    test()

La portée locale permet d'éviter que toutes les variables utilisées dans une fonction deviennent automatiquement des variables globales.

---

# `retourner`

Une fonction peut renvoyer une valeur avec `retourner`.

    fonction additionner(a, b):
        retourner a + b

La valeur retournée peut être stockée :

    resultat = additionner(10, 5)

    afficher(resultat)

Résultat :

    15

Une fonction peut également être appelée directement dans une expression.

---

# Fonctions dans les expressions

Une fonction qui retourne une valeur peut être utilisée dans une expression.

    fonction doubler(nombre):
        retourner nombre * 2

    resultat = doubler(5) + 10

    afficher(resultat)

Résultat :

    20

---

# `nul`

`nul` représente une absence de valeur.

    valeur = nul

    afficher(valeur)

Il peut également être utilisé dans une comparaison :

    valeur = nul

    afficher(valeur est nul)

---

# Commentaires

Les commentaires commencent avec `#`.

Exemple :

    # Ceci est un commentaire
    afficher("Bonjour")

Un commentaire permet d'écrire une information destinée aux personnes qui lisent le code.

Le commentaire n'est pas exécuté comme une instruction.

---

# Gestion des erreurs

PyQ permet de gérer certaines erreurs d'exécution avec :

    essayer
    sauf
    enfin

Exemple :

    essayer:
        nombre = 10 / 0
        afficher(nombre)
    sauf:
        afficher("Une erreur est survenue")
    enfin:
        afficher("Fin du traitement")

Si une erreur survient dans le bloc `essayer`, le bloc `sauf` peut être exécuté.

Le bloc `enfin` est exécuté à la fin du traitement.

---

# Messages d'erreur

PyQ fournit des messages d'erreur d'exécution qui peuvent notamment indiquer le numéro de ligne concerné.

Cela permet de trouver plus facilement l'endroit où le programme rencontre un problème.

Lorsqu'une erreur apparaît, il est recommandé de regarder :

1. le numéro de ligne indiqué ;
2. l'instruction présente sur cette ligne ;
3. les valeurs utilisées ;
4. la structure du bloc concerné ;
5. les lignes précédentes qui peuvent avoir modifié une variable.

---

# Combiner plusieurs fonctionnalités

Les fonctionnalités de PyQ peuvent être combinées.

Par exemple, une liste peut être parcourue avec une boucle et une condition peut être utilisée à l'intérieur.

    nombres = [1, 2, 3, 4, 5]

    pour nombre dans nombres:
        si nombre % 2 == 0:
            afficher(nombre)

Résultat :

    2
    4

Les fonctions peuvent également utiliser des listes, des conditions et des boucles.

    fonction afficher_pairs(nombres):
        pour nombre dans nombres:
            si nombre % 2 == 0:
                afficher(nombre)

    valeurs = [1, 2, 3, 4, 5, 6]

    afficher_pairs(valeurs)

---

# Créer un petit programme

Un programme PyQ peut combiner plusieurs fonctionnalités.

Exemple :

    fonction verifier_age(age):
        si age >= 18:
            retourner "Majeur"
        sinon si age >= 13:
            retourner "Adolescent"
        sinon:
            retourner "Enfant"

    ages = [8, 14, 20]

    pour age dans ages:
        resultat = verifier_age(age)
        afficher(resultat)

Ce programme utilise :

- une fonction ;
- un paramètre ;
- `retourner` ;
- plusieurs conditions ;
- une liste ;
- une boucle `pour` ;
- des variables ;
- `afficher()`.

---

# Architecture de PyQ

PyQ suit une architecture classique pour un langage interprété.

Le chemin général est :

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
    Interpréteur
         ↓
       Résultat

---

# Lexer

Le lexer analyse le texte du programme.

Il transforme le code source en une suite de tokens.

Un token représente une unité reconnue du langage.

Le lexer de PyQ prend notamment en compte :

- les nombres ;
- les chaînes ;
- les identifiants ;
- les opérateurs ;
- les parenthèses ;
- les crochets ;
- les accolades ;
- les virgules ;
- les points ;
- les deux-points ;
- les nouvelles lignes ;
- l'indentation ;
- la désindentation ;
- les commentaires.

---

# Parser

Le parser reçoit les tokens produits par le lexer.

Il construit ensuite une représentation structurée du programme.

Le parser prend notamment en charge les constructions correspondant aux fonctionnalités du langage :

- affectations ;
- affectations composées ;
- expressions ;
- appels de fonctions ;
- comparaisons ;
- opérations logiques ;
- opérateurs d'appartenance ;
- opérateurs d'identité ;
- listes ;
- dictionnaires ;
- indexation ;
- tranches ;
- méthodes ;
- conditions ;
- boucles ;
- fonctions ;
- valeurs de retour ;
- gestion des erreurs.

---

# AST

AST signifie **Abstract Syntax Tree**, ou arbre syntaxique abstrait.

L'AST représente la structure logique du programme.

Au lieu de manipuler directement le texte original, l'interpréteur peut travailler avec cette structure.

Cela permet notamment de distinguer les différentes parties d'un programme :

- expressions ;
- valeurs ;
- variables ;
- affectations ;
- conditions ;
- boucles ;
- fonctions ;
- appels ;
- retours ;
- gestion des erreurs.

---

# Interpréteur

L'interpréteur exécute directement l'AST de PyQ.

Le programme `.pyq` n'est donc pas converti en programme Python avant son exécution.

Python sert actuellement d'environnement d'implémentation de l'interpréteur.

Cette distinction est importante :

**PyQ est le langage.**

**Python est actuellement utilisé pour construire son interpréteur.**

---

# Python et PyQ

PyQ s'inspire de nombreux concepts familiers de Python, mais PyQ n'est pas Python traduit mot à mot.

Quelques correspondances courantes :

| Python | PyQ |
|---|---|
| `print()` | `afficher()` |
| `if` | `si` |
| `elif` | `sinon si` |
| `else` | `sinon` |
| `while` | `tantque` |
| `for` | `pour` |
| `in` | `dans` |
| `not` | `non` |
| `and` | `et` |
| `or` | `ou` |
| `True` | `vrai` |
| `False` | `faux` |
| `None` | `nul` |
| `return` | `retourner` |
| `def` | `fonction` |
| `break` | `interrompre` |
| `continue` | `continuer` |
| `try` | `essayer` |
| `except` | `sauf` |
| `finally` | `enfin` |

Cette table sert à comprendre l'idée générale de PyQ.

PyQ possède néanmoins son propre fonctionnement interne.

---

# Référence rapide

## Affichage

    afficher(valeur)

## Variable

    nom = valeur

## Condition

    si condition:
        instructions

## Sinon

    sinon:
        instructions

## Sinon si

    sinon si condition:
        instructions

## Boucle

    tantque condition:
        instructions

## Parcours

    pour element dans collection:
        instructions

## Fonction

    fonction nom(parametre):
        instructions

## Retour

    retourner valeur

## Liste

    valeurs = [1, 2, 3]

## Dictionnaire

    donnees = {
        "nom": "Nolan"
    }

## Commentaire

    # commentaire

## Gestion des erreurs

    essayer:
        instructions
    sauf:
        instructions
    enfin:
        instructions

---

# Conseils pour apprendre PyQ

Si tu débutes complètement en programmation, il est recommandé de suivre cet ordre :

1. Afficher du texte
2. Variables
3. Types de données
4. Calculs
5. Comparaisons
6. Booléens
7. Conditions
8. Boucles
9. Listes
10. Dictionnaires
11. Chaînes de caractères
12. Fonctions
13. Valeurs de retour
14. Gestion des erreurs

Ne cherche pas forcément à tout apprendre immédiatement.

Commence par écrire de petits programmes.

Par exemple :

    nom = "Nolan"
    age = 14

    si age >= 13:
        afficher("Bonjour")
        afficher(nom)

Puis ajoute progressivement des fonctionnalités.

---

# Exemples disponibles

Le dépôt PyQ contient plusieurs exemples permettant d'expérimenter différentes fonctionnalités.

Ils se trouvent dans le dossier :

    exemples/

On y trouve notamment des exemples concernant :

- les variables ;
- les calculs ;
- les comparaisons ;
- les booléens ;
- les conditions ;
- les boucles ;
- les listes ;
- les dictionnaires ;
- les fonctions ;
- les commentaires ;
- les nombres décimaux ;
- `nul` ;
- les opérateurs ;
- les tranches ;
- les méthodes de chaînes ;
- la gestion des erreurs.

Pour tester un exemple :

    python pyq.py exemples/nom_du_fichier.pyq

---

# Limites actuelles

PyQ est encore en développement.

Certaines fonctionnalités présentes dans des langages plus complets peuvent ne pas encore être disponibles.

La syntaxe et les fonctionnalités peuvent également évoluer entre les versions.

La documentation doit donc être considérée comme la référence correspondant à la version actuelle du langage.

---

# Version actuelle

**PyQ 0.9**

La version 0.9 contient notamment :

- nombres décimaux ;
- `nul` ;
- dictionnaires ;
- méthodes de listes ;
- méthodes de chaînes ;
- tranches ;
- modulo ;
- division entière ;
- puissance ;
- affectations composées ;
- opérateurs d'appartenance ;
- opérateurs d'identité ;
- gestion des erreurs ;
- `essayer`, `sauf` et `enfin`.

Les fonctionnalités précédentes du langage comprennent notamment :

- variables ;
- opérations mathématiques ;
- booléens ;
- comparaisons ;
- opérateurs logiques ;
- conditions ;
- boucles `tantque` ;
- boucles `pour` ;
- `interrompre` ;
- `continuer` ;
- listes ;
- fonctions ;
- paramètres ;
- valeurs de retour ;
- commentaires.

---

# PyQ 1.0

PyQ 1.0 sera une étape importante du développement du langage.

L'objectif est de consolider les fonctionnalités existantes et de continuer à construire les bases nécessaires à des programmes plus importants.

Les fonctionnalités prévues peuvent évoluer pendant le développement.

---

# À propos du projet

PyQ est un projet indépendant créé par **LaBanane415**.

Le développement est réalisé sous l'identité GitHub **Nolabjfjdj**.

L'objectif du projet est de construire progressivement un langage de programmation francophone possédant sa propre syntaxe et son propre interpréteur.

PyQ est un projet en développement et sa syntaxe peut continuer à évoluer.

---

# Licence

PyQ est distribué sous licence MIT.

La licence complète se trouve dans le fichier :

    LICENSE

---

# Documentation

Cette documentation a pour objectif d'expliquer PyQ de manière simple tout en servant de référence pour la syntaxe et les fonctionnalités actuellement disponibles.

Lorsque le langage évolue, cette documentation peut être mise à jour afin de correspondre aux nouvelles versions de PyQ.