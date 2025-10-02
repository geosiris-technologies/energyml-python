<!--
Copyright (c) 2022-2023 Geosiris.
SPDX-License-Identifier: Apache-2.0
-->
energyml-utils
==============

[![PyPI version](https://badge.fury.io/py/energyml-utils.svg)](https://badge.fury.io/py/energyml-utils)
[![License](https://img.shields.io/pypi/l/energyml-utils)](https://github.com/geosiris-technologies/geosiris-technologies/blob/main/energyml-utils/LICENSE)
[![Documentation Status](https://readthedocs.org/projects/geosiris-technologies/badge/?version=latest)](https://geosiris-technologies.readthedocs.io/en/latest/?badge=latest)
![Python version](https://img.shields.io/pypi/pyversions/energyml-utils)
![Status](https://img.shields.io/pypi/status/energyml-utils)




Installation
------------

energyml-utils can be installed with pip : 

```console
pip install energyml-utils
```

or with poetry: 
```console
poetry add energyml-utils
```


Features
--------

### Supported packages versions

This package supports read/write in xml/json the following packages : 
- EML (common) : 2.0, 2.1, 2.2, 2.3
- RESQML : 2.0.1, 2.2dev3, 2.2
- WITSMl : 2.0, 2.1
- PRODML : 2.0, 2.2

/!\\ By default, these packages are not installed and are published independently.
You can install only the versions you need by adding the following lines in the .toml file : 
```toml
energyml-common2-0 = "^1.12.0"
energyml-common2-1 = "^1.12.0"
energyml-common2-2 = "^1.12.0"
energyml-common2-3 = "^1.12.0"
energyml-resqml2-0-1 = "^1.12.0"
energyml-resqml2-2-dev3 = "^1.12.0"
energyml-resqml2-2 = "^1.12.0"
energyml-witsml2-0 = "^1.12.0"
energyml-witsml2-1 = "^1.12.0"
energyml-prodml2-0 = "^1.12.0"
energyml-prodml2-2 = "^1.12.0"
```

### Content of the package :

- Support EPC + h5 read and write
  - *.rels* files are automatically generated, but it is possible to add custom Relations.
  - You can add "raw files" such as PDF or anything else, in your EPC instance, and it will be package with other files in the ".epc" file when you call the "export" function.
  - You can work with local files, but also with IO (BytesIO). This is usefull to work with cloud application to avoid local storage.
- Supports xml / json read and write (for energyml objects)
- *Work in progress* : Supports the read of 3D data inside the "AbstractMesh" class (and sub-classes "PointSetMesh", "PolylineSetMesh", "SurfaceMesh"). This gives you a instance containing a list of point and a list of indices to easily re-create a 3D representation of the data.
  -  These "mesh" classes provides *.obj*, *.off*, and *.geojson* export.
- Introspection : This package includes functions to ease the access of specific values inside energyml objects.
  - Functions to access to UUID, object Version, and more generic functions for any other attributes with regex like ".Citation.Title" or "Cit\\.*.Title" (regular dots are used as in python object attribute access. To use dot in regex, you must escape them with a '\\')
  - Functions to parse, or generate from an energyml object the "ContentType" or "QualifiedType"
  - Generation of random data : you can generate random values for a specific energyml object. For example, you can generate a WITSML Tubular object with random values in it.
- Objects correctness validation :
  - You can verify if your objects are valid following the energyml norm (a check is done on regex contraint attributes, maxCount, minCount, mandatory etc...)
  - The DOR validation is tested : check if the DOR has correct information (title, ContentType/QualifiedType, object version), and also if the referenced object exists in the context of the EPC instance (or a list of object).
- Abstractions done to ease use with *ETP* (Energistics Transfer Protocol) :
  - The "EnergymlWorkspace" class allows to abstract the access of numerical data like "ExternalArrays". This class can thus be extended to interact with ETP "GetDataArray" request etc...
- ETP URI support : the "Uri" class allows to parse/write an etp uri.

## EPC Stream Reader

The **EpcStreamReader** provides memory-efficient handling of large EPC files through lazy loading and smart caching. Unlike the standard `Epc` class which loads all objects into memory, the stream reader loads objects on-demand, making it ideal for handling very large EPC files with thousands of objects.

### Key Features

- **Lazy Loading**: Objects are loaded only when accessed, reducing memory footprint
- **Smart Caching**: LRU (Least Recently Used) cache with configurable size  
- **Automatic EPC Version Detection**: Supports both CLASSIC and EXPANDED EPC formats
- **Add/Remove/Update Operations**: Full CRUD operations with automatic file structure maintenance
- **Context Management**: Automatic resource cleanup with `with` statements
- **Memory Monitoring**: Track cache efficiency and memory usage statistics

### Basic Usage

```python
from energyml.utils.epc_stream import EpcStreamReader

# Open EPC file with context manager (recommended)
with EpcStreamReader('large_file.epc', cache_size=50) as reader:
    # List all objects without loading them
    print(f"Total objects: {reader.stats.total_objects}")
    
    # Get object by identifier
    obj: Any = reader.get_object_by_identifier("uuid.version")
    
    # Get objects by type
    features: List[Any] = reader.get_objects_by_type("BoundaryFeature")
    
    # Get all objects with same UUID
    versions: List[Any] = reader.get_object_by_uuid("12345678-1234-1234-1234-123456789abc")
```

### Adding Objects

```python
from energyml.utils.epc_stream import EpcStreamReader
from energyml.utils.constants import gen_uuid
import energyml.resqml.v2_2.resqmlv2 as resqml
import energyml.eml.v2_3.commonv2 as eml

# Create a new EnergyML object
boundary_feature = resqml.BoundaryFeature()
boundary_feature.uuid = gen_uuid()
boundary_feature.citation = eml.Citation(title="My Feature")

with EpcStreamReader('my_file.epc') as reader:
    # Add object - path is automatically generated based on EPC version
    identifier = reader.add_object(boundary_feature)
    print(f"Added object with identifier: {identifier}")
    
    # Or specify custom path (optional)
    identifier = reader.add_object(boundary_feature, "custom/path/MyFeature.xml")
```

### Removing Objects

```python
with EpcStreamReader('my_file.epc') as reader:
    # Remove specific version by full identifier
    success = reader.remove_object("uuid.version")
    
    # Remove ALL versions by UUID only
    success = reader.remove_object("12345678-1234-1234-1234-123456789abc")
    
    if success:
        print("Object(s) removed successfully")
```

### Updating Objects

```python
...
from energyml.utils.introspection import set_attribute_from_path

with EpcStreamReader('my_file.epc') as reader:
    # Get existing object
    obj = reader.get_object_by_identifier("uuid.version")
    
    # Modify the object
    set_attribute_from_path(obj, "citation.title", "Updated Title")
    
    # Update in EPC file
    new_identifier = reader.update_object(obj)
    print(f"Updated object: {new_identifier}")
```

### Performance Monitoring

```python
with EpcStreamReader('large_file.epc', cache_size=100) as reader:
    # Access some objects...
    for i in range(10):
        obj = reader.get_object_by_identifier(f"uuid-{i}.1")
    
    # Check performance statistics
    print(f"Cache hit rate: {reader.stats.cache_hit_rate:.1f}%")
    print(f"Memory efficiency: {reader.stats.memory_efficiency:.1f}%") 
    print(f"Objects in cache: {reader.stats.loaded_objects}/{reader.stats.total_objects}")
```

### EPC Version Support

The EpcStreamReader automatically detects and handles both EPC packaging formats:

- **CLASSIC Format**: Flat file structure (e.g., `obj_BoundaryFeature_{uuid}.xml`)
- **EXPANDED Format**: Namespace structure (e.g., `namespace_resqml201/version_{id}/obj_BoundaryFeature_{uuid}.xml` or `namespace_resqml201/obj_BoundaryFeature_{uuid}.xml`)

```python
with EpcStreamReader('my_file.epc') as reader:
    print(f"Detected EPC version: {reader.export_version}")
    # Objects added will use the same format as the existing EPC file
```

### Advanced Usage

```python
# Initialize without preloading metadata for faster startup
reader = EpcStreamReader('huge_file.epc', preload_metadata=False, cache_size=200)

try:
    # Manual metadata loading when needed
    reader._load_metadata()
    
    # Get object dependencies
    deps = reader.get_object_dependencies("uuid.version")
    
    # Batch processing with memory monitoring
    for obj_type in ["BoundaryFeature", "PropertyKind"]:
        objects = reader.get_objects_by_type(obj_type)
        print(f"Processing {len(objects)} {obj_type} objects")
        
finally:
    reader.close()  # Manual cleanup if not using context manager
```

The EpcStreamReader is perfect for applications that need to work with large EPC files efficiently, such as data processing pipelines, web applications, or analysis tools where memory usage is a concern.


# Poetry scripts : 

- extract_3d : extract a representation into an 3D file (obj/off)
- csv_to_dataset : translate csv data into h5 dataset
- generate_data : generate a random data from a qualified_type 
- xml_to_json : translate an energyml xml file into json.
- json_to_xml : translate an energyml json file into an xml file
- describe_as_csv : create a csv description of an EPC content
- validate : validate an energyml object or an EPC instance (or a folder containing energyml objects)



## Installation to test poetry scripts : 

```bash
poetry install
```

if you fail to run a script, you may have to add "src" to your PYTHONPATH environment variable. For example, in powershell : 

```powershell
$env:PYTHONPATH="src"
```


## Validation examples : 

An epc file:
```bash
poetry run validate --file "path/to/your/energyml/object.epc" *> output_logs.json
```

An xml file:
```bash
poetry run validate --file "path/to/your/energyml/object.xml" *> output_logs.json
```

A json file:
```bash
poetry run validate --file "path/to/your/energyml/object.json" *> output_logs.json
```

A folder containing Epc/xml/json files:
```bash
poetry run validate --file "path/to/your/folder" *> output_logs.json
```

