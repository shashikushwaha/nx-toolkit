import math

import pytest
from nxopenkit.maths.matrix3x3 import Matrix3X3

class TestMatrix3X3:
    
    def test_matrix3X3_initialization(self):
        matrix = Matrix3X3(
            1, 2, 3,
            4, 5, 6,
            7, 8, 9
        )
        assert matrix.Xx == 1
        assert matrix.Xy == 2
        assert matrix.Xz == 3
        assert matrix.Yx == 4
        assert matrix.Yy == 5
        assert matrix.Yz == 6
        assert matrix.Zx == 7
        assert matrix.Zy == 8
        assert matrix.Zz == 9

    def test_matrix3X3_equality(self):
        matrix1 = Matrix3X3(
            1, 2, 3,
            4, 5, 6,
            7, 8, 9
        )
        matrix2 = Matrix3X3(
            1, 2, 3,
            4, 5, 6,
            7, 8, 9
        )
        assert matrix1 == matrix2