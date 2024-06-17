# Date: 2023-9-25   
# Version: 1.0
# Test cases for getSubspaceListFromBitVector() function in app/mod_dim/createHeidi.py

import sys
sys.path.insert(0, '/Users/ayushigupta/Desktop/github/tq/TOOL')

import pytest
from heidi.matrix.subspace import getSubspaceListFromBitVector

# Positive test cases
def test_getSubspaceListFromBitVector_positive():
    # Test case with a subspace of 5 and column size of 8
    assert getSubspaceListFromBitVector(5, 8) == [0, 2]
    # Test case with a subspace of 10 and column size of 16
    assert getSubspaceListFromBitVector(10, 16) == [1, 3]
    # Test case with a subspace of 15 and column size of 32
    assert getSubspaceListFromBitVector(15, 32) == [0, 1, 2, 3]
    # Test case with a subspace of 11 and column size of 4
    assert getSubspaceListFromBitVector(11, 4) == [0, 1, 3]
    # Test case with a subspace of 12 and column size of 4
    assert getSubspaceListFromBitVector(14, 4) == [1, 2, 3]
    

# Edge test cases
def test_getSubspaceListFromBitVector_edge():
    # Test case with a subspace of 1 and column size of 1
    assert getSubspaceListFromBitVector(1, 1) == [0]
    # Test case with a subspace of 2 and column size of 2
    assert getSubspaceListFromBitVector(2, 2) == [1]
    # Test case with a subspace of 31 and column size of 32
    assert getSubspaceListFromBitVector(31, 32) == [0, 1, 2, 3, 4]
