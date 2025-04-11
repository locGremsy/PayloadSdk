from enum import Enum

class IntEnumBase(Enum):
    def __int__(self):
        return int(self.value)

class FloatEnumBase(Enum):
    def __float__(self):
        return float(self.value)