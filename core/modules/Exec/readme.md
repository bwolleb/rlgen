# Description

This hacky module allows to run embedded code, either by running it immediately or by defining a custom block processor.

## Block types
- exec: run python code on the fly, even build drawable reportlab blocks
- function: define a new block processor that will be used on certain block types, just like normal modules (lazy you!) 

# Usage
## Exec block
The python code is directly run, and has access to the following items:

- engine: the main generator engine, which holds loaded modules, resources, fonts, ...
- path: the current path (useful if data must be loaded)
- utils: the `utils` lib
- build: empty list, items added to it are inserted to the document flow (and ar therefore expected to be reportlab objects / flowables)

### Args
- python: code to be run, can be multiline (see example)

## Function block
The python code is run each time specified block types are encountered, the available resources are almost the same:

- engine: the main generator engine, which holds loaded modules, resources, fonts, ...
- path: the current path (useful if data must be loaded)
- utils: the `utils` lib
- build: empty list, items added to it are inserted to the document flow (and ar therefore expected to be reportlab objects / flowables)
- block: the current block

### Args
- python: code to be run, can be multiline (see example)
- blockTypes: list of block types which will trigger the module

# Examples
## Exec block
```
type: exec
python: |
  utils.error("Warning, running dynamic code!")
  build = engine.processBlock({"type": "text", "content": "hello world"}, path)
```

## Function block
```
type: function
blockTypes: [loadtext]
python: |
  with open(block["file"]) as textfile:
    txt = textfile.read()
    txt.close()
    build = engine.processBlock({"type": "text", "content": txt}, path)
```
