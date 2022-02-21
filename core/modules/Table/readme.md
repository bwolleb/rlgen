# Description

Insert a table in the document. This module is one of the most versatile blocks available: the column sizes and style can all be customized using the inner reportlab TableStyle syntax. Each cells of a table can contain a single text, a block, or a list of blocks to build and insert directly in the cell frame. Tables can be nested without problem.

By default, a table is aligned on the left of the page, all its cells have a top-left alignment, with a 0.5 pt black grid. The default header has a light gray background, if applicable. Each column has the same width and fill the available width of the main page style frame.

Keep in mind that a cell can not be split, so reportlab will crash if a cell is taller than the available frame height of the current page style.

## Block types
- table: insert a table

# Usage
## Args
- rows: actual content of the table, must be a list or the path to a resource which is a list. Then, each item of the list can be:
  - a list cells (see below)
  - an object where the `keys` are the columns and the value of each is a cell (see below)

### Cells
A cell can be either:
- a string, which will be built using the current default text style (see [Text](../Text))
- a block, which is built by the normal engine mechanism
- a list of blocks, which are built by the normal engine mechanism

## Optional
- keys: column keys, needed when rows are objects
- header: list of cells to insert in the first row, at the beginning of the table, with the default header style. This is 100% sugar syntax as the header could be specified in the `rows`.
- border: boolean, allows to hide the black grid, default is true
- widths: list of values to set the width of each column, by default each column has the same width and fill the available page width
- heights: list of values to set the height of each row, by default this value is automatically computed for each row according to the content of all cells. *Warning*: if this property is set, the number of rows is fixed and generation will crash if the data don't match.
- unit: set the unit of the column widths/heights, can be cm, mm or percent (of the current page style frame width), default is cm
- align: horizontal alignment of the table on the page, can be LEFT, CENTER or RIGHT, default is LEFT
- repeatRows: integer, tell the table to repeat n rows if the table is split over several pages
- style: list of objects to fully customize the inner TableStyle (border, padding, background, span, ...). Providing a custom style overrides the default style (cell alignment, grid, header). See reportlab doc for more information.

# Examples
Simple table:
```
type: table
header: [Col1, Col2, Col3]
rows:
  - [Hello, Amazing, World]
  - [Good, to see, You]
```

Using column objects, no header and custom widths:
```
type: table
widths: [20, 30, 20]
unit: percent
keys: [c1, c2, c3]
align: CENTER
rows:
  - id: 4333
    c2: my
    c1: Oh
    c3: god!
  - unusedProperty: asdfghjk
    c3: awesome!
    c2: is
    c1: It
  - c1: Here is
    c2: my photo:
    c3:
      type: image
      path: me.jpg
      width: 3
```

Rows from a resource, a custom style and a repeated header:
```
type: table
widths: [4, 5, 3]
unit: cm
header: [Col1, Col2, Col3]
keys: [c1, c2, c3]
align: CENTER
rows: testData/table1
repeatRows: 1
style:
  - [GRID, [0,0], [-1,-1], 0.5, ff0000]
  - [ALIGN, [2,2], [3,3], CENTER]
  - [BACKGROUND, [1,0], [1,-1], 0000ff]
```
