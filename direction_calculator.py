import numpy as np

EAST_VECTOR = (1, 0)

ANGLE_DIRECTION_MAP = {
    0: 'E',
    90: 'N',
    180: 'W',
    270: 'S'
}

ANGLE_TURN_MAP = {
    0: 'straight',
    90: 'right',
    270: 'left'
}

def get_unit_vector(vector):
    return vector / np.linalg.norm(vector)

def get_angle(vector_1, vector_2):
    unit_vector_1 = get_unit_vector(vector_1)
    unit_vector_2 = get_unit_vector(vector_2)

    angle1 = np.arctan2(*unit_vector_1[::-1])
    angle2 = np.arctan2(*unit_vector_2[::-1])

    return np.rad2deg((angle2 - angle1) % (2 * np.pi))

def get_approximate_direction(vector):
    angle = get_angle(EAST_VECTOR, vector)
    return min(ANGLE_DIRECTION_MAP, key=lambda x:abs(x - angle))

def get_turn(vector_1, vector_2):
    current_direction = get_approximate_direction(vector_1)
    next_direction = get_approximate_direction(vector_2)
    difference = current_direction - next_direction

    if difference < 0:
        difference += 360

    return ANGLE_TURN_MAP[difference]