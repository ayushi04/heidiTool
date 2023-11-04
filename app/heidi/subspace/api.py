
from itertools import combinations
import math

from app.heidi.subspace import subspace as sb


def getColumnIndexListFromBitVector(bitVector, col):
    return sb.getColumnIndexListFromBitVector(bitVector, col)


def getAllSubspaces(dims):
    return sb.getAllSubspaces(dims)

def getColumnNameListFromBitVector(bitVector, col, all_col_names):
    return sb.getColumnNameListFromBitVector(bitVector, col, all_col_names)

def getAllSubspacesFromSelectedDimensionSet(all_col_names):
    return sb.getAllSubspacesFromSelectedDimensionSet(all_col_names)