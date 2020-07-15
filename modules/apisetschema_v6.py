import ctypes

from modules.apisetschemaentry import ApiSetNamespaceEntry, ApiSetNamespaceEntryValue
from modules.structure import MyStructure
from modules.utils import read_string


class StructApiSetHashEntryV6(MyStructure):
    _fields_ = [
        ('Hash', ctypes.c_uint32),
        ('Index', ctypes.c_uint32)
    ]


class StructApiSetNamespaceEntryV6(MyStructure):
    _fields_ = [
        ('Flags', ctypes.c_uint32),
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('HashedLength', ctypes.c_uint32),
        ('ValueOffset', ctypes.c_uint32),
        ('ValueCount', ctypes.c_uint32)
    ]


class StructApiSetValueEntryV6(MyStructure):
    _fields_ = [
        ('Flags', ctypes.c_uint32),
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('ValueOffset', ctypes.c_uint32),
        ('ValueLength', ctypes.c_uint32)
    ]


class StructApiSetNamespaceV6(MyStructure):
    _fields_ = [
        ('Version', ctypes.c_uint32),
        ('Size', ctypes.c_uint32),
        ('Flags', ctypes.c_uint32),
        ('Count', ctypes.c_uint32),
        ('EntryOffset', ctypes.c_uint32),
        ('HashOffset', ctypes.c_uint32),
        ('HashFactor', ctypes.c_uint32)
    ]


class ApiSetSchemaV6:

    def __init__(self, data):
        self._data = data
        self._entries = []

        header = StructApiSetNamespaceV6(self._data)
        self._flag = header.Flags
        self._version = header.Version

        self._load_entries(header.EntryOffset, header.Count)

    @property
    def entries(self):
        return self._entries

    def _load_entries(self, offset, count):
        for i in range(count):
            entry_header = StructApiSetNamespaceEntryV6(
                self._data[offset:offset + ctypes.sizeof(StructApiSetNamespaceEntryV6)])

            entry_flags = entry_header.Flags
            entry_name = read_string(self._data, entry_header.NameOffset, entry_header.NameLength)
            entry_values = []

            value_offset = entry_header.ValueOffset
            for j in range(entry_header.ValueCount):
                entry_value_header = StructApiSetValueEntryV6(
                    self._data[value_offset:value_offset + ctypes.sizeof(StructApiSetValueEntryV6)])

                entry_values.append(ApiSetNamespaceEntryValue(
                    flags=entry_value_header.Flags,
                    name=read_string(self._data, entry_value_header.NameOffset, entry_value_header.NameLength),
                    value=read_string(self._data, entry_value_header.ValueOffset, entry_value_header.ValueLength)
                ))

                value_offset += ctypes.sizeof(StructApiSetValueEntryV6)

            self._entries.append(ApiSetNamespaceEntry(name=entry_name, values=entry_values, flags=entry_flags))

            offset += ctypes.sizeof(StructApiSetNamespaceEntryV6)
