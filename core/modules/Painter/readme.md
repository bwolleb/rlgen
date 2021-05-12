# Description

This hacky module allows to directly draw on canvas. The reportlab canvas class is the low level interface that allows to draw shapes, text and other special elements on the PDF page, see reportlab documentation. This module is mainly useful to define a custom [decoration](../Decorator).

## Block types
- paint: draw something directly on canvas in python

# Usage
## Exec
The python code is directly run, and has access to the following items:

- engine: the main generator engine, which holds loaded modules, resources, fonts, ...
- path: the current path (useful if data must be loaded)
- canvas: the reportlab canvas
- utils: the `utils` lib
- cm: the centimeter unit, from `from reportlab.lib.units`, useful to draw in cm instead of native pt

## Args
- python: code to be run, can be multiline (see example)

# Examples
Draw a blue circle in the center of the page
```
type: paint
python : |
  canvas.setFillColor(utils.hexcolor("5555ee"))
  canvas.circle(10.5*cm, 2*cm, 1*cm, 0, 1)
```

Define a custom decoration that will print the page number in a blue square at the bottom left of each page;
```
type: decoration
items:
  - type: paint
    python : |
      canvas.setStrokeColor(utils.hexcolor("2222aa"))
      canvas.rect(0, 0, 1*cm, 1*cm, 1, 0)
  - type: text
    content: "{{data(build/pageNum)}}"
    font: footer
    x: 0
    y: 0.3
    width: 1
    height: 1
```
