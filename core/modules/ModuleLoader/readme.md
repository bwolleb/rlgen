# Description

This module is responsible to load the other modules, or run special instructions on loaded modules. It is the only one directly created by the engine. When loading a module, it is possible to pass arguments using the `arg` for the modules which support it.

A module is loaded using importlib on the default python path, which can be extended. If a module is already loaded, a warning is displayed, but the new instance will replace the old one. This behavior may be changed in the future to allow multipl instances of a module, if it is needed.

Using the `set` and `call` keys, it is also possible to change attributes and call methods of a loaded module.

## Block types
- module: load module, set module attributes or call module method

# Usage
## Args
- id: module to load from the current pathon path

## Optional
- path: extend python path
- args: dict of args to pass to the module constructor, for the ones which support it
- set: change attribute of a loaded module
- call: call mthod of a loaded module
- data: data to set in the `set` attribute, or passed to the method of `call`

## Example
Load the [Toc](../Toc) module:
```
type: module
id: core.modules.Toc
```

Use a custom path:
```
type: module
id: mycompany.docs.SpecialBlock
path: /data/templates
```

Load [Image](../Image) module disabling the optimization:
```
type: module
id: core.modules.Image
args:
  renderOnLastBuild: no
```

Set property of a module at build time:
```
type: module
id: core.modules.BladeRunner
set: deckard
data: replicant
```

Call method of a module at build time:
```
type: module
id: core.modules.StarWars
call: order
data: 66
```
