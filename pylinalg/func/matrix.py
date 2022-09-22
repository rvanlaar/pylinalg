from functools import partial, reduce

import numpy as np


matrix_combine = partial(reduce, np.dot)


def matrix_make_translation(vector, dtype="f8"):
    """Make a matrix given a translation vector, or a
    single offset to apply to all axes."""
    vector = np.asarray(vector, dtype=dtype)

    vector = np.atleast_1d(vector)
    if vector.ndim != 1:
        raise NotImplementedError()

    if vector.size == 1:
        vector = np.full((3,), vector[0], dtype=dtype)
    elif vector.shape != (3,):
        raise NotImplementedError()

    matrix = np.identity(4, dtype=dtype)
    matrix[:-1, -1] = vector
    return matrix


def matrix_make_scaling(factors, dtype="f8"):
    """Make a matrix given scaling factors per axis, or a
    single uniform scaling factor."""
    factors = np.asarray(factors, dtype=dtype)

    factors = np.atleast_1d(factors)
    if factors.ndim != 1:
        raise NotImplementedError()

    if factors.size == 1:
        factors = np.full((3,), factors[0], dtype=dtype)
    elif factors.shape != (3,):
        raise NotImplementedError()

    matrix = np.identity(4, dtype=dtype)
    matrix[0, 0] = factors[0]
    matrix[1, 1] = factors[1]
    matrix[2, 2] = factors[2]
    return matrix


def matrix_make_rotation_from_euler_angles(angles, order="xyz", dtype="f8"):
    """Make a matrix given euler angles per axis."""
    angles = np.asarray(angles)
    matrix = {
        "x": np.identity(4, dtype=dtype),
        "y": np.identity(4, dtype=dtype),
        "z": np.identity(4, dtype=dtype),
    }

    matrix["x"][1, 1] = np.cos(angles[0])
    matrix["x"][1, 2] = -np.sin(angles[0])
    matrix["x"][2, 1] = np.sin(angles[0])
    matrix["x"][2, 2] = np.cos(angles[0])

    matrix["y"][0, 0] = np.cos(angles[1])
    matrix["y"][0, 2] = np.sin(angles[1])
    matrix["y"][2, 0] = -np.sin(angles[1])
    matrix["y"][2, 2] = np.cos(angles[1])

    matrix["z"][0, 0] = np.cos(angles[2])
    matrix["z"][0, 1] = -np.sin(angles[2])
    matrix["z"][1, 0] = np.sin(angles[2])
    matrix["z"][1, 1] = np.cos(angles[2])

    return matrix_combine([matrix[i] for i in reversed(order.lower())])
