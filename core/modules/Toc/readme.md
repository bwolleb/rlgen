# Description

Insert a table of contents in the document. The table will collect and display all [TocEntry](../TocEntry) items inserted in the flow of the document, including titles (which automatically insert a toc entry when they are built). The style of each entry can be specified.

## Block types
- toc: insert a table of contents

# Usage
## Optional
- dotsMinLevel: tweak the reportlab TableOfContents object, according to the doc: Set dotsMinLevel to determine from which level on a line of dots should be drawn between the text and the page number. If dotsMinLevel is set to a negative value, no dotted lines are drawn. Default is 1.
- style: list of font styles to use for each entry level, each item if the list can be:
  - a string, which is the identifier of an existing font style to use for the corresponding entry level
  - a dict, which defines a new font style in place using the [FontLoader](../FontLoader) syntax for the corresponding entry level

## Example
Insert a table of contents:
```
type: toc
```

Insert a table of contents with a custom style:
```
type: toc
style: [title1, title2, title3]
```
