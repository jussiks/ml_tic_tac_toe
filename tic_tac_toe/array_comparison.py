# -*- coding: utf-8 -*-

import numpy as np


def are_sqr_arrays_equal(array1, array2):
    # Checks if two arrays are equal
    ndarray1 = np.array(array1)
    ndarray2 = np.array(array2)

    if len(ndarray1.shape) != 2 or len(ndarray2.shape) != 2:
        raise ValueError("Arrays must be two dimensional.")

    if ndarray1.shape[0] != ndarray1.shape[1] or ndarray2.shape[0] != ndarray2.shape[1]:
        raise ValueError("Arrays must be square arrays.")

    alternatives = generate_equal_arrays(ndarray2)
    return next(
        (True for x in alternatives if np.array_equal(x, ndarray1)), False)


def generate_equal_arrays(array):
    array = np.array(array)

    if len(array.shape) != 2:
        raise ValueError("Array must be two dimensional.")

    if array.shape[0] != array.shape[1]:
        raise ValueError("Array must be a square array.")

    for i in range(2):
        for j in range(4):
            array = rotate(array)
            yield array
        array = reflect(array)


def rotate(arr, turns=1):
    arr = np.array(arr)
    for i in range(turns):
        arr = np.rot90(arr)
    return arr


def reflect(arr):
    # Mirrors the array
    return np.fliplr(arr)
