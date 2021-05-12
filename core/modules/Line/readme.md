# Description

Draw a horizontal line. Without providing anything, insert a simple solid thin black line with the width of the frame of the current page template.

## Block types
- line: insert a horizontal line

# Usage
## Optional args
- width: specify width of the line, default is the frame of the current page template
- unit: unit to use for the width, can be cm, mm or percent (of the frame), default is cm
- color: default is black
- dashes: list of int that defines the dash pattern in reportlab format (see official doc), default is none (continuous line)
- thickness: in pt, default is 0.5
- rounded: round the caps, default is false
- align: LEFT, CENTER or RIGHT, default is CENTER

# Example
Simple line:

```
type: line
```

Fancy line

```
type: line
width: 12
color: ffbb00
dashes: [1, 2]
thickness: 1
rounded: yes
```
