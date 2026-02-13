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
- **Relationship Management**: Automatic or manual .rels file updates with parallel processing support
- **External Data Arrays**: Read/write HDF5, Parquet, CSV arrays with intelligent file caching
- **Context Management**: Automatic resource cleanup with `with` statements
- **Memory Monitoring**: Track cache efficiency and memory usage statistics

### Basic Usage

```python
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode

# Open EPC file with context manager (recommended)
with EpcStreamReader('large_file.epc', 
                     cache_size=50,
                     rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE) as reader:
    # List all objects without loading them
    print(f"Total objects: {len(reader)}")
    
    # Get object by identifier
    obj = reader.get_object("uuid.version")
    
    # List objects by type (returns metadata, not full objects)
    features = reader.list_objects(object_type="BoundaryFeature")
    print(f"Found {len(features)} features")
    
    # Get all objects with same UUID
    versions = reader.get_object_by_uuid("12345678-1234-1234-1234-123456789abc")
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
    # Remove by full identifier
    success = reader.delete_object("uuid.version")
    
    # Or use the alias
    success = reader.remove_object("uuid.version")
    
    if success:
        print("Object removed successfully")
```

### Updating Objects

```python
from energyml.utils.epc_stream import EpcStreamReader
from energyml.utils.introspection import set_attribute_from_path

with EpcStreamReader('my_file.epc') as reader:
    # Get existing object
    obj = reader.get_object("uuid.version")
    
    # Modify the object
    set_attribute_from_path(obj, "citation.title", "Updated Title")
    
    # Update in EPC file
    new_identifier = reader.put_object(obj)
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

### Relationship Management

```python
from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode

# Choose relationship update strategy
with EpcStreamReader('my_file.epc', 
                     rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE,
                     enable_parallel_rels=True) as reader:
    
    # Add/modify objects - rels updated automatically based on mode
    reader.add_object(my_object)
    
    # Manual rebuild of all relationships (e.g., after bulk operations)
    stats = reader.rebuild_all_rels(clean_first=True)
    print(f"Rebuilt {stats['rels_files_created']} .rels files")
```

### External Data Arrays

```python
import numpy as np

with EpcStreamReader('my_file.epc') as reader:
    # Read array from HDF5/Parquet/CSV
    data = reader.read_array(
        proxy=my_representation,
        path_in_external="/geometry/points"
    )
    
    # Write array to external file
    new_data = np.array([[1, 2, 3], [4, 5, 6]])
    success = reader.write_array(
        proxy=my_representation,
        path_in_external="/geometry/points",
        array=new_data
    )
    
    # Get metadata without loading full array
    metadata = reader.get_array_metadata(my_representation)
    print(f"Array shape: {metadata.dimensions}, dtype: {metadata.array_type}")
```

### Advanced Usage

```python
# Initialize with persistent ZIP connection for better performance
reader = EpcStreamReader('huge_file.epc', 
                         keep_open=True,
                         cache_size=200,
                         enable_parallel_rels=True,
                         parallel_worker_ratio=10)

try:
    # Get object dependencies
    deps = reader.get_object_dependencies("uuid.version")
    
    # Batch processing with memory monitoring
    for obj_type in ["BoundaryFeature", "PropertyKind"]:
        obj_list = reader.list_objects(object_type=obj_type)
        print(f"Processing {len(obj_list)} {obj_type} objects")
        
        for metadata in obj_list:
            obj = reader.get_object(metadata.identifier)
            # Process object...
        
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



## Poetry Script Examples : 

### Validation

Validate an EPC file:
```bash
poetry run validate --file "path/to/your/energyml/object.epc" *> output_logs.json
```

Validate an XML file:
```bash
poetry run validate --file "path/to/your/energyml/object.xml" *> output_logs.json
```

Validate a JSON file:
```bash
poetry run validate --file "path/to/your/energyml/object.json" *> output_logs.json
```

Validate a folder containing EPC/XML/JSON files:
```bash
poetry run validate --file "path/to/your/folder" *> output_logs.json
```

Ignore specific error types (e.g., INFO):
```bash
poetry run validate --file "path/to/file.epc" --ignore-err-type INFO *> output_logs.json
```

Group errors by their class for better organization:
```bash
poetry run validate --file "path/to/file.epc" --group-by-err-class *> output_logs.json
```

Include PRODML version errors in validation (by default they are ignored):
```bash
poetry run validate --file "path/to/file.epc" --ignore-prodml-version-errs *> output_logs.json
```

Combined example with multiple options:
```bash
poetry run validate --file "path/to/file.epc" -i INFO WARNING --group-by-err-class *> output_logs.json
```

### Extract 3D Representations

Extract all representations from an EPC to OBJ files:
```bash
poetry run extract_3d --epc "path/to/file.epc" --output "output_folder"
```

Extract specific representations by UUID:
```bash
poetry run extract_3d --epc "path/to/file.epc" --output "output_folder" --uuid "uuid1" "uuid2"
```

Extract to OFF format without CRS displacement:
```bash
poetry run extract_3d --epc "path/to/file.epc" --output "output_folder" --file-format OFF --no-crs
```

### CSV to Dataset

Convert CSV to HDF5:
```bash
poetry run csv_to_dataset --csv "data.csv" --output "output.h5"
```

Convert CSV to Parquet with custom delimiter:
```bash
poetry run csv_to_dataset --csv "data.csv" --output "output.parquet" --csv-delimiter ";"
```

With dataset name prefix:
```bash
poetry run csv_to_dataset --csv "data.csv" --output "output.h5" --prefix "/my/path/"
```

With column mapping (JSON file):
```bash
poetry run csv_to_dataset --csv "data.csv" --output "output.h5" --mapping "mapping.json"
```

With inline column mapping:
```bash
poetry run csv_to_dataset --csv "data.csv" --output "output.h5" --mapping-line '{"DATASET_A": ["COL1", "COL2"], "DATASET_B": ["COL3"]}'
```

### Generate Random Data

Generate a random RESQML object in JSON:
```bash
poetry run generate_data --type "energyml.resqml.v2_2.resqmlv2.TriangulatedSetRepresentation" --file-format json
```

Generate a random object in XML:
```bash
poetry run generate_data --type "energyml.resqml.v2_0_1.resqmlv2.Grid2dRepresentation" --file-format xml
```

Using qualified type:
```bash
poetry run generate_data --type "resqml22.WellboreFeature" --file-format json
```

### XML to JSON Conversion

Convert an XML file to JSON:
```bash
poetry run xml_to_json --file "path/to/object.xml"
```

Convert with custom output path:
```bash
poetry run xml_to_json --file "path/to/object.xml" --out "output.json"
```

Convert entire EPC to JSON array:
```bash
poetry run xml_to_json --file "path/to/file.epc" --out "output.json"
```

### JSON to XML Conversion

Convert a JSON file to XML:
```bash
poetry run json_to_xml --file "path/to/object.json"
```

Convert with custom output directory:
```bash
poetry run json_to_xml --file "path/to/object.json" --out "output_folder/"
```

### Describe as CSV

Generate a CSV description of all objects in a folder:
```bash
poetry run describe_as_csv --folder "path/to/folder"
```

With custom columns:
```bash
poetry run describe_as_csv --folder "path/to/folder" \
  --columnsNames "Title" "Type" "UUID" \
  --columnsValues "citation.title" "$qualifiedType" "Uuid"
```

Available special values for columnsValues:
- `$type`: Object Python type
- `$qualifiedType`: EnergyML qualified type
- `$contentType`: EnergyML content type
- `$path`: File path
- `$dor`: UUIDs of referenced objects

