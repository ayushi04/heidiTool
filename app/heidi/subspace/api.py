
from itertools import combinations
import math

from app.heidi.subspace import subspace as sb
from app.utils.decorators import TimingDecorator, DebugDecorator


@TimingDecorator
def getColumnIndexListFromBitVector(bitVector, col):
    return sb.getColumnIndexListFromBitVector(bitVector, col)


@TimingDecorator
def getAllSubspaces(dims):
    return sb.getAllSubspaces(dims)

@TimingDecorator
def getColumnNameListFromBitVector(bitVector, col, all_col_names):
    return sb.getColumnNameListFromBitVector(bitVector, col, all_col_names)

@TimingDecorator
def getAllSubspacesFromSelectedDimensionSet(all_col_names):
    return sb.getAllSubspacesFromSelectedDimensionSet(all_col_names)