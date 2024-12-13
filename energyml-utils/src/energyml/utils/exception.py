# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from typing import Optional


class DetailedNotImplementedError(Exception):
    """Exception for not implemented functions"""

    def __init__(self, msg):
        super().__init__(msg)


class MissingExtraInstallation(DetailedNotImplementedError):
    """Exception for missing extra installation"""

    def __init__(self, extra_name):
        super().__init__(msg=f"Missing energml-utils extras installation '{extra_name}'")


class NoCrsError(Exception):
    pass


class ObjectNotFoundNotError(Exception):
    def __init__(self, obj_id):
        super().__init__(f"Object id: {obj_id}")


class UnknownTypeFromQualifiedType(Exception):
    def __init__(self, qt: Optional[str] = None):
        super().__init__(f"not matchable qualified type: {qt}")


class NotParsableType(Exception):
    def __init__(self, t: Optional[str] = None):
        super().__init__(f"type: {t}")


class UnparsableFile(Exception):
    def __init__(self, t: Optional[str] = None):
        super().__init__(f"File is not parsable for an EPC file. Please use RawFile class for non energyml files.")
