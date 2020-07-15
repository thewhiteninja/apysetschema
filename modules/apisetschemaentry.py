class ApiSetNamespaceEntry:
    def __init__(self, name, values, flags=0):
        self._name = name
        self._values = values
        self._flags = flags

    @property
    def name(self):
        return self._name

    @property
    def flags(self):
        return self._flags

    @property
    def values(self):
        return self._values

    def __repr__(self):
        return '<%s flags="%d" name="%s" values="%d">' % (
            self.__class__.__name__, self._flags, self._name, len(self._values))


class ApiSetNamespaceEntryValue:
    def __init__(self, name, value, flags=0):
        self._name = name
        self._value = value
        self._flags = flags

    @property
    def name(self):
        return self._name

    @property
    def flags(self):
        return self._flags

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return '<%s flags="%d" name="%s" value="%s">' % (self.__class__.__name__, self._flags, self._name, self._value)
