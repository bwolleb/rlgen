# Description

Insert a blank space, pretty useful if blocks are too close. By default, the space unit is in pt, and the size is 12, which is usually sufficient to separate blocks.

## Block types
- vspace: insert a vertical space
- hspace: insert a horizontal space
- space: insert a space, both horizontal and vertical

# Usage
## Optional
- unit: set the spacing unit, can be cm, mm or percent (of the page), default is pt
- size: can be a single number, or a list of two numbers, which is the horizontal/vertical space of the spacer. This number is then multiplied by the unit. The default is 12.

## Example
Insert a simple 12 pt vertical space:
```
type: vspace
```

Insert a rectangular space in cm:
```
type: space
size: 2
unit: cm
```

Insert a big horizontal space in percent:
```
type: hspace
size: 20
unit: percent
```
