# Description

Insert an image in the document, using the `image` or `img` block type. All image formats supported by PIL should work, but for now, the allowed types are: jpg, png, bmp, tiff, gif.

Inserting a vector image is also possible, just pass a PDF file and it should work seamlessly. Other vector formats are currently not supported, just convert them to PDF with Inkscape. If the provided pdf contains more than one page, only the first will be used.

By default, the image will be centered and resized using the width of the main frame of the current page template.

## Block types
- image: insert an image
- img: alias for `image`

## Optimization

As reportlab will probably build the document several times in order to satisfy the indexing items, a special optimization is currently used in order to include the actual graphics only at the last pass. Using a special block that has the exact same dimensions as the image, the intermediate builds are processed on empty space and the image is swapped at the last, final build. This trick allows to process the builds much faster.

However, if any problem occurs, it can be disabled within the plugin by the `renderOnLastBuild` property, just set it to `False` when loading the module:

```
type: module
id: core.modules.Image
args:
  renderOnLastBuild: no
```

# Usage
## Args
- path: path to the image file to load, can be relative or absolute

## Optional
- width: image width in cm, default is main frame width
- align: LEFT, CENTER, RIGHT, default is CENTER

# Example
```
type: image
path: flower.png
width: 8
align: LEFT
```
