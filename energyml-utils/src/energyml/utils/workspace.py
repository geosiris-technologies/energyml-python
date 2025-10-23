# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Any, Union

from energyml.utils.uri import Uri
import numpy as np


@dataclass
class EnergymlWorkspace:
    def get_object(self, uuid: str, object_version: Optional[str]) -> Optional[Any]:
        raise NotImplementedError("EnergymlWorkspace.get_object")

    def get_object_by_identifier(self, identifier: str) -> Optional[Any]:
        _tmp = identifier.split(".")
        return self.get_object(_tmp[0], _tmp[1] if len(_tmp) > 1 else None)

    def get_object_by_uuid(self, uuid: str) -> Optional[Any]:
        return self.get_object(uuid, None)

    # def read_external_array(
    #     self,
    #     energyml_array: Any,
    #     root_obj: Optional[Any] = None,
    #     path_in_root: Optional[str] = None,
    # ) -> List[Any]:
    #     raise NotImplementedError("EnergymlWorkspace.get_object")

    @abstractmethod
    def add_object(self, obj: Any) -> bool:
        raise NotImplementedError("EnergymlWorkspace.add_object")

    @abstractmethod
    def remove_object(self, identifier: Union[str, Uri]) -> None:
        raise NotImplementedError("EnergymlWorkspace.remove_object")

    @abstractmethod
    def read_array(self, proxy: Union[str, Uri, Any], path_in_external: str) -> Optional[np.ndarray]:
        raise NotImplementedError("EnergymlWorkspace.read_array")

    @abstractmethod
    def write_array(self, proxy: Union[str, Uri, Any], path_in_external: str, array: Any) -> bool:
        raise NotImplementedError("EnergymlWorkspace.write_array")
