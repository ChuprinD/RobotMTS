from enum import Enum

class Direction(Enum):
    FORWARD = '4'
    BACKWARD = '1'
    LEFT = '2'
    RIGHT = '5'
    RIGHT_45_DEGREES = '3'
    LEFT_45_DEGREES = '6'

    @classmethod
    def get_ordered_directions(cls, data_from_laser):
        return [data_from_laser[cls.FORWARD.value],
                data_from_laser[cls.RIGHT.value],
                data_from_laser[cls.BACKWARD.value],
                data_from_laser[cls.LEFT.value]]