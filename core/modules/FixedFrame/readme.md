# Description

A bit similar to the [Absolute](../Absolute) module, this one allows to define a rectangle drawable area on the current page. This area behaves just like the normal drawing zone of the page: drawable blocks can be added to it and will be drawn one below each other.

## Block types
- frame: define the frame and build contained blocks
- appendFrame: add blocks to an existing frame

# Usage
## Define a frame
### Args
- x: horizontal position in cm, from left of canvas
- y: vertical position in cm, from bottom of canvas
- width: width of frame, in cm
- height: height of frame, in cm

### Optional
- content: list of blocks to build and add to the frame
- id: identifier of the frame, useful if `appendFrame` is called afterwards
- leftPadding: left padding in pt, default to 6
- bottomPadding: bottom padding in pt, default to 6
- rightPadding: right padding in pt, default to 6
- topPadding: top padding in pt, default to 6
- showBoundary: show a basic, solid, black border, default to 0 (disabled)
- border: specify a more complex border to draw around the frame (overrides `showBoundary`)

The border property can be:

- A float, in this case it defines the thickness of the black solid border
- A boolean, equivalent to `showBoundary: 1`
- An object that can have the following properties:
  - color: hex color, default is black
  - width: thickness of the boundary in pt, default is 0.5
  - dashes: list of int that defines the dash pattern in reportlab format (see official doc), default is none (continuous line)

## Append object to a frame
### Args
- id: identifier of the frame in which the objects has to be added
- content: list of blocks to build and add to the frame

# Example
Define a simple invisible frame
```
type: frame
x: 12
y: 15
width: 5
height: 5
content:
  - type: text
    content: I look like a floating text, but I am in a frame
```

A visible frame with a fancy border
```
type: frame
id: frm1
x: 12
y: 15
width: 5
height: 5
border:
  color: "0022aa"
  width: 1
  dashes: [1, 2]
content:
  - type: text
    content: Not really floating
```

Add an item to the frame:
```
type: appendFrame
id: frm1
content:
  - type: text
    content: Hello world
```
