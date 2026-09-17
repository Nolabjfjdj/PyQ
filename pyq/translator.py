"""Traducteur de code PyQ vers Python."""

from pathlib import Path


MOTS_PYQ = {
    "afficher": "print",
}


def traduire(code: str) -> str:
    """Traduit du code PyQ en code Python."""

    for mot_pyq, mot_python in MOTS_PYQ.items():
        code = code.replace(mot_pyq, mot_python)

    return code


def traduire_fichier(source: Path, destination: Path) -> None:
    """Traduit un fichier .pyq en fichier Python."""

    code_pyq = source.read_text(encoding="utf-8")
    code_python = traduire(code_pyq)

    destination.write_text(code_python, encoding="utf-8")