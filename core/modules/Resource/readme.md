# Description

This module allows to load data in the available resources.

The name of the new resource to insert in the `engine.resources` dict must be specified in `alias`. If the resource already exists, an error is displayed and the resource is not overridden.

By default, resources are inserted at the root of the `engine.resources` dict, but it is possible to load them in a sub dict if a prefix is provided as argument to the module:
```
type: module
id: core.modules.Resource
args:
  prefix: otherData
```

Currently, json, yaml and csv files are supported. All are loaded in UTF-8 (yes, this is the encoding you should use too!). When loading a CSV file, the delimiter is guessed from the first lines, and a list is returned.

## Block types
- resource: load a json, yaml or csv file as resource
- data: set provided data as resource

# Usage
## Load a data file
- alias: name of the resource to create
- path: path to the json, yaml or csv file to load, can be absolute or relative

## Set data in place
- alias: name of the resource to create
- data: data to insert, can be anything

## Example
Load file:
```
type: resource
alias: testData1
path: ../data1.json
```

Insert data:
```
type: data
alias: testData2
data:
  name: me
  lastname: myself
  age: 42
```
