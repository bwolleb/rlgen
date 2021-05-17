# rlgen
A non-WYSIWYG, customizable, highly sugary syntax, document generator inspired by [noWord](https://github.com/mmuellersk/noWord) (from which certain portions of code are taken) using reportlab as backend processor.

# Concept
Similarly to a LaTeX document, the engine uses plain text input instructions and generates a consistent PDF document. This allows to:

- Use the generator in a headless environment / scripts
- Easily keep track of the input files with versioning tools as they are structured plain text (git-able, commits, branches, pull-requests, etc)
- Easily split the document in several input files and `include` them in a flexible way to keep the document organized and clean
- Define include-able custom set of templates and styles that can be used in several documents, keeping a consistent look for all the documentation

The inputs to provide to the engine is a list of so-called `blocks`, which are simple key-value maps (python dicts). Each one has a `type` which will be recognized and processed by a [module](core/modules) and can archieve the following purposes:

- structural operations: configure engine, load modules, define page layouts, define font styles, ...
- actual document content: insert titles, text, tables, lists, images, ...

A set of [templates](core/modules/Template/templates) is provided that define the most common layouts and styles so that it is easy to create a simple document.

# Build process
The build process is done in two stages:

The "build" time when the engine processes a list of blocks using the available [modules](core/modules) and transforms them into reportlab blocks, called flowable objects.

The "render" time when the reportlab engine uses the flowable objects and generates the final PDF document. This is usually done several times so that the indexing items, such as the table of content, are up to date with all the document content (like a LaTeX document).

# Dependencies
To use it, you will need the following python packages:
- reportlab
- Pillow
- pdfrw
- pyaml
- python-dateutil
- python-magic

# Usage
The easiest way to use it is to run the `main.py` script, which has the following interface: `main.py src [dst]`

- src is your document entry point, which should be a yaml or json file. Yaml is preferred because it is the easiest human-editable structured format.
- dst is the path to the pdf to create, if nothing is provided, the file `document.pdf` will be created in the current directory.

Usually, the document entry point is a file that will include all the other document files. Look at the [demos](demo) and the [templates](core/modules/Template/templates) for examples on how to create a simple document.

The engine itself can also be easily used in any python script as the only required steps to generate a document are:
```
e = engine.Engine() # Instanciate the engine
build = e.processBlocks(blocks, "/path/to/document/working/dir") # Feed blocks
e.build(build, "/path/to/pdf/to/generate") # Generate PDF
```

# Document structure
As demonstrated by the [demos](demo), the document structure to feed to the engine should be:

- load desired modules
- define page layout(s) available in the document
- define font styles available in the document
- define page decorations if desired
- set default font styles for the paragraphs, titles, table of contents
- set document metadata
- insert actual content

Which is easy to split in multiple files using the `include` mechanism.

# Available blocks
Currently, all the following block types can be used:

- [absolute](core/modules/Absolute): draw block in absolute position instead of inserting it in the document flow
- [appendFrame](core/modules/FixedFrame): add blocks to an existing frame
- [bookmark](core/modules/Bookmark): create a bookmark that references this document position, can be used to jump to any particular position with a link
- [chapter](core/modules/Title): alias for `title`
- [data](core/modules/Resource): set provided data as resource
- [decoration](core/modules/Decorator): define a new decoration
- [disableDecoration](core/modules/Decorator): stop decorating the document with specified decoration
- [enableDecoration](core/modules/Decorator): start decorating the document with specified decoration from this point (repeatable)
- [exec](core/modules/Exec): run python code on the fly, even build drawable reportlab blocks
- [font](core/modules/FontLoader): create a new font style
- [frame](core/modules/FixedFrame): define the frame and build contained blocks
- [function](core/modules/Exec): define a new block processor that will be used on certain block types, just like normal modules
- [hspace](core/modules/Spacer): insert a horizontal space
- [if](core/modules/Condition): insert a conditional block
- [image](core/modules/Image): insert an image
- [img](core/modules/Image): alias for `image`
- [include](core/modules/Include): include file content or a whole folder, can be recursive
- [line](core/modules/Line): insert a horizontal line
- [list](core/modules/Line): insert a bullet or numbered list
- [loop](core/modules/Loop): loop over a resource and render blocks at each iteration
- [meta](core/modules/Metadata): set metadata of the generated PDF document
- [module](core/modules/ModuleLoader): load module, set module attributes or call module method
- [newpage](core/modules/NewPage): insert a page break, using current page style or a custom one
- [page](core/modules/PageStyle): define a new page style
- [pagestyle](core/modules/PageStyle): set initial default page style
- [paint](core/modules/Painter): draw something directly on canvas in python
- [qr](core/modules/QRCode): insert a QR code in the document
- [resource](core/modules/Resource): load a json, yaml or csv file as resource
- [space](core/modules/Spacer): insert a space, both horizontal and vertical
- [table](core/modules/Table): insert a table
- [template](core/modules/Template): load a predefined template
- [vspace](core/modules/Spacer): insert a vertical space
- [text](core/modules/Text): insert a paragraph
- [txt](core/modules/Text): alias for `txt`
- [textstyle](core/modules/Text): change default font to use from this point
- [title](core/modules/Title): insert a title
- [titleFormat](core/module/Title): change title number formatting
- [titleNum](core/module/Title): change title level number format
- [titleStyle](core/modules/Title): change the default chapter font styles
- [tocEntry](core/modules/TocEntry): insert a manual entry in the table of contents

# Todo
- Add a plot block to insert data charts using matplotlib
- Allow to instanciate multiple module instances and call a specific one in a block
- Blocks to ease variable/resource manipulation (set, eval, remove, update dict, update list, ...)
- Moar blocks: square, link area, line, arc, shape, circle, barcode, qr code, ...
- Implement footnotes (currently not available in reportlab)
