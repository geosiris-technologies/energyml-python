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


## Validation examples : 

An epc file:
```bash
poetry run validate --input "path/to/your/energyml/object.epc" *> output_logs.json
```

An xml file:
```bash
poetry run validate --input "path/to/your/energyml/object.xml" *> output_logs.json
```

A json file:
```bash
poetry run validate --input "path/to/your/energyml/object.json" *> output_logs.json
```

A folder containing Epc/xml/json files:
```bash
poetry run validate --input "path/to/your/folder" *> output_logs.json
```
