# PyQ

> **PyQ** est un langage de programmation indépendant, francophone et interprété, créé par **LaBanane415**.

PyQ propose une manière de programmer inspirée de Python, mais avec une syntaxe pensée pour le français.

PyQ possède sa propre syntaxe, son lexer, son parser, son AST et son interpréteur.

Python est actuellement utilisé pour développer l'interpréteur de PyQ. Les programmes PyQ ne sont pas transformés en fichiers Python.

## ✨ Pourquoi PyQ ?

PyQ a été créé avec une idée simple :

> Et si on pouvait programmer avec une syntaxe proche de Python, mais entièrement adaptée au français ?

Par exemple :

Python :

    if age >= 18:
        print("Majeur")

PyQ :

    si age >= 18:
        afficher("Majeur")

L'objectif de PyQ est de rendre certains concepts de programmation plus accessibles aux francophones tout en construisant un véritable langage de programmation indépendant.

## 🚀 Fonctionnalités

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
- Affectations composées
- Booléens `vrai` et `faux`
- Comparaisons
- Opérateurs logiques `et`, `ou` et `non`
- Opérateurs d'appartenance `dans` et `pas dans`
- Opérateurs d'identité `est` et `n'est pas`
- Conditions `si`, `sinon` et `sinon si`
- Blocs avec indentation
- Boucles `tantque`
- Boucles `pour`
- `interrompre`
- `continuer`
- Listes
- Listes imbriquées
- Dictionnaires
- Dictionnaires imbriqués
- Accès et modification des éléments
- Indexation
- Tranches
- Méthodes de listes
- Méthodes de chaînes
- Fonctions
- Paramètres de fonctions
- Portées locales
- Valeurs de retour avec `retourner`
- Fonctions utilisées dans des expressions
- Commentaires avec `#`
- Gestion des erreurs avec `essayer`, `sauf` et `enfin`
- Messages d'erreur d'exécution avec numéro de ligne

## 📦 Installation

PyQ fonctionne actuellement avec Python.

### 1. Installer Python

Installe Python depuis le site officiel :

https://www.python.org/downloads/

Pendant l'installation de Python sous Windows, il est recommandé d'activer l'option permettant d'ajouter Python au PATH.

### 2. Vérifier l'installation

Ouvre l'invite de commandes Windows et exécute :

    python --version

Si Python est correctement installé, une version de Python sera affichée.

### 3. Télécharger PyQ

Avec Git installé, clone le dépôt :

    git clone https://github.com/Nolabjfjdj/PyQ.git

Puis entre dans le dossier :

    cd PyQ

### 4. Exécuter un premier programme

Lance l'exemple fourni avec PyQ :

    python pyq.py exemples/bonjour.pyq

Tu peux ensuite créer tes propres fichiers `.pyq`.

Pour exécuter un programme :

    python pyq.py chemin/vers/programme.pyq

## 🧪 Premier programme

Crée un fichier appelé `bonjour.pyq` :

    afficher("Bonjour le monde !")

Puis exécute-le avec :

    python pyq.py bonjour.pyq

## 📚 Documentation

La documentation complète de PyQ explique le langage progressivement, avec des exemples et des explications sur son fonctionnement.

**[→ Lire la documentation complète](documentation.md)**

La documentation contient notamment :

- Les bases du langage
- Les variables
- Les types de données
- Les calculs
- Les conditions
- Les boucles
- Les listes
- Les dictionnaires
- Les chaînes de caractères
- Les fonctions
- Les opérateurs
- Les erreurs
- La gestion des erreurs
- La syntaxe complète de PyQ
- Le fonctionnement interne du langage

## 📁 Structure du projet

    PyQ/
    ├── README.md
    ├── documentation.md
    ├── LICENSE
    ├── pyq.py
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
    └── pyq/
        ├── __init__.py
        ├── lexer.py
        ├── parser.py
        ├── ast.py
        └── interpreter.py

## 🧠 Fonctionnement

PyQ suit une architecture classique de langage interprété :

    Programme .pyq
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

Le lexer analyse le code source et produit des tokens.

Le parser transforme ces tokens en structure logique.

L'AST représente cette structure sous forme d'objets.

Enfin, l'interpréteur exécute directement cette structure.

PyQ n'est donc pas simplement un programme qui traduit du code PyQ en Python.

## 🎯 Objectif

PyQ est actuellement en développement.

L'objectif est de construire progressivement un langage de programmation francophone complet, avec une syntaxe cohérente et suffisamment de fonctionnalités pour créer de véritables programmes.

À long terme, le projet pourra évoluer avec notamment :

- davantage de types de données
- davantage de structures de contrôle
- des modules
- une bibliothèque standard
- davantage d'outils pour les développeurs
- un environnement d'exécution plus complet

## 📌 Version actuelle

**PyQ 0.9**

PyQ 0.9 continue de renforcer les fondations du langage avec notamment les nombres décimaux, `nul`, les dictionnaires, les méthodes de listes et de chaînes, les tranches, les affectations composées, les opérateurs d'appartenance et d'identité ainsi qu'une gestion plus complète des erreurs.

## 🚀 Prochaine étape

**PyQ 1.0** sera une étape importante du développement du langage.

L'objectif est de continuer à consolider les fonctionnalités existantes et de préparer PyQ à accueillir des programmes de plus en plus complets.

## 👤 Auteur

**LaBanane415**

Développement :

**Nolabjfjdj**

## 📄 Licence

PyQ est distribué sous licence MIT.

**[→ Consulter la licence complète](LICENSE)**

## 📚 Documentation complète

**[→ Apprendre PyQ et consulter la référence du langage](documentation.md)**