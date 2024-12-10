# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from io import BytesIO
from typing import Optional, List, Any, Union


@dataclass
class DatasetReader:
    def read_array(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
        return None

    def get_array_dimension(self, source: Union[BytesIO, str], path_in_external_file: str) -> Optional[List[Any]]:
        return None


@dataclass
class ETPReader(DatasetReader):
    def read_array(self, obj_uri: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None

    def get_array_dimension(self, source: str, path_in_external_file: str) -> Optional[List[Any]]:
        return None
