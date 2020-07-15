import ctypes

from modules.apisetschemaentry import ApiSetNamespaceEntry, ApiSetNamespaceEntryValue
from modules.structure import MyStructure
from modules.utils import read_string


class StructApiSetValueEntryRedirectionV4(MyStructure):
    _fields_ = [
        ('Flags', ctypes.c_uint32),
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('ValueOffset', ctypes.c_uint32),
        ('ValueLength', ctypes.c_uint32)
    ]


class StructApiSetValueEntryV4(MyStructure):
    _fields_ = [
        ('Flags', ctypes.c_uint32),
        ('NumberOfRedirections', ctypes.c_uint32)
    ]


class StructApiSetNamespaceEntryV4(MyStructure):
    _fields_ = [
        ('Flags', ctypes.c_uint32),
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('AliasOffset', ctypes.c_uint32),
        ('AliasLength', ctypes.c_uint32),
        ('DataOffset', ctypes.c_uint32)
    ]


class StructApiSetNamespaceV4(MyStructure):
    _fields_ = [
        ('Version', ctypes.c_uint32),
        ('Size', ctypes.c_uint32),
        ('Flags', ctypes.c_uint32),
        ('Count', ctypes.c_uint32)
    ]


class ApiSetSchemaV4:

    def __init__(self, data):
        self._data = data
        self._entries = []
        header = StructApiSetNamespaceV4(self._data)
        self._flag = header.Flags
        self._version = header.Version

        self._load_entries(ctypes.sizeof(StructApiSetNamespaceV4), header.Count)

    @property
    def entries(self):
        return self._entries

    def _load_entries(self, offset, count):
        for i in range(count):
            entry_header = StructApiSetNamespaceEntryV4(
                self._data[offset:offset + ctypes.sizeof(StructApiSetNamespaceEntryV4)])

            entry_flags = entry_header.Flags
            entry_name = read_string(self._data, entry_header.NameOffset, entry_header.NameLength)

            entry_values = []

            data_offset = entry_header.DataOffset
            entry_value_header = StructApiSetValueEntryV4(
                self._data[data_offset:data_offset + ctypes.sizeof(StructApiSetValueEntryV4)])

            redirection_offset = ctypes.sizeof(StructApiSetValueEntryV4)
            for j in range(entry_value_header.NumberOfRedirections):
                entry_value_redirection_header = StructApiSetValueEntryRedirectionV4(
                    self._data[data_offset + redirection_offset:data_offset + redirection_offset + ctypes.sizeof(
                        StructApiSetValueEntryRedirectionV4)])

                entry_values.append(ApiSetNamespaceEntryValue(
                    flags=entry_value_redirection_header.Flags,
                    name=read_string(self._data, entry_value_redirection_header.NameOffset, entry_value_redirection_header.NameLength),
                    value=read_string(self._data, entry_value_redirection_header.ValueOffset, entry_value_redirection_header.ValueLength)
                ))
                redirection_offset += ctypes.sizeof(StructApiSetValueEntryRedirectionV4)

            self._entries.append(ApiSetNamespaceEntry(flags=entry_flags, name=entry_name, values=entry_values))

            offset += ctypes.sizeof(StructApiSetNamespaceEntryV4)
