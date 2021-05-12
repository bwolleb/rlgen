# Description

This module allows to define the page styles available in the document. A page style defines:

- The page dimensions (width, height)
- The frames, which are the drawing zones where the reportlab flowables will be inserted, one below the others

For example, the most standard page style is:

- A4 portrait, 21cm x 29.7cm
- One big central frame

The first page style to be defined will be used as default, this can be overridden using the `default` argument (see below) or using the `pagestyle` block.

## Block types
- page: define a new page style
- pagestyle: set default page style. *Warning* this only sets the initial page style at render time, so more than on block of this type is useless as only the last one will be deeterminent. To change page style within the document, see the [NewPage](../NewPage) module.

# Usage
## Define page style
### Args
- name: identifier of the page style which can be used later in the document in a [NewPage](../NewPage) for example
- size: the dimensions of the page, can be a string or a list of floats
  - when providing a string like "A4", it is loaded in the `reportlab.lib.pagesizes` package and an `orientation` can be used to specify it
  - When providing a list of floats, defines the page width and the page height in cm
- frames: list of drawing frames, each item should be an object defining the frame dimensions and position, see below

### Frames
Each frame can be defined on two ways. First is providing the raw dimnsions and position:
- x: horizontal position from the left of the page in cm
- y: vertical position from the bottom of the page in cm
- width: frame width in cm
- height: frame height in cm

Or providing the margins from the edges of the page:
- margin_left: distance to the left edge of the page in cm
- margin_right: distance to the right edge of the page in cm
- margin_top: distance to the top edge of the page in cm
- margin_bottom: distance to the bottom edge of the page in cm

The created frames have no internal padding.

### Optional
- orientation: either "portrait" or "landscape", can be used to define the orientation of a page size loaded from `reportlab.lib.pagesizes`
- default: boolean, if true, set the new style as default

## Set default page style
- name: identifier of the page style to set as default, the style must exist beforehands

# Examples
Simple A4 portrait page style:
```
type: page
name: a4_portrait
size: A4
orientation: portrait
frames:
  - margin_left: 2
    margin_right: 2
    margin_top: 2
    margin_bottom: 2
```

Custom dimensions with two columns:
```
type: page
name: custom_twocols
size: [37, 22.6]
frames:
  - x: 2
    y: 2
    width: 15.5
    height: 18.6
  - x: 19.5
    y: 2
    width: 15.5
    height: 18.6
```
