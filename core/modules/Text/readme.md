# Description

Create a paragraph in the document. The inserted text will be formatted using the current default font if nothing is specified, but the `font` key can be used to customize it. Text items may be processed through [TextProcessors](../TextProcessor).

## Block types

- text: insert a paragraph
- txt: alias for `txt`
- textstyle: change default font to use

# Usage
## Insert text
### Args
- content: Text to write

### Optional
- font: font to use to build the paragraph. If a string is provided, it should reference the name of an existing font. If a dict is provided, a font style will be created and used for this paragraph, see [FontLoader](../FontLoader) for the syntax to use.

## Set default font
- name: identifier of the font style to set as default, the style must exist beforehands

## Example
Insert a paragraph using current default style:

```
type: text
content: Hello world!
```

Insert a paragraph using a defined custom font:

```
type: text
content: Hello solar system!
font: myfont2
```

Insert a paragraph using a custom font:

```
type: text
content: Hello galaxy!
font:
  font: Courier
  name: myfont3
  size: 12
  align: left
  color: "555555"
```

Set default font from now on:
```
type: textstyle
name: myfont3
```
