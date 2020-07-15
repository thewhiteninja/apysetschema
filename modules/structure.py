import ctypes


class MyStructure(ctypes.Structure):

    def __init__(self, data):
        super(MyStructure, self).__init__()
        ctypes.memmove(ctypes.addressof(self), data, ctypes.sizeof(self))

    def __repr__(self):
        values = ",\n".join(f"  {name}={value}" for name, value in self._asdict().items())
        return f"<{self.__class__.__name__}:\n{values}>"

    def _asdict(self):
        return { field[0]: getattr(self, field[0]) for field in self._fields_ }
