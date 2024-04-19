# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

class NotImplementedError(Exception):
    """Exception for not implemented functions"""

    def __init__(self, msg):
        super().__init__(msg)


class NoCrsError(Exception):
    pass

class ObjectNotFoundNotError(Exception):
    def __init__(self, obj_id):
        super().__init__(f"Object id: {obj_id}")