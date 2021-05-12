# Description

This plugin allows to draw one block at an absolute position on the page. For now, it is only possible to draw one single object, if you need multiple objects, se plugin [FixedFrame](../FixedFrame).

## Block types
- absolute: draw block in absolute position instead of inserting it in the document flow

# Usage
## Args
- x: horizontal position in cm, from left of canvas
- y: vertical position in cm, from bottom of canvas
- content: list of blocks to draw

# Example
```
type: absolute
x: 8
y: 12
content:
  - type: text
    content: This is an absolute text
```
