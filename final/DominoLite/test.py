from plateau import *
from tour import Tour
from joueurs import *

import random
import numpy as np
import unittest

class TestDomino(unittest.TestCase):

    def test_Dominos(self):
        "Test du bon nombre de dominos"
        dominos = []
        for dots1 in range(0, 7):
            for dots2 in range(dots1, 7):
                dominos.append([dots1, dots2])
        self.assertEqual(28, len(dominos))

        a = Plateau.generation(7)
        b = Plateau.generation(7)
        "On vérifie le caractère aléatoires des mains & pioche générés"
        self.assertNotEqual(a,b)

        self.assertEqual(len(a),len(b))

    def test_type(self):
        mains = Plateau.generation(7)
        self.assertIsInstance(mains, list)

    """On vérifie que toutes les pièces ont été crées"""
    def test_var(self):
        for i in range(3):
            pieces = Plateau.generation(7)
            verif = []
            for i in range(7):
                for j in range(7):
                    verif.append([i, j])
                    for piece in verif:
                        if piece == [j, i] and j != i:
                            verif.remove(piece)
        for piece in verif:
            if not piece in pieces:
                return False
        return True

    def test_type2(self):
        Tour == Tour

if __name__ == '__main__':
    unittest.main()

