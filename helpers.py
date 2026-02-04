from math import sqrt, pow


def calc_angle_diff(target_ang, current_ang):
    return (target_ang - current_ang + 180) % 360 - 180


def calc_distance_two_boids(one, other):
    return sqrt(
        pow(one.position[0] - other.position[0], 2)
        + pow(one.position[1] - other.position[1], 2)
    )


def normalize(vector):
    return vector.normalize() if vector.length_squared() > 0 else vector
