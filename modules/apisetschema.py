import struct

import pefile as pefile

from modules import logger
from modules.apisetschema_v2 import ApiSetSchemaV2
from modules.apisetschema_v4 import ApiSetSchemaV4
from modules.apisetschema_v6 import ApiSetSchemaV6


class ApiSetSchema:

    def __init__(self, filename):
        self._version = 0
        self._count = 0
        self._api = None

        logger.log_info("Loading file: %s" % filename)
        self._filename = filename
        try:
            with open(filename, "rb") as f:
                self._data = f.read()
            if self._load():
                self._parse()
        except OSError as e:
            logger.log_err(e.strerror)

    @property
    def version(self):
        return self._version

    @property
    def count(self):
        return self._count

    @property
    def entries(self):
        return self._api.entries

    def _load(self):
        try:
            pe = pefile.PE(data=self._data, fast_load=True)
        except pefile.PEFormatError as e:
            logger.log_err(e.value)
            return False

        for section in pe.sections:
            if section.Name.decode('utf-8').strip("\x00") == ".apiset":
                self._data = self._data[section.PointerToRawData:section.SizeOfRawData]
                return True

        logger.log_err('No ".apiset" section found')
        return False

    def _parse(self):
        self._version = struct.unpack("B", self._data[0:1])[0]
        if self._version in [2,4,6]:
            if self._version == 0x6:
                self._api = ApiSetSchemaV6(self._data)
            elif self._version == 0x4:
                self._api = ApiSetSchemaV4(self._data)
            elif self._version == 0x2:
                self._api = ApiSetSchemaV2(self._data)
            self._count = len(self._api.entries)
            return True
        else:
            logger.log_err("Unknown ApiSetSchema version %d" % self._version)
            return False
