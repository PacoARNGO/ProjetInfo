import random
import unittest

from plateau import *
import numpy as np
class TestDomino(unittest.TestCase):
    def test_dispoPlateau(self):
        for i in range(3):
            nd = random.randint(0, 28)
            plat = Plateau([[random.randint(0, 7), random.randint(0, 7)] for k in range(nd)], [])
            startIndex = random.randint(0, nd)
            start = plat.plateau[startIndex]
            plat.dispositionPlateau(start)
            for x in range(startIndex, len(plat.plateau) - 1):
                if plat.plateau[x][-1] != plat.plateau[x + 1][0]:
                    return False
            for x in range(startIndex, 0, -1):
                if plat.plateau[x][0] != plat.plateau[x - 1][-1]:
                    return False

    def test_var(self):
        for i in range(3):
            plat = Plateau()
            pieces = plat.generation()
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

if __name__ == "__main__":
    TestDomino.test_dispoPlateau()
    TestDomino.test_var()

