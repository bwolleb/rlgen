# Description

This module allows to define one or more decorations that will be drawn on pages.

## Decoration content
A decoration is the only object that will build objects during the rendering, which has several limitations but allows to use the `pageNum` and `pageTot` variables. 

Items on a decoration are built using the normal module system, but built blocks are not inserted in the document flow, they are drawn directly on the canvas, using absolute positions.

However, this is quite fragile and no check is performed on decoration items, so don't put stupid things in it (like a `newpage`).

## Decoration trigger
By default, a decoration is drawn as soon as it is defined, unconditionally on each page. This behavior can be altered in two ways:

- A decoration can be created and set to disabled, and then be manually enabled/disabled using the `enableDecoration` and `disableDecoration` blocks. This allows, for example, to simply use a decoration on each page except the first.

- A condition rule can be specified. Like the [Condition](../Condition) module, the (optional) condition is a boolean expression which is run using exec. It is checked each time the decoration is internally triggered (at the beginning or end of a page) and has access to build resources as locals. This is specifically designed to be able to draw custom decorations on certain page templates or page numbers. Think of a specific decoration for portrait/landscape or even/odd pages.

## Block types
- decoration: define a new decoration
- enableDecoration: start decorating the document with specified decoration from this point (repeatable)
- disableDecoration: stop decorating the document with specified decoration

# Usage
## Define a decoration
### Args
- items: List of blocks to build and draw

Each item is a normal block with additional absolute positioning coordinates:

- x: horizontal position in cm, from left of canvas
- y: vertical position in cm, from bottom of canvas
- width: width of the virtual zone where the item is drawn in cm
- height: height of the virtual zone where the item is drawn in cm

Having proper `width` and `height` values is mainly useful when drawing a centered text.

### Optional
- trigger: sepcify when the decoration must be checked and drawn. This field can be either `begin` or `end`, defaults to `begin`. This is rarely useful to override.
- expression: boolean expression to execute to fine-tune the decoration trigger. The default is none, a decoration is always drawn.
- enabled: boolean, allows to create a disabled decoration that can be manually enabled later
- id: give an identifier to the decoration, this is necessary to use the enable/disable mecanism

# Example
Simple centered decoration at the bottom of each page, showing "current / total" page numbers:
```
type: decoration
items:
  - type: text
    content: Page {{data(build/pageNum)}} / {{data(build/pageTot)}}
    font: footer
    x: 7
    y: 0.5
    width: 7
    height: 1
```

The same decoration defined only for landscape pages (having the `a4_landscape` template) and disabled by default:
```
type: decoration
id: landscape_pagenums
enabled: no
expression: pageTemplate == "a4_landscape"
items:
  - type: text
    content: page {{data(build/pageNum)}} / {{data(build/pageTot)}}
    font: footer
    x: 10
    y: 0.5
    width: 10
    height: 1
```
## Enable/disable a decoration
Enable the previously defined decoration:
```
type: enableDecoration
id: landscape_pagenums
```

Disable it:
```
type: disableDecoration
id: landscape_pagenums
```
