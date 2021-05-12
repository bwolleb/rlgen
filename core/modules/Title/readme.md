# Description

Allows to insert a title in the document. Titles are just standard paragraphs with a few automation:

- Automatic style according to chapter level
- Automatic numbering (if wanted) according to chapter level
- Automatic bookmarking so the chapter can be referenced anywhere, if the module is loaded
- Automatic insertion of the chapter in the table of content if the module is loaded
- Dynamic resource where all chapter data can be found and used

Chapter levels begin at 0 and no level can be skipped: you can't insert a title level 0 and a title level 2 skipping level 1, but you can jump from a level x to a lower level at any time (see reportlab documentation for more details).

## Separators
By default, chapter levels are separated using dots and numbering is separated of the text using ". ", so the resulting displayed text is "1.2.3. My Chapter". Both are configurable as arg of the module:
- levelSep: "."
- numberingEnd: ". "

## Chapter resource
The module creates and maintain the `chapters` resource containing the following items:
- counters: list of integers keeping track of the current chapter numbering, for example [2, 3, 1] if the current chapter is 2.3.1
- id: map to all chapters of the document, this allows to access chapter data using its id
- current: dict of the current chapter, if any

Each chapter is stored as a dict containing the following items:
- text: Original text of the title
- id: identifier of the chapter
- level: level of the title, begins at 0
- number: numbering of the chapter level, for example the value is 4 for chapter 2.3.4
- fullnumber: full, displayable chapter numbering like 4.5.6
- fulltext: full, displayable chapter text like "1.2.3. My Chapter"

Currently, no block allows to manually manipulate the chapter counters, for example to reset them inside the document, but it is easy as changing the `chapters/counters` list content.

## Block types
- title: insert a title
- chapter: alias for `title`
- titleStyle: change the default chapter font styles

# Usage
## Insert a title
### Args
- text: Actual text of the title to insert

### Optional
- level: chapter level, begins at 0, default is 0
- id: identifier of the chapter, useful to reference anywhere in the document, default is a uid
- numbered: boolean to enable/disable numbereing, default is true

## Assign title styles
## Args
- style: font style(s) to use for the titles, can be:
  - a string, which is the identifier of an existing font style to use for the specified chapter level
  - a list of strings, where each one is the identifier of an existing font style to use for the corresponding chapter level, this syntax allows to define all styles at once
  - a dict, which defines a new font style in place using the [FontLoader](../FontLoader) syntax for the specified chapter level

### Optional
- level: specify level to assign the style to, mandatory if the `style` is a string or a dict

## Example
Insert a simple, level 0 chapter:
```
type: title
text: Introduction
```

Insert a level 1 chapter
```
type: chapter
text: The universe
level: 1
id: universeChap
```

Insert a level 1 chapter
```
type: chapter
text: The universe
level: 1
id: universeChap
```

Insert an unnumbered title, using title style of level 2
```
type: chapter
text: The planets
level: 2
numbered: no
```

Assign all title styles
```
type: titleStyle
style: [title1, title2, title3]
```

Change level 1 style
```
type: titleStyle
style: anotherStyle
level: 1
```

Define level 2 style in place
```
type: titleStyle
level: 2
style:
  font: Times-Roman
  name: awesomeStyle3
  size: 14
  align: left
  color: "ff0000"
```

Use the chapter resource system:
```
type: text
content: So we are now in chapter {{data(chapters/current/fulltext)}} which is the best one!
```
