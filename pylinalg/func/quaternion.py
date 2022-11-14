"""Note that we assume unit quaternions for faster implementations"""

import numpy as np


def quaternion_to_matrix(q, out=None):
    x, y, z, w = q
    x2 = x * 2
    y2 = y * 2
    z2 = z * 2
    xx = x * x2
    xy = x * y2
    xz = x * z2
    yy = y * y2
    yz = y * z2
    zz = z * z2
    wx = w * x2
    wy = w * y2
    wz = w * z2

    if out is None:
        out = np.identity(4, dtype=q.dtype)

    out[0, 0] = 1 - (yy + zz)
    out[1, 0] = xy + wz
    out[2, 0] = xz - wy
    out[0, 1] = xy - wz
    out[1, 1] = 1 - (xx + zz)
    out[2, 1] = yz + wx
    out[0, 2] = xz + wy
    out[1, 2] = yz - wx
    out[2, 2] = 1 - (xx + yy)

    return out


def quaternion_multiply_quaternion(a, b, out=None):
    if out is None:
        out = np.empty(4, dtype=a.dtype)

    xyz = a[3] * b[:3] + b[3] * a[:3] + np.cross(a[:3], b[:3])
    w = a[3] * b[3] - a[:3].dot(b[:3])

    out[:3] = xyz
    out[3] = w

    return out


def quaternion_from_unit_vectors(a, b, out=None, dtype=None):
    if out is None:
        out = np.empty(4, dtype=dtype)

    w = 1 + np.dot(a, b)
    xyz = np.cross(a, b)

    out[:3] = xyz
    out[3] = w

    out /= np.linalg.norm(out)

    return out


def quaternion_inverse(q, out=None, dtype=None):
    if out is None:
        out = np.empty_like(q, dtype=dtype)

    out[:] = q
    out[..., :3] *= -1

    return out


def quaternion_from_axis_angle(axis, angle, out=None, dtype=None):
    if out is None:
        out = np.empty(4, dtype=dtype)

    angle_half = angle / 2
    out[:3] = np.asarray(axis) * np.sin(angle_half)
    out[3] = np.cos(angle_half)

    return out
