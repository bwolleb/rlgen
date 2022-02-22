# Description

This module allows to define the font styles which can be used in the document. Defined fonts can then be set to be used automatically for titles, table of content sections, etc...

The native font can be specified by family name, then the system font will be used, or directly by providing the path to TTF files.

The first font style to be defined will be used as default by the [Text](../Text) module for all text fields, this can be overridden using the `default` argument (see below).

## Block types
- font: create a new font style

# Usage
## Args
- name: the name of the font style to define, using that name is the main way to use your font style in the document
- font: name of the system font family to use, if a TTF section is provided, the loaded font will be named using this field
- align: text alignment to use, can be `left`, `center`, `right` or `justify`
- color: hex color to use
- size: size of the font in pt

## Optional
- default: boolean, if true, set the new style as default font for all texts.

If using a custom font family which is not installed on the system, the `ttf` field can be used, it must contain paths to the files to load for the family:

- normal: path to normal TTF file
- bold: path to bold TTF file
- italic: path to italic TTF file
- boldItalic: path to bold/italic TTF font

All keys of reportlab ParagraphStyle.defaults dict can be specified:

- leading
- leftIndent
- rightIndent
- firstLineIndent
- spaceBefore
- spaceAfter

... and many more, see official documentation or reportlab sources.

## Hyphenation
If you want your text to automatically hyphenate words, you'll have to install the `pyphen` package, as it is the backend reportlab uses to hyphenate, and set the `hyphenationLang` property to one of the supported languages (from LibreOffice dictionnaries, see pyphen documentation) in the desired font style.

# Example
Simple black font:
```
type: font
font: Courier
name: default
size: 12
align: left
color: "000000"
```

Custom fancy font providing TTF:
```
type: font
font: western
name: western_big
size: 24
align: left
color: "6f4f28"
ttf:
  normal: western.ttf
  bold: western.ttf
  italic: western.ttf
  boldItalic: western.ttf
```
