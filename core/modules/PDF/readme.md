# Description

Insert a whole PDF document or a page subset of it. Each page is drawn as is on the canvas, which is resized to the exact same dimension of the page being merged. Still, the rlgen callbacks work through the page insertion, so you may want to disable decorations or other things.

## Block types
- pdf: insert a whole pdf document or a subset within the current flow.

# Usage
## Optional
- pages: specify the page numbers to include as a list of integers.
- from: indicate the start of the page range to include
- to: indicate the end of the page range to include

**Warning**: these are "natural" indices: they start at 1!

## Example

Include all pages:
```
type: pdf
path: path/to/doc.pdf
```

Include a range:
```
type: pdf
path: path/to/doc.pdf
from: 3
to: 8
```

Include specific pages:
```
type: pdf
path: path/to/doc.pdf
pages: [2, 4, 1]
```
