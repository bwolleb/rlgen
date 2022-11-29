# Description

This hacky module is a POC for footnotes support, it is **not** considered stable. It works in a semi-manual way:

- Footnotes can be declared in their own `footnote` block, or within any `text` block (if loaded with `preprocess: [text]`). They should be simple text strings, but experimental support for generic blocks is implemented.
- Numbered footnotes can be referenced within text with the `fn` text processor (they must have a document-wide **unique** identifier for that).
- As they have to be drawn at render time, a special block is inserted in the flow. When those special blocks are processed (drawn via inside the reportlab internal loop) the footnote content is collected.
- When the page ends, all collected footnotes contents is inserted in a table which is drawn at the bottom of the page.
- There is a high risk that the table overlaps the actual content at the bottom of the page, a warning is printed if such a situation is detected, but with no guarantees. In this case, the content must be split and manually pushed to the next page using `newpage`.

There is no guarantee that a particular footnote appears on the same page where it is referenced within the text, but maybe this does not happen if all the overlapping warnings are fixed.

## Initialization

The module behavior and style of the footnotes is managed by internal variables that can be customized when the module is loaded (with module `args`) or anywhere in the document with the `set` command. However, changing the settings won't affect anything until rendering, so only the latest state is relevant. Changing the settings during render time could be implemented with a special block later. The following variables can be changed:

- `counting`: automatically count the footnotes, default is true
- `width`: footnotes table width in cm, if None the frame width is used
- `maxHeight`: maximum height of the table in cm, if None it is set to half of the width
- `x`: x position of the table from the left border of the page in cm, if None the frame postion is used
- `y`: y position of the table from the bottom border of the page in cm, default is 1
- `font`: font to use to render numbers and text, if None the default style is used
- `counterWidth`: width of the counter column in cm, default is 5mm
- `numFormat`: format string of the counter (within the table), default is "<para align='right'>{num}. </para>"
- `inlineFormat`: format string of the text processor, default is "[{num}]"
- `preprocess`: list of block types to preprocess (look for `fn`, `notes`, `footnotes`, `note`), disable this if you don't use the footnote keyword within other blocks, default is [text, txt]
- `warnOverlap`: print a warning in the console during rendering if an overlap is detected (not bulletproof!), default is true
- `style`: reportlab table style for the footnote table, see sources for the defaults

## Block types
- footnote: insert a footnote on the current page
- fn: alias for footnote

# Usage
## Args
- content: actual content of the footnote, should be plain text but can also be a block or a list of blocks

## Optional
- id: footnote identifier to use within text

# Examples
Create a (anonymous) footnote on the current page:
```
- type: fn
  content: My first footnote
```

Create a footnote within a text block and reference it:
```
- type: text
  content: In the first {{fn(casRoy)}} James bond movie starring Daniel Craig, ...
  notes:
    casRoy: Casino Royale, Martin Campbell, 2006
```

Load footnote module and set the counter formatting to "num) " instead of the default "num. ". Also set the font to the newly declared `fn` style:
```
- type: font
  font: Times-Roman
  name: fn
  size: 10
  align: left
  color: "9e0299"

- type: module
  id: extra.Footnotes
  args:
    font: fn
    numFormat: "<para align='right'>{num}) </para>"
```
