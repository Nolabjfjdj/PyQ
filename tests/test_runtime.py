import contextlib
import io
import unittest

from pyq.interpreter import Interpreter
from pyq.lexer import Lexer
from pyq.parser import Parser


class PyQRuntimeTests(unittest.TestCase):
    def run_program(self, source):
        output = io.StringIO()
        interpreter = Interpreter()

        with contextlib.redirect_stdout(output):
            tokens = Lexer(source).tokenize()
            program = Parser(tokens).parse()
            interpreter.execute(program)

        return output.getvalue().splitlines()

    def test_try_except_finally(self):
        result = self.run_program(
            "essayer:\n"
            "    valeur = 10 / 0\n"
            "sauf erreur:\n"
            "    afficher(erreur)\n"
            "enfin:\n"
            "    afficher(\"termine\")\n"
        )
        self.assertEqual(result, ["Division par zéro", "termine"])

    def test_type_conversions(self):
        result = self.run_program(
            "afficher(entier(\"42\"))\n"
            "afficher(decimal(\"2.5\"))\n"
            "afficher(texte(12))\n"
            "afficher(booleen(1))\n"
            "afficher(type_de(nul))\n"
        )
        self.assertEqual(result, ["42", "2.5", "12", "vrai", "nul"])

    def test_type_checks(self):
        result = self.run_program(
            "afficher(est_nombre(12))\n"
            "afficher(est_texte(\"PyQ\"))\n"
            "afficher(est_liste([]))\n"
            "afficher(est_tuple((1, 2)))\n"
            "afficher(est_dictionnaire({}))\n"
            "afficher(est_booleen(vrai))\n"
            "afficher(est_nul(nul))\n"
        )
        self.assertEqual(result, ["vrai"] * 7)

    def test_sets(self):
        result = self.run_program(
            "a = ensemble([1, 2, 2, 3])\n"
            "b = ensemble([3, 4])\n"
            "afficher(a.taille())\n"
            "afficher(a.union(b))\n"
            "afficher(a.intersection(b))\n"
            "afficher(a.difference(b))\n"
        )
        self.assertEqual(result, ["3", "{1, 2, 3, 4}", "{3}", "{1, 2}"])


    def test_math_functions(self):
        result = self.run_program(
            "afficher(arrondir(sinus(0), 5))\\n"
            "afficher(arrondir(cosinus(0), 5))\\n"
            "afficher(degres(3.141592653589793))\\n"
            "afficher(radians(180))\\n"
            "afficher(logarithme(100, 10))\\n"
            "afficher(arrondir(exponentielle(1), 5))\\n"
        )
        self.assertEqual(result, ["0", "1", "180", "3.141592653589793", "2", "2.71828"])

    def test_set_display(self):
        result = self.run_program(
            "valeurs = ensemble([3, 1, 2])\\n"
            "afficher(valeurs)\\n"
            "afficher(texte(valeurs))\\n"
        )
        self.assertEqual(result, ["{1, 2, 3}", "{1, 2, 3}"])

    def test_tuple_methods(self):
        result = self.run_program(
            "valeurs = (1, 2, 2, 3)\\n"
            "afficher(valeurs.taille())\\n"
            "afficher(valeurs.compter(2))\\n"
            "afficher(valeurs.position(3))\\n"
            "afficher(valeurs.inverser())\\n"
        )
        self.assertEqual(result, ["4", "2", "3", "(3, 2, 2, 1)"])

    def test_list_and_dictionary_methods(self):
        result = self.run_program(
            "liste = [3, 1, 2]\n"
            "liste.trier()\n"
            "afficher(liste)\n"
            "profil = {\"nom\": \"PyQ\"}\n"
            "afficher(profil.obtenir(\"nom\"))\n"
            "afficher(profil.cles())\n"
        )
        self.assertEqual(result, ["[1, 2, 3]", "PyQ", "[nom]"])


if __name__ == "__main__":
    unittest.main()
