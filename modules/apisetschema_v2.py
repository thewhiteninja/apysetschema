import ctypes

from modules.apisetschemaentry import ApiSetNamespaceEntryValue, ApiSetNamespaceEntry
from modules.structure import MyStructure
from modules.utils import read_string


class StructApiSetValueEntryRedirectionV2(MyStructure):
    _fields_ = [
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('ValueOffset', ctypes.c_uint32),
        ('ValueLength', ctypes.c_uint32)
    ]


class StructApiSetValueEntryV2(MyStructure):
    _fields_ = [
        ('NumberOfRedirections', ctypes.c_uint32)
    ]


class StructApiSetNamespaceEntryV2(MyStructure):
    _fields_ = [
        ('NameOffset', ctypes.c_uint32),
        ('NameLength', ctypes.c_uint32),
        ('DataOffset', ctypes.c_uint32)
    ]


class StructApiSetNamespaceV2(MyStructure):
    _fields_ = [
        ('Version', ctypes.c_uint32),
        ('Count', ctypes.c_uint32)
    ]


class ApiSetSchemaV2:

    def __init__(self, data):
        self._data = data
        self._entries = []
        header = StructApiSetNamespaceV2(self._data)
        self._version = header.Version

        self._load_entries(ctypes.sizeof(StructApiSetNamespaceV2), header.Count)

    @property
    def entries(self):
        return self._entries

    def _load_entries(self, offset, count):
        for i in range(count):
            entry_header = StructApiSetNamespaceEntryV2(
                self._data[offset:offset + ctypes.sizeof(StructApiSetNamespaceEntryV2)])

            entry_name = read_string(self._data, entry_header.NameOffset, entry_header.NameLength)
            entry_values = []

            data_offset = entry_header.DataOffset
            entry_value_header = StructApiSetValueEntryV2(
                self._data[data_offset:data_offset + ctypes.sizeof(StructApiSetValueEntryV2)])

            redirection_offset = ctypes.sizeof(StructApiSetValueEntryV2)
            for j in range(entry_value_header.NumberOfRedirections):
                entry_value_redirection_header = StructApiSetValueEntryRedirectionV2(
                    self._data[data_offset + redirection_offset:data_offset + redirection_offset + ctypes.sizeof(
                        StructApiSetValueEntryRedirectionV2)])

                entry_values.append(ApiSetNamespaceEntryValue(
                    name=read_string(self._data, entry_value_redirection_header.NameOffset,
                                     entry_value_redirection_header.NameLength),
                    value=read_string(self._data, entry_value_redirection_header.ValueOffset,
                                      entry_value_redirection_header.ValueLength)
                ))
                redirection_offset += ctypes.sizeof(StructApiSetValueEntryRedirectionV2)

            self._entries.append(ApiSetNamespaceEntry(name=entry_name, values=entry_values))

            offset += ctypes.sizeof(StructApiSetNamespaceEntryV2)
