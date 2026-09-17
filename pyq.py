"""Point d'entrée temporaire de PyQ."""

import sys
from pathlib import Path

from pyq.translator import traduire_fichier


def main() -> None:
    """Lance le traducteur PyQ."""

    if len(sys.argv) != 2:
        print("Utilisation : python pyq.py <programme.pyq>")
        sys.exit(1)

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"Erreur : le fichier '{source}' n'existe pas.")
        sys.exit(1)

    if source.suffix != ".pyq":
        print("Erreur : le fichier doit avoir l'extension .pyq.")
        sys.exit(1)

    destination = source.with_suffix(".py")

    traduire_fichier(source, destination)

    print(f"PyQ : {source} → {destination}")


if __name__ == "__main__":
    main()